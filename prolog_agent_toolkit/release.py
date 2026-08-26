import datetime
import os
import re
import sys

sys.dont_write_bytecode = True
os.environ["PYTHONDONTWRITEBYTECODE"] = "1"


def get_pyproject_version(target_dir: str) -> str:
    """Read canonical release version from pyproject.toml using standard Python libraries."""
    pyproject_path = os.path.join(target_dir, "pyproject.toml")
    if os.path.exists(pyproject_path):
        if sys.version_info >= (3, 11):
            import tomllib
            with open(pyproject_path, "rb") as f:
                data = tomllib.load(f)
                return data.get("project", {}).get("version", "0.0.1")
        else:
            with open(pyproject_path, "r", encoding="utf-8") as f:
                content = f.read()
            m = re.search(r'version\s*=\s*["\']([^"\']+)["\']', content)
            if m:
                return m.group(1)
    return "0.0.1"


def sync_file_version(filepath: str, old_ver_pattern: str, new_ver_str: str) -> bool:
    """Replace version string matching regex pattern in a file."""
    if not os.path.exists(filepath):
        return False
    with open(filepath, "r", encoding="utf-8") as f:
        content = f.read()

    new_content = re.sub(old_ver_pattern, new_ver_str, content)
    if new_content != content:
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(new_content)
        return True
    return False


def run_release(new_version: str = None, target_dir: str = ".") -> int:
    """
    Synchronize version numbers across project files using pyproject.toml as the canonical source,
    generate or update CHANGELOG.md, and output Git tag and publishing steps.
    """
    target_dir = os.path.abspath(target_dir)

    pyproject_path = os.path.join(target_dir, "pyproject.toml")
    if new_version:
        # Update canonical version in pyproject.toml
        sync_file_version(
            pyproject_path,
            r'version\s*=\s*["\'][^"\']+["\']',
            f'version = "{new_version}"'
        )
    else:
        # Use existing canonical version from pyproject.toml
        new_version = get_pyproject_version(target_dir)

    print(f"Preparing release v{new_version} in {target_dir}...")

    # 1. Update bakage.toml
    sync_file_version(
        os.path.join(target_dir, "bakage.toml"),
        r'version\s*=\s*["\'][^"\']+["\']',
        f'version = "{new_version}"'
    )

    # 2. Update pack.pl
    sync_file_version(
        os.path.join(target_dir, "pack.pl"),
        r"version\(['\"][^'\"]+['\"]\)",
        f"version('{new_version}')"
    )

    # 3. Update package.json
    sync_file_version(
        os.path.join(target_dir, "package.json"),
        r'"version"\s*:\s*"[^"]+"',
        f'"version": "{new_version}"'
    )

    # 4. Generate / update CHANGELOG.md
    changelog_path = os.path.join(target_dir, "CHANGELOG.md")
    today = datetime.date.today().isoformat()
    changelog_entry = (
        f"## [{new_version}] - {today}\n\n"
        f"### Summary of Changes\n- Release v{new_version} synchronized across manifest files.\n\n"
        f"### Added / Modified Predicates\n- Dialect updates and purity enhancements.\n\n"
        f"### Breaking Changes\n- None.\n\n"
    )

    if os.path.exists(changelog_path):
        with open(changelog_path, "r", encoding="utf-8") as f:
            old_changelog = f.read()
        if f"## [{new_version}]" not in old_changelog:
            with open(changelog_path, "w", encoding="utf-8") as f:
                f.write(changelog_entry + "\n" + old_changelog)
    else:
        with open(changelog_path, "w", encoding="utf-8") as f:
            f.write(f"# Changelog\n\nAll notable changes to this project will be documented in this file.\n\n" + changelog_entry)

    print("\nRelease Preparation Complete!")
    print("------------------------------------------------------------------")
    print(f"1. Commit changes: git commit -am \"Release v{new_version}\"")
    print(f"2. Create Git tag:  git tag -a v{new_version} -m \"Release v{new_version}\"")
    print("3. Push tag:        git push origin main --tags")
    print("------------------------------------------------------------------\n")

    return 0
