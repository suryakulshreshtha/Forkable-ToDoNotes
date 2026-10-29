"""Chapter 09: set up through the API, assert through the UI (and the reverse).

Creating 20 notes by clicking would take seconds and test nothing new.
`page.request` shares the page's base_url (and cookies), so seeding is one
HTTP call per note.
"""

from playwright.sync_api import Page, expect

from tests.e2e.pages import EditorPage, HomePage


def test_seed_via_api_then_check_the_ui(page: Page) -> None:
    for number in range(1, 21):
        response = page.request.post("/api/notes", data={"title": f"Note {number:02d}"})
        expect(response).to_be_ok()
    home = HomePage(page).open()
    expect(home.cards).to_have_count(20)
    expect(page.get_by_role("heading", level=1)).to_contain_text("20")


def test_change_in_ui_then_check_the_api(page: Page) -> None:
    editor = EditorPage(page).open_new()
    editor.write("From the UI", "typed by Playwright")
    editor.save()
    notes = page.request.get("/api/notes").json()["notes"]
    assert [(n["title"], n["body"]) for n in notes] == [("From the UI", "typed by Playwright")]


def test_api_validation_errors_are_json(page: Page) -> None:
    response = page.request.post("/api/notes", data={"title": "x" * 201})
    assert response.status == 400
    assert "too long" in response.json()["error"]
