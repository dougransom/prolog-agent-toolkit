import sys
import os

sys.dont_write_bytecode = True
os.environ["PYTHONDONTWRITEBYTECODE"] = "1"

from prolog_agent_toolkit.runner import run_prolog_safe
from prolog_agent_toolkit.skill_validator import validate_skills_cli


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
    prolog_safe_main()

