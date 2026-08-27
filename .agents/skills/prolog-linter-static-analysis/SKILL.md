---
name: prolog-linter-static-analysis
description: Static analysis, linting, and code quality guidelines for Prolog. Use when detecting singletons, discontiguous predicates, unreferenced parameters, infinite recursion, and non-logical cuts.
---

# Prolog Static Analysis & Code Quality Guidelines

Use this skill to audit, lint, and analyze Prolog code for common errors, singleton variables, discontiguous clauses, non-deterministic performance issues, and non-logical constructs.

## 1. Common Linter Warnings & Remedies

| Issue / Warning | Cause | Recommended Solution |
| :--- | :--- | :--- |
| **Singleton variables** | Variable appears only once in a clause (often a typo or unreferenced value). | Prefix with `_` (e.g. `_Var`) or use anonymous variable `_`. |
| **Discontiguous predicate** | Clauses of the same predicate are separated by other predicates. | Group clauses together or add `:- discontiguous Name/Arity.` directive. |
| **Unknown predicate** | Calling a predicate that has not been defined or imported. | Add `:- use_module(...)` or correct predicate name/arity. |
| **Non-logical cut (`!`)** | Impure control flow masking logic bugs or disabling backtracking. | Replace with `if_/3` from `library(reif)` or pure `dif/2`. |
| **Negation-as-failure (`\+/1`) for inequality** | Using `\+ (X = Y)` or `\+ Goal` to express inequality on potentially uninstantiated terms (unsound). | Replace with pure `dif(X, Y)` constraint. |
| **Defaulty Representation** | Data element kinds cannot be distinguished by principal functor (forcing `var/1` or catch-all default clauses). | Wrap elements in distinct principal functors (e.g. `leaf(X)`, `node(L, R)`). Convert external defaulty data early at boundaries. |
| **Mis-typed Neck Operator (`:`)** | Dropped `-` from neck operator `:-` (or directive `: module(...)`). Prolog parses `head : body` as module qualification `Module:Goal` (fact with head `Module:Goal`). | Replace `:` with `:-`. |
| **Wrong Comment Symbol (`#` / `//`)** | Using `#` (Python/Bash) or `//` (C/C++/JS) for comments instead of `%`. | Replace `#` or `//` line comment symbols with `%`. |
| **DCG Operator Typo (`->`)** | Using `->` (if-then) instead of `-->` for DCG grammar rules. | Replace `->` with `-->`. |
| **Invalid Comparison (`!=`, `<=`, `=>`, `<>`)** | Using C/Python comparison symbols instead of Prolog standard operators. | Use `=\=` / `\=` for inequality, `=<` for less-than-or-equal, `>=` for greater-than-or-equal. |

---

## 2. Automated Engine Linting & Human Error Diagnostics

Execute engine checks non-interactively using cross-platform safety wrappers. If a file fails to compile, `prolog-safe` automatically scans and reports line/column locations of human syntax editing typos:

- **Scryer Prolog Syntax & Warning Check**:
  ```bash
  PROLOG_ENGINE=scryer prolog-safe -g "consult('src/target.pl'), halt."
  ```
- **SWI-Prolog Check & Cross-Reference Utility (`check`)**:
  ```bash
  PROLOG_ENGINE=swi prolog-safe -g "consult('src/target.pl'), check, halt."
  ```
- **Proactive Standalone Human Syntax Check**:
  ```bash
  prolog-safe --check src/target.pl
  ```

---

## 3. Code Audit Checklist for AI Assistants

When auditing or reviewing Prolog code, perform the following verification steps:

1. **Human Editing Punctuation Audit**: Scan for dropped symbols (`:` instead of `:-`, `->` instead of `-->`), wrong comment tokens (`#`, `//`), or mistyped comparison operators (`!=`, `<=`, `=>`).
2. **Singleton Check**: Scan for un-annotated singletons in clause heads and bodies.
3. **Determinism Audit**: Verify whether predicates intended to be deterministic leave open choice points.
4. **Clean Data Representation Audit**: Scan for **defaulty representations** where term variants lack distinguishing principal functors or rely on runtime `var/1`/`nonvar/1` tests or fallback default clauses. Inform the programmer and recommend clean functor tags (`leaf(L)`, `val(V)`).
5. **Mode & Type Audit**: Verify input type checks use module `si` (Safe Type Tests) in Scryer:
   ```prolog
   :- use_module(library(si)).
   
   my_pred(X) :-
       atom_si(X),
       ...
   ```
6. **Character & String Representation**: Verify double-quoted strings represent character lists (`chars`) rather than SWI-specific string objects or code lists.


