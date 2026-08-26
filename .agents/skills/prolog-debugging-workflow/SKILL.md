---
name: prolog-debugging-workflow
description: Step-by-step interactive debugging and tracing guidelines for Prolog. Use when stepping through failing goals, setting spy points, inspecting stack frames, and capturing term representations.
---

# Prolog Debugging & Tracing Workflow

Use this skill when diagnosing test failures, unexpected predicate failures, or infinite loops in Prolog code.

## 1. Interactive Tracer Basics (4-Port Model)

Prolog debuggers use the **4-Port Execution Model**:
- **Call**: Initial invocation of a goal.
- **Exit**: Successful unification/derivation of a goal.
- **Redo**: Backtracking into a goal to find alternative solutions.
- **Fail**: Complete failure of a goal to unify or satisfy constraints.

---

## 2. Setting Trace Points & Leashing

```prolog
% Enable execution tracing
:- trace.

% Spy on specific predicate
:- spy(my_predicate/2).

% Turn off tracing
:- nodebug.
```

---

## 3. Engine-Specific Debugging Instructions

### SWI-Prolog
- Interactive tracer: Call `trace, my_goal(X).`
- Graphical tracer: `gtrace, my_goal(X).`
- Term printing: `portray_clause(Term).`

### Scryer Prolog
- Print tracing: Use `write/1`, `format/2`, or `portray_clause/1` from `library(format)` to inspect non-ground terms.
- Use `library(debug)` directives when available.

---

## 4. Debugging Non-Ground Terms & Constraints

When debugging constraint logic code (`CLP(Z)` / `CLP(FD)`), avoid plain `write/1` which may hide constraint attributes. Use `copy_term/3` or attribute inspection:

```prolog
% Scryer Prolog attribute inspection
:- use_module(library(clpz)).

debug_vars(Vars) :-
    copy_term(Vars, Vars, Goals),
    format("Residual constraints: ~w~n", [Goals]).
```
