"""Tests the args parsing."""
import unittest

from yamkix.args import parse_cli
from yamkix.config import get_default_yamkix_config, YamkixConfig


class TestArgs(unittest.TestCase):
    """Provide unit tests for the args package."""

    def test_defaults(self):
        """Test when no input is provided."""
        sut: YamkixConfig = parse_cli(dict())
        yamkix_default_config = get_default_yamkix_config()

        self.assertEqual(sut.parsing_mode, yamkix_default_config.parsing_mode)
        self.assertEqual(
            sut.explicit_start, yamkix_default_config.explicit_start
        )
        self.assertEqual(sut.explicit_end, yamkix_default_config.explicit_end)
        self.assertEqual(
            sut.default_flow_style, yamkix_default_config.default_flow_style
        )
        self.assertEqual(sut.dash_inwards, yamkix_default_config.dash_inwards)
        self.assertEqual(
            sut.quotes_preserved, yamkix_default_config.quotes_preserved
        )
        self.assertEqual(
            sut.spaces_before_comment,
            yamkix_default_config.spaces_before_comment,
        )
        self.assertEqual(sut.line_width, yamkix_default_config.line_width)
        self.assertEqual(sut.version, yamkix_default_config.version)
