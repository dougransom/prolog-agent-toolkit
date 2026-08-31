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

## 3. Constraint Operators & Logical Connectives

Prefer CLP constraints over imperative `(is)/2` arithmetic to maintain bidirectionality.

### Core Operators & Domain Constraints
- **Arithmetic Constraints**: `#=`, `#\=`, `#>`, `#>=`, `#<`, `#=<`
- **Domain Declarations**: `X in Low..High`, `Vars ins Low..High` (always post domains **before** posting complex relations)
- **Combinatorial Constraints**: Prefer **`all_distinct(Vars)`** over `all_different(Vars)` for strong domain consistency (hyper-arc pruning) in combinatorial puzzles.

### Logical Connectives & Solver Reification

| Connective | Description | When the Agent Should Use It |
| :--- | :--- | :--- |
| **`#\ Q`** | Negation (Not `Q`) | Enforce that constraint `Q` must NOT hold in the solver model. |
| **`P #\/ Q`** | Disjunction (Or) | Enforce that at least one of two constraints holds (e.g. non-overlapping time windows `EndA #=< StartB #\/ EndB #=< StartA`). |
| **`P #/\ Q`** | Conjunction (And) | Join multiple constraint conditions inside reifications or domain flags. |
| **`P #\ Q`** | Exclusive Or (XOR) | Enforce that exactly one of two choices is selected, but not both (mutually exclusive allocation). |
| **`P #<==> Q`** | Bi-implication / Equivalence | **Link a 0..1 model flag to a constraint**: `X #> 10 #<==> B #= 1` (primary reification tool inside integer models). |
| **`P #==> Q`** | Implication (If P then Q) | Model conditional solver rules without search/cuts (e.g. `Task_Machine #= 1 #==> Task_Start #>= 50`). |
| **`P #<== Q`** | Converse Implication | Model converse conditional rules (`Q` implies `P`). |

```prolog
% Reification Example: B is 1 if X > 10, else 0
x_greater_ten_flag(X, B) :-
    B in 0..1,
    X #> 10 #<==> B #= 1.

% Conditional Machine Assignment Rule
machine_start_rule(Machine, StartTime) :-
    Machine #= 2 #==> StartTime #>= 100.
```

---

## 4. Reified CLP(Z) Predicates (`(#=)/3`, `(#<)/3`, `clpz_t/2`)

When interfacing CLP(Z) constraints with higher-order reified logic or control flow:

1. **Reified Arithmetic Predicates (`(#=)/3`, `(#<)/3`, `(#>)/3`, `(#=<)/3`, `(#>=)/3`, `(#\=)/3`)**:
   - Relate two arithmetic expressions to boolean `true`/`false` (`'#='(X, Y, Truth)`).
   - **When to use**: Pass partial 2-argument closures to `tfilter/3` or `tpartition/4` for pure collection processing.
     ```prolog
     % Keep all positive integers deterministically
     keep_positives(Numbers, Positives) :-
         tfilter((#<)(0), Numbers, Positives).
     ```
2. **`clpz_t(Constraint, Truth)`**:
   - Reifies any general CLP(Z) constraint expression `Constraint` into boolean `Truth` (`true` or `false`).
   - **When to use**: Adapt compound CLP(Z) expressions (e.g., `X #> 0 #/\ Y #< 10`) for use with `library(reif)` predicates (`if_/3`, `cond_t/3`, `tfilter/3`).
     ```prolog
     % Pure conditional branching based on compound integer constraint
     check_range(X, Status) :-
         cond_t(clpz_t(X #>= 10 #/\ X #=< 20), Status = in_range, Status = out_of_range).
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
