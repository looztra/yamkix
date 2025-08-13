"""Provide integration tests related to kubesplit compatibility."""

import subprocess
from pathlib import Path

import pytest


@pytest.mark.integration
class TestKubesplitCompatibility:
    """Provide integration tests for kubesplit compatibility."""

    def test_kubesplit_version(
        self,
        wheel_file: Path,
        path_to_uv: str,
        uv_tool_dir: Path,
        install_env: dict[str, str],
        project_path: Path,
    ) -> None:
        """Test we can install kubesplit and get its version."""
        tool_name = "kubesplit"
        result_tool_install = subprocess.run(  # noqa: S603
            [
                path_to_uv,
                "tool",
                "install",
                "--no-config",
                "--find-links",
                wheel_file.parent,
                "--prerelease",
                "allow",
                "kubesplit",
            ],
            check=False,
            cwd=project_path,
            capture_output=True,
            text=True,
            env=install_env,
        )
        assert result_tool_install.returncode == 0, f"Installation failed: {result_tool_install.stderr}"
        assert f"Installed 1 executable: {tool_name}" in result_tool_install.stderr, (
            f"{tool_name.capitalize()} installation message not found"
        )
        assert (uv_tool_dir / tool_name).exists(), f"UV {tool_name} bin directory should exist"
        result_tool_run = subprocess.run(  # noqa: S603
            [str(uv_tool_dir / tool_name / "bin" / tool_name), "--version"],
            check=False,
            capture_output=True,
            text=True,
        )
        assert result_tool_run.returncode == 0, f"Installed {tool_name} executable is not functional"
        result_tool_uninstall = subprocess.run(  # noqa: S603
            [path_to_uv, "tool", "uninstall", "--no-config", tool_name],
            check=False,
            cwd=project_path,
            capture_output=True,
            text=True,
            env=install_env,
        )
        assert result_tool_uninstall.returncode == 0, f"Uninstallation failed: {result_tool_uninstall.stderr}"

    def test_kubesplit_run(  # noqa: PLR0913
        self,
        wheel_file: Path,
        path_to_uv: str,
        uv_tool_dir: Path,
        install_env: dict[str, str],
        project_path: Path,
        datadir: Path,
    ) -> None:
        """Test we can install kubesplit and get its version."""
        tool_name = "kubesplit"
        result_tool_install = subprocess.run(  # noqa: S603
            [
                path_to_uv,
                "tool",
                "install",
                "--no-config",
                "--find-links",
                wheel_file.parent,
                "--prerelease",
                "allow",
                "kubesplit",
            ],
            check=False,
            cwd=project_path,
            capture_output=True,
            text=True,
            env=install_env,
        )
        assert result_tool_install.returncode == 0, f"Installation failed: {result_tool_install.stderr}"
        assert f"Installed 1 executable: {tool_name}" in result_tool_install.stderr, (
            f"{tool_name.capitalize()} installation message not found"
        )
        assert (uv_tool_dir / tool_name).exists(), f"UV {tool_name} bin directory should exist"

        source_file_path = str(datadir / "all-in-one.yml")
        target_path = str(datadir / "kubesplit-output")
        result_tool_run = subprocess.run(  # noqa: S603
            [str(uv_tool_dir / tool_name / "bin" / tool_name), "--input", source_file_path, "--output", target_path],
            check=False,
            capture_output=True,
            text=True,
        )
        assert result_tool_run.returncode == 0, f"Installed {tool_name} executable is not functional"

        result_tool_uninstall = subprocess.run(  # noqa: S603
            [path_to_uv, "tool", "uninstall", "--no-config", tool_name],
            check=False,
            cwd=project_path,
            capture_output=True,
            text=True,
            env=install_env,
        )
        assert result_tool_uninstall.returncode == 0, f"Uninstallation failed: {result_tool_uninstall.stderr}"
