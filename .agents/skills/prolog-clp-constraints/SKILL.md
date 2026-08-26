---
name: prolog-clp-constraints
description: Best practices for Constraint Logic Programming (CLP(Z), CLP(FD), CLP(R), CLP(Q)) in Prolog. Use when modeling combinatorial optimization, scheduling, Sudoku, cryptarithmetic, symbolic math, labeling strategies, and declarative arithmetic constraints.
---

# Constraint Logic Programming (CLP) Guidelines

Use this skill when designing, solving, or refactoring combinatorial optimization problems, integer constraints, symbolic arithmetic, or scheduling tasks in Prolog.

## 1. Module Declarations & Engine Compatibility

Always import the appropriate constraint library based on the target engine:

- **Scryer Prolog (Default)**: Use `library(clpz)`
  ```prolog
  :- use_module(library(clpz)).
  ```
- **SWI-Prolog**: Use `library(clpfd)`
  ```prolog
  :- use_module(library(clpfd)).
  ```
- **Trealla Prolog**: Use `library(clpz)`
  ```prolog
  :- use_module(library(clpz)).
  ```

---

## 2. Separation of Concerns: Declaration vs Search

Structure constraint programs into two distinct phases:

1. **Constraint Declaration**: Declare variables, domains (`ins`, `in`), and relations (`#=`, `#\=`, `all_different/1`). This phase must remain purely declarative without triggering premature search.
2. **Search (`labeling/2`)**: Bind variables to concrete values using search strategies (`labeling/2` or `label/1`).

```prolog
% Example: N-Queens problem
n_queens(N, Qs) :-
    length(Qs, N),
    Qs ins 1..N,
    all_different(Qs),
    safe_diagonals(Qs),
    labeling([ff], Qs). % Search heuristic: First-Fail (ff)
```

---

## 3. Constraint Operators & Reification

Prefer CLP constraints over imperative `(is)/2` arithmetic to maintain bidirectionality:

- **Arithmetic Constraints**: `#=`, `#\=`, `#>`, `#>=`, `#<`, `#=<`
- **Domain Declarations**: `X in Low..High`, `Vars ins Low..High`
- **Combinatorial Constraints**: `all_different(Vars)`, `all_distinct(Vars)`, `circuit(Vars)`
- **Logical Connectives & Reification**:
  - `#/\` (and), `#\/` (or), `#\` (not)
  - `#<==>` (equivalent / bi-implication), `#==>` (implication)

```prolog
% Reification Example: B is 1 if X > 10, else 0
x_greater_ten_flag(X, B) :-
    B in 0..1,
    X #> 10 #<==> B #= 1.
```

---

## 4. Arithmetic Purity vs Performance

- **Declarative Code**: Always prefer `#=` over `(is)/2` for general application logic, relations, and data structures.
- **Low-level Optimizations**: Use `(is)/2`, `(>)/2`, and `(=:=)/2` only when building performance-critical term expansions or low-level array indexed operations where inputs are guaranteed to be instantiated integers.

---

## 5. Execution Safety

Run constraint solvers with timeouts via `prolog-safe` to prevent unbounded search trees:

```bash
PROLOG_ENGINE=scryer prolog-safe -g "n_queens(8, Qs), write(Qs), halt."
```
