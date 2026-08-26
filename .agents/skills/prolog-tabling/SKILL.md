---
name: prolog-tabling
description: Guidelines for tabling, memoization, and SLG resolution in Prolog. Use when handling recursive graph queries, transitive closures, Datalog queries, reachability graphs, dynamic programming, and preventing infinite recursion loops.
---

# Prolog Tabling & SLG Resolution Guidelines

Use this skill when implementing recursive graph algorithms, transitive closures, Datalog queries, or dynamic programming in Prolog engines that support tabling (SLG resolution).

## 1. When to Use Tabling

Tabling (memoization of subgoals and answers) guarantees termination for left-recursive and cyclic graph queries:

- **Graph Reachability & Transitive Closures** (avoiding infinite loops in cyclic graphs)
- **Grammar Parsing with Left Recursion**
- **Datalog-style Deductive Database Queries**
- **Dynamic Programming** (e.g. shortest path, Fibonacci, editing distances)

---

## 2. Declaration Syntax

Declare tabling directives before predicate definitions:

```prolog
% SWI-Prolog / Scryer / Trealla (where supported)
:- table reach/2.

% Cyclic graph reachability
reach(X, Y) :- edge(X, Y).
reach(X, Y) :- reach(X, Z), edge(Z, Y).
```

---

## 3. Answer Subsumption & Mode Directed Tabling

When computing min/max/sum costs over graphs, use mode-directed tabling or answer subsumption:

```prolog
% SWI-Prolog mode-directed tabling for shortest path:
:- table shortest_path(?, ?, min).

shortest_path(X, Y, Dist) :- edge(X, Y, Dist).
shortest_path(X, Y, Dist) :-
    shortest_path(X, Z, D1),
    edge(Z, Y, D2),
    Dist is D1 + D2.
```

---

## 4. Portability & Fallbacks

For Prolog engines without tabling support (or when writing portable ISO code), fall back to an explicit **visited list accumulator**:

```prolog
% Portable fallback for reachability in cyclic graphs without tabling
reach_portable(X, Y) :-
    reach_path(X, Y, [X]).

reach_path(X, Y, _Visited) :- edge(X, Y).
reach_path(X, Y, Visited) :-
    edge(X, Z),
    \+ member(Z, Visited),
    reach_path(Z, Y, [Z|Visited]).
```

---

## 5. Table Management & Invalidation

When facts change dynamically during program execution, clear existing tabled answers:

```prolog
% SWI-Prolog table cleanup
:- retract(edge(a, b)), abolishing_all_tables.
```
