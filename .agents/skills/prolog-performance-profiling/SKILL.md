---
name: prolog-performance-profiling
description: Performance optimization and choicepoint profiling guidelines for Prolog. Use when eliminating unintended choice points, analyzing argument indexing, optimizing space complexity, and refactoring with library(reif).
---

# Prolog Performance & Choicepoint Profiling Guidelines

Use this skill when auditing Prolog programs for memory usage, execution speed, tail recursion, indexing efficiency, and choicepoint leaks.

## 1. Choicepoint Elimination & Indexing

Unintended choice points consume stack memory and degrade performance.

- **First-Argument Indexing**: Most Prolog engines index on the principal functor of the **first argument**. Ensure the distinguishing input parameter is placed in the first position (`+Input, -Output`).

```prolog
% GOOD: First argument indexing distinguishes empty list vs non-empty list
process_list([], 0).
process_list([X|Xs], Sum) :- ...
```

- **Clean Data Representations for Indexing**: Ensure terms are **clean** ([metalevel.at/prolog/data#clean](https://www.metalevel.at/prolog/data#clean)) by wrapping every data element kind in a distinct principal functor (e.g. `leaf(L)` vs `node(L, R)`). Defaulty representations prevent indexing and create open choicepoints.

- **Reification over Cuts (`zcompare/3` & `if_/3`)**: Use `zcompare(Order, X, Y)` (from `library(clpz)`) for integer comparisons. It reifies the comparison into an atom (`<`, `=`, `>`) that matches directly in the first argument, avoiding choice points and cuts:

```prolog
:- use_module(library(clpz)).
:- use_module(library(reif)).

% GOOD: Reified comparison produces an atom amenable to argument indexing
max_pure(X, Y, Max) :-
    zcompare(Order, X, Y),
    max_order(Order, X, Y, Max).

max_order(<, _, Y, Y).
max_order(=, X, _, X).
max_order(>, X, _, X).
```

- **Early Pruning**: Place deterministic, non-suspending goals (`dif/2`, CLP(Z) constraints) before general search goals to prune search trees as early as possible.


---

## 2. Tail Call Optimization (TCO) & Accumulators

Ensure recursive predicates process large inputs in constant stack space:

- **Tail Position**: Place recursive calls as the **very last goal** of a clause.
- **Accumulator Pattern**: Pass running state in an extra argument rather than evaluating on return.

```prolog
% Non-tail recursive (builds stack frame per element)
sum_list([], 0).
sum_list([X|Xs], Sum) :- sum_list(Xs, Rest), Sum is X + Rest.

% Tail recursive with accumulator (constant stack space)
sum_list_tco(Xs, Sum) :- sum_list_acc(Xs, 0, Sum).

sum_list_acc([], Acc, Acc).
sum_list_acc([X|Xs], Acc0, Sum) :-
    Acc1 #= Acc0 + X,
    sum_list_acc(Xs, Acc1, Sum).
```

---

## 3. Profiling Execution Time & Memory

Audit goal execution using built-in measurement predicates via `prolog-safe`:

```prolog
% SWI-Prolog time & statistics
:- time(my_goal(Result)).

% Scryer Prolog time measurement
:- use_module(library(time)).
:- time(my_goal(Result)).
```
