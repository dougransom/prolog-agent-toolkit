# Contributing to Prolog Agent Toolkit

Thank you for contributing to the **Prolog Agent Toolkit**! We welcome contributions for adding new engine safety wrappers, extending AI agent skills, and improving Prolog guidelines.

> [!NOTE]
> **Project Status: Active Development**  
> The toolkit is fully functional and usable today, but remains under **active development**. We strongly encourage community feedback and contributions!
>
> We are open to:
> - **[Pull Requests](https://docs.github.com/en/pull-requests/collaborating-with-pull-requests/proposing-changes-to-your-work-with-pull-requests/about-pull-requests)**: Code changes, new Prolog engine safety wrappers, bug fixes, or AI skill additions.
> - **[GitHub Issues](https://github.com/dougransom/prolog-agent-toolkit/issues)** for:
>   - Suggestions for new features, architectural goals, or engine targets.
>   - Examples of unwanted AI-generated Prolog code ("AI slop", copy-pasted loops, unnecessary low-level cuts `!`, `->`, `\+`) to help refine agent rules and purity guidelines.
>   - Suggestions for prompts or agent workflows to run on this project itself!

---

## 1. Project Architecture

The toolkit consists of two primary layers:

1. **Python Execution Safety CLI** (`prolog_agent_toolkit/`):
   - Cross-platform resource sandboxing, execution timeout monitoring, low-CPU scheduling, and RAM limits.
   - Entry points: `prolog-safe`, `scryer-safe`, `swi-safe`, `trealla-safe`, `tau-safe`.
2. **AI Agent Customizations** (`.agents/`):
   - Rules (`.agents/AGENTS.md`, `.agents/references/`) defining Prolog coding standards and portable ISO code targets. `.agents/AGENTS.md` (symlinked as `AGENTS.md` at root) is the **vendor-agnostic single source of truth** across all AI tools.
   - Skills (`.agents/skills/`) for dialect standards, unit testing (`testing.pl`), package management (`bakage`), and version releases.

### Vendor Neutrality & Agent Configuration Rules
All AI agent instructions, rules, and skills MUST remain **100% vendor-neutral** and open-format:
- **Use Open Standards**: All guidelines MUST be authored in standard Markdown and JSON inside `.agents/` (`AGENTS.md`, `.agents/skills/<name>/SKILL.md`, `.agents/agents/<name>.md`).
- **Prohibit Vendor/IDE Lock-In Files**: Do **NOT** create proprietary, vendor-specific, or IDE-harness-specific configuration files or directories (such as `.claude/`, `.windsurfrule`, `.cursorrules`, `.github/copilot-instructions.md`, `.clinerules`, `.gemini/`, or harness-specific Emacs config snippets).
- **Universal Portability**: By storing guidelines strictly in standard `.agents/` layout, any AI coding assistant or harness (Google Antigravity, Claude Code, Cursor, Windsurf, GitHub Copilot, aidermacs/agent-shell/gptel) can natively read and apply the instructions without fragmentation.

---

## 2. Adding a New Skill

> [!NOTE]
> **Generating Skills with AI**: You can also ask your AI coding agent to write and register the skill for you rather than writing it manually (e.g. *"Create a new skill in `.agents/skills/my-skill` covering XYZ"*).

1. Create a new directory in `.agents/skills/<skill-name>/`.
2. Include a `SKILL.md` file with standard YAML frontmatter:
   ```markdown
   ---
   name: skill-name
   description: Concise description of when and why the AI should use this skill.
   ---

   # Skill Title

   Detailed instructions for the AI assistant...
   ```
3. Test skill discovery in Google Antigravity, Claude Code, or Emacs AI (`aidermacs`/`gptel`).

---

## 3. Running Tests Locally & Python Execution Rules

Python tools and tests MUST NOT leave intermediate bytecode (`__pycache__`, `.pyc`) or test cache artifacts inside the source or test directories.

Always run pytest and Python tools with `PYTHONDONTWRITEBYTECODE=1` (or `PYTHONPYCACHEPREFIX=.cache/pycache`):

```bash
# Run pytest suite without generating __pycache__ in source tree
PYTHONDONTWRITEBYTECODE=1 uv run pytest

# Test CLI commands manually
PYTHONDONTWRITEBYTECODE=1 uv run scryer-safe -g "write('Test OK'), nl, halt."
```

### Installing in Development / Editable Mode

For contributors working on the Python source code (`prolog_agent_toolkit/`), install the CLI tools locally in **editable mode** so changes to Python files take effect immediately:

```bash
uv tool install --editable . --force
```

> [!TIP]
> If you installed in non-editable mode (`uv tool install . --force`), re-run `uv tool install . --force` after modifying Python code to rebuild and update the system binaries on your `PATH`.

---

## 4. Submitting Pull Requests & Commits

- Commit messages follow Conventional Commits format (e.g. `feat(cli): add support for Ciao Prolog`, `docs(skills): update testing.pl guidelines`).
- Development takes place on branch `DEV202608`.
- Ensure all version numbers remain synchronized across `README.md`, `pyproject.toml`, and `prolog_agent_toolkit/__init__.py`.

---

## 5. Adding Support for New Prolog Engines (Mandatory Metadata & Skills Checklist)

> [!TIP]
> **Interactive Workflow Available**: You can automate and execute this onboarding process step-by-step with your AI assistant by using the [`prolog-engine-onboarding`](.agents/skills/prolog-engine-onboarding/SKILL.md) skill (e.g. *"Use `prolog-engine-onboarding` skill to guide me through adding support for GNU Prolog"*).

Whenever adding or extending support for a new Prolog engine (e.g. GNU Prolog, Ciao Prolog, SICStus, B-Prolog, ECLiPSe, etc.), you **MUST** update all of the following:

1. **Metadata & Web Annotations**:
   - `README.md`: Update OpenGraph description `<meta>`, Schema.org JSON-LD snippet `<script type="application/ld+json">`, supported engines table, CLI list, and keywords array.
   - `schema.org.jsonld`: Update `description` and `keywords` array.
   - `pyproject.toml`: Add engine keyword (e.g. `"tau-prolog"`) and script entry point (e.g. `<engine>-safe`).
2. **CLI Runner & Sandboxing**:
   - `prolog_agent_toolkit/runner.py`: Add binary mapping in `resolve_engine_binary()`.
   - `prolog_agent_toolkit/cli.py`: Add entry point function (e.g. `<engine>_safe_main()`).
   - `tests/test_runner.py`: Add unit test assertions verifying binary resolution.
3. **Coding Rules & Standards**:
   - Create `.agents/skills/<engine>-prolog-standards/SKILL.md` detailing dialect syntax, modules, string types, and constraints.
   - `.agents/AGENTS.md`: Add standard entry under **Multi-Engine Dialect Selection & Rules**.
4. **Packaging Frameworks**:
   - `.agents/skills/prolog-packaging/SKILL.md`: Document engine package manager conventions (e.g. `bakage`, `pack`, `npm`).
5. **Testing Frameworks**:
   - `.agents/skills/prolog-testing/SKILL.md`: Document assertion patterns, test runner predicates, and execution CLI options.


---

## AI Agent Contribution Protocol

AI coding agents (Google Antigravity, Claude Code, Cursor, Windsurf, Copilot, or Emacs AI tools) contributing changes to this repository MUST follow this protocol:

1. **Orientation**: Read [`AGENT_GUIDE.md`](AGENT_GUIDE.md), [`AGENTS.md`](AGENTS.md), and inspect [`AGENT_INDEX.json`](AGENT_INDEX.json) before proposing or implementing changes.
2. **Anti-Pattern Check**: Check [`docs/ANTI_PATTERNS.md`](docs/ANTI_PATTERNS.md) to ensure proposed changes do not violate purity rules or duplicate existing helpers.
3. **Execution Safety**: Execute Prolog goals via safe execution wrappers (`prolog-safe`, `scryer-safe`, `swi-safe`). Never run raw interpreter binaries.
4. **Clean Bytecode**: Always invoke Python tools with bytecode disabled (`PYTHONDONTWRITEBYTECODE=1 uv run pytest`).
5. **Skill Validation**: When adding or modifying skills in [`.agents/skills/`](.agents/skills/), run `prolog-agent validate-skills` to ensure YAML frontmatter compliance.
6. **Version Parity**: When modifying version numbers, edit [`pyproject.toml`](pyproject.toml) as canonical source of truth and run `prolog-agent release`. Run `prolog-agent check-version` to verify parity.
7. **Portable Hyperlinks**: Avoid absolute `file://` hyperlinks. Use relative Markdown links for local workspace files. If a `file://` link was authored by a human contributor, ask them if they want to fix it first before replacing it.
