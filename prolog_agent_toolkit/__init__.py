import sys
import os
from importlib.metadata import version, PackageNotFoundError

sys.dont_write_bytecode = True
os.environ["PYTHONDONTWRITEBYTECODE"] = "1"

"""Prolog Agent Toolkit package."""

try:
    __version__ = version("prolog-agent-toolkit")
except PackageNotFoundError:
    __version__ = "0.0.1.dev3"
