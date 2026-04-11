"""Tests for the Typer-based CLI implementation."""

from pathlib import Path

import pytest
from pytest_mock import MockerFixture
from typer.testing import CliRunner

from yamkix._cli import app, echo_version
from yamkix.config import get_default_yamkix_config
from yamkix.errors import InvalidYamlContentError
from yamkix.yamkix import FileProcessingResult

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
        assert "'invalid' is not one of" in result.output
        assert "'safe', 'rt'" in result.output

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
            enforce_double_quotes=default_config.enforce_double_quotes,
            line_width=default_config.line_width,
            align_comments=default_config.align_comments,
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
            enforce_double_quotes=default_config.enforce_double_quotes,
            line_width=default_config.line_width,
            align_comments=default_config.align_comments,
            files=[test_file],
        )
        mock_print_config.assert_called_once_with(mock_config)
        mock_round_trip.assert_called_once_with(mock_config)

    def test_default_values_with_two_arguments(self, mocker: MockerFixture, shared_datadir: Path) -> None:
        """Test running the CLI without any parameters uses default values."""
        # GIVEN
        mock_create_config = mocker.patch("yamkix._cli.create_yamkix_config_from_typer_args")
        mock_config1 = mocker.Mock()
        mock_config2 = mocker.Mock()
        configs = [mock_config1, mock_config2]
        mock_create_config.return_value = configs
        mock_print_config = mocker.patch("yamkix._cli.print_yamkix_config")
        mock_round_trip = mocker.patch("yamkix._cli.round_trip_and_format")
        test_file1 = shared_datadir / "simple.yml"
        test_file2 = shared_datadir / "multi-doc-1.yml"
        # WHEN
        result = runner.invoke(app, [str(test_file1), str(test_file2)])

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
            enforce_double_quotes=default_config.enforce_double_quotes,
            line_width=default_config.line_width,
            align_comments=default_config.align_comments,
            files=[test_file1, test_file2],
        )
        mock_print_config.assert_called()
        assert mock_print_config.call_count == len(configs)
        mock_round_trip.assert_called()
        assert mock_round_trip.call_count == len(configs)

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

    def test_invalid_yaml_content_error_management(self, mocker: MockerFixture, shared_datadir: Path) -> None:
        """Test that InvalidYamlContentError is raised for invalid YAML content."""
        # GIVEN
        mock_create_config = mocker.patch("yamkix._cli.create_yamkix_config_from_typer_args")
        mock_config = mocker.Mock()
        mock_create_config.return_value = [mock_config]
        mock_print_config = mocker.patch("yamkix._cli.print_yamkix_config")
        mock_round_trip = mocker.patch("yamkix._cli.round_trip_and_format", side_effect=InvalidYamlContentError)
        mock_get_stderr_console = mocker.patch("yamkix._cli.get_stderr_console")
        mock_stderr_console = mock_get_stderr_console.return_value
        test_file = shared_datadir / "simple.yml"
        # WHEN
        result = runner.invoke(app, ["--input", str(test_file)])

        # THEN
        assert result.exit_code == 0
        mock_create_config.assert_called_once()
        mock_print_config.assert_called_once()
        mock_round_trip.assert_called_once()
        mock_stderr_console.print.assert_called()

    def test_line_width_arg(self, mocker: MockerFixture, shared_datadir: Path) -> None:
        """Test the line_width arg."""
        # GIVEN
        mock_create_config = mocker.patch("yamkix._cli.create_yamkix_config_from_typer_args")
        mock_config = mocker.Mock()
        mock_create_config.return_value = [mock_config]
        mocker.patch("yamkix._cli.print_yamkix_config")
        mocker.patch("yamkix._cli.round_trip_and_format")
        test_file = shared_datadir / "simple.yml"

        # WHEN
        result = runner.invoke(app, ["--line-width", "100", "--input", str(test_file)])

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
            enforce_double_quotes=default_config.enforce_double_quotes,
            line_width=100,
            align_comments=default_config.align_comments,
            files=None,
        )

    def test_summary_mode_not_printed_when_flag_absent(self, mocker: MockerFixture, shared_datadir: Path) -> None:
        """Test that summary is not printed when --summary is not passed."""
        # GIVEN
        mock_create_config = mocker.patch("yamkix._cli.create_yamkix_config_from_typer_args")
        mock_config = mocker.Mock()
        mock_create_config.return_value = [mock_config]
        mocker.patch("yamkix._cli.print_yamkix_config")
        fake_result = FileProcessingResult(input_display_name="test.yml", error=False, unchanged=True)
        mocker.patch("yamkix._cli.round_trip_and_format", return_value=fake_result)
        mock_get_stderr_console = mocker.patch("yamkix._cli.get_stderr_console")
        mock_stderr_console = mock_get_stderr_console.return_value
        test_file = shared_datadir / "simple.yml"

        # WHEN
        result = runner.invoke(app, ["--input", str(test_file)])

        # THEN
        assert result.exit_code == 0
        mock_stderr_console.print.assert_not_called()

    def test_summary_mode_printed_when_flag_present(self, mocker: MockerFixture, shared_datadir: Path) -> None:
        """Test that summary is printed to stderr when --summary is passed."""
        # GIVEN
        mock_create_config = mocker.patch("yamkix._cli.create_yamkix_config_from_typer_args")
        mock_config = mocker.Mock()
        mock_create_config.return_value = [mock_config]
        mocker.patch("yamkix._cli.print_yamkix_config")
        fake_result = FileProcessingResult(input_display_name="test.yml", error=False, unchanged=False)
        mocker.patch("yamkix._cli.round_trip_and_format", return_value=fake_result)
        mock_get_stderr_console = mocker.patch("yamkix._cli.get_stderr_console")
        mock_stderr_console = mock_get_stderr_console.return_value
        test_file = shared_datadir / "simple.yml"

        # WHEN
        result = runner.invoke(app, ["--summary", "--input", str(test_file)])

        # THEN
        assert result.exit_code == 0
        mock_stderr_console.print.assert_called_once()
        call_args = mock_stderr_console.print.call_args
        summary_text = call_args[0][0]
        assert "1 file(s) processed" in summary_text
        assert "0 error(s)" in summary_text
        assert "0 unchanged" in summary_text

    def test_summary_mode_counts_errors_and_unchanged(self, mocker: MockerFixture, shared_datadir: Path) -> None:
        """Test that summary correctly counts errors and unchanged files across multiple configs."""
        # GIVEN
        mock_create_config = mocker.patch("yamkix._cli.create_yamkix_config_from_typer_args")
        mock_config1 = mocker.Mock()
        mock_config2 = mocker.Mock()
        mock_config3 = mocker.Mock()
        mock_create_config.return_value = [mock_config1, mock_config2, mock_config3]
        mocker.patch("yamkix._cli.print_yamkix_config")
        results = [
            FileProcessingResult(input_display_name="a.yml", error=False, unchanged=True),
            FileProcessingResult(input_display_name="b.yml", error=False, unchanged=False),
            FileProcessingResult(input_display_name="c.yml", error=True, unchanged=False),
        ]
        mocker.patch("yamkix._cli.round_trip_and_format", side_effect=results)
        mock_get_stderr_console = mocker.patch("yamkix._cli.get_stderr_console")
        mock_stderr_console = mock_get_stderr_console.return_value
        test_file = shared_datadir / "simple.yml"

        # WHEN - InvalidYamlContentError is raised for mock_config3 inside the CLI loop
        mocker.patch(
            "yamkix._cli.round_trip_and_format",
            side_effect=[
                FileProcessingResult(input_display_name="a.yml", error=False, unchanged=True),
                FileProcessingResult(input_display_name="b.yml", error=False, unchanged=False),
                InvalidYamlContentError,
            ],
        )
        mock_config3.io_config.input_display_name = "c.yml"
        result = runner.invoke(app, ["--summary", str(test_file)])

        # THEN
        assert result.exit_code == 0
        # The summary print is the last call on the console
        last_call_args = mock_stderr_console.print.call_args_list[-1]
        summary_text = last_call_args[0][0]
        assert "3 file(s) processed" in summary_text
        assert "1 error(s)" in summary_text
        assert "1 unchanged" in summary_text
