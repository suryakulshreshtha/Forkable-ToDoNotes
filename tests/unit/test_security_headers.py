"""Security headers: every response says what the page may and may not do.

The Content-Security-Policy is the second line of defence behind template
escaping: even if a note's text ever ran as HTML, the browser would refuse to
execute inline script or to load anything from another site.
"""

from __future__ import annotations

import re
from pathlib import Path

import pytest
from flask.testing import FlaskClient

TEMPLATES = Path(__file__).resolve().parents[2] / "src" / "todonotes" / "templates"

REQUIRED_HEADERS = [
    "Content-Security-Policy",
    "X-Content-Type-Options",
    "Referrer-Policy",
    "Cross-Origin-Opener-Policy",
    "Cross-Origin-Resource-Policy",
    "X-Frame-Options",
]


@pytest.mark.parametrize(
    "path",
    [
        "/",
        "/notes/new",
        "/api/health",
        "/api/notes",
        "/export.json",
        "/export.md",
        "/static/app.js",
    ],
)
def test_every_response_has_the_security_headers(client: FlaskClient, path: str) -> None:
    response = client.get(path)
    assert response.status_code == 200
    for name in REQUIRED_HEADERS:
        assert name in response.headers, f"{name} missing on {path}"


def test_error_responses_have_them_too(client: FlaskClient) -> None:
    missing = client.get("/notes/9999")
    foreign_host = client.get("/", headers={"Host": "evil.example"})
    assert missing.status_code == 404
    assert foreign_host.status_code == 400
    for response in (missing, foreign_host):
        for name in REQUIRED_HEADERS:
            assert name in response.headers


def test_policy_blocks_framing_inline_script_and_other_sites(client: FlaskClient) -> None:
    policy = client.get("/").headers["Content-Security-Policy"]
    assert "frame-ancestors 'none'" in policy  # no other site can frame the app (clickjacking)
    assert "script-src 'self'" in policy
    assert "default-src 'none'" in policy
    assert "base-uri 'none'" in policy
    assert "form-action 'self'" in policy
    assert "unsafe-inline" not in policy
    assert "unsafe-eval" not in policy
    assert not re.search(r"https?:|\*", policy)  # nothing is allowed from outside


def test_pages_and_api_are_not_cached_but_static_files_are_left_alone(
    client: FlaskClient,
) -> None:
    assert client.get("/").headers["Cache-Control"] == "no-store"
    assert client.get("/api/notes").headers["Cache-Control"] == "no-store"
    assert "no-store" not in client.get("/static/app.css").headers.get("Cache-Control", "")


def test_nosniff_and_referrer_policy_values(client: FlaskClient) -> None:
    headers = client.get("/").headers
    assert headers["X-Content-Type-Options"] == "nosniff"
    assert headers["Referrer-Policy"] == "same-origin"
    assert headers["X-Frame-Options"] == "DENY"


@pytest.mark.parametrize("template", sorted(TEMPLATES.glob("*.html")), ids=lambda p: p.name)
def test_templates_contain_nothing_the_policy_would_block(template: Path) -> None:
    """The policy only works if the templates keep to it: no inline script, style or handlers."""
    html = template.read_text(encoding="utf-8")
    assert not re.search(r"<script(?![^>]*\bsrc=)", html), "inline <script> block"
    assert not re.search(r"<style\b", html), "inline <style> block"
    assert not re.search(r"\sstyle=", html), "inline style attribute"
    assert not re.search(r"\son[a-z]+=", html), "inline event handler attribute"
