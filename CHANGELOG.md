# Changelog

All notable changes to this project are documented here.
The format follows [Keep a Changelog 1.1.0](https://keepachangelog.com/en/1.1.0/),
and the project uses [Semantic Versioning](https://semver.org/).

## [Unreleased]

## [1.0.0] - 2026-10-29

### Added
- Course chapters 00–11 in five sections, each ending with a `chNN` Git tag (versions `0.1.0`–`0.11.0`).
- Notes with title, body and pin; checklists with tick/untick; Markdown and JSON export.
- SQLite storage with migrations; FTS5 full-text search with LIKE fallback.
- Flask web UI with a purple light/dark design system and WCAG AA contrast tests.
- Playwright end-to-end suite: journeys, API+UI hybrids, offline proof, theme contract, autosave.
- GitHub Actions CI (lint, unit matrix on 3 OSes × 2 Pythons, e2e, CI gate) and release builds.
- Dependency audit script with a vendor policy.
