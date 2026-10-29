"""Chapter 09: search, from the user's side — typing, highlights, shortcuts."""

import pytest
from playwright.sync_api import Page, expect

from tests.e2e.pages import HomePage

pytestmark = pytest.mark.search


@pytest.fixture
def notes(page: Page) -> None:
    for title, body in [
        ("Groceries", "buy milk and eggs"),
        ("Recipes", "chocolate milkshake"),
        ("Work", "call the dentist"),
    ]:
        page.request.post("/api/notes", data={"title": title, "body": body})


@pytest.mark.usefixtures("notes")
def test_prefix_search_highlights_matches(page: Page) -> None:
    home = HomePage(page).open()
    home.search("mil")
    expect(home.heading()).to_have_text("2 results for “mil”")
    expect(home.card("Groceries").locator("mark")).to_have_text("milk")
    expect(home.card("Recipes").locator("mark")).to_have_text("milkshake")


@pytest.mark.usefixtures("notes")
def test_no_results_offers_a_way_back(page: Page) -> None:
    home = HomePage(page).open()
    home.search("zebra")
    expect(page.get_by_text("No notes match “zebra”.")).to_be_visible()
    page.get_by_role("link", name="Show all notes").click()
    expect(home.cards).to_have_count(3)


@pytest.mark.usefixtures("notes")
def test_slash_key_focuses_search(page: Page) -> None:
    home = HomePage(page).open()
    page.keyboard.press("/")
    expect(home.search_box).to_be_focused()
    page.keyboard.type("dent")
    page.keyboard.press("Enter")
    expect(home.cards).to_have_count(1)


@pytest.mark.usefixtures("notes")
def test_html_in_notes_is_shown_as_text(page: Page) -> None:
    page.request.post("/api/notes", data={"title": "xss", "body": "<img src=x onerror=alert(1)>"})
    home = HomePage(page).open()
    home.search("onerror")
    expect(home.card("xss")).to_contain_text("<img src=x onerror=alert(1)>")
    expect(home.card("xss").locator("img")).to_have_count(0)
