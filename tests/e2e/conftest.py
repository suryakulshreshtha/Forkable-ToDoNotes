"""Fixtures for the Playwright browser tests.

pytest-playwright already gives us `page`, `context` and `browser`.
We add one thing: a REAL running copy of the app, so the browser has
something to talk to.

    live_server  (session)  starts the app on a free 127.0.0.1 port, once
    base_url     (session)  tells pytest-playwright where it is, so tests
                            can write page.goto("/") instead of full URLs
    clean_db     (autouse)  empties the database before every test, so tests
                            never depend on each other's leftovers
"""

from __future__ import annotations

import sqlite3
import threading
from collections.abc import Iterator
from contextlib import closing
from dataclasses import dataclass
from pathlib import Path

import pytest
from werkzeug.serving import make_server

from todonotes.web import create_app


@dataclass
class LiveServer:
    url: str
    db_path: Path


@pytest.fixture(scope="session")
def live_server(tmp_path_factory: pytest.TempPathFactory) -> Iterator[LiveServer]:
    db_path = tmp_path_factory.mktemp("e2e") / "notes.db"
    app = create_app(db_path)
    # Port 0 = "any free port". threaded=True lets the browser load the page,
    # its CSS and its JavaScript in parallel, like a real server would.
    server = make_server("127.0.0.1", 0, app, threaded=True)
    thread = threading.Thread(target=server.serve_forever, daemon=True)
    thread.start()
    yield LiveServer(url=f"http://127.0.0.1:{server.server_port}", db_path=db_path)
    server.shutdown()
    thread.join(timeout=5)


@pytest.fixture(scope="session")
def base_url(live_server: LiveServer) -> str:
    """Overrides pytest-playwright's own `base_url` fixture with the live server's URL."""
    return live_server.url


@pytest.fixture(autouse=True)
def clean_db(live_server: LiveServer) -> None:
    with closing(sqlite3.connect(live_server.db_path)) as conn, conn:  # close AND commit
        conn.execute("PRAGMA foreign_keys = ON")
        conn.execute("DELETE FROM notes")  # items go too (ON DELETE CASCADE)
