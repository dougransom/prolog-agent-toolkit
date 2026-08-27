## [0.0.1.dev11] - 2026-08-27

### Summary of Changes
- Release v0.0.1.dev11 synchronized across manifest files.

### Added / Modified Predicates
- Dialect updates and purity enhancements.

### Breaking Changes
- None.


## [0.0.1.dev10] - 2026-08-27

### Summary of Changes
- Updated `README.md` to remove file-copying setup and promote `skills.json` multi-directory search path as Option B (Recommended for Personal Setup).
- Added tip in `CONTRIBUTING.md` for automating engine onboarding with `prolog-engine-onboarding` skill.
- Synchronized version `v0.0.1.dev10` across manifest files.

### Added / Modified Predicates
- Documentation and setup configuration updates.

### Breaking Changes
- None.


## [0.0.1.dev9] - 2026-08-27

### Summary of Changes
- Release v0.0.1.dev9 synchronized across manifest files.

### Added / Modified Predicates
- Dialect updates and purity enhancements.

### Breaking Changes
- None.


## [0.0.1.dev8] - 2026-08-27

### Summary of Changes
- Added Standard Library Cheat Sheets across all dialect skills (`scryer-prolog-standards`, `swi-prolog-standards`, `trealla-prolog-standards`, `tau-prolog-standards`).
- Added Standard Library Steering rules to `.agents/AGENTS.md` and `.agents/skills/prolog-conventions/SKILL.md` to enforce explicit `:- use_module(library(...)).` headers while prohibiting raw OS stdlib file inspection.
- Created `prolog-engine-onboarding` interactive skill (`.agents/skills/prolog-engine-onboarding/SKILL.md`) for onboarding new Prolog engines iteratively.
- Added "Onboarding an Additional Prolog System" section to `README.md`.

### Added / Modified
- `.agents/skills/scryer-prolog-standards/SKILL.md`: Added stdlib cheat sheet table for `dcgs`, `charsio`, `reif`, `clpz`, `si`, `lambda`, `lists`, `format`, `assoc`, `between`, `time`, `random`.
- `.agents/skills/swi-prolog-standards/SKILL.md`: Added stdlib cheat sheet table for `clpfd`, `yall`, `apply`, `dcg/basics`, `ordsets`, `plunit`, and dicts.
- `.agents/skills/trealla-prolog-standards/SKILL.md`: Added stdlib cheat sheet table for `dcgs`, `charsio`, `clpz`, `reif`, `when`, `format`, `random`.
- `.agents/skills/tau-prolog-standards/SKILL.md`: Added stdlib cheat sheet table for `dom`, `js`, `lists`, `format`, `random`.
- `.agents/skills/prolog-engine-onboarding/SKILL.md`: 6-phase interactive workflow for adding new Prolog engine targets.
- `.agents/AGENTS.md` & `README.md`: Documented onboarding skill and standard library cheat sheet steering rules.

### Breaking Changes
- None.


## [0.0.1.dev7] - 2026-08-26

### Summary of Changes
- Integrated complete canonical `README.md` generator into Python project initializer (`project.py`) and bash initializer script (`prolog_agent_init.sh`).
- Enhanced main `README.md` with explicit `uv tool` installation workflows, CLI reference summary table, and quickstart guides for new and existing Prolog projects.

### Added / Modified
- Updated `prolog_agent_toolkit/project.py` with `generate_readme_content` supporting dynamic dialect descriptions, manifest names, safe runner commands, and test suites.
- Updated `scripts/prolog_agent_init.sh` to generate the matching structured 6-section README layout.
- Updated main `README.md` with step-by-step onboarding for bootstrapping new projects and adopting rules/subagents in existing Prolog codebases.
- Updated `.agents/skills/prolog-initializer/SKILL.md` documentation.

### Breaking Changes
- None.



## [0.0.1.dev6] - 2026-08-26

### Summary of Changes
- Dialect-aware project initializer, template generator, module generator, and bash initializer script.
- Added `prolog-agent template`, `prolog-agent module`, `prolog-agent init-script` CLI subcommands.

### Added / Modified
- Added `.agents/skills/prolog-initializer/SKILL.md` and ready-to-drop `.agents/skills/initializer.pl`.
- Added POSIX bash project initializer script `scripts/prolog_agent_init.sh`.
- Added canonical starter project template in `templates/starter_project/`.
- Added dialect-aware module template in `templates/module_template.pl.tpl`.

### Breaking Changes
- None.



## [0.0.1.dev5] - 2026-08-26

### Summary of Changes
- Release v0.0.1.dev5 synchronized across manifest files.

### Added / Modified Predicates
- Dialect updates and purity enhancements.

### Breaking Changes
- None.


## [0.0.1.dev4] - 2026-08-26

### Summary of Changes
- Release v0.0.1.dev4 synchronized across manifest files.

### Added / Modified Predicates
- Dialect updates and purity enhancements.

### Breaking Changes
- None.


# Changelog

All notable changes to this project will be documented in this file.

## [0.0.1] - 2026-08-26

### Summary of Changes
- Release v0.0.1 synchronized across manifest files.

### Added / Modified Predicates
- Dialect updates and purity enhancements.

### Breaking Changes
- None.

