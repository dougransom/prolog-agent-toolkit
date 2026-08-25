import sys
import os

sys.dont_write_bytecode = True
os.environ["PYTHONDONTWRITEBYTECODE"] = "1"

from prolog_agent_toolkit.runner import run_prolog_safe



def prolog_safe_main() -> None:
    """CLI entry point for prolog-safe."""
    exit_code = run_prolog_safe(sys.argv[1:])
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


if __name__ == "__main__":
    prolog_safe_main()
