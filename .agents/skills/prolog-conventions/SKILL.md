---
name: prolog-conventions
description: Coding standards and guidelines for portable, pure ISO-compliant Prolog across all conforming engines. Use when writing Prolog code intended to run on any ISO Prolog interpreter.
---

# Prolog Conventions

Guidelines for writing clean, portable, pure ISO-compliant Prolog.

## Core Guidelines

1. **Logical Purity**: Prefer pure predicates. Avoid unnecessary side effects or non-deterministic cuts `!` where pure logic constructs can be used.
2. **Standard DCGs**: Use Definite Clause Grammars (`-->`) for sequence parsing, formatting, and tree transformations.
3. **Control Structures**: Use standard ISO control structures:  `(,)/2`, `(;)/2`.  But consider alternatives to non-monotonic structures, like `(\+)/1` and `!/0`, where possible.
4. Prefer CLPZ constraints like (#=)/2, (#>)/2 instead of the built ins (is)/2, (>)/2, (=:=)/2 etc. Prefer reification of constraints where possible.  See CLPZ and reif documentation in references. Treat (is)/2, (>)/2, (=:=)/2  as lower level predicates more suitable when optimizing for performance in term_expansions or goal expansions.  Reference https://www.metalevel.at/prolog/clpz.

5. **Avoid Non-Standard Extensions**: Do not rely on engine-specific types (e.g. SWI dicts or SWI strings) when writing portable code. Represent text as lists of characters or standard atoms.
6. **Safety**: Execute code using `prolog-safe`.

## Universal Guidelines & References

- [Covington Prolog Style Guide](../../references/covington_style.md)
- [Prolog Purity Guidelines](../../references/prolog_guidelines.md)
