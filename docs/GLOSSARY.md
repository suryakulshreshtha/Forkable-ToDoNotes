# 📖 Glossary

Words that appear in the course, in plain language. The chapter where each one matters most is in brackets.

| Term | Meaning |
|---|---|
| **Annotated tag** | A Git tag that stores who made it, when, and a message — used for every `chNN` checkpoint. (00, 01) |
| **API (JSON)** | URLs under `/api/…` that send and receive data as JSON instead of HTML pages. (05) |
| **Application factory** | A function (`create_app`) that builds a new, configured Flask app each time it is called. (05) |
| **Autoescaping** | Jinja turning `<` into `&lt;` (and so on) in `{{ … }}`, so user text can never become HTML. (05, 07) |
| **BM25 / rank** | The relevance score FTS5 uses; smaller is better, so `ORDER BY rank` is best-first. (07) |
| **CSRF** | Cross-Site Request Forgery: another website making *your* browser send a request to *your* app. (05) |
| **Debounce** | Waiting until typing pauses before acting (autosave waits 600 ms). (06) |
| **Design token** | A named value (`--plum`, `--primary`) used instead of raw colours. (06) |
| **DNS rebinding** | A trick where a website re-points its own domain at `127.0.0.1` to reach local apps. (05) |
| **Editable install** | `pip install -e .` — the package points at your `src/` folder, so edits apply instantly. (01) |
| **End-to-end (e2e) test** | A test that drives the real app through a real browser, like a user would. (08) |
| **External content table** | An FTS5 table that stores only the index and reads text from another table. (07) |
| **Fixture** | A pytest function that prepares something a test needs; requested by argument name. (04) |
| **FTS5** | SQLite's full-text search engine, built into most SQLite builds. (07) |
| **Gate job** | One CI job that passes only when all required jobs passed. (10) |
| **Locator** | Playwright's lazy description of how to find an element (by role, label, text…). (08) |
| **Loopback (`127.0.0.1`)** | The address that always means "this computer"; nothing else on the network can reach it. (05) |
| **Marker** | A pytest label (`unit`, `e2e`, `offline`) used to select tests with `-m`. (04) |
| **Matrix** | A CI job repeated for each combination, e.g. 3 OSes × 2 Python versions. (10) |
| **Migration** | A numbered script that upgrades an existing database's schema. (03) |
| **Page object** | A class that wraps one screen's locators and actions for tests. (08) |
| **Parameter (`?`)** | A placeholder in SQL that receives a value separately — the cure for SQL injection. (03) |
| **Post/Redirect/Get** | Answer every form POST with a redirect, so refresh never re-submits. (02, 05) |
| **Progressive enhancement** | Build with plain HTML first; JavaScript only adds conveniences. (06) |
| **Service layer** | Code that holds the rules, between the web layer and storage. (04) |
| **Supply chain** | All the packages (and their packages) your project installs and ships. (11) |
| **Virtual environment** | A per-project folder of Python packages (`.venv`). (01) |
| **Web-first assertion** | Playwright's `expect(...)`, which retries until true instead of failing instantly. (08) |
| **WSGI** | The standard interface between Python web apps and web servers (Flask ↔ Waitress). (05) |

[⬅️ Learning path](README.md)
