---
name: prolog-conventions
description: Coding standards and guidelines for writing portable ISO-compliant Prolog code across Prolog systems. Use when writing code intended to run across multiple engines subject to engine capabilities.
---

# Portable ISO Prolog Conventions

Guidelines for writing clean, portable Prolog code aiming for standard ISO compliance subject to target engine limitations.

## Core Guidelines

1. **Logical Purity & Impure Construct Restrictions**: Prefer pure predicates (`dif/2`, `if_/3`). NEVER introduce cuts (`!`), negation-as-failure (`\+/1`), or soft cuts (`->`) for performance optimization. If an impure construct (`!`, `\+/1`, `->`) must be introduced for *correctness* (when pure constructs `if_/3` or `dif/2` cannot express the logic), write an explicit inline comment justifying why pure logic constructs were insufficient. Prefer `dif(X, Y)` over `\+ (X = Y)` for sound term inequality.
2. **Strings as Character Lists (`chars`)**: Represent strings and text as lists of characters (`chars`). `double_quotes` must always be set to `chars`.
3. **Safe Type Testing**: Prefer pure, safe type tests (e.g. `library(si)`: `list_si/1`, `atom_si/1`, `chars_si/1`, `integer_si/1`) over impure non-monotonic type checks (`is_list/1`).
4. **Higher-Order Logic & Lambdas**: Use higher-order predicates (`call/N`, `call//N`, `maplist/N`, `foldl/N`, `include/3`, `exclude/3`) and `library(lambda)` (`\X^...`, `\X^Y^Goal`) to eliminate code repetition.
5. **Standard & Higher-Order DCGs**: Use Definite Clause Grammars (`-->`) for sequence parsing, formatting, and tree transformations. Use `call//N` for higher-order DCG non-terminals.
6. **Explicit Library Declarations**: Always explicitly import required library modules (e.g. `:- use_module(library(dcgs)).`, `:- use_module(library(charsio)).`, `:- use_module(library(lambda)).`, `:- use_module(library(clpz)).`). Do not assume SWI-style autoloading when targeting ISO or embedded engines.
7. **Control Structures & CLP(Z)**: Use standard ISO control structures `(,)/2`, `(;)/2`. Prefer CLP(Z) constraints (`#=`, `#>`) and reified arithmetic (`zcompare/3`) over low-level evaluation (`is/2`, `>/2`).
8. **Coroutining & Goal Suspension**: Use `freeze/2` for single-variable activation guards (`nonvar/1`) and `when/2` for multi-variable or disjunctive activation conditions (`(nonvar(A) ; nonvar(B))`). Prefer CLP(Z)/`dif/2` over manual coroutining where domain-specific constraints apply.
9. **Clean Data Representations**: Prefer clean data structures where element kinds are distinguished by principal functor (`leaf(L)` vs `node(L, R)`). Avoid defaulty representations that force runtime type tests (`var/1`) or procedural default branches. Convert raw input data into clean trees early.
10. **Macro & Compile-Time Expansion**: Use Prolog's macro mechanism (`user:term_expansion/2` and `user:goal_expansion/2`) to transform clauses or rewrite inline goals at compile time to eliminate boilerplate and redundant rules. Prefer static compile-time expansion over dynamic database modification (`asserta`/`assertz`).
11. **Avoid Non-Standard Extensions**: Do not rely on engine-specific types (e.g. SWI dicts or SWI string types) when writing standard Prolog code.
12. **Library Steering vs Reading Source**: Rely on dialect-specific Standard Library Cheat Sheets for module header declarations and predicate exports. AI assistants MUST NOT read raw standard library implementation source files, relying instead on concise cheat sheets and pre-trained semantics to save context tokens.
13. **Safety**: Execute code using `prolog-safe`.

## Universal Guidelines & References

- [Covington Prolog Style Guide](../../references/covington_style.md)
- [Prolog Purity Guidelines](../../references/prolog_guidelines.md)
- [Metalevel.at Clean Data Representations](https://www.metalevel.at/prolog/data#clean)
- [Metalevel.at Prolog Efficiency](https://www.metalevel.at/prolog/efficiency)

