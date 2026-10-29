"""Command-line entry point: ``python -m todonotes`` (or the ``todonotes`` command).

Right now it only knows ``--version``. Chapter 05 turns it into a launcher
that starts the local web server and opens your browser.
"""

from __future__ import annotations

import argparse

from todonotes import APP_NAME, __version__


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="todonotes",
        description=f"{APP_NAME}: a standalone, offline-first notes + to-do app.",
    )
    parser.add_argument("--version", action="version", version=f"{APP_NAME} {__version__}")
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    print(f"{APP_NAME} {__version__} — nothing to run yet. See docs/README.md.")
    del args
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
