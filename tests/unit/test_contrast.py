"""Chapter 06: the colour palette stays readable (WCAG AA) in every theme."""

import importlib.util
from pathlib import Path

import pytest

SCRIPT = Path(__file__).resolve().parents[2] / "scripts" / "check_contrast.py"
spec = importlib.util.spec_from_file_location("check_contrast", SCRIPT)
check_contrast = importlib.util.module_from_spec(spec)
spec.loader.exec_module(check_contrast)

SAMPLED_PALETTE = {
    "--orchid": "#af6bbb",
    "--amethyst": "#672891",
    "--iris": "#603db7",
    "--royal-purple": "#5316a6",
    "--violet": "#5a1a9c",
    "--purple-heart": "#601475",
    "--grape": "#571269",
    "--plum": "#46104c",
}


def test_palette_matches_the_sampled_colours() -> None:
    base = check_contrast.parse_blocks(check_contrast.THEME_CSS.read_text("utf-8"))["base"]
    for token, hex_value in SAMPLED_PALETTE.items():
        assert base[token] == hex_value


@pytest.mark.parametrize("row", check_contrast.check(), ids=lambda r: f"{r[0]}:{r[1]}/{r[3]}")
def test_text_pairs_meet_wcag_aa(row) -> None:
    theme, fg, fg_hex, bg, bg_hex, ratio = row
    assert ratio >= check_contrast.AA_NORMAL_TEXT, f"{theme}: {fg} on {bg} is {ratio:.2f}:1"


def test_contrast_formula_known_values() -> None:
    assert check_contrast.contrast("#000000", "#ffffff") == pytest.approx(21.0)
    assert check_contrast.contrast("#777777", "#777777") == pytest.approx(1.0)
