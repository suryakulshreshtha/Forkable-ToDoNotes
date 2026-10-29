"""What every screen shares: the top bar."""

from __future__ import annotations

from playwright.sync_api import Locator, Page


class BasePage:
    def __init__(self, page: Page) -> None:
        self.page = page
        # Locators are lazy: nothing is looked up until an action or assertion runs.
        # Prefer what a user perceives (role + accessible name) over CSS classes.
        self.new_note_link = page.get_by_role("link", name="New note")
        self.search_box = page.get_by_role("searchbox", name="Search notes")
        self.theme_toggle = page.get_by_role("button", name="Switch light or dark theme")

    def heading(self) -> Locator:
        return self.page.get_by_role("heading", level=1)

    def search(self, text: str) -> None:
        self.search_box.fill(text)
        self.search_box.press("Enter")
