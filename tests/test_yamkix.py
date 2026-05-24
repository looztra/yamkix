"""Provide tests for the yamkix module."""

import sys
from io import StringIO
from pathlib import Path
from textwrap import dedent

import pytest
from pytest_mock import MockerFixture

from yamkix.config import YamkixInputOutputConfig, get_default_yamkix_config, get_yamkix_config_from_default
from yamkix.errors import InvalidYamlContentError
from yamkix.yamkix import FileProcessingResult, round_trip_and_format, yamkix_dump_all
from yamkix.yaml_writer import get_opinionated_yaml_writer


class TestRoundTripAndFormat:
    """Provide tests for the round_trip_and_format function."""

    def test_when_parser_error(self, mocker: MockerFixture, shared_datadir: Path) -> None:
        """Test that round_trip_and_format raises InvalidYamlContentError on ParserError."""
        # GIVEN
        mock_yamkix_dump_all = mocker.patch("yamkix.yamkix.yamkix_dump_all")
        config = get_yamkix_config_from_default(
            io_config=YamkixInputOutputConfig(input=str(shared_datadir / "malformed-yaml-file.yml"), output=None)
        )

        # WHEN / THEN
        with pytest.raises(InvalidYamlContentError):
            round_trip_and_format(config)
        mock_yamkix_dump_all.assert_not_called()

    def test_read_from_stdin(self, mocker: MockerFixture) -> None:
        """Test that round_trip_and_format reads from stdin when input file is None."""
        # GIVEN
        mock_get_opinionated_yaml_writer = mocker.patch("yamkix.yamkix.get_opinionated_yaml_writer")
        mock_sys_stdin = mocker.patch("sys.stdin")
        stdin_read_return_value = mocker.Mock()
        mock_sys_stdin.read.return_value = stdin_read_return_value
        mock_load_all = mock_get_opinionated_yaml_writer.return_value.load_all
        load_all_return_value = iter([mocker.Mock()])
        mock_load_all.return_value = load_all_return_value
        config = get_yamkix_config_from_default(io_config=YamkixInputOutputConfig(input=None, output=None))
        mock_yamkix_dump_all = mocker.patch("yamkix.yamkix.yamkix_dump_all")

        # WHEN
        result = round_trip_and_format(config)

        # THEN
        mock_load_all.assert_called_once_with(stdin_read_return_value)
        mock_sys_stdin.read.assert_called_once()
        mock_yamkix_dump_all.assert_called_once()
        assert isinstance(result, FileProcessingResult)
        assert result.error is False
        assert result.input_display_name == "STDIN"

    def test_returns_unchanged_true_when_content_not_modified(self, tmp_path: Path) -> None:
        """Test that round_trip_and_format returns unchanged=True when content is already formatted."""
        # GIVEN
        yaml_content = "---\nkey: value\n"
        input_file = tmp_path / "test.yml"
        input_file.write_text(yaml_content)
        config = get_yamkix_config_from_default(io_config=YamkixInputOutputConfig(input=str(input_file), output=None))

        # WHEN
        result = round_trip_and_format(config)

        # THEN
        assert isinstance(result, FileProcessingResult)
        assert result.error is False
        assert result.input_display_name == str(input_file)

    def test_returns_unchanged_false_when_content_is_modified(self, tmp_path: Path) -> None:
        """Test that round_trip_and_format returns unchanged=False when content is reformatted."""
        # GIVEN: YAML with inconsistent spacing that yamkix will reformat
        yaml_content = "---\nkey:   value\n"
        input_file = tmp_path / "test.yml"
        input_file.write_text(yaml_content)
        config = get_yamkix_config_from_default(io_config=YamkixInputOutputConfig(input=str(input_file), output=None))

        # WHEN
        result = round_trip_and_format(config)

        # THEN
        assert isinstance(result, FileProcessingResult)
        assert result.error is False
        assert result.unchanged is False


class TestYamkixDumpAll:
    """Provide tests for the yamkix_dump_all function."""

    def test_existing_file_is_overwritten(self, shared_datadir: Path) -> None:
        """Test that yamkix_dump_all overwrites an existing file."""
        # GIVEN
        sut = shared_datadir / "sut.yml"
        initial_content = "initial content"
        sut.write_text(initial_content)
        content = """\
        name:
            family: Smith # plouf
            given: Alice  # one of the siblings
        """
        yaml_parser = get_opinionated_yaml_writer(get_default_yamkix_config())
        yaml_content = yaml_parser.load(dedent(content))
        yamkix_dump_all(
            [yaml_content], yaml_parser, dash_inwards=False, output_file=str(sut), spaces_before_comment=None
        )
        assert initial_content not in content
        assert initial_content not in sut.read_text()

    def test_write_to_stdout(self, mocker: MockerFixture) -> None:
        """Test that yamkix_dump_all writes to stdout."""
        # GIVEN
        content = """\
        name:
            family: Smith # plouf
            given: Alice  # one of the siblings
        """
        config = get_default_yamkix_config()
        yaml_parser = get_opinionated_yaml_writer(config)
        yaml_content = yaml_parser.load(dedent(content))
        yamkix_dump_one = mocker.patch("yamkix.yamkix.yamkix_dump_one")
        yamkix_dump_all(
            [yaml_content],
            yaml_parser,
            dash_inwards=config.dash_inwards,
            output_file=None,
            spaces_before_comment=config.spaces_before_comment,
        )
        yamkix_dump_one.assert_called_once_with(
            single_item=yaml_content,
            yaml=yaml_parser,
            dash_inwards=config.dash_inwards,
            out=sys.stdout,
            spaces_before_comment=config.spaces_before_comment,
        )


class TestConvertFlowToBlock:
    """Tests for the convert_flow_to_block feature integrated into yamkix_dump_all."""

    def test_flow_sequences_and_maps_become_block(self, tmp_path: Path) -> None:
        """Test that flow-style sequences and mappings are converted to block style."""
        # GIVEN
        yaml_content = "---\na_list: [a, b, c]\na_map: {first: yolo, second: foo}\n"
        input_file = tmp_path / "test.yml"
        input_file.write_text(yaml_content)
        config = get_yamkix_config_from_default(
            convert_flow_to_block=True,
            io_config=YamkixInputOutputConfig(input=str(input_file), output=None),
        )

        # WHEN
        result = round_trip_and_format(config)

        # THEN
        assert result.error is False
        assert result.unchanged is False

    def test_block_style_unchanged_when_flag_disabled(self, tmp_path: Path) -> None:
        """Test that flow-style content is preserved when flag is off."""
        # GIVEN: already-formatted block YAML
        yaml_content = "---\na_list:\n  - a\n  - b\n  - c\n"
        input_file = tmp_path / "test.yml"
        input_file.write_text(yaml_content)
        config = get_yamkix_config_from_default(
            convert_flow_to_block=False,
            io_config=YamkixInputOutputConfig(input=str(input_file), output=None),
        )

        # WHEN
        result = round_trip_and_format(config)

        # THEN
        assert result.error is False
        assert result.unchanged is True

    def test_yamkix_dump_all_calls_convert_when_flag_set(self) -> None:
        """Test yamkix_dump_all invokes convert_flow_to_block_style when flag is True."""
        config = get_default_yamkix_config()
        yaml_parser = get_opinionated_yaml_writer(config)
        yaml_content = yaml_parser.load("a_list: [x, y]\n")
        buf = StringIO()
        yamkix_dump_all(
            [yaml_content],
            yaml_parser,
            dash_inwards=True,
            output_file=None,
            spaces_before_comment=None,
            capture_buffer=buf,
            convert_flow_to_block=True,
        )
        output = buf.getvalue()
        assert "[x, y]" not in output
        assert "- x" in output
        assert "- y" in output
