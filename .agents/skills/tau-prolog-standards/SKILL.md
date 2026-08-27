---
name: tau-prolog-standards
description: Coding standards and guidelines for Tau Prolog applications, Node.js scripts, and browser DOM targets. Use when targeting Tau Prolog specifically.
---

# Tau Prolog Standards

Guidelines for writing idiomatic Tau Prolog code:

## Core Rules

1. **ISO Compliance & JS Execution**: Tau Prolog is an open-source ISO Prolog interpreter implemented entirely in JavaScript for browser and Node.js environments.
2. **Text & Double Quotes**: Follow standard ISO character lists (`chars`) representation for string manipulation.
3. **DOM & JS Interoperability**:
   - Use `library(dom)` for browser DOM queries and event handling.
   - Use `library(js)` for JavaScript interop and object inspection.
   - Use `library(random)` for random number generation.
4. **Asynchronous Query Execution**:
   - In JavaScript embeddings, handle queries asynchronously using session callback streams (`session.query()`, `session.answer()`).
5. **Library Cheat-Sheet Usage**: Always include explicit `:- use_module(library(...)).` headers based on the Standard Library Cheat Sheet below.
6. **Safety**: Always execute Node.js / CLI runner scripts using `tau-safe` or `prolog-safe` with `PROLOG_ENGINE=tau`.

## Tau Prolog Standard Library Cheat Sheet

| Feature / Topic | Import Header | Primary Exported Predicates | Notes / Dialect Rules |
| :--- | :--- | :--- | :--- |
| **DOM Integration** | `:- use_module(library(dom)).` | `get_by_id/2`, `set_html/2`, `add_event_listener/3` | Browser DOM manipulation. |
| **JS Interoperability**| `:- use_module(library(js)).` | `eval/2`, `global/2`, `prop/3` | Direct JavaScript runtime interop. |
| **List Manipulation** | `:- use_module(library(lists)).` | `member/2`, `append/3`, `length/2` | Core ISO list utilities. |
| **Formatted Printing**| `:- use_module(library(format)).` | `format/2`, `format/3` | Formatted string output. |
| **Randomization** | `:- use_module(library(random)).` | `random/1`, `random_integer/3` | JS-backed random generator. |

## Universal Guidelines & References

- [Covington Prolog Style Guide](../../references/covington_style.md)
- [Prolog Purity Guidelines](../../references/prolog_guidelines.md)
