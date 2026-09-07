# Anti-Patterns & Reusability Guide

This document specifies **forbidden practices** and **anti-patterns** that AI coding agents must avoid when working in this repository, alongside an inventory of pre-existing helpers to prevent duplicate implementations.

---

## 1. Forbidden Anti-Patterns for AI Agents

| Category | Forbidden Anti-Pattern | Correct Reusable Alternative |
| :--- | :--- | :--- |
| **Execution** | Calling raw binary interpreters directly ([`scryer-prolog`](https://github.com/mthom/scryer-prolog), [`swipl`](https://www.swi-prolog.org/), [`tpl`](https://github.com/trealla-prolog/trealla), [`tau-prolog`](http://tau-prolog.org/)). | Use safe execution wrappers: `prolog-safe`, `scryer-safe`, `swi-safe`, `trealla-safe`, `tau-safe`. |
| **Purity** | Using non-logical cut (`!`) or negation-as-failure (`\+/1`) for term inequality. | Use `dif(X, Y)` or reified `if_/3` from [`library(reif)`](https://github.com/mthom/scryer-prolog/blob/master/src/lib/reif.pl). |
| **Data Types** | Using [SWI-Prolog](https://www.swi-prolog.org/) dicts (`_{a: 1}`) or SWI string types in portable ISO-target Prolog modules. | Use standard terms or clean functor representations (`leaf(L)`, `node(L, R)`), and `chars` for strings. |
| **Python Tooling** | Allowing Python executions or test runs to leave `__pycache__` or `.pyc` clutter. | Set `PYTHONDONTWRITEBYTECODE=1` on all Python invocations (`PYTHONDONTWRITEBYTECODE=1 uv run pytest`). |
| **Version Sync** | Manually hardcoding version strings in individual files (`pack.pl`, `README.md`). | Version source of truth is [`pyproject.toml`](../pyproject.toml). Run `prolog-agent release --version X.Y.Z` or resolve version via `importlib.metadata.version("prolog-agent-toolkit")`. |
| **Syntax Errors** | Ignoring human punctuation errors (`:` instead of `:-`, `->` instead of `-->`). | Use [`prolog_agent_toolkit.syntax_checker`](../prolog_agent_toolkit/syntax_checker.py) to parse compilation failures and recommend exact fixes. |
| **Hyperlinks** | Using absolute `file://` URIs for local files (`file:///path/to/doc.md`). | Use relative Markdown links (`[AGENT_GUIDE.md](../AGENT_GUIDE.md)`). Ask human authors before converting human-written `file://` links. |

---

## 2. The Imperative Control Flow Bias in LLMs vs. Declarative Pure Prolog

### Why LLMs Default to `!`, `\+`, `->` (Context for Humans & Machines)

AI coding assistants have a profound statistical and conceptual bias toward imperative Prolog control flow:
1. **1000:1 Historical Training Imbalance**: Over 99% of open-source Prolog code created between 1980 and 2012 relied on green/red cuts (`!`), soft cuts (`->`), and negation-as-failure (`\+`). Ulrich Neumerkel's reification framework (`library(reif)`) was introduced in 2014 and only recently became standard across ISO systems like Scryer and Trealla. LLM token predictions naturally reproduce legacy patterns unless strictly constrained.
2. **Imperative Control Flow Transfer**: LLMs generalize patterns from Python, C, and JavaScript. An if-statement like `if cond: return A else: return B` is reflexively mapped to `( Cond -> A ; B )` and `!`. In Prolog, however, `->` and `!` are *destructive cuts* that commit irreversibly, prune choice points, and render predicates unidirectional (failing on variable inputs).

### The 5 Reification Compiler Traps & How to Solve Them

When an LLM attempts pure reification, it frequently trips over these 5 compiler traps and regresses to `!`. The table below provides the failure modes and correct pure patterns:

| Compiler Trap | Broken Anti-Pattern | Pure Recipe (Correct) | Rationale |
| :--- | :--- | :--- | :--- |
| **1. Compound Condition in `if_/3`** | `if_((A, B), Then, Else)` | `if_(A, if_(B, Then, Else), Else)` | `library(reif)` reifies each condition by appending a boolean argument. `','/3` does not exist. Nest the `if_/3` calls. |
| **2. DCG Macro Expansion** | `phrase --> if_(C, T, E).` | `{ if_(C, T, E) }` or clause dispatch with `dif/2` | The DCG preprocessor adds two stream arguments to every goal in the body, turning `if_/3` into `if_/5`. Wrap in `{ ... }` or use separate DCG clauses. |
| **3. Arity Mismatch on Engine Builtins** | `if_(char_type(C, lower), T, E)` | `char_type_lower_t(C, Truth)` wrapper or `memberd_t(C, LowerChars, Truth)` | `char_type/3` is not a truth-reifying predicate. Provide a 2-argument reified wrapper or use `memberd_t/3`. |
| **4. Partial Unification in `if_/3`** | `if_(Rest = ['*'\|_], T, E)` | `Rest = [C\|Cs], if_(C = '*', T, E)` or separate clauses | `=(Rest, ['*'\|_], Truth)` cannot reify equality on an uninstantiated tail variable. Match the head first. |
| **5. Option & Map Lookups** | `member(Key(Val), Opts) -> ... ; Val = Def` | `lookup_option/4` using `Opt =.. [K, V]` and `if_(K = Key, ...)` | Soft cuts prune valid alternatives. A pure helper preserves bidirectionality and backtracking. |

### Mandatory Post-Generation Self-Audit Checklist

Every AI agent must self-audit code before presenting or committing:
- [ ] **No Unjustified Cuts (`!`)**: Replace with `dif/2` or `if_/3`. If required for engine side-effects, foreign I/O, or interactive CLI prompts, format with `% Justification: <reason>`.
- [ ] **No Soft Cuts (`->`)**: Replace with `if_/3` or `cond_t`.
- [ ] **No Unsound Inequality (`\+ (X = Y)`)**: Replace with `dif(X, Y)`.
- [ ] **No Impure Membership in Conditionals**: Replace `member(X, Xs)` inside branching conditions with `memberd_t(X, Xs, Truth)`.

---

## 3. Reusable Helper & Utility Inventory

Before implementing new code, verify whether the required functionality already exists in the repository:

- **Safety Execution Engine**: [`prolog_agent_toolkit/runner.py`](../prolog_agent_toolkit/runner.py) -> `run_prolog_safe()`
- **Project & Module Generator**: [`prolog_agent_toolkit/project.py`](../prolog_agent_toolkit/project.py) -> `init_project()`, `generate_module()`
- **Syntax Diagnostic Engine**: [`prolog_agent_toolkit/syntax_checker.py`](../prolog_agent_toolkit/syntax_checker.py) -> `check_prolog_syntax()`
- **Skill Validator**: [`prolog_agent_toolkit/skill_validator.py`](../prolog_agent_toolkit/skill_validator.py) -> `validate_skill_frontmatter()`
- **Release Synchronization Engine**: [`prolog_agent_toolkit/release.py`](../prolog_agent_toolkit/release.py) -> `run_release()`, `check_versions()`
- **Git Hooks Installer**: [`prolog_agent_toolkit/hooks.py`](../prolog_agent_toolkit/hooks.py) -> `install_hooks()`
