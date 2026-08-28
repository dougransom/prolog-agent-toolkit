# AI Agent Navigation Guide & Onboarding Blueprint

Welcome to **`prolog-agent-toolkit`**. This document is the primary onboarding entry point designed specifically for AI coding agents ([Google Antigravity](https://antigravity.google), [Claude Code](https://docs.anthropic.com/en/docs/agents-and-tools/claude-code/overview), [Cursor](https://www.cursor.com/), [Windsurf](https://codeium.com/windsurf), [GitHub Copilot](https://github.com/features/copilot), and [Emacs](https://www.gnu.org/software/emacs/) AI tools such as [`aidermacs`](https://github.com/MatthewZMD/aidermacs), [`agent-shell`](https://github.com/xenodium/agent-shell), and [`gptel`](https://github.com/karthink/gptel)).

This repository is **100% vendor-neutral**. All steering guidelines, specifications, and navigation blueprints follow open, standard Markdown (`AGENTS.md`, `.agents/skills/<name>/SKILL.md`, `.agents/agents/<name>.md`) and JSON metadata format conventions.

> [!IMPORTANT]
> **Vendor Neutrality Principle**: AI agent instructions MUST remain vendor-agnostic. Do NOT create vendor-specific or IDE-harness-specific configuration files (such as `.claude/`, `.windsurfrule`, `.cursorrules`, `.github/copilot-instructions.md`, `.clinerules`, `.gemini/`, or harness-specific Emacs configs). All rules and skills belong strictly in standard `.agents/` layout so any AI coding tool or harness can consume them natively.

---

## 1. Top 10 Agent Onboarding Q&A

### Q1: What is this project?
A multi-engine, cross-platform Prolog safety runner, project scaffolding tool, release manager, AI agent standards registry, and declarative skill toolkit for **[Scryer Prolog](https://github.com/mthom/scryer-prolog)**, **[SWI-Prolog](https://www.swi-prolog.org/)**, **[Trealla Prolog](https://github.com/trealla-prolog/trealla)**, and **[Tau Prolog](http://tau-prolog.org/)**.

### Q2: Why does it exist?
To allow AI coding agents to safely write, test, refactor, and run pure ISO-compliant Prolog code without causing infinite loops, crashing operating system resources, or producing unsound/defaulty logic.

### Q3: What are its major components?
1. **Python Toolkit Package** ([`prolog_agent_toolkit/`](prolog_agent_toolkit)): Safety runners (`prolog-safe`, `scryer-safe`), CLI initializer (`prolog-agent init`), syntax diagnostic checker, skill frontmatter validator, and release sync manager.
2. **Declarative Agent Layer** ([`.agents/`](.agents)): 21 declarative skills ([`.agents/skills/`](.agents/skills)), 8 autonomous subagents ([`.agents/agents/`](.agents/agents)), and purity reference guides ([`.agents/references/`](.agents/references)).
3. **Repository Architecture & Metadata** ([`docs/`](docs)): Human-readable ontology ([`docs/ONTOLOGY.md`](docs/ONTOLOGY.md)), machine-readable ontology graph ([`docs/repository_ontology.json`](docs/repository_ontology.json)), capability manifests ([`docs/capability_manifest.json`](docs/capability_manifest.json)), glossary ([`docs/GLOSSARY.md`](docs/GLOSSARY.md)), and Architecture Decision Records ([`docs/adr/`](docs/adr)).
4. **Scaffolding Templates** ([`templates/`](templates)): Starter projects and pure Prolog module templates.

### Q4: What terminology is important?
- **ISO Scryer Prolog**: Primary target engine enforcing ISO standard compliance.
- **Logical Purity**: Preferring `if_/3` (reification from [`library(reif)`](https://github.com/mthom/scryer-prolog/blob/master/src/lib/reif.pl)) and `dif/2` over non-logical cuts (`!`) or negation-as-failure (`\+/1`).
- **Chars**: Representing strings strictly as lists of 1-character atoms (`"abc"` = `['a','b','c']`).
- **Safety Runner**: Capped execution wrapper (`scryer-safe`, `prolog-safe`) enforcing CPU/memory quotas to protect host systems.
- **Bakage**: Standard Scryer Prolog package manifest format (`bakage.toml`).

### Q5: Which files are authoritative?
- **Package Version**: [`pyproject.toml`](pyproject.toml) is the single canonical source of truth for versions.
- **Agent Rules & Steering**: [`AGENTS.md`](AGENTS.md) and [`.agents/AGENTS.md`](.agents/AGENTS.md).
- **Directory & Navigation Index**: [`AGENT_INDEX.json`](AGENT_INDEX.json).
- **Component Graph**: [`docs/repository_ontology.json`](docs/repository_ontology.json).

### Q6: Where should new functionality be added?
- Safety/CLI feature -> [`prolog_agent_toolkit/`](prolog_agent_toolkit)
- AI Skill -> [`.agents/skills/<skill-name>/SKILL.md`](.agents/skills)
- Subagent -> [`.agents/agents/<subagent-name>.md`](.agents/agents)
- Scaffolding Template -> [`templates/`](templates)
- Architectural Decision -> [`docs/adr/`](docs/adr)

### Q7: Which standards apply?
- Universal Prolog Style & Purity: [`.agents/references/prolog_guidelines.md`](.agents/references/prolog_guidelines.md)
- Covington Prolog Style Guide: [`.agents/references/covington_style.md`](.agents/references/covington_style.md)
- Dialect Standards: [`.agents/skills/scryer-prolog-standards/SKILL.md`](.agents/skills/scryer-prolog-standards/SKILL.md), [`.agents/skills/swi-prolog-standards/SKILL.md`](.agents/skills/swi-prolog-standards/SKILL.md)

### Q8: Which skills already exist?
21 declarative skills are cataloged in [`.agents/skills.json`](.agents/skills.json), spanning [`CLP(Z)`](https://github.com/mthom/scryer-prolog/blob/master/src/lib/clpz.pl), pure DCGs, tabling, web services, testing, packaging, profiling, and engine onboarding.

### Q9: What should not be duplicated?
Review [`docs/ANTI_PATTERNS.md`](docs/ANTI_PATTERNS.md) before writing new code. Never re-implement syntax checking (use `prolog_agent_toolkit.syntax_checker`), hardcode version strings, or invoke raw interpreter binaries ([`scryer-prolog`](https://github.com/mthom/scryer-prolog), [`swipl`](https://www.swi-prolog.org/)) directly.

### Q10: How should changes be proposed?
Follow the **AI Agent Contribution Protocol** in [`CONTRIBUTING.md`](CONTRIBUTING.md): run `pytest`, validate skills (`prolog-agent validate-skills`), check version synchronization (`prolog-agent check-version`), and submit PRs with verification trace logs.

### Q11: Are unit tests or package manifests required for simple/toplevel use cases?
No. Scaffolding creates `tests/` and manifests (`bakage.toml`/`pack.pl`) as a best practice so AI agents can perform automated test verification. However, safety runners (`scryer-safe`, `swi-safe`, `trealla-safe`, `prolog-safe`) work standalone:
- **Interactive REPL**: Run `scryer-safe` or `swi-safe` directly to launch a sandboxed top-level REPL without any project or tests.
- **Scratch Scripts**: Run `scryer-safe scratch.pl` to execute standalone scripts without a test suite or manifest.
- **Minimal Codebases**: Users are free to remove `tests/` or manifest files from scaffolded projects.

---

## 2. Information Architecture & Key Files Map

```
prolog-agent-toolkit/
├── AGENT_GUIDE.md                   # Primary Onboarding Blueprint (This File)
├── AGENT_INDEX.json                 # Machine-Readable File Index & Directory Map
├── AGENTS.md                        # Universal Agent Rules & Core Guidelines
├── README.md                        # Human & Web Overview
├── pyproject.toml                   # Version Source of Truth & Package Build Spec
├── schema.org.jsonld                # Schema.org Metadata Specification
│
├── docs/                            # Architectural & Machine-Readable Domain Context
│   ├── repository_ontology.json     # Graph of Module Dependencies & File Relations
│   ├── capability_manifest.json     # Executable CLI & Subagent Tool Registry
│   ├── GLOSSARY.md                  # Detailed Terminology Reference
│   ├── terminology.json             # Machine-Readable Term Dictionary
│   ├── ANTI_PATTERNS.md             # Forbidden Coding Practices & Helper Inventory
│   └── adr/                         # Architectural Decision Records (0001 - 0003)
│
├── .agents/                         # Declarative Agent Knowledge & Rules System
│   ├── AGENTS.md                    # Deep Guidelines Reference
│   ├── skills.json                  # Detailed Skill Metadata Catalog
│   ├── agents/                      # 8 Autonomous Subagents
│   ├── references/                  # Purity, Covington Style & Steering Guidelines
│   └── skills/                      # 21 Declarative Skill Modules
│
├── prolog_agent_toolkit/            # Python Engine & CLI Package
│   ├── cli.py                       # Main CLI Commands (`prolog-agent`, `prolog-safe`)
│   ├── runner.py                    # Resource-Capped Execution Safety Wrappers
│   ├── project.py                   # Project & Module Scaffolding Engine
│   ├── syntax_checker.py            # Prolog Syntax Diagnostics
│   ├── skill_validator.py           # Skill Frontmatter Validator
│   └── release.py                   # Release & Version Synchronization Engine
│
└── tests/                           # Pytest Execution Safety Suite
```

---

## 3. Modification & Execution Workflows for Agents

### Command Execution Policy
AI agents **MUST ALWAYS** use safety entry points instead of raw interpreter binaries:
- `prolog-safe "consult('module.pl'), test_goal."`
- `scryer-safe "-g test_goal module.pl"`
- `swi-safe "-g test_goal module.pl"`

### Clean Workspace Requirement
All Python scripts and tests **MUST NOT** write `__pycache__` artifacts into source trees:
```bash
PYTHONDONTWRITEBYTECODE=1 uv run pytest
```
