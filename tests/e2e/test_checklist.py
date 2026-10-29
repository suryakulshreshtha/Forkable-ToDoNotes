"""Chapter 09: checklist items — add, tick (no page reload), remove."""

from playwright.sync_api import Page, expect

from tests.e2e.pages import EditorPage, HomePage


def test_add_and_tick_items(page: Page) -> None:
    note = page.request.post("/api/notes", data={"title": "Trip"}).json()
    page.goto(f"/notes/{note['id']}")
    editor = EditorPage(page)

    for text in ["passport", "charger"]:
        editor.add_item(text)
    expect(editor.item("passport")).not_to_be_checked()

    # app.js intercepts this click and PATCHes the API. Waiting for that exact
    # response proves the toggle went through the API, not a full form reload.
    with page.expect_response(lambda r: "/api/items/" in r.url and r.request.method == "PATCH"):
        editor.item("passport").click()
    expect(editor.item("passport")).to_be_checked()
    expect(page.locator("#checklist-heading .count")).to_have_text("1/2")

    page.reload()
    expect(editor.item("passport")).to_be_checked()  # it really was saved

    home = HomePage(page).open()
    expect(home.card("Trip")).to_contain_text("☑ 1/2")


def test_remove_item(page: Page) -> None:
    note = page.request.post("/api/notes", data={"title": "t", "items": ["temporary"]}).json()
    page.goto(f"/notes/{note['id']}")
    page.get_by_role("button", name="Remove “temporary”").click()
    expect(EditorPage(page).item("temporary")).to_have_count(0)


def test_checklist_works_without_javascript(browser, base_url: str) -> None:
    """Progressive enhancement: the plain HTML form path still works."""
    context = browser.new_context(java_script_enabled=False, base_url=base_url)
    page = context.new_page()
    note = page.request.post("/api/notes", data={"title": "no js", "items": ["works"]}).json()
    page.goto(f"/notes/{note['id']}")
    EditorPage(page).item("works").click()  # submits the form, server redirects back
    expect(EditorPage(page).item("works")).to_be_checked()
    context.close()
