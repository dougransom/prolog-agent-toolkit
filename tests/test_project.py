import os
import shutil
import tempfile
import pytest

from prolog_agent_toolkit.project import init_project
from prolog_agent_toolkit.release import run_release


@pytest.fixture
def temp_project_dir():
    temp_dir = tempfile.mkdtemp(prefix="prolog_proj_test_")
    yield temp_dir
    shutil.rmtree(temp_dir, ignore_errors=True)


def test_init_project_scryer(temp_project_dir):
    res = init_project("my_scryer_app", engine="scryer", base_dir=temp_project_dir)
    assert res == 0

    proj_dir = os.path.join(temp_project_dir, "my_scryer_app")
    assert os.path.exists(os.path.join(proj_dir, "src", "my_scryer_app.pl"))
    assert os.path.exists(os.path.join(proj_dir, "tests", "testing.pl"))
    assert os.path.exists(os.path.join(proj_dir, "bakage.toml"))
    assert os.path.exists(os.path.join(proj_dir, "README.md"))

    with open(os.path.join(proj_dir, "bakage.toml"), "r") as f:
        content = f.read()
    assert 'name = "my_scryer_app"' in content
    assert 'version = "0.1.0"' in content


def test_init_project_swi(temp_project_dir):
    res = init_project("my_swi_app", engine="swi", base_dir=temp_project_dir)
    assert res == 0

    proj_dir = os.path.join(temp_project_dir, "my_swi_app")
    assert os.path.exists(os.path.join(proj_dir, "src", "my_swi_app.pl"))
    assert os.path.exists(os.path.join(proj_dir, "tests", "test_my_swi_app.pl"))
    assert os.path.exists(os.path.join(proj_dir, "pack.pl"))

    with open(os.path.join(proj_dir, "pack.pl"), "r") as f:
        content = f.read()
    assert "name('my_swi_app')" in content


def test_init_project_tau(temp_project_dir):
    res = init_project("my_tau_app", engine="tau", base_dir=temp_project_dir)
    assert res == 0

    proj_dir = os.path.join(temp_project_dir, "my_tau_app")
    assert os.path.exists(os.path.join(proj_dir, "package.json"))

    with open(os.path.join(proj_dir, "package.json"), "r") as f:
        content = f.read()
    assert '"name": "my_tau_app"' in content
    assert '"tau-prolog"' in content


def test_run_release(temp_project_dir):
    init_project("release_app", engine="scryer", base_dir=temp_project_dir)
    proj_dir = os.path.join(temp_project_dir, "release_app")

    res = run_release(new_version="0.2.0", target_dir=proj_dir)
    assert res == 0

    with open(os.path.join(proj_dir, "bakage.toml"), "r") as f:
        content = f.read()
    assert 'version = "0.2.0"' in content

    changelog_path = os.path.join(proj_dir, "CHANGELOG.md")
    assert os.path.exists(changelog_path)
    with open(changelog_path, "r") as f:
        cl_text = f.read()
    assert "## [0.2.0]" in cl_text
