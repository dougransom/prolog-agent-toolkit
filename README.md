# Prolog Agent Toolkit

**Version**: `0.0.1.dev1`

Multi-engine, cross-platform (Linux, macOS, BSD, Windows) Prolog execution sandboxing and agent skills toolkit.

## Features

- **Cross-Platform Safety Wrappers**: Runs Prolog engines (`scryer-prolog`, `swipl`, `tpl`, `gprolog`, `ciao`) safely with execution timeout limits, low CPU priority, and memory quota monitoring across Linux, macOS, BSD, and Windows.
- **CLI Entry Points**: Built-in CLI commands:
  - `prolog-safe` — Multi-engine generic safety runner (controlled via `PROLOG_ENGINE`).
  - `scryer-safe` — Scryer Prolog safety runner shortcut.
  - `swi-safe` — SWI-Prolog safety runner shortcut.
  - `trealla-safe` — Trealla Prolog safety runner shortcut.
- **Agent Rules & Skills**: Pre-configured standards and workflows for:
  - **Engine Dialects**: `scryer-prolog-standards`, `swi-prolog-standards`, `trealla-prolog-standards`, `prolog-conventions`.
  - **Testing**: `prolog-testing` (Scryer [`testing.pl`](https://github.com/bakaq/testing.pl), SWI `plunit`, portable ISO assertions).
  - **Packaging**: `prolog-packaging` (Scryer [`bakage`](https://github.com/bakaq/bakage) manifests, SWI `pack`).
  - **Release & Versioning**: `prolog-release` (Multi-file version synchronization, Git tagging, post-release workflows).

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

To make your AI coding assistant (Google Antigravity, Claude Code, Cursor, Windsurf) follow these Prolog standards and execution rules in your target project:

#### A. Google Antigravity
Copy or symlink the `.agents/` directory into your target Prolog repository root:
```bash
# In your target Prolog repository:
cp -r /path/to/prolog-agent-toolkit/.agents ./
```
*Antigravity automatically discovers `.agents/AGENTS.md` rules and `.agents/skills/*` skills.*

#### B. Claude Code
Append the rules to your project's `CLAUDE.md` and copy skills:
```bash
# Append universal rules to CLAUDE.md
cat /path/to/prolog-agent-toolkit/.agents/AGENTS.md >> CLAUDE.md

# Copy skills to .claude/skills (or .agents/skills)
mkdir -p .claude/skills
cp -r /path/to/prolog-agent-toolkit/.agents/skills/* .claude/skills/
```

#### C. Cursor / Windsurf / Copilot
Copy the guidelines to your project rules file:
```bash
# For Cursor:
cat /path/to/prolog-agent-toolkit/.agents/AGENTS.md >> .cursorrules

# For Windsurf:
cat /path/to/prolog-agent-toolkit/.agents/AGENTS.md >> .windsurfrules
```

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

## Release & Versioning Workflow

- Development versions follow `X.Y.Z.devN` (e.g. `0.0.1.dev1`).
- Official releases match Git annotated tags (e.g. `0.0.1` matches Git tag `v0.0.1`).

