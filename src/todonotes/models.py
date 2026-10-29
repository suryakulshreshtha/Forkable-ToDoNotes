"""Plain data objects shared by every layer.

They hold data and a little presentation logic, but no SQL and no HTTP.
That keeps them easy to create in tests: ``Note(id=1, title="x", ...)``.
"""

from __future__ import annotations

from dataclasses import asdict, dataclass, field

UNTITLED = "Untitled note"


@dataclass
class ChecklistItem:
    id: int
    note_id: int
    text: str
    done: bool
    position: int

    def to_dict(self) -> dict:
        return asdict(self)


@dataclass
class Note:
    id: int
    title: str
    body: str
    pinned: bool
    created_at: str  # ISO 8601, UTC, e.g. "2026-10-29T07:15:00+00:00"
    updated_at: str
    items: list[ChecklistItem] = field(default_factory=list)

    @property
    def display_title(self) -> str:
        """The title, or the first line of the body, or a placeholder."""
        if self.title.strip():
            return self.title.strip()
        for line in self.body.splitlines():
            if line.strip():
                text = line.strip()
                return text if len(text) <= 60 else text[:57] + "…"
        return UNTITLED

    @property
    def done_count(self) -> int:
        return sum(1 for item in self.items if item.done)

    def to_dict(self) -> dict:
        data = asdict(self)
        data["display_title"] = self.display_title
        return data
