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

---

## 2. Automated Engine Linting via Safety Runners

Execute engine checks non-interactively using cross-platform safety wrappers:

- **Scryer Prolog Syntax & Warning Check**:
  ```bash
  PROLOG_ENGINE=scryer prolog-safe -g "consult('src/target.pl'), halt."
  ```
- **SWI-Prolog Check & Cross-Reference Utility (`check`)**:
  ```bash
  PROLOG_ENGINE=swi prolog-safe -g "consult('src/target.pl'), check, halt."
  ```

---

## 3. Code Audit Checklist for AI Assistants

When auditing or reviewing Prolog code, perform the following verification steps:

1. **Singleton Check**: Scan for un-annotated singletons in clause heads and bodies.
2. **Determinism Audit**: Verify whether predicates intended to be deterministic leave open choice points.
3. **Mode & Type Audit**: Verify input type checks use module `si` (Safe Type Tests) in Scryer:
   ```prolog
   :- use_module(library(si)).
   
   my_pred(X) :-
       atom_si(X),
       ...
   ```
4. **Character & String Representation**: Verify double-quoted strings represent character lists (`chars`) rather than SWI-specific string objects or code lists.
