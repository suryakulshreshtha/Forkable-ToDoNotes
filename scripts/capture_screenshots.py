"""Regenerate the screenshots in docs/assets/screenshots/ with Playwright.

Automation is not only for tests: this script starts the app on a throwaway
database, fills it with demo notes, and photographs each screen in both
themes. Run it after any UI change so the docs never show an outdated look.

Usage:
    python scripts/capture_screenshots.py
    python scripts/capture_screenshots.py --executable-path "/path/to/chrome"
        (optional: use an already-installed Chrome/Chromium instead of Playwright's)
"""

from __future__ import annotations

import argparse
import logging
import tempfile
import threading
from pathlib import Path

from playwright.sync_api import Page, sync_playwright
from werkzeug.serving import make_server

from todonotes.web import create_app

OUT = Path(__file__).resolve().parents[1] / "docs" / "assets" / "screenshots"
DESKTOP = {"width": 1280, "height": 800}
PHONE = {"width": 390, "height": 844}

DEMO_NOTES = [
    {
        "title": "Weekend groceries",
        "body": "Farmers market first, then the corner shop.",
        "pinned": True,
        "items": ["oat milk", "eggs", "basil", "lemons"],
        "done": [0, 2],
    },
    {
        "title": "Chapter 07 ideas",
        "body": "Prefix search: 'mil' finds milk and milkshake.",
        "items": [],
        "done": [],
    },
    {
        "title": "Trip to Jaipur",
        "body": "Hawa Mahal at sunrise. Book the train early.",
        "items": ["passport", "charger", "sunscreen"],
        "done": [0],
    },
    {
        "title": "",
        "body": "Untitled notes use their first line as the title.\nLike this one.",
        "items": [],
        "done": [],
    },
    {
        "title": "Milkshake recipe",
        "body": "Banana, cold milk, a spoon of honey. Blend 30 seconds.",
        "items": [],
        "done": [],
    },
]


def seed(app) -> int:
    service = app.extensions["todonotes"]
    first_id = 0
    for demo in DEMO_NOTES:
        note = service.create(demo["title"], demo["body"], demo.get("pinned", False))
        first_id = first_id or note.id
        items = [service.add_item(note.id, text) for text in demo["items"]]
        for index in demo["done"]:
            service.set_item_done(items[index].id, True)
    return first_id


def shoot(page: Page, name: str) -> None:
    path = OUT / f"{name}.png"
    page.screenshot(path=str(path))
    print(f"📸 {path.relative_to(OUT.parents[2])}")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--executable-path", help="use this Chrome/Chromium binary")
    args = parser.parse_args()

    OUT.mkdir(parents=True, exist_ok=True)
    logging.getLogger("werkzeug").setLevel(logging.ERROR)  # hide per-request log lines
    with tempfile.TemporaryDirectory() as tmp:
        app = create_app(Path(tmp) / "demo.db")
        first_id = seed(app)
        server = make_server("127.0.0.1", 0, app, threaded=True)
        threading.Thread(target=server.serve_forever, daemon=True).start()
        base = f"http://127.0.0.1:{server.server_port}"
        try:
            with sync_playwright() as playwright:
                browser = playwright.chromium.launch(executable_path=args.executable_path)
                for scheme in ("dark", "light"):
                    page = browser.new_page(viewport=DESKTOP, color_scheme=scheme, base_url=base)
                    page.goto("/")
                    shoot(page, f"home-{scheme}")
                    page.goto(f"/notes/{first_id}")
                    shoot(page, f"editor-{scheme}")
                    page.goto("/?q=mil")
                    shoot(page, f"search-{scheme}")
                    page.close()
                phone = browser.new_page(viewport=PHONE, color_scheme="dark", base_url=base)
                phone.goto("/")
                shoot(phone, "phone-dark")
                browser.close()
        finally:
            server.shutdown()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
