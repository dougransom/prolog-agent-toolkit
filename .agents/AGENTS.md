# Prolog Agent Toolkit Guidelines & Standards

> **System Authority**: This document is the source of truth for all coding, architectural, and procedural standards within the Prolog Agent Toolkit.
> **Cross-Reference Index**:
> - [Onboarding Blueprint](AGENT_GUIDE.md) | [Directory Map](AGENT_INDEX.json)
> - [Component Ontology](docs/repository_ontology.json) | [Glossary](docs/GLOSSARY.md) | [Anti-Patterns](docs/ANTI_PATTERNS.md)

When writing, refactoring, reviewing, or running Prolog code across any project or Prolog engine, all AI assistants ([Google Antigravity](https://antigravity.google), [Claude Code](https://docs.anthropic.com/en/docs/agents-and-tools/claude-code/overview), [Cursor](https://www.cursor.com/), [Windsurf](https://codeium.com/windsurf), [GitHub Copilot](https://github.com/features/copilot), [`aidermacs`](https://github.com/MatthewZMD/aidermacs)/[`agent-shell`](https://github.com/xenodium/agent-shell)/[`gptel`](https://github.com/karthink/gptel) in [Emacs](https://www.gnu.org/software/emacs/)) MUST adhere to the standards defined below.


## Universal Prolog Style & Purity Guidelines

All Prolog code (regardless of target engine) MUST follow the universal style and purity principles:

- **Vendor Neutrality & Open Standards**:
  - All AI agent guidelines, instructions, rules, and skills MUST remain 100% vendor-neutral and open format (`AGENTS.md`, `.agents/skills/<name>/SKILL.md`, `.agents/agents/<name>.md`).
  - Do NOT create proprietary, vendor-specific, or IDE-harness-specific configuration files or directories (such as `.claude/`, `.windsurfrule`, `.cursorrules`, `.github/copilot-instructions.md`, `.clinerules`, `.gemini/`, or harness-specific Emacs configs).
- **Covington Prolog Style Guide**: [.agents/references/covington_style.md](.agents/references/covington_style.md)
  - Write for humans first; keep clauses simple and readable; use explicit goal ordering and clean predicate naming.
- **Purity Guidelines**: [.agents/references/prolog_guidelines.md](.agents/references/prolog_guidelines.md)
  - Prefer logical purity (`if_/3`, `dif/2`, pure DCGs); prefer `dif/2` over negation-as-failure `\+/1` for sound term inequality; avoid unnecessary cuts (`!`) and side effects.
  - Prefer **clean vs. defaulty data representations** where element kinds are distinguished by principal functors (e.g. `leaf(L)` vs `node(L, R)`).
  - Prefer higher-order constructs (`call/N`, `call//N`, `maplist/N`, `foldl/N`) and [`library(lambda)`](https://github.com/mthom/scryer-prolog/blob/master/src/lib/lambda.pl) (`\X^...`, `\X^Y^Goal`) to avoid duplicating predicate structures or DCG traversals.
  - Prefer pure efficiency: first-argument indexing, reified `zcompare/3` arithmetic comparison, and early constraint pruning (`dif/2`, [`CLP(Z)`](https://github.com/mthom/scryer-prolog/blob/master/src/lib/clpz.pl)).
  - Prefer coroutining (`freeze/2`, `when/2`) to suspend goals until variables are instantiated, preferring [`CLP(Z)`](https://github.com/mthom/scryer-prolog/blob/master/src/lib/clpz.pl)/`dif/2` over manual coroutining where specialized constraints apply.
  - When relating conditions to values, isolate the test-value relation (e.g. `if_(G, A="A", A="B"), write(A)`).
- **Declarative AI Workflow**: [.agents/skills/prolog-declarative-workflow/SKILL.md](.agents/skills/prolog-declarative-workflow/SKILL.md)
  - Use declarative reasoning based on unification, constraints, and backtracking (never imperative thinking).
  - Specify mode (`+`/`-`), determinism (`det`, `semidet`, `nondet`), and choice-point expectations.
  - Use test-first scaffolding (`testing.pl` / `plunit` / configured test framework) and DCG structure generation.
- **Programmer Steering Guidelines**: [.agents/references/programmer_guidelines.md](.agents/references/programmer_guidelines.md)
  - Best practices for human programmers when prompting, constraining, and steering AI coding assistants.
- **Pre-Code-Generation Library Discovery Policy**: [.agents/skills/prolog-library-discovery/SKILL.md](.agents/skills/prolog-library-discovery/SKILL.md)
  - BEFORE generating Prolog code, AI assistants MUST execute the 7-step discovery protocol: (1) Identify target engine; (2) Run `prolog-agent discover --engine <engine>` or inspect dialect cheat sheets / manifests; (3) Prefer discovered built-in libraries and installed packs over writing custom logic from scratch; (4) Explicitly declare `:- use_module(library(...)).` headers; (5) Document selected dependencies in headers; (6) Explain dependency selection rationale; (7) Only implement custom code when no suitable library exists.
- **Standard Library Cheat-Sheet Steering**:
  - AI assistants MUST use dialect skill cheat sheets for `:- use_module(library(...)).` declarations and predicate signatures instead of assuming SWI-style autoloading.
  - AI assistants MUST NOT read raw standard library implementation source files, relying on concise cheat sheets and pre-trained semantics to conserve context window tokens.
- **Human Editing Syntax Error Diagnostics**:
  - Whenever Prolog compilation or consult fails after human editing, AI assistants MUST scan target source files for common punctuation typos (`:` instead of `:-`, `->` instead of `-->`, `#` or `//` line comments, `!=`, `<=`, `=>`, `<>`), and report exact file, line number, column, and fix recommendations to the programmer.

## Multi-Engine Dialect Selection & Rules

AI assistants MUST select and follow the specific dialect standards corresponding to the target Prolog engine:

- **ISO [Scryer Prolog](https://github.com/mthom/scryer-prolog)**: [.agents/skills/scryer-prolog-standards/SKILL.md](.agents/skills/scryer-prolog-standards/SKILL.md)
  - Pure DCGs, [`library(si)`](https://github.com/mthom/scryer-prolog/blob/master/src/lib/si.pl), `chars` strings, `dif/2`, `if_/3` from [`library(reif)`](https://github.com/mthom/scryer-prolog/blob/master/src/lib/reif.pl).
- **[SWI-Prolog](https://www.swi-prolog.org/)**: [.agents/skills/swi-prolog-standards/SKILL.md](.agents/skills/swi-prolog-standards/SKILL.md)
  - SWI dicts, SWI string types, module declarations, pack manager.
- **[Trealla Prolog](https://github.com/trealla-prolog/trealla)**: [.agents/skills/trealla-prolog-standards/SKILL.md](.agents/skills/trealla-prolog-standards/SKILL.md)
  - ISO compliance, WASM embedding, fast standard library parsing.
- **[Tau Prolog](http://tau-prolog.org/)**: [.agents/skills/tau-prolog-standards/SKILL.md](.agents/skills/tau-prolog-standards/SKILL.md)
  - ISO compliance, JavaScript/Browser DOM integration, `library(dom)`, `library(js)`.
- **Portable ISO Prolog Conventions**: [.agents/skills/prolog-conventions/SKILL.md](.agents/skills/prolog-conventions/SKILL.md)
  - Engine-agnostic ISO standard code compatible across all conforming implementations.
- **Prolog Testing**: [.agents/skills/prolog-testing/SKILL.md](.agents/skills/prolog-testing/SKILL.md)
  - Scryer `testing.pl` (default), SWI `plunit`, and portable ISO assertions.
- **Prolog Packaging**: [.agents/skills/prolog-packaging/SKILL.md](.agents/skills/prolog-packaging/SKILL.md)
  - Scryer `bakage` manifests (default) and SWI `pack` manager.
- **Prolog Release & Versioning**: [.agents/skills/prolog-release/SKILL.md](.agents/skills/prolog-release/SKILL.md)
  - Multi-file version synchronization (`pack.pl`, `pyproject.toml`, `README.md`), Git tagging, and post-release prompts.
- **CLP Constraints**: [.agents/skills/prolog-clp-constraints/SKILL.md](.agents/skills/prolog-clp-constraints/SKILL.md)
  - Combinatorial optimization, scheduling, integer constraints (`library(clpz)`, `library(clpfd)`), labeling strategies, and reification.
- **DCG Mastery**: [.agents/skills/prolog-dcg-mastery/SKILL.md](.agents/skills/prolog-dcg-mastery/SKILL.md)
  - Definite Clause Grammars, AST constructors, tokenizer passes, pushback lookahead without cuts, and sequence serializers.
- **Prolog Tabling**: [.agents/skills/prolog-tabling/SKILL.md](.agents/skills/prolog-tabling/SKILL.md)
  - Memoization, SLG resolution, cyclic graph reachability, Datalog queries, and mode-directed tabling.
- **Linter & Static Analysis**: [.agents/skills/prolog-linter-static-analysis/SKILL.md](.agents/skills/prolog-linter-static-analysis/SKILL.md)
  - Detection of singleton variables, discontiguous clauses, non-terminating recursion, and non-logical cuts via safety runners.
- **Performance & Profiling**: [.agents/skills/prolog-performance-profiling/SKILL.md](.agents/skills/prolog-performance-profiling/SKILL.md)
  - Choicepoint audits, first-argument indexing optimization, tail-recursion accumulators, and pure reified logic (`library(reif)`).
- **Debugging Workflow**: [.agents/skills/prolog-debugging-workflow/SKILL.md](.agents/skills/prolog-debugging-workflow/SKILL.md)
  - 4-port model debugging (`trace`, `spy`, `gtrace`), step-by-step goal execution, and residual constraint inspection.
- **FFI & WASM Embedding**: [.agents/skills/prolog-ffi-wasm-embedding/SKILL.md](.agents/skills/prolog-ffi-wasm-embedding/SKILL.md)
  - Interfacing Prolog with C, Rust, Python (`janus-swi`), JavaScript, and WebAssembly targets.
- **Web Services & HTTP**: [.agents/skills/prolog-web-services/SKILL.md](.agents/skills/prolog-web-services/SKILL.md)
  - Microservices, REST APIs, JSON endpoints, and WebSockets in Prolog.
- **Neurosymbolic AI**: [.agents/skills/prolog-neurosymbolic-agent/SKILL.md](.agents/skills/prolog-neurosymbolic-agent/SKILL.md)
  - LLM + Prolog integration architecture: LLM for translation & heuristics, Prolog for ground-truth logic verification.
- **Code Review**: [.agents/skills/prolog-code-review/SKILL.md](.agents/skills/prolog-code-review/SKILL.md)
  - Guidelines and checklists for auditing Prolog PRs, checking logical purity, determinism, portability, and safety.
- **Engine Onboarding**: [.agents/skills/prolog-engine-onboarding/SKILL.md](.agents/skills/prolog-engine-onboarding/SKILL.md)
  - Interactive, iterative workflow for onboarding new Prolog engines and dialect targets into the toolkit.

## Autonomous Agent Subagents (`.agents/agents/`)

The toolkit provides dedicated subagents for automated agentic workflows:
- **Refactoring Agent**: [.agents/agents/prolog-refactor-agent.md](.agents/agents/prolog-refactor-agent.md) — Converts imperative Prolog to pure ISO Prolog (`if_/3`, `dif/2`, pure DCGs).
- **Test Generator Agent**: [.agents/agents/prolog-test-generator-agent.md](.agents/agents/prolog-test-generator-agent.md) — Automates unit test suite creation across `testing.pl` and `plunit`.
- **Benchmark Runner Agent**: [.agents/agents/prolog-benchmark-runner-agent.md](.agents/agents/prolog-benchmark-runner-agent.md) — Multi-engine performance and determinism comparisons.
- **Doc Generator Agent**: [.agents/agents/prolog-doc-generator-agent.md](.agents/agents/prolog-doc-generator-agent.md) — Extracts Covington comments and generates Markdown API references.
- **PR Reviewer Agent**: [.agents/agents/prolog-pr-reviewer-agent.md](.agents/agents/prolog-pr-reviewer-agent.md) — Automated Pull Request auditor, static analysis & test runner.
- **Purity Reviewer Agent**: [.agents/agents/prolog-purity-reviewer-agent.md](.agents/agents/prolog-purity-reviewer-agent.md) — Logical purity, reification, and Covington style auditor.
- **Portability Reviewer Agent**: [.agents/agents/prolog-portability-reviewer-agent.md](.agents/agents/prolog-portability-reviewer-agent.md) — Multi-engine compatibility auditor across Scryer, SWI, Trealla, Tau, and ISO.
- **Security Reviewer Agent**: [.agents/agents/prolog-security-reviewer-agent.md](.agents/agents/prolog-security-reviewer-agent.md) — Code injection, search bounds, and dynamic database safety auditor.

## Project Bootstrapping & Initializer Workflow

AI assistants provide the virtual and CLI commands:
- `prolog-agent init <project-name> [--dialect scryer|swi|trealla]`
- `prolog-agent template <project-name> [--dialect scryer|swi|trealla]`
- `prolog-agent module <module-name> [--dialect scryer|swi|trealla]`
- `prolog-agent init-script`

When a user requests a new project or starts a new Prolog repository, AI assistants MUST execute or guide the initializer workflow:
1. **Directory Structure**: Create `<project-name>/`, containing `src/`, `tests/`, `README.md`, `CHANGELOG.md`, and `.agents/` (symlink or copy instructions).
2. **Package Manifest**:
   - **Scryer / ISO**: Create `bakage.toml` (`name`, `version = "0.1.0"`, `modules = ["src/<project-name>.pl"]`, `requires`) and `pack.pl`.
   - **SWI-Prolog**: Create `pack.pl` manifest (`name('<project-name>')`, `version('0.1.0')`, `title`, `author`).
   - **Trealla Prolog**: No manifest created (no package manager).
   - **Tau Prolog**: Create `package.json` (`name`, `version`, `tau-prolog` dependency).
3. **Starter Module**: Create `src/<project-name>.pl` with module declaration, Covington comment block, sample pure predicate, DCG stub, and CLP(Z) stub.
4. **Testing Scaffolding**: Create `tests/testing.pl` (Scryer/ISO/Trealla) or `tests/test_<project-name>.pl` (`plunit` for SWI).
5. **Dialect Standards**: Include relevant dialect skills (`scryer-prolog-standards`, `swi-prolog-standards`, `trealla-prolog-standards`, `prolog-conventions`, `prolog-initializer`).
6. **README.md**: Include instructions for running tests, using safe runners (`prolog-safe`, `scryer-safe`, `swi-safe`), linking agent skills, and dialect notes.


## Safety & Cross-Platform Execution

- **CLI Entry Points**: ALL Prolog code executions MUST use the cross-platform CLI safety entry points (`prolog-agent`, `prolog-safe`, `scryer-safe`, `swi-safe`, `trealla-safe`, `tau-safe`).
- **Forbidden Invocations**: AI assistants MUST NEVER execute raw interpreter binaries ([`scryer-prolog`](https://github.com/mthom/scryer-prolog), [`swipl`](https://www.swi-prolog.org/), [`tpl`](https://github.com/trealla-prolog/trealla), [`tau-prolog`](http://tau-prolog.org/), [`gprolog`](http://gprolog.org/), [`ciao`](https://ciao-lang.org/)) directly.
- **Specifying Engine**: Set `PROLOG_ENGINE` environment variable (e.g., `export PROLOG_ENGINE=scryer`, `export PROLOG_ENGINE=swi`, `export PROLOG_ENGINE=trealla`, `export PROLOG_ENGINE=tau`).
- **Python Invocation & Clean Workspace**:
  - Python tools, test runners, and CLI invocations MUST NOT leave intermediate bytecode or cache artifacts (`__pycache__`, `.pyc`, `.pytest_cache`) in source or test directories.
  - Python MUST be invoked with bytecode generation disabled (`PYTHONDONTWRITEBYTECODE=1` or `python -B`), or redirected to a central cache directory (`PYTHONPYCACHEPREFIX=.cache/pycache`).
  - Example command: `PYTHONDONTWRITEBYTECODE=1 uv run pytest` or `PYTHONDONTWRITEBYTECODE=1 uv run <script>`.

## Release & Versioning Workflow (`prolog-agent release`)

AI assistants provide the virtual and CLI command: `prolog-agent release [--version X.Y.Z]`.

### Canonical Version Source of Truth & Rules:
1. **Canonical Version**: `pyproject.toml` is the single canonical source of truth for the release version (which may include development tags such as `X.Y.Z.devN` or `vX.Y.Z`).
2. **Runtime Python Resolution**: Python files MUST resolve the package version dynamically at runtime via `importlib.metadata.version("prolog-agent-toolkit")`.
3. **Multi-File Synchronization**: Non-Python manifest/doc files (`bakage.toml`, `pack.pl`, `package.json`, `README.md`, `CHANGELOG.md`) MUST be updated by the agent whenever the `pyproject.toml` version changes or when running `prolog-agent release`.
4. **Git Tag Matching**: The Git tag created during release MUST exactly match the version string in `pyproject.toml` (e.g. `v0.0.1` or `v0.0.1.dev3`).

### Release Execution Steps:
1. **Synchronize Versions**: Run `prolog-agent release [--version X.Y.Z]`.
2. **Verify Version Parity**: Run `prolog-agent check-version` (or use `prolog-agent install-hooks` for pre-commit enforcement).
3. **Generate CHANGELOG.md**: Update `CHANGELOG.md` with release version header (`## [X.Y.Z] - YYYY-MM-DD`).
4. **Commit & Tag**: Commit changes (`git commit -am "Release vX.Y.Z"`) and tag with exact `pyproject.toml` version (`git tag -a vX.Y.Z -m "Release vX.Y.Z"`).
5. **Push**: Push commits and tags (`git push origin <branch> --tags`).

## Future Engine Expansion & Metadata Protocol

Whenever a new Prolog engine or system is added or supported in this toolkit, all AI assistants MUST follow the interactive workflow in [.agents/skills/prolog-engine-onboarding/SKILL.md](.agents/skills/prolog-engine-onboarding/SKILL.md) and systematically update:
1. **Metadata & Web Annotations**:
   - `README.md`: Update OpenGraph description (`<meta property="og:description">`), Schema.org snippet (`<script type="application/ld+json">`), keywords, features list, and engine support tables.
   - `schema.org.jsonld`: Update `description` and `keywords` array.
   - `pyproject.toml`: Add engine tag to `keywords` and CLI entry point script.
2. **Coding Standards & Dialect Cheat Sheets**:
   - Create `.agents/skills/<engine>-prolog-standards/SKILL.md` detailing ISO/engine compliance rules AND including a comprehensive **Standard Library Cheat Sheet** (import headers, exported predicates, and dialect autoload differences).
   - Register dialect skill under **Multi-Engine Dialect Selection & Rules** in `.agents/AGENTS.md`.
3. **Packaging & Dependencies**:
   - Update `.agents/skills/prolog-packaging/SKILL.md` to cover package management for the engine (e.g. `bakage`, `pack`, `npm`).
4. **Testing Frameworks**:
   - Update `.agents/skills/prolog-testing/SKILL.md` to cover test assertions, runners, and CLI invocation commands.
5. **Safety Runners & CLI**:
   - Update `prolog_agent_toolkit/runner.py` and `prolog_agent_toolkit/cli.py` to support binary resolution and safety wrapper entry point `<engine>-safe`.

