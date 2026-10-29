# 🛡️ Supply chain — exactly what gets installed, and from whom

> Recorded on **2026-10-29** by running [`scripts/audit_deps.py`](../scripts/audit_deps.py) in two
> **fresh, empty** virtual environments (Python 3.13, Linux). Re-run it yourself — versions move.

## 📋 Policy

This project does not depend on technology from China-based vendors. The list of organisations
is kept in [`scripts/vendor_policy.txt`](../scripts/vendor_policy.txt) and checked automatically.

> [!IMPORTANT]
> Package metadata states who **publishes** a package, not who contributed every line. The audit
> is a first filter for a human, not a verdict. Read the tables below — that is the point of them.

> [!NOTE]
> The *Publisher* column shows **names only**. Package metadata also carries maintainers' personal
> e-mail addresses; the audit uses them for the policy check but never prints or commits them.

## 📦 Runtime — what ships inside the app

Installed by `pip install -r requirements.txt`. These are the only third-party packages inside
the downloadable app built in Chapter 10.

| Package | Version | Publisher (from metadata) | Licence | Source |
|---|---|---|---|---|
| `blinker` | 1.9.0 | Jason Kirtland | - | https://github.com/pallets-eco/blinker/ |
| `click` | 8.5.0 | Pallets | BSD-3-Clause | https://github.com/pallets/click/ |
| `Flask` | 3.1.3 | Pallets | BSD-3-Clause | https://github.com/pallets/flask/ |
| `forkable-todonotes` | 1.0.0 | Surya Kulshreshtha | MIT | https://github.com/suryakulshreshtha/Forkable-ToDoNotes |
| `itsdangerous` | 2.2.0 | Pallets | - | https://github.com/pallets/itsdangerous/ |
| `Jinja2` | 3.1.6 | Pallets | - | https://github.com/pallets/jinja/ |
| `MarkupSafe` | 3.0.4 | Pallets | BSD-3-Clause | https://github.com/pallets/markupsafe/ |
| `waitress` | 3.0.2 | Zope Foundation and Contributors | ZPL 2.1 | https://github.com/Pylons/waitress |
| `Werkzeug` | 3.1.9 | Pallets | BSD-3-Clause | https://github.com/pallets/werkzeug/ |

**Result: 9 packages · 0 match the vendor policy.** The Python standard library provides
`sqlite3`, `argparse`, `webbrowser` and everything else.

## 🧪 Development — tests, lint and packaging

Installed by `pip install -r requirements-dev.txt` (includes the runtime set above).

| Package | Version | Publisher (from metadata) | Licence | Source |
|---|---|---|---|---|
| `altgraph` | 0.17.5 | Ronald Oussoren | MIT | https://altgraph.readthedocs.io |
| `blinker` | 1.9.0 | Jason Kirtland | - | https://github.com/pallets-eco/blinker/ |
| `click` | 8.5.0 | Pallets | BSD-3-Clause | https://github.com/pallets/click/ |
| `Flask` | 3.1.3 | Pallets | BSD-3-Clause | https://github.com/pallets/flask/ |
| `forkable-todonotes` | 1.0.0 | Surya Kulshreshtha | MIT | https://github.com/suryakulshreshtha/Forkable-ToDoNotes |
| `greenlet` | 3.5.6 | Alexey Borzenkov | MIT AND PSF-2.0 | https://github.com/python-greenlet/greenlet |
| `iniconfig` | 2.3.1 | Ronny Pfannschmidt, Holger Krekel | MIT | https://github.com/pytest-dev/iniconfig |
| `itsdangerous` | 2.2.0 | Pallets | - | https://github.com/pallets/itsdangerous/ |
| `Jinja2` | 3.1.6 | Pallets | - | https://github.com/pallets/jinja/ |
| `MarkupSafe` | 3.0.4 | Pallets | BSD-3-Clause | https://github.com/pallets/markupsafe/ |
| `packaging` | 26.3 | Donald Stufft | Apache-2.0 OR BSD-2-Clause | https://github.com/pypa/packaging |
| `playwright` | 1.64.1 | Microsoft Corporation | Apache-2.0 | https://github.com/Microsoft/playwright-python |
| `pluggy` | 1.7.0 | Holger Krekel | MIT | https://github.com/pytest-dev/pluggy |
| `pyee` | 14.0.0 | Josh Holbrook | MIT | https://github.com/jfhbrook/pyee |
| `Pygments` | 2.21.0 | Matthäus G. Chajdas | BSD-2-Clause | https://github.com/pygments/pygments |
| `pyinstaller` | 6.22.3 | Hartmut Goebel, Giovanni Bajo, David Vierra, David Cortesi, Martin Zibricky | GPLv2-or-later with a special exception  | https://github.com/pyinstaller/pyinstaller |
| `pyinstaller-hooks-contrib` | 2026.9 | Legorooj | - | https://github.com/pyinstaller/pyinstaller-hooks-contrib |
| `pytest` | 9.2.0 | Brianna Laugher, Bruno Oliveira, Floris Bruynooghe, Freya Bruhin, Holger Krekel, Others (See AUTHORS), Ronny Pfannschmidt | MIT | https://github.com/pytest-dev/pytest |
| `pytest-playwright` | 0.10.0 | Microsoft | Apache License | https://github.com/microsoft/playwright-pytest |
| `python-slugify` | 9.1.3 | Val Neekman | MIT | https://github.com/un33k/python-slugify |
| `ruff` | 0.17.3 | Astral Software Inc. | MIT | https://docs.astral.sh/ruff |
| `text-unidecode` | 1.3 | Mikhail Korobov | Artistic License | https://github.com/kmike/text-unidecode/ |
| `typing_extensions` | 4.16.0 | Guido van Rossum, Jukka Lehtosalo, Łukasz Langa, Michael Lee | PSF-2.0 | https://github.com/python/typing_extensions/issues |
| `waitress` | 3.0.2 | Zope Foundation and Contributors | ZPL 2.1 | https://github.com/Pylons/waitress |
| `Werkzeug` | 3.1.9 | Pallets | BSD-3-Clause | https://github.com/pallets/werkzeug/ |

**Result: 25 packages · 0 match the vendor policy.**

### Platform-specific extras (not visible in a Linux audit)

pip installs a few more packages only on certain systems. Their metadata was checked separately:

| Package | Installed on | Pulled in by | Publisher (from metadata) | Source |
|---|---|---|---|---|
| `colorama` | Windows | pytest | Jonathan Hartley | https://github.com/tartley/colorama |
| `pefile` | Windows | PyInstaller | Ero Carrera | https://github.com/erocarrera/pefile |
| `pywin32-ctypes` | Windows | PyInstaller | Enthought Inc. | https://github.com/enthought/pywin32-ctypes |
| `macholib` | macOS | PyInstaller | Ronald Oussoren | https://github.com/ronaldoussoren/macholib |

## 🎭 Non-Python downloads

| What | When | Downloaded from | Notes |
|---|---|---|---|
| Chromium for Playwright | `python -m playwright install chromium` (dev only) | `cdn.playwright.dev`, fallback `playwright.download.prss.microsoft.com` | The build is Google's *Chrome for Testing*; the URLs come from `playwright install --dry-run` |
| GitHub Actions (`actions/checkout@v7`, `setup-python@v7`, `upload-artifact@v7`, `download-artifact@v8`) | CI only | `github.com/actions/*` | Official actions published by GitHub |

The **running app downloads nothing** — proven on every CI run by
[`tests/e2e/test_offline.py`](../tests/e2e/test_offline.py).

## 🔁 Re-run the audit

<table>
<tr><th width="50%">🍎 macOS · Terminal (zsh)</th><th width="50%">🪟 Windows · PowerShell</th></tr>
<tr>
<td>

```bash
python scripts/audit_deps.py
python scripts/audit_deps.py --markdown audit.md
```

</td>
<td>

```powershell
python scripts/audit_deps.py
python scripts/audit_deps.py --markdown audit.md
```

</td>
</tr>
<tr><td colspan="2" align="center">✅ <b>Same command on both</b> — Git and pip behave identically here; only the shell differs.</td></tr>
</table>

[⬅️ Learning path](README.md)
