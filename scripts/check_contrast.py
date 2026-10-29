"""Check that every text/background pair in theme.css meets WCAG 2.x AA (4.5:1).

Usage:
    python scripts/check_contrast.py          # prints a table, exit code 1 on failure

How it works: it reads the CSS custom properties from theme.css, resolves
var(--x) references for each theme, and computes the WCAG contrast ratio
for the pairs listed in PAIRS. Only plain #rrggbb values are checked; borders
made with color-mix() are decoration, not text, so they are skipped.

Formula source: WCAG 2.2, "contrast ratio" and "relative luminance" definitions.
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

THEME_CSS = Path(__file__).resolve().parents[1] / "src" / "todonotes" / "static" / "theme.css"
AA_NORMAL_TEXT = 4.5

# (foreground token, background token) pairs that carry readable text.
PAIRS = [
    ("--text", "--bg"),
    ("--text", "--surface"),
    ("--text", "--surface-2"),
    ("--text", "--input-bg"),
    ("--text-muted", "--bg"),
    ("--text-muted", "--surface"),
    ("--link", "--bg"),
    ("--link", "--surface"),
    ("--on-primary", "--primary"),
    ("--on-primary", "--primary-hover"),
    ("--mark-text", "--mark-bg"),
    ("--on-danger", "--danger"),
]

BLOCK = re.compile(r"([^{}]+)\{([^{}]*)\}")
DECLARATION = re.compile(r"(--[\w-]+)\s*:\s*([^;]+);")
VAR = re.compile(r"^var\((--[\w-]+)\)$")


def parse_blocks(css: str) -> dict[str, dict[str, str]]:
    """Map each theme name to the custom properties declared for it."""
    css = re.sub(r"/\*.*?\*/", "", css, flags=re.DOTALL)  # drop comments
    blocks: dict[str, dict[str, str]] = {"base": {}, "dark": {}, "light": {}, "system-light": {}}
    for selector, body in BLOCK.findall(css):
        values = {name: " ".join(value.split()) for name, value in DECLARATION.findall(body)}
        if ":not([data-theme])" in selector:
            blocks["system-light"].update(values)
        elif 'data-theme="light"' in selector:
            blocks["light"].update(values)
        elif 'data-theme="dark"' in selector:
            blocks["dark"].update(values)
        elif selector.strip() == ":root":
            blocks["base"].update(values)
    return blocks


def themes(css: str) -> dict[str, dict[str, str]]:
    blocks = parse_blocks(css)
    dark = {**blocks["base"], **blocks["dark"]}
    return {
        "dark": dark,
        "light": {**dark, **blocks["light"]},
        "light (from OS setting)": {**dark, **blocks["system-light"]},
    }


def resolve(name: str, values: dict[str, str], depth: int = 0) -> str:
    value = values[name]
    match = VAR.match(value)
    if match and depth < 10:
        return resolve(match.group(1), values, depth + 1)
    return value


def luminance(hex_color: str) -> float:
    red, green, blue = (int(hex_color[i : i + 2], 16) / 255 for i in (1, 3, 5))

    def channel(c: float) -> float:
        return c / 12.92 if c <= 0.04045 else ((c + 0.055) / 1.055) ** 2.4

    return 0.2126 * channel(red) + 0.7152 * channel(green) + 0.0722 * channel(blue)


def contrast(foreground: str, background: str) -> float:
    lighter, darker = sorted((luminance(foreground), luminance(background)), reverse=True)
    return (lighter + 0.05) / (darker + 0.05)


def check(css: str | None = None) -> list[tuple[str, str, str, str, str, float]]:
    """Return rows of (theme, fg token, fg hex, bg token, bg hex, ratio)."""
    css = css if css is not None else THEME_CSS.read_text(encoding="utf-8")
    rows = []
    for theme, values in themes(css).items():
        for fg, bg in PAIRS:
            fg_hex, bg_hex = resolve(fg, values), resolve(bg, values)
            if fg_hex.startswith("#") and bg_hex.startswith("#"):
                rows.append((theme, fg, fg_hex, bg, bg_hex, contrast(fg_hex, bg_hex)))
    return rows


def main() -> int:
    rows = check()
    failures = 0
    print(f"{'theme':<26}{'foreground':<26}{'background':<28}ratio")
    for theme, fg, fg_hex, bg, bg_hex, ratio in rows:
        ok = ratio >= AA_NORMAL_TEXT
        failures += not ok
        mark = "✅" if ok else "❌"
        print(f"{theme:<26}{fg + ' ' + fg_hex:<26}{bg + ' ' + bg_hex:<28}{ratio:5.2f} {mark}")
    print(f"\n{len(rows) - failures}/{len(rows)} pairs meet WCAG AA ({AA_NORMAL_TEXT}:1).")
    return 1 if failures else 0


if __name__ == "__main__":
    sys.exit(main())
