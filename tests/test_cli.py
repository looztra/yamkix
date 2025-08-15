"""Tests for the Typer-based CLI implementation."""

from pathlib import Path

import pytest
from pytest_mock import MockerFixture
from typer.testing import CliRunner

from yamkix._cli import app, echo_version
from yamkix.config import get_default_yamkix_config

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

    def test_default_values_with_dash_input(self, mocker: MockerFixture, shared_datadir: Path) -> None:
        """Test running the CLI without any parameters uses default values."""
        # GIVEN
        mock_create_config = mocker.patch("yamkix._cli.create_yamkix_config_from_typer_args")
        mock_config = mocker.Mock()
        mock_create_config.return_value = [mock_config]
        mock_print_config = mocker.patch("yamkix._cli.print_yamkix_config")
        mock_round_trip = mocker.patch("yamkix._cli.round_trip_and_format")
        test_file = shared_datadir / "simple.yml"
        # WHEN
        result = runner.invoke(app, ["--input", str(test_file)])

        # THEN
        assert result.exit_code == 0
        default_config = get_default_yamkix_config()
        mock_create_config.assert_called_once_with(
            input_file=str(test_file),
            output_file=default_config.io_config.output,
            stdout=False,
            typ=default_config.parsing_mode,
            no_explicit_start=not default_config.explicit_start,
            explicit_end=default_config.explicit_end,
            no_quotes_preserved=not default_config.quotes_preserved,
            default_flow_style=default_config.default_flow_style,
            no_dash_inwards=not default_config.dash_inwards,
            spaces_before_comment=default_config.spaces_before_comment,
            files=None,
        )
        mock_print_config.assert_called_once_with(mock_config)
        mock_round_trip.assert_called_once_with(mock_config)

    def test_default_values_with_one_argument(self, mocker: MockerFixture, shared_datadir: Path) -> None:
        """Test running the CLI without any parameters uses default values."""
        # GIVEN
        mock_create_config = mocker.patch("yamkix._cli.create_yamkix_config_from_typer_args")
        mock_config = mocker.Mock()
        mock_create_config.return_value = [mock_config]
        mock_print_config = mocker.patch("yamkix._cli.print_yamkix_config")
        mock_round_trip = mocker.patch("yamkix._cli.round_trip_and_format")
        test_file = shared_datadir / "simple.yml"
        # WHEN
        result = runner.invoke(app, [str(test_file)])

        # THEN
        assert result.exit_code == 0
        default_config = get_default_yamkix_config()
        mock_create_config.assert_called_once_with(
            input_file=default_config.io_config.input,
            output_file=default_config.io_config.output,
            stdout=False,
            typ=default_config.parsing_mode,
            no_explicit_start=not default_config.explicit_start,
            explicit_end=default_config.explicit_end,
            no_quotes_preserved=not default_config.quotes_preserved,
            default_flow_style=default_config.default_flow_style,
            no_dash_inwards=not default_config.dash_inwards,
            spaces_before_comment=default_config.spaces_before_comment,
            files=[test_file],
        )
        mock_print_config.assert_called_once_with(mock_config)
        mock_round_trip.assert_called_once_with(mock_config)

    def test_silent_mode(self, mocker: MockerFixture, shared_datadir: Path) -> None:
        """Test running the CLI without any parameters uses default values."""
        # GIVEN
        mock_create_config = mocker.patch("yamkix._cli.create_yamkix_config_from_typer_args")
        mock_config = mocker.Mock()
        mock_create_config.return_value = [mock_config]
        mock_print_config = mocker.patch("yamkix._cli.print_yamkix_config")
        mock_round_trip = mocker.patch("yamkix._cli.round_trip_and_format")
        test_file = shared_datadir / "simple.yml"
        # WHEN
        result = runner.invoke(app, ["--silent", "--input", str(test_file)])

        # THEN
        assert result.exit_code == 0
        mock_create_config.assert_called_once()
        mock_print_config.assert_not_called()
        mock_round_trip.assert_called_once()
