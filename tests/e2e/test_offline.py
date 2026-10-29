"""Chapter 09: prove the app never reaches beyond 127.0.0.1.

`context.route("**/*", ...)` puts Playwright between the browser and the
network for EVERY request from every page in this context. Anything not aimed
at our local server is recorded and aborted. The test then walks through the
whole app; if any page tries to load a CDN font, a script or an analytics
beacon, the list is not empty and the test fails, naming the URL.
"""

from urllib.parse import urlsplit

import pytest
from playwright.sync_api import BrowserContext, Page, Route, expect

from tests.e2e.pages import EditorPage, HomePage

pytestmark = pytest.mark.offline


def test_nothing_leaves_the_machine(context: BrowserContext, page: Page) -> None:
    escaped: list[str] = []

    def guard(route: Route) -> None:
        host = urlsplit(route.request.url).hostname
        if host in {"127.0.0.1", "localhost"}:
            route.continue_()
        else:
            escaped.append(route.request.url)
            route.abort()

    context.route("**/*", guard)

    home = HomePage(page).open()
    home.new_note_link.click()
    editor = EditorPage(page)
    editor.write("Offline", "no internet needed")
    editor.save()
    editor.add_item("still works")
    home.open()
    home.search("internet")
    home.theme_toggle.click()
    expect(home.cards).to_have_count(1)

    assert escaped == [], f"The app tried to reach the internet: {escaped}"
