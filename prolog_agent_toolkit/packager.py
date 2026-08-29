import os
import sys
import tarfile
import zipfile
import re
import json

sys.dont_write_bytecode = True
os.environ["PYTHONDONTWRITEBYTECODE"] = "1"

try:
    import tomllib  # Python 3.11+
except ImportError:
    try:
        import tomli as tomllib  # Fallback for older python
    except ImportError:
        tomllib = None


def parse_bakage_toml(filepath: str) -> dict:
    """Parse bakage.toml file for package metadata."""
    metadata = {}
    if not os.path.exists(filepath):
        return metadata

    if tomllib is not None:
        try:
            with open(filepath, "rb") as f:
                data = tomllib.load(f)
                metadata["name"] = data.get("name")
                metadata["version"] = data.get("version")
                metadata["modules"] = data.get("modules", [])
                metadata["requires"] = data.get("requires", [])
                return metadata
        except Exception:
            pass

    # Basic regex fallback if tomllib/tomli not available
    with open(filepath, "r", encoding="utf-8") as f:
        content = f.read()

    name_m = re.search(r'name\s*=\s*["\']([^"\']+)["\']', content)
    ver_m = re.search(r'version\s*=\s*["\']([^"\']+)["\']', content)

    if name_m:
        metadata["name"] = name_m.group(1)
    if ver_m:
        metadata["version"] = ver_m.group(1)

    return metadata


def parse_pack_pl(filepath: str) -> dict:
    """Parse SWI/Scryer pack.pl for metadata."""
    metadata = {}
    if not os.path.exists(filepath):
        return metadata

    with open(filepath, "r", encoding="utf-8") as f:
        content = f.read()

    name_m = re.search(r"name\(\s*['\"]?([a-zA-Z0-9_\-]+)['\"]?\s*\)", content)
    ver_m = re.search(r"version\(\s*['\"]?([a-zA-Z0-9_\-\.]+)['\"]?\s*\)", content)

    if name_m:
        metadata["name"] = name_m.group(1)
    if ver_m:
        metadata["version"] = ver_m.group(1)

    return metadata


def parse_package_json(filepath: str) -> dict:
    """Parse package.json for Tau Prolog metadata."""
    metadata = {}
    if not os.path.exists(filepath):
        return metadata

    try:
        with open(filepath, "r", encoding="utf-8") as f:
            data = json.load(f)
            metadata["name"] = data.get("name")
            metadata["version"] = data.get("version")
    except Exception:
        pass

    return metadata


def build_package(target_dir: str = ".", engine: str = "scryer", out_dir: str = "dist") -> int:
    """
    Validate manifest and build distribution archive for Prolog package.
    """
    target_dir = os.path.abspath(target_dir)
    engine = (engine or "scryer").lower()

    bakage_toml = os.path.join(target_dir, "bakage.toml")
    pack_pl = os.path.join(target_dir, "pack.pl")
    package_json = os.path.join(target_dir, "package.json")

    metadata = {}
    manifest_type = None

    if engine in ("scryer", "iso", "trealla"):
        if os.path.exists(bakage_toml):
            metadata = parse_bakage_toml(bakage_toml)
            manifest_type = "bakage.toml"
        elif os.path.exists(pack_pl):
            metadata = parse_pack_pl(pack_pl)
            manifest_type = "pack.pl"
    elif engine == "swi":
        if os.path.exists(pack_pl):
            metadata = parse_pack_pl(pack_pl)
            manifest_type = "pack.pl"
    elif engine == "tau":
        if os.path.exists(package_json):
            metadata = parse_package_json(package_json)
            manifest_type = "package.json"

    # General fallback
    if not metadata.get("name"):
        if os.path.exists(bakage_toml):
            metadata = parse_bakage_toml(bakage_toml)
            manifest_type = "bakage.toml"
        elif os.path.exists(pack_pl):
            metadata = parse_pack_pl(pack_pl)
            manifest_type = "pack.pl"

    pkg_name = metadata.get("name") or os.path.basename(target_dir)
    pkg_ver = metadata.get("version") or "0.1.0"

    print(f"=== Prolog Agent Packager ===")
    print(f"Engine Target: {engine}")
    print(f"Manifest File: {manifest_type or 'None found'}")
    print(f"Package Name : {pkg_name}")
    print(f"Package Vers : {pkg_ver}")

    # Validate modules if specified in bakage.toml
    modules = metadata.get("modules", [])
    for mod in modules:
        mod_path = os.path.join(target_dir, mod)
        if not os.path.exists(mod_path):
            sys.stderr.write(f"Warning: Declared module file '{mod}' in bakage.toml not found at {mod_path}\n")

    dist_path = os.path.join(target_dir, out_dir)
    os.makedirs(dist_path, exist_ok=True)

    archive_base = f"{pkg_name}-{pkg_ver}-{engine}"

    def should_include(rel_path: str) -> bool:
        parts = rel_path.split(os.sep)
        ignore_dirs = {".git", ".cache", "__pycache__", ".venv", ".pytest_cache", "dist", "node_modules"}
        if any(p in ignore_dirs for p in parts):
            return False
        if rel_path.endswith((".pyc", ".pyo", ".swp", ".tmp")):
            return False
        return True

    if engine == "swi":
        archive_name = f"{archive_base}.zip"
        archive_file = os.path.join(dist_path, archive_name)
        print(f"Building SWI pack zip archive: {archive_file}...")
        with zipfile.ZipFile(archive_file, "w", zipfile.ZIP_DEFLATED) as zf:
            for root, dirs, files in os.walk(target_dir):
                dirs[:] = [d for d in dirs if d not in {".git", ".cache", "__pycache__", ".venv", "dist", "node_modules"}]
                for file in files:
                    full_path = os.path.join(root, file)
                    rel_path = os.path.relpath(full_path, target_dir)
                    if should_include(rel_path):
                        arcname = os.path.join(f"{pkg_name}-{pkg_ver}", rel_path)
                        zf.write(full_path, arcname)
    else:
        archive_name = f"{archive_base}.tar.gz"
        archive_file = os.path.join(dist_path, archive_name)
        print(f"Building Scryer/ISO bakage tar.gz archive: {archive_file}...")
        with tarfile.open(archive_file, "w:gz") as tar:
            for root, dirs, files in os.walk(target_dir):
                dirs[:] = [d for d in dirs if d not in {".git", ".cache", "__pycache__", ".venv", "dist", "node_modules"}]
                for file in files:
                    full_path = os.path.join(root, file)
                    rel_path = os.path.relpath(full_path, target_dir)
                    if should_include(rel_path):
                        arcname = os.path.join(f"{pkg_name}-{pkg_ver}", rel_path)
                        tar.add(full_path, arcname=arcname)

    print(f"Package successfully built at: {archive_file}")
    return 0
