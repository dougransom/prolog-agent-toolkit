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

## Multi-File Version Synchronization Checklist

When bumping or releasing a version, the AI assistant MUST inspect and synchronize version strings across all applicable files:

1. **Prolog Package Manifests**:
   - `pack.pl` (`version('X.Y.Z').` or `version("X.Y.Z").`).
   - Prolog entry module `version/1` predicate (if defined).
2. **Project Metadata (if Python toolkit / CLI wrapper is present)**:
   - `pyproject.toml` (`version = "X.Y.Z"`).
   - Package `__init__.py` (`__version__ = "X.Y.Z"`).
3. **Documentation**:
   - `README.md` version badges, installation code snippets, or release headers.
4. **Git Branching & Tags**:
   - Ensure working on active development branch (e.g., `DEV202608`).
   - Create annotated tag: `git tag -a vX.Y.Z -m "Release vX.Y.Z"`.

---

## Release Execution Workflow

When the user asks to prepare or cut a release:

1. **Audit Files**: Search the workspace for all version references using code search.
2. **Update to Release Version**: Change working `.devN` versions to clean release format `X.Y.Z` across all audited files.
3. **Commit & Tag**:
   ```bash
   git commit -am "Release vX.Y.Z"
   git tag -a vX.Y.Z -m "Release vX.Y.Z"
   ```
4. **Post-Release Prompting**:
   Prompt the user:
   - *Is a new dev branch warranted for future development?*
   - *What is the target version for the next release (e.g. update files to `0.0.2.dev1` or `0.1.0.dev1`)?*
