"""Where the app keeps its notes file.

Each operating system has a conventional per-user folder for application data.
We follow that convention so the notes survive app upgrades and never land in a
random working directory:

    macOS    ~/Library/Application Support/Forkable-ToDoNotes/notes.db
    Windows  %APPDATA%\\Forkable-ToDoNotes\\notes.db
    Linux    $XDG_DATA_HOME/Forkable-ToDoNotes/notes.db  (default ~/.local/share/...)

Set the TODONOTES_DB environment variable (or pass --db) to use another file.
"""

from __future__ import annotations

import os
import sys
from pathlib import Path

from todonotes import APP_NAME

ENV_DB = "TODONOTES_DB"


def default_data_dir() -> Path:
    """Return the per-user data folder for this operating system."""
    if sys.platform == "darwin":
        base = Path.home() / "Library" / "Application Support"
    elif os.name == "nt":
        base = Path(os.environ.get("APPDATA") or Path.home() / "AppData" / "Roaming")
    else:
        base = Path(os.environ.get("XDG_DATA_HOME") or Path.home() / ".local" / "share")
    return base / APP_NAME


def default_db_path() -> Path:
    """The notes file to use: TODONOTES_DB if set, otherwise the per-user default."""
    override = os.environ.get(ENV_DB)
    if override:
        return Path(override).expanduser()
    return default_data_dir() / "notes.db"
