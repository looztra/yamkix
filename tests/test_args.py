"""Tests the args parsing."""

from yamkix.args import get_override_or_default, parse_cli
from yamkix.config import YamkixConfig, get_default_yamkix_config


class TestArgs:
    """Provide unit tests for the args package."""

    def test_defaults(self) -> None:
        """Test when no input is provided."""
        sut: YamkixConfig = parse_cli([])
        yamkix_default_config = get_default_yamkix_config()

        assert sut.parsing_mode == yamkix_default_config.parsing_mode
        assert sut.explicit_start == yamkix_default_config.explicit_start
        assert sut.explicit_end == yamkix_default_config.explicit_end
        assert sut.default_flow_style == yamkix_default_config.default_flow_style
        assert sut.dash_inwards == yamkix_default_config.dash_inwards
        assert sut.quotes_preserved == yamkix_default_config.quotes_preserved
        assert sut.spaces_before_comment == yamkix_default_config.spaces_before_comment
        assert sut.line_width == yamkix_default_config.line_width
        assert sut.version == yamkix_default_config.version

    def test_get_override_or_default_when_key_doesnt_exist(self) -> None:
        """Test get_override_or_default when key doesn't exist."""
        sut = {}
        key = "any"
        default_value = "yolo"
        result = get_override_or_default(sut, key, default_value)
        assert result == default_value

    def test_get_override_or_default_when_key_exists(self) -> None:
        """Test get_override_or_default when key exists."""
        sut = {}
        key = "i_m_the_one"
        value_for_key = "yamkix_rulez"
        default_value = "yolo"
        sut[key] = value_for_key
        result = get_override_or_default(sut, key, default_value)
        assert result == value_for_key

    def test_get_override_or_default_when_override_is_none(self) -> None:
        """Test get_override_or_default when override is none."""
        sut = None
        key = "any"
        default_value = "yolo"
        result = get_override_or_default(sut, key, default_value)
        assert result == default_value
