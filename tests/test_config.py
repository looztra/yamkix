"""Tests the YamkixConfig stuff."""
from yamkix.config import YamkixConfig
from yamkix.config import get_default_yamkix_config


def test_default_values():
    """Test YamkixConfig default values."""
    sut: YamkixConfig = get_default_yamkix_config()
    assert sut.parsing_mode == "rt"
    assert sut.explicit_start
    assert not sut.explicit_end
    assert not sut.default_flow_style
    assert sut.dash_inwards
    assert sut.quotes_preserved
    assert sut.spaces_before_comment is None
    assert sut.line_width == 2048
    assert not sut.version
