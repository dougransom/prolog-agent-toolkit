<!-- OpenGraph Metadata -->
<meta property="og:title" content="Prolog Agent Toolkit" />
<meta property="og:type" content="website" />
<meta property="og:description" content="Multi-engine, cross-platform Prolog execution sandboxing, AI agent standards, and skills toolkit for Scryer Prolog, SWI-Prolog, Trealla Prolog, and Tau Prolog. Supporting Google Antigravity, Claude Code, GitHub Copilot, Cursor, aidermacs, agent-shell, and gptel." />
<meta property="og:category" content="Developer Tools, Prolog, AI Agents" />

<!-- Schema.org JSON-LD Metadata -->
<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@type": "SoftwareSourceCode",
  "name": "Prolog Agent Toolkit",
  "version": "0.0.1.dev5",
  "description": "Multi-engine, cross-platform Prolog execution sandboxing, AI agent standards, and skills toolkit for Scryer Prolog, SWI-Prolog, Trealla Prolog, and Tau Prolog. Supporting Google Antigravity, Claude Code, GitHub Copilot, Cursor, aidermacs, agent-shell, and gptel.",
  "programmingLanguage": "Prolog",
  "targetProduct": [
    { "@type": "SoftwareApplication", "name": "Google Antigravity" },
    { "@type": "SoftwareApplication", "name": "Claude Code" },
    { "@type": "SoftwareApplication", "name": "GitHub Copilot" },
    { "@type": "SoftwareApplication", "name": "Cursor" },
    { "@type": "SoftwareApplication", "name": "aidermacs" },
    { "@type": "SoftwareApplication", "name": "agent-shell" },
    { "@type": "SoftwareApplication", "name": "gptel" }
  ],
  "keywords": ["prolog", "scryer-prolog", "swi-prolog", "trealla-prolog", "tau-prolog", "agent-toolkit", "antigravity", "claude-code", "copilot", "cursor", "aidermacs", "agent-shell", "gptel", "emacs", "dcg", "clpz", "sandboxing"]
}
</script>

# Prolog Agent Toolkit

**Version**: `0.0.1.dev5`  
**Category**: AI Assistant Developer Tools / Prolog Language Tooling  
**Metadata**: [schema.org.jsonld](schema.org.jsonld)

Multi-engine, cross-platform (Linux, macOS, BSD, Windows) Prolog execution sandboxing and AI agent skills toolkit.

## Categories & Supported Platforms

| Category | Supported Technologies / Systems |
|---|---|
| **AI Assistants & IDEs** | Google Antigravity (AGY), Claude Code (Anthropic), GitHub Copilot, Cursor, Windsurf, Emacs AI (`aidermacs`, `agent-shell`, `gptel`) |
| **Prolog Engines** | Scryer Prolog (ISO Default), SWI-Prolog, Trealla Prolog, Tau Prolog, GNU Prolog, Ciao Prolog |
| **Language Standards** | ISO Prolog, Definite Clause Grammars (DCG), CLP(Z) Constraints, Reification (`reif`) |
| **Agent Capabilities** | Execution Sandboxing, `testing.pl` Unit Testing, `bakage` Manifests, Multi-file Release Versioning |

**Keywords**: `prolog`, `agent-toolkit`, `scryer-prolog`, `swi-prolog`, `trealla-prolog`, `tau-prolog`, `antigravity`, `claude-code`, `copilot`, `cursor`, `aidermacs`, `agent-shell`, `gptel`, `emacs`, `dcg`, `clpz`, `sandboxing`, `testing.pl`, `bakage`

## Features

- **Cross-Platform Safety Wrappers**: Runs Prolog engines (`scryer-prolog`, `swipl`, `tpl`, `tau-prolog`, `gprolog`, `ciao`) safely with execution timeout limits, low CPU priority, and memory quota monitoring across Linux, macOS, BSD, and Windows.
- **CLI Entry Points**: Built-in CLI commands:
  - `prolog-agent` — Project initializer (`init`), release version manager (`release`), subagent listing, and skill validation.
  - `prolog-safe` — Multi-engine generic safety runner (controlled via `PROLOG_ENGINE`).
  - `scryer-safe` — Scryer Prolog safety runner shortcut.
  - `swi-safe` — SWI-Prolog safety runner shortcut.
  - `trealla-safe` — Trealla Prolog safety runner shortcut.
  - `tau-safe` — Tau Prolog safety runner shortcut.
- **Project Initializer & Release Workflows**:
  - `prolog-agent init <project-name> [--engine scryer|swi|trealla|tau|iso]` — Scaffolds `src/`, `tests/`, `README.md`, `.agents` link instructions, engine-specific manifest (`bakage.toml`, `pack.pl`, `package.json`), starter module, and test harness (`testing.pl` / `plunit`).
  - `prolog-agent release [--version X.Y.Z]` — Version synchronization across manifest files, `CHANGELOG.md` generation, and Git release tagging instructions.
- **Agent Rules & Skills**: Pre-configured standards and workflows for:
  - **Engine Dialects**: `scryer-prolog-standards`, `swi-prolog-standards`, `trealla-prolog-standards`, `tau-prolog-standards`, `prolog-conventions`.
  - **Testing**: `prolog-testing` (Scryer [`testing.pl`](https://github.com/bakaq/testing.pl), SWI `plunit`, portable ISO assertions).
  - **Packaging**: `prolog-packaging` (Scryer [`bakage`](https://github.com/bakaq/bakage) manifests, SWI `pack`).
  - **Release & Versioning**: `prolog-release` (Multi-file version synchronization, Git tagging, post-release workflows).
  - **Logic Paradigms**: `prolog-clp-constraints` (CLP(Z)/CLP(FD)), `prolog-dcg-mastery` (pure DCGs & parsing), `prolog-tabling` (SLG memoization).
  - **Quality & Profiling**: `prolog-linter-static-analysis` (syntax & warning audits), `prolog-performance-profiling` (choicepoint elimination & TCO), `prolog-debugging-workflow` (4-port model debugging).
  - **Integration & Systems**: `prolog-ffi-wasm-embedding` (C, Rust, Python, WASM, JS), `prolog-web-services` (REST & WebSockets), `prolog-neurosymbolic-agent` (LLM + Prolog verifiers).
  - **Code Review**: `prolog-code-review` (Automated PR reviews, purity, portability & safety audits).
- **Autonomous Subagents**: Specialized AI subagent definitions in `.agents/agents/`:
  - `prolog-refactor-agent` (Imperative to pure ISO Prolog refactoring).
  - `prolog-test-generator-agent` (Automated unit test generation).
  - `prolog-benchmark-runner-agent` (Multi-engine benchmark comparisons).
  - `prolog-doc-generator-agent` (Covington comment & API documentation extraction).
  - `prolog-pr-reviewer-agent` (Automated PR auditing, static analysis & test runner).
  - `prolog-purity-reviewer-agent` (Purity & Covington style review).
  - `prolog-portability-reviewer-agent` (Multi-engine dialect & portability review).
  - `prolog-security-reviewer-agent` (Dynamic term injection & safety limits audit).

## Installation & Setup

### 1. Install CLI Safety Tools (`scryer-safe`, `swi-safe`, etc.)

First, install the Python CLI package so safety runners (`scryer-safe`, `swi-safe`, `trealla-safe`, `prolog-safe`) are accessible globally on your system PATH:

Using [`uv`](https://github.com/astral-sh/uv) (recommended):

```bash
# Install directly from local repository directory
uv tool install . --force

# Or install in editable mode for development
uv pip install -e .
```

Verify installation:
```bash
scryer-safe --help
```

---

### 2. Integrating Agent Rules & Skills with AI Assistants

To ensure your rules and skills **never get clobbered or overwritten** when updating or working inside target repositories, use one of the following recommended methods:

---

#### Option A: Symlink into Target Project (Recommended for Team & Project Scope)
Symlinking links your target project to `prolog-agent-toolkit` directly. When you update `prolog-agent-toolkit`, all linked projects get the updates automatically without clobbering local repo files!

```bash
# Inside your target Prolog project root:
ln -s /home/doug/code/prolog-agent-toolkit/.agents .agents
```

---

#### Option B: Global Machine Installation (Recommended for Personal Setup)
Install rules and skills into your global AI configuration folder so **every** project automatically inherits them across your system:

* **Google Antigravity**:
  ```bash
  mkdir -p ~/.gemini/config/skills
  cp -r /home/doug/code/prolog-agent-toolkit/.agents/skills/* ~/.gemini/config/skills/
  cat /home/doug/code/prolog-agent-toolkit/.agents/AGENTS.md >> ~/.gemini/config/AGENTS.md
  ```

* **Vendor-Agnostic AI Rules (`AGENTS.md`)**:
  ```bash
  # Root AGENTS.md symlinked directly to .agents/AGENTS.md:
  ln -s .agents/AGENTS.md AGENTS.md
  ```

---

### Single Source of Truth Architecture

To prevent instruction drift across different AI tools and assistants:

- **Vendor-Agnostic Single Source of Truth**: [.agents/AGENTS.md](.agents/AGENTS.md) (symlinked as `AGENTS.md` at root) is the single source of truth for all Prolog rules, dialect choices, and safety constraints.
- **Universal Tool Support**: All modern AI tools (Gemini CLI, Antigravity, Claude Code, Cursor, Windsurf, Codex, Emacs `aidermacs`/`agent-shell`/`gptel`) read `AGENTS.md` natively, eliminating the need for vendor-specific files like `CLAUDE.md` or `.cursorrules`.
- **Zero Maintenance Overhead**: Editing `.agents/AGENTS.md` updates all tools instantly without copy-pasting or file duplication.

#### Option C: Custom Search Paths via `skills.json` (Multi-Directory Search Path)
Google Antigravity automatically loads rules and skills from **both**:
1. **Global Root**: `~/.gemini/config` (active across all your workspaces)
2. **Workspace Root**: `.agents` (active in the specific project)

If you have skills scattered across multiple repositories or team folders (e.g., `prolog-agent-toolkit`, `data-science-skills`, `team-shared-skills`), you can create a `skills.json` file in your `.agents/` or `~/.gemini/config/` directory to act as a **search path**:

Create `.agents/skills.json` (or `~/.gemini/config/skills.json`):
```json
{
  "entries": [
    { "path": "/home/doug/code/prolog-agent-toolkit/.agents/skills" },
    { "path": "/home/doug/code/another-repo/.agents/skills" }
  ],
  "inherits": [
    { "path": "/path/to/shared/team_skills.json" }
  ],
  "exclude": [
    "optional_skill_to_ignore"
  ]
}
```

---

> [!TIP]
> **Why Symlinks / Global Configs / `skills.json` prevent clobbering:**
> 1. **Search Path (`skills.json`)**: Lets you keep skills in their native repos while referencing them dynamically in any project.
> 2. **Symlinking (`ln -s`)**: Keeps rules in `prolog-agent-toolkit` as the single source of truth without `git` merge conflicts in target projects.
> 3. **Global Config (`~/.gemini/config`)**: Automatically applies across all projects without modifying target repo files.

---

## Usage

```bash
# Run Scryer Prolog safely
scryer-safe -g "use_module(library(format)), format(\"Hello~n\", []), halt."

# Run SWI-Prolog safely
swi-safe -g "writeln('Hello SWI'), halt."

# Select engine using environment variable
PROLOG_ENGINE=trealla prolog-safe -g "write('Hello Trealla'), nl, halt."

# Configure safety limits via environment variables
PROLOG_TIMEOUT=10s PROLOG_MEMORY_MAX=100M prolog-safe -g "my_pred, halt."
```

## Agent Skills & Project Bootstrapping

The toolkit includes automated agent skills located in `.agents/skills/`:

- **Project Setup**: When initializing a project, the agent prompts to set up testing (`testing.pl` / `plunit`) and packaging manifests (`bakage` / `pack.pl`).
- **Clean Workspace**: Python bytecode creation is disabled (`PYTHONDONTWRITEBYTECODE=1`), and test caches are stored centrally in `.cache/pytest`.
- **Release Synchronization**: `prolog-release` synchronizes version strings consistently across `pack.pl`, `pyproject.toml`, `README.md`, `__init__.py`, and annotated Git tags.

## Programmer Guidelines: Working with AI for Prolog

For complete details, see [.agents/references/programmer_guidelines.md](.agents/references/programmer_guidelines.md).

When working with AI coding assistants (Google Antigravity, Claude Code, Cursor, Copilot, Emacs `aidermacs`/`gptel`) on Prolog software:

1. **Provide Semantics & AST Shapes, Not Logic Invention**: Give the AI module skeletons, AST constructors, and type invariants instead of asking it to invent relations from scratch.
2. **Specify Mode & Determinism Contracts Explicitly**: State input/output modes (`+`/`-`) and determinism requirements (`det`, `semidet` fail cleanly, `nondet` backtracking).
3. **Use Test-First Prompting**: Provide expected test cases (`testing.pl`, `plunit`, or test runner) first, then request code satisfying those tests.
4. **Enforce the Declarative Mindset**: Explicitly prompt: *"Do not use imperative reasoning. Use declarative reasoning based on unification, constraints, and backtracking."*
5. **Delegate DCG & Structural Boilerplate**: Let AI handle grammar production rules, AST building, and string formatting.
6. **Use AI for Refactoring & Choice-Point Audits**: Ask AI to identify choice points, make code tail-recursive, or transform cut-heavy logic into pure forms (`dif/2`, `if_/3`).

## Release & Versioning Workflow

- Development versions follow `X.Y.Z.devN` (e.g. `0.0.1.dev1`).
- Official releases match Git annotated tags (e.g. `0.0.1` matches Git tag `v0.0.1`).

