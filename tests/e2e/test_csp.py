"""Security: the Content-Security-Policy is real, and the app obeys it.

Two proofs. First, every page of the app loads, and works, without the browser
reporting a single policy violation (`securitypolicyviolation` events). Second,
the policy actually blocks what it promises to: an inline script injected into
the page is refused by the browser.
"""

import pytest
from playwright.sync_api import Page, expect

from tests.e2e.pages import EditorPage, HomePage

# Runs in the page before any of its own scripts: collects every violation the browser reports.
COLLECT_VIOLATIONS = """
window.__violations = [];
document.addEventListener("securitypolicyviolation", (event) => {
  window.__violations.push(event.violatedDirective + " blocked " + (event.blockedURI || "inline"));
});
"""

pytestmark = pytest.mark.smoke


def test_the_whole_app_runs_without_a_single_policy_violation(page: Page) -> None:
    page.add_init_script(COLLECT_VIOLATIONS)
    home = HomePage(page).open()
    home.new_note_link.click()
    editor = EditorPage(page)
    editor.write("Policy check", "plain text, <b>not markup</b>")
    editor.save()
    editor.add_item("tick me")
    home.open()
    home.search("policy")
    home.theme_toggle.click()
    expect(home.cards).to_have_count(1)

    assert page.evaluate("window.__violations") == []


def test_the_browser_refuses_an_injected_inline_script(page: Page) -> None:
    page.add_init_script(COLLECT_VIOLATIONS)
    HomePage(page).open()

    page.evaluate(
        """() => {
            const script = document.createElement("script");
            script.textContent = "window.__injected = true";
            document.head.appendChild(script);
        }"""
    )

    assert page.evaluate("window.__injected") is None  # it never ran
    assert any("script-src" in v for v in page.evaluate("window.__violations"))
