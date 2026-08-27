import os
import shutil
import stat
import tempfile
import pytest

from prolog_agent_toolkit.release import check_versions
from prolog_agent_toolkit.hooks import install_hooks


@pytest.fixture
def temp_project_dir():
    temp_dir = tempfile.mkdtemp()
    yield temp_dir
    shutil.rmtree(temp_dir, ignore_errors=True)


def test_check_versions_success(temp_project_dir):
    pyproject = os.path.join(temp_project_dir, "pyproject.toml")
    readme = os.path.join(temp_project_dir, "README.md")
    schema = os.path.join(temp_project_dir, "schema.org.jsonld")

    with open(pyproject, "w", encoding="utf-8") as f:
        f.write('[project]\nversion = "1.2.3"\n')
    with open(readme, "w", encoding="utf-8") as f:
        f.write("# Project\n**Version**: `1.2.3`\n")
    with open(schema, "w", encoding="utf-8") as f:
        f.write('{"version": "1.2.3"}\n')

    assert check_versions(target_dir=temp_project_dir) == 0


def test_check_versions_mismatch(temp_project_dir):
    pyproject = os.path.join(temp_project_dir, "pyproject.toml")
    readme = os.path.join(temp_project_dir, "README.md")

    with open(pyproject, "w", encoding="utf-8") as f:
        f.write('[project]\nversion = "1.2.3"\n')
    with open(readme, "w", encoding="utf-8") as f:
        f.write("# Project\n**Version**: `1.0.0`\n")

    assert check_versions(target_dir=temp_project_dir) == 1


def test_install_hooks_success(temp_project_dir):
    git_dir = os.path.join(temp_project_dir, ".git")
    os.makedirs(git_dir, exist_ok=True)

    assert install_hooks(target_dir=temp_project_dir, hook_type="pre-commit") == 0

    hook_file = os.path.join(git_dir, "hooks", "pre-commit")
    assert os.path.exists(hook_file)

    # Check executable permission
    st = os.stat(hook_file)
    assert bool(st.st_mode & stat.S_IXUSR)

    with open(hook_file, "r", encoding="utf-8") as f:
        content = f.read()
    assert "prolog-agent check-version" in content
    assert "prolog-agent validate-skills" in content


def test_install_hooks_no_git_dir(temp_project_dir):
    # Should fail if .git does not exist
    assert install_hooks(target_dir=temp_project_dir, hook_type="pre-commit") == 1
