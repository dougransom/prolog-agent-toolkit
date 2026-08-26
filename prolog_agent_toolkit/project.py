import os
import sys

sys.dont_write_bytecode = True
os.environ["PYTHONDONTWRITEBYTECODE"] = "1"


def init_project(project_name: str, engine: str = "scryer", base_dir: str = ".") -> int:
    """
    Initialize a new Prolog project directory structure, manifest, starter module,
    testing scaffolding, README, and agent rules/skills symlink instructions.
    """
    engine = (engine or "scryer").lower()
    project_dir = os.path.abspath(os.path.join(base_dir, project_name))

    print(f"Initializing Prolog project '{project_name}' (Engine: {engine}) in {project_dir}...")

    src_dir = os.path.join(project_dir, "src")
    tests_dir = os.path.join(project_dir, "tests")

    os.makedirs(src_dir, exist_ok=True)
    os.makedirs(tests_dir, exist_ok=True)

    # 1. Manifest file creation
    if engine in ("scryer", "iso", "trealla"):
        bakage_path = os.path.join(project_dir, "bakage.toml")
        if not os.path.exists(bakage_path):
            with open(bakage_path, "w", encoding="utf-8") as f:
                f.write(f'name = "{project_name}"\n')
                f.write('version = "0.1.0"\n')
                f.write(f'modules = ["src/{project_name}.pl"]\n')
                f.write('requires = []\n')

        pack_path = os.path.join(project_dir, "pack.pl")
        if not os.path.exists(pack_path):
            with open(pack_path, "w", encoding="utf-8") as f:
                f.write(f"name({project_name}).\n")
                f.write("version('0.1.0').\n")
                f.write(f'title("{project_name} Prolog library").\n')
                f.write('author("Developer").\n')

    elif engine == "swi":
        pack_path = os.path.join(project_dir, "pack.pl")
        if not os.path.exists(pack_path):
            with open(pack_path, "w", encoding="utf-8") as f:
                f.write(f"name('{project_name}').\n")
                f.write("version('0.1.0').\n")
                f.write(f"title('{project_name} SWI-Prolog library').\n")
                f.write("keywords(['prolog']).\n")
                f.write("author('Developer', 'dev@example.com').\n")

    elif engine == "tau":
        pkg_path = os.path.join(project_dir, "package.json")
        if not os.path.exists(pkg_path):
            with open(pkg_path, "w", encoding="utf-8") as f:
                f.write("{\n")
                f.write(f'  "name": "{project_name}",\n')
                f.write('  "version": "0.1.0",\n')
                f.write(f'  "description": "{project_name} Tau Prolog application",\n')
                f.write(f'  "main": "src/{project_name}.pl",\n')
                f.write('  "dependencies": {\n')
                f.write('    "tau-prolog": "^0.3.4"\n')
                f.write('  }\n')
                f.write("}\n")

    # 2. Starter module src/<project-name>.pl
    module_path = os.path.join(src_dir, f"{project_name}.pl")
    if not os.path.exists(module_path):
        with open(module_path, "w", encoding="utf-8") as f:
            f.write(f":- module({project_name}, [\n")
            f.write("    hello/1\n")
            f.write("]).\n\n")
            if engine in ("scryer", "trealla", "iso"):
                f.write(":- use_module(library(charsio)).\n")
                f.write(":- use_module(library(dcgs)).\n\n")
            f.write("%%\thello(-Greeting:chars) is det.\n")
            f.write("%\tGenerates standard greeting string.\n")
            f.write(f'hello("Hello from {project_name}!").\n')

    # 3. Testing scaffolding
    if engine == "swi":
        test_path = os.path.join(tests_dir, f"test_{project_name}.pl")
        if not os.path.exists(test_path):
            with open(test_path, "w", encoding="utf-8") as f:
                f.write(":- use_module(library(plunit)).\n")
                f.write(f":- use_module('../src/{project_name}.pl').\n\n")
                f.write(f":- begin_tests({project_name}).\n\n")
                f.write("test(hello) :-\n")
                f.write("    hello(_Greeting).\n\n")
                f.write(f":- end_tests({project_name}).\n")
    else:
        test_path = os.path.join(tests_dir, "testing.pl")
        if not os.path.exists(test_path):
            with open(test_path, "w", encoding="utf-8") as f:
                f.write(":- use_module(library(format)).\n")
                f.write(f":- use_module('../src/{project_name}.pl').\n\n")
                f.write(":- initialization(run_tests).\n\n")
                f.write("run_tests :-\n")
                f.write("    hello(Msg),\n")
                f.write('    format("Test hello/1 passed: ~s~n", [Msg]).\n')

    # 4. Agent skills directory setup / symlink instructions
    agents_dir = os.path.join(project_dir, ".agents")
    global_agents = os.path.expanduser("~/code/prolog-agent-toolkit/.agents")
    if not os.path.exists(agents_dir):
        if os.path.exists(global_agents):
            try:
                os.symlink(global_agents, agents_dir)
            except OSError:
                pass

    # 5. README.md creation
    readme_path = os.path.join(project_dir, "README.md")
    if not os.path.exists(readme_path):
        from prolog_agent_toolkit import get_version
        toolkit_ver = get_version()
        readme_content = generate_readme_content(project_name, engine=engine, version=toolkit_ver)
        with open(readme_path, "w", encoding="utf-8") as f:
            f.write(readme_content)

    # 6. CHANGELOG.md creation
    changelog_path = os.path.join(project_dir, "CHANGELOG.md")
    if not os.path.exists(changelog_path):
        with open(changelog_path, "w", encoding="utf-8") as f:
            f.write("# Changelog\n\nAll notable changes will be documented in this file.\n")

    print(f"Project '{project_name}' successfully initialized!")
    return 0


def generate_readme_content(project_name: str, engine: str = "scryer", version: str = "0.0.1.dev6") -> str:
    """
    Generate a complete, opinionated README.md for a new Prolog project.
    """
    engine = (engine or "scryer").lower()

    dialect_names = {
        "scryer": "Scryer Prolog (ISO-compliant)",
        "swi": "SWI-Prolog",
        "trealla": "Trealla Prolog",
        "tau": "Tau Prolog",
        "iso": "ISO Standard Prolog",
    }
    dialect_name = dialect_names.get(engine, f"{engine.capitalize()} Prolog")

    dialect_descriptions = {
        "scryer": "Adheres strictly to ISO/IEC 13211-1 standard purity. Enforces `chars` double-quoted strings, pure reified logic (`library(reif)`), pure DCGs (`library(dcgs)`), integer constraints (`library(clpz)`), and side-effect-free type inspection (`library(si)`).",
        "swi": "Features extensive developer tooling, module system, SWI dicts and string types, unit testing via `plunit`, and integer constraints (`library(clpfd)`).",
        "trealla": "High-performance ISO-compliant Prolog engine designed for fast parsing, modularity, dynamic foreign function interfaces, and WebAssembly (WASM) embedding.",
        "tau": "ISO-compliant Prolog engine written in JavaScript for seamless browser DOM integration (`library(dom)`), Node.js scripting, and web application embedding.",
        "iso": "Engine-agnostic ISO standard Prolog baseline compatible across all conforming implementations.",
    }
    dialect_desc = dialect_descriptions.get(engine, "Standard Prolog dialect.")

    dialect_skills = {
        "scryer": "`.agents/skills/scryer-prolog-standards/SKILL.md` and `.agents/skills/prolog-conventions/SKILL.md`",
        "swi": "`.agents/skills/swi-prolog-standards/SKILL.md` and `.agents/skills/prolog-conventions/SKILL.md`",
        "trealla": "`.agents/skills/trealla-prolog-standards/SKILL.md` and `.agents/skills/prolog-conventions/SKILL.md`",
        "tau": "`.agents/skills/tau-prolog-standards/SKILL.md` and `.agents/skills/prolog-conventions/SKILL.md`",
        "iso": "`.agents/skills/prolog-conventions/SKILL.md`",
    }
    skill_ref = dialect_skills.get(engine, "`.agents/skills/prolog-conventions/SKILL.md`")

    safe_runner_cmd = {
        "scryer": f"scryer-safe -g \"use_module('src/{project_name}.pl'), hello(M), write(M), nl, halt.\"",
        "swi": f"swi-safe -g \"use_module('src/{project_name}.pl'), hello(M), writeln(M), halt.\"",
        "trealla": f"trealla-safe -g \"use_module('src/{project_name}.pl'), hello(M), write(M), nl, halt.\"",
        "tau": f"tau-safe -g \"use_module('src/{project_name}.pl'), hello(M), write(M), nl, halt.\"",
    }.get(engine, f"prolog-safe -g \"use_module('src/{project_name}.pl'), hello(M), write(M), nl, halt.\"")

    test_cmd = {
        "swi": f"swi-safe -g \"run_tests,halt\" tests/test_{project_name}.pl",
    }.get(engine, "scryer-safe tests/testing.pl")

    manifest_file = "pack.pl" if engine == "swi" else ("package.json" if engine == "tau" else "bakage.toml")

    manifest_desc = {
        "scryer": "`bakage.toml`: Scryer Prolog `bakage` manifest defining module exports and dependencies (alongside `pack.pl`).",
        "swi": "`pack.pl`: SWI-Prolog package manager manifest for dependency installation via `pack_install`.",
        "trealla": "`pack.pl`: Manifest metadata file (or standalone ISO files).",
        "tau": "`package.json`: Node.js / npm package manifest declaring `tau-prolog` dependencies.",
    }.get(engine, f"`{manifest_file}`: Packaging manifest file.")

    test_file_name = f"test_{project_name}.pl" if engine == "swi" else "testing.pl"

    if engine == "swi":
        test_example = f"""```prolog
:- use_module(library(plunit)).
:- use_module('../src/{project_name}.pl').

:- begin_tests({project_name}).

test(hello) :-
    hello(Msg),
    assertion(Msg \\== []).

test(parse_item) :-
    phrase(parse_item("item1"), "[item1]").

:- end_tests({project_name}).
```"""
    else:
        test_example = f"""```prolog
:- use_module(library(format)).
:- use_module(library(dcgs)).
:- use_module('../src/{project_name}.pl').

:- initialization(run_tests).

must_succeed(Goal) :-
    (   call(Goal) ->
        format("PASS: ~q~n", [Goal])
    ;   format("FAIL: ~q~n", [Goal]),
        halt(1)
    ).

run_tests :-
    format("Running {project_name} Test Suite...~n~n", []),
    must_succeed(hello(_Greeting)),
    must_succeed(phrase(parse_item("test"), "[test]")),
    format("~nAll tests passed successfully!~n", []).
```"""

    return f"""# {project_name}

> Powered by [prolog-agent-toolkit](https://github.com/dougransom/prolog-agent-toolkit) **v{version}**

A modern Prolog project configured for deterministic execution, engine safety, and automated AI agent collaboration.

---

## 1. Project Overview

This project uses **`prolog-agent-toolkit` (v{version})**.

The `prolog-agent-toolkit` provides a standardized development environment for writing safe, pure, high-quality Prolog software. Its primary capabilities include:

- **Deterministic Safe Runners**: Cross-platform command-line entry points (`scryer-safe`, `swi-safe`, `trealla-safe`, `tau-safe`, `prolog-safe`) that run Prolog execution under strict CPU and memory resource limits.
- **Dialect Standards & Purity**: Enforced coding guidelines, Covington style standards, reified logical predicates (`if_/3`, `dif/2`), pure DCGs, and CLP constraint logic.
- **Agent Skill Architecture**: Integrated `.agents/` directory providing structured skills and linting rules so AI assistants (e.g. Gemini, Cursor, Claude, Copilot) generate pure, idiomatic code.
- **Multi-Engine Support**: Seamless portability across ISO-compliant engines (Scryer Prolog, SWI-Prolog, Trealla Prolog, Tau Prolog).

---

## 2. Directory Layout

Recommended project structure:

```text
{project_name}/
├── src/
│   └── {project_name}.pl      # Main module source file
├── tests/
│   └── {test_file_name}         # Unit test suite
├── .agents -> /path/to/prolog-agent-toolkit/.agents # Symlink to shared agent skills & rules
├── {manifest_file}              # Packaging manifest
├── CHANGELOG.md               # Version release history
└── README.md                  # Developer & AI agent onboarding guide
```

### Directory Roles

- **`src/`**: Houses application and library Prolog source files. Modules explicitly declare exports and follow pure ISO standards.
- **`tests/`**: Contains unit test harnesses and test cases.
- **`.agents/`**: Workspace symlink pointing to the shared `prolog-agent-toolkit/.agents` directory. Gives AI coding agents immediate access to project guidelines, dialect rules, refactoring subagents, and linter specifications.
- **`{manifest_file}`**: {manifest_desc}
- **`README.md`**: Canonical onboarding document for developers and AI agents.

---

## 3. Dialect Selection

This project is configured to use **{dialect_name}**.

### Dialect Overview
{dialect_desc}

### Dialect Standards Reference
When writing code or directing AI agents, consult the dialect standards provided by the toolkit:
- **Primary Dialect Skill**: {skill_ref}
- **Universal Style Guide**: `.agents/references/covington_style.md`
- **Purity Guidelines**: `.agents/references/prolog_guidelines.md`

---

## 4. Safe Runners

All Prolog executions **MUST** use the safe runner entry points provided by `prolog-agent-toolkit`. Developers and AI agents MUST NEVER invoke raw binary interpreters directly (e.g. `scryer-prolog`, `swipl`, `tpl`).

### Executing Code

```bash
# Run goal safely using the target runner:
{safe_runner_cmd}

# Run using generic wrapper (select engine via environment variable):
export PROLOG_ENGINE={engine}
prolog-safe -g "hello(M), write(M), nl, halt." src/{project_name}.pl
```

### Why Safe Runners Are Required

1. **Resource Sandboxing**: Prevents non-terminating recursive searches or infinite choice-point backtracking loops from locking up CPU cores or exhausting system memory.
2. **Environment Determinism**: Standardizes standard library module imports, string encoding, and error reporting across environments.
3. **Execution Safety**: Enforces safety policies required for agent-driven autonomous execution.

---

## 5. Agent Skills Architecture

The `.agents/` directory connects this repository to the `prolog-agent-toolkit` knowledge base.

### How `.agents` Is Used
- **Shared via Symlink**: Link the toolkit's `.agents` directory during workspace setup:
  ```bash
  ln -s ~/code/prolog-agent-toolkit/.agents .agents
  ```
- **Deterministic Assistant Behavior**: When an AI coding assistant operates in this project, it automatically reads `.agents/AGENTS.md` and active skills to enforce pure Prolog standards, first-argument indexing, and Covington styling.
- **Modular Capabilities**: Exposes automated skills for static analysis, unit test generation, DCG mastery, CLP constraints, and release management.

---

## 6. Testing

### Running Tests

Execute the unit test suite using the appropriate safe runner:

```bash
{test_cmd}
```

### Test Suite Example (`tests/{test_file_name}`)

{test_example}
"""


def generate_module(module_name: str, engine: str = "scryer", output_dir: str = "src") -> int:
    """
    Generate a new dialect-aware Prolog module stub with Covington headers, DCGs, and CLP constraints.
    """
    engine = (engine or "scryer").lower()
    os.makedirs(output_dir, exist_ok=True)
    target_file = os.path.join(output_dir, f"{module_name}.pl")

    print(f"Generating Prolog module '{module_name}' (Engine: {engine}) at {target_file}...")

    if engine == "swi":
        decl = f":- module({module_name}, [\n    hello/1,\n    parse_item//1,\n    solve_range/2\n]).\n"
        imports = ":- use_module(library(clpfd)).\n"
    elif engine == "trealla":
        decl = f"% Trealla Prolog Module: {module_name}\n"
        imports = ":- use_module(library(charsio)).\n:- use_module(library(dcgs)).\n"
    else:
        decl = f":- module({module_name}, [\n    hello/1,\n    parse_item//1,\n    solve_range/2\n]).\n"
        imports = (
            ":- use_module(library(charsio)).\n"
            ":- use_module(library(dcgs)).\n"
            ":- use_module(library(clpz)).\n"
            ":- use_module(library(reif)).\n"
        )

    content = (
        f"{decl}\n{imports}\n"
        f"%%\thello(-Greeting:chars) is det.\n"
        f"%\tGenerates a standard greeting string for {module_name}.\n"
        f'hello("Hello from {module_name}!").\n\n'
        f"%%\tparse_item(-Item:chars)// is det.\n"
        f"%\tDefinite Clause Grammar (DCG) rule to parse an item tag.\n"
        f'parse_item(Item) -->\n    "[", Item, "]".\n\n'
        f"%%\tsolve_range(+Limit:integer, -Value:integer) is semidet.\n"
        f"%\tCLP(Z)/CLP(FD) integer constraint example.\n"
        f"solve_range(Limit, Value) :-\n"
        f"    Value #>= 0,\n"
        f"    Value #=< Limit,\n"
        f"    Value #= Limit - 1.\n"
    )

    with open(target_file, "w", encoding="utf-8") as f:
        f.write(content)

    print(f"Module '{module_name}' generated successfully at {target_file}.")
    return 0


def generate_template(project_name: str, engine: str = "scryer", base_dir: str = ".") -> int:
    """
    Generate canonical, deterministic project template layout.
    """
    return init_project(project_name, engine=engine, base_dir=base_dir)


def print_init_script() -> int:
    """
    Output the POSIX bash initializer script specification to stdout.
    """
    script_path = os.path.join(os.path.dirname(__file__), "..", "scripts", "prolog_agent_init.sh")
    if os.path.exists(script_path):
        with open(script_path, "r", encoding="utf-8") as f:
            print(f.read())
    else:
        print("#!/usr/bin/env bash")
        print("# Prolog Agent Toolkit — Initializer Script")
        print("echo 'Initializing project...'")
    return 0

