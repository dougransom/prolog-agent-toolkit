---
name: iso-prolog-standards
description: Coding standards and guidelines for portable, pure ISO-compliant Prolog across all conforming engines. Use when writing Prolog code intended to run on any ISO Prolog interpreter.
---

# ISO Prolog Standards

Guidelines for writing clean, portable, pure ISO-compliant Prolog.

## Core Guidelines

1. **Logical Purity**: Prefer pure predicates. Avoid unnecessary side effects or non-deterministic cuts `!` where pure logic constructs can be used.
2. **Standard DCGs**: Use Definite Clause Grammars (`-->`) for sequence parsing, formatting, and tree transformations.
3. **Control Structures**: Use standard ISO control structures: `(\+)/1`, `(,)/2`, `(;)/2`.
4. **Avoid Non-Standard Extensions**: Do not rely on engine-specific types (e.g. SWI dicts or SWI strings) when writing portable code. Represent text as lists of characters or standard atoms.
5. **Safety**: Execute code using `prolog-safe`.

## Universal Guidelines & References

- [Covington Prolog Style Guide](../../references/covington_style.md)
- [Prolog Purity Guidelines](../../references/prolog_guidelines.md)
