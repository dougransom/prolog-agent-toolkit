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
        with open(readme_path, "w", encoding="utf-8") as f:
            f.write(f"# {project_name}\n\n")
            f.write(f"Prolog project `{project_name}` initialized for engine `{engine}` using `prolog-agent-toolkit`.\n\n")
            f.write("## Running Tests\n\n")
            if engine == "swi":
                f.write("Run unit tests with `swi-safe`:\n```bash\nswi-safe -g \"run_tests,halt\" tests/test_" + project_name + ".pl\n```\n\n")
            else:
                f.write("Run unit tests with `scryer-safe` or `prolog-safe`:\n```bash\nscryer-safe tests/testing.pl\n```\n\n")
            f.write("## Using Safe Runners\n\n")
            f.write("Always execute Prolog code using cross-platform safety runners:\n")
            f.write("- `prolog-safe`\n- `scryer-safe`\n- `swi-safe`\n- `trealla-safe`\n- `tau-safe`\n\n")
            f.write("## Agent Skills & Dialect Standards\n\n")
            f.write("Link the toolkit's agent skills:\n```bash\nln -s ~/code/prolog-agent-toolkit/.agents .agents\n```\n")

    # 6. CHANGELOG.md creation
    changelog_path = os.path.join(project_dir, "CHANGELOG.md")
    if not os.path.exists(changelog_path):
        with open(changelog_path, "w", encoding="utf-8") as f:
            f.write("# Changelog\n\nAll notable changes will be documented in this file.\n")

    print(f"Project '{project_name}' successfully initialized!")
    return 0


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

