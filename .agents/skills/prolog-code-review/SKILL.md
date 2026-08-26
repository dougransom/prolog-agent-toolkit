---
name: prolog-code-review
description: Comprehensive guidelines, checklists, and automated procedures for conducting Prolog code reviews, checking logical purity, determinism, portability, safety, and test coverage.
---

# Prolog Code Review Guidelines & Checklist

Use this skill when reviewing Prolog pull requests, auditing code diffs, or evaluating code quality before merging into main development branches.

## 1. Code Review Checklist

| Dimension | Check Items |
| :--- | :--- |
| **Logical Purity** | - Are cuts (`!`) avoided in favor of `if_/3` from `library(reif)` or `dif/2`?<br>- Are conditions and test-values isolated (e.g. `if_(G, A="A", A="B"), write(A)`)?<br>- Are Definite Clause Grammars (`-->`) used for sequence parsing/formatting instead of imperative loops? |
| **Determinism & Performance** | - Do deterministic predicates leave open choice points?<br>- Is the primary input placed in the first argument position for first-argument indexing?<br>- Are recursive calls in tail position (TCO) with accumulators? |
| **Engine Portability** | - Are engine-specific types (SWI dicts, SWI strings) avoided in ISO / multi-engine code?<br>- Are explicit module imports declared (e.g. `:- use_module(library(dcgs)).`, `library(si)`)? |
| **Safety & Security** | - Is user input sanitized before `consult/1` or `read_term/2`?<br>- Are execution timeouts enforced via `prolog-safe`? |
| **Testing & Documentation** | - Are unit tests provided (`testing.pl` / `plunit`) covering success, failure, and edge cases?<br>- Are mode annotations (`+`, `-`, `?`) and Covington comments (`%%`) present? |

---

## 2. Automated Review Execution via Safety Runners

Execute static analysis and linting checks non-interactively using safety runners:

```bash
# Check syntax & warnings with Scryer Prolog
PROLOG_ENGINE=scryer prolog-safe -g "consult('src/target.pl'), halt."

# Run SWI-Prolog cross-reference and check utility
PROLOG_ENGINE=swi prolog-safe -g "consult('src/target.pl'), check, halt."
```

---

## 3. Formatting Code Review Feedback

Structure PR review comments using GitHub alerts:

> [!IMPORTANT]
> **Logical Purity Concern**: Replace cut `!` on line 24 with pure reification using `if_/3` from `library(reif)` to preserve bidirectionality.

> [!WARNING]
> **Choicepoint Leak**: `process_data/2` leaves an open choice point when given ground input. Ensure clauses are mutually exclusive via first-argument indexing.
