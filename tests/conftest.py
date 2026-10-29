"""Shared pytest fixtures and hooks for the whole test suite.

pytest discovers this file automatically; tests never import it. A fixture
is requested simply by naming it as a test function argument.
"""

from __future__ import annotations

from pathlib import Path

import pytest


def pytest_collection_modifyitems(items: list[pytest.Item]) -> None:
    """Mark every test by the folder it lives in, so nobody forgets a marker.

    tests/unit/... -> @pytest.mark.unit   (run with: pytest -m unit)
    """
    for item in items:
        parts = Path(str(item.path)).parts
        if "unit" in parts:
            item.add_marker(pytest.mark.unit)
