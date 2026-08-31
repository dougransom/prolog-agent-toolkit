## [0.0.1.dev19] - 2026-08-31

### Summary of Changes
- Standardized software package metadata format by renaming `schema.org.jsonld` to `codemeta.json` adhering to the CodeMeta / Schema.org JSON-LD standard for software repositories.
- Updated package URLs in `pyproject.toml` to point to `codemeta.json`.
- Updated release synchronization (`prolog_agent_toolkit/release.py`) and pre-commit test assertions (`tests/test_hooks.py`) to validate `codemeta.json`.
- Updated project documentation, file tree maps, and engine onboarding guidelines across `README.md`, `AGENT_GUIDE.md`, `CONTRIBUTING.md`, `docs/index.html`, `docs/adr/0003-pyproject-version-source-of-truth.md`, and `.agents/AGENTS.md`.

### Added / Modified
- `codemeta.json`: Renamed from `schema.org.jsonld` and added `"codemeta"` keyword.
- `prolog_agent_toolkit/release.py`: Updated version check and synchronization to target `codemeta.json`.
- `tests/test_hooks.py`: Updated hook and version parity tests.
- `pyproject.toml`, `README.md`, `AGENT_GUIDE.md`, `CONTRIBUTING.md`, `docs/index.html`, `docs/adr/0003-pyproject-version-source-of-truth.md`, `.agents/AGENTS.md`, `.agents/skills/prolog-engine-onboarding/SKILL.md`: Updated metadata file references.

### Breaking Changes
- Renamed repository root metadata file `schema.org.jsonld` to `codemeta.json`.


## [0.0.1.dev18] - 2026-08-31

### Summary of Changes
- Added Meta-Predicate Declarations (`:- meta_predicate`) guidelines and standards across `prolog-conventions`, `prolog-dcg-mastery`, `prolog-code-review`, `AGENTS.md`, and `prolog_guidelines.md`.
- Added explicit rules for caller-module expansion, closure arity specifiers (`0`, `1`..`N`, `//`), and non-callable data term markings (`+`, `-`, `?`, `*`).
- Updated Code Review checklist to audit module encapsulation and meta-predicate declarations.
- Synchronized version `0.0.1.dev18` across manifests and documentation.

### Added / Modified
- `.agents/skills/prolog-conventions/SKILL.md`: Added Rule 9 on Meta-Predicate Declarations.
- `.agents/skills/prolog-code-review/SKILL.md`: Added Meta-Predicate Declarations verification row to code review checklist.
- `.agents/skills/prolog-dcg-mastery/SKILL.md`: Added meta-predicate declarations example for higher-order DCG non-terminals.
- `.agents/AGENTS.md`: Added meta-predicate declaration standard to Universal Prolog Style & Purity Guidelines.
- `.agents/references/prolog_guidelines.md`: Added detailed meta-predicate reference section.

### Breaking Changes
- None.


## [0.0.1.dev17] - 2026-08-29

### Summary of Changes
- Updated `CONTRIBUTING.md` guidelines for reporting unwanted AI-generated Prolog code ("AI slop", copy-pasted loops, unnecessary low-level cuts `!`, `->`, `\+`) to refine agent rules and purity standards.
- Created GitHub issues [#2](https://github.com/dougransom/prolog-agent-toolkit/issues/2) and [#3](https://github.com/dougransom/prolog-agent-toolkit/issues/3) for agent purity guidance and duplication detection/refactoring.

### Added / Modified
- `CONTRIBUTING.md`: GitHub Issues reporting guidelines.

### Breaking Changes
- None.


## [0.0.1.dev16] - 2026-08-28

### Summary of Changes
- Refactored ISO Prolog references across `AGENTS.md`, dialect skills (`scryer`, `trealla`, `tau`, `prolog-conventions`), documentation (`GLOSSARY.md`, `README.md`, `AGENT_GUIDE.md`, `CONTRIBUTING.md`, `ADR 0001`), and CLI scaffolding (`project.py`, `prolog_agent_init.sh`) to eliminate claims of Prolog engine ISO compliance.
- Established explicit directive for AI agents to attempt ISO-compliant code generation (ISO/IEC 13211-1) subject to target engine capabilities and limitations.
- Addresses defect report https://github.com/dougransom/prolog-agent-toolkit/issues/1 and community discussion https://github.com/mthom/scryer-prolog/discussions/3436.

### Added / Modified Predicates
- ISO Prolog code generation directive and target policy in `.agents/AGENTS.md`.

### Breaking Changes
- None.


## [0.0.1.dev15] - 2026-08-28

### Summary of Changes
- Release v0.0.1.dev15 synchronized across manifest files.

### Added / Modified Predicates
- Dialect updates and purity enhancements.

### Breaking Changes
- None.


## [0.0.1.dev14] - 2026-08-28

### Summary of Changes
- Updated project descriptions to emphasize reusable AI agent skills, coding standards, and multi-engine safety execution.
- Enhanced Agent Navigation Quick Start section in `README.md` with explicit links to purity standards, library discovery protocol (`prolog-agent discover`), and agent guidelines (`AGENTS.md`).
- Synchronized version `0.0.1.dev14` across all manifests (`pyproject.toml`, `README.md`, `schema.org.jsonld`, `docs/capability_manifest.json`, `docs/repository_ontology.json`, `CHANGELOG.md`).

### Added / Modified
- `README.md`, `pyproject.toml`, `schema.org.jsonld`: Refined project description and navigation references.
- `docs/capability_manifest.json`, `docs/repository_ontology.json`: Updated version metadata to `0.0.1.dev14`.

### Breaking Changes
- None.


## [0.0.1.dev13] - 2026-08-28

### Summary of Changes
- Created human-readable Repository Ontology documentation in [`docs/ONTOLOGY.md`](docs/ONTOLOGY.md) explaining the 3-Layer Ontology Architecture (Component Graph, Capability Registry, Domain Terminology).
- Integrated ontology cross-references across [`docs/GLOSSARY.md`](docs/GLOSSARY.md) and [`AGENT_GUIDE.md`](AGENT_GUIDE.md).
- Documented Maintenance & Update Policy requiring version string and `Last Updated: YYYY-MM-DD` timestamp synchronization whenever repository architecture evolves.

### Added / Modified
- `docs/ONTOLOGY.md`: New human-readable ontology guide with Mermaid architecture graph diagrams.
- `docs/GLOSSARY.md`: Added Section 4 (*System Architecture & Metadata*) linking to `docs/ONTOLOGY.md` and `docs/repository_ontology.json`.
- `AGENT_GUIDE.md`: Updated Q3 (*Major Components*) to reference `docs/ONTOLOGY.md`.
- `docs/repository_ontology.json`, `docs/capability_manifest.json`, `schema.org.jsonld`, `README.md`, `pyproject.toml`: Synchronized version `0.0.1.dev13`.

### Breaking Changes
- None.


## [0.0.1.dev12] - 2026-08-28

### Summary of Changes
- Integrated Pre-Code-Generation Prolog Library & Capability Discovery protocol (`prolog-agent discover`, dynamic introspection, static cheat sheets, and Covington header rationale comments).
- Enhanced `prolog-agent module` and project scaffolding to automatically inject library dependency documentation in Covington headers.
- Enforced vendor-neutral open agent guidelines across `.agents/AGENTS.md`, `AGENT_GUIDE.md`, and `CONTRIBUTING.md`, prohibiting proprietary IDE/harness config files (`.claude/`, `.windsurfrule`, `.cursorrules`).
- Added 4-layer architectural blueprint section to `README.md` for applying agent toolkit patterns to other programming languages.
- Documented developer workflow flexibility for lightweight/test-free use cases (interactive REPL top-levels, scratch scripts) in `README.md` and `AGENT_GUIDE.md`.

### Added / Modified
- `prolog_agent_toolkit/discovery.py` & `cli.py`: Enhanced discovery engine, query filtering, and report formatting.
- `prolog_agent_toolkit/project.py`: Updated module header generation with library rationale stubs.
- `.agents/skills/prolog-library-discovery/SKILL.md`: Added Covington header standards and pure ISO fallback examples.
- `.agents/agents/prolog-refactor-agent.md` & `prolog-test-generator-agent.md`: Added mandatory pre-code-generation discovery protocol.
- `README.md`, `AGENT_GUIDE.md`, `CONTRIBUTING.md`, `pyproject.toml`, `schema.org.jsonld`, `docs/capability_manifest.json`, `docs/repository_ontology.json`: Synchronized version `0.0.1.dev12` and added vendor neutrality and workflow flexibility documentation.

### Breaking Changes
- None.


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

