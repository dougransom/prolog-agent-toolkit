---
name: prolog-engine-onboarding
description: Interactive, iterative process for adding support for a new Prolog engine or system (e.g. GNU Prolog, Ciao, ECLiPSe, B-Prolog, Ichiban, YAP) to the toolkit. Asks clarifying questions, generates/edits required files step-by-step, builds safety runners, and updates metadata until the human confirms completion.
---

# Prolog Engine Onboarding Workflow

Use this skill whenever adding a new Prolog engine or dialect target to the toolkit.

The onboarding process is **interactive and iterative**: at each phase, ask clarifying questions to gather exact requirements, create or modify files incrementally, run tests/validations, and seek user feedback before proceeding to the next step until the human programmer explicitly confirms that onboarding is complete.

---

## Phase 1: Information Gathering & Dialect Assessment

Ask the human programmer (or inspect engine documentation/CLI):
1. **Engine Identification**: Full name (e.g., `GNU Prolog`, `Ciao Prolog`), CLI binary name (e.g. `gprolog`, `ciao`), and short slug (e.g. `gprolog`, `ciao`).
2. **Engine Features & String Representation**: Supported standard features and double quote representation (`chars`, `codes`, `atom`, or custom `string`)?
3. **Standard Libraries & Import Directives**: What is the import syntax (`:- use_module(library(...)).` vs `:- use_module(...)` vs auto-loaded)? List key libraries: DCG, CLP, reification, safe type tests, formatting, list utilities.
4. **Package & Build System**: Package manager (`bakage`, `pack`, `npm`, none)?
5. **Testing Framework**: Native test framework (`testing.pl`, `plunit`, `bsl`, custom)?
6. **Safety & Timeout Execution Flags**: Default CLI execution flags (e.g. `--quiet`, `-g`, `--goal`) for batch/script execution under safety runners.

---

## Phase 2: Dialect Standards & Standard Library Cheat Sheet Creation

Create `.agents/skills/<engine-slug>-prolog-standards/SKILL.md`:
1. **Core Guidelines**: Engine guidelines, ISO code generation target rules, string representation, memory limits, and explicit `use_module/1` declarations.
2. **Standard Library Cheat Sheet**:
   - Table containing: Topic/Feature, Import Header (`:- use_module(library(X)).`), Exported Predicates, Dialect Notes.
   - Explicit directive prohibiting AI agents from reading raw OS standard library source files, mandating reliance on the cheat sheet.
3. **Cross-references**: Link to [Portable ISO Prolog Conventions](../prolog-conventions/SKILL.md), [Covington Prolog Style Guide](../../references/covington_style.md), and [Prolog Purity Guidelines](../../references/prolog_guidelines.md).

---

## Phase 3: Safety Runner & CLI Registration

1. **`prolog_agent_toolkit/runner.py`**:
   - Add `<engine-slug>` binary resolution to `RESOLVERS`.
   - Add `<engine-slug>-safe` execution command entry point.
2. **`prolog_agent_toolkit/cli.py`**:
   - Register `<engine-slug>-safe` entry point command function.
3. **`pyproject.toml`**:
   - Register `<engine-slug>-safe = "prolog_agent_toolkit.cli:<engine_slug>_safe"` in `[project.scripts]`.

---

## Phase 4: Initializer & Scaffolding Updates

1. **`prolog_agent_toolkit/initializer.py`**:
   - Add `<engine-slug>` option to `prolog-agent init <name> --dialect <engine-slug>`.
   - Update starter module generator and package manifest defaults (`bakage.toml`, `pack.pl`, `package.json`, etc.).
2. **`templates/starter_project/`**:
   - Ensure scaffolding works cleanly for the new engine.

---

## Phase 5: Repository Metadata & Agent Documentation

Update metadata across the entire toolkit:
1. **`.agents/AGENTS.md`**:
   - Register the new dialect under **Multi-Engine Dialect Selection & Rules**.
   - Add reference under **Future Engine Expansion & Metadata Protocol**.
2. **`README.md`**:
   - Update features list, CLI command table (`<engine-slug>-safe`), installation prerequisites, and compatibility tables.
   - Update OpenGraph description and Schema.org JSON-LD snippet.
3. **`codemeta.json`**:
   - Update description and `keywords` list.

---

## Phase 6: Automated Verification & Iterative Review

1. **Run Unit Tests**:
   - Execute `PYTHONDONTWRITEBYTECODE=1 uv run pytest`.
2. **Validate Skills**:
   - Execute `PYTHONDONTWRITEBYTECODE=1 uv run prolog-agent validate-skills`.
3. **Human Confirmation & Checkpoint**:
   - Summarize all changes made across files.
   - Ask the human programmer: *"Are there any additional dialect rules, standard libraries, or safety runner flags needed for `<engine>`, or are we finished?"*
   - Continue iterating on any requested additions until the human explicitly confirms completion.
