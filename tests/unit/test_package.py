"""Chapter 01: the package installs, imports and reports its version."""

import re

import pytest

import todonotes
from todonotes.__main__ import build_parser, main


def test_version_is_semver() -> None:
    assert re.fullmatch(r"\d+\.\d+\.\d+", todonotes.__version__)


def test_version_flag_prints_name_and_version(capsys: pytest.CaptureFixture[str]) -> None:
    with pytest.raises(SystemExit) as exit_info:
        main(["--version"])
    assert exit_info.value.code == 0
    assert capsys.readouterr().out.strip() == f"Forkable-ToDoNotes {todonotes.__version__}"


def test_parser_defaults() -> None:
    args = build_parser().parse_args([])
    assert args.port == 8765
    assert args.db is None
    assert args.no_browser is False


def test_pick_port_falls_back_when_preferred_is_busy() -> None:
    import socket

    from todonotes.__main__ import pick_port

    with socket.socket() as busy:
        busy.bind(("127.0.0.1", 0))
        busy.listen()
        taken = busy.getsockname()[1]
        assert pick_port(taken) != taken
