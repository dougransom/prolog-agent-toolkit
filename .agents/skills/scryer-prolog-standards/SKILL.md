---
name: scryer-prolog-standards
description: Coding standards and guidelines for pure, ISO-compliant Scryer Prolog projects. Use when writing, refactoring, or debugging Prolog code specifically for Scryer Prolog.
---

# Scryer Prolog Standards

When writing, refactoring, or reviewing Prolog code for Scryer Prolog, adhere to these standards:

## Core Rules

- **Implementation**: Always use Scryer Prolog (ISO-compliant). Never use SWI-Prolog specifics like dicts, string types, or `is_list/1`.
- **Type Tests**: Prefer `library(si)` (`list_si/1`, `atom_si/1`, `chars_si/1`, `integer_si/1`).
- **Strings**: Treat strings as lists of characters (`chars`). `double_quotes` must always be set to `chars`.
- **Libraries**: Explicitly import `:- use_module(library(dcgs)).` and `:- use_module(library(charsio)).`.
- **DCGs**: Use pure DCG syntax for all parsing and matching logic.
- **Purity**: Prefer `dif/2` (`library(dif)`) and `if_/3` (`library(reif)`). Avoid `->` when `if_/3` can be used.
- **Safety**: Execute code using `scryer-safe` or `prolog-safe` with `PROLOG_ENGINE=scryer`.
