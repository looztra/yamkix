"""Test the yaml_writer init stuff."""

from typing import TYPE_CHECKING

import pytest

from yamkix.config import (
    DEFAULT_LINE_WIDTH,
    YamkixConfig,
    YamkixInputOutputConfig,
    get_default_yamkix_config,
)
from yamkix.yaml_writer import (
    OPINIONATED_MAPPING_VALUE,
    OPINIONATED_OFFSET_VALUE,
    OPINIONATED_SEQUENCE_VALUE,
    get_opinionated_yaml_writer,
)

if TYPE_CHECKING:
    from ruamel.yaml import YAML

# Constants for testing
CUSTOM_LINE_WIDTH_120 = 120
CUSTOM_LINE_WIDTH_80 = 80
CUSTOM_LINE_WIDTH_100 = 100
CUSTOM_LINE_WIDTH_200 = 200
CUSTOM_LINE_WIDTH_1024 = 1024
RUAMEL_DEFAULT_MAP_INDENT = 2
RUAMEL_DEFAULT_SEQUENCE_INDENT = 4
RUAMEL_DEFAULT_SEQUENCE_DASH_OFFSET = 2


def test_get_opinionated_yaml_writer_with_defaults() -> None:
    """Test get_opinionated_yaml_writer default values."""
    sut: YAML = get_opinionated_yaml_writer(get_default_yamkix_config())
    assert sut.typ == ["rt"]
    assert sut.explicit_start is True
    assert sut.explicit_end is False
    assert sut.default_flow_style is False
    assert sut.preserve_quotes is True
    assert sut.map_indent == OPINIONATED_MAPPING_VALUE
    assert sut.sequence_dash_offset == OPINIONATED_OFFSET_VALUE
    assert sut.sequence_indent == OPINIONATED_SEQUENCE_VALUE
    assert sut.width == DEFAULT_LINE_WIDTH


class TestGetOpinionatedYamlWriter:
    """Provide comprehensive unit tests for get_opinionated_yaml_writer function."""

    def test_safe_parsing_mode(self) -> None:
        """Test YAML writer with safe parsing mode."""
        # GIVEN
        config = YamkixConfig(
            parsing_mode="safe",
            explicit_start=True,
            explicit_end=False,
            default_flow_style=False,
            dash_inwards=True,
            quotes_preserved=True,
            spaces_before_comment=None,
            line_width=DEFAULT_LINE_WIDTH,
            enforce_double_quotes=False,
            version=False,
            io_config=YamkixInputOutputConfig(input=None, output=None),
        )

        # WHEN
        yaml_writer = get_opinionated_yaml_writer(config)

        # THEN
        assert yaml_writer.typ == ["safe"]
        assert yaml_writer.explicit_start is True
        assert yaml_writer.explicit_end is False
        assert yaml_writer.default_flow_style is False
        assert yaml_writer.preserve_quotes is True
        assert yaml_writer.width == DEFAULT_LINE_WIDTH

    def test_rt_parsing_mode(self) -> None:
        """Test YAML writer with rt (round-trip) parsing mode."""
        # GIVEN
        config = YamkixConfig(
            parsing_mode="rt",
            explicit_start=False,
            explicit_end=True,
            default_flow_style=True,
            dash_inwards=False,
            quotes_preserved=False,
            spaces_before_comment=2,
            enforce_double_quotes=False,
            line_width=CUSTOM_LINE_WIDTH_120,
            version=False,
            io_config=YamkixInputOutputConfig(input=None, output=None),
        )

        # WHEN
        yaml_writer = get_opinionated_yaml_writer(config)

        # THEN
        assert yaml_writer.typ == ["rt"]
        assert yaml_writer.explicit_start is False
        assert yaml_writer.explicit_end is True
        assert yaml_writer.default_flow_style is True
        assert yaml_writer.preserve_quotes is False
        assert yaml_writer.width == CUSTOM_LINE_WIDTH_120

    def test_dash_inwards_enabled(self) -> None:
        """Test YAML writer with dash_inwards enabled (default behavior)."""
        # GIVEN
        config = YamkixConfig(
            parsing_mode="rt",
            explicit_start=True,
            explicit_end=False,
            default_flow_style=False,
            dash_inwards=True,  # This should trigger the indent configuration
            quotes_preserved=True,
            spaces_before_comment=None,
            enforce_double_quotes=False,
            line_width=DEFAULT_LINE_WIDTH,
            version=False,
            io_config=YamkixInputOutputConfig(input=None, output=None),
        )

        # WHEN
        yaml_writer = get_opinionated_yaml_writer(config)

        # THEN
        assert yaml_writer.map_indent == OPINIONATED_MAPPING_VALUE
        assert yaml_writer.sequence_dash_offset == OPINIONATED_OFFSET_VALUE
        assert yaml_writer.sequence_indent == OPINIONATED_SEQUENCE_VALUE

    def test_dash_inwards_disabled(self) -> None:
        """Test YAML writer with dash_inwards disabled."""
        # GIVEN
        config = YamkixConfig(
            parsing_mode="rt",
            explicit_start=True,
            explicit_end=False,
            default_flow_style=False,
            dash_inwards=False,  # This should NOT trigger the indent configuration
            quotes_preserved=True,
            spaces_before_comment=None,
            enforce_double_quotes=False,
            line_width=DEFAULT_LINE_WIDTH,
            version=False,
            io_config=YamkixInputOutputConfig(input=None, output=None),
        )

        # WHEN
        yaml_writer = get_opinionated_yaml_writer(config)

        # THEN
        # When dash_inwards is False, the indent method is not called,
        # so the YAML writer indentation properties should be their defaults
        assert yaml_writer.map_indent is None
        assert yaml_writer.sequence_indent is None
        assert yaml_writer.sequence_dash_offset == 0  # Default value for ruamel.yaml

    def test_custom_line_width(self) -> None:
        """Test YAML writer with custom line width."""
        # GIVEN
        custom_width = 80
        config = YamkixConfig(
            parsing_mode="rt",
            explicit_start=True,
            explicit_end=False,
            default_flow_style=False,
            dash_inwards=True,
            quotes_preserved=True,
            spaces_before_comment=None,
            enforce_double_quotes=False,
            line_width=custom_width,
            version=False,
            io_config=YamkixInputOutputConfig(input=None, output=None),
        )

        # WHEN
        yaml_writer = get_opinionated_yaml_writer(config)

        # THEN
        assert yaml_writer.width == custom_width

    def test_all_flags_disabled(self) -> None:
        """Test YAML writer with all boolean flags disabled."""
        # GIVEN
        config = YamkixConfig(
            parsing_mode="safe",
            explicit_start=False,
            explicit_end=False,
            default_flow_style=False,
            dash_inwards=False,
            quotes_preserved=False,
            spaces_before_comment=None,
            enforce_double_quotes=False,
            line_width=CUSTOM_LINE_WIDTH_100,
            version=False,
            io_config=YamkixInputOutputConfig(input=None, output=None),
        )

        # WHEN
        yaml_writer = get_opinionated_yaml_writer(config)

        # THEN
        assert yaml_writer.typ == ["safe"]
        assert yaml_writer.explicit_start is False
        assert yaml_writer.explicit_end is False
        assert yaml_writer.default_flow_style is False
        assert yaml_writer.preserve_quotes is False
        assert yaml_writer.width == CUSTOM_LINE_WIDTH_100

    def test_all_flags_enabled(self) -> None:
        """Test YAML writer with all boolean flags enabled."""
        # GIVEN
        config = YamkixConfig(
            parsing_mode="rt",
            explicit_start=True,
            explicit_end=True,
            default_flow_style=True,
            dash_inwards=True,
            quotes_preserved=True,
            spaces_before_comment=1,
            enforce_double_quotes=True,
            line_width=CUSTOM_LINE_WIDTH_200,
            version=True,
            io_config=YamkixInputOutputConfig(input="test.yaml", output="output.yaml"),
        )

        # WHEN
        yaml_writer = get_opinionated_yaml_writer(config)

        # THEN
        assert yaml_writer.typ == ["rt"]
        assert yaml_writer.explicit_start is True
        assert yaml_writer.explicit_end is True
        assert yaml_writer.default_flow_style is True
        assert yaml_writer.preserve_quotes is True
        assert yaml_writer.width == CUSTOM_LINE_WIDTH_200
        assert yaml_writer.map_indent == OPINIONATED_MAPPING_VALUE
        assert yaml_writer.sequence_dash_offset == OPINIONATED_OFFSET_VALUE
        assert yaml_writer.sequence_indent == OPINIONATED_SEQUENCE_VALUE

    @pytest.mark.parametrize(
        "parsing_mode",
        [
            pytest.param("safe", id="safe-mode"),
            pytest.param("rt", id="rt-mode"),
        ],
    )
    def test_parsing_modes(self, parsing_mode: str) -> None:
        """Test YAML writer with different parsing modes."""
        # GIVEN
        config = YamkixConfig(
            parsing_mode=parsing_mode,
            explicit_start=True,
            explicit_end=False,
            default_flow_style=False,
            dash_inwards=True,
            quotes_preserved=True,
            spaces_before_comment=None,
            enforce_double_quotes=False,
            line_width=DEFAULT_LINE_WIDTH,
            version=False,
            io_config=YamkixInputOutputConfig(input=None, output=None),
        )

        # WHEN
        yaml_writer = get_opinionated_yaml_writer(config)

        # THEN
        assert yaml_writer.typ == [parsing_mode]

    @pytest.mark.parametrize(
        "line_width",
        [
            pytest.param(CUSTOM_LINE_WIDTH_80, id="width-80"),
            pytest.param(CUSTOM_LINE_WIDTH_120, id="width-120"),
            pytest.param(CUSTOM_LINE_WIDTH_200, id="width-200"),
            pytest.param(CUSTOM_LINE_WIDTH_1024, id="width-1024"),
        ],
    )
    def test_different_line_widths(self, line_width: int) -> None:
        """Test YAML writer with different line widths."""
        # GIVEN
        config = YamkixConfig(
            parsing_mode="rt",
            explicit_start=True,
            explicit_end=False,
            default_flow_style=False,
            dash_inwards=True,
            quotes_preserved=True,
            spaces_before_comment=None,
            enforce_double_quotes=False,
            line_width=line_width,
            version=False,
            io_config=YamkixInputOutputConfig(input=None, output=None),
        )

        # WHEN
        yaml_writer = get_opinionated_yaml_writer(config)

        # THEN
        assert yaml_writer.width == line_width
