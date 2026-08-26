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

---

## 5. Compilation Failure & Human Editing Syntax Diagnostics

If a Prolog module fails to compile or consult after human editing:

1. **Automatic Diagnostics**: Run standard safety wrapper (`prolog-safe` / `scryer-safe`). Upon non-zero compilation status, `prolog-safe` automatically outputs line, column, and fix recommendations for human syntax typos.
2. **Manual Check Command**:
   ```bash
   prolog-safe --check target_file.pl
   ```
3. **Common Human Operator & Comment Typos**:
   - **`:` instead of `:-`**: Dropped hyphen causes Prolog to parse `head : body` as module qualification `Module:Goal` (creating a fact with head `Module:Goal`).
   - **`#` or `//` instead of `%`**: Using Python or C comment symbols triggers syntax errors at line start.
   - **`->` instead of `-->`**: Using single-arrow if-then in place of DCG rule operator.
   - **`!=`, `<=`, `=>`, `<>`**: Using non-Prolog comparison symbols instead of `=\=`, `\=`, `=<`, `>=`.

