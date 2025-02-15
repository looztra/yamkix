"""Tests the args parsing."""

import unittest

from yamkix.args import get_override_or_default, parse_cli
from yamkix.config import get_default_yamkix_config, YamkixConfig


class TestArgs(unittest.TestCase):
    """Provide unit tests for the args package."""

    def test_defaults(self):
        """Test when no input is provided."""
        sut: YamkixConfig = parse_cli(dict())
        yamkix_default_config = get_default_yamkix_config()

        self.assertEqual(sut.parsing_mode, yamkix_default_config.parsing_mode)
        self.assertEqual(sut.explicit_start, yamkix_default_config.explicit_start)
        self.assertEqual(sut.explicit_end, yamkix_default_config.explicit_end)
        self.assertEqual(sut.default_flow_style, yamkix_default_config.default_flow_style)
        self.assertEqual(sut.dash_inwards, yamkix_default_config.dash_inwards)
        self.assertEqual(sut.quotes_preserved, yamkix_default_config.quotes_preserved)
        self.assertEqual(
            sut.spaces_before_comment,
            yamkix_default_config.spaces_before_comment,
        )
        self.assertEqual(sut.line_width, yamkix_default_config.line_width)
        self.assertEqual(sut.version, yamkix_default_config.version)

    def test_get_override_or_default_when_key_doesnt_exist(self):
        """Test get_override_or_default when key doesn't exist."""
        sut = dict()
        key = "any"
        default_value = "yolo"
        result = get_override_or_default(sut, key, default_value)
        self.assertEqual(result, default_value)

    def test_get_override_or_default_when_key_exists(self):
        """Test get_override_or_default when key exists."""
        sut = dict()
        key = "i_m_the_one"
        value_for_key = "yamkix_rulez"
        default_value = "yolo"
        sut[key] = value_for_key
        result = get_override_or_default(sut, key, default_value)
        self.assertEqual(result, value_for_key)

    def test_get_override_or_default_when_override_is_none(self):
        """Test get_override_or_default when override is none."""
        sut = None
        key = "any"
        default_value = "yolo"
        result = get_override_or_default(sut, key, default_value)
        self.assertEqual(result, default_value)
