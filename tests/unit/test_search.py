"""Chapter 07: full-text search with FTS5, and the LIKE fallback."""

import pytest
from flask.testing import FlaskClient

from todonotes import storage
from todonotes.models import MARK_END, MARK_START
from todonotes.storage import NoteRepository, to_fts_query
from todonotes.web import highlight


def marked(word: str) -> str:
    return f"{MARK_START}{word}{MARK_END}"


@pytest.fixture
def seeded(repo: NoteRepository) -> NoteRepository:
    repo.create_note(title="Groceries", body="buy milk and eggs")
    repo.create_note(title="Recipes", body="chocolate milkshake with ice cream")
    repo.create_note(title="Work", body="call the dentist at 10:30")
    return repo


@pytest.mark.parametrize(
    ("typed", "query"),
    [
        ("milk", '"milk"*'),
        ("mil  eg", '"mil"* "eg"*'),
        ('say "hi"', '"say"* "hi"*'),
        ("a-b OR (c)", '"a-b"* "OR"* "(c)"*'),
        ("   ", ""),
    ],
)
def test_to_fts_query_quotes_every_word(typed: str, query: str) -> None:
    assert to_fts_query(typed) == query


def test_fts5_is_used_when_available(repo: NoteRepository) -> None:
    assert repo.fts_enabled is storage.fts5_available()


def test_prefix_search_finds_both_milk_notes(seeded: NoteRepository) -> None:
    titles = {hit.note.title for hit in seeded.search("mil")}
    assert titles == {"Groceries", "Recipes"}


def test_every_word_must_match(seeded: NoteRepository) -> None:
    assert [hit.note.title for hit in seeded.search("milk eggs")] == ["Groceries"]


def test_snippet_marks_the_match(seeded: NoteRepository) -> None:
    [hit] = seeded.search("dentist")
    assert marked("dentist") in hit.snippet


@pytest.mark.parametrize("tricky", ['"', "AND", "NEAR(", "-", "*", "10:30", "a'b", "%_"])
def test_operator_characters_never_crash(seeded: NoteRepository, tricky: str) -> None:
    seeded.search(tricky)  # must not raise sqlite3.OperationalError


def test_index_follows_updates_and_deletes(seeded: NoteRepository) -> None:
    [hit] = seeded.search("dentist")
    seeded.update_note(hit.note.id, body="call the plumber")
    assert seeded.search("dentist") == []
    assert len(seeded.search("plumber")) == 1
    seeded.delete_note(hit.note.id)
    assert seeded.search("plumber") == []


def test_like_fallback_without_fts5(monkeypatch: pytest.MonkeyPatch, db_path) -> None:
    monkeypatch.setattr(storage, "fts5_available", lambda: False)
    repo = NoteRepository(db_path)
    repo.initialize()
    assert repo.fts_enabled is False
    repo.create_note(title="Groceries", body="buy milk")
    repo.create_note(title="Percent", body="100% sure")
    [hit] = repo.search("mil")
    assert hit.note.title == "Groceries"
    assert marked("mil") in hit.snippet
    assert [h.note.title for h in repo.search("%")] == ["Percent"]  # % is literal


def test_index_is_rebuilt_when_fts5_comes_back(monkeypatch: pytest.MonkeyPatch, db_path) -> None:
    if not storage.fts5_available():
        pytest.skip("this Python's SQLite has no FTS5")
    with monkeypatch.context() as patch:
        patch.setattr(storage, "fts5_available", lambda: False)
        repo = NoteRepository(db_path)
        repo.initialize()
        repo.create_note(title="written without an index")
    repo = NoteRepository(db_path)
    repo.initialize()  # FTS5 available again: triggers recreated + index rebuilt
    assert repo.fts_enabled
    assert len(repo.search("index")) == 1


def test_highlight_escapes_before_marking() -> None:
    html = str(highlight(f"<b>{marked('milk')}</b>"))
    assert html == "&lt;b&gt;<mark>milk</mark>&lt;/b&gt;"


def test_search_page_and_api(client: FlaskClient) -> None:
    client.post("/api/notes", json={"title": "Groceries", "body": "buy milk"})
    page = client.get("/?q=mil").get_data(as_text=True)
    assert "1 result for" in page
    assert "<mark>milk</mark>" in page
    hits = client.get("/api/notes?q=mil").get_json()["hits"]
    assert hits[0]["note"]["title"] == "Groceries"


def test_no_results_page(client: FlaskClient) -> None:
    page = client.get("/?q=zebra").get_data(as_text=True)
    assert "No notes match" in page
