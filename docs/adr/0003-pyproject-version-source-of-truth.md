# ADR 0003: Pyproject.toml as Version Source of Truth

- **Status**: Accepted
- **Date**: 2026-08-28

## Context
This project contains package manifests and documentation across multiple ecosystems: Python (`pyproject.toml`), Scryer Prolog (`bakage.toml`), SWI-Prolog (`pack.pl`), Tau Prolog (`package.json`), web metadata (`schema.org.jsonld`), and Markdown documentation (`README.md`, `CHANGELOG.md`).

## Decision
[`pyproject.toml`](file:///home/doug/code/prolog-agent-toolkit/pyproject.toml) is designated as the single canonical source of truth for the project version string.

## Rationale
1. **Single Source of Truth**: Eliminates version mismatch bugs and manual editing across multiple files.
2. **Automated Synchronization**: Running `prolog-agent release [--version X.Y.Z]` reads or updates `pyproject.toml` and automatically propagates the version string to all non-Python manifests and doc files.
3. **Runtime Inspection**: Python modules resolve package version dynamically via `importlib.metadata.version("prolog-agent-toolkit")`.

## Consequences
- AI agents MUST NOT manually edit version strings in `pack.pl`, `bakage.toml`, or `package.json`.
- `prolog-agent check-version` verifies version parity across all files during CI/pre-commit checks.
