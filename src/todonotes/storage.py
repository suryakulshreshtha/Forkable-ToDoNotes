"""SQLite storage — the only module in the app that speaks SQL.

Design rules used throughout this file:

* One short-lived connection per operation. SQLite opens in microseconds,
  and this sidesteps every "connection used from another thread" problem
  (the web server handles requests on several threads).
* ``with conn:`` wraps each write in a transaction: commit on success,
  rollback on error. It does NOT close the connection, so we also use
  ``contextlib.closing``.
* Values are always passed as ``?`` parameters, never formatted into SQL.
  That is what makes SQL injection impossible here.
* The schema version lives in ``PRAGMA user_version``; ``MIGRATIONS`` is an
  append-only list, so existing databases upgrade themselves on start-up.
"""

from __future__ import annotations

import sqlite3
from collections.abc import Iterator
from contextlib import closing, contextmanager
from datetime import datetime, timezone
from pathlib import Path

from todonotes.models import ChecklistItem, Note

# Each entry upgrades the schema by one version. Never edit an entry that has
# shipped; append a new one instead (see the Chapter 03 exercise).
MIGRATIONS: list[str] = [
    # v1 — notes and their checklist items
    """
    CREATE TABLE notes (
        id         INTEGER PRIMARY KEY AUTOINCREMENT,
        title      TEXT    NOT NULL DEFAULT '',
        body       TEXT    NOT NULL DEFAULT '',
        pinned     INTEGER NOT NULL DEFAULT 0 CHECK (pinned IN (0, 1)),
        created_at TEXT    NOT NULL,
        updated_at TEXT    NOT NULL
    );
    CREATE TABLE checklist_items (
        id       INTEGER PRIMARY KEY AUTOINCREMENT,
        note_id  INTEGER NOT NULL REFERENCES notes(id) ON DELETE CASCADE,
        text     TEXT    NOT NULL,
        done     INTEGER NOT NULL DEFAULT 0 CHECK (done IN (0, 1)),
        position INTEGER NOT NULL DEFAULT 0
    );
    CREATE INDEX idx_items_note ON checklist_items(note_id, position);
    """,
]


def utc_now() -> str:
    """Current time as an ISO 8601 string in UTC, to the second."""
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


def _note_from_row(row: sqlite3.Row) -> Note:
    return Note(
        id=row["id"],
        title=row["title"],
        body=row["body"],
        pinned=bool(row["pinned"]),
        created_at=row["created_at"],
        updated_at=row["updated_at"],
    )


def _item_from_row(row: sqlite3.Row) -> ChecklistItem:
    return ChecklistItem(
        id=row["id"],
        note_id=row["note_id"],
        text=row["text"],
        done=bool(row["done"]),
        position=row["position"],
    )


class NoteRepository:
    """Create, read, update and delete notes in one SQLite file."""

    def __init__(self, db_path: Path | str) -> None:
        self.db_path = Path(db_path)

    # ------------------------------------------------------------------ setup
    def connect(self) -> sqlite3.Connection:
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row  # rows behave like dicts: row["title"]
        conn.execute("PRAGMA foreign_keys = ON")  # off by default in SQLite!
        return conn

    @contextmanager
    def _transaction(self) -> Iterator[sqlite3.Connection]:
        with closing(self.connect()) as conn:
            with conn:  # commit on success, rollback on exception
                yield conn

    def initialize(self) -> None:
        """Create the file if needed and bring the schema up to date."""
        self.db_path.parent.mkdir(parents=True, exist_ok=True)
        with self._transaction() as conn:
            version = conn.execute("PRAGMA user_version").fetchone()[0]
            for number, script in enumerate(MIGRATIONS, start=1):
                if number > version:
                    conn.executescript(script)
                    # PRAGMA cannot take ? parameters; `number` is our own int.
                    conn.execute(f"PRAGMA user_version = {int(number)}")

    def schema_version(self) -> int:
        with closing(self.connect()) as conn:
            return conn.execute("PRAGMA user_version").fetchone()[0]

    # ------------------------------------------------------------------ notes
    def create_note(self, title: str = "", body: str = "", pinned: bool = False) -> Note:
        now = utc_now()
        with self._transaction() as conn:
            cursor = conn.execute(
                "INSERT INTO notes (title, body, pinned, created_at, updated_at)"
                " VALUES (?, ?, ?, ?, ?)",
                (title, body, int(pinned), now, now),
            )
            note_id = cursor.lastrowid
        note = self.get_note(note_id)
        assert note is not None
        return note

    def get_note(self, note_id: int) -> Note | None:
        with closing(self.connect()) as conn:
            row = conn.execute("SELECT * FROM notes WHERE id = ?", (note_id,)).fetchone()
            if row is None:
                return None
            note = _note_from_row(row)
            note.items = [
                _item_from_row(r)
                for r in conn.execute(
                    "SELECT * FROM checklist_items WHERE note_id = ? ORDER BY position, id",
                    (note_id,),
                )
            ]
            return note

    def list_notes(self) -> list[Note]:
        """All notes: pinned first, then most recently updated."""
        with closing(self.connect()) as conn:
            notes = [
                _note_from_row(row)
                for row in conn.execute(
                    "SELECT * FROM notes ORDER BY pinned DESC, updated_at DESC, id DESC"
                )
            ]
            self._attach_items(conn, notes)
            return notes

    def _attach_items(self, conn: sqlite3.Connection, notes: list[Note]) -> None:
        """Load checklist items for many notes with ONE query (avoids N+1 queries)."""
        by_id = {note.id: note for note in notes}
        if not by_id:
            return
        placeholders = ",".join("?" * len(by_id))  # "?,?,?" — values still go as parameters
        rows = conn.execute(
            f"SELECT * FROM checklist_items WHERE note_id IN ({placeholders})"
            " ORDER BY position, id",
            tuple(by_id),
        )
        for row in rows:
            by_id[row["note_id"]].items.append(_item_from_row(row))

    def update_note(
        self,
        note_id: int,
        *,
        title: str | None = None,
        body: str | None = None,
        pinned: bool | None = None,
    ) -> Note | None:
        """Change only the fields that are given; returns None if the note is gone."""
        changes: dict[str, object] = {}
        if title is not None:
            changes["title"] = title
        if body is not None:
            changes["body"] = body
        if pinned is not None:
            changes["pinned"] = int(pinned)
        changes["updated_at"] = utc_now()
        # Column names come from the fixed keys above, never from user input.
        assignments = ", ".join(f"{column} = ?" for column in changes)
        with self._transaction() as conn:
            cursor = conn.execute(
                f"UPDATE notes SET {assignments} WHERE id = ?", (*changes.values(), note_id)
            )
            if cursor.rowcount == 0:
                return None
        return self.get_note(note_id)

    def delete_note(self, note_id: int) -> bool:
        with self._transaction() as conn:
            cursor = conn.execute("DELETE FROM notes WHERE id = ?", (note_id,))
            return cursor.rowcount > 0

    def count_notes(self) -> int:
        with closing(self.connect()) as conn:
            return conn.execute("SELECT COUNT(*) FROM notes").fetchone()[0]

    # ------------------------------------------------------------ checklist
    def _touch(self, conn: sqlite3.Connection, note_id: int) -> None:
        conn.execute("UPDATE notes SET updated_at = ? WHERE id = ?", (utc_now(), note_id))

    def add_item(self, note_id: int, text: str) -> ChecklistItem | None:
        with self._transaction() as conn:
            if conn.execute("SELECT 1 FROM notes WHERE id = ?", (note_id,)).fetchone() is None:
                return None
            position = conn.execute(
                "SELECT COALESCE(MAX(position), -1) + 1 FROM checklist_items WHERE note_id = ?",
                (note_id,),
            ).fetchone()[0]
            cursor = conn.execute(
                "INSERT INTO checklist_items (note_id, text, position) VALUES (?, ?, ?)",
                (note_id, text, position),
            )
            self._touch(conn, note_id)
            item_id = cursor.lastrowid
        return self.get_item(item_id)

    def get_item(self, item_id: int) -> ChecklistItem | None:
        with closing(self.connect()) as conn:
            row = conn.execute("SELECT * FROM checklist_items WHERE id = ?", (item_id,)).fetchone()
            return _item_from_row(row) if row else None

    def set_item_done(self, item_id: int, done: bool) -> ChecklistItem | None:
        with self._transaction() as conn:
            row = conn.execute(
                "SELECT note_id FROM checklist_items WHERE id = ?", (item_id,)
            ).fetchone()
            if row is None:
                return None
            conn.execute("UPDATE checklist_items SET done = ? WHERE id = ?", (int(done), item_id))
            self._touch(conn, row["note_id"])
        return self.get_item(item_id)

    def delete_item(self, item_id: int) -> int | None:
        """Delete an item; returns its note id (handy for redirects) or None."""
        with self._transaction() as conn:
            row = conn.execute(
                "SELECT note_id FROM checklist_items WHERE id = ?", (item_id,)
            ).fetchone()
            if row is None:
                return None
            conn.execute("DELETE FROM checklist_items WHERE id = ?", (item_id,))
            self._touch(conn, row["note_id"])
            return row["note_id"]
