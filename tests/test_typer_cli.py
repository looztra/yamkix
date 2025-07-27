"""Tests for the Typer-based CLI implementation."""

from yamkix.config import get_default_yamkix_config
from yamkix.typer_cli import create_yamkix_config_from_typer_args


class TestTyperCli:
    """Provide unit tests for the Typer CLI."""

    def test_create_yamkix_config_from_typer_args(self) -> None:
        """Test the config creation function."""
        config = create_yamkix_config_from_typer_args(
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
            version=False,
        )

        assert config.io_config.input == "test.yaml"
        assert config.io_config.output == "output.yaml"
        assert config.parsing_mode == "rt"
        assert config.explicit_start  # not no_explicit_start
        assert config.explicit_end
        assert config.quotes_preserved  # not no_quotes_preserved
        assert config.default_flow_style
        assert config.dash_inwards  # not no_dash_inwards
        assert config.spaces_before_comment == 1

    def test_create_yamkix_config_stdout_override(self) -> None:
        """Test that stdout option overrides output file."""
        config = create_yamkix_config_from_typer_args(
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
            version=False,
        )

        assert config.io_config.input == "test.yaml"
        assert config.io_config.output is None  # Should be None due to stdout=True

    def test_create_yamkix_config_defaults(self) -> None:
        """Test default configuration values."""
        config = create_yamkix_config_from_typer_args(
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
            version=False,
        )

        default_config = get_default_yamkix_config()
        assert config.parsing_mode == default_config.parsing_mode
        assert config.explicit_start == default_config.explicit_start
        assert config.explicit_end == default_config.explicit_end
        assert config.default_flow_style == default_config.default_flow_style
        assert config.dash_inwards == default_config.dash_inwards
        assert config.quotes_preserved == default_config.quotes_preserved
        assert config.spaces_before_comment == default_config.spaces_before_comment

    def test_create_yamkix_config_negated_flags(self) -> None:
        """Test negated boolean flags work correctly."""
        config = create_yamkix_config_from_typer_args(
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
            version=False,
        )

        assert config.parsing_mode == "safe"
        assert not config.explicit_start  # no_explicit_start=True
        assert not config.explicit_end
        assert not config.quotes_preserved  # no_quotes_preserved=True
        assert not config.default_flow_style
        assert not config.dash_inwards  # no_dash_inwards=True

    def test_create_yamkix_config_io_logic(self) -> None:
        """Test input/output file logic."""
        # Test case: input file but no output specified -> output should be same as input
        config = create_yamkix_config_from_typer_args(
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
            version=False,
        )
        assert config.io_config.input == "input.yaml"
        assert config.io_config.output == "input.yaml"

        # Test case: no input file but output specified -> output should be the specified file
        config = create_yamkix_config_from_typer_args(
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
            version=False,
        )
        assert config.io_config.input is None
        assert config.io_config.output == "output.yaml"

        # Test case: no input file and no output -> output should be None (STDOUT)
        config = create_yamkix_config_from_typer_args(
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
            version=False,
        )
        assert config.io_config.input is None
        assert config.io_config.output is None

        # Test case: output is "STDOUT" -> output should be None
        config = create_yamkix_config_from_typer_args(
            input_file="input.yaml",
            output_file="STDOUT",
            stdout=False,
            typ="rt",
            no_explicit_start=False,
            explicit_end=False,
            no_quotes_preserved=False,
            default_flow_style=False,
            no_dash_inwards=False,
            spaces_before_comment=None,
            version=False,
        )
        assert config.io_config.input == "input.yaml"
        assert config.io_config.output is None
