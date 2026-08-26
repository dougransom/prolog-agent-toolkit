# Prolog Agent Toolkit Guidelines & Standards

When writing, refactoring, reviewing, or running Prolog code across any project or Prolog engine, all AI assistants MUST adhere to the standards defined below.

## Universal Prolog Style & Purity Guidelines

All Prolog code (regardless of target engine) MUST follow the universal style and purity principles:

- **Covington Prolog Style Guide**: [.agents/references/covington_style.md](.agents/references/covington_style.md)
  - Write for humans first; keep clauses simple and readable; use explicit goal ordering and clean predicate naming.
- **Purity Guidelines**: [.agents/references/prolog_guidelines.md](.agents/references/prolog_guidelines.md)
  - Prefer logical purity (`if_/3`, `dif/2`, pure DCGs); avoid unnecessary cuts (`!`) and side effects.
  - When relating conditions to values, isolate the test-value relation (e.g. `if_(G, A="A", A="B"), write(A)`).
- **Declarative AI Workflow**: [.agents/skills/prolog-declarative-workflow/SKILL.md](.agents/skills/prolog-declarative-workflow/SKILL.md)
  - Use declarative reasoning based on unification, constraints, and backtracking (never imperative thinking).
  - Specify mode (`+`/`-`), determinism (`det`, `semidet`, `nondet`), and choice-point expectations.
  - Use test-first scaffolding (`testing.pl` / `plunit` / configured test framework) and DCG structure generation.

## Multi-Engine Dialect Selection & Rules

AI assistants MUST select and follow the specific dialect standards corresponding to the target Prolog engine:

- **ISO Scryer Prolog**: [.agents/skills/scryer-prolog-standards/SKILL.md](.agents/skills/scryer-prolog-standards/SKILL.md)
  - Pure DCGs, `library(si)`, `chars` strings, `dif/2`, `if_/3` from `library(reif)`.
- **SWI-Prolog**: [.agents/skills/swi-prolog-standards/SKILL.md](.agents/skills/swi-prolog-standards/SKILL.md)
  - SWI dicts, SWI string types, module declarations, pack manager.
- **Trealla Prolog**: [.agents/skills/trealla-prolog-standards/SKILL.md](.agents/skills/trealla-prolog-standards/SKILL.md)
  - ISO compliance, WASM embedding, fast standard library parsing.
- **Tau Prolog**: [.agents/skills/tau-prolog-standards/SKILL.md](.agents/skills/tau-prolog-standards/SKILL.md)
  - ISO compliance, JavaScript/Browser DOM integration, `library(dom)`, `library(js)`.
- **Portable ISO Prolog Conventions**: [.agents/skills/prolog-conventions/SKILL.md](.agents/skills/prolog-conventions/SKILL.md)
  - Engine-agnostic ISO standard code compatible across all conforming implementations.
- **Prolog Testing**: [.agents/skills/prolog-testing/SKILL.md](.agents/skills/prolog-testing/SKILL.md)
  - Scryer `testing.pl` (default), SWI `plunit`, and portable ISO assertions.
- **Prolog Packaging**: [.agents/skills/prolog-packaging/SKILL.md](.agents/skills/prolog-packaging/SKILL.md)
  - Scryer `bakage` manifests (default) and SWI `pack` manager.
- **Prolog Release & Versioning**: [.agents/skills/prolog-release/SKILL.md](.agents/skills/prolog-release/SKILL.md)
  - Multi-file version synchronization (`pack.pl`, `pyproject.toml`, `README.md`), Git tagging, and post-release prompts.

## Project Bootstrapping & Setup Workflow


When initializing, bootstrapping, or creating a new Prolog project/repository, all AI assistants MUST prompt the user:
1. **Testing Setup**: *"Would you like to set up unit testing (`testing.pl` for Scryer, `plunit` for SWI)?"*
2. **Packaging Setup**: *"Would you like to set up package metadata (`bakage` manifest `pack.pl` for Scryer, `pack.pl` for SWI)?"*

## Safety & Cross-Platform Execution

- **CLI Entry Points**: ALL Prolog code executions MUST use the cross-platform CLI safety entry points (`prolog-safe`, `scryer-safe`, `swi-safe`, `trealla-safe`, `tau-safe`).
- **Forbidden Invocations**: AI assistants MUST NEVER execute raw interpreter binaries (`scryer-prolog`, `swipl`, `tpl`, `tau-prolog`, `gprolog`, `ciao`) directly.
- **Specifying Engine**: Set `PROLOG_ENGINE` environment variable (e.g., `export PROLOG_ENGINE=scryer`, `export PROLOG_ENGINE=swi`, `export PROLOG_ENGINE=trealla`, `export PROLOG_ENGINE=tau`).


## Git Branching & Release Workflow

AI assistants MUST adhere to the following release workflow:

1. **Development Branching**: Development commits for current work take place on branch `DEV202608` (or active development branch).
2. **Dev Version Format**: Working version numbers follow the `X.Y.Z.devN` convention (e.g. `0.0.1.dev1`) across `README.md`, `pyproject.toml`, and `prolog_agent_toolkit/__init__.py`.
3. **Release Execution**:
   - Update version in `README.md`, `pyproject.toml`, and `prolog_agent_toolkit/__init__.py` to release version (e.g. `0.0.1`).
   - Create annotated Git tag (e.g. `git tag -a v0.0.1 -m "Release v0.0.1"`).
   - Commit and push.
4. **Post-Release Prompting**:
   - Immediately after a release, ask the user:
     1. Is a new dev branch warranted?
     2. What is the current release number?
     3. What is the next release to work on (and update version with `.dev1`)?
