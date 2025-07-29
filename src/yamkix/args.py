"""Deal with args."""

import argparse


def get_override_or_default(short_opt_override: dict[str, str] | None, key: str, default_value: str) -> str:
    """Return the override to apply or the default value."""
    if short_opt_override and key in short_opt_override:
        return short_opt_override[key]
    return default_value


def add_yamkix_options_to_parser(
    parser: argparse.ArgumentParser, short_opt_override: dict[str, str] | None = None
) -> None:
    """Add yamkix reusable options to a parser object."""
    parser.add_argument(
        get_override_or_default(short_opt_override, "--typ", "-t"),
        "--typ",
        required=False,
        default="rt",
        help="the yaml parser mode. Can be `safe` or `rt`",
    )
    parser.add_argument(
        get_override_or_default(short_opt_override, "--no-explicit-start", "-n"),
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
        get_override_or_default(short_opt_override, "--no-quotes-preserved", "-q"),
        "--no-quotes-preserved",
        action="store_true",
        help="by default, quotes are preserved \
                                you can disable this with this option",
    )
    parser.add_argument(
        get_override_or_default(short_opt_override, "--default-flow-style", "-f"),
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
        get_override_or_default(short_opt_override, "--spaces-before-comment", "-c"),
        "--spaces-before-comment",
        default=None,
        help="specify the number of spaces between comments and content. \
                        If not specified, comments are left as is.",
    )
