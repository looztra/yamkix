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


class TestCli:
    """Provide unit tests for the CLI."""

    def test_invalid_typ(self) -> None:
        """Test running the CLI with an invalid typ."""
        # WHEN
        result = runner.invoke(app, ["--typ", "invalid"])

        # THEN
        assert result.exit_code != 0
        assert "Invalid value 'invalid'" in result.output
        assert "Must be 'safe' or 'rt'" in result.output

    def test_default_values(self, mocker: MockerFixture) -> None:
        """Test running the CLI without any parameters uses default values."""
        # GIVEN
        mock_create_config = mocker.patch("yamkix._cli.create_yamkix_config_from_typer_args")
        mock_print_config = mocker.patch("yamkix._cli.print_yamkix_config")
        mock_round_trip = mocker.patch("yamkix._cli.round_trip_and_format")

        # WHEN
        result = runner.invoke(app, [])

        # THEN
        assert result.exit_code == 0
        mock_create_config.assert_called_once_with(
            input_file=None,
            output_file=None,
            stdout=False,
            typ="rt",
            no_explicit_start=False,
            explicit_end=False,
            no_quotes_preserved=False,
            default_flow_style=False,
            no_dash_inwards=False,
            spaces_before_comment=None,
            version=None,  # Typer passes None when callback option is not used
        )
        mock_print_config.assert_called_once()
        mock_round_trip.assert_called_once()
