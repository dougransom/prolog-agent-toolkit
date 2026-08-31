---
name: prolog-library-discovery
description: Guidelines and commands for discovering and reusing existing libraries, modules, and packages across Prolog engines before implementing functionality from scratch.
---

# Prolog Library & Module Discovery

Use this skill whenever an AI agent needs to analyze requirements, identify target Prolog engines, and discover available standard libraries or third-party packages before generating Prolog code.

## Mandatory Pre-Code-Generation Protocol

Before generating Prolog code for any module, predicate, or solution, AI assistants **MUST** execute the 7-step pre-code-generation protocol:

1. **Identify Target Engine**: Determine the target engine (`scryer`, `swi`, `trealla`, `tau`, `gnu`, `iso`) from `AGENTS.md`, CLI flags (`--engine`/`--system`), or environment variables (`PROLOG_ENGINE`).
2. **Discover Available Capabilities**: Run `prolog-agent discover --engine <engine>` or consult static cheat sheets and local manifests (`bakage.toml`, `pack.pl`, `package.json`).
3. **Prefer Installed Capabilities**: Reuse built-in standard libraries or installed packages instead of implementing functionality from scratch.
4. **Explicitly Import Dependencies**: Always declare explicit module imports (e.g., `:- use_module(library(clpz)).`, `:- use_module(library(dcgs)).`). Do NOT rely on implicit autoloading.
5. **Document Selected Dependencies**: Detail all imported modules in Covington predicate and file headers.
6. **Explain Rationale**: Document why each selected library was chosen (e.g., performance, ISO compliance, established contract).
7. **Pure ISO Fallback**: Implement custom predicate logic manually ONLY when no suitable library or package exists.

---

## Discovery Commands & CLI Usage

Agents and developers can perform static, manifest, or dynamic discovery using the `prolog-agent discover` CLI tool:

```bash
# Discover all libraries for target engine
prolog-agent discover --engine scryer

# Search for a specific feature keyword across all supported engines
prolog-agent discover --query constraint

# Search for a feature keyword for a specific engine
prolog-agent discover --engine swi --query constraint

# Output discovery results in structured JSON format
prolog-agent discover --engine trealla --json
```

---

## Dynamic Introspection Goals by Engine

When operating dynamically in safe environments, agents can interrogate live Prolog interpreters:

| Engine | Dynamic Module Query Goal | Installed Package Inspection |
| :--- | :--- | :--- |
| **Scryer Prolog** | `current_module(M)` | Read `bakage.toml` & `pack.pl` |
| **SWI-Prolog** | `current_module(M)` | `pack_list_installed/0`, `pack_property(P, directory(D))` |
| **Trealla Prolog**| `current_module(M)` | Read `pack.pl` |
| **Tau Prolog** | `current_module(M)` | Read `package.json` (`npm`) |
| **GNU Prolog** | `current_predicate(N/A)` | Built-in predicate inspection |

---

## Decision Strategy: Portability vs Optimization

- **Declared Target Engine**: Choose engine-specific optimized standard libraries (e.g., `library(clpz)` for Scryer/Trealla vs `library(clpfd)` for SWI).
- **Generic ISO Baseline**: When writing engine-agnostic logic (`src/core/`), restrict logic to 100% pure ISO Prolog constructs (`dif/2`, reified `if_/3`, pure DCGs) to maximize cross-engine portability.

---

## Covington Header Standard & Examples

AI assistants MUST include dependency documentation in the Covington module header:

### Example: Module with Discovered Libraries
```prolog
:- module(n_queens, [n_queens/2]).

/** <module> N-Queens Constraint Solver
 *
 *  Dependencies & Rationale:
 *  - library(clpz): Used for (#=)/2 and labeling/2. Chosen for declarative
 *    domain constraints and optimal performance over custom search routines.
 *  - library(lists): Used for length/2 and maplist/2. Chosen for ISO purity.
 */

:- use_module(library(clpz)).
:- use_module(library(lists)).

n_queens(N, Qs) :-
    length(Qs, N),
    Qs ins 1..N,
    n_queens_constraints(Qs),
    labeling([], Qs).
```

### Example: Pure ISO Fallback (No Suitable Library Found)
```prolog
:- module(custom_tree, [tree_depth/2]).

/** <module> Custom Binary Tree Depth
 *
 *  Dependencies & Rationale:
 *  - No standard library found for custom tree AST depth computation.
 *  - Fallback: Implemented using 100% pure ISO Prolog pattern matching and dif/2.
 */

:- use_module(library(reif), [if_/3]).

tree_depth(nil, 0).
tree_depth(node(_, L, R), D) :-
    tree_depth(L, DL),
    tree_depth(R, DR),
    D0 #= max(DL, DR),
    D #= D0 + 1.
```

---

## Universal Guidelines & References

- [Portable ISO Prolog Conventions](../prolog-conventions/SKILL.md)
- [Covington Prolog Style Guide](../../references/covington_style.md)
- [Prolog Packaging Standards](../prolog-packaging/SKILL.md)
