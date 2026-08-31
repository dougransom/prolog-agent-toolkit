# Prolog Agent Toolkit Guidelines & Standards

> **System Authority**: This document is the source of truth for all coding, architectural, and procedural standards within the Prolog Agent Toolkit.
> **Cross-Reference Index**:
> - [Onboarding Blueprint](AGENT_GUIDE.md) | [Directory Map](AGENT_INDEX.json)
> - [Component Ontology](docs/repository_ontology.json) | [Glossary](docs/GLOSSARY.md) | [Anti-Patterns](docs/ANTI_PATTERNS.md)

When writing, refactoring, reviewing, or running Prolog code across any project or Prolog engine, all AI assistants ([Google Antigravity](https://antigravity.google), [Claude Code](https://docs.anthropic.com/en/docs/agents-and-tools/claude-code/overview), [Cursor](https://www.cursor.com/), [Windsurf](https://codeium.com/windsurf), [GitHub Copilot](https://github.com/features/copilot), [`aidermacs`](https://github.com/MatthewZMD/aidermacs)/[`agent-shell`](https://github.com/xenodium/agent-shell)/[`gptel`](https://github.com/karthink/gptel) in [Emacs](https://www.gnu.org/software/emacs/)) MUST adhere to the standards defined below.


## Universal Prolog Style & Purity Guidelines

All Prolog code (regardless of target engine) MUST follow the universal style and purity principles:

- **ISO Prolog Code Generation Goal & Engine Neutrality**:
  - AI assistants MUST attempt to produce ISO-compliant code (standard ISO/IEC 13211-1) subject to the capabilities and limitations of the target Prolog system being used.
  - AI assistants MUST NOT describe or claim that any Prolog system (e.g. Scryer, SWI, Trealla, Tau, GNU, Ciao) is "ISO compliant" or an "ISO Prolog system". Systems may make their own compliance claims.
- **Vendor Neutrality & Open Standards**:
  - All AI agent guidelines, instructions, rules, and skills MUST remain 100% vendor-neutral and open format (`AGENTS.md`, `.agents/skills/<name>/SKILL.md`, `.agents/agents/<name>.md`).
  - Do NOT create proprietary, vendor-specific, or IDE-harness-specific configuration files or directories (such as `.claude/`, `.windsurfrule`, `.cursorrules`, `.github/copilot-instructions.md`, `.clinerules`, `.gemini/`, or harness-specific Emacs configs).
- **Generalized Common Baseline & Engine Idiosyncrasies**:
  - The core goal of this toolkit is to declare as much as possible as a **generalized, common Prolog standard** applicable across all Prolog systems (pure logic, reification `=(X,Y,Truth)`/`cond_t`, `CLP(Z)`/`CLP(FD)` constraints, pure DCGs, `chars`, safe type testing `library(si)`, Covington layout, and efficiency).
  - System-specific skill guidelines (`scryer-prolog-standards`, `swi-prolog-standards`, `trealla-prolog-standards`, `tau-prolog-standards`) MUST capture only what is **idiosyncratic or engine-specific** (module load headers, system types like SWI dicts, WASM limits, packaging, DOM interop), while delegating all common style, purity, and usage rules to the central generalized baseline.
- **Canonical Common Coding Standards**: [.agents/skills/prolog-conventions/SKILL.md](.agents/skills/prolog-conventions/SKILL.md)
  - All common Prolog coding guidelines, purity rules, reification patterns, DCG conventions, variable naming, safe type testing, and syntax diagnostics are operationally defined in `prolog-conventions`. AI agents MUST activate `prolog-conventions` whenever generating, refactoring, or auditing Prolog code.
  - **Code Review Skill Synchronization Policy**: Whenever core coding guidelines or system rules are updated, AI assistants MUST prompt the programmer to update the Code Review skill ([`prolog-code-review`](.agents/skills/prolog-code-review/SKILL.md)) to keep review checklists aligned with operational coding standards.
- **Covington Prolog Style Guide**: [.agents/references/covington_style.md](.agents/references/covington_style.md)
  - Write for humans first; keep clauses simple and readable; use explicit goal ordering and clean predicate naming.
- **Purity Guidelines**: [.agents/references/prolog_guidelines.md](.agents/references/prolog_guidelines.md)
  - Prefer logical purity (`if_/3`, `dif/2`, pure DCGs); prefer `dif/2` over negation-as-failure `\+/1` for sound term inequality.
  - **Avoid `!`, `\+/1`, `->` for Performance**: NEVER introduce cuts (`!`), negation-as-failure (`\+/1`), or soft cuts (`->`) merely for performance reasons.
  - **Mandatory Comment Justifications for Correctness**: If cuts (`!`), `\+/1`, or `->` must be introduced for *correctness* when pure logic constructs (`if_/3`, `dif/2`) cannot achieve the required behavior, write an explicit comment in the code explaining why pure constructs were insufficient.
  - Prefer **clean vs. defaulty data representations** where element kinds are distinguished by principal functors (e.g. `leaf(L)` vs `node(L, R)`).
  - Prefer higher-order constructs (`call/N`, `call//N`, `maplist/N`, `foldl/N`) and [`library(lambda)`](https://github.com/mthom/scryer-prolog/blob/master/src/lib/lambda.pl) (`\X^...`, `\X^Y^Goal`) to avoid duplicating predicate structures or DCG traversals.
  - **ISO DCG Indicator Convention (`Name//Arity`)**: Always use `Name//Arity` notation (e.g. `parse_item//1`) for DCG non-terminals in module export lists (`:- module(M, [rule//N]).`), import lists (`:- use_module(M, [rule//N]).`), Covington doc headers (`%% rule//N`), and predicate identification.
  - **Variable & Indicator Naming Guidelines**:
    - **Prefer Meaningful Variable Names**: Use domain-descriptive names (`Tree`, `TokenStream`, `Result`, `Acc`) for public predicate parameters and non-trivial clauses, avoiding arbitrary placeholders like `Arg1` or `P2`.
    - **Idiomatic Short Names in Local Contexts**: Short, standard variable names (`X`, `Y`, `Xs`, `Ys`, `N`) are encouraged in tight list traversals, mathematical constraints, and local higher-order closures.
    - **Clear Names for Dual-Mode & Polymorphic Predicates**: When a predicate accepts dual calling modes (e.g., direct lists vs. DCG difference-lists), use parameter names that clarify both roles (e.g., `InputOrMatch`, `RestOrState`).
    - **Consistent DCG Threading Pairs**: Use standard conventions for threaded state pairs, such as `L0, L1, ..., L` for character streams and `S0, S1, ..., S` for general state accumulators.
  - Prefer pure efficiency: first-argument indexing, reified `zcompare/3` arithmetic comparison, and early constraint pruning (`dif/2`, [`CLP(Z)`](https://github.com/mthom/scryer-prolog/blob/master/src/lib/clpz.pl)).
  - Prefer coroutining (`freeze/2`, `when/2`) to suspend goals until variables are instantiated, preferring [`CLP(Z)`](https://github.com/mthom/scryer-prolog/blob/master/src/lib/clpz.pl)/`dif/2` over manual coroutining where specialized constraints apply.
  - **Direct Reification over `if_/3` for Booleans**: Always prefer direct reified predicates (e.g. `=(X, Y, Truth)`, `memberd_t/3`, `tpartition/4`) over wrapping boolean assignments inside `if_/3` (e.g. use `=(X, Y, Truth)` instead of `if_(X = Y, Truth = true, Truth = false)`). Reserve `if_/3` strictly for selecting non-boolean values (`if_(G, Val = 'yes', Val = 'no')`) or executing conditional branches with distinct control paths.
  - **Prefer `cond_t` over `if_` / `->` (DRY Principle)**: Aggressively prefer `cond_t` over `if_` and `->` when choosing between choices or values based on a test. Use `cond_t` to avoid repeating the same variable or assignment in both the true and false clauses of `if_` (Don't Repeat Yourself principle).
  - **Meta-Predicate Declarations (`meta_predicate`)**: When defining module-level predicates that accept callable goals (`0`), closures (`1`..`N`), DCG non-terminals (`//` or `2`), or module-sensitive terms (`:`), always insert explicit `:- meta_predicate` declarations directly below the module header. Use exact closure arities for higher-order arguments and standard specifiers (`+`, `-`, `?`, `*`) for non-callable data arguments to prevent unwanted caller module expansion.
- **Declarative AI Workflow**: [.agents/skills/prolog-declarative-workflow/SKILL.md](.agents/skills/prolog-declarative-workflow/SKILL.md)
  - Use declarative reasoning based on unification, constraints, and backtracking (never imperative thinking).
  - Specify mode (`+`/`-`), determinism (`det`, `semidet`, `nondet`), and choice-point expectations.
  - Use test-first scaffolding (`testing.pl` / `plunit` / configured test framework) and DCG structure generation.
- **Programmer Steering Guidelines**: [.agents/references/programmer_guidelines.md](.agents/references/programmer_guidelines.md)
  - Best practices for human programmers when prompting, constraining, and steering AI coding assistants.
- **Pre-Code-Generation Library Discovery Policy**: [.agents/skills/prolog-library-discovery/SKILL.md](.agents/skills/prolog-library-discovery/SKILL.md)
  - BEFORE generating Prolog code, AI assistants MUST execute the 7-step discovery protocol: (1) Identify target engine; (2) Run `prolog-agent discover --engine <engine>` or inspect system cheat sheets / manifests; (3) Prefer discovered built-in libraries and installed packs over writing custom logic from scratch; (4) Explicitly declare `:- use_module(library(...)).` headers; (5) Document selected dependencies in headers; (6) Explain dependency selection rationale; (7) Only implement custom code when no suitable library exists.
- **Standard Library Cheat-Sheet Steering**:
  - AI assistants MUST use system skill cheat sheets for `:- use_module(library(...)).` declarations and predicate signatures instead of assuming SWI-style autoloading.
  - AI assistants MUST NOT read raw standard library implementation source files, relying on concise cheat sheets and pre-trained semantics to conserve context window tokens.
- **Human Editing Syntax Error Diagnostics**:
  - Whenever Prolog compilation or consult fails after human editing, AI assistants MUST scan target source files for common punctuation typos (`:` instead of `:-`, `->` instead of `-->`, `#` or `//` line comments, `!=`, `<=`, `=>`, `<>`), and report exact file, line number, column, and fix recommendations to the programmer.
- **Portable Hyperlinks Policy**:
  - Avoid absolute `file://` hyperlinks on the local filesystem that break on other machines or on GitHub.
  - When encountering or adding local file links, use portable relative Markdown links (e.g. `[AGENT_GUIDE.md](AGENT_GUIDE.md)` instead of `file:///path/to/AGENT_GUIDE.md`).
  - If a `file://` link was provided by a human programmer (rather than an AI code agent), ask the programmer if they want to fix it first before replacing it.
- **Custom Style Overrides & Programmer Preference Precedence**:
  - Whenever a human programmer provides explicit code generation examples, AST term constructors, mode/determinism contracts, or custom style rules (in prompt text, workspace rules `.agents/AGENTS.md` / `.agents/rules/`, or custom project skills `.agents/skills/`), AI assistants MUST prioritize the programmer's explicit instructions and reference examples over toolkit default choices.
  - Precedence order: (1) In-prompt instructions & AST constructors; (2) Workspace rules & custom skills (`.agents/`); (3) Global user rules (`~/.gemini/config/`); (4) Toolkit defaults & built-in skills.
- **Homoiconicity & Skill Invocation**: Prolog is homoiconic — terms ARE the program. The agent toolkit leverages this so that skills, capabilities, and invocations are represented as Prolog terms/facts, making them simultaneously documentation, data, and executable code.
  - **Concrete skill registry format**: Declare skill capabilities as two-argument facts `skill(SkillName, Capabilities)` where `SkillName` is an atom and `Capabilities` is a list of capability atoms:
    ```prolog
    skill(prolog_conventions,   [purity, dcg, clp, type_testing, strings]).
    skill(prolog_code_review,   [purity, determinism, portability, safety, testing]).
    skill(prolog_clp_constraints, [clp, scheduling, optimization, labeling]).
    skill(scryer_prolog_standards, [scryer, modules, reif, si, chars]).
    ```
  - **Discovery via queries**: Because skills are Prolog facts, capability lookup becomes a standard Prolog query — no string matching or external config parsing required:
    ```prolog
    % Find all skills relevant to DCG work:
    ?- skill(Name, Caps), member(dcg, Caps).
    ```
  - **Composition via `call/N`**: Skill dispatch and composition can use `call/N`, `functor/3`, and `=..` — the same mechanisms used for any Prolog goal — making skill orchestration a first-class Prolog program rather than a harness side-channel.
  - **Tooling consistency**: Programs in the toolkit that process or generate Prolog source SHOULD be written in Prolog itself (ISO core + flat engine shims), consistent with the homoiconicity principle. See Guideline 16 in [prolog-conventions](.agents/skills/prolog-conventions/SKILL.md).


## Multi-Engine Prolog System Selection & Rules

AI assistants MUST select and follow the specific system standards corresponding to the target Prolog system / engine:

- **[Scryer Prolog](https://github.com/mthom/scryer-prolog)**: [.agents/skills/scryer-prolog-standards/SKILL.md](.agents/skills/scryer-prolog-standards/SKILL.md)
  - Pure DCGs, [`library(si)`](https://github.com/mthom/scryer-prolog/blob/master/src/lib/si.pl), `chars` strings, `dif/2`, `if_/3` from [`library(reif)`](https://github.com/mthom/scryer-prolog/blob/master/src/lib/reif.pl).
- **[SWI-Prolog](https://www.swi-prolog.org/)**: [.agents/skills/swi-prolog-standards/SKILL.md](.agents/skills/swi-prolog-standards/SKILL.md)
  - SWI dicts, SWI string types, module declarations, pack manager.
- **[Trealla Prolog](https://github.com/trealla-prolog/trealla)**: [.agents/skills/trealla-prolog-standards/SKILL.md](.agents/skills/trealla-prolog-standards/SKILL.md)
  - WASM embedding, fast standard library parsing.
- **[Tau Prolog](http://tau-prolog.org/)**: [.agents/skills/tau-prolog-standards/SKILL.md](.agents/skills/tau-prolog-standards/SKILL.md)
  - JavaScript/Browser DOM integration, `library(dom)`, `library(js)`.
- **Portable ISO Prolog Conventions**: [.agents/skills/prolog-conventions/SKILL.md](.agents/skills/prolog-conventions/SKILL.md)
  - Guidelines for aiming for standard ISO-compliant Prolog code across engines subject to target engine limitations.
- **Prolog Testing**: [.agents/skills/prolog-testing/SKILL.md](.agents/skills/prolog-testing/SKILL.md)
  - Scryer `testing.pl` (default), SWI `plunit`, and portable assertions.
- **Prolog Packaging**: [.agents/skills/prolog-packaging/SKILL.md](.agents/skills/prolog-packaging/SKILL.md)
  - Scryer `bakage` manifests (default), SWI `pack` manager, `npm` for Tau, and optional `make packages` Makefile recipes.
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
  - Interactive, iterative workflow for onboarding new Prolog engines and system targets into the toolkit.
- **Project Migration**: [.agents/skills/prolog-migrate-project/SKILL.md](.agents/skills/prolog-migrate-project/SKILL.md)
  - Migration workflow for upgrading legacy Prolog codebases to toolkit conventions in a safe Git branch/worktree.

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
- `prolog-agent init <project-name> [--system scryer|swi|trealla]`
- `prolog-agent template <project-name> [--system scryer|swi|trealla]`
- `prolog-agent module <module-name> [--system scryer|swi|trealla]`
- `prolog-agent init-script`

When a user requests a new project or starts a new Prolog repository, AI assistants MUST execute or guide the initializer workflow:
1. **Directory Structure**: Create `<project-name>/`, containing `src/`, `tests/`, `README.md`, `CHANGELOG.md`, and `.agents/` (recommending Git Submodule integration `git submodule add ... .agents-toolkit` or symlink).
2. **Package Manifest**:
   - **Scryer / ISO**: Create `scryer-manifest.pl` (`name("pkg")`, `version("0.1.0")`, `main_file("src/<project-name>.pl")`, `dependencies([])`) and `pack.pl`.
   - **SWI-Prolog**: Create `pack.pl` manifest (`name('<project-name>')`, `version('0.1.0')`, `title`, `author`).
   - **Trealla Prolog**: No manifest created (no package manager).
   - **Tau Prolog**: Create `package.json` (`name`, `version`, `tau-prolog` dependency).
3. **Starter Module**: Create `src/<project-name>.pl` with module declaration, Covington comment block, sample pure predicate, DCG stub, and CLP(Z) stub.
4. **Testing Scaffolding**: Create `tests/testing.pl` (Scryer/ISO/Trealla) or `tests/test_<project-name>.pl` (`plunit` for SWI).
5. **System Standards**: Include relevant system skills (`scryer-prolog-standards`, `swi-prolog-standards`, `trealla-prolog-standards`, `prolog-conventions`, `prolog-initializer`).
6. **README.md**: Include instructions for running tests, using safe runners (`prolog-safe`, `scryer-safe`, `swi-safe`), linking agent skills, and system notes.


## Safety & Cross-Platform Execution

- **CLI Entry Points**: ALL Prolog code executions MUST use the cross-platform CLI safety entry points (`prolog-agent`, `prolog-safe`, `scryer-safe`, `swi-safe`, `trealla-safe`, `tau-safe`).
- **Interactive Top-Level Queries & Persistent Sessions**:
  - Software agents can post multiple queries successively to a running Prolog interpreter using `PrologSession` or `prolog-agent query`/`prolog-agent repl`.
  - The Prolog interpreter process remains active across queries and is **only terminated if a posted query fails to respond within the configured timeout** (`prolog-safe` timeout, defaulting to 20s).
- **Forbidden Invocations**: AI assistants MUST NEVER execute raw interpreter binaries ([`scryer-prolog`](https://github.com/mthom/scryer-prolog), [`swipl`](https://www.swi-prolog.org/), [`tpl`](https://github.com/trealla-prolog/trealla), [`tau-prolog`](http://tau-prolog.org/), [`gprolog`](http://gprolog.org/), [`ciao`](https://ciao-lang.org/)) directly without safety wrappers (`PrologSession`, `prolog-safe`, `scryer-safe`, etc.).

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
3. **Multi-File Synchronization**: Non-Python manifest/doc files (`scryer-manifest.pl`, `pack.pl`, `package.json`, `README.md`, `CHANGELOG.md`) MUST be updated by the agent whenever the `pyproject.toml` version changes or when running `prolog-agent release`.
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
   - `codemeta.json`: Update `description` and `keywords` array.
   - `pyproject.toml`: Add engine tag to `keywords` and CLI entry point script.
2. **Coding Standards & System Cheat Sheets**:
   - Create `.agents/skills/<engine>-prolog-standards/SKILL.md` detailing ISO/engine compliance rules AND including a comprehensive **Standard Library Cheat Sheet** (import headers, exported predicates, and system autoload differences).
   - Register system skill under **Multi-Engine Prolog System Selection & Rules** in `.agents/AGENTS.md`.
3. **Packaging & Dependencies**:
   - Update `.agents/skills/prolog-packaging/SKILL.md` to cover package management for the engine (e.g. `bakage`, `pack`, `npm`).
4. **Testing Frameworks**:
   - Update `.agents/skills/prolog-testing/SKILL.md` to cover test assertions, runners, and CLI invocation commands.
5. **Safety Runners & CLI**:
   - Update `prolog_agent_toolkit/runner.py` and `prolog_agent_toolkit/cli.py` to support binary resolution and safety wrapper entry point `<engine>-safe`.

