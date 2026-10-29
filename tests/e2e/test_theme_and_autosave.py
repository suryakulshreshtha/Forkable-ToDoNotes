"""Chapter 09: the purple theme contract, theme memory, and autosave."""

import re

import pytest
from playwright.sync_api import Page, expect

from tests.e2e.pages import EditorPage, HomePage

PLUM = "rgb(70, 16, 76)"  # #46104c, dark background
LILAC = "rgb(248, 242, 250)"  # #f8f2fa, light background


@pytest.fixture
def dark_os(page: Page) -> None:
    """Pretend the operating system is in dark mode, for repeatable results."""
    page.emulate_media(color_scheme="dark")


@pytest.mark.usefixtures("dark_os")
def test_dark_theme_uses_the_palette(page: Page) -> None:
    HomePage(page).open()
    expect(page.locator("body")).to_have_css("background-color", PLUM)


@pytest.mark.usefixtures("dark_os")
def test_theme_toggle_is_remembered(page: Page) -> None:
    home = HomePage(page).open()
    home.theme_toggle.click()
    expect(page.locator("html")).to_have_attribute("data-theme", "light")
    expect(page.locator("body")).to_have_css("background-color", LILAC)
    page.reload()
    expect(page.locator("body")).to_have_css("background-color", LILAC)


def test_light_os_setting_is_followed(page: Page) -> None:
    page.emulate_media(color_scheme="light")
    HomePage(page).open()
    expect(page.locator("body")).to_have_css("background-color", LILAC)


def test_autosave_while_typing(page: Page) -> None:
    note = page.request.post("/api/notes", data={"title": "Autosave"}).json()
    page.goto(f"/notes/{note['id']}")
    editor = EditorPage(page)
    editor.body.press_sequentially("saved without clicking Save")
    expect(editor.status).to_have_text(re.compile(r"^Saved ✓ "))
    page.reload()
    expect(editor.body).to_have_value("saved without clicking Save")


def test_ctrl_s_saves(page: Page) -> None:
    note = page.request.post("/api/notes", data={"title": "Shortcut"}).json()
    page.goto(f"/notes/{note['id']}")
    editor = EditorPage(page)
    editor.title.fill("Saved with the keyboard")
    page.keyboard.press("ControlOrMeta+s")
    expect(page).to_have_url(re.compile(r"saved=1"))
    expect(editor.title).to_have_value("Saved with the keyboard")
