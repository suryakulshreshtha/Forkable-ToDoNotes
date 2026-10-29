# 🤖 AGENTS.md — rules for AI coding agents working in this repository

Humans: this file is for automated assistants. You can read it too — it is the
same policy we would give a new teammate.

## ✅ Allowed

| Task | Conditions |
|---|---|
| **Address reviews** | Change code or docs to answer a review comment. Reply on the thread with what changed. |
| **Fix CI failures** | Make `ruff check .`, `ruff format --check .` and `pytest` pass. Never delete or skip a test to get green — fix the cause or explain why the test is wrong. |
| **Resolve conflicts** | Rebase or merge `main` into the branch and resolve conflicts, keeping both sides' intent. Re-run the full test suite afterwards. |

## ⛔ Not allowed

| Task | Why |
|---|---|
| **Merge pull requests** | A human owner reads the diff and presses the button. Always. |
| Push to `main` directly, move or delete tags | Chapter tags (`ch00` … `ch11`) are the learning path; moving them breaks it for every reader. |
| Add authorship/attribution lines for AI tools | Commits carry the human author's identity only. |
| Add a dependency without asking a maintainer first | Every package is reviewed for licence and vendor policy (automated in Chapter 11). |

## 🧭 House rules

- Keep the three layers separate: `web.py` → `service.py` → `storage.py`. No SQL outside `storage.py`.
- Commit messages follow [Conventional Commits](https://www.conventionalcommits.org/en/v1.0.0/).
