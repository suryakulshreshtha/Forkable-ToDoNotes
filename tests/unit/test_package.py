"""Chapter 01: the package installs, imports and reports its version."""

import re

import pytest

import todonotes
from todonotes.__main__ import main


def test_version_is_semver() -> None:
    assert re.fullmatch(r"\d+\.\d+\.\d+", todonotes.__version__)


def test_version_flag_prints_name_and_version(capsys: pytest.CaptureFixture[str]) -> None:
    with pytest.raises(SystemExit) as exit_info:
        main(["--version"])
    assert exit_info.value.code == 0
    assert capsys.readouterr().out.strip() == f"Forkable-ToDoNotes {todonotes.__version__}"


def test_main_without_arguments_is_a_friendly_no_op(capsys: pytest.CaptureFixture[str]) -> None:
    assert main([]) == 0
    assert "nothing to run yet" in capsys.readouterr().out
