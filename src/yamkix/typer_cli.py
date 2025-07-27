"""Typer-based CLI implementation for yamkix."""

from typing import Annotated

import typer

from yamkix import __version__
from yamkix.config import YamkixConfig, YamkixInputOutputConfig, print_yamkix_config
from yamkix.helpers import print_version
from yamkix.yamkix import round_trip_and_format


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
        line_width=2048,  # DEFAULT_LINE_WIDTH from config.py
        version=version,
        io_config=io_config,
    )


def validate_typ(value: str) -> str:
    """Validate the typ parameter."""
    if value not in ["safe", "rt"]:
        msg = f"Invalid value '{value}'. Must be 'safe' or 'rt'"
        raise typer.BadParameter(msg)
    return value


def main(  # noqa: PLR0913
    input_file: Annotated[
        str | None,
        typer.Option(
            "-i",
            "--input",
            help="the file to parse or 'STDIN'. Defaults to 'STDIN' if not specified",
        ),
    ] = None,
    output_file: Annotated[
        str | None,
        typer.Option(
            "-o",
            "--output",
            help=(
                "the name of the file to generate (can be 'STDOUT') "
                "(same as input file if not specified, hence 'STDOUT' if 'STDIN' as input)"
            ),
        ),
    ] = None,
    stdout: Annotated[
        bool,
        typer.Option(
            "-s",
            "--stdout",
            help="output is STDOUT whatever the value for input (-i) and output (-o)",
        ),
    ] = False,
    typ: Annotated[
        str,
        typer.Option(
            "-t",
            "--typ",
            help="the yaml parser mode. Can be 'safe' or 'rt'",
            callback=validate_typ,
        ),
    ] = "rt",
    no_explicit_start: Annotated[
        bool,
        typer.Option(
            "-n",
            "--no-explicit-start",
            help="by default, explicit start of the yaml doc is 'On', you can disable it with this option",
        ),
    ] = False,
    explicit_end: Annotated[
        bool,
        typer.Option(
            "-e",
            "--explicit-end",
            help="by default, explicit end of the yaml doc is 'Off', you can enable it with this option",
        ),
    ] = False,
    no_quotes_preserved: Annotated[
        bool,
        typer.Option(
            "-q",
            "--no-quotes-preserved",
            help="by default, quotes are preserved you can disable this with this option",
        ),
    ] = False,
    default_flow_style: Annotated[
        bool,
        typer.Option(
            "-f",
            "--default-flow-style",
            help=(
                "enable the default flow style 'Off' by default. "
                "In default flow style (with typ='rt'), maps and lists are written like json"
            ),
        ),
    ] = False,
    no_dash_inwards: Annotated[
        bool,
        typer.Option(
            "-d",
            "--no-dash-inwards",
            help=(
                "by default, dash are pushed inwards "
                "use '--no-dash-inwards' to have the dash start at the sequence level"
            ),
        ),
    ] = False,
    spaces_before_comment: Annotated[
        int | None,
        typer.Option(
            "-c",
            "--spaces-before-comment",
            help=(
                "specify the number of spaces between comments and content. If not specified, comments are left as is."
            ),
        ),
    ] = None,
    version: Annotated[
        bool,
        typer.Option(
            "-v",
            "--version",
            help="show yamkix version",
        ),
    ] = False,
    silent_mode: Annotated[
        bool,
        typer.Option(
            "-S",
            "--silent",
            help="silent mode, don't print config when processing file(s)",
        ),
    ] = False,
) -> None:
    """Format yaml input file.

    Yamkix formats YAML files with opinionated styling rules.
    By default, explicit_start is 'On', explicit_end is 'Off'
    and array elements are pushed inwards the start of the
    matching sequence. Comments are preserved thanks to default
    parsing mode 'rt'.
    """
    # Handle version display
    if version:
        print_version()
        return

    # Create configuration
    yamkix_config = create_yamkix_config_from_typer_args(
        input_file=input_file,
        output_file=output_file,
        stdout=stdout,
        typ=typ,
        no_explicit_start=no_explicit_start,
        explicit_end=explicit_end,
        no_quotes_preserved=no_quotes_preserved,
        default_flow_style=default_flow_style,
        no_dash_inwards=no_dash_inwards,
        spaces_before_comment=spaces_before_comment,
        version=version,
    )
    if not silent_mode:
        print_yamkix_config(yamkix_config)
    round_trip_and_format(yamkix_config)


# Create the Typer app
app = typer.Typer(
    name="yamkix",
    help=f"Yamkix v{__version__}. Format yaml input file.",
    add_completion=False,
    no_args_is_help=False,  # Allow running without arguments (uses defaults)
)

# Register the main function as the default command
app.command()(main)


if __name__ == "__main__":
    app()
