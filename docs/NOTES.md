# 📝 Notes — the whole course on one page

The key takeaways of every chapter, collected for revision. Follow the links for the full story.

## 🧭 Section 1 · Orientation

| Ch | Remember this |
|---|---|
| [00](section-1-orientation/chapter-00-how-to-read-this-repo.md) | `git switch --detach chNN` jumps to a chapter; `git switch -c my-branch chNN` to experiment from it. `git diff chA chB` shows what a chapter changed. |
| [01](section-1-orientation/chapter-01-setup-python-git-and-venv.md) | macOS uses `python3`, Windows uses `py` — until the venv is active, then both say `python`. PowerShell may need `Set-ExecutionPolicy RemoteSigned -Scope CurrentUser` once. Ranges live in `pyproject.toml`, exact pins in `requirements*.txt`. `.gitattributes` keeps line endings sane across OSes. |
| [02](section-1-orientation/chapter-02-architecture-and-data-flow.md) | Three layers — web → service → storage — and arrows only point down. Diagrams are Mermaid text; docs are tested by `test_docs.py`. |

## 🗄️ Section 2 · Data & logic

| Ch | Remember this |
|---|---|
| [03](section-2-data-and-logic/chapter-03-sqlite-storage.md) | Always `?` parameters, never f-strings with user input. `PRAGMA foreign_keys = ON` on every connection. `with conn:` commits/rolls back but doesn't close — add `closing()`. Migrations are append-only; `PRAGMA user_version` remembers where a file is. |
| [04](section-2-data-and-logic/chapter-04-service-layer-and-unit-tests.md) | Rules live in the service; storage just stores. Fixtures chain (`tmp_path → db_path → repo → service`) so every test gets a fresh database. `--strict-markers` turns marker typos into errors. |

## 🎨 Section 3 · Web UI

| Ch | Remember this |
|---|---|
| [05](section-3-web-ui/chapter-05-flask-routes-and-templates.md) | Post/Redirect/Get for every form. Autoescaping protects `{{ … }}` — the `safe` filter and `Markup` are your responsibility. Bind to `127.0.0.1`, check `Host`, `Sec-Fetch-Site` and `Origin`. Use Waitress, not Flask's dev server. |
| [06](section-3-web-ui/chapter-06-design-system-css-and-js.md) | Palette tokens → semantic tokens → components. 4.5:1 contrast for normal text, measured by a test. Orchid is decoration only. JavaScript is optional by design. |
| [07](section-3-web-ui/chapter-07-full-text-search-fts5.md) | Quote every typed word: `"word"*`. Escape the snippet *then* add `<mark>`. Run `'rebuild'` after creating the index. Fall back to `LIKE` (with `ESCAPE`) when FTS5 is missing. |

## 🎭 Section 4 · Automation

| Ch | Remember this |
|---|---|
| [08](section-4-automation/chapter-08-playwright-foundations.md) | Live server on port 0 in a thread, `base_url` fixture, `clean_db` before each test. Locate by role/label. Never `sleep()` — use `expect()`. `--headed --slowmo 300` to watch; `PWDEBUG=1` to step through. |
| [09](section-4-automation/chapter-09-playwright-showcase.md) | `expect_response()` waits for a real API call. `page.request` seeds data fast. `context.route("**/*")` proves offline. `emulate_media()` + `to_have_css()` test the theme. Traces explain failures. |

## 🚀 Section 5 · Ship & share

| Ch | Remember this |
|---|---|
| [10](section-5-ship-and-share/chapter-10-ci-and-releases.md) | Require only the **CI gate** check. `permissions: contents: read` by default. PyInstaller builds per OS (`--collect-data todonotes` for templates). Tags `v*.*.*` release; `ch*` tags don't. Unsigned apps: Gatekeeper "Open Anyway", SmartScreen warning. |
| [11](section-5-ship-and-share/chapter-11-fork-extend-and-audit.md) | Fork to contribute, template to start fresh. Audit dependencies before adding them. SemVer + changelog for every release. |

[⬅️ Learning path](README.md)
