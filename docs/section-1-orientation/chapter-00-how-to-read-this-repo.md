# 🧭 Chapter 00 · How to read this repo

> **Section 1 · Orientation** · ⏱️ 15 min · 🏷️ checkpoint tag: `ch00`

## 🎯 Goal

By the end of this chapter you will know **what** you are going to build, **how**
the repository is organised, and **how to jump** to the exact code of any chapter.

## 📝 What you will build

**Forkable-ToDoNotes** is a notes + to-do app that runs entirely on your own computer:

| Feature | How it works | Chapter |
|---|---|---|
| ✍️ Notes with a title and body | SQLite database file in your user folder | 03 |
| ☑️ Checklists inside notes | A second table, linked to notes | 03 |
| 📏 Validation and sensible defaults | A *service layer* of plain Python rules | 04 |
| 🌐 A clean web interface | Flask serves HTML to your browser on `127.0.0.1` | 05 |
| 💜 Purple light/dark theme | CSS design tokens + contrast tests | 06 |
| 🔎 Instant search with highlights | SQLite's FTS5 full-text index | 07 |
| 🎭 Proof that it works | Playwright drives a real browser | 08–09 |
| 📦 Double-click app for macOS, Windows, Linux | PyInstaller + GitHub Actions | 10 |

It needs **no internet** once installed, has **no account**, and keeps your notes
in **one file you own**.

## 🗂️ How the repository is organised

```text
Forkable-ToDoNotes/
├── README.md            ← start page: quick start, screenshots, chapter cards
├── docs/                ← 📚 the course (you are here)
│   ├── README.md        ← the learning path: sections → chapters
│   ├── section-1-orientation/
│   ├── section-2-data-and-logic/
│   ├── section-3-web-ui/
│   ├── section-4-automation/
│   ├── section-5-ship-and-share/
│   ├── diagrams/        ← Mermaid sources (.mmd) + offline images (.svg)
│   └── assets/          ← banner, badges, palette, screenshots
├── src/todonotes/       ← the app (arrives in chapters 01 → 07)
├── tests/               ← unit tests + Playwright browser tests
├── scripts/             ← helper tools (contrast check, screenshots, audit, build)
└── .github/             ← CI and release workflows
```

Folders appear as you progress: at tag `ch00` only the docs exist; `src/` arrives in Chapter 01.

## 🏷️ Following along with Git tags

Each chapter is built on its own branch, merged into `main`, and marked with a
tag. A tag is a permanent bookmark on one commit, so `ch05` always means
"the code exactly as it was at the end of Chapter 05".

<table>
<tr><th width="50%">🍎 macOS · Terminal (zsh)</th><th width="50%">🪟 Windows · PowerShell</th></tr>
<tr>
<td>

```bash
# Get the repository (once)
git clone https://github.com/suryakulshreshtha/Forkable-ToDoNotes.git
cd Forkable-ToDoNotes

# See every checkpoint
git tag --list "ch*"

# Travel to the end of Chapter 05 (read-only "detached HEAD")
git switch --detach ch05

# Come back to the latest version
git switch main
```

</td>
<td>

```powershell
# Get the repository (once)
git clone https://github.com/suryakulshreshtha/Forkable-ToDoNotes.git
cd Forkable-ToDoNotes

# See every checkpoint
git tag --list "ch*"

# Travel to the end of Chapter 05 (read-only "detached HEAD")
git switch --detach ch05

# Come back to the latest version
git switch main
```

</td>
</tr>
<tr><td colspan="2" align="center">✅ <b>Same command on both</b> — Git and pip behave identically here; only the shell differs.</td></tr>
</table>

Want to see **only what one chapter changed**? Compare two tags:

<table>
<tr><th width="50%">🍎 macOS · Terminal (zsh)</th><th width="50%">🪟 Windows · PowerShell</th></tr>
<tr>
<td>

```bash
git diff --stat ch04 ch05     # which files changed
git diff ch04 ch05 -- src/    # the actual code changes
```

</td>
<td>

```powershell
git diff --stat ch04 ch05     # which files changed
git diff ch04 ch05 -- src/    # the actual code changes
```

</td>
</tr>
<tr><td colspan="2" align="center">✅ <b>Same command on both</b> — Git and pip behave identically here; only the shell differs.</td></tr>
</table>

## 🧱 How every chapter is laid out

| Block | What it gives you |
|---|---|
| 🎯 **Goal** | One paragraph: what exists at the end of the chapter |
| 🧠 **Concepts** | The ideas, in plain words, before any code |
| 🗺️ **Diagram** | How data flows — Mermaid, rendered by GitHub, with an offline SVG copy |
| 🛠️ **Build it** | The code, with its file path, and *why* it is written that way |
| ▶️ **Run it** | Commands in two columns: 🍎 macOS (zsh) and 🪟 Windows (PowerShell) |
| 🌿 **Git checkpoint** | The branch → commit → merge → tag steps for that chapter |
| 📝 **Notes** | Gotchas and tips (also collected in one place at the end of the course) |
| 🧪 **Your turn** | A small exercise to make the knowledge stick |
| 📚 **Sources** | Official documentation for every tool used |

## 🎨 Conventions used in the docs

- **Two columns** = the same step on 🍎 macOS and 🪟 Windows. When the command is identical,
  the table says **✅ Same command on both**; the columns are still shown so you never have to guess.
- `code in backticks` = something you type, a file name, or a value.
- Callout boxes:

> [!NOTE]
> Useful background you can skip on a first read.

> [!TIP]
> A shortcut or a better way to do something.

> [!WARNING]
> A common mistake — read this one.

## 📝 Notes

> [!IMPORTANT]
> A tag in **detached HEAD** state is for *reading and running*. If you want to
> experiment from a chapter, make a branch first: `git switch -c my-experiment ch05`.

> [!TIP]
> GitHub can show you any tag in the browser too: open the branch dropdown, choose
> the **Tags** tab, and pick `ch05`.

## 🧪 Your turn

1. Clone the repository and run `git tag --list`. How many chapter tags are there?
2. Run `git log --oneline --graph --decorate` and find where each `ch` tag sits.
3. Open [docs/README.md](../README.md) and pick the chapter that sounds most interesting.
   (Then come back and start at 01 anyway. 😉)

## 📚 Sources

- Pro Git book — [Tagging](https://git-scm.com/book/en/v2/Git-Basics-Tagging) (annotated tags, checking out tags)
- Git reference — [git switch](https://git-scm.com/docs/git-switch) (`--detach`, `-c`)
- GitHub Docs — [Basic writing and formatting syntax](https://docs.github.com/en/get-started/writing-on-github/getting-started-with-writing-and-formatting-on-github/basic-writing-and-formatting-syntax) (alerts, task lists, relative links)
- GitHub Docs — [Creating diagrams](https://docs.github.com/en/get-started/writing-on-github/working-with-advanced-formatting/creating-diagrams) (Mermaid in Markdown)

---

[📚 Learning path](../README.md) · Next: Chapter 01 arrives at tag `ch01`.
