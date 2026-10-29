"""Chapter 11: the supply-chain audit never publishes anyone's e-mail address.

Package metadata contains maintainers' personal e-mail addresses. The audit may
use them to check the vendor policy, but it must not print them or write them
into the committed supply-chain record.
"""

from __future__ import annotations

import importlib.util
import re
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[2]
EMAIL_ADDRESS = re.compile(r"[A-Za-z0-9._%+-]+@[A-Za-z0-9-]+\.[A-Za-z.]+")


def _load_audit_module():
    """scripts/ is not a package, so load the file by path (and register it for dataclasses)."""
    spec = importlib.util.spec_from_file_location("audit_deps", ROOT / "scripts" / "audit_deps.py")
    module = importlib.util.module_from_spec(spec)
    sys.modules["audit_deps"] = module
    spec.loader.exec_module(module)
    return module


audit = _load_audit_module()


@pytest.mark.parametrize(
    ("raw", "shown"),
    [
        ("Pallets <contact@example.com>", "Pallets"),
        ('"Astral Software Inc." <hello@example.com>', "Astral Software Inc."),
        (
            "Ronny Pfannschmidt <opensource@example.de>, Holger Krekel <holger@example.com>",
            "Ronny Pfannschmidt, Holger Krekel",
        ),
        ("Jason Kirtland", "Jason Kirtland"),
        ("contact@example.org", "(name not published)"),
        ("-", "-"),
    ],
)
def test_publisher_is_shown_without_email_addresses(raw: str, shown: str) -> None:
    assert audit.publisher_display(raw) == shown


def test_policy_still_matches_on_an_email_domain() -> None:
    """Hiding an address from readers must not hide it from the policy check."""
    package = audit.Package(
        name="example",
        version="1.0",
        publisher="Someone <someone@blocked.example>",
        url="https://example.org",
        license="MIT",
    )
    assert "blocked.example" in package.haystack()
    assert "blocked.example" not in package.publisher_display


def test_committed_supply_chain_record_has_no_email_addresses() -> None:
    text = (ROOT / "docs" / "SUPPLY-CHAIN.md").read_text(encoding="utf-8")
    assert EMAIL_ADDRESS.findall(text) == []
