"""Chapter 02: the docs are tested like code.

1. Every relative link in every Markdown file points at a file that exists.
2. Every code excerpt marked with <!-- snippet: path --> still matches the
   real file, line for line. If someone changes the code and forgets the docs,
   this test fails and names the chapter.
3. Every chapter has the same skeleton (goal … sources).
"""

from __future__ import annotations

import re
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[2]
SKIP_DIRS = {".venv", "venv", "node_modules", ".git", "build", "dist", "test-results"}
MARKDOWN = sorted(p for p in ROOT.rglob("*.md") if not SKIP_DIRS & set(p.relative_to(ROOT).parts))
CHAPTERS = sorted(ROOT.glob("docs/section-*/chapter-*.md"))

LINK = re.compile(r"!?\[[^\]]*\]\(([^)\s]+)\)")
HTML_LINK = re.compile(r'(?:href|src)="([^"]+)"')
SNIPPET = re.compile(r"<!-- snippet: ([^ ]+) -->\n```[\w-]*\n(.*?)```", re.DOTALL)
REQUIRED_HEADINGS = ["## 🎯", "## 📝 Notes", "## 🧪 Your turn", "## 📚 Sources"]


def ids(paths: list[Path]) -> list[str]:
    return [p.relative_to(ROOT).as_posix() for p in paths]


@pytest.mark.parametrize("md", MARKDOWN, ids=ids(MARKDOWN))
def test_relative_links_resolve(md: Path) -> None:
    text = re.sub(r"```.*?```", "", md.read_text(encoding="utf-8"), flags=re.DOTALL)
    broken = []
    for target in LINK.findall(text) + HTML_LINK.findall(text):
        if re.match(r"^(https?:|mailto:|#)", target):
            continue
        path = target.split("#", 1)[0]
        if path and not (md.parent / path).exists():
            broken.append(target)
    assert broken == [], f"{md.relative_to(ROOT)} links to missing files: {broken}"


@pytest.mark.parametrize("md", MARKDOWN, ids=ids(MARKDOWN))
def test_code_snippets_match_the_source(md: Path) -> None:
    for rel, block in SNIPPET.findall(md.read_text(encoding="utf-8")):
        source_lines = {line.strip() for line in (ROOT / rel).read_text("utf-8").splitlines()}
        for line in block.splitlines():
            stripped = line.strip()
            if stripped and stripped not in {"...", "…", "# ...", "# …"}:
                assert stripped in source_lines, f"{md.name}: '{stripped}' is not in {rel}"


@pytest.mark.parametrize("chapter", CHAPTERS, ids=ids(CHAPTERS))
def test_chapter_skeleton(chapter: Path) -> None:
    text = chapter.read_text(encoding="utf-8")
    missing = [heading for heading in REQUIRED_HEADINGS if heading not in text]
    assert missing == [], f"{chapter.name} is missing sections: {missing}"
