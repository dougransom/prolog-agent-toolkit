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
- **Agent Rules & Skills**: Pre-configured guidelines for Scryer Prolog, SWI-Prolog, Trealla Prolog, and ISO Prolog standard compliance.

## Installation

Using [`uv`](https://github.com/astral-sh/uv):

```bash
# Install as CLI tools on PATH
uv tool install /home/doug/code/prolog-agent-toolkit --force

# Or install in editable mode in a Python environment
uv pip install -e /home/doug/code/prolog-agent-toolkit
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

## Release & Versioning Workflow

- Development versions follow `0.0.X.devY` (e.g. `0.0.1.dev1`).
- Official releases match Git annotated tags (e.g. `0.0.1` matches Git tag `v0.0.1`).
