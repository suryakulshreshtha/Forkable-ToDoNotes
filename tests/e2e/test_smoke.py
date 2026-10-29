"""Chapter 08: the first browser tests — does the app open, and can I create a note?"""

import re

import pytest
from playwright.sync_api import Page, expect

from tests.e2e.pages import EditorPage, HomePage

pytestmark = pytest.mark.smoke


def test_home_page_loads(page: Page) -> None:
    home = HomePage(page).open()
    expect(page).to_have_title(re.compile("All notes"))
    expect(home.heading()).to_contain_text("All notes")
    expect(page.get_by_text("No notes yet")).to_be_visible()


def test_create_a_note(page: Page) -> None:
    home = HomePage(page).open()
    home.new_note_link.click()

    editor = EditorPage(page)
    editor.write("Groceries", "milk\neggs")
    editor.save()

    # Web-first assertions retry until they pass (or time out), so no sleep() needed.
    expect(page).to_have_url(re.compile(r"/notes/\d+"))
    expect(editor.status).to_have_text("Saved ✓")

    home.open()
    expect(home.cards).to_have_count(1)
    expect(home.card("Groceries")).to_contain_text("milk")
