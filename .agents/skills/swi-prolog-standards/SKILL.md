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
4. **Safety**: Always execute code using `swi-safe` or `prolog-safe` with `PROLOG_ENGINE=swi`.
