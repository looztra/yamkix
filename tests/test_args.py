"""Tests the args parsing."""
from yamkix.args import parse_cli
from yamkix.config import get_default_yamkix_config, YamkixConfig


def test_defaults():
    """Test when no input is provided."""
    sut: YamkixConfig = parse_cli(dict())
    yamkix_default_config = get_default_yamkix_config()

    assert sut.parsing_mode == yamkix_default_config.parsing_mode
    assert sut.explicit_start == yamkix_default_config.explicit_start
    assert sut.explicit_end == yamkix_default_config.explicit_end
    assert sut.default_flow_style == yamkix_default_config.default_flow_style
    assert sut.dash_inwards == yamkix_default_config.dash_inwards
    assert sut.quotes_preserved == yamkix_default_config.quotes_preserved
    assert (
        sut.spaces_before_comment
        == yamkix_default_config.spaces_before_comment
    )
    assert sut.line_width == yamkix_default_config.line_width
    assert sut.version == yamkix_default_config.version
