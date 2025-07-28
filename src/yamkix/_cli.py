"""Typer-based CLI implementation for yamkix."""

from typing import Annotated

import typer
from typer import echo as typer_echo

from yamkix.__version__ import __version__
from yamkix.config import create_yamkix_config_from_typer_args, print_yamkix_config
from yamkix.yamkix import round_trip_and_format

# Create the Typer app
app = typer.Typer(
    name="yamkix",
    help=f"Yamkix v{__version__}. Format yaml input file.",
    context_settings={"help_option_names": ["-h", "--help"]},
    add_completion=False,
    no_args_is_help=False,  # Allow running without arguments (uses defaults)
)


def validate_typ(value: str) -> str:
    """Validate the typ parameter."""
    if value not in ["safe", "rt"]:
        msg = f"Invalid value '{value}'. Must be 'safe' or 'rt'"
        raise typer.BadParameter(msg)
    return value


def echo_version() -> None:
    """Print version."""
    typer_echo("yamkix v" + __version__)


def version_callback(value: bool) -> None:
    """Provide a version callback."""
    if value:
        echo_version()
        raise typer.Exit(code=0)


@app.command()
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
        typer.Option("-v", "--version", help="show yamkix version", callback=version_callback),
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


if __name__ == "__main__":
    app()  # pragma: no cover
