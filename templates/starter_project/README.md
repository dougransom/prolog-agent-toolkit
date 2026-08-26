# starter_project

Canonical Prolog starter project skeleton for `prolog-agent-toolkit`.

## Features
- Pure Scryer / ISO / SWI / Trealla Prolog layout (`src/`, `tests/`)
- Pure DCGs (`library(dcgs)`), CLP(Z) integer constraints (`library(clpz)`), and reification (`library(reif)`)
- Multi-engine test harness support (`testing.pl` and `plunit`)
- Safe execution entry points (`scryer-safe`, `swi-safe`, `prolog-safe`)

## Running Tests
```bash
# Scryer Prolog
scryer-safe tests/testing.pl

# SWI-Prolog
swi-safe -g "run_tests,halt" tests/test_starter_project.pl
```
