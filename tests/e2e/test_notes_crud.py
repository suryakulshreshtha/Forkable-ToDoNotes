"""Chapter 09: the full life of a note, driven through the real UI."""

import re

from playwright.sync_api import Page, expect

from tests.e2e.pages import EditorPage, HomePage


def test_edit_pin_and_delete(page: Page) -> None:
    editor = EditorPage(page).open_new()
    editor.write("Draft", "first version")
    editor.save()

    editor.title.fill("Final")
    editor.save()
    expect(editor.title).to_have_value("Final")

    home = HomePage(page).open()
    home.toggle_pin("Final")
    expect(home.card("Final")).to_have_class(re.compile(r"\bpinned\b"))

    home.open_note("Final")
    editor.delete_note()
    expect(page).to_have_url(re.compile(r"/$"))
    expect(home.cards).to_have_count(0)


def test_pinned_note_comes_first(page: Page) -> None:
    for title in ["Alpha", "Beta", "Gamma"]:
        page.request.post("/api/notes", data={"title": title, "pinned": title == "Beta"})
    home = HomePage(page).open()
    expect(home.cards.first).to_contain_text("Beta")


def test_title_falls_back_to_first_line(page: Page) -> None:
    editor = EditorPage(page).open_new()
    editor.write("", "\n  shopping list for Saturday\nmore")
    editor.save()
    expect(page).to_have_title(re.compile("shopping list for Saturday"))
