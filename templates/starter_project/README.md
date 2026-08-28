# starter_project

[Project Summary & Goals - Write a brief human-facing overview of your Prolog library or application here]

## Documentation & AI Agent Rules

- **`README.md`**: Human-facing project overview, architecture, and setup instructions.
- **`AGENTS.md`**: AI assistant rules, dialect standards, and safe runner constraints.

## Project Structure

Recommended canonical project layout supporting single or multi-dialect development:

```text
starter_project/
├── src/                            # Source code directory
│   ├── core/                       # Portable Prolog core (dialect-agnostic ISO target)
│   │   └── logic.pl
│   ├── adapters/                   # Engine shims & compatibility layers
│   │   ├── scryer/compat.pl        # Scryer imports (charsio, reif, clpz)
│   │   ├── swi/compat.pl           # SWI imports (clpfd, plunit)
│   │   ├── trealla/compat.pl       # Trealla compatibility shims
│   │   └── tau/compat.pl           # Tau JS/DOM shims
│   └── starter_project.pl          # Main module entry point
├── tests/                          # Test suites directory
│   ├── portable/                   # Engine-agnostic goal assertions
│   ├── scryer/                     # Scryer testing.pl harness
│   ├── swi/                        # SWI plunit test suite
│   └── testing.pl                  # Default test harness
├── AGENTS.md                       # AI assistant rules & dialect guidelines
├── bakage.toml                     # Scryer Prolog bakage manifest
├── pack.pl                         # SWI-Prolog pack manifest & Scryer fallback
├── package.json                    # Tau Prolog / npm manifest (optional for Node/DOM)
├── CHANGELOG.md                    # Version release history
└── README.md                       # Human-facing project documentation
```

## Running Tests

```bash
# Scryer Prolog / Portable Runner
scryer-safe tests/testing.pl

# SWI-Prolog
swi-safe -g "run_tests,halt" tests/test_starter_project.pl
```
