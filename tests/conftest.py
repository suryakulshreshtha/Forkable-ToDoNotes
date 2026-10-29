"""Shared pytest fixtures and hooks for the whole test suite.

pytest discovers this file automatically; tests never import it. A fixture
is requested simply by naming it as a test function argument.
"""

from __future__ import annotations

from pathlib import Path

import pytest

from todonotes.service import NoteService
from todonotes.storage import NoteRepository


def pytest_collection_modifyitems(items: list[pytest.Item]) -> None:
    """Mark every test by the folder it lives in, so nobody forgets a marker.

    tests/unit/... -> @pytest.mark.unit   (run with: pytest -m unit)
    tests/e2e/...  -> @pytest.mark.e2e    (run with: pytest -m e2e)
    """
    for item in items:
        parts = Path(str(item.path)).parts
        if "unit" in parts:
            item.add_marker(pytest.mark.unit)
        elif "e2e" in parts:
            item.add_marker(pytest.mark.e2e)


@pytest.fixture
def db_path(tmp_path: Path) -> Path:
    """A fresh, empty notes file inside pytest's per-test temporary folder."""
    return tmp_path / "notes.db"


@pytest.fixture
def repo(db_path: Path) -> NoteRepository:
    repository = NoteRepository(db_path)
    repository.initialize()
    return repository


@pytest.fixture
def service(repo: NoteRepository) -> NoteService:
    return NoteService(repo)


@pytest.fixture
def app(db_path: Path):
    from todonotes.web import create_app

    return create_app(db_path)


@pytest.fixture
def client(app):
    """Flask's test client: makes requests without starting a real server."""
    return app.test_client()
