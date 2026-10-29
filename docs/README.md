# 📚 The learning path

> Build **Forkable-ToDoNotes** from an empty folder to a tested, downloadable
> app — one chapter at a time. Every chapter ends with a Git **tag**, so you can
> jump to the exact code of any step with `git switch --detach chNN`.

<p align="center"><img src="assets/banner.svg" alt="Forkable-ToDoNotes banner" width="100%"></p>

## 🧭 Sections and chapters

| Section | Chapter | You will build / learn | ⏱️ | 🏷️ Tag |
|---|---|---|---|---|
| **1 · 🧭 Orientation** | [00 · How to read this repo](section-1-orientation/chapter-00-how-to-read-this-repo.md) | The map, the conventions, how tags work | 15 min | `ch00` |
| | [01 · Setup: Python, Git, venv](section-1-orientation/chapter-01-setup-python-git-and-venv.md) | A working toolchain on 🍎 and 🪟, first test passing | 45 min | `ch01` |
| | [02 · Architecture & data flow](section-1-orientation/chapter-02-architecture-and-data-flow.md) | Layers, diagrams-as-code, docs that are tested | 30 min | `ch02` |
| **2 · 🗄️ Data & logic** | [03 · SQLite storage](section-2-data-and-logic/chapter-03-sqlite-storage.md) | Schema, migrations, parameters, transactions | 60 min | `ch03` |
| | [04 · Service layer & unit tests](section-2-data-and-logic/chapter-04-service-layer-and-unit-tests.md) | Business rules, pytest fixtures, parametrize | 45 min | `ch04` |
| **3 · 🎨 Web UI** | [05 · Flask routes & templates](section-3-web-ui/chapter-05-flask-routes-and-templates.md) | Pages, forms, a JSON API, local-only safety | 75 min | `ch05` |
| | [06 · Design system: CSS & JS](section-3-web-ui/chapter-06-design-system-css-and-js.md) | The purple palette, themes, contrast tests, autosave | 60 min | `ch06` |
| | [07 · Full-text search (FTS5)](section-3-web-ui/chapter-07-full-text-search-fts5.md) | Prefix search, ranking, safe highlighting | 60 min | `ch07` |
| **4 · 🎭 Automation** | [08 · Playwright foundations](section-4-automation/chapter-08-playwright-foundations.md) | Live server, page objects, first browser tests | 60 min | `ch08` |
| | [09 · Playwright showcase](section-4-automation/chapter-09-playwright-showcase.md) | API+UI hybrids, offline proof, emulation, screenshots | 90 min | `ch09` |
| **5 · 🚀 Ship & share** | [10 · CI & releases](section-5-ship-and-share/chapter-10-ci-and-releases.md) | GitHub Actions gate, PyInstaller apps for 3 OSes | 60 min | `ch10` |
| | [11 · Fork, extend & audit](section-5-ship-and-share/chapter-11-fork-extend-and-audit.md) | Make it yours, supply-chain audit, where next | 45 min | `ch11` |

## 📌 Suggested reading order

```text
Section 1  🧭  00 → 01 → 02     read the map, set up, see the whole design
Section 2  🗄️  03 → 04          data first, rules second (no web yet!)
Section 3  🎨  05 → 06 → 07     pages, then looks, then search
Section 4  🎭  08 → 09          prove it works in a real browser
Section 5  🚀  10 → 11          ship it, then make it yours
```

## 🧰 Reference pages

| Page | Use it when… |
|---|---|
| [🌿 GIT-GUIDE.md](GIT-GUIDE.md) | you need a Git command for 🍎 macOS or 🪟 Windows |
| [📖 GLOSSARY.md](GLOSSARY.md) | a word like *WSGI*, *fixture* or *FTS5* is new to you |
| [📝 NOTES.md](NOTES.md) | you want every chapter's key notes on one page |
| [🔗 SOURCES.md](SOURCES.md) | you want the official documentation behind a claim |
| [🛡️ SUPPLY-CHAIN.md](SUPPLY-CHAIN.md) | you want to know exactly what gets installed, and from whom |
| [⬅️ Project README](../README.md) | you want the quick start and the screenshots |
