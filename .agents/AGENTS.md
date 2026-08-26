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
- **Programmer Steering Guidelines**: [.agents/references/programmer_guidelines.md](.agents/references/programmer_guidelines.md)
  - Best practices for human programmers when prompting, constraining, and steering AI coding assistants.

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

## Future Engine Expansion & Metadata Protocol

Whenever a new Prolog engine or system is added or supported in this toolkit, all AI assistants MUST systematically update:
1. **Metadata & Web Annotations**:
   - `README.md`: Update OpenGraph description (`<meta property="og:description">`), Schema.org snippet (`<script type="application/ld+json">`), keywords, features list, and engine support tables.
   - `schema.org.jsonld`: Update `description` and `keywords` array.
   - `pyproject.toml`: Add engine tag to `keywords` and CLI entry point script.
2. **Coding Standards & Dialects**:
   - Create `.agents/skills/<engine>-prolog-standards/SKILL.md` detailing ISO/engine compliance rules.
   - Register dialect skill under **Multi-Engine Dialect Selection & Rules** in `.agents/AGENTS.md`.
3. **Packaging & Dependencies**:
   - Update `.agents/skills/prolog-packaging/SKILL.md` to cover package management for the engine (e.g. `bakage`, `pack`, `npm`).
4. **Testing Frameworks**:
   - Update `.agents/skills/prolog-testing/SKILL.md` to cover test assertions, runners, and CLI invocation commands.
5. **Safety Runners & CLI**:
   - Update `prolog_agent_toolkit/runner.py` and `prolog_agent_toolkit/cli.py` to support binary resolution and safety wrapper entry point `<engine>-safe`.

