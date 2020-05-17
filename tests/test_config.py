"""Tests the YamkixConfig stuff."""
import unittest

from argparse import Namespace

from yamkix.config import YamkixConfig, YamkixInputOutputConfig
from yamkix.config import (
    get_config_from_args,
    get_default_yamkix_config,
    get_input_output_config_from_args,
    get_spaces_before_comment_from_args,
    get_yamkix_config_from_default,
)


class TestConfig(unittest.TestCase):
    """Provide unit tests for the config package."""

    def test_default_values(self):
        """Test YamkixConfig default values."""
        sut: YamkixConfig = get_default_yamkix_config()
        self.assertEqual(sut.parsing_mode, "rt")
        self.assertTrue(sut.explicit_start)
        self.assertFalse(sut.explicit_end)
        self.assertFalse(sut.default_flow_style)
        self.assertTrue(sut.dash_inwards)
        self.assertTrue(sut.quotes_preserved)
        self.assertIsNone(sut.spaces_before_comment)
        self.assertEqual(sut.line_width, 2048)
        self.assertFalse(sut.version)

    def test_get_io_config_when_defaults(self):
        """Test get_input_output_config_from_args.

        input=None, output=None, stdout=None
        """
        parsed = Namespace(input=None, output=None, stdout=None)
        sut: YamkixInputOutputConfig = get_input_output_config_from_args(
            parsed
        )
        self.assertIsNone(sut.input)
        self.assertEqual(sut.input_display_name, "STDIN")
        self.assertIsNone(sut.output)
        self.assertEqual(sut.output_display_name, "STDOUT")

    def test_get_io_config_when_file_input_provided(self):
        """Test get_input_output_config_from_args.

        input=f_input, output=None, stdout=None
        """
        f_input = "path/to/input"
        parsed = Namespace(input=f_input, output=None, stdout=None)
        sut: YamkixInputOutputConfig = get_input_output_config_from_args(
            parsed
        )
        self.assertEqual(sut.input, f_input)
        self.assertEqual(sut.input_display_name, f_input)
        self.assertEqual(sut.output, f_input)
        self.assertEqual(sut.output_display_name, f_input)

    def test_get_io_config_when_file_input_and_output_provided(self):
        """Test get_input_output_config_from_args.

        input=f_input, output=f_output, stdout=None
        """
        f_input = "path/to/input"
        f_output = "path/to/output"
        parsed = Namespace(input=f_input, output=f_output, stdout=None)
        sut: YamkixInputOutputConfig = get_input_output_config_from_args(
            parsed
        )
        self.assertEqual(sut.input, f_input)
        self.assertEqual(sut.input_display_name, f_input)
        self.assertEqual(sut.output, f_output)
        self.assertEqual(sut.output_display_name, f_output)

    def test_get_io_config_when_file_input_provided_and_stdout(self):
        """Test get_input_output_config_from_args.

        input=f_input, output=None, stdout=True
        """
        f_input = "path/to/input"
        parsed = Namespace(input=f_input, output=None, stdout=True)
        sut: YamkixInputOutputConfig = get_input_output_config_from_args(
            parsed
        )

        self.assertEqual(sut.input, f_input)
        self.assertEqual(sut.input_display_name, f_input)
        self.assertIsNone(sut.output)
        self.assertEqual(sut.output_display_name, "STDOUT")

    def test_get_io_config_when_file_input_and_output_provided_and_stdout(
        self,
    ):
        """Test get_input_output_config_from_args.

        input=f_input, output=f_output, stdout=True
        """
        f_input = "path/to/input"
        f_output = "path/to/output"
        parsed = Namespace(input=f_input, output=f_output, stdout=True)
        sut: YamkixInputOutputConfig = get_input_output_config_from_args(
            parsed
        )
        self.assertEqual(sut.input, f_input)
        self.assertEqual(sut.input_display_name, f_input)
        self.assertIsNone(sut.output)
        self.assertEqual(sut.output_display_name, "STDOUT")

    def test_get_io_config_when_output_stdout(self):
        """Test get_input_output_config_from_args.

        input=f_input, output=f_output, stdout=None
        """
        f_input = "path/to/input"
        f_output = "STDOUT"
        parsed = Namespace(input=f_input, output=f_output, stdout=None)
        sut: YamkixInputOutputConfig = get_input_output_config_from_args(
            parsed
        )
        self.assertEqual(sut.input, f_input)
        self.assertEqual(sut.input_display_name, f_input)
        self.assertIsNone(sut.output)
        self.assertEqual(sut.output_display_name, "STDOUT")

    def test_get_io_config_when_file_output_provided(self):
        """Test get_input_output_config_from_args.

        input=None, output=f_output, stdout=None
        """
        f_output = "path/to/output"
        parsed = Namespace(input=None, output=f_output, stdout=None)
        sut: YamkixInputOutputConfig = get_input_output_config_from_args(
            parsed
        )

        self.assertIsNone(sut.input)
        self.assertEqual(sut.input_display_name, "STDIN")
        self.assertEqual(sut.output, f_output)
        self.assertEqual(sut.output_display_name, f_output)

    def test_get_config_from_args_with_invalid_typ(self):
        """Test get_config_from_args.

        typ=yolo
        """
        parsed = Namespace(typ="yolo")
        with self.assertRaises(ValueError):
            get_config_from_args(parsed)

    def test_get_config_from_args_with_no_args(self):
        """Test get_config_from_args.

        input=None
        output=None
        stdout=None
        typ="rt"
        no_explicit_start=None
        explicit_end=None
        no_quotes_preserved=None
        default_flow_style=None
        no_dash_inwards=None
        stdout=None
        spaces_before_comment=None
        version=None
        """
        parsed = Namespace(
            input=None,
            output=None,
            stdout=None,
            typ="rt",
            no_explicit_start=None,
            explicit_end=None,
            no_quotes_preserved=None,
            default_flow_style=None,
            no_dash_inwards=None,
            spaces_before_comment=None,
            version=None,
        )
        sut: YamkixConfig = get_config_from_args(parsed)
        sut_io = sut.io_config
        yamkix_default_config = get_default_yamkix_config()
        self.assertIsNone(sut_io.input)
        self.assertEqual(sut_io.input_display_name, "STDIN")
        self.assertIsNone(sut_io.output)
        self.assertEqual(sut_io.output_display_name, "STDOUT")

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

    def test_get_config_from_args_with_no_io(self):
        """Test get_config_from_args.

        input=None
        output=None
        stdout=None
        typ="rt"
        no_explicit_start=None
        explicit_end=None
        no_quotes_preserved=None
        default_flow_style=None
        no_dash_inwards=None
        stdout=None
        spaces_before_comment=None
        version=None
        inc_io_config=False
        """
        parsed = Namespace(
            input=None,
            output=None,
            stdout=None,
            typ="rt",
            no_explicit_start=None,
            explicit_end=None,
            no_quotes_preserved=None,
            default_flow_style=None,
            no_dash_inwards=None,
            spaces_before_comment=None,
            version=None,
        )
        sut: YamkixConfig = get_config_from_args(parsed, inc_io_config=False)
        self.assertIsNone(sut.io_config)

    def test_get_spaces_before_comment_from_args_when_none(self):
        """Test get_spaces_before_comment_from_args.

        spaces_before_comment=None
        """
        parsed = Namespace(spaces_before_comment=None)
        sut = get_spaces_before_comment_from_args(parsed)
        self.assertIsNone(sut)

    def test_get_spaces_before_comment_from_args_when_int(self):
        """Test get_spaces_before_comment_from_args.

        spaces_before_comment=722
        """
        parsed = Namespace(spaces_before_comment=722)
        sut = get_spaces_before_comment_from_args(parsed)
        self.assertEqual(sut, 722)

    def test_get_spaces_before_comment_from_args_when_invalid(self):
        """Test get_spaces_before_comment_from_args.

        spaces_before_comment=yolo
        """
        parsed = Namespace(spaces_before_comment="yolo")
        sut = get_spaces_before_comment_from_args(parsed)
        self.assertIsNone(sut)

    def test_get_yamkix_config_from_default_parsing_mode(self):
        """Test get_yamkix_config_from_default.

        change parsing_mode
        """
        reference = get_yamkix_config_from_default()
        new_val = "zoro"
        sut = get_yamkix_config_from_default(parsing_mode=new_val)
        self.assertEqual(sut.parsing_mode, new_val)
        self.assertEqual(sut.explicit_start, reference.explicit_start)
        self.assertEqual(sut.explicit_end, reference.explicit_end)
        self.assertEqual(sut.default_flow_style, reference.default_flow_style)
        self.assertEqual(sut.dash_inwards, reference.dash_inwards)
        self.assertEqual(sut.quotes_preserved, reference.quotes_preserved)
        self.assertEqual(
            sut.spaces_before_comment, reference.spaces_before_comment
        )
        self.assertEqual(sut.line_width, reference.line_width)
        self.assertEqual(sut.io_config, reference.io_config)

    def test_get_yamkix_config_from_default_explicit_start(self):
        """Test get_yamkix_config_from_default.

        change explicit_start
        """
        reference = get_yamkix_config_from_default()
        new_val = not reference.explicit_start
        sut = get_yamkix_config_from_default(explicit_start=new_val)
        self.assertEqual(sut.parsing_mode, reference.parsing_mode)
        self.assertEqual(sut.explicit_start, new_val)
        self.assertEqual(sut.explicit_end, reference.explicit_end)
        self.assertEqual(sut.default_flow_style, reference.default_flow_style)
        self.assertEqual(sut.dash_inwards, reference.dash_inwards)
        self.assertEqual(sut.quotes_preserved, reference.quotes_preserved)
        self.assertEqual(
            sut.spaces_before_comment, reference.spaces_before_comment
        )
        self.assertEqual(sut.line_width, reference.line_width)
        self.assertEqual(sut.io_config, reference.io_config)

    def test_get_yamkix_config_from_default_explicit_end(self):
        """Test get_yamkix_config_from_default.

        change explicit_end
        """
        reference = get_yamkix_config_from_default()
        new_val = not reference.explicit_end
        sut = get_yamkix_config_from_default(explicit_end=new_val)
        self.assertEqual(sut.parsing_mode, reference.parsing_mode)
        self.assertEqual(sut.explicit_start, reference.explicit_start)
        self.assertEqual(sut.explicit_end, new_val)
        self.assertEqual(sut.default_flow_style, reference.default_flow_style)
        self.assertEqual(sut.dash_inwards, reference.dash_inwards)
        self.assertEqual(sut.quotes_preserved, reference.quotes_preserved)
        self.assertEqual(
            sut.spaces_before_comment, reference.spaces_before_comment
        )
        self.assertEqual(sut.line_width, reference.line_width)
        self.assertEqual(sut.io_config, reference.io_config)

    def test_get_yamkix_config_from_default_default_flow_style(self):
        """Test get_yamkix_config_from_default.

        change default_flow_style
        """
        reference = get_yamkix_config_from_default()
        new_val = not reference.default_flow_style
        sut = get_yamkix_config_from_default(default_flow_style=new_val)
        self.assertEqual(sut.parsing_mode, reference.parsing_mode)
        self.assertEqual(sut.explicit_start, reference.explicit_start)
        self.assertEqual(sut.explicit_end, reference.explicit_end)
        self.assertEqual(sut.default_flow_style, new_val)
        self.assertEqual(sut.dash_inwards, reference.dash_inwards)
        self.assertEqual(sut.quotes_preserved, reference.quotes_preserved)
        self.assertEqual(
            sut.spaces_before_comment, reference.spaces_before_comment
        )
        self.assertEqual(sut.line_width, reference.line_width)
        self.assertEqual(sut.io_config, reference.io_config)

    def test_get_yamkix_config_from_default_dash_inwards(self):
        """Test get_yamkix_config_from_default.

        change dash_inwards
        """
        reference = get_yamkix_config_from_default()
        new_val = not reference.dash_inwards
        sut = get_yamkix_config_from_default(dash_inwards=new_val)
        self.assertEqual(sut.parsing_mode, reference.parsing_mode)
        self.assertEqual(sut.explicit_start, reference.explicit_start)
        self.assertEqual(sut.explicit_end, reference.explicit_end)
        self.assertEqual(sut.default_flow_style, reference.default_flow_style)
        self.assertEqual(sut.dash_inwards, new_val)
        self.assertEqual(sut.quotes_preserved, reference.quotes_preserved)
        self.assertEqual(
            sut.spaces_before_comment, reference.spaces_before_comment
        )
        self.assertEqual(sut.line_width, reference.line_width)
        self.assertEqual(sut.io_config, reference.io_config)

    def test_get_yamkix_config_from_default_quotes_preserved(self):
        """Test get_yamkix_config_from_default.

        change quotes_preserved
        """
        reference = get_yamkix_config_from_default()
        new_val = not reference.quotes_preserved
        sut = get_yamkix_config_from_default(quotes_preserved=new_val)
        self.assertEqual(sut.parsing_mode, reference.parsing_mode)
        self.assertEqual(sut.explicit_start, reference.explicit_start)
        self.assertEqual(sut.explicit_end, reference.explicit_end)
        self.assertEqual(sut.default_flow_style, reference.default_flow_style)
        self.assertEqual(sut.dash_inwards, reference.dash_inwards)
        self.assertEqual(sut.quotes_preserved, new_val)
        self.assertEqual(
            sut.spaces_before_comment, reference.spaces_before_comment
        )
        self.assertEqual(sut.line_width, reference.line_width)
        self.assertEqual(sut.io_config, reference.io_config)

    def test_get_yamkix_config_from_default_spaces_before_comment(self):
        """Test get_yamkix_config_from_default.

        change spaces_before_comment
        """
        reference = get_yamkix_config_from_default()
        new_val = 722
        sut = get_yamkix_config_from_default(spaces_before_comment=new_val)
        self.assertEqual(sut.parsing_mode, reference.parsing_mode)
        self.assertEqual(sut.explicit_start, reference.explicit_start)
        self.assertEqual(sut.explicit_end, reference.explicit_end)
        self.assertEqual(sut.default_flow_style, reference.default_flow_style)
        self.assertEqual(sut.dash_inwards, reference.dash_inwards)
        self.assertEqual(sut.quotes_preserved, reference.quotes_preserved)
        self.assertEqual(sut.spaces_before_comment, new_val)
        self.assertEqual(sut.line_width, reference.line_width)
        self.assertEqual(sut.io_config, reference.io_config)

    def test_get_yamkix_config_from_default_line_width(self):
        """Test get_yamkix_config_from_default.

        change line_width
        """
        reference = get_yamkix_config_from_default()
        new_val = 722
        sut = get_yamkix_config_from_default(line_width=new_val)
        self.assertEqual(sut.parsing_mode, reference.parsing_mode)
        self.assertEqual(sut.explicit_start, reference.explicit_start)
        self.assertEqual(sut.explicit_end, reference.explicit_end)
        self.assertEqual(sut.default_flow_style, reference.default_flow_style)
        self.assertEqual(sut.dash_inwards, reference.dash_inwards)
        self.assertEqual(sut.quotes_preserved, reference.quotes_preserved)
        self.assertEqual(
            sut.spaces_before_comment, reference.spaces_before_comment
        )
        self.assertEqual(sut.line_width, new_val)
        self.assertEqual(sut.io_config, reference.io_config)

    def test_get_yamkix_config_from_default_io_config(self):
        """Test get_yamkix_config_from_default.

        change io_config
        """
        reference = get_yamkix_config_from_default()
        new_val = 722
        sut = get_yamkix_config_from_default(io_config=new_val)
        self.assertEqual(sut.parsing_mode, reference.parsing_mode)
        self.assertEqual(sut.explicit_start, reference.explicit_start)
        self.assertEqual(sut.explicit_end, reference.explicit_end)
        self.assertEqual(sut.default_flow_style, reference.default_flow_style)
        self.assertEqual(sut.dash_inwards, reference.dash_inwards)
        self.assertEqual(sut.quotes_preserved, reference.quotes_preserved)
        self.assertEqual(
            sut.spaces_before_comment, reference.spaces_before_comment
        )
        self.assertEqual(sut.line_width, reference.line_width)
        self.assertEqual(sut.io_config, new_val)
