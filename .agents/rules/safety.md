# Prolog Safety & Execution Invariants

> **System Authority**: This document defines the permanent safety and process execution invariants for all Prolog code execution within this project.
> These rules are persistently active for all AI agents and developers.

## 1. Mandatory Safe CLI Entry Points
- **Cross-Platform Safety Wrappers**: ALL Prolog code executions MUST use the cross-platform CLI safety entry points:
  - Generic multi-engine runner: `prolog-safe`
  - Scryer Prolog runner: `scryer-safe`
  - SWI-Prolog runner: `swi-safe`
  - Trealla Prolog runner: `trealla-safe`
  - Tau Prolog runner: `tau-safe`
  - Toolkit management CLI: `prolog-agent`
- **Forbidden Raw Invocations**: AI assistants MUST NEVER execute raw interpreter binaries (`scryer-prolog`, `swipl`, `tpl`, `tau-prolog`, `gprolog`, `ciao`) directly without safety wrappers.

## 2. Resource Sandboxing & Execution Guarantees
- **CPU & Memory Bounds**: The safety runners enforce OS-level cgroups (`systemd-run`), POSIX `RLIMIT_AS`, and priority constraints (`nice -n 19`, `BELOW_NORMAL_PRIORITY_CLASS`) to ensure that runaway computations, infinite recursion, or combinatorial explosions cannot exhaust host system memory or starve CPU resources.
- **5-Second Initial Query Timeout & Suspension**: Interactive queries enforce a default 5.0-second safety timeout. If a query does not complete within 5 seconds, the Prolog process tree is suspended (`SIGSTOP`), freezing CPU usage to zero while preserving interpreter memory.
- **Fibonacci Continuation Progression**: In interactive sessions, resumption proceeds in Fibonacci intervals (**8s**, then **13s**, **21s**, **34s**, etc.) using `SIGCONT`, or terminates upon human/agent rejection.
- **Non-Interactive Fallback**: In automated/piped environments (CI/CD, scripts), the process terminates immediately after the initial timeout to prevent unattended runaway background tasks.

## 3. Python Invocation & Clean Workspace
- **Bytecode Artifact Prevention**: Python tools, test runners, and CLI invocations MUST NOT leave intermediate bytecode or cache artifacts (`__pycache__`, `.pyc`, `.pytest_cache`) in source or test directories.
- **Mandatory Flag**: Python MUST be invoked with bytecode generation disabled:
  ```bash
  PYTHONDONTWRITEBYTECODE=1 uv run pytest
  # or
  python -B <script>
  ```
