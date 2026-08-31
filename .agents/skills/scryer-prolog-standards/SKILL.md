---
name: scryer-prolog-standards
description: Coding standards and guidelines for pure Scryer Prolog projects. Use when writing, refactoring, or debugging Prolog code specifically for Scryer Prolog.
---

# [Scryer Prolog](https://github.com/mthom/scryer-prolog) Standards

When writing, refactoring, or reviewing Prolog code for Scryer Prolog, adhere to these standards:

## Core Rules

Scryer Prolog guidelines emphasize pure Prolog conventions and standard ISO-compliant code structures:

- **General Prolog Conventions**: Inherits all general rules from [Portable ISO Prolog Conventions](../prolog-conventions/SKILL.md) (strings as `chars`, safe [`library(si)`](https://github.com/mthom/scryer-prolog/blob/master/src/lib/si.pl) type tests, `dif/2`, `if_/3` reification from [`library(reif)`](https://github.com/mthom/scryer-prolog/blob/master/src/lib/reif.pl), higher-order `call/N`, `call//N`, and [`library(lambda)`](https://github.com/mthom/scryer-prolog/blob/master/src/lib/lambda.pl)). Agents should attempt to write ISO-compliant code subject to Scryer's capabilities.
- **No Non-Standard Specifics**: Never use [SWI-Prolog](https://www.swi-prolog.org/) specifics like dicts, SWI string types, or `is_list/1`.
- **Required Library Imports**: Always explicitly declare imports using `:- use_module(library(...)).`. Do not rely on SWI-Prolog autoloading.
- **Library Cheat-Sheet Usage**: Rely on the Standard Library Cheat Sheet below for module declarations; do NOT read raw standard library source files unless working with un-documented custom project code.
- **Safety Execution**: Execute code using `scryer-safe` or `prolog-safe` with `PROLOG_ENGINE=scryer`.

## Scryer Prolog Standard Library Cheat Sheet

> **Universal Coding Standards Note**: The cheat sheet table below specifies Scryer-specific module import headers (`:- use_module(library(...)).`). The underlying coding guidelines, purity rules, reification patterns (`=(X,Y,Truth)`, `cond_t`, `if_`), integer constraints (`clpz`), DCGs, safe type testing (`library(si)`), higher-order lambdas, and formatted output follow the **universal Prolog coding standards** defined in [`prolog-conventions`](../prolog-conventions/SKILL.md) and [`prolog_guidelines.md`](../../references/prolog_guidelines.md).

| Feature / Topic | Import Header | Primary Exported Predicates | Notes / Dialect Rules |
| :--- | :--- | :--- | :--- |
| **DCG Parsing** | `:- use_module(`[`library(dcgs)`](https://github.com/mthom/scryer-prolog/blob/master/src/lib/dcgs.pl)`).` | `phrase/2`, `phrase/3`, `seq//1`, `seq_with//2` | Mandatory for any `-->` grammars. |
| **Character I/O** | `:- use_module(`[`library(charsio)`](https://github.com/mthom/scryer-prolog/blob/master/src/lib/charsio.pl)`).` | `read_from_chars/2`, `write_to_chars/2`, `get_single_char/1` | All strings in Scryer are `chars`. |
| **Reified Logic** | `:- use_module(`[`library(reif)`](https://github.com/mthom/scryer-prolog/blob/master/src/lib/reif.pl)`).` | `if_/3`, `cond_t/3`, `dif/2`, `dif/3`, `(=)/3`, `memberd_t/3`, `tfilter/3`, `tpartition/4` | Pure reified conditional testing & collection traversals. Prefer direct reified predicates (`=/3`, `memberd_t/3`, `dif/3`) and `cond_t` over `if_`/`->`. |
| **CLP(Z) Constraints**| `:- use_module(`[`library(clpz)`](https://github.com/mthom/scryer-prolog/blob/master/src/lib/clpz.pl)`).` | `(#=)/2`, `(#\/)/2`, `label/1`, `labeling/2`, `zcompare/3` | Integer arithmetic constraints (Scryer uses `clpz`, NOT `clpfd`). |
| **Safe Type Testing**| `:- use_module(`[`library(si)`](https://github.com/mthom/scryer-prolog/blob/master/src/lib/si.pl)`).` | `list_si/1`, `atom_si/1`, `integer_si/1`, `chars_si/1` | Monotonic type tests (`si` = safely instantiated). |
| **Higher-Order Lambda**| `:- use_module(`[`library(lambda)`](https://github.com/mthom/scryer-prolog/blob/master/src/lib/lambda.pl)`).` | `\X^...`, `\X^Y^Goal` | Inline anonymous lambda expressions. |
| **Formatted Output** | `:- use_module(`[`library(format)`](https://github.com/mthom/scryer-prolog/blob/master/src/lib/format.pl)`).` | `format/2`, `format/3`, `portray_clause/1` | Formatted printing with `~w`, `~q`, `~a`, `~s`. |
| **List Utilities** | `:- use_module(`[`library(lists)`](https://github.com/mthom/scryer-prolog/blob/master/src/lib/lists.pl)`).` | `member/2`, `select/3`, `append/3`, `length/2`, `reverse/2` | Core list manipulation. |
| **Association Maps** | `:- use_module(`[`library(assoc)`](https://github.com/mthom/scryer-prolog/blob/master/src/lib/assoc.pl)`).` | `empty_assoc/1`, `get_assoc/3`, `put_assoc/4` | AVL-tree key-value maps. |
| **Range Iteration** | `:- use_module(`[`library(between)`](https://github.com/mthom/scryer-prolog/blob/master/src/lib/between.pl)`).` | `between/3` | Integer range generation. |
| **Time & System** | `:- use_module(`[`library(time)`](https://github.com/mthom/scryer-prolog/blob/master/src/lib/time.pl)`).` | `time/1`, `current_time/1` | Benchmarking and timestamping. |
| **Randomization** | `:- use_module(`[`library(random)`](https://github.com/mthom/scryer-prolog/blob/master/src/lib/random.pl)`).` | `maybe/0`, `random_integer/3` | Pseudorandom generation. |

## Universal Guidelines & References

- [Portable ISO Prolog Conventions](../prolog-conventions/SKILL.md)
- [Covington Prolog Style Guide](../../references/covington_style.md)
- [Prolog Purity Guidelines](../../references/prolog_guidelines.md)
