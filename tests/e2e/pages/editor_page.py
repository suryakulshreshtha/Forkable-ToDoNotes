"""The note editor at /notes/new and /notes/<id>."""

from __future__ import annotations

from playwright.sync_api import Locator

from tests.e2e.pages.base_page import BasePage


class EditorPage(BasePage):
    def __init__(self, page) -> None:
        super().__init__(page)
        self.title = page.get_by_label("Title")
        self.body = page.get_by_label("Note", exact=True)
        self.save_button = page.get_by_role("button", name="Save").or_(
            page.get_by_role("button", name="Create note")
        )
        self.status = page.get_by_role("status")
        self.new_item = page.get_by_label("New checklist item")

    def open_new(self) -> EditorPage:
        self.page.goto("/notes/new")
        return self

    def write(self, title: str, body: str = "") -> None:
        self.title.fill(title)
        self.body.fill(body)

    def save(self) -> None:
        self.save_button.click()

    def add_item(self, text: str) -> None:
        self.new_item.fill(text)
        self.new_item.press("Enter")

    def item(self, text: str) -> Locator:
        """A checklist item's checkbox, found by its accessible name."""
        return self.page.get_by_role("checkbox", name=text, exact=True)

    def delete_note(self) -> None:
        self.page.get_by_text("Delete this note…").click()
        self.page.get_by_role("button", name="Yes, delete it").click()
