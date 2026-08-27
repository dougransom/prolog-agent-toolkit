# starter_project

[Project Summary & Goals - Write a brief human-facing overview of your Prolog library or application here]

## Documentation & AI Agent Rules

- **`README.md`**: Human-facing project overview, architecture, and setup instructions.
- **`AGENTS.md`**: AI assistant rules, dialect standards, and safe runner constraints.

## Project Structure

- **`src/`**: Prolog module source code.
- **`tests/`**: Unit test harness (`testing.pl` / `plunit`).

## Running Tests

```bash
# Scryer Prolog / ISO
scryer-safe tests/testing.pl

# SWI-Prolog
swi-safe -g "run_tests,halt" tests/test_starter_project.pl
```
