"""Yamkix configuration helpers."""

import sys
from argparse import Namespace
from dataclasses import dataclass

from typer import echo as typer_echo

from yamkix.__version__ import __version__
from yamkix.errors import InvalidTypValueError

DEFAULT_LINE_WIDTH = 2048
STDIN_DISPLAY_NAME = "STDIN"
STDOUT_DISPLAY_NAME = "STDOUT"


@dataclass
class YamkixInputOutputConfig:
    """`Yamkix` input/output configuration.

    Part of the config that manages `input` and `output`.

    Attributes:
        input: The input file to parse or `STDIN` or `None`. Defaults to `STDIN` if not specified
        output: The name of the file to generate (can be `STDOUT`). Will be the same as input file
            if not specified (`None`), or `STDOUT` if `STDIN` was specified as input
    """

    input: str | None
    output: str | None

    def __post_init__(self) -> None:
        """Set display names for `input` and `output`."""
        self.input_display_name = STDIN_DISPLAY_NAME if self.input is None else self.input
        self.output_display_name = STDOUT_DISPLAY_NAME if self.output is None else self.output


@dataclass
class YamkixConfig:  # pylint: disable=too-many-instance-attributes
    """Defines the available `Yamkix` configuration.

    Attributes:
        explicit_start: Whether to include explicit start markers (`---`).
        explicit_end: Whether to include explicit end markers (`...`).
        default_flow_style: Whether to use default flow style. Setting `default_flow_style = False` ensures
            that all collections are dumped in block style by default, which is the typical YAML format where sequences
            and mappings are presented with indentation and newlines. Conversely, setting `default_flow_style = True`
            forces all collections to be dumped in flow style, meaning they are written on
            a single line using square brackets `[]` for sequences and curly braces `{}` for mappings.
        dash_inwards: Whether to use dash inwards, i.e. whether to indent the dash in front of a sequence.
        quotes_preserved: Whether to preserve quotes, i.e. preserve the original quotes
            used in the input in the output.
        spaces_before_comment: Number of spaces before comments.
        line_width: Maximum line width.
        version: Whether to include version information (deprecated)
        io_config: Input/Output configuration.

    """

    explicit_start: bool
    explicit_end: bool
    default_flow_style: bool
    dash_inwards: bool
    quotes_preserved: bool
    parsing_mode: str
    spaces_before_comment: int | None
    line_width: int
    version: bool | None
    io_config: YamkixInputOutputConfig


def get_default_yamkix_config() -> YamkixConfig:
    """Return `Yamkix` default configuration.

    Returns:
        yamkix_config: The default configuration provided by `Yamkix`:
            <ul>
                <li><i>parsing_mode = rt</i></li>
                <li><i>explicit_start = True</i></li>
                <li><i>explicit_end = False</i></li>
                <li><i>default_flow_style = False</i></li>
                <li><i>dash_inwards = True</i></li>
                <li><i>quotes_preserved = True</i></li>
                <li><i>spaces_before_comment = None</i></li>
                <li><i>line_width = 2048</i></li>
                <li><i>io_config</i>:
                    <ul>
                        <li><i>input = None</i></li>
                        <li><i>output = None</i></li>
                    </ul>
                </li>
            </ul>
    """
    return YamkixConfig(
        parsing_mode="rt",
        explicit_start=True,
        explicit_end=False,
        default_flow_style=False,
        dash_inwards=True,
        quotes_preserved=True,
        spaces_before_comment=None,
        line_width=DEFAULT_LINE_WIDTH,
        version=False,
        io_config=get_default_yamkix_input_output_config(),
    )


def get_default_yamkix_input_output_config() -> YamkixInputOutputConfig:
    """Return a default `input` / `output` configuration.

    Returns:
        yamkix_input_output_config: A default `YamkixInputOutputConfig` object.
    """
    return YamkixInputOutputConfig(
        input=None,
        output=None,
    )


def get_yamkix_config_from_default(  # noqa: PLR0913
    parsing_mode: str | None = None,
    explicit_start: bool | None = None,
    explicit_end: bool | None = None,
    default_flow_style: bool | None = None,
    dash_inwards: bool | None = None,
    quotes_preserved: bool | None = None,
    spaces_before_comment: int | None = None,
    line_width: int | None = None,
    io_config: YamkixInputOutputConfig | None = None,
) -> YamkixConfig:
    """Return a `Yamkix` configuration, based on the default one.

    Parameters:
        parsing_mode: `rt`/`None` -> RoundTripLoader/RoundTripDumper, (default)
            `safe` -> SafeLoader/SafeDumper,
            `unsafe` -> normal/unsafe Loader/Dumper (pending deprecation)
            `full` -> full Dumper only, including python built-ins that are
                potentially unsafe to load
            `base` -> baseloader
                explicit_start: Whether to include explicit start markers (`---`).
        explicit_end: Whether to include explicit end markers (`...`).
        default_flow_style: Whether to use default flow style. Setting `default_flow_style = False` ensures
            that all collections are dumped in block style by default, which is the typical YAML format where sequences
            and mappings are presented with indentation and newlines. Conversely, setting `default_flow_style = True`
            forces all collections to be dumped in flow style, meaning they are written on
            a single line using square brackets [] for sequences and curly braces {} for mappings.
        dash_inwards: Whether to use dash inwards, i.e. whether to indent the dash in front of a sequence.
        quotes_preserved: Whether to preserve quotes, i.e. preserve the original quotes
            used in the input in the output.
        spaces_before_comment: Number of spaces before comments.
        line_width: Maximum line width.
        io_config: Input/Output configuration.

    Returns:
        yamkix_config: A `YamkixConfig` object with the specified overrides.

    Tip:
        Use this function when you want to create a custom configuration that just overrides
        some of the default values.

    Note:
        If you want to create a configuration from scratch, build a `YamkixConfig` object directly.
    """
    default_config = get_default_yamkix_config()
    return YamkixConfig(
        parsing_mode=parsing_mode if parsing_mode is not None else default_config.parsing_mode,
        explicit_start=explicit_start if explicit_start is not None else default_config.explicit_start,
        explicit_end=explicit_end if explicit_end is not None else default_config.explicit_end,
        default_flow_style=default_flow_style if default_flow_style is not None else default_config.default_flow_style,
        dash_inwards=dash_inwards if dash_inwards is not None else default_config.dash_inwards,
        quotes_preserved=quotes_preserved if quotes_preserved is not None else default_config.quotes_preserved,
        spaces_before_comment=spaces_before_comment
        if spaces_before_comment is not None
        else default_config.spaces_before_comment,
        line_width=line_width if line_width is not None else default_config.line_width,
        version=None,
        io_config=io_config if io_config is not None else get_default_yamkix_input_output_config(),
    )


def print_yamkix_config(yamkix_config: YamkixConfig) -> None:
    """Print a human readable Yamkix config on stderr."""
    yamkix_input_output_config = yamkix_config.io_config
    typer_echo(
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
    args: Namespace,
) -> YamkixInputOutputConfig:
    """Get input, output and associated labels as YamkixInputOutputConfig."""
    f_input = None if args.input is None else args.input
    if args.stdout:
        f_output = None
    elif args.output is not None and args.output != STDOUT_DISPLAY_NAME:
        f_output = args.output
    elif args.output == STDOUT_DISPLAY_NAME or f_input is None:
        f_output = None
    else:
        f_output = args.input
    return YamkixInputOutputConfig(
        input=f_input,
        output=f_output,
    )


def get_config_from_args(args: Namespace, inc_io_config: bool = True) -> YamkixConfig:
    """Build a YamkixConfig object from parsed args."""
    if args.typ not in ["safe", "rt"]:
        raise InvalidTypValueError(args.typ)
    if inc_io_config:
        yamkix_input_output_config = get_input_output_config_from_args(args)
    else:
        yamkix_input_output_config = get_default_yamkix_input_output_config()
    default_yamkix_config = get_default_yamkix_config()
    return YamkixConfig(
        explicit_start=not args.no_explicit_start,
        explicit_end=args.explicit_end if args.explicit_end is not None else False,
        default_flow_style=args.default_flow_style if args.default_flow_style is not None else False,
        dash_inwards=not args.no_dash_inwards,
        quotes_preserved=not args.no_quotes_preserved,
        parsing_mode=args.typ,
        version=args.version if args.version is not None else False,
        spaces_before_comment=get_spaces_before_comment_from_args(args),
        io_config=yamkix_input_output_config,
        line_width=default_yamkix_config.line_width,
    )


def get_spaces_before_comment_from_args(args: Namespace) -> None | int:
    """Extract a valid value for spaces_before_comment from args."""
    if args.spaces_before_comment is None:
        spaces_before_comment = None
    else:
        try:
            spaces_before_comment = int(args.spaces_before_comment)
        except ValueError:
            spaces_before_comment = None
    return spaces_before_comment


def create_yamkix_config_from_typer_args(  # noqa: PLR0913
    input_file: str | None,
    output_file: str | None,
    stdout: bool,
    typ: str,
    no_explicit_start: bool,
    explicit_end: bool,
    no_quotes_preserved: bool,
    default_flow_style: bool,
    no_dash_inwards: bool,
    spaces_before_comment: int | None,
    version: bool,
) -> YamkixConfig:
    """Create YamkixConfig from Typer arguments."""
    # Handle I/O configuration - match the original logic exactly
    f_input = None if input_file is None else input_file
    if stdout:
        f_output = None
    elif output_file is not None and output_file != "STDOUT":
        f_output = output_file
    elif output_file == "STDOUT" or f_input is None:
        f_output = None
    else:
        f_output = f_input

    io_config = YamkixInputOutputConfig(
        input=f_input,
        output=f_output,
    )

    return YamkixConfig(
        explicit_start=not no_explicit_start,
        explicit_end=explicit_end,
        default_flow_style=default_flow_style,
        dash_inwards=not no_dash_inwards,
        quotes_preserved=not no_quotes_preserved,
        parsing_mode=typ,
        spaces_before_comment=spaces_before_comment,
        line_width=DEFAULT_LINE_WIDTH,
        version=version,
        io_config=io_config,
    )
