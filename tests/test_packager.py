import os
import shutil
import tempfile
import tarfile
import pytest

from prolog_agent_toolkit.packager import build_package, parse_bakage_toml, parse_pack_pl


@pytest.fixture
def temp_pkg_dir():
    temp_dir = tempfile.mkdtemp(prefix="prolog_pack_test_")
    yield temp_dir
    shutil.rmtree(temp_dir, ignore_errors=True)


def test_build_package_scryer(temp_pkg_dir):
    bakage_path = os.path.join(temp_pkg_dir, "bakage.toml")
    with open(bakage_path, "w") as f:
        f.write('name = "test_pkg"\nversion = "1.2.3"\nmodules = ["src/test_pkg.pl"]\n')

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
        assert any("bakage.toml" in n for n in names)
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
