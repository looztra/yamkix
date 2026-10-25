"""Tests the YamkixConfig stuff."""
# pylint: disable=too-many-lines

from argparse import Namespace
from pathlib import Path

import pytest
from faker import Faker
from pytest_mock import MockerFixture

from yamkix.config import (
    DEFAULT_LINE_WIDTH,
    STDIN_DISPLAY_NAME,
    STDOUT_DISPLAY_NAME,
    YamkixConfig,
    YamkixInputOutputConfig,
    create_yamkix_config_from_typer_args,
    get_config_from_args,
    get_default_yamkix_config,
    get_input_output_config_from_args,
    get_spaces_before_comment_from_args,
    get_yamkix_config_from_default,
    print_yamkix_config,
    raise_enforce_block_style_warning_if_needed,
    raise_enforce_double_quotes_warning_if_needed,
    raise_input_output_warning_if_needed,
)
from yamkix.errors import InvalidTypValueError


class TestYamkixInputOutputConfig:
    """Provide unit tests for the YamkixInputOutputConfig class."""

    def test_get_io_config_when_defaults(self) -> None:
        """Test get_input_output_config_from_args.

        input=None, output=None, stdout=None
        """
        parsed = Namespace(input=None, output=None, stdout=None)
        sut: YamkixInputOutputConfig = get_input_output_config_from_args(parsed)
        assert sut.input is None
        assert sut.input_display_name == "STDIN"
        assert sut.output is None
        assert sut.output_display_name == "STDOUT"

    def test_get_io_config_when_file_input_provided(self) -> None:
        """Test get_input_output_config_from_args.

        input=f_input, output=None, stdout=None
        """
        f_input = "path/to/input"
        parsed = Namespace(input=f_input, output=None, stdout=None)
        sut: YamkixInputOutputConfig = get_input_output_config_from_args(parsed)
        assert sut.input == f_input
        assert sut.input_display_name == f_input
        assert sut.output == f_input
        assert sut.output_display_name == f_input

    def test_get_io_config_when_explicit_stdin_input_provided(self) -> None:
        """Test get_input_output_config_from_args.

        input=STDIN, output=None, stdout=None
        """
        parsed = Namespace(input=STDIN_DISPLAY_NAME, output=None, stdout=None)
        sut: YamkixInputOutputConfig = get_input_output_config_from_args(parsed)
        assert sut.input is None
        assert sut.input_display_name == STDIN_DISPLAY_NAME
        assert sut.output is None
        assert sut.output_display_name == STDOUT_DISPLAY_NAME

    def test_get_io_config_when_explicit_stdin_and_stdout_provided(self) -> None:
        """Test get_input_output_config_from_args.

        input=STDIN, output=STDOUT, stdout=None
        """
        parsed = Namespace(input=STDIN_DISPLAY_NAME, output=STDOUT_DISPLAY_NAME, stdout=None)
        sut: YamkixInputOutputConfig = get_input_output_config_from_args(parsed)
        assert sut.input is None
        assert sut.input_display_name == STDIN_DISPLAY_NAME
        assert sut.output is None
        assert sut.output_display_name == STDOUT_DISPLAY_NAME

    def test_get_io_config_when_file_input_and_output_provided(self) -> None:
        """Test get_input_output_config_from_args.

        input=f_input, output=f_output, stdout=None
        """
        f_input = "path/to/input"
        f_output = "path/to/output"
        parsed = Namespace(input=f_input, output=f_output, stdout=None)
        sut: YamkixInputOutputConfig = get_input_output_config_from_args(parsed)
        assert sut.input == f_input
        assert sut.input_display_name == f_input
        assert sut.output == f_output
        assert sut.output_display_name == f_output

    def test_get_io_config_when_file_input_provided_and_stdout(self) -> None:
        """Test get_input_output_config_from_args.

        input=f_input, output=None, stdout=True
        """
        f_input = "path/to/input"
        parsed = Namespace(input=f_input, output=None, stdout=True)
        sut: YamkixInputOutputConfig = get_input_output_config_from_args(parsed)

        assert sut.input == f_input
        assert sut.input_display_name == f_input
        assert sut.output is None
        assert sut.output_display_name == "STDOUT"

    def test_get_io_config_when_file_input_and_output_provided_and_stdout(
        self,
    ) -> None:
        """Test get_input_output_config_from_args.

        input=f_input, output=f_output, stdout=True
        """
        f_input = "path/to/input"
        f_output = "path/to/output"
        parsed = Namespace(input=f_input, output=f_output, stdout=True)
        sut: YamkixInputOutputConfig = get_input_output_config_from_args(parsed)
        assert sut.input == f_input
        assert sut.input_display_name == f_input
        assert sut.output is None
        assert sut.output_display_name == "STDOUT"

    def test_get_io_config_when_output_stdout(self) -> None:
        """Test get_input_output_config_from_args.

        input=f_input, output=f_output, stdout=None
        """
        f_input = "path/to/input"
        f_output = STDOUT_DISPLAY_NAME
        parsed = Namespace(input=f_input, output=f_output, stdout=None)
        sut: YamkixInputOutputConfig = get_input_output_config_from_args(parsed)
        assert sut.input == f_input
        assert sut.input_display_name == f_input
        assert sut.output is None
        assert sut.output_display_name == STDOUT_DISPLAY_NAME

    def test_get_io_config_when_file_output_provided(self) -> None:
        """Test get_input_output_config_from_args.

        input=None, output=f_output, stdout=None
        """
        f_output = "path/to/output"
        parsed = Namespace(input=None, output=f_output, stdout=None)
        sut: YamkixInputOutputConfig = get_input_output_config_from_args(parsed)

        assert sut.input is None
        assert sut.input_display_name == STDIN_DISPLAY_NAME
        assert sut.output == f_output
        assert sut.output_display_name == f_output


class TestYamkixConfigFromArgs:
    """Provide unit tests related to getting YamkixConfig from args."""

    def test_default_values(self) -> None:
        """Test YamkixConfig default values."""
        sut: YamkixConfig = get_default_yamkix_config()
        assert sut.parsing_mode == "rt"
        assert sut.explicit_start is True
        assert sut.explicit_end is False
        assert sut.default_flow_style is False
        assert sut.dash_inwards is True
        assert sut.quotes_preserved is True
        assert sut.spaces_before_comment is None
        assert sut.line_width == DEFAULT_LINE_WIDTH
        assert sut.enforce_block_style is False
        assert sut.enforce_double_quotes is False
        assert sut.align_comments is False
        assert sut.version is False

    def test_get_config_from_args_with_invalid_typ(self) -> None:
        """Test get_config_from_args.

        typ=yolo
        """
        parsed = Namespace(typ="yolo")
        with pytest.raises(InvalidTypValueError):
            get_config_from_args(parsed)

    def test_get_config_from_args_with_no_args(self) -> None:
        """Test get_config_from_args.

        input=None
        output=None
        stdout=None
        typ="rt"
        no_explicit_start=None
        explicit_end=None
        no_quotes_preserved=None
        default_flow_style=None
        no_dash_inwards=None
        stdout=None
        spaces_before_comment=None
        version=None
        """
        parsed = Namespace(
            input=None,
            output=None,
            stdout=None,
            typ="rt",
            no_explicit_start=None,
            explicit_end=None,
            no_quotes_preserved=None,
            default_flow_style=None,
            no_dash_inwards=None,
            spaces_before_comment=None,
            version=None,
        )
        sut: YamkixConfig = get_config_from_args(parsed)
        sut_io = sut.io_config
        yamkix_default_config = get_default_yamkix_config()
        assert sut_io.input is None
        assert sut_io.input_display_name == "STDIN"
        assert sut_io.output is None
        assert sut_io.output_display_name == "STDOUT"

        assert sut.parsing_mode == yamkix_default_config.parsing_mode
        assert sut.explicit_start == yamkix_default_config.explicit_start
        assert sut.explicit_end == yamkix_default_config.explicit_end
        assert sut.default_flow_style == yamkix_default_config.default_flow_style
        assert sut.dash_inwards == yamkix_default_config.dash_inwards
        assert sut.quotes_preserved == yamkix_default_config.quotes_preserved
        assert sut.spaces_before_comment == yamkix_default_config.spaces_before_comment
        assert sut.line_width == yamkix_default_config.line_width
        assert sut.enforce_block_style == yamkix_default_config.enforce_block_style
        assert sut.version == yamkix_default_config.version

    def test_get_config_from_args_with_no_io(self) -> None:
        """Test get_config_from_args.

        input=None
        output=None
        stdout=None
        typ="rt"
        no_explicit_start=None
        explicit_end=None
        no_quotes_preserved=None
        default_flow_style=None
        no_dash_inwards=None
        stdout=None
        spaces_before_comment=None
        version=None
        inc_io_config=False
        """
        parsed = Namespace(
            input=None,
            output=None,
            stdout=None,
            typ="rt",
            no_explicit_start=None,
            explicit_end=None,
            no_quotes_preserved=None,
            default_flow_style=None,
            no_dash_inwards=None,
            spaces_before_comment=None,
            version=None,
        )
        sut: YamkixConfig = get_config_from_args(parsed, inc_io_config=False)
        assert sut is not None

    def test_get_spaces_before_comment_from_args_when_none(self) -> None:
        """Test get_spaces_before_comment_from_args.

        spaces_before_comment=None
        """
        parsed = Namespace(spaces_before_comment=None)
        sut = get_spaces_before_comment_from_args(parsed)
        assert sut is None

    def test_get_spaces_before_comment_from_args_when_int(self, faker: Faker) -> None:
        """Test get_spaces_before_comment_from_args.

        spaces_before_comment=722
        """
        space_before_comments = faker.random_int(min=1, max=1000)
        parsed = Namespace(spaces_before_comment=space_before_comments)
        sut = get_spaces_before_comment_from_args(parsed)
        assert sut == space_before_comments

    def test_get_spaces_before_comment_from_args_when_invalid(self, faker: Faker) -> None:
        """Test get_spaces_before_comment_from_args.

        spaces_before_comment=yolo
        """
        parsed = Namespace(spaces_before_comment=faker.word())
        sut = get_spaces_before_comment_from_args(parsed)
        assert sut is None


class TestGetYamkixConfigFromDefault:
    """Provide unit tests for get_yamkix_config_from_default."""

    @pytest.mark.parametrize("new_val", [pytest.param("rt", id="rt"), pytest.param("safe", id="safe")])
    def test_get_yamkix_config_from_default_parsing_mode(self, new_val: str) -> None:
        """Test get_yamkix_config_from_default.

        change parsing_mode
        """
        reference = get_yamkix_config_from_default()
        sut = get_yamkix_config_from_default(parsing_mode=new_val)
        assert sut.parsing_mode == new_val
        assert sut.explicit_start == reference.explicit_start
        assert sut.explicit_end == reference.explicit_end
        assert sut.default_flow_style == reference.default_flow_style
        assert sut.dash_inwards == reference.dash_inwards
        assert sut.quotes_preserved == reference.quotes_preserved
        assert sut.spaces_before_comment == reference.spaces_before_comment
        assert sut.line_width == reference.line_width
        assert sut.io_config == reference.io_config

    @pytest.mark.parametrize("parsing_mode", [pytest.param("yolo", id="unknown"), pytest.param("RT", id="upper")])
    def test_get_yamkix_config_from_default_refuses_invalid_parsing_mode(self, parsing_mode: str) -> None:
        """An unknown parser mode is refused when the configuration is built."""
        with pytest.raises(InvalidTypValueError):
            get_yamkix_config_from_default(parsing_mode=parsing_mode)

    def test_get_yamkix_config_from_default_explicit_start(self) -> None:
        """Test get_yamkix_config_from_default.

        change explicit_start
        """
        reference = get_yamkix_config_from_default()
        new_val = not reference.explicit_start
        sut = get_yamkix_config_from_default(explicit_start=new_val)
        assert sut.parsing_mode == reference.parsing_mode
        assert sut.explicit_start == new_val
        assert sut.explicit_end == reference.explicit_end
        assert sut.default_flow_style == reference.default_flow_style
        assert sut.dash_inwards == reference.dash_inwards
        assert sut.quotes_preserved == reference.quotes_preserved
        assert sut.spaces_before_comment == reference.spaces_before_comment
        assert sut.line_width == reference.line_width
        assert sut.io_config == reference.io_config

    def test_get_yamkix_config_from_default_explicit_end(self) -> None:
        """Test get_yamkix_config_from_default.

        change explicit_end
        """
        reference = get_yamkix_config_from_default()
        new_val = not reference.explicit_end
        sut = get_yamkix_config_from_default(explicit_end=new_val)
        assert sut.parsing_mode == reference.parsing_mode
        assert sut.explicit_start == reference.explicit_start
        assert sut.explicit_end == new_val
        assert sut.default_flow_style == reference.default_flow_style
        assert sut.dash_inwards == reference.dash_inwards
        assert sut.quotes_preserved == reference.quotes_preserved
        assert sut.spaces_before_comment == reference.spaces_before_comment
        assert sut.line_width == reference.line_width
        assert sut.io_config == reference.io_config

    def test_get_yamkix_config_from_default_default_flow_style(self) -> None:
        """Test get_yamkix_config_from_default.

        change default_flow_style
        """
        reference = get_yamkix_config_from_default()
        new_val = not reference.default_flow_style
        sut = get_yamkix_config_from_default(default_flow_style=new_val)
        assert sut.parsing_mode == reference.parsing_mode
        assert sut.explicit_start == reference.explicit_start
        assert sut.explicit_end == reference.explicit_end
        assert sut.default_flow_style == new_val
        assert sut.dash_inwards == reference.dash_inwards
        assert sut.quotes_preserved == reference.quotes_preserved
        assert sut.spaces_before_comment == reference.spaces_before_comment
        assert sut.line_width == reference.line_width
        assert sut.io_config == reference.io_config

    def test_get_yamkix_config_from_default_dash_inwards(self) -> None:
        """Test get_yamkix_config_from_default.

        change dash_inwards
        """
        reference = get_yamkix_config_from_default()
        new_val = not reference.dash_inwards
        sut = get_yamkix_config_from_default(dash_inwards=new_val)
        assert sut.parsing_mode == reference.parsing_mode
        assert sut.explicit_start == reference.explicit_start
        assert sut.explicit_end == reference.explicit_end
        assert sut.default_flow_style == reference.default_flow_style
        assert sut.dash_inwards == new_val
        assert sut.quotes_preserved == reference.quotes_preserved
        assert sut.spaces_before_comment == reference.spaces_before_comment
        assert sut.line_width == reference.line_width
        assert sut.io_config == reference.io_config

    def test_get_yamkix_config_from_default_quotes_preserved(self) -> None:
        """Test get_yamkix_config_from_default.

        change quotes_preserved
        """
        reference = get_yamkix_config_from_default()
        new_val = not reference.quotes_preserved
        sut = get_yamkix_config_from_default(quotes_preserved=new_val)
        assert sut.parsing_mode == reference.parsing_mode
        assert sut.explicit_start == reference.explicit_start
        assert sut.explicit_end == reference.explicit_end
        assert sut.default_flow_style == reference.default_flow_style
        assert sut.dash_inwards == reference.dash_inwards
        assert sut.quotes_preserved == new_val
        assert sut.spaces_before_comment == reference.spaces_before_comment
        assert sut.line_width == reference.line_width
        assert sut.io_config == reference.io_config

    def test_get_yamkix_config_from_default_spaces_before_comment(self) -> None:
        """Test get_yamkix_config_from_default.

        change spaces_before_comment
        """
        reference = get_yamkix_config_from_default()
        new_val = 722
        sut = get_yamkix_config_from_default(spaces_before_comment=new_val)
        assert sut.parsing_mode == reference.parsing_mode
        assert sut.explicit_start == reference.explicit_start
        assert sut.explicit_end == reference.explicit_end
        assert sut.default_flow_style == reference.default_flow_style
        assert sut.dash_inwards == reference.dash_inwards
        assert sut.quotes_preserved == reference.quotes_preserved
        assert sut.spaces_before_comment == new_val
        assert sut.line_width == reference.line_width
        assert sut.io_config == reference.io_config

    def test_get_yamkix_config_from_default_line_width(self) -> None:
        """Test get_yamkix_config_from_default.

        change line_width
        """
        reference = get_yamkix_config_from_default()
        new_val = 722
        sut = get_yamkix_config_from_default(line_width=new_val)
        assert sut.parsing_mode == reference.parsing_mode
        assert sut.explicit_start == reference.explicit_start
        assert sut.explicit_end == reference.explicit_end
        assert sut.default_flow_style == reference.default_flow_style
        assert sut.dash_inwards == reference.dash_inwards
        assert sut.quotes_preserved == reference.quotes_preserved
        assert sut.spaces_before_comment == reference.spaces_before_comment
        assert sut.line_width == new_val
        assert sut.io_config == reference.io_config

    def test_get_yamkix_config_from_default_enforce_double_quotes(self) -> None:
        """Test get_yamkix_config_from_default.

        change enforce_double_quotes
        """
        reference = get_yamkix_config_from_default()
        sut = get_yamkix_config_from_default(enforce_double_quotes=True)
        assert sut.parsing_mode == reference.parsing_mode
        assert sut.explicit_start == reference.explicit_start
        assert sut.explicit_end == reference.explicit_end
        assert sut.default_flow_style == reference.default_flow_style
        assert sut.dash_inwards == reference.dash_inwards
        assert sut.quotes_preserved == reference.quotes_preserved
        assert sut.spaces_before_comment == reference.spaces_before_comment
        assert sut.enforce_double_quotes is True
        assert sut.line_width == reference.line_width
        assert sut.io_config == reference.io_config

    def test_get_yamkix_config_from_default_enforce_block_style(self) -> None:
        """Test get_yamkix_config_from_default.

        change enforce_block_style
        """
        reference = get_yamkix_config_from_default()
        sut = get_yamkix_config_from_default(enforce_block_style=True)
        assert sut.parsing_mode == reference.parsing_mode
        assert sut.explicit_start == reference.explicit_start
        assert sut.explicit_end == reference.explicit_end
        assert sut.default_flow_style == reference.default_flow_style
        assert sut.dash_inwards == reference.dash_inwards
        assert sut.quotes_preserved == reference.quotes_preserved
        assert sut.spaces_before_comment == reference.spaces_before_comment
        assert sut.enforce_block_style is True
        assert sut.line_width == reference.line_width
        assert sut.io_config == reference.io_config

    def test_get_yamkix_config_from_default_io_config(self) -> None:
        """Test get_yamkix_config_from_default.

        change io_config
        """
        reference = get_yamkix_config_from_default()
        new_val = YamkixInputOutputConfig(input="f_input", output="f_output")

        sut = get_yamkix_config_from_default(io_config=new_val)
        assert sut.parsing_mode == reference.parsing_mode
        assert sut.explicit_start == reference.explicit_start
        assert sut.explicit_end == reference.explicit_end
        assert sut.default_flow_style == reference.default_flow_style
        assert sut.dash_inwards == reference.dash_inwards
        assert sut.quotes_preserved == reference.quotes_preserved
        assert sut.spaces_before_comment == reference.spaces_before_comment
        assert sut.line_width == reference.line_width
        assert sut.io_config == new_val


class TestCreateYamkixConfigFromTyperArgs:
    """Provide unit tests for the Typer CLI."""

    def test_create_yamkix_config_from_typer_args(self) -> None:
        """Test the config creation function."""
        configs = create_yamkix_config_from_typer_args(
            input_file="test.yaml",
            output_file="output.yaml",
            stdout=False,
            typ="rt",
            no_explicit_start=False,
            explicit_end=True,
            no_quotes_preserved=False,
            default_flow_style=True,
            no_dash_inwards=False,
            spaces_before_comment=1,
            enforce_double_quotes=False,
            line_width=DEFAULT_LINE_WIDTH,
            align_comments=False,
            files=None,
        )

        assert len(configs) == 1
        assert configs[0].io_config.input == "test.yaml"
        assert configs[0].io_config.output == "output.yaml"
        assert configs[0].parsing_mode == "rt"
        assert configs[0].explicit_start  # not no_explicit_start
        assert configs[0].explicit_end
        assert configs[0].quotes_preserved  # not no_quotes_preserved
        assert configs[0].default_flow_style
        assert configs[0].dash_inwards  # not no_dash_inwards
        assert configs[0].spaces_before_comment == 1
        assert configs[0].enforce_double_quotes is False
        assert configs[0].enforce_block_style is False

    def test_create_yamkix_config_from_typer_args_enforce_block_style(self) -> None:
        """Test the config creation function with enforce_block_style set."""
        configs = create_yamkix_config_from_typer_args(
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
            enforce_double_quotes=False,
            line_width=DEFAULT_LINE_WIDTH,
            align_comments=False,
            files=None,
            enforce_block_style=True,
        )

        assert len(configs) == 1
        assert configs[0].enforce_block_style is True

    def test_create_yamkix_config_stdout_override(self) -> None:
        """Test that stdout option overrides output file."""
        configs = create_yamkix_config_from_typer_args(
            input_file="test.yaml",
            output_file="output.yaml",
            stdout=True,  # This should override output_file
            typ="rt",
            no_explicit_start=False,
            explicit_end=False,
            no_quotes_preserved=False,
            default_flow_style=False,
            no_dash_inwards=False,
            spaces_before_comment=None,
            enforce_double_quotes=False,
            line_width=DEFAULT_LINE_WIDTH,
            align_comments=False,
            files=None,
        )
        assert len(configs) == 1
        assert configs[0].io_config.input == "test.yaml"
        assert configs[0].io_config.output is None  # Should be None due to stdout=True

    def test_create_yamkix_config_defaults(self) -> None:
        """Test default configuration values."""
        configs = create_yamkix_config_from_typer_args(
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
            enforce_double_quotes=False,
            line_width=DEFAULT_LINE_WIDTH,
            align_comments=False,
            files=None,
        )

        default_config = get_default_yamkix_config()
        assert len(configs) == 1
        assert configs[0].parsing_mode == default_config.parsing_mode
        assert configs[0].explicit_start == default_config.explicit_start
        assert configs[0].explicit_end == default_config.explicit_end
        assert configs[0].default_flow_style == default_config.default_flow_style
        assert configs[0].dash_inwards == default_config.dash_inwards
        assert configs[0].quotes_preserved == default_config.quotes_preserved
        assert configs[0].spaces_before_comment == default_config.spaces_before_comment

    def test_create_yamkix_config_negated_flags(self) -> None:
        """Test negated boolean flags work correctly."""
        configs = create_yamkix_config_from_typer_args(
            input_file=None,
            output_file=None,
            stdout=False,
            typ="safe",
            no_explicit_start=True,
            explicit_end=False,
            no_quotes_preserved=True,
            default_flow_style=False,
            no_dash_inwards=True,
            spaces_before_comment=None,
            enforce_double_quotes=False,
            line_width=DEFAULT_LINE_WIDTH,
            align_comments=False,
            files=None,
        )

        assert len(configs) == 1
        assert configs[0].parsing_mode == "safe"
        assert not configs[0].explicit_start  # no_explicit_start=True
        assert not configs[0].explicit_end
        assert not configs[0].quotes_preserved  # no_quotes_preserved=True
        assert not configs[0].default_flow_style
        assert not configs[0].dash_inwards  # no_dash_inwards=True

    def test_create_yamkix_config_io_logic_with_input_file(self) -> None:
        """Test input/output file logic."""
        # Test case: input file but no output specified -> output should be same as input
        configs = create_yamkix_config_from_typer_args(
            input_file="input.yaml",
            output_file=None,
            stdout=False,
            typ="rt",
            no_explicit_start=False,
            explicit_end=False,
            no_quotes_preserved=False,
            default_flow_style=False,
            no_dash_inwards=False,
            spaces_before_comment=None,
            enforce_double_quotes=False,
            line_width=DEFAULT_LINE_WIDTH,
            align_comments=False,
            files=None,
        )
        assert configs[0].io_config.input == "input.yaml"
        assert configs[0].io_config.output == "input.yaml"

    def test_create_yamkix_config_io_logic_with_output_file(self) -> None:
        """Test input/output file logic."""
        # Test case: no input file but output specified -> output should be the specified file
        configs = create_yamkix_config_from_typer_args(
            input_file=None,
            output_file="output.yaml",
            stdout=False,
            typ="rt",
            no_explicit_start=False,
            explicit_end=False,
            no_quotes_preserved=False,
            default_flow_style=False,
            no_dash_inwards=False,
            spaces_before_comment=None,
            enforce_double_quotes=False,
            line_width=DEFAULT_LINE_WIDTH,
            align_comments=False,
            files=None,
        )
        assert configs[0].io_config.input is None
        assert configs[0].io_config.output == "output.yaml"

    def test_create_yamkix_config_io_logic_with_input_none_and_output_none(self) -> None:
        """Test input/output file logic."""
        # Test case: no input file and no output -> output should be None (STDOUT)
        configs = create_yamkix_config_from_typer_args(
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
            enforce_double_quotes=False,
            line_width=DEFAULT_LINE_WIDTH,
            align_comments=False,
            files=None,
        )
        assert configs[0].io_config.input is None
        assert configs[0].io_config.output is None

    @pytest.mark.parametrize(
        "input_file",
        [
            pytest.param(STDIN_DISPLAY_NAME, id="STDIN"),
            pytest.param("StDin", id="StDin"),
            pytest.param(STDIN_DISPLAY_NAME.lower(), id="stdin"),
        ],
    )
    def test_create_yamkix_config_io_logic_with_explicit_stdin_as_input(self, input_file: str) -> None:
        """Test input/output file logic."""
        # Test case: input set explicitly to STDIN and no output -> output should be None (STDOUT)
        configs = create_yamkix_config_from_typer_args(
            input_file=input_file,
            output_file=None,
            stdout=False,
            typ="rt",
            no_explicit_start=False,
            explicit_end=False,
            no_quotes_preserved=False,
            default_flow_style=False,
            no_dash_inwards=False,
            spaces_before_comment=None,
            enforce_double_quotes=False,
            line_width=DEFAULT_LINE_WIDTH,
            align_comments=False,
            files=None,
        )
        assert configs[0].io_config.input is None
        assert configs[0].io_config.output is None

    @pytest.mark.parametrize(
        "output_file",
        [
            pytest.param(STDOUT_DISPLAY_NAME, id="STDOUT"),
            pytest.param("StDout", id="StDout"),
            pytest.param(STDOUT_DISPLAY_NAME.lower(), id="stdout"),
        ],
    )
    def test_create_yamkix_config_io_logic_with_explicit_stdout_as_output(self, output_file: str) -> None:
        """Test input/output file logic."""
        # Test case: output is "STDOUT" -> output should be None
        configs = create_yamkix_config_from_typer_args(
            input_file="input.yaml",
            output_file=output_file,
            stdout=False,
            typ="rt",
            no_explicit_start=False,
            explicit_end=False,
            no_quotes_preserved=False,
            default_flow_style=False,
            no_dash_inwards=False,
            spaces_before_comment=None,
            enforce_double_quotes=False,
            line_width=DEFAULT_LINE_WIDTH,
            align_comments=False,
            files=None,
        )
        assert configs[0].io_config.input == "input.yaml"
        assert configs[0].io_config.output is None

    def test_create_yamkix_config_io_logic_with_single_argument(self, shared_datadir: Path) -> None:
        """Test input/output file logic."""
        test_file1 = shared_datadir / "simple.yml"
        configs = create_yamkix_config_from_typer_args(
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
            enforce_double_quotes=False,
            line_width=DEFAULT_LINE_WIDTH,
            align_comments=False,
            files=[test_file1],
        )
        assert configs[0].io_config.input == str(test_file1)
        assert configs[0].io_config.output == str(test_file1)

    def test_create_yamkix_config_io_logic_with_two_arguments(self, shared_datadir: Path) -> None:
        """Test input/output file logic."""
        test_file1 = shared_datadir / "simple.yml"
        test_file2 = shared_datadir / "multi-doc-1.yml"
        input_files = [test_file1, test_file2]
        configs = create_yamkix_config_from_typer_args(
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
            enforce_double_quotes=False,
            line_width=DEFAULT_LINE_WIDTH,
            align_comments=False,
            files=input_files,
        )
        assert len(configs) == len(input_files)
        assert configs[0].io_config.input == str(test_file1)
        assert configs[0].io_config.output == str(test_file1)
        assert configs[1].io_config.input == str(test_file2)
        assert configs[1].io_config.output == str(test_file2)

    def test_create_yamkix_config_io_logic_with_empty_files(self) -> None:
        """Test input/output file logic."""
        with pytest.raises(ValueError, match=r"The 'files' argument cannot be an empty list."):
            create_yamkix_config_from_typer_args(
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
                enforce_double_quotes=False,
                line_width=DEFAULT_LINE_WIDTH,
                align_comments=False,
                files=[],
            )


class TestPrintYamkixConfig:
    """Provide unit tests for print_yamkix_config function."""

    def test_yamkix_input_output_config_str_with_file_paths(self) -> None:
        """Test __str__ method of YamkixInputOutputConfig with file paths."""
        # GIVEN
        config = YamkixInputOutputConfig(input="input.yaml", output="output.yaml")

        # WHEN
        result = str(config)

        # THEN
        assert result == "input=input.yaml, output=output.yaml"

    def test_yamkix_config_str_with_default_values(self) -> None:
        """Test __str__ method of YamkixConfig with default values."""
        # GIVEN
        config = get_default_yamkix_config()

        # WHEN
        result = str(config)

        # THEN
        expected = (
            "typ=rt, explicit_start=True, explicit_end=False, default_flow_style=False, "
            "quotes_preserved=True, enforce_double_quotes=False, enforce_block_style=False, "
            "dash_inwards=True, spaces_before_comment=None"
            ", line_width=2048, align_comments=False"
        )
        assert result == expected

    def test_print_yamkix_config_calls_stderr_console(self, mocker: MockerFixture) -> None:
        """Test that print_yamkix_config calls typer_echo with correct message."""
        # GIVEN
        mock_get_stderr_console = mocker.patch("yamkix.config.get_stderr_console")
        mock_console = mocker.Mock()
        mock_get_stderr_console.return_value = mock_console
        config = get_default_yamkix_config()

        # WHEN
        print_yamkix_config(config)

        # THEN
        mock_console.print.assert_called_once()
        args, _ = mock_console.print.call_args

        # Verify the message contains expected content
        message = args[0]
        assert "yamkix" in message
        assert "Processing:" in message
        assert "input=STDIN" in message
        assert "output=STDOUT" in message
        assert "typ=rt" in message
        assert "explicit_start=True" in message
        assert "explicit_end=False" in message
        assert "default_flow_style=False" in message
        assert "quotes_preserved=True" in message
        assert "enforce_block_style=False" in message
        assert "dash_inwards=True" in message
        assert "spaces_before_comment=None" in message


class TestRaiseEnforceDoubleQuotesWarning:
    """Test the raise_enforce_double_quotes_warning_if_needed function."""

    def test_warning_is_raised(self, mocker: MockerFixture) -> None:
        """Test that a warning is raised when needed."""
        mock_get_stderr_console = mocker.patch("yamkix.config.get_stderr_console")
        mock_console = mocker.Mock()
        mock_get_stderr_console.return_value = mock_console

        # WHEN
        raise_enforce_double_quotes_warning_if_needed(
            enforce_double_quotes=True,
            no_quotes_preserved=False,
            typ="rt",
        )

        # THEN
        mock_console.print.assert_called_once()
        args, _ = mock_console.print.call_args
        assert (
            "WARNING: Option '--enforce-double-quotes' is useless unless '--no-quotes-preserved' is also set."
            in args[0]
        )

    def test_warning_is_raised_in_safe_mode(self, mocker: MockerFixture) -> None:
        """Safe mode keeps no quote kind, so the option is reported as having no effect."""
        mock_get_stderr_console = mocker.patch("yamkix.config.get_stderr_console")
        mock_console = mocker.Mock()
        mock_get_stderr_console.return_value = mock_console

        # WHEN
        raise_enforce_double_quotes_warning_if_needed(
            enforce_double_quotes=True,
            no_quotes_preserved=True,
            typ="safe",
        )

        # THEN
        mock_console.print.assert_called_once()
        args, _ = mock_console.print.call_args
        assert "WARNING: Option '--enforce-double-quotes' has no effect with '--typ safe'." in args[0]

    @pytest.mark.parametrize(
        ("enforce_double_quotes", "no_quotes_preserved", "typ"),
        [
            pytest.param(True, True, "rt", id="both_set"),
            pytest.param(False, False, "rt", id="neither_set"),
            pytest.param(False, True, "rt", id="only_no_quotes_set"),
            pytest.param(False, True, "safe", id="only_no_quotes_set_safe"),
        ],
    )
    def test_no_warning_is_raised(
        self, mocker: MockerFixture, enforce_double_quotes: bool, no_quotes_preserved: bool, typ: str
    ) -> None:
        """Test that no warning is raised when not needed."""
        mock_get_stderr_console = mocker.patch("yamkix.config.get_stderr_console")
        mock_console = mocker.Mock()
        mock_get_stderr_console.return_value = mock_console

        # WHEN
        raise_enforce_double_quotes_warning_if_needed(
            enforce_double_quotes=enforce_double_quotes,
            no_quotes_preserved=no_quotes_preserved,
            typ=typ,
        )

        # THEN
        mock_console.print.assert_not_called()


class TestRaiseEnforceBlockStyleWarning:
    """Test the raise_enforce_block_style_warning_if_needed function."""

    def test_warning_is_raised(self, mocker: MockerFixture) -> None:
        """Test that a warning is raised when needed."""
        mock_get_stderr_console = mocker.patch("yamkix.config.get_stderr_console")
        mock_console = mocker.Mock()
        mock_get_stderr_console.return_value = mock_console

        # WHEN
        raise_enforce_block_style_warning_if_needed(
            enforce_block_style=True,
            default_flow_style=True,
            typ="rt",
        )

        # THEN
        mock_console.print.assert_called_once()
        args, _ = mock_console.print.call_args
        assert "WARNING: Option '--enforce-block-style' overrides '--default-flow-style'" in args[0]

    @pytest.mark.parametrize(
        ("default_flow_style", "expected"),
        [
            pytest.param(False, "no effect with '--typ safe'.", id="alone"),
            pytest.param(True, "dumped in flow style because of '--default-flow-style'", id="with_default_flow_style"),
        ],
    )
    def test_warning_is_raised_in_safe_mode(
        self, mocker: MockerFixture, default_flow_style: bool, expected: str
    ) -> None:
        """Safe mode ignores the option, and the warning says what the output will be."""
        mock_get_stderr_console = mocker.patch("yamkix.config.get_stderr_console")
        mock_console = mocker.Mock()
        mock_get_stderr_console.return_value = mock_console

        # WHEN
        raise_enforce_block_style_warning_if_needed(
            enforce_block_style=True,
            default_flow_style=default_flow_style,
            typ="safe",
        )

        # THEN
        mock_console.print.assert_called_once()
        args, _ = mock_console.print.call_args
        assert "WARNING: Option '--enforce-block-style' has no effect with '--typ safe'." in args[0]
        assert expected in args[0]
        assert "overrides" not in args[0]

    @pytest.mark.parametrize(
        ("enforce_block_style", "default_flow_style", "typ"),
        [
            pytest.param(False, False, "rt", id="neither_set"),
            pytest.param(True, False, "rt", id="only_enforce_block_style_set"),
            pytest.param(False, True, "rt", id="only_default_flow_style_set"),
            pytest.param(False, True, "safe", id="only_default_flow_style_set_safe"),
        ],
    )
    def test_no_warning_is_raised(
        self, mocker: MockerFixture, enforce_block_style: bool, default_flow_style: bool, typ: str
    ) -> None:
        """Test that no warning is raised when not needed."""
        mock_get_stderr_console = mocker.patch("yamkix.config.get_stderr_console")
        mock_console = mocker.Mock()
        mock_get_stderr_console.return_value = mock_console

        # WHEN
        raise_enforce_block_style_warning_if_needed(
            enforce_block_style=enforce_block_style,
            default_flow_style=default_flow_style,
            typ=typ,
        )

        # THEN
        mock_console.print.assert_not_called()


class TestRaiseInputOutputWarningIfNeeded:
    """Test the raise_input_output_warning_if_needed function."""

    @pytest.mark.parametrize(
        ("input_f", "output_f", "stdout"),
        [
            pytest.param("file.yml", None, False, id="input_only"),
            pytest.param("file.yml", None, True, id="input_stdout"),
            pytest.param("file.yml", "plouf.yml", False, id="input_output"),
            pytest.param("file.yml", "plouf.yml", True, id="input_output_stdout"),
            pytest.param(None, "plouf.yml", False, id="output_only"),
            pytest.param(None, "plouf.yml", True, id="output_stdout"),
            pytest.param(None, None, True, id="stdout_only"),
        ],
    )
    def test_warning_is_raised(
        self, tmp_path: Path, mocker: MockerFixture, input_f: str, output_f: str, stdout: bool
    ) -> None:
        """Test that a warning is raised when needed."""
        files = [tmp_path / "input.yaml"]
        mock_get_stderr_console = mocker.patch("yamkix.config.get_stderr_console")
        mock_console = mocker.Mock()
        mock_get_stderr_console.return_value = mock_console

        # WHEN
        raise_input_output_warning_if_needed(
            files=files,
            input_file=input_f,
            output_file=output_f,
            stdout=stdout,
        )

        # THEN
        mock_console.print.assert_called_once()
        args, _ = mock_console.print.call_args
        assert "WARNING" in args[0]
        assert "input" in args[0]
        assert "output" in args[0]
        assert "stdout" in args[0]
        assert "not honored" in args[0]

    @pytest.mark.parametrize(
        ("input_f", "output_f", "stdout"),
        [
            pytest.param("file.yml", None, False, id="input_only"),
            pytest.param("file.yml", None, True, id="input_stdout"),
            pytest.param("file.yml", "plouf.yml", False, id="input_output"),
            pytest.param("file.yml", "plouf.yml", True, id="input_output_stdout"),
            pytest.param(None, "plouf.yml", False, id="output_only"),
            pytest.param(None, "plouf.yml", True, id="output_stdout"),
            pytest.param(None, None, True, id="stdout_only"),
        ],
    )
    def test_warning_is_not_raised(self, mocker: MockerFixture, input_f: str, output_f: str, stdout: bool) -> None:
        """Test that a warning is not raised when not needed."""
        mock_get_stderr_console = mocker.patch("yamkix.config.get_stderr_console")
        mock_console = mocker.Mock()
        mock_get_stderr_console.return_value = mock_console

        # WHEN
        raise_input_output_warning_if_needed(
            files=None,
            input_file=input_f,
            output_file=output_f,
            stdout=stdout,
        )

        # THEN
        mock_console.print.assert_not_called()
