---
name: prolog-conventions
description: Coding standards and guidelines for portable, pure ISO-compliant Prolog across all conforming engines. Use when writing Prolog code intended to run on any ISO Prolog interpreter.
---

# Prolog Conventions

Guidelines for writing clean, portable, pure ISO-compliant Prolog.

## Core Guidelines

1. **Logical Purity**: Prefer pure predicates. Avoid unnecessary side effects or non-deterministic cuts `!` where pure logic constructs (`dif/2`, `if_/3`) can be used.
2. **Strings as Character Lists (`chars`)**: Represent strings and text as lists of characters (`chars`). `double_quotes` must always be set to `chars`.
3. **Safe Type Testing**: Prefer pure, safe type tests (e.g. `library(si)`: `list_si/1`, `atom_si/1`, `chars_si/1`, `integer_si/1`) over impure non-monotonic type checks (`is_list/1`).
4. **Higher-Order Logic & Lambdas**: Use higher-order predicates (`call/N`, `call//N`, `maplist/N`, `foldl/N`, `include/3`, `exclude/3`) and `library(lambda)` (`\X^...`, `\X^Y^Goal`) to eliminate code repetition.
5. **Standard & Higher-Order DCGs**: Use Definite Clause Grammars (`-->`) for sequence parsing, formatting, and tree transformations. Use `call//N` for higher-order DCG non-terminals.
6. **Explicit Library Declarations**: Explicitly import required modules (e.g. `:- use_module(library(dcgs)).`, `:- use_module(library(charsio)).`, `:- use_module(library(lambda)).`).
7. **Control Structures & CLP(Z)**: Use standard ISO control structures `(,)/2`, `(;)/2`. Prefer CLP(Z) constraints (`#=`, `#>`) and reified arithmetic (`zcompare/3`) over low-level evaluation (`is/2`, `>/2`).
8. **Clean Data Representations**: Prefer clean data structures where element kinds are distinguished by principal functor (`leaf(L)` vs `node(L, R)`). Avoid defaulty representations that force runtime type tests (`var/1`) or procedural default branches. Convert raw input data into clean trees early.
9. **Macro & Compile-Time Expansion**: Use Prolog's macro mechanism (`user:term_expansion/2` and `user:goal_expansion/2`) to transform clauses or rewrite inline goals at compile time to eliminate boilerplate and redundant rules. Prefer static compile-time expansion over dynamic database modification (`asserta`/`assertz`).
10. **Avoid Non-Standard Extensions**: Do not rely on engine-specific types (e.g. SWI dicts or SWI string types) when writing standard Prolog code.
11. **Safety**: Execute code using `prolog-safe`.

## Universal Guidelines & References

- [Covington Prolog Style Guide](../../references/covington_style.md)
- [Prolog Purity Guidelines](../../references/prolog_guidelines.md)
- [Metalevel.at Clean Data Representations](https://www.metalevel.at/prolog/data#clean)
- [Metalevel.at Prolog Efficiency](https://www.metalevel.at/prolog/efficiency)

