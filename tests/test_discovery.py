import os
import shutil
import tempfile
import pytest

from prolog_agent_toolkit.discovery import (
    discover_capabilities,
    discover_manifest_packages,
    format_discovery_report,
)
from prolog_agent_toolkit.project import init_project


@pytest.fixture
def temp_project_dir():
    temp_dir = tempfile.mkdtemp(prefix="prolog_discovery_test_")
    yield temp_dir
    shutil.rmtree(temp_dir, ignore_errors=True)


def test_discover_capabilities_static():
    res = discover_capabilities(engine="scryer", query="constraint", mode="static")
    assert "engines" in res
    assert "scryer" in res["engines"]
    libs = res["engines"]["scryer"]["static_libraries"]
    assert len(libs) > 0
    assert any(lib["name"] == "clpz" for lib in libs)


def test_discover_capabilities_all_engines():
    res = discover_capabilities(engine="all", query="format", mode="static")
    assert "scryer" in res["engines"]
    assert "swi" in res["engines"]
    assert "trealla" in res["engines"]
    assert "tau" in res["engines"]


def test_discover_manifest_packages(temp_project_dir):
    init_project("disc_scryer_app", engine="scryer", base_dir=temp_project_dir)
    app_dir = os.path.join(temp_project_dir, "disc_scryer_app")

    manifests = discover_manifest_packages(project_dir=app_dir)
    assert len(manifests) >= 1
    bakage_m = next((m for m in manifests if m["source"] == "bakage.toml"), None)
    assert bakage_m is not None
    assert bakage_m["name"] == "disc_scryer_app"


def test_format_discovery_report():
    data = discover_capabilities(engine="scryer", query="dcg", mode="static")
    report = format_discovery_report(data)
    assert "PROLOG AGENT TOOLKIT — LIBRARY & CAPABILITY DISCOVERY REPORT" in report
    assert "SCRYER PROLOG" in report
    assert "dcgs" in report
    assert "PRE-CODE-GENERATION POLICY REMINDER" in report
