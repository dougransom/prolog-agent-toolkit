---
name: prolog-code-review
description: Comprehensive guidelines, checklists, and automated procedures for conducting Prolog code reviews, checking logical purity, determinism, portability, safety, and test coverage.
---

# Prolog Code Review Guidelines & Checklist

Use this skill when reviewing Prolog pull requests, auditing code diffs, or evaluating code quality before merging into main development branches.

## 1. Code Review Checklist

| Dimension | Check Items |
| :--- | :--- |
| **Logical Purity & Reified Traversals** | - Are cuts (`!`), negation-as-failure (`\+/1`), and soft cuts (`->`) avoided in favor of `if_/3` from `library(reif)` or `dif/2` (preferring `dif(X, Y)` over `\+ (X = Y)`)?<br>- Are cuts (`!`), `\+/1`, `->` omitted for performance tuning? If introduced for *correctness*, is an explicit inline comment present justifying why pure logic constructs (`if_/3`, `dif/2`) were insufficient?<br>- Are direct reified predicates (e.g., `=(X, Y, Truth)`, `memberd_t/3`, `dif/3`) used directly when binding booleans instead of wrapping boolean assignments inside `if_/3`?<br>- Is `cond_t` aggressively preferred over `if_` and `->` when selecting between choices or values to adhere to the DRY principle (avoiding repeated variable unifications across true/false branches)?<br>- Are `tfilter/3` and `tpartition/4` used for pure reified list filtering/partitioning instead of non-reified `include/3`/`exclude/3` or manual recursive loops? |
| **CLP Constraints & Modeling** | - Is **`CLP(B)`** (`library(clpb)`) selected for pure boolean logic, tautology verification (`taut/2`), or instant solution counting (`sat_count/2`), while **`CLP(Z)`** (`library(clpz)`) is selected for integer arithmetic, ranges, and scheduling?<br>- Are domain declarations (`ins`, `in`) posted **before** posting complex arithmetic constraints to enable early constraint propagation?<br>- Is **`all_distinct/1`** preferred over `all_different/1` for hard combinatorial puzzles to enforce domain consistency (hyper-arc pruning)?<br>- Are 0..1 model flags linked via `#<==>` (bi-implication) and solver rules expressed via `#==>` (implication) rather than cuts/soft cuts?<br>- Are partial closures `(#=)/3`, `(#<)/3`, or `clpz_t/2` passed to `tfilter/3` or `cond_t` when filtering/branching on integer constraints? |
| **Clean Data Representation** | - Can every data element kind be distinguished solely by its **principal functor** (e.g., `leaf(L)` vs `node(L, R)`)?<br>- Are defaulty representations avoided so argument indexing works automatically?<br>- Are external defaulty/unstructured inputs converted into clean trees early? |
| **Determinism & Performance** | - Do deterministic predicates leave open choice points?<br>- Is the primary input placed in the first argument position for first-argument indexing?<br>- Is `zcompare/3` used for reified integer comparisons?<br>- Are recursive calls in tail position (TCO) with accumulators? |
| **Variable Naming & Syntax** | - Are public API parameter names domain-descriptive (`Tree`, `TokenStream`) while standard short names (`X`, `Xs`, `N`) are kept in tight local contexts?<br>- Are DCG state pairs consistently named (`L0..L` / `S0..S`)?<br>- Are neck operators `:-` free of dropped characters (`:` instead of `:-`)?<br>- Are line comments formatted with `%` rather than `#` or `//`?<br>- Are DCG rules declared with `-->` rather than `->`?<br>- Are comparison operators Prolog-standard (`=\=`, `\=`, `=<`, `>=`) rather than C/Python symbols (`!=`, `<=`, `=>`)?<br>- Do module export lists (`:- module/2`), import lists (`:- use_module/2`), and doc comments use ISO `Name//Arity` indicator notation for DCG non-terminals? |
| **Engine Portability** | - Are engine-specific types (SWI dicts, SWI strings) avoided in ISO / multi-engine code?<br>- Are explicit module imports declared (e.g. `:- use_module(library(dcgs)).`, `library(si)`, `library(clpz)`)? |
| **Safety & Security** | - Is user input sanitized before `consult/1` or `read_term/2`?<br>- Are execution timeouts enforced via `prolog-safe`? |
| **Testing & Documentation** | - Are unit tests provided (`testing.pl` / `plunit`) covering success, failure, and edge cases?<br>- Are mode annotations (`+`, `-`, `?`), DCG indicators (`Name//Arity`), and Covington comments (`%%`) present? |

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
> **Defaulty Representation Detected**: Data elements in `tree_node/2` cannot be distinguished by principal functor (omitting tag wrappers on leaves). Refactor to use clean compound terms (e.g. `leaf(X)` and `node(L, R)`). See [Metalevel.at Clean Data Representations](https://www.metalevel.at/prolog/data#clean).

> [!WARNING]
> **Choicepoint Leak**: `process_data/2` leaves an open choice point when given ground input. Ensure clauses are mutually exclusive via first-argument indexing or reified integer comparison `zcompare/3`.

