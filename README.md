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

## Installation

### 1. Install `uv` (if not already installed)

- **Linux / macOS (Bash)**:
  ```bash
  curl -LsSf https://astral.sh/uv/install.sh | sh
  ```
- **Windows (PowerShell)**:
  ```powershell
  powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
  ```
- **Via Pip**:
  ```bash
  pip install uv
  ```

### 2. Install Prolog Agent Toolkit

Using [`uv`](https://github.com/astral-sh/uv):

```bash
# Install as CLI tools on PATH
uv tool install prolog-agent-toolkit --force

# Or install in editable mode for local development
uv pip install -e .
```


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

