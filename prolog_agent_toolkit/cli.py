import sys
import os

sys.dont_write_bytecode = True
os.environ["PYTHONDONTWRITEBYTECODE"] = "1"

from prolog_agent_toolkit.runner import run_prolog_safe
from prolog_agent_toolkit.skill_validator import validate_skills_cli
from prolog_agent_toolkit.project import init_project
from prolog_agent_toolkit.release import run_release


def list_subagents(agents_dir: str = ".agents/agents") -> None:
    """Scan and list available autonomous subagents in the toolkit."""
    if not os.path.exists(agents_dir):
        sys.stderr.write(f"Agents directory '{agents_dir}' not found.\n")
        sys.exit(1)

    print("==================================================================")
    print("PROLOG AGENT TOOLKIT - AVAILABLE AUTONOMOUS SUBAGENTS")
    print("==================================================================")
    subagents = [f for f in os.listdir(agents_dir) if f.endswith(".md")]
    subagents.sort()

    for agent_file in subagents:
        path = os.path.join(agents_dir, agent_file)
        name = agent_file[:-3]
        first_line = ""
        with open(path, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if line.startswith("#"):
                    first_line = line.lstrip("#").strip()
                    break
        print(f"• {name:<35} | {first_line or 'Prolog Subagent'}")
        print(f"  File: {path}\n")


def prolog_agent_main() -> None:
    """CLI entry point for prolog-agent."""
    args = sys.argv[1:]
    if not args or args[0] in ("-h", "--help", "help"):
        print("Prolog Agent Toolkit CLI")
        print("Usage:")
        print("  prolog-agent init <project-name> [--engine scryer|swi|trealla|tau|iso]")
        print("  prolog-agent release [--version X.Y.Z]")
        print("  prolog-agent list-subagents")
        print("  prolog-agent validate-skills")
        sys.exit(0)

    cmd = args[0]
    if cmd == "init":
        if len(args) < 2:
            sys.stderr.write("Error: Missing project name for prolog-agent init.\n")
            sys.stderr.write("Usage: prolog-agent init <project-name> [--engine scryer|swi|trealla|tau|iso]\n")
            sys.exit(1)
        project_name = args[1]
        engine = "scryer"
        if "--engine" in args:
            idx = args.index("--engine")
            if idx + 1 < len(args):
                engine = args[idx + 1]
        exit_code = init_project(project_name, engine=engine)
        sys.exit(exit_code)

    elif cmd == "release":
        version = None
        if "--version" in args:
            idx = args.index("--version")
            if idx + 1 < len(args):
                version = args[idx + 1]
        exit_code = run_release(new_version=version)
        sys.exit(exit_code)

    elif cmd == "list-subagents":
        list_subagents()
        sys.exit(0)

    elif cmd == "validate-skills":
        exit_code = validate_skills_cli()
        sys.exit(exit_code)

    else:
        sys.stderr.write(f"Unknown command: {cmd}\n")
        sys.exit(1)


def prolog_safe_main() -> None:
    """CLI entry point for prolog-safe."""
    if "--list-subagents" in sys.argv:
        list_subagents()
        sys.exit(0)
    exit_code = run_prolog_safe(sys.argv[1:])
    sys.exit(exit_code)


def validate_skills_main() -> None:
    """CLI entry point for prolog-validate-skills."""
    exit_code = validate_skills_cli()
    sys.exit(exit_code)


def scryer_safe_main() -> None:
    """CLI entry point for scryer-safe."""
    os.environ["PROLOG_ENGINE"] = "scryer"
    exit_code = run_prolog_safe(sys.argv[1:], default_engine="scryer")
    sys.exit(exit_code)


def swi_safe_main() -> None:
    """CLI entry point for swi-safe."""
    os.environ["PROLOG_ENGINE"] = "swi"
    exit_code = run_prolog_safe(sys.argv[1:], default_engine="swi")
    sys.exit(exit_code)


def trealla_safe_main() -> None:
    """CLI entry point for trealla-safe."""
    os.environ["PROLOG_ENGINE"] = "trealla"
    exit_code = run_prolog_safe(sys.argv[1:], default_engine="trealla")
    sys.exit(exit_code)


def tau_safe_main() -> None:
    """CLI entry point for tau-safe."""
    os.environ["PROLOG_ENGINE"] = "tau"
    exit_code = run_prolog_safe(sys.argv[1:], default_engine="tau")
    sys.exit(exit_code)


if __name__ == "__main__":
    prolog_agent_main()


