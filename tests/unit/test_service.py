"""Chapter 04: the business rules, tested without HTTP or a browser."""

import json

import pytest

from todonotes.models import UNTITLED, Note
from todonotes.service import MAX_TITLE, NoteService, NotFoundError, ValidationError


def test_create_strips_title_and_normalises_newlines(service: NoteService) -> None:
    note = service.create(title="  Plan  ", body="line one\r\nline two\r\n\r\n")
    assert note.title == "Plan"
    assert note.body == "line one\nline two"


def test_title_length_is_limited(service: NoteService) -> None:
    with pytest.raises(ValidationError, match="Title is too long"):
        service.create(title="x" * (MAX_TITLE + 1))


@pytest.mark.parametrize(
    ("title", "body", "expected"),
    [
        ("Groceries", "milk", "Groceries"),
        ("", "\n\n  first real line \nsecond", "first real line"),
        ("", "", UNTITLED),
        ("", "y" * 80, "y" * 57 + "…"),
    ],
)
def test_display_title(title: str, body: str, expected: str) -> None:
    note = Note(id=1, title=title, body=body, pinned=False, created_at="", updated_at="")
    assert note.display_title == expected


def test_get_unknown_note_raises(service: NoteService) -> None:
    with pytest.raises(NotFoundError):
        service.get(404)


def test_update_and_toggle_pin(service: NoteService) -> None:
    note = service.create(title="a")
    assert service.update(note.id, body="new body").body == "new body"
    assert service.toggle_pin(note.id).pinned is True
    assert service.toggle_pin(note.id).pinned is False


def test_delete_unknown_note_raises(service: NoteService) -> None:
    with pytest.raises(NotFoundError):
        service.delete(7)


def test_add_item_collapses_whitespace(service: NoteService) -> None:
    note = service.create(title="t")
    assert service.add_item(note.id, "  buy\n  milk  ").text == "buy milk"


def test_empty_item_is_rejected(service: NoteService) -> None:
    note = service.create(title="t")
    with pytest.raises(ValidationError):
        service.add_item(note.id, "   ")


def test_toggle_item_flips_done(service: NoteService) -> None:
    note = service.create(title="t")
    item = service.add_item(note.id, "x")
    assert service.toggle_item(item.id).done is True
    assert service.toggle_item(item.id).done is False


def test_remove_item_returns_parent_note(service: NoteService) -> None:
    note = service.create(title="t")
    item = service.add_item(note.id, "x")
    assert service.remove_item(item.id) == note.id
    with pytest.raises(NotFoundError):
        service.remove_item(item.id)


def test_export_data_is_json_serialisable(service: NoteService) -> None:
    note = service.create(title="t", body="b")
    service.add_item(note.id, "x")
    data = json.loads(json.dumps(service.export_data()))
    assert data["app"] == "Forkable-ToDoNotes"
    assert data["notes"][0]["items"][0]["text"] == "x"


def test_export_markdown_uses_task_lists(service: NoteService) -> None:
    note = service.create(title="Trip", body="Pack light", pinned=True)
    done = service.add_item(note.id, "passport")
    service.add_item(note.id, "charger")
    service.toggle_item(done.id)
    text = service.export_markdown()
    assert "## Trip 📌" in text
    assert "- [x] passport" in text
    assert "- [ ] charger" in text
