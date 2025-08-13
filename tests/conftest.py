"""Provide shared fixtures."""

import os
import shutil
import subprocess
from pathlib import Path

import pytest

# Path to this module file
MODULE_PATH = Path(__file__)
PROJECT_PATH = MODULE_PATH.parent.parent


@pytest.fixture(name="uv_tests_root_dir", scope="session")
def uv_tests_root_dir_fixture(tmp_path_factory: pytest.TempPathFactory) -> Path:
    """Provide a temporary directory for UV tests."""
    return tmp_path_factory.mktemp("uv-tests")


@pytest.fixture(name="uv_tool_dir")
def uv_tool_dir_fixture(uv_tests_root_dir: Path) -> Path:
    """Provide a temporary directory for UV tool installation."""
    return uv_tests_root_dir / "tool-install"


@pytest.fixture(name="uv_tool_bin_dir", scope="session")
def uv_tool_bin_dir_fixture(uv_tests_root_dir: Path) -> Path:
    """Provide a temporary directory for UV tool binaries."""
    return uv_tests_root_dir / "bin"


@pytest.fixture(name="install_env")
def install_env_fixture(uv_tool_dir: Path, uv_tool_bin_dir: Path) -> dict[str, str]:
    """Provide environment variables for UV tool installation."""
    install_env = os.environ.copy()
    install_env["UV_TOOL_DIR"] = str(uv_tool_dir)
    install_env["UV_TOOL_BIN_DIR"] = str(uv_tool_bin_dir)
    install_env["UV_LINK_MODE"] = "copy"
    install_env["UV_NO_PROGRESS"] = "1"
    return install_env


@pytest.fixture(name="dist_dir", scope="session")
def dist_dir_fixture(uv_tests_root_dir: Path) -> Path:
    """Return the distribution directory."""
    dist_dir = uv_tests_root_dir / "dist"
    dist_dir.mkdir(parents=True, exist_ok=True)
    return dist_dir


@pytest.fixture(name="path_to_uv", scope="session")
def path_to_uv_fixture() -> str:
    """Return the path to the UV tool."""
    path_to_uv = shutil.which("uv")
    assert path_to_uv is not None, "UV tool should be available in PATH"
    path_to_uv_resolved = Path(path_to_uv).resolve()
    assert path_to_uv_resolved.is_file(), f"UV tool path {path_to_uv_resolved} should be a file"
    assert os.access(path_to_uv_resolved, os.X_OK), f"UV tool path {path_to_uv_resolved} should be executable"
    return path_to_uv


@pytest.fixture(name="wheel_file", scope="session")
def wheel_file_fixture(dist_dir: Path, path_to_uv: str) -> Path:
    """Build the distribution."""
    # Assuming a build command is available, e.g., `python setup.py bdist_wheel`
    result = subprocess.run(  # noqa: S603
        [path_to_uv, "build", "--wheel", "--out-dir", str(dist_dir)],
        check=False,
        cwd=PROJECT_PATH,
        capture_output=True,
        text=True,
    )
    assert result.returncode == 0, f"Building distribution failed: {result.stderr}"
    wheel_files = list(dist_dir.glob("yamkix-*.whl"))
    assert wheel_files, "No yamkix wheel file found in dist directory"
    assert len(wheel_files) == 1, "Expected exactly one yamkix wheel file in dist directory"
    return wheel_files[0].resolve()


@pytest.fixture(name="project_path", scope="session")
def project_path() -> Path:
    """Return the project root path."""
    return PROJECT_PATH
