# 🔗 Sources — every official reference used in the course

Collected from each chapter's **📚 Sources** section. Every link was opened and checked
against the claim it supports while the course was written (October 2026). Documentation
moves; if a link breaks, please open an issue.

## [🧭 Chapter 00 · How to read this repo](section-1-orientation/chapter-00-how-to-read-this-repo.md)

- Pro Git book — [Tagging](https://git-scm.com/book/en/v2/Git-Basics-Tagging) (annotated tags, checking out tags)
- Git reference — [git switch](https://git-scm.com/docs/git-switch) (`--detach`, `-c`)
- GitHub Docs — [Basic writing and formatting syntax](https://docs.github.com/en/get-started/writing-on-github/getting-started-with-writing-and-formatting-on-github/basic-writing-and-formatting-syntax) (alerts, task lists, relative links)
- GitHub Docs — [Creating diagrams](https://docs.github.com/en/get-started/writing-on-github/working-with-advanced-formatting/creating-diagrams) (Mermaid in Markdown)

## [🧰 Chapter 01 · Setup: Python, Git and a virtual environment](section-1-orientation/chapter-01-setup-python-git-and-venv.md)

- Python docs — [Using Python on Windows](https://docs.python.org/3/using/windows.html) (install manager, `py` command)
- Python docs — [Using Python on macOS](https://docs.python.org/3/using/mac.html) (installer, Install Certificates)
- Python docs — [venv](https://docs.python.org/3/library/venv.html) (create/activate per shell, PowerShell execution policy)
- pip docs — [pip install](https://pip.pypa.io/en/stable/cli/pip_install/) and [requirements file format](https://pip.pypa.io/en/stable/reference/requirements-file-format/)
- Python Packaging — [pyproject.toml specification](https://packaging.python.org/en/latest/specifications/pyproject-toml/)
- GitHub Docs — [Email addresses reference (noreply address)](https://docs.github.com/en/account-and-profile/reference/email-addresses-reference) · [Setting your commit email address](https://docs.github.com/en/account-and-profile/setting-up-and-managing-your-personal-account-on-github/managing-email-preferences/setting-your-commit-email-address)
- Git — [Install on macOS](https://git-scm.com/install/mac) · [Install on Windows](https://git-scm.com/install/windows) · [First-time setup](https://git-scm.com/book/en/v2/Getting-Started-First-Time-Git-Setup)
- Git reference — [gitattributes](https://git-scm.com/docs/gitattributes) · [git merge `--no-ff`](https://git-scm.com/docs/git-merge)
- [Conventional Commits 1.0.0](https://www.conventionalcommits.org/en/v1.0.0/)
- pytest — [Get started](https://docs.pytest.org/en/stable/getting-started.html) · Ruff — [formatter](https://docs.astral.sh/ruff/formatter/) and [linter](https://docs.astral.sh/ruff/linter/)

## [🗺️ Chapter 02 · Architecture and data flow](section-1-orientation/chapter-02-architecture-and-data-flow.md)

- GitHub Docs — [Creating diagrams](https://docs.github.com/en/get-started/writing-on-github/working-with-advanced-formatting/creating-diagrams)
- Mermaid — [Introduction](https://mermaid.js.org/intro/) (flowchart, sequence, ER and git graph syntaxes)
- Flask — [Application factories](https://flask.palletsprojects.com/en/stable/patterns/appfactories/) (why `create_app()` makes testing easy)
- pytest — [How to parametrize tests](https://docs.pytest.org/en/stable/how-to/parametrize.html)

## [🗄️ Chapter 03 · SQLite storage](section-2-data-and-logic/chapter-03-sqlite-storage.md)

- Python docs — [sqlite3](https://docs.python.org/3/library/sqlite3.html) (placeholders, `Row`, transactions and the context manager, threads)
- SQLite — [Foreign key support](https://sqlite.org/foreignkeys.html) · [PRAGMA user_version](https://sqlite.org/pragma.html#pragma_user_version)
- Python docs — [dataclasses](https://docs.python.org/3/library/dataclasses.html)
- freedesktop.org — [XDG Base Directory Specification](https://specifications.freedesktop.org/basedir-spec/latest/)
- pytest — [tmp_path](https://docs.pytest.org/en/stable/how-to/tmp_path.html) · [monkeypatch](https://docs.pytest.org/en/stable/how-to/monkeypatch.html)

## [🧠 Chapter 04 · Service layer and unit tests](section-2-data-and-logic/chapter-04-service-layer-and-unit-tests.md)

- pytest — [How to use fixtures](https://docs.pytest.org/en/stable/how-to/fixtures.html) · [parametrize](https://docs.pytest.org/en/stable/how-to/parametrize.html) · [markers](https://docs.pytest.org/en/stable/how-to/mark.html) · [the `pytest_collection_modifyitems` example](https://docs.pytest.org/en/stable/example/markers.html)
- pytest — [Configuration (`[tool.pytest]` in pyproject.toml)](https://docs.pytest.org/en/stable/reference/customize.html)
- Python docs — [dataclasses](https://docs.python.org/3/library/dataclasses.html) (`@property` on a dataclass works like on any class)

## [🧭 Chapter 05 · Flask routes and templates](section-3-web-ui/chapter-05-flask-routes-and-templates.md)

- Flask — [Templates](https://flask.palletsprojects.com/templating/) (autoescaping, `|safe`, `Markup`) · [Testing](https://flask.palletsprojects.com/en/stable/testing/) · [Development server](https://flask.palletsprojects.com/en/stable/server/) · [Application factories](https://flask.palletsprojects.com/en/stable/patterns/appfactories/)
- Jinja — [Template Designer Documentation](https://jinja.palletsprojects.com/en/stable/templates/) (`extends`, `block`, `include`, filters)
- Waitress — [Documentation](https://docs.pylonsproject.org/projects/waitress/en/stable/) · [Arguments](https://docs.pylonsproject.org/projects/waitress/en/stable/arguments.html) · Flask — [Deploying with Waitress](https://flask.palletsprojects.com/en/stable/deploying/waitress/)
- OWASP — [CSRF Prevention Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Cross-Site_Request_Forgery_Prevention_Cheat_Sheet.html) (Fetch Metadata first, Origin as fallback)
- MDN — [Origin header](https://developer.mozilla.org/en-US/docs/Web/HTTP/Reference/Headers/Origin) · [Sec-Fetch-Site](https://developer.mozilla.org/en-US/docs/Web/HTTP/Reference/Headers/Sec-Fetch-Site)
- NCC Group — [Preventing DNS rebinding attacks](https://github.com/nccgroup/singularity/wiki/Preventing-DNS-Rebinding-Attacks) (allow-list the `Host` header for loopback services)
- Python docs — [webbrowser](https://docs.python.org/3/library/webbrowser.html)

## [💜 Chapter 06 · Design system: CSS tokens and a little JavaScript](section-3-web-ui/chapter-06-design-system-css-and-js.md)

- WCAG 2.2 — [Understanding Contrast (Minimum)](https://www.w3.org/WAI/WCAG22/Understanding/contrast-minimum.html) · [Technique G18 (the formula)](https://www.w3.org/WAI/WCAG22/Techniques/general/G18)
- MDN — [Using CSS custom properties](https://developer.mozilla.org/en-US/docs/Web/CSS/Guides/Cascading_variables/Using_custom_properties) · [prefers-color-scheme](https://developer.mozilla.org/en-US/docs/Web/CSS/Reference/At-rules/@media/prefers-color-scheme) · [color-mix()](https://developer.mozilla.org/en-US/docs/Web/CSS/Reference/Values/color_value/color-mix)
- MDN — [localStorage](https://developer.mozilla.org/en-US/docs/Web/API/Window/localStorage) · [ARIA checkbox role](https://developer.mozilla.org/en-US/docs/Web/Accessibility/ARIA/Reference/Roles/checkbox_role)

## [🔎 Chapter 07 · Full-text search with SQLite FTS5](section-3-web-ui/chapter-07-full-text-search-fts5.md)

- SQLite — [FTS5](https://sqlite.org/fts5.html) (external content tables, triggers, `rebuild`, `snippet()`, `bm25()`/`rank`, prefix queries)
- SQLite — [LIKE and ESCAPE](https://sqlite.org/lang_expr.html#like)
- MarkupSafe — [Documentation](https://markupsafe.palletsprojects.com/en/stable/) (`escape`, `Markup`)
- Flask — [Templates: controlling autoescaping](https://flask.palletsprojects.com/templating/)

## [🎭 Chapter 08 · Playwright foundations](section-4-automation/chapter-08-playwright-foundations.md)

- Playwright for Python — [Installation](https://playwright.dev/python/docs/intro) · [Pytest plugin reference](https://playwright.dev/python/docs/test-runners) (`--headed`, `--slowmo`, `--base-url`, fixtures)
- Playwright — [Locators](https://playwright.dev/python/docs/locators) · [Assertions](https://playwright.dev/python/docs/test-assertions) · [Page Object Models](https://playwright.dev/python/docs/pom)
- Playwright — [Browsers](https://playwright.dev/python/docs/browsers) (`install`, `--with-deps`, cache folders) · [Debugging](https://playwright.dev/python/docs/debug) (`PWDEBUG`) · [Codegen](https://playwright.dev/python/docs/codegen)
- pytest — [Fixtures (scope, autouse, yield)](https://docs.pytest.org/en/stable/how-to/fixtures.html) · Werkzeug — [Serving (port 0)](https://werkzeug.palletsprojects.com/en/stable/serving/)

## [🎪 Chapter 09 · Playwright showcase — automation beyond clicking](section-4-automation/chapter-09-playwright-showcase.md)

- Playwright — [Network (route, abort, continue)](https://playwright.dev/python/docs/network) · [APIRequestContext](https://playwright.dev/python/docs/api/class-apirequestcontext) (shared cookie jar, JSON `data`)
- Playwright — [Emulation](https://playwright.dev/python/docs/emulation) (`color_scheme`, viewport, `java_script_enabled`) · [Input](https://playwright.dev/python/docs/input) (`fill` vs `press_sequentially`) · [Keyboard](https://playwright.dev/python/docs/api/class-keyboard) (`ControlOrMeta`)
- Playwright — [Assertions](https://playwright.dev/python/docs/test-assertions) · [Screenshots](https://playwright.dev/python/docs/screenshots) · [Trace viewer](https://playwright.dev/python/docs/trace-viewer)

## [🚀 Chapter 10 · CI and releases](section-5-ship-and-share/chapter-10-ci-and-releases.md)

- GitHub Docs — [Workflow syntax](https://docs.github.com/en/actions/reference/workflows-and-actions/workflow-syntax) · [Matrix jobs](https://docs.github.com/en/actions/how-tos/write-workflows/choose-what-workflows-do/run-job-variations) · [Concurrency](https://docs.github.com/en/actions/how-tos/write-workflows/choose-when-workflows-run/control-workflow-concurrency) · [Contexts (`needs.*.result`)](https://docs.github.com/en/actions/reference/workflows-and-actions/contexts)
- GitHub Docs — [GitHub-hosted runners](https://docs.github.com/en/actions/reference/runners/github-hosted-runners) · [GitHub CLI in workflows](https://docs.github.com/en/actions/how-tos/write-workflows/choose-what-workflows-do/use-github-cli) · [Storing workflow data as artifacts](https://docs.github.com/en/actions/tutorials/store-and-share-data) · [Status badges](https://docs.github.com/en/actions/how-tos/monitor-workflows/add-a-status-badge)
- GitHub Docs — [About protected branches](https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/managing-protected-branches/about-protected-branches) · [About releases](https://docs.github.com/en/repositories/releasing-projects-on-github/about-releases)
- GitHub CLI — [gh release create](https://cli.github.com/manual/gh_release_create)
- PyInstaller — [Using PyInstaller](https://pyinstaller.org/en/stable/usage.html) · [Requirements and "not a cross-compiler" (PyPI page)](https://pypi.org/project/pyinstaller/)
- Apple — [Open a Mac app from an unknown developer](https://support.apple.com/guide/mac-help/open-a-mac-app-from-an-unknown-developer-mh40616/mac) · Microsoft — [Microsoft Defender SmartScreen](https://learn.microsoft.com/en-us/windows/security/operating-system-security/virus-and-threat-protection/microsoft-defender-smartscreen/)

## [🍴 Chapter 11 · Fork, extend and audit](section-5-ship-and-share/chapter-11-fork-extend-and-audit.md)

- GitHub Docs — [Fork a repository](https://docs.github.com/en/pull-requests/collaborating-with-pull-requests/working-with-forks/fork-a-repo) · GitHub CLI — [gh repo fork](https://cli.github.com/manual/gh_repo_fork) · [Creating a template repository](https://docs.github.com/en/repositories/creating-and-managing-repositories/creating-a-template-repository)
- GitHub Docs — [Dependabot options reference](https://docs.github.com/en/code-security/dependabot/working-with-dependabot/dependabot-options-reference) · [Supported ecosystems](https://docs.github.com/en/code-security/dependabot/ecosystems-supported-by-dependabot/supported-ecosystems-and-repositories)
- Python docs — [importlib.metadata](https://docs.python.org/3/library/importlib.metadata.html)
- [Semantic Versioning 2.0.0](https://semver.org/) · [Keep a Changelog 1.1.0](https://keepachangelog.com/en/1.1.0/)
- Playwright — [Browsers](https://playwright.dev/python/docs/browsers)

## [🌿 Git guide](GIT-GUIDE.md)

- [Pro Git book](https://git-scm.com/book/en/v2) — especially [First-time setup](https://git-scm.com/book/en/v2/Getting-Started-First-Time-Git-Setup), [Branching and merging](https://git-scm.com/book/en/v2/Git-Branching-Basic-Branching-and-Merging) and [Tagging](https://git-scm.com/book/en/v2/Git-Basics-Tagging)
- Git reference — [git switch](https://git-scm.com/docs/git-switch) · [git merge](https://git-scm.com/docs/git-merge) · [git restore](https://git-scm.com/docs/git-restore) · [git revert](https://git-scm.com/docs/git-revert) · [gitattributes](https://git-scm.com/docs/gitattributes)
- GitHub Docs — [Email addresses reference (noreply address)](https://docs.github.com/en/account-and-profile/reference/email-addresses-reference)
- [Conventional Commits 1.0.0](https://www.conventionalcommits.org/en/v1.0.0/)

[⬅️ Learning path](README.md)
