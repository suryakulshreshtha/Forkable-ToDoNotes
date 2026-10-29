"""Command-line entry point: ``python -m todonotes`` (or the ``todonotes`` command).

It starts a small local web server on 127.0.0.1 (your machine only) and opens
your default browser at it. Nothing listens on your network, nothing phones home.
"""

from __future__ import annotations

import argparse
import socket
import sys
import threading
import webbrowser
from pathlib import Path

from todonotes import APP_NAME, __version__
from todonotes.config import default_db_path

DEFAULT_PORT = 8765
LOOPBACK = "127.0.0.1"


def pick_port(preferred: int) -> int:
    """Return ``preferred`` if it is free on loopback, otherwise any free port.

    Binding to port 0 asks the operating system for an unused port.
    """
    for candidate in (preferred, 0):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            try:
                sock.bind((LOOPBACK, candidate))
            except OSError:
                continue
            return sock.getsockname()[1]
    raise RuntimeError("Could not find a free port on 127.0.0.1")


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="todonotes",
        description=f"{APP_NAME}: a standalone, offline-first notes + to-do app.",
    )
    parser.add_argument("--version", action="version", version=f"{APP_NAME} {__version__}")
    parser.add_argument(
        "--port", type=int, default=DEFAULT_PORT, help=f"preferred port (default {DEFAULT_PORT})"
    )
    parser.add_argument(
        "--db", type=Path, default=None, help="path to the SQLite file (default: per-user data dir)"
    )
    parser.add_argument(
        "--no-browser", action="store_true", help="do not open a browser window automatically"
    )
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    # Imported here so `--version` and `--help` stay instant.
    from waitress import serve

    from todonotes.web import create_app

    # Windows consoles redirected to a file may not speak UTF-8; never crash on an emoji.
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(errors="replace")

    db_path = args.db or default_db_path()
    app = create_app(db_path)
    port = pick_port(args.port)
    url = f"http://{LOOPBACK}:{port}/"

    print(f"📝 {APP_NAME} {__version__}")
    print(f"   Notes file : {db_path}")
    print(f"   Open       : {url}")
    print("   Stop       : press Ctrl+C in this window", flush=True)

    if not args.no_browser:
        # Give the server a moment to start before the browser asks for the page.
        threading.Timer(1.0, webbrowser.open, args=(url,)).start()

    serve(app, host=LOOPBACK, port=port, threads=4)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
