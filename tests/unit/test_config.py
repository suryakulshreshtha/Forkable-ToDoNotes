"""Chapter 03: the notes file lands in the right per-user folder."""

from pathlib import Path

import pytest

from todonotes import config


def test_env_var_overrides_default(monkeypatch: pytest.MonkeyPatch, tmp_path: Path) -> None:
    target = tmp_path / "elsewhere" / "my-notes.db"
    monkeypatch.setenv(config.ENV_DB, str(target))
    assert config.default_db_path() == target


def test_default_file_is_notes_db_in_app_folder(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.delenv(config.ENV_DB, raising=False)
    path = config.default_db_path()
    assert path.name == "notes.db"
    assert path.parent.name == "Forkable-ToDoNotes"


def test_macos_uses_application_support(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr(config.sys, "platform", "darwin")
    expected = Path.home() / "Library" / "Application Support" / "Forkable-ToDoNotes"
    assert config.default_data_dir() == expected
