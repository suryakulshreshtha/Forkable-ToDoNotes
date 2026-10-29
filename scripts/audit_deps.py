"""List every installed Python package with who publishes it — and flag policy hits.

Why: "pip install flask" quietly installs six more packages. Before you ship,
you should know every one of them, who maintains it, and under which licence.

Usage (inside the project's virtual environment):
    python scripts/audit_deps.py                      # table in the terminal
    python scripts/audit_deps.py --markdown out.md    # also write a Markdown table
    python scripts/audit_deps.py --policy scripts/vendor_policy.txt

The policy file lists organisations your project has decided not to depend on
(one per line). A package is flagged when any of them appears in its name,
author, maintainer, e-mail or URLs. Exit code 1 means "flagged: review needed".

Limits, stated honestly: package metadata says who PUBLISHES a package, not
who contributed every line. This is a first filter for a human, not a verdict.
"""

from __future__ import annotations

import argparse
import sys
from dataclasses import dataclass
from importlib.metadata import Distribution, distributions
from pathlib import Path

SKIP = {"pip", "setuptools", "wheel"}
DEFAULT_POLICY = Path(__file__).with_name("vendor_policy.txt")


@dataclass
class Package:
    name: str
    version: str
    publisher: str
    url: str
    license: str

    def haystack(self) -> str:
        return " ".join([self.name, self.publisher, self.url]).lower()


def describe(dist: Distribution) -> Package:
    meta = dist.metadata
    publisher = (
        meta.get("Author")
        or meta.get("Maintainer")
        or meta.get("Author-email")
        or meta.get("Maintainer-email")
        or "-"
    )
    urls = [entry.split(",", 1)[-1].strip() for entry in (meta.get_all("Project-URL") or [])]
    fallback = urls[0] if urls else "-"
    url = meta.get("Home-page") or next((u for u in urls if "github" in u), fallback)
    licence = meta.get("License-Expression") or (meta.get("License") or "-").splitlines()[0]
    return Package(meta["Name"], dist.version, " ".join(publisher.split()), url, licence[:40])


def load_policy(path: Path) -> list[str]:
    if not path.exists():
        return []
    lines = path.read_text(encoding="utf-8").splitlines()
    return [line.strip().lower() for line in lines if line.strip() and not line.startswith("#")]


def main() -> int:
    parser = argparse.ArgumentParser(description="Audit installed Python packages.")
    parser.add_argument("--markdown", type=Path, help="write a Markdown table to this file")
    parser.add_argument("--policy", type=Path, default=DEFAULT_POLICY, help="vendor policy file")
    args = parser.parse_args()

    unique = {}
    for dist in distributions():
        name = dist.metadata["Name"]
        if name.lower() not in SKIP:
            unique[name.lower()] = describe(dist)  # one row per package name
    packages = sorted(unique.values(), key=lambda p: p.name.lower())
    policy = load_policy(args.policy)
    flagged = [(p, term) for p in packages for term in policy if term in p.haystack()]

    for p in packages:
        print(f"{p.name:<28} {p.version:<12} {p.publisher[:34]:<36} {p.license}")
    print(f"\n{len(packages)} packages · policy terms checked: {len(policy)}")
    for p, term in flagged:
        print(f"🚩 {p.name} matches policy term '{term}' — review before shipping.")
    if not flagged:
        print("✅ No package matches the vendor policy.")

    if args.markdown:
        rows = [
            "| Package | Version | Publisher (from metadata) | Licence | Source |",
            "|---|---|---|---|---|",
        ]
        for p in packages:
            publisher = p.publisher.replace("|", "/")
            rows.append(f"| `{p.name}` | {p.version} | {publisher} | {p.license} | {p.url} |")
        args.markdown.write_text("\n".join(rows) + "\n", encoding="utf-8")
        print(f"📝 Wrote {args.markdown}")
    return 1 if flagged else 0


if __name__ == "__main__":
    sys.exit(main())
