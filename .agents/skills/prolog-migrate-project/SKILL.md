---
name: prolog-migrate-project
description: Step-by-step guidance for migrating legacy or ad-hoc Prolog projects to Prolog Agent Toolkit conventions, cleaning up subsumed vendor configs, adopting standard directory layouts, pure ISO Prolog logic, and encouraging execution in a fresh Git branch and worktree.
---

# Legacy Prolog Project Migration Skill

Use this skill whenever migrating an existing or legacy Prolog project (e.g. built with early prompts, ad-hoc scripts, or vendor-specific AGY/Gemini/Claude configs) over to the **Prolog Agent Toolkit** standards and conventions.

---

## Phase 1: Safe Git Isolation (Branch & Worktree First)

> [!IMPORTANT]
> **Safety First**: NEVER perform structural refactoring or delete legacy files directly in your primary working directory or on the `main`/`master` branch without a clean backup.

Before editing code or deleting files:
1. **Check Git Status**:
   ```bash
   git status
   ```
2. **Create a Dedicated Git Worktree & Branch** (Recommended):
   If using Git, isolate the migration work in a separate worktree so your existing working codebase remains untouched until verification is complete:
   ```bash
   # Create a new branch 'migrate/prolog-agent-toolkit' in a parallel worktree directory
   git worktree add -b migrate/prolog-agent-toolkit ../<project-name>-migrate main
   cd ../<project-name>-migrate
   ```
3. **Alternative Feature Branch** (If worktrees are unavailable):
   ```bash
   git checkout -b migrate/prolog-agent-toolkit
   ```

---

## Phase 2: Purging Subsumed Vendor & Harness Configurations

The toolkit enforces **100% vendor neutrality** (see [AGENTS.md](../../AGENTS.md)). Ad-hoc prompt scripts, IDE-specific configs, and harness-specific settings are fully subsumed by the open-standard `.agents/` architecture.

Identify and remove legacy vendor/harness configuration directories and files:

```bash
# Remove local AGY / IDE runtime configuration overrides
rm -rf .gemini

# Remove other vendor-specific or IDE-harness configs if present
rm -rf .claude .cursorrules .windsurfrule .clinerules .github/copilot-instructions.md
```

> [!NOTE]
> Standard `.gitignore`, `.github/workflows/`, and general project build files should be preserved unless they conflict with Prolog engine safety runners.

---

## Phase 3: Linking Agent Architecture & Standards

Connect the project to the central Prolog Agent Toolkit skills, subagents, and guidelines:

1. **Link or Copy `.agents/`**:
   ```bash
   # Option A: Symlink central .agents directory (recommended for local dev)
   ln -s /path/to/prolog-agent-toolkit/.agents .agents

   # Option B: Copy .agents directory (for standalone repo distribution)
   cp -r /path/to/prolog-agent-toolkit/.agents .agents
   ```
2. **Verify `AGENTS.md`**:
   Ensure a vendor-neutral `AGENTS.md` file exists in the project root referencing Covington style guidelines and dialect standards.

---

## Phase 4: Restructuring Folder Layout

Upgrade the repository structure to the canonical multi-dialect layout:

```text
<project-name>/
├── src/
│   ├── core/                  # 100% Pure ISO Prolog logic (engine-agnostic)
│   ├── adapters/              # Dialect shims (Scryer, SWI, Trealla, Tau)
│   └── <project-name>.pl      # Main module entry point
├── tests/
│   ├── portable/              # ISO-compliant unit test assertions
│   ├── scryer/                # Scryer testing.pl harness
│   ├── swi/                   # SWI plunit test harness
│   └── testing.pl             # Default runner harness (Scryer/Trealla/ISO)
├── .agents/                   # Symlink/copy of toolkit .agents directory
├── AGENTS.md                  # Universal AI assistant instructions
├── bakage.toml                # Scryer manifest
├── pack.pl                    # SWI pack manifest
├── CHANGELOG.md               # Version history
└── README.md                  # Human & agent onboarding documentation
```

### CLI Scaffolding Helper
To quickly generate missing layout boilerplate and manifests:
```bash
prolog-agent template <project-name> --dialect scryer
```
Then move existing `.pl` source files into `src/` (or `src/core/`) and test scripts into `tests/`.

---

## Phase 5: Refactoring Prolog Source Code for Purity & Conventions

Refactor existing Prolog logic according to toolkit guidelines:

1. **Pure ISO Logic & Reification**:
   - Replace non-logical cuts (`!`) and `->` with `if_/3` (from `library(reif)`) and `dif/2`.
   - Use pure DCGs (`library(dcgs)`) for text/token parsing.
   - Use `library(clpz)` or `library(clpfd)` for integer constraints.
2. **Explicit Standard Library Imports**:
   - Add explicit headers to all Prolog files instead of relying on dialect autoloading:
     ```prolog
     :- use_module(library(dcgs)).
     :- use_module(library(charsio)).
     :- use_module(library(reif)).
     :- use_module(library(si)).
     ```
3. **String Representation**:
   - Treat strings strictly as lists of characters (`chars` double-quoted lists). Avoid SWI string types or SWI dicts when targeting portable ISO / Scryer Prolog.
4. **Library Discovery Protocol**:
   - Run `prolog-agent discover --engine <engine>` to find standard library predicates instead of reinventing them from scratch.
5. **Use Autonomous Refactoring Subagent**:
   - Invoke `prolog-refactor-agent` or `prolog-purity-reviewer-agent` to automatically identify non-pure patterns and suggest fixes.

---

## Phase 6: Automated Verification & Worktree Merge

1. **Execute Tests via Safety Runners**:
   Replace raw binary calls with resource-capped safety execution wrappers:
   ```bash
   # For Scryer / Trealla / ISO
   scryer-safe tests/testing.pl

   # For SWI-Prolog
   swi-safe -g "run_tests,halt" tests/test_<project-name>.pl
   ```
2. **Review Git Diff**:
   Inspect the clean changes in your worktree:
   ```bash
   git status
   git diff
   ```
3. **Commit & Merge**:
   ```bash
   git add .
   git commit -m "Migrate project to Prolog Agent Toolkit conventions"
   
   # Switch back to main repo and merge the migration branch
   cd /path/to/original/<project-name>
   git merge migrate/prolog-agent-toolkit
   ```
4. **Clean Up Worktree**:
   ```bash
   git worktree remove ../<project-name>-migrate
   git branch -d migrate/prolog-agent-toolkit
   ```
