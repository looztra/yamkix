"""Provide tests for the yamkix module."""

import sys
from pathlib import Path
from textwrap import dedent

import pytest
from pytest_mock import MockerFixture

from yamkix.config import YamkixInputOutputConfig, get_default_yamkix_config, get_yamkix_config_from_default
from yamkix.errors import InvalidYamlContentError
from yamkix.yamkix import round_trip_and_format, yamkix_dump_all
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
        round_trip_and_format(config)

        # THENm
        mock_load_all.assert_called_once_with(stdin_read_return_value)
        mock_sys_stdin.read.assert_called_once()
        mock_yamkix_dump_all.assert_called_once()


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
        yaml_parser = get_opinionated_yaml_writer(get_default_yamkix_config())
        yaml_content = yaml_parser.load(dedent(content))
        yamkix_dump_one = mocker.patch("yamkix.yamkix.yamkix_dump_one")
        yamkix_dump_all([yaml_content], yaml_parser, dash_inwards=False, output_file=None, spaces_before_comment=None)
        yamkix_dump_one.assert_called_once_with(
            single_item=yaml_content, yaml=yaml_parser, dash_inwards=False, out=sys.stdout, spaces_before_comment=None
        )
