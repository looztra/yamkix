"""Tests for the Typer-based CLI implementation."""

import pytest
from pytest_mock import MockerFixture
from typer.testing import CliRunner

from yamkix._cli import app, echo_version

runner = CliRunner()


def test_help_command() -> None:
    """Test help command."""
    # GIVEN/WHEN
    result = runner.invoke(app=app, args=["--help"])

    # THEN
    assert result.exit_code == 0
    assert "Usage" in result.stdout
    assert "Options" in result.stdout


def test_version_arg(mocker: MockerFixture) -> None:
    """Test the version arg."""
    # GIVEN
    mock_echo_version = mocker.patch("yamkix._cli.echo_version")

    # WHEN
    result = runner.invoke(app, "--version")

    # THEN
    assert result.exit_code == 0
    mock_echo_version.assert_called_once()


def test_echo_version(
    mocker: MockerFixture,
    capsys: pytest.CaptureFixture[str],
) -> None:
    """Test echo_version."""
    # GIVEN
    mocker.patch("yamkix._cli.__version__", "1.0.0")

    # WHEN
    echo_version()

    # THEN
    captured = capsys.readouterr()
    assert "1.0.0" in captured.out
