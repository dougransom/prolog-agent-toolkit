import os
import sys
import tarfile
import zipfile
import re
import json
from typing import Dict, List, Optional, Protocol, Tuple, Callable

sys.dont_write_bytecode = True
os.environ["PYTHONDONTWRITEBYTECODE"] = "1"


# --- Abstract Protocols / Interfaces ---

class ManifestParser(Protocol):
    manifest_name: str

    def parse_content(self, content: str) -> Dict[str, str]: ...
    def parse_file(self, filepath: str) -> Dict[str, str]: ...


class ArchiveWriter(Protocol):
    extension: str

    def write_archive(
        self,
        target_dir: str,
        archive_path: str,
        pkg_name: str,
        pkg_ver: str,
        filter_fn: Optional[Callable[[str], bool]] = None
    ) -> None: ...


# --- Concrete Manifest Parsers ---

class ScryerManifestParser:
    manifest_name = "scryer-manifest.pl"

    def parse_content(self, content: str) -> Dict[str, str]:
        metadata = {}
        name_m = re.search(r"name\(\s*[\"\']?([a-zA-Z0-9_\-]+)[\"\']?\s*\)", content)
        ver_m = re.search(r"version\(\s*[\"\']?([a-zA-Z0-9_\-\.]+)[\"\']?\s*\)", content)
        main_m = re.search(r"main_file\(\s*[\"\']?([^\"\']+)[\"\']?\s*\)", content)

        if name_m:
            metadata["name"] = name_m.group(1)
        if ver_m:
            metadata["version"] = ver_m.group(1)
        if main_m:
            metadata["main_file"] = main_m.group(1)

        return metadata

    def parse_file(self, filepath: str) -> Dict[str, str]:
        if not os.path.exists(filepath):
            return {}
        with open(filepath, "r", encoding="utf-8") as f:
            return self.parse_content(f.read())


class SwiPackParser:
    manifest_name = "pack.pl"

    def parse_content(self, content: str) -> Dict[str, str]:
        metadata = {}
        name_m = re.search(r"name\(\s*['\"]?([a-zA-Z0-9_\-]+)['\"]?\s*\)", content)
        ver_m = re.search(r"version\(\s*['\"]?([a-zA-Z0-9_\-\.]+)['\"]?\s*\)", content)

        if name_m:
            metadata["name"] = name_m.group(1)
        if ver_m:
            metadata["version"] = ver_m.group(1)

        return metadata

    def parse_file(self, filepath: str) -> Dict[str, str]:
        if not os.path.exists(filepath):
            return {}
        with open(filepath, "r", encoding="utf-8") as f:
            return self.parse_content(f.read())


class TauJsonParser:
    manifest_name = "package.json"

    def parse_content(self, content: str) -> Dict[str, str]:
        metadata = {}
        try:
            data = json.loads(content)
            metadata["name"] = data.get("name")
            metadata["version"] = data.get("version")
        except Exception:
            pass
        return metadata

    def parse_file(self, filepath: str) -> Dict[str, str]:
        if not os.path.exists(filepath):
            return {}
        try:
            with open(filepath, "r", encoding="utf-8") as f:
                return self.parse_content(f.read())
        except Exception:
            return {}


# --- Concrete Archive Writers ---

class TarGzArchiveWriter:
    extension = "tar.gz"

    def write_archive(
        self,
        target_dir: str,
        archive_path: str,
        pkg_name: str,
        pkg_ver: str,
        filter_fn: Optional[Callable[[str], bool]] = None
    ) -> None:
        with tarfile.open(archive_path, "w:gz") as tar:
            for root, dirs, files in os.walk(target_dir):
                dirs[:] = [d for d in dirs if d not in {".git", ".cache", "__pycache__", ".venv", "dist", "node_modules"}]
                for file in files:
                    full_path = os.path.join(root, file)
                    rel_path = os.path.relpath(full_path, target_dir)
                    if filter_fn is None or filter_fn(rel_path):
                        arcname = os.path.join(f"{pkg_name}-{pkg_ver}", rel_path)
                        tar.add(full_path, arcname=arcname)


class ZipArchiveWriter:
    extension = "zip"

    def write_archive(
        self,
        target_dir: str,
        archive_path: str,
        pkg_name: str,
        pkg_ver: str,
        filter_fn: Optional[Callable[[str], bool]] = None
    ) -> None:
        with zipfile.ZipFile(archive_path, "w", zipfile.ZIP_DEFLATED) as zf:
            for root, dirs, files in os.walk(target_dir):
                dirs[:] = [d for d in dirs if d not in {".git", ".cache", "__pycache__", ".venv", "dist", "node_modules"}]
                for file in files:
                    full_path = os.path.join(root, file)
                    rel_path = os.path.relpath(full_path, target_dir)
                    if filter_fn is None or filter_fn(rel_path):
                        arcname = os.path.join(f"{pkg_name}-{pkg_ver}", rel_path)
                        zf.write(full_path, arcname)


# --- Dependency Injection Package Builder ---

class PackageBuilder:
    """
    Package builder orchestrator leveraging injected manifest parsers and archive writers.
    """

    def __init__(
        self,
        parsers: Optional[List[ManifestParser]] = None,
        archive_writers: Optional[Dict[str, ArchiveWriter]] = None
    ):
        self.parsers = parsers or [
            ScryerManifestParser(),
            SwiPackParser(),
            TauJsonParser()
        ]
        self.archive_writers = archive_writers or {
            "swi": ZipArchiveWriter(),
            "scryer": TarGzArchiveWriter(),
            "trealla": TarGzArchiveWriter(),
            "tau": TarGzArchiveWriter(),
            "iso": TarGzArchiveWriter(),
            "default": TarGzArchiveWriter()
        }

    def resolve_manifest(self, target_dir: str, engine: str) -> Tuple[Dict[str, str], Optional[str]]:
        preferred_manifest = {
            "scryer": "scryer-manifest.pl",
            "iso": "scryer-manifest.pl",
            "trealla": "scryer-manifest.pl",
            "swi": "pack.pl",
            "tau": "package.json"
        }.get(engine)

        if preferred_manifest:
            parser = next((p for p in self.parsers if getattr(p, "manifest_name", None) == preferred_manifest), None)
            if parser:
                filepath = os.path.join(target_dir, parser.manifest_name)
                if os.path.exists(filepath):
                    meta = parser.parse_file(filepath)
                    if meta.get("name"):
                        return meta, parser.manifest_name

        for parser in self.parsers:
            filepath = os.path.join(target_dir, parser.manifest_name)
            if os.path.exists(filepath):
                meta = parser.parse_file(filepath)
                if meta.get("name"):
                    return meta, parser.manifest_name

        return {}, None

    def default_filter(self, rel_path: str) -> bool:
        parts = rel_path.split(os.sep)
        ignore_dirs = {".git", ".cache", "__pycache__", ".venv", ".pytest_cache", "dist", "node_modules"}
        if any(p in ignore_dirs for p in parts):
            return False
        if rel_path.endswith((".pyc", ".pyo", ".swp", ".tmp")):
            return False
        return True

    def build(self, target_dir: str = ".", engine: str = "scryer", out_dir: str = "dist") -> int:
        target_dir = os.path.abspath(target_dir)
        engine = (engine or "scryer").lower()

        metadata, manifest_type = self.resolve_manifest(target_dir, engine)

        pkg_name = metadata.get("name") or os.path.basename(target_dir)
        pkg_ver = metadata.get("version") or "0.1.0"

        print(f"=== Prolog Agent Packager ===")
        print(f"Engine Target: {engine}")
        print(f"Manifest File: {manifest_type or 'None found'}")
        print(f"Package Name : {pkg_name}")
        print(f"Package Vers : {pkg_ver}")

        main_file = metadata.get("main_file")
        if main_file:
            main_path = os.path.join(target_dir, main_file)
            if not os.path.exists(main_path):
                sys.stderr.write(f"Warning: Declared main_file '{main_file}' in manifest not found at {main_path}\n")

        dist_path = os.path.join(target_dir, out_dir)
        os.makedirs(dist_path, exist_ok=True)

        writer = self.archive_writers.get(engine, self.archive_writers.get("default", TarGzArchiveWriter()))
        archive_name = f"{pkg_name}-{pkg_ver}-{engine}.{writer.extension}"
        archive_file = os.path.join(dist_path, archive_name)

        print(f"Building {engine} archive ({writer.extension}): {archive_file}...")
        writer.write_archive(target_dir, archive_file, pkg_name, pkg_ver, filter_fn=self.default_filter)

        print(f"Package successfully built at: {archive_file}")
        return 0
