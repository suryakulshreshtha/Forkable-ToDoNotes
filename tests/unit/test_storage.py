"""Chapter 03: the SQLite repository stores and returns exactly what it was given."""

import sqlite3
import time

from todonotes.storage import MIGRATIONS, NoteRepository


def test_initialize_creates_file_and_sets_schema_version(repo: NoteRepository) -> None:
    assert repo.db_path.exists()
    assert repo.schema_version() == len(MIGRATIONS)


def test_initialize_twice_is_safe(repo: NoteRepository) -> None:
    repo.create_note(title="keep me")
    repo.initialize()  # must not re-run migrations or lose data
    assert repo.count_notes() == 1


def test_create_and_get_round_trip(repo: NoteRepository) -> None:
    created = repo.create_note(title="Groceries", body="milk\neggs", pinned=True)
    loaded = repo.get_note(created.id)
    assert loaded == created
    assert loaded.title == "Groceries"
    assert loaded.body == "milk\neggs"
    assert loaded.pinned is True
    assert loaded.created_at == loaded.updated_at


def test_get_missing_note_returns_none(repo: NoteRepository) -> None:
    assert repo.get_note(999) is None


def test_list_puts_pinned_first_then_newest(repo: NoteRepository) -> None:
    old = repo.create_note(title="old")
    pinned = repo.create_note(title="pinned", pinned=True)
    time.sleep(1.01)  # timestamps have one-second resolution
    new = repo.create_note(title="new")
    assert [n.id for n in repo.list_notes()] == [pinned.id, new.id, old.id]


def test_update_changes_only_given_fields(repo: NoteRepository) -> None:
    note = repo.create_note(title="before", body="body stays")
    updated = repo.update_note(note.id, title="after")
    assert updated is not None
    assert (updated.title, updated.body) == ("after", "body stays")


def test_update_missing_note_returns_none(repo: NoteRepository) -> None:
    assert repo.update_note(42, title="nope") is None


def test_values_are_parameters_not_sql(repo: NoteRepository) -> None:
    sneaky = "x'); DROP TABLE notes; --"
    note = repo.create_note(title=sneaky)
    assert repo.get_note(note.id).title == sneaky
    assert repo.count_notes() == 1


def test_checklist_items_keep_their_order(repo: NoteRepository) -> None:
    note = repo.create_note(title="trip")
    for text in ["passport", "charger", "snacks"]:
        repo.add_item(note.id, text)
    items = repo.get_note(note.id).items
    assert [i.text for i in items] == ["passport", "charger", "snacks"]
    assert [i.position for i in items] == [0, 1, 2]


def test_add_item_to_missing_note_returns_none(repo: NoteRepository) -> None:
    assert repo.add_item(123, "orphan") is None


def test_set_item_done(repo: NoteRepository) -> None:
    note = repo.create_note(title="t")
    item = repo.add_item(note.id, "do it")
    assert repo.set_item_done(item.id, True).done is True
    assert repo.set_item_done(item.id, False).done is False
    assert repo.set_item_done(999, True) is None


def test_deleting_a_note_deletes_its_items(repo: NoteRepository) -> None:
    note = repo.create_note(title="t")
    repo.add_item(note.id, "a")
    assert repo.delete_note(note.id) is True
    with sqlite3.connect(repo.db_path) as conn:
        assert conn.execute("SELECT COUNT(*) FROM checklist_items").fetchone()[0] == 0


def test_delete_item_returns_note_id(repo: NoteRepository) -> None:
    note = repo.create_note(title="t")
    item = repo.add_item(note.id, "a")
    assert repo.delete_item(item.id) == note.id
    assert repo.delete_item(item.id) is None
