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

    print(f"Project '{project_name}' successfully initialized!")
    return 0
