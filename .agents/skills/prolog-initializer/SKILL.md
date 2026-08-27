---
name: prolog-initializer
description: Dialect-aware Prolog project initialization, module generation, template scaffolding, bash script generation, and release workflow for Scryer, SWI, and Trealla.
---

# Prolog Agent Toolkit — Dialect-Aware Project Initializer & Workflow Skill

This skill provides authoritative instructions and automation for initializing Prolog projects, generating modules, generating project templates, producing POSIX bash initialization scripts, and running release workflows across **Scryer Prolog**, **SWI-Prolog**, and **Trealla Prolog**.

## Virtual Commands & Workflows

### 1. Project Initializer Tool (`prolog-agent init`)
```bash
prolog-agent init <project-name> [--dialect scryer|swi|trealla]
```
If dialect is omitted, default to **scryer**.

**Initializer Workflow:**
1. **Directory Structure**: Create `<project-name>/` with `src/`, `tests/`, `README.md`, `CHANGELOG.md`, and `.agents/` symlink/copy.
2. **Packaging**:
   - **Scryer**: Create `bakage.toml` (`name`, `version="0.1.0"`, `modules=["src/<project-name>.pl"]`, `requires=[]`).
   - **SWI**: Create `pack.pl` (`name('<project-name>')`, `version('0.1.0')`, `title`, `author`).
   - **Trealla**: No packaging manifest created.
3. **Starter Module**: Create `src/<project-name>.pl` with module header, Covington documentation comments, DCG stub, and pure predicate.
4. **Test Harness**:
   - **Scryer / Trealla / ISO**: Create `tests/testing.pl`.
   - **SWI**: Create `tests/test_<project-name>.pl` using `plunit`.
5. **Dialect Standards**: Include `scryer-prolog-standards`, `swi-prolog-standards`, `trealla-prolog-standards`, and `prolog-conventions`.
6. **README.md**: Create canonical onboarding README with 6 structured sections (Project Overview, Directory Layout, Dialect Selection, Safe Runners, Agent Skills, and Testing).

---

### 2. Project Template Generator (`prolog-agent template`)
```bash
prolog-agent template <project-name> [--dialect scryer|swi|trealla]
```
Generates a deterministic canonical project layout:
```text
<project-name>/
  src/
    core/                  # 100% Pure ISO Prolog core
    adapters/              # Dialect shims (scryer, swi, trealla, tau)
    <project-name>.pl      # Main module entry point
  tests/
    portable/              # Pure ISO assertions
    scryer/                # Scryer testing.pl harness
    swi/                   # SWI plunit test suite
    testing.pl or test_<project-name>.pl
  AGENTS.md                # AI assistant guidelines
  bakage.toml              # Scryer manifest
  pack.pl                  # SWI pack manifest & fallback
  package.json             # Tau Prolog / npm manifest
  CHANGELOG.md             # Release history
  README.md                # Human-facing documentation
```

---

### 3. Module Generator Tool (`prolog-agent module`)
```bash
prolog-agent module <module-name> [--dialect scryer|swi|trealla]
```
Generates `src/<module-name>.pl` with:
- Dialect-appropriate module declaration (Scryer `:- module(name, [...]).`, SWI `:- module(name, [...]).`, Trealla ISO clean exports).
- Covington comment header (mode, determinism, purity).
- Deterministic pure predicate stubs.
- Pure DCG grammar example (`library(dcgs)`).
- CLP(Z) / CLP(FD) constraint example (`library(clpz)`).

---

### 4. Bash Initializer Script Generator (`prolog-agent init-script`)
```bash
prolog-agent init-script
```
Outputs a POSIX-compatible bash script (`scripts/prolog_agent_init.sh`) that automates project initialization without execution (user copy/paste or direct execution).

---

### 5. Release Workflow Tool (`prolog-agent release`)
```bash
prolog-agent release [--version X.Y.Z]
```
1. **Synchronize Versions**: Synchronize version in `bakage.toml`, `pack.pl`, `pyproject.toml`, and `README.md`.
2. **Generate CHANGELOG**: Create/update `CHANGELOG.md` with version header (`## [X.Y.Z] - YYYY-MM-DD`).
3. **Tag Release**: Prompt git tag creation matching version (`git tag -a vX.Y.Z -m "Release vX.Y.Z"`).
4. **Publish**: Prepare `bakage` or `pack` metadata for distribution.

---

## User Project Initialization Instructions
When a user asks how to start a new Prolog project:
1. `mkdir myproj && cd myproj`
2. `ln -s ~/code/prolog-agent-toolkit/.agents .agents`
3. Choose dialect: Scryer (default), SWI, or Trealla.
4. Execute `prolog-agent init myproj --dialect <dialect>` or run `scripts/prolog_agent_init.sh myproj <dialect>`.
5. Run tests with `scryer-safe tests/testing.pl` or `swi-safe -g "run_tests,halt" tests/test_myproj.pl`.

---

## Agent Behavior Rules
- Always generate deterministic, reproducible project structures.
- Never mix Prolog dialects unless explicitly instructed.
- Always use safe runners (`prolog-safe`, `scryer-safe`, `swi-safe`, `trealla-safe`).
- Always follow the initializer workflow and release workflow exactly.
- Prefer pure predicates, DCGs, and CLP(Z) constraints.
- Default dialect is Scryer.
