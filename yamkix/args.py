"""Deal with args."""

import argparse

from yamkix import __version__
from yamkix.config import (
    get_config_from_args,
    YamkixConfig,
)


def get_override_or_default(short_opt_override, key, default_value):
    """Returns the override to apply or the default value."""
    if short_opt_override and key in short_opt_override:
        return short_opt_override[key]
    return default_value


def add_yamkix_options_to_parser(parser, short_opt_override=None):
    """Add yamkix reusable options to a parser object."""
    parser.add_argument(
        get_override_or_default(short_opt_override, "--typ", "-t"),
        "--typ",
        required=False,
        default="rt",
        help="the yaml parser mode. Can be `safe` or `rt`",
    )
    parser.add_argument(
        get_override_or_default(
            short_opt_override, "--no-explicit-start", "-n"
        ),
        "--no-explicit-start",
        action="store_true",
        help="by default, explicit start of the yaml doc \
                                is `On`, you can disable it with this option",
    )
    parser.add_argument(
        get_override_or_default(short_opt_override, "--explicit-end", "-e"),
        "--explicit-end",
        action="store_true",
        help="by default, explicit end of the yaml doc \
                                is `Off`, you can enable it with this option",
    )
    parser.add_argument(
        get_override_or_default(
            short_opt_override, "--no-quotes-preserved", "-q"
        ),
        "--no-quotes-preserved",
        action="store_true",
        help="by default, quotes are preserved \
                                you can disable this with this option",
    )
    parser.add_argument(
        get_override_or_default(
            short_opt_override, "--default-flow-style", "-f"
        ),
        "--default-flow-style",
        action="store_true",
        help="enable the default flow style \
                                `Off` by default. In default flow style \
                                (with typ=`rt`), maps and lists are written \
                                like json",
    )
    parser.add_argument(
        get_override_or_default(short_opt_override, "--no-dash-inwards", "-d"),
        "--no-dash-inwards",
        action="store_true",
        help="by default, dash are pushed inwards \
                                use `--no-dash-inwards` to have the dash \
                                start at the sequence level",
    )
    parser.add_argument(
        get_override_or_default(
            short_opt_override, "--spaces-before-comment", "-c"
        ),
        "--spaces-before-comment",
        default=None,
        help="specify the number of spaces between comments and content. \
                        If not specified, comments are left as is.",
    )


def build_parser():
    """Build the cli args parser."""
    parser = argparse.ArgumentParser(
        description=f"""Yamkix v{__version__}.
            Format yaml input file.
            By default, explicit_start is `On`, explicit_end is `Off`
            and array elements are pushed inwards the start of the
            matching sequence. Comments are preserved thanks to default
            parsing mode `rt`.
        """
    )
    parser.add_argument(
        "-i",
        "--input",
        required=False,
        help="""the file to parse or 'STDIN'.
            Defaults to 'STDIN' if not specified
        """,
    )
    parser.add_argument(
        "-o",
        "--output",
        required=False,
        help="the name of the file to generate (can be 'STDOUT') \
                            (same as input file if not specified, \
                                hence 'STDOUT' if 'STDIN' as input)",
    )
    parser.add_argument(
        "-s",
        "--stdout",
        action="store_true",
        help="output is STDOUT whatever the value for \
                        input (-i) and output (-o)",
    )
    add_yamkix_options_to_parser(parser)
    parser.add_argument(
        "-v",
        "--version",
        action="store_true",
        help="show yamkix version",
    )
    return parser


def parse_cli(args) -> YamkixConfig:
    """Parse the cli args."""
    parser = build_parser()
    args = parser.parse_args(args)
    yamkix_config = get_config_from_args(args, inc_io_config=True)
    return yamkix_config
