"""Business rules: what counts as a valid note, what the defaults are.

The service sits between the web layer and storage. It never sees HTTP and
never writes SQL, so every rule here can be unit-tested in milliseconds.
"""

from __future__ import annotations

from todonotes import APP_NAME, __version__
from todonotes.models import ChecklistItem, Note, SearchHit
from todonotes.storage import NoteRepository, utc_now

MAX_TITLE = 200
MAX_BODY = 100_000
MAX_ITEM = 500
MAX_QUERY = 200


class ValidationError(ValueError):
    """The input breaks a rule. The message is safe to show to the user."""


class NotFoundError(LookupError):
    """The requested note or checklist item does not exist."""


def _clean_text(value: str) -> str:
    """Normalise line endings (Windows sends \\r\\n) and strip trailing spaces."""
    return value.replace("\r\n", "\n").replace("\r", "\n").rstrip()


def _check_length(label: str, value: str, limit: int) -> None:
    if len(value) > limit:
        raise ValidationError(f"{label} is too long ({len(value):,} > {limit:,} characters).")


class NoteService:
    def __init__(self, repo: NoteRepository) -> None:
        self.repo = repo

    # ------------------------------------------------------------------ notes
    def create(self, title: str = "", body: str = "", pinned: bool = False) -> Note:
        title, body = title.strip(), _clean_text(body)
        _check_length("Title", title, MAX_TITLE)
        _check_length("Body", body, MAX_BODY)
        return self.repo.create_note(title=title, body=body, pinned=pinned)

    def get(self, note_id: int) -> Note:
        note = self.repo.get_note(note_id)
        if note is None:
            raise NotFoundError(f"Note {note_id} not found.")
        return note

    def list(self) -> list[Note]:
        return self.repo.list_notes()

    def update(
        self,
        note_id: int,
        *,
        title: str | None = None,
        body: str | None = None,
        pinned: bool | None = None,
    ) -> Note:
        if title is not None:
            title = title.strip()
            _check_length("Title", title, MAX_TITLE)
        if body is not None:
            body = _clean_text(body)
            _check_length("Body", body, MAX_BODY)
        note = self.repo.update_note(note_id, title=title, body=body, pinned=pinned)
        if note is None:
            raise NotFoundError(f"Note {note_id} not found.")
        return note

    def toggle_pin(self, note_id: int) -> Note:
        return self.update(note_id, pinned=not self.get(note_id).pinned)

    def delete(self, note_id: int) -> None:
        if not self.repo.delete_note(note_id):
            raise NotFoundError(f"Note {note_id} not found.")

    # ------------------------------------------------------------ checklist
    def add_item(self, note_id: int, text: str) -> ChecklistItem:
        text = " ".join(text.split())  # collapse newlines and runs of spaces
        if not text:
            raise ValidationError("A checklist item needs some text.")
        _check_length("Checklist item", text, MAX_ITEM)
        item = self.repo.add_item(note_id, text)
        if item is None:
            raise NotFoundError(f"Note {note_id} not found.")
        return item

    def set_item_done(self, item_id: int, done: bool) -> ChecklistItem:
        item = self.repo.set_item_done(item_id, done)
        if item is None:
            raise NotFoundError(f"Checklist item {item_id} not found.")
        return item

    def toggle_item(self, item_id: int) -> ChecklistItem:
        item = self.repo.get_item(item_id)
        if item is None:
            raise NotFoundError(f"Checklist item {item_id} not found.")
        return self.set_item_done(item_id, not item.done)

    def remove_item(self, item_id: int) -> int:
        """Delete an item and return the id of the note it belonged to."""
        note_id = self.repo.delete_item(item_id)
        if note_id is None:
            raise NotFoundError(f"Checklist item {item_id} not found.")
        return note_id

    # --------------------------------------------------------------- search
    def search(self, query: str) -> list[SearchHit]:
        query = " ".join(query.split())[:MAX_QUERY]
        return self.repo.search(query) if query else []

    # --------------------------------------------------------------- export
    def export_data(self) -> dict:
        """Everything, as plain JSON-ready data (a backup you can read)."""
        return {
            "app": APP_NAME,
            "version": __version__,
            "exported_at": utc_now(),
            "notes": [note.to_dict() for note in self.list()],
        }

    def export_markdown(self) -> str:
        """Everything as one Markdown document, checklists as GitHub task lists."""
        lines = [f"# {APP_NAME} export", "", f"_Exported {utc_now()}_", ""]
        for note in self.list():
            pin = " 📌" if note.pinned else ""
            lines += [f"## {note.display_title}{pin}", ""]
            if note.body:
                lines += [note.body, ""]
            for item in note.items:
                lines.append(f"- [{'x' if item.done else ' '}] {item.text}")
            if note.items:
                lines.append("")
            lines += [f"<sub>Updated {note.updated_at}</sub>", ""]
        return "\n".join(lines).rstrip() + "\n"
