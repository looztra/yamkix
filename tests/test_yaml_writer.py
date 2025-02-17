"""Test the yaml_writer init stuff."""

import unittest
from typing import TYPE_CHECKING

from yamkix.config import get_default_yamkix_config
from yamkix.yaml_writer import get_opinionated_yaml_writer

if TYPE_CHECKING:
    from ruamel.yaml import YAML


class TestYamlWriter(unittest.TestCase):
    """Provide unit tests for the yaml_writer package."""

    def test_get_opinionated_yaml_writer_with_defaults(self) -> None:
        """Test get_opinionated_yaml_writer default values."""
        sut: YAML = get_opinionated_yaml_writer(get_default_yamkix_config())
        self.assertEqual(sut.typ, ["rt"])
        self.assertTrue(sut.explicit_start)
        self.assertFalse(sut.explicit_end)
        self.assertFalse(sut.default_flow_style)
        self.assertTrue(sut.preserve_quotes)
        self.assertEqual(sut.map_indent, 2)
        self.assertEqual(sut.sequence_dash_offset, 2)
        self.assertEqual(sut.sequence_indent, 4)
        self.assertEqual(sut.width, 2048)
        self.assertFalse(sut.version)
