---
name: swi-prolog-standards
description: Coding standards and guidelines for SWI-Prolog applications and scripts. Use when targeting SWI-Prolog specifically.
---

# SWI-Prolog Standards

Guidelines for writing idiomatic SWI-Prolog code:

## Core Rules

1. **Modules**: Define clear module headers with `:- module(name, [exports...]).`.
2. **Data Structures**: Utilize SWI dicts (`_{key: Value}`) and SWI strings where appropriate for modern SWI applications.
3. **Packs & Libraries**: Manage external packages using SWI-Prolog `pack_install/1`.
4. **Library Cheat-Sheet Usage**: Use the Standard Library Cheat Sheet below for module imports; do NOT read raw system library files unless working with un-documented custom packages.
5. **Safety**: Always execute code using `swi-safe` or `prolog-safe` with `PROLOG_ENGINE=swi`.

## SWI-Prolog Standard Library Cheat Sheet

> **Universal Coding Standards Note**: The cheat sheet table below specifies SWI-specific module import headers (`:- use_module(library(...)).`) and built-ins. While SWI has dialect-specific module names (e.g. `library(clpfd)`, `library(yall)`), all underlying coding guidelines, purity rules, reification patterns (`=(X,Y,Truth)`, `cond_t`, `if_`), DCG syntax, safe type testing, and formatted output follow the **universal Prolog coding standards** defined in [`prolog-conventions`](../prolog-conventions/SKILL.md) and [`prolog_guidelines.md`](../../references/prolog_guidelines.md).

| Feature / Topic | Import Header | Primary Exported Predicates | Notes / Dialect Rules |
| :--- | :--- | :--- | :--- |
| **CLP(FD) Constraints**| `:- use_module(library(clpfd)).` | `(#=)/2`, `in/2`, `label/1`, `labeling/2` | Integer constraints in SWI (SWI uses `clpfd`). |
| **Higher-Order Lambdas**| `:- use_module(library(yall)).` | `[X]>>...`, `[X,Y]>>Goal` | SWI built-in lambda syntax (`yall`). |
| **Higher-Order Apply**| `:- use_module(library(apply)).` | `maplist/2..5`, `include/3`, `exclude/3`, `foldl/4` | List mapping and filtering. |
| **DCG Basics** | `:- use_module(library(dcg/basics)).` | `string//1`, `integer//1`, `whites//0` | Common parsing non-terminals. |
| **Ordered Sets** | `:- use_module(library(ordsets)).` | `list_to_ord_set/2`, `ord_union/3` | Set operations on sorted lists. |
| **Unit Testing** | `:- use_module(library(plunit)).` | `:- begin_tests(name).`, `:- end_tests(name).` | Native SWI test harness. |
| **Dict Manipulation** | *Built-in* | `get_dict/3`, `put_dict/4`, `is_dict/1` | Native SWI dict support (`Dict.Key`). |

## Universal Guidelines & References

- [Covington Prolog Style Guide](../../references/covington_style.md)
- [Prolog Purity Guidelines](../../references/prolog_guidelines.md)
