import os
import shutil
import tempfile
import tarfile
import pytest

from prolog_agent_toolkit.packager import (
    build_package,
    parse_scryer_manifest,
    parse_pack_pl,
    PackageBuilder,
    ScryerManifestParser,
    SwiPackParser,
    TauJsonParser,
)


@pytest.fixture
def temp_pkg_dir():
    temp_dir = tempfile.mkdtemp(prefix="prolog_pack_test_")
    yield temp_dir
    shutil.rmtree(temp_dir, ignore_errors=True)


def test_build_package_scryer(temp_pkg_dir):
    manifest_path = os.path.join(temp_pkg_dir, "scryer-manifest.pl")
    with open(manifest_path, "w") as f:
        f.write('name("test_pkg").\nversion("1.2.3").\nmain_file("src/test_pkg.pl").\n')

    src_dir = os.path.join(temp_pkg_dir, "src")
    os.makedirs(src_dir, exist_ok=True)
    with open(os.path.join(src_dir, "test_pkg.pl"), "w") as f:
        f.write(":- module(test_pkg, []).\n")

    res = build_package(target_dir=temp_pkg_dir, engine="scryer", out_dir="dist")
    assert res == 0

    dist_dir = os.path.join(temp_pkg_dir, "dist")
    tar_path = os.path.join(dist_dir, "test_pkg-1.2.3-scryer.tar.gz")
    assert os.path.exists(tar_path)

    with tarfile.open(tar_path, "r:gz") as tar:
        names = tar.getnames()
        assert any("scryer-manifest.pl" in n for n in names)
        assert any("src/test_pkg.pl" in n for n in names)


def test_build_package_swi(temp_pkg_dir):
    pack_path = os.path.join(temp_pkg_dir, "pack.pl")
    with open(pack_path, "w") as f:
        f.write("name('swi_pkg').\nversion('0.5.0').\n")

    res = build_package(target_dir=temp_pkg_dir, engine="swi", out_dir="dist")
    assert res == 0

    dist_dir = os.path.join(temp_pkg_dir, "dist")
    zip_path = os.path.join(dist_dir, "swi_pkg-0.5.0-swi.zip")
    assert os.path.exists(zip_path)


class MockCustomParser:
    manifest_name = "custom-manifest.txt"

    def parse_content(self, content: str):
        return {"name": "custom_injected_app", "version": "9.9.9"}

    def parse_file(self, filepath: str):
        return {"name": "custom_injected_app", "version": "9.9.9"}


class MockCustomWriter:
    extension = "mock"
    written = False

    def write_archive(self, target_dir, archive_path, pkg_name, pkg_ver, filter_fn=None):
        self.written = True
        with open(archive_path, "w") as f:
            f.write(f"{pkg_name}=={pkg_ver}")


def test_package_builder_dependency_injection(temp_pkg_dir):
    manifest_path = os.path.join(temp_pkg_dir, "custom-manifest.txt")
    with open(manifest_path, "w") as f:
        f.write("custom content")

    mock_parser = MockCustomParser()
    mock_writer = MockCustomWriter()

    builder = PackageBuilder(
        parsers=[mock_parser],
        archive_writers={"custom_engine": mock_writer}
    )

    res = builder.build(target_dir=temp_pkg_dir, engine="custom_engine", out_dir="dist")
    assert res == 0
    assert mock_writer.written is True

    out_file = os.path.join(temp_pkg_dir, "dist", "custom_injected_app-9.9.9-custom_engine.mock")
    assert os.path.exists(out_file)
    with open(out_file, "r") as f:
        assert f.read() == "custom_injected_app==9.9.9"
