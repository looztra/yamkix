"""Test the yaml_writer init stuff."""

from typing import TYPE_CHECKING

from yamkix.config import DEFAULT_LINE_WIDTH, get_default_yamkix_config
from yamkix.yaml_writer import (
    OPINIONATED_MAPPING_VALUE,
    OPINIONATED_OFFSET_VALUE,
    OPINIONATED_SEQUENCE_VALUE,
    get_opinionated_yaml_writer,
)

if TYPE_CHECKING:
    from ruamel.yaml import YAML


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
