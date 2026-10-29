# 🍴 Chapter 11 · Fork, extend and audit

> **Section 5 · Ship & share** · ⏱️ 45 min · 🏷️ checkpoint tag: `ch11`

## 🎯 Goal

Make the project **yours**: start a copy the right way, know exactly which packages you ship
and who publishes them, keep them up to date safely, and pick a next feature to build.

## 🧠 Concepts

| Idea | In one sentence |
|---|---|
| **Fork** | A linked copy: you can send pull requests back and pull updates from the original (*upstream*). |
| **Template** | An unlinked fresh start: same files, **new** history. Best for "my own notes app". |
| **Supply chain** | Every package you install — and every package *they* install — is code you ship. |
| **Vendor policy** | A written list of organisations a project has decided not to depend on, checked automatically. |
| **Dependabot** | Opens a pull request when a pinned version has an update; CI then tests it for you. |
| **SemVer + changelog** | `MAJOR.MINOR.PATCH` tells users what changed; `CHANGELOG.md` tells them in words. |

## 🛠️ Build it

### 1 · Fork or template?

| You want to… | Use | Keeps history? | Can PR back? |
|---|---|---|---|
| Fix a typo in a chapter | **Fork** | ✅ | ✅ |
| Learn along with the chapter tags | **Fork**, then `git fetch upstream --tags` | ✅ | ✅ |
| Start your own app from the finished code | **Use this template** | ❌ fresh history | ❌ |

Forking from the command line, and staying in sync with the original:

<table>
<tr><th width="50%">🍎 macOS · Terminal (zsh)</th><th width="50%">🪟 Windows · PowerShell</th></tr>
<tr>
<td>

```bash
gh repo fork suryakulshreshtha/Forkable-ToDoNotes --clone   # needs GitHub CLI
cd Forkable-ToDoNotes
git remote -v          # "origin" = your fork. No "upstream" line? Add it:
git remote add upstream https://github.com/suryakulshreshtha/Forkable-ToDoNotes.git
git fetch upstream --tags                     # chapter tags ch00…ch11 included
git switch main && git merge upstream/main    # bring in new chapters/fixes
```

</td>
<td>

```powershell
gh repo fork suryakulshreshtha/Forkable-ToDoNotes --clone   # needs GitHub CLI
cd Forkable-ToDoNotes
git remote -v          # "origin" = your fork. No "upstream" line? Add it:
git remote add upstream https://github.com/suryakulshreshtha/Forkable-ToDoNotes.git
git fetch upstream --tags                     # chapter tags ch00…ch11 included
git switch main; git merge upstream/main      # bring in new chapters/fixes
```

</td>
</tr>
<tr><td colspan="2" align="center">✅ <b>Same command on both</b> — Git and pip behave identically here; only the shell differs.</td></tr>
</table>

Without the GitHub CLI: click **Fork** on GitHub, `git clone` your fork, then run the same
`git remote add upstream …` and `git fetch upstream --tags` lines.

### 2 · Know what you ship — [`scripts/audit_deps.py`](../../scripts/audit_deps.py)

<table>
<tr><th width="50%">🍎 macOS · Terminal (zsh)</th><th width="50%">🪟 Windows · PowerShell</th></tr>
<tr>
<td>

```bash
python scripts/audit_deps.py
python scripts/audit_deps.py --markdown docs/SUPPLY-CHAIN-table.md
```

</td>
<td>

```powershell
python scripts/audit_deps.py
python scripts/audit_deps.py --markdown docs/SUPPLY-CHAIN-table.md
```

</td>
</tr>
<tr><td colspan="2" align="center">✅ <b>Same command on both</b> — Git and pip behave identically here; only the shell differs.</td></tr>
</table>

It lists every installed package with its version, publisher and licence (read from the package's
own metadata with `importlib.metadata`), then checks each one against
[`scripts/vendor_policy.txt`](../../scripts/vendor_policy.txt). Exit code `1` means "flagged — a human should look".

<!-- snippet: scripts/audit_deps.py -->
```python
policy = load_policy(args.policy)
flagged = [(p, term) for p in packages for term in policy if term in p.haystack()]
```

This project's policy excludes dependencies from China-based technology vendors. The result for
the full development environment is recorded in [🛡️ SUPPLY-CHAIN.md](../SUPPLY-CHAIN.md):
**9 packages ship inside the app, 25 are used to develop it — 0 flagged.**

> [!IMPORTANT]
> Package metadata says who **publishes** a package, not who wrote every line. The audit is a
> first filter for a human review — read the table, don't just trust the exit code.

### 3 · Updates without surprises — [`.github/dependabot.yml`](../../.github/dependabot.yml)

Dependabot checks `pip` pins and GitHub Actions versions weekly and opens a pull request for each
update. The **CI gate** then runs the whole suite on it. Before merging, run the audit too.

### 4 · Version numbers that mean something

| Change | Bump | Example |
|---|---|---|
| A bug fix | PATCH | `1.0.0 → 1.0.1` |
| A new feature that breaks nothing | MINOR | `1.0.1 → 1.1.0` |
| Anything that breaks existing notes files or the API | MAJOR | `1.1.0 → 2.0.0` |

During the course each chapter tag carries version `0.N.0` (a 0.x version means "still being
built"). The finished app is `1.0.0`, recorded in [`CHANGELOG.md`](../../CHANGELOG.md).

## 💡 What to build next

| Idea | Difficulty | Revisit chapter |
|---|---|---|
| 🏷️ Tags/labels on notes (new table + filter) | ⭐⭐ | 03 · 05 |
| 🔎 Search checklist items too | ⭐⭐ | 07 |
| 📥 Import a JSON export (restore a backup) | ⭐⭐ | 04 · 05 |
| 🎨 A colour per note (the migration 2 exercise) | ⭐ | 03 · 06 |
| 📝 Render Markdown in note bodies — safely | ⭐⭐⭐ | 05 · 07 |
| 🖨️ "Print this note" stylesheet | ⭐ | 06 |
| ✍️ Sign the release builds | ⭐⭐⭐ | 10 |

## 🔗 Where next — the Forkable index

This repository is part of a series of `Forkable*` learning repos. The map lives at
**[suryakulshreshtha/SuryaKulshreshtha](https://github.com/suryakulshreshtha/SuryaKulshreshtha)**.
Natural next steps after this course:

| Repo | Why after this one |
|---|---|
| [ForkablePythonLearningShowcase](https://github.com/suryakulshreshtha/ForkablePythonLearningShowcase) | More test-automation fundamentals with Playwright + pytest |
| [Forkable04EyePythonPlaywrightLearning](https://github.com/suryakulshreshtha/Forkable04EyePythonPlaywrightLearning) | Larger suites: sharding, nightly runs, visual baselines in CI |
| [ForkablePythonProjectShowcase](https://github.com/suryakulshreshtha/ForkablePythonProjectShowcase) | A full UI + API framework with network mocking and Docker |

## 🌿 Git checkpoint

<table>
<tr><th width="50%">🍎 macOS · Terminal (zsh)</th><th width="50%">🪟 Windows · PowerShell</th></tr>
<tr>
<td>

```bash
git switch -c chapter/11-fork-extend-audit
git add scripts/audit_deps.py scripts/vendor_policy.txt .github
git commit -m "chore: dependency audit, vendor policy, Dependabot and templates"
git add docs CHANGELOG.md
git commit -m "docs: notes, sources, supply chain and the final chapter"
git switch main
git merge --no-ff chapter/11-fork-extend-audit -m "Merge chapter 11: fork, extend and audit"
git tag -a ch11 -m "Chapter 11 checkpoint: fork, extend and audit"
```

</td>
<td>

```powershell
git switch -c chapter/11-fork-extend-audit
git add scripts/audit_deps.py scripts/vendor_policy.txt .github
git commit -m "chore: dependency audit, vendor policy, Dependabot and templates"
git add docs CHANGELOG.md
git commit -m "docs: notes, sources, supply chain and the final chapter"
git switch main
git merge --no-ff chapter/11-fork-extend-audit -m "Merge chapter 11: fork, extend and audit"
git tag -a ch11 -m "Chapter 11 checkpoint: fork, extend and audit"
```

</td>
</tr>
<tr><td colspan="2" align="center">✅ <b>Same command on both</b> — Git and pip behave identically here; only the shell differs.</td></tr>
</table>

## 📝 Notes

> [!TIP]
> Turn on **Template repository** in your copy's Settings if you want others to start from it.
> Only repository admins can change that setting.

> [!WARNING]
> Branches created from a template have **unrelated histories** to the original: you cannot open
> pull requests between them. If you might contribute back, fork instead.

> [!NOTE]
> Playwright's browsers are downloaded from `cdn.playwright.dev` (with a Microsoft-hosted fallback);
> the Chromium build is Google's *Chrome for Testing*. That download is a development tool only —
> the shipped app contains no browser.

## 🧪 Your turn

1. Add `vendor_policy.txt` terms for your organisation and run the audit.
2. Pick one idea from the table, write the test first, and ship it as `v1.1.0` with a CHANGELOG entry.

## 📚 Sources

- GitHub Docs — [Fork a repository](https://docs.github.com/en/pull-requests/collaborating-with-pull-requests/working-with-forks/fork-a-repo) · GitHub CLI — [gh repo fork](https://cli.github.com/manual/gh_repo_fork) · [Creating a template repository](https://docs.github.com/en/repositories/creating-and-managing-repositories/creating-a-template-repository)
- GitHub Docs — [Dependabot options reference](https://docs.github.com/en/code-security/dependabot/working-with-dependabot/dependabot-options-reference) · [Supported ecosystems](https://docs.github.com/en/code-security/dependabot/ecosystems-supported-by-dependabot/supported-ecosystems-and-repositories)
- Python docs — [importlib.metadata](https://docs.python.org/3/library/importlib.metadata.html)
- [Semantic Versioning 2.0.0](https://semver.org/) · [Keep a Changelog 1.1.0](https://keepachangelog.com/en/1.1.0/)
- Playwright — [Browsers](https://playwright.dev/python/docs/browsers)

---

[⬅️ Chapter 10](chapter-10-ci-and-releases.md) · [📚 Learning path](../README.md) · 🎉 **You finished the course!** See [📝 NOTES.md](../NOTES.md) for a one-page recap.
