"""Page objects: one class per screen, holding its locators and actions.

Tests read like a user story ("open the home page, create a note…") and the
"how do I find that button" details live here, in one place.
"""

from tests.e2e.pages.editor_page import EditorPage
from tests.e2e.pages.home_page import HomePage

__all__ = ["EditorPage", "HomePage"]
