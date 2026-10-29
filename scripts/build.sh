#!/usr/bin/env bash
# Build a single-file executable for THIS operating system (macOS or Linux).
# PyInstaller is not a cross-compiler: build on macOS for macOS, on Windows for Windows.
# Usage:  ./scripts/build.sh        (run from the repository root, venv active)
set -euo pipefail
cd "$(dirname "$0")/.."

python -m pip install -r requirements-dev.txt
python -m PyInstaller \
  --noconfirm --clean \
  --onefile \
  --name ForkableToDoNotes \
  --collect-data todonotes \
  packaging/launch.py

echo "✅ Built: dist/ForkableToDoNotes"
