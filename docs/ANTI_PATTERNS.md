# Anti-Patterns & Reusability Guide

This document specifies **forbidden practices** and **anti-patterns** that AI coding agents must avoid when working in this repository, alongside an inventory of pre-existing helpers to prevent duplicate implementations.

---

## 1. Forbidden Anti-Patterns for AI Agents

| Category | Forbidden Anti-Pattern | Correct Reusable Alternative |
| :--- | :--- | :--- |
| **Execution** | Calling raw binary interpreters directly ([`scryer-prolog`](https://github.com/mthom/scryer-prolog), [`swipl`](https://www.swi-prolog.org/), [`tpl`](https://github.com/trealla-prolog/trealla), [`tau-prolog`](http://tau-prolog.org/)). | Use safe execution wrappers: `prolog-safe`, `scryer-safe`, `swi-safe`, `trealla-safe`, `tau-safe`. |
| **Purity** | Using non-logical cut (`!`) or negation-as-failure (`\+/1`) for term inequality. | Use `dif(X, Y)` or reified `if_/3` from [`library(reif)`](https://github.com/mthom/scryer-prolog/blob/master/src/lib/reif.pl). |
| **Data Types** | Using [SWI-Prolog](https://www.swi-prolog.org/) dicts (`_{a: 1}`) or SWI string types in ISO Prolog modules. | Use pure ISO terms or clean functor representations (`leaf(L)`, `node(L, R)`), and `chars` for strings. |
| **Python Tooling** | Allowing Python executions or test runs to leave `__pycache__` or `.pyc` clutter. | Set `PYTHONDONTWRITEBYTECODE=1` on all Python invocations (`PYTHONDONTWRITEBYTECODE=1 uv run pytest`). |
| **Version Sync** | Manually hardcoding version strings in individual files (`pack.pl`, `README.md`). | Version source of truth is [`pyproject.toml`](../pyproject.toml). Run `prolog-agent release --version X.Y.Z` or resolve version via `importlib.metadata.version("prolog-agent-toolkit")`. |
| **Syntax Errors** | Ignoring human punctuation errors (`:` instead of `:-`, `->` instead of `-->`). | Use [`prolog_agent_toolkit.syntax_checker`](../prolog_agent_toolkit/syntax_checker.py) to parse compilation failures and recommend exact fixes. |
| **Hyperlinks** | Using absolute `file://` URIs for local files (`file:///path/to/doc.md`). | Use relative Markdown links (`[AGENT_GUIDE.md](../AGENT_GUIDE.md)`). Ask human authors before converting human-written `file://` links. |

---

## 2. Reusable Helper & Utility Inventory

Before implementing new code, verify whether the required functionality already exists in the repository:

- **Safety Execution Engine**: [`prolog_agent_toolkit/runner.py`](../prolog_agent_toolkit/runner.py) -> `run_prolog_safe()`
- **Project & Module Generator**: [`prolog_agent_toolkit/project.py`](../prolog_agent_toolkit/project.py) -> `init_project()`, `generate_module()`
- **Syntax Diagnostic Engine**: [`prolog_agent_toolkit/syntax_checker.py`](../prolog_agent_toolkit/syntax_checker.py) -> `check_prolog_syntax()`
- **Skill Validator**: [`prolog_agent_toolkit/skill_validator.py`](../prolog_agent_toolkit/skill_validator.py) -> `validate_skill_frontmatter()`
- **Release Synchronization Engine**: [`prolog_agent_toolkit/release.py`](../prolog_agent_toolkit/release.py) -> `run_release()`, `check_versions()`
- **Git Hooks Installer**: [`prolog_agent_toolkit/hooks.py`](../prolog_agent_toolkit/hooks.py) -> `install_hooks()`
