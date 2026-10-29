# 🔐 Security policy

## What this app does to protect you

| Protection | Where |
|---|---|
| Listens on `127.0.0.1` only — not reachable from your network | `src/todonotes/__main__.py` |
| Refuses requests whose `Host` is not `127.0.0.1`/`localhost` (DNS-rebinding defence) | `web.py → only_local_and_same_origin` |
| Refuses cross-site form posts using the browser's `Origin` header (CSRF defence) | same function |
| All SQL uses `?` parameters — no string-built queries with user input | `storage.py` |
| Templates auto-escape; search highlights escape **before** adding `<mark>` | `templates/`, `web.py → highlight` |
| No network calls, CDNs, fonts or analytics — proven by a Playwright test | `tests/e2e/test_offline.py` |
| Content-Security-Policy: scripts and styles only from the app itself, no inline script, no framing (`frame-ancestors 'none'`) — a Playwright test proves the app obeys it and the browser refuses an injected script | `web.py → add_security_headers`, `tests/e2e/test_csp.py` |
| `nosniff`, `same-origin` referrer policy, same-origin resource and opener policies, no caching of pages or the API | same function, `tests/unit/test_security_headers.py` |

## Reporting a vulnerability

Please **do not open a public issue**. Use GitHub's private reporting instead:
the repository's **Security** tab → **Report a vulnerability**. You will get an
answer as soon as the maintainer can look at it.
