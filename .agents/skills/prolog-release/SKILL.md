---
name: prolog-release
description: Guidelines and automated workflow for releasing Prolog projects, bumping version numbers consistently across manifests (pack.pl, pyproject.toml, README.md, __init__.py), creating Git tags, and managing dev branch versions.
---

# Prolog Project Release & Versioning Skill

Use this skill when cutting a release, bumping project versions, tagging Git releases, or managing development branches.

## Version Numbering Conventions

1. **Development Version Format**: `X.Y.Z.devN` (e.g. `0.0.1.dev1`).
2. **Release Version Format**: `X.Y.Z` (e.g. `0.0.1` or `0.1.0`).

---

## Canonical Version Source of Truth & Rules

1. **Canonical Version**: `pyproject.toml` (`version = "X.Y.Z"`) is the single canonical source of truth for project versioning (including development versions like `0.0.1.dev3`).
2. **Runtime Resolution**: Python modules resolve version at runtime via `importlib.metadata.version(...)`.
3. **Synchronization**: Non-Python manifests (`bakage.toml`, `pack.pl`, `package.json`) and documentation (`README.md`, `CHANGELOG.md`) are synchronized to match `pyproject.toml`.
4. **Git Tag Matching**: Git release tags MUST use the exact version string from `pyproject.toml` (e.g., `git tag -a v0.0.1 -m "Release v0.0.1"` or `git tag -a v0.0.1.dev3 -m "Release v0.0.1.dev3"`).

---

## Release Execution Workflow (`prolog-agent release`)

When preparing or cutting a release, execute or run:

```bash
prolog-agent release [--version X.Y.Z]
```

### Workflow Steps:
1. **Audit & Synchronize Versions**: Change working `.devN` versions to clean release format `X.Y.Z` across `bakage.toml`, `pack.pl`, `package.json`, `pyproject.toml`, `__init__.py`, and `README.md`.
2. **Generate CHANGELOG.md**: Create or update `CHANGELOG.md` with:
   - Version header (`## [X.Y.Z] - YYYY-MM-DD`)
   - Summary of changes
   - Added/modified predicates
   - Breaking changes
3. **Commit & Tag**:
   ```bash
   git commit -am "Release vX.Y.Z"
   git tag -a vX.Y.Z -m "Release vX.Y.Z"
   ```
4. **Post-Release Prompting**:
   Prompt the user:
   - *Is a new dev branch warranted for future development?*
   - *What is the target version for the next release (e.g. update files to `0.0.2.dev1` or `0.1.0.dev1`)?*

