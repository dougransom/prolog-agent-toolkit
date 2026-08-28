---
name: trealla-prolog-standards
description: Coding standards and guidelines for Trealla Prolog applications and WASM targets. Use when targeting Trealla Prolog specifically.
---

# Trealla Prolog Standards

Guidelines for writing idiomatic Trealla Prolog code:

## Core Rules

1. **ISO Code Target**: Trealla Prolog emphasizes fast execution, modularity, and WASM support. AI agents should attempt to produce standard ISO-compliant code subject to Trealla's capabilities and limitations.
2. **Text & Double Quotes**: Follow standard character lists (`chars`) representation.
3. **Library Cheat-Sheet Usage**: Explicitly declare imports using `:- use_module(library(...)).`. Use the Standard Library Cheat Sheet below.
4. **Safety**: Always execute code using `trealla-safe` or `prolog-safe` with `PROLOG_ENGINE=trealla`.

## Trealla Prolog Standard Library Cheat Sheet

| Feature / Topic | Import Header | Primary Exported Predicates | Notes / Dialect Rules |
| :--- | :--- | :--- | :--- |
| **DCG Parsing** | `:- use_module(library(dcgs)).` | `phrase/2`, `phrase/3` | Standard ISO DCG grammars. |
| **Character I/O** | `:- use_module(library(charsio)).` | `read_from_chars/2`, `write_to_chars/2` | Double-quoted strings are `chars`. |
| **CLP(Z) Constraints**| `:- use_module(library(clpz)).` | `(#=)/2`, `label/1`, `labeling/2` | Integer constraints in Trealla (`clpz`). |
| **Reified Logic** | `:- use_module(library(reif)).` | `if_/3`, `dif/2`, `(=)/3` | Reified condition evaluation. |
| **Coroutining / Delay**| `:- use_module(library(when)).` | `when/2`, `freeze/2` | Goal suspension and coroutining. |
| **Formatted Printing**| `:- use_module(library(format)).` | `format/2`, `format/3` | C-style formatted string/stdout output. |
| **Randomization** | `:- use_module(library(random)).` | `maybe/0`, `random_integer/3` | Fast pseudorandom generation. |

## Universal Guidelines & References

- [Covington Prolog Style Guide](../../references/covington_style.md)
- [Prolog Purity Guidelines](../../references/prolog_guidelines.md)
