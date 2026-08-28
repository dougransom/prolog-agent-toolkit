# ADR 0002: Mandatory Execution Safety Sandboxing

- **Status**: Accepted
- **Date**: 2026-08-28

## Context
AI coding agents executing arbitrary Prolog goals can accidentally introduce non-terminating recursive search loops, unbounded backtracking, or high memory allocations that freeze or crash host OS environments.

## Decision
All Prolog executions invoked by AI agents or automated test suites MUST use resource-capped execution wrappers (`prolog-safe`, `scryer-safe`, `swi-safe`, `trealla-safe`, `tau-safe`) provided by [`prolog_agent_toolkit/runner.py`](file:///home/doug/code/prolog-agent-toolkit/prolog_agent_toolkit/runner.py). Direct execution of raw interpreter binaries (`scryer-prolog`, `swipl`, `tpl`) is strictly forbidden.

## Rationale
1. **Host Stability**: `runner.py` applies process timeouts and memory quotas via `psutil`.
2. **Deterministic Termination**: Runaway search branches are safely terminated with clean error output instead of locking system resources.
3. **Cross-Platform Parity**: The safety entry points normalize command-line flags across OS platforms and Prolog engines.

## Consequences
- AI agent instructions (`AGENTS.md`) explicitly forbid raw interpreter execution.
- CLI entry points (`prolog-safe`, `scryer-safe`, `swi-safe`, `trealla-safe`, `tau-safe`) are registered in `pyproject.toml`.
