---
name: scryer-prolog-standards
description: Coding standards and guidelines for pure, ISO-compliant Scryer Prolog projects. Use when writing, refactoring, or debugging Prolog code specifically for Scryer Prolog.
---

# Scryer Prolog Standards

When writing, refactoring, or reviewing Prolog code for Scryer Prolog, adhere to these standards:

## Core Rules

Scryer Prolog strictly enforces pure, ISO-compliant Prolog conventions:

- **General Prolog Conventions**: Inherits all general rules from [Portable ISO Prolog Conventions](../prolog-conventions/SKILL.md) (strings as `chars`, safe `library(si)` type tests, `dif/2`, `if_/3` reification, higher-order `call/N`, `call//N`, and `library(lambda)`).
- **No Non-Standard Specifics**: Never use SWI-Prolog specifics like dicts, SWI string types, or `is_list/1`.
- **Required Library Imports**: Always explicitly declare imports (e.g. `:- use_module(library(dcgs)).`, `:- use_module(library(charsio)).`, `:- use_module(library(lambda)).`).
- **Safety Execution**: Execute code using `scryer-safe` or `prolog-safe` with `PROLOG_ENGINE=scryer`.

## Universal Guidelines & References

- [Portable ISO Prolog Conventions](../prolog-conventions/SKILL.md)
- [Covington Prolog Style Guide](../../references/covington_style.md)
- [Prolog Purity Guidelines](../../references/prolog_guidelines.md)
