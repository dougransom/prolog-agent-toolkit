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
5. **Safety**: Always execute Node.js / CLI runner scripts using `tau-safe` or `prolog-safe` with `PROLOG_ENGINE=tau`.

## Universal Guidelines & References

- [Covington Prolog Style Guide](../../references/covington_style.md)
- [Prolog Purity Guidelines](../../references/prolog_guidelines.md)
