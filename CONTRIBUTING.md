# 🤝 Contributing

Thanks for wanting to improve **Forkable-ToDoNotes**! This repo is a *learning*
project, so clarity beats cleverness every time.

## 🌿 Workflow

1. Fork the repo (or use **Use this template**) and clone your copy.
2. Create a branch: `git switch -c fix/short-description`.
3. Make the change **and** a test that proves it.
4. Run the checks locally:

<table>
<tr><th width="50%">🍎 macOS · Terminal (zsh)</th><th width="50%">🪟 Windows · PowerShell</th></tr>
<tr>
<td>

```bash
ruff check . && ruff format --check .
python -m pytest
```

</td>
<td>

```powershell
ruff check . ; ruff format --check .
python -m pytest
```

</td>
</tr>
<tr><td colspan="2" align="center">✅ <b>Same command on both</b> — Git and pip behave identically here; only the shell differs.</td></tr>
</table>

5. Commit with a [Conventional Commit](https://www.conventionalcommits.org/en/v1.0.0/) message, e.g. `fix(search): ignore empty queries`.
6. Push and open a pull request.

## ✍️ Writing docs

- Each chapter follows the same skeleton (goal → concepts → diagram → build → run → git → notes → exercise → sources).
- Show commands for **both** macOS and Windows using the two-column tables.
- Link to **official documentation** for every claim about a tool. If you could not verify something, say so.

