# Contributing to Prolog Agent Toolkit

Thank you for contributing to the **Prolog Agent Toolkit**! We welcome contributions for adding new engine safety wrappers, extending AI agent skills, and improving ISO Prolog guidelines.

---

## 1. Project Architecture

The toolkit consists of two primary layers:

1. **Python Execution Safety CLI** (`prolog_agent_toolkit/`):
   - Cross-platform resource sandboxing, execution timeout monitoring, low-CPU scheduling, and RAM limits.
   - Entry points: `prolog-safe`, `scryer-safe`, `swi-safe`, `trealla-safe`.
2. **AI Agent Customizations** (`.agents/`):
   - Rules (`.agents/AGENTS.md`, `.agents/references/`) defining ISO Prolog coding standards.
   - Skills (`.agents/skills/`) for dialect standards, unit testing (`testing.pl`), package management (`bakage`), and version releases.

---

## 2. Adding a New Skill

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
3. Test skill discovery in Google Antigravity or Claude Code.

---

## 3. Running Tests Locally

Use `uv` to run pytest suite for CLI wrappers:

```bash
# Run pytest suite
uv run pytest

# Test CLI commands manually
uv run scryer-safe -g "write('Test OK'), nl, halt."
```

---

## 4. Submitting Pull Requests & Commits

- Commit messages follow Conventional Commits format (e.g. `feat(cli): add support for Ciao Prolog`, `docs(skills): update testing.pl guidelines`).
- Development takes place on branch `DEV202608`.
- Ensure all version numbers remain synchronized across `README.md`, `pyproject.toml`, and `prolog_agent_toolkit/__init__.py`.
