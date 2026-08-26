import sys
import os
from importlib.metadata import version, PackageNotFoundError

sys.dont_write_bytecode = True
os.environ["PYTHONDONTWRITEBYTECODE"] = "1"

"""Prolog Agent Toolkit package."""


def get_version() -> str:
    """Dynamically resolve package version from metadata or pyproject.toml as source of truth."""
    try:
        return version("prolog-agent-toolkit")
    except PackageNotFoundError:
        pyproject_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "pyproject.toml")
        if os.path.exists(pyproject_path):
            if sys.version_info >= (3, 11):
                import tomllib
                with open(pyproject_path, "rb") as f:
                    data = tomllib.load(f)
                    return data.get("project", {}).get("version", "0.0.1")
            else:
                import re
                with open(pyproject_path, "r", encoding="utf-8") as f:
                    content = f.read()
                m = re.search(r'version\s*=\s*["\']([^"\']+)["\']', content)
                if m:
                    return m.group(1)
        return "0.0.1"


__version__ = get_version()
