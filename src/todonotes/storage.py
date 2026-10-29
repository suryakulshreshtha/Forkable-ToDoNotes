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

import re
import sqlite3
from collections.abc import Iterator
from contextlib import closing, contextmanager
from datetime import datetime, timezone
from pathlib import Path

from todonotes.models import MARK_END, MARK_START, ChecklistItem, Note, SearchHit

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

# Full-text search index (FTS5). It is an "external content" table: it stores
# only the search index and reads the actual text from `notes`. The three
# triggers below are the pattern from the official FTS5 documentation and keep
# the index in step with every INSERT, UPDATE and DELETE on `notes`.
FTS_TABLE_SQL = """
CREATE VIRTUAL TABLE IF NOT EXISTS notes_fts USING fts5(
    title, body, content='notes', content_rowid='id', prefix='2 3'
);
"""
FTS_TRIGGERS_SQL = """
CREATE TRIGGER IF NOT EXISTS notes_ai AFTER INSERT ON notes BEGIN
    INSERT INTO notes_fts(rowid, title, body) VALUES (new.id, new.title, new.body);
END;
CREATE TRIGGER IF NOT EXISTS notes_ad AFTER DELETE ON notes BEGIN
    INSERT INTO notes_fts(notes_fts, rowid, title, body)
        VALUES ('delete', old.id, old.title, old.body);
END;
CREATE TRIGGER IF NOT EXISTS notes_au AFTER UPDATE ON notes BEGIN
    INSERT INTO notes_fts(notes_fts, rowid, title, body)
        VALUES ('delete', old.id, old.title, old.body);
    INSERT INTO notes_fts(rowid, title, body) VALUES (new.id, new.title, new.body);
END;
"""
FTS_TRIGGERS = ("notes_ai", "notes_ad", "notes_au")


def fts5_available() -> bool:
    """True if this Python's SQLite library was compiled with FTS5."""
    with closing(sqlite3.connect(":memory:")) as conn:
        try:
            conn.execute("CREATE VIRTUAL TABLE probe USING fts5(x)")
        except sqlite3.OperationalError:
            return False
    return True


def to_fts_query(text: str) -> str:
    """Turn what a person typed into a safe FTS5 query.

    Every word becomes a quoted prefix term, e.g. ``mil eg`` -> ``"mil"* "eg"*``.
    Quoting means characters like ``-``, ``:`` or ``(`` are treated as text,
    not as FTS5 operators, so no input can produce a syntax error.
    """
    terms = [word.replace('"', "") for word in text.split()]
    return " ".join(f'"{term}"*' for term in terms if term)


def _like_pattern(term: str) -> str:
    """Escape LIKE wildcards so a typed % or _ is matched literally."""
    escaped = term.replace("\\", "\\\\").replace("%", "\\%").replace("_", "\\_")
    return f"%{escaped}%"


def make_snippet(text: str, terms: list[str], width: int = 80) -> str:
    """Python fallback for FTS5's snippet(): a short window with marked matches."""
    if not text:
        return ""
    lowered = text.lower()
    positions = [lowered.find(t.lower()) for t in terms if t and t.lower() in lowered]
    start = max(0, min(positions) - width // 3) if positions else 0
    window = text[start : start + width]
    pattern = re.compile("|".join(re.escape(t) for t in terms if t), re.IGNORECASE)
    marked = pattern.sub(lambda m: f"{MARK_START}{m.group(0)}{MARK_END}", window)
    prefix = "…" if start > 0 else ""
    suffix = "…" if start + width < len(text) else ""
    return f"{prefix}{marked}{suffix}"


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
        self.fts_enabled = False

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
        self._ensure_search_index()

    def schema_version(self) -> int:
        with closing(self.connect()) as conn:
            return conn.execute("PRAGMA user_version").fetchone()[0]

    def _ensure_search_index(self) -> None:
        """Create (or safely disable) the FTS5 index, depending on this SQLite build.

        If a notes file created on a machine *with* FTS5 is opened on one
        *without* it, the triggers would make every write fail with
        "no such module: fts5". So in that case we drop the triggers and fall
        back to LIKE search; when FTS5 is available again we recreate them and
        rebuild the index from scratch.
        """
        with self._transaction() as conn:
            existing = {
                row[0]
                for row in conn.execute("SELECT name FROM sqlite_master WHERE type = 'trigger'")
            }
            if not fts5_available():
                for name in FTS_TRIGGERS:
                    if name in existing:
                        conn.execute(f"DROP TRIGGER {name}")  # name from our own tuple
                self.fts_enabled = False
                return
            conn.executescript(FTS_TABLE_SQL)
            if not set(FTS_TRIGGERS) <= existing:
                conn.executescript(FTS_TRIGGERS_SQL)
                conn.execute("INSERT INTO notes_fts(notes_fts) VALUES ('rebuild')")
            self.fts_enabled = True

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

    # --------------------------------------------------------------- search
    def search(self, text: str, limit: int = 50) -> list[SearchHit]:
        """Find notes whose title or body contain every typed word (as a prefix)."""
        terms = [word for word in text.split() if word.replace('"', "")]
        if not terms:
            return []
        if self.fts_enabled:
            return self._search_fts(to_fts_query(text), limit)
        return self._search_like(terms, limit)

    def _search_fts(self, query: str, limit: int) -> list[SearchHit]:
        with closing(self.connect()) as conn:
            rows = conn.execute(
                "SELECT notes.*, snippet(notes_fts, -1, ?, ?, '…', 12) AS snip"
                " FROM notes_fts JOIN notes ON notes.id = notes_fts.rowid"
                " WHERE notes_fts MATCH ? ORDER BY rank LIMIT ?",
                (MARK_START, MARK_END, query, limit),
            ).fetchall()
            hits = [SearchHit(note=_note_from_row(row), snippet=row["snip"]) for row in rows]
            self._attach_items(conn, [hit.note for hit in hits])
            return hits

    def _search_like(self, terms: list[str], limit: int) -> list[SearchHit]:
        condition = "(title LIKE ? ESCAPE '\\' OR body LIKE ? ESCAPE '\\')"
        clause = " AND ".join(condition for _ in terms)  # every word must match
        params: list[object] = []
        for term in terms:
            params += [_like_pattern(term), _like_pattern(term)]
        with closing(self.connect()) as conn:
            rows = conn.execute(  # `clause` is our fixed text; the words go as parameters
                f"SELECT * FROM notes WHERE {clause} ORDER BY updated_at DESC LIMIT ?",
                (*params, limit),
            ).fetchall()
            hits = []
            for row in rows:
                note = _note_from_row(row)
                in_body = any(term.lower() in note.body.lower() for term in terms)
                source = note.body if in_body else note.title
                hits.append(SearchHit(note=note, snippet=make_snippet(source, terms)))
            self._attach_items(conn, [hit.note for hit in hits])
            return hits
