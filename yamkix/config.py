"""Yamkix configuration helpers."""
import collections
import sys

from typing import Dict

from yamkix import __version__

YamkixConfig = collections.namedtuple(
    "YamkixConfig",
    "explicit_start \
        explicit_end \
        default_flow_style \
        dash_inwards \
        quotes_preserved \
        parsing_mode \
        spaces_before_comment \
        line_width \
        version \
        io_config",
)

YamkixInputOutputConfig = collections.namedtuple(
    "YamkixInputOutputConfig",
    "input input_display_name output output_display_name",
)


def get_default_yamkix_config() -> YamkixConfig:
    """Return Yamkix default config."""
    return YamkixConfig(
        parsing_mode="rt",
        explicit_start=True,
        explicit_end=False,
        default_flow_style=False,
        dash_inwards=True,
        quotes_preserved=True,
        spaces_before_comment=None,
        line_width=2048,
        version=False,
        io_config=get_default_yamkix_input_output_config(),
    )


def get_default_yamkix_input_output_config() -> YamkixInputOutputConfig:
    """Return a default input / output config."""
    return YamkixInputOutputConfig(
        input=None,
        output=None,
        input_display_name="STDIN",
        output_display_name="STDOUT",
    )


def print_yamkix_config(yamkix_config: YamkixConfig):
    """Print a human readable Yamkix config on stderr."""
    yamkix_input_output_config = yamkix_config.io_config
    print(
        "[yamkix("
        + __version__
        + ")] Processing: input="
        + yamkix_input_output_config.input_display_name
        + ", output="
        + yamkix_input_output_config.output_display_name
        + ", typ="
        + yamkix_config.parsing_mode
        + ", explicit_start="
        + str(yamkix_config.explicit_start)
        + ", explicit_end="
        + str(yamkix_config.explicit_end)
        + ", default_flow_style="
        + str(yamkix_config.default_flow_style)
        + ", quotes_preserved="
        + str(yamkix_config.quotes_preserved)
        + ", dash_inwards="
        + str(yamkix_config.dash_inwards)
        + ", spaces_before_comment="
        + str(yamkix_config.spaces_before_comment)
        + ", show_version="
        + str(yamkix_config.version),
        file=sys.stderr,
    )


def get_input_output_config_from_args(
    argparse_args: Dict[str, any]
) -> YamkixInputOutputConfig:
    """Get input, output and associated labels as YamkixInputOutputConfig."""
    input_display_name = "STDIN"
    if argparse_args.input is None:
        f_input = None
    else:
        f_input = argparse_args.input
        input_display_name = f_input
    if argparse_args.stdout:
        f_output = None
    else:
        if (
            argparse_args.output is not None
            and argparse_args.output != "STDOUT"
        ):
            f_output = argparse_args.output
        else:
            if argparse_args.output == "STDOUT":
                f_output = None
            else:
                if f_input is None:
                    f_output = None
                else:
                    f_output = argparse_args.input
    if f_output is None:
        output_display_name = "STDOUT"
    else:
        output_display_name = f_output
    return YamkixInputOutputConfig(
        input=f_input,
        input_display_name=input_display_name,
        output=f_output,
        output_display_name=output_display_name,
    )


def get_config_from_args(args: Dict[str, any]) -> YamkixConfig:
    """Build a YamkixConfig object from parsed args."""
    yamkix_input_output_config = get_input_output_config_from_args(args)
    if args.typ not in ["safe", "rt"]:
        raise ValueError(
            "'%s' is not a valid value for option --typ. "
            "Allowed values are 'safe' and 'rt'" % args.type
        )
    default_yamkix_config = get_default_yamkix_config()
    return YamkixConfig(
        explicit_start=not args.no_explicit_start,
        explicit_end=args.explicit_end,
        default_flow_style=args.default_flow_style,
        dash_inwards=not args.no_dash_inwards,
        quotes_preserved=not args.no_quotes_preserved,
        parsing_mode=args.typ,
        version=args.version,
        spaces_before_comment=get_spaces_before_comment_from_args(args),
        io_config=yamkix_input_output_config,
        line_width=default_yamkix_config.line_width,
    )


def get_spaces_before_comment_from_args(args: Dict[str, any]):
    """Extract a valid value for spaces_before_comment from args."""
    if args.spaces_before_comment is None:
        spaces_before_comment = None
    else:
        try:
            spaces_before_comment = int(args.spaces_before_comment)
        except ValueError:
            spaces_before_comment = None
    return spaces_before_comment
