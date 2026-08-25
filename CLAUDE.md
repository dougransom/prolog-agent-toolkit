# Prolog Agent Toolkit — Claude Code Instructions

When working with Prolog code in this repository or target Prolog projects, adhere to the universal standards defined below:

## CLI Safety Wrappers
- **CLI Entry Points**: ALWAYS use the cross-platform CLI safety entry points (`prolog-safe`, `scryer-safe`, `swi-safe`, `trealla-safe`).
- **Forbidden Invocations**: NEVER execute raw interpreter binaries (`scryer-prolog`, `swipl`, `tpl`, `gprolog`, `ciao`) directly.
- **Specifying Engine**: Set `PROLOG_ENGINE` environment variable (e.g., `export PROLOG_ENGINE=scryer`).

## Prolog Style & Guidelines
- **ISO Scryer Prolog**: Prefer pure Scryer Prolog (ISO-compliant).
- **Strings**: Treat strings as lists of characters (`chars`).
- **Logical Purity**: Prefer `dif/2`, `clpz`, and `if_/3` from `library(reif)`. Avoid unnecessary cuts (`!`).
- **Definite Clause Grammars (DCGs)**: Use pure DCG syntax (`-->`) for parsing, formatting, string building, and state threading.
- **Term & Goal Expansion**: Use compile-time hooks (`user:term_expansion/2`, `user:goal_expansion/2`) to eliminate boilerplate code.

## References & Skills
See [.agents/AGENTS.md](.agents/AGENTS.md) and [.agents/skills/](.agents/skills/) for detailed dialect rules, unit testing (`testing.pl`), packaging (`bakage`), and release workflows.
