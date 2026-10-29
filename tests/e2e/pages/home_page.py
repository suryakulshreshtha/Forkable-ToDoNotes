"""The note list (and search results) at "/"."""

from __future__ import annotations

from playwright.sync_api import Locator

from tests.e2e.pages.base_page import BasePage


class HomePage(BasePage):
    def open(self) -> HomePage:
        self.page.goto("/")
        return self

    @property
    def cards(self) -> Locator:
        return self.page.locator("article.card")

    def card(self, title: str) -> Locator:
        return self.cards.filter(has=self.page.get_by_role("link", name=title, exact=True))

    def open_note(self, title: str) -> None:
        self.page.get_by_role("link", name=title, exact=True).click()

    def toggle_pin(self, title: str) -> None:
        self.card(title).get_by_role("button", name="Pin").or_(
            self.card(title).get_by_role("button", name="Unpin")
        ).click()
