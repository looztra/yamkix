"""Test the yaml_writer init stuff."""
from ruamel.yaml import YAML
from yamkix.yaml_writer import get_opinionated_yaml_writer
from yamkix.config import get_default_yamkix_config


def test_get_opinionated_yaml_writer_with_defaults():
    """Test get_opinionated_yaml_writer default values."""
    sut: YAML = get_opinionated_yaml_writer(get_default_yamkix_config())
    assert sut.typ == ["rt"]
    assert sut.explicit_start
    assert not sut.explicit_end
    assert not sut.default_flow_style
    assert sut.preserve_quotes
    assert sut.map_indent == 2
    assert sut.sequence_dash_offset == 2
    assert sut.sequence_indent == 4
    assert not sut.version
