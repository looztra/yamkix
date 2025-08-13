"""Provide tests that verify we can install the package."""

import subprocess
from pathlib import Path

import pytest


@pytest.mark.integration
class TestPackageInstallation:
    """Provide integration tests for package installation."""

    @pytest.mark.parametrize(
        "resolution",
        [
            pytest.param("highest", id="highest"),
            pytest.param("lowest", id="lowest"),
            pytest.param("lowest-direct", id="lowest-direct"),
        ],
    )
    def test_yamkix_can_be_installed_from_dist(  # noqa: PLR0913
        self,
        wheel_file: Path,
        path_to_uv: str,
        uv_tool_dir: Path,
        install_env: dict[str, str],
        resolution: str,
        project_path: Path,
    ) -> None:
        """Test that yamkix can be installed from the distribution."""
        tool_name = "yamkix"
        result = subprocess.run(  # noqa: S603
            [path_to_uv, "tool", "install", "--no-config", "--resolution", resolution, str(wheel_file)],
            check=False,
            cwd=project_path,
            capture_output=True,
            text=True,
            env=install_env,
        )
        assert result.returncode == 0, f"Installation failed: {result.stderr}"
        assert f"Installed 1 executable: {tool_name}" in result.stderr, (
            f"{tool_name.capitalize()} installation message not found"
        )
        assert (uv_tool_dir / tool_name).exists(), f"UV {tool_name} bin directory should exist"
        result = subprocess.run(  # noqa: S603
            [str(uv_tool_dir / tool_name / "bin" / tool_name), "--help"],
            check=False,
            capture_output=True,
            text=True,
        )
        assert result.returncode == 0, f"Installed {tool_name} executable is not functional"
        # Let's uninstall the package after testing because we want to be able to install it again during the session
        result = subprocess.run(  # noqa: S603
            [path_to_uv, "tool", "uninstall", "--no-config", tool_name],
            check=False,
            cwd=project_path,
            capture_output=True,
            text=True,
            env=install_env,
        )
        assert result.returncode == 0, f"Uninstallation failed: {result.stderr}"
