"""Typer-based CLI implementation for yamkix."""

from enum import Enum
from pathlib import Path
from typing import Annotated

import typer

from yamkix.__version__ import __version__
from yamkix.config import DEFAULT_LINE_WIDTH, create_yamkix_config_from_typer_args, print_yamkix_config
from yamkix.errors import InvalidYamlContentError
from yamkix.helpers import get_stderr_console, get_stdout_console
from yamkix.yamkix import round_trip_and_format

# Create the Typer app
app = typer.Typer(
    name="yamkix",
    help=f"Yamkix v{__version__}. Format yaml input file.",
    context_settings={"help_option_names": ["-h", "--help"]},
    add_completion=False,
    no_args_is_help=False,  # Allow running without arguments (uses defaults)
)


def echo_version() -> None:
    """Print version."""
    get_stdout_console().print("yamkix v" + __version__, highlight=False)


def version_callback(value: bool) -> None:
    """Provide a version callback."""
    if value:
        echo_version()
        raise typer.Exit(code=0)


# We cannot use StrEnum as we want to support python 3.10 too
class SupportedYamlParserMode(str, Enum):
    """Supported YAML parser modes."""

    SAFE = "safe"
    RT = "rt"


@app.command()
def main(  # noqa: PLR0913
    input_file: Annotated[
        str | None,
        typer.Option(
            "-i",
            "--input",
            help="the single file to parse or 'STDIN'. Defaults to 'STDIN' if not specified."
            " Cannot be used if the list of files to process is specified using arguments. "
            "If you need to specify multiple files, pass them as arguments instead of using this option. "
            "This flag will not be honored if the input file(s) has/have been specify using arguments "
            "(and not -i/--input)",
        ),
    ] = None,
    output_file: Annotated[
        str | None,
        typer.Option(
            "-o",
            "--output",
            help=(
                "the name of the file to generate (can be 'STDOUT'). "
                "Will be the same as input file if not specified, and 'STDOUT' if 'STDIN' was specified as input. "
                "This flag will not be honored if the input file(s) has/have been specify using arguments "
                "(and not -i/--input)"
            ),
        ),
    ] = None,
    stdout: Annotated[
        bool,
        typer.Option(
            "-s",
            "--stdout",
            help="output is 'STDOUT' whatever the value for input (-i/--input) and output (-o/--output). "
            "This flag will not be honored if the input file(s) has/have been specify using arguments "
            "(and not -i/--input)",
        ),
    ] = False,
    typ: Annotated[
        SupportedYamlParserMode,
        typer.Option(
            "-t",
            "--typ",
            help="the yaml parser mode. Can be 'safe' or 'rt'. Using 'safe' will remove all comments.",
            case_sensitive=False,
        ),
    ] = SupportedYamlParserMode.RT,
    no_explicit_start: Annotated[
        bool,
        typer.Option(
            "-n",
            "--no-explicit-start",
            help="by default, explicit start of the yaml doc is 'On', you can disable it with this option.",
        ),
    ] = False,
    explicit_end: Annotated[
        bool,
        typer.Option(
            "-e",
            "--explicit-end",
            help="by default, explicit end of the yaml doc is 'Off', you can enable it with this option.",
        ),
    ] = False,
    no_quotes_preserved: Annotated[
        bool,
        typer.Option(
            "-q",
            "--no-quotes-preserved",
            help="by default, quotes are preserved you can disable this with this option.",
        ),
    ] = False,
    enforce_double_quotes: Annotated[
        bool,
        typer.Option(
            "-E",
            "--enforce-double-quotes",
            help="enforce double quotes when --no-quotes-preserved is activated "
            "(by default, you get single quotes which is the recommended behavior)",
        ),
    ] = False,
    default_flow_style: Annotated[
        bool,
        typer.Option(
            "-f",
            "--default-flow-style",
            help=(
                "enable the default flow style 'Off' by default. "
                "In default flow style (with --typ 'rt'), maps and lists are written like json."
            ),
        ),
    ] = False,
    no_dash_inwards: Annotated[
        bool,
        typer.Option(
            "-d",
            "--no-dash-inwards",
            help=(
                "by default, dash are pushed inwards. "
                "Use '--no-dash-inwards' to have the dash start at the sequence level."
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
    line_width: Annotated[
        int,
        typer.Option(
            "-w",
            "--line-width",
            help="specify the maximum line width.",
        ),
    ] = DEFAULT_LINE_WIDTH,
    silent_mode: Annotated[
        bool,
        typer.Option(
            "-S",
            "--silent",
            help="silent mode, don't print config when processing file(s)",
        ),
    ] = False,
    _version: Annotated[
        bool,
        typer.Option("-v", "--version", help="show yamkix version", callback=version_callback),
    ] = False,
    files: Annotated[
        list[Path] | None, typer.Argument(help="the files to process, cannot be used with -i/--input")
    ] = None,
) -> None:
    """Format yaml input file.

    Yamkix formats YAML files with opinionated styling rules.
    By default, explicit_start is 'On', explicit_end is 'Off'
    and array elements are pushed inwards the start of the
    matching sequence. Comments are preserved if you use the default
    parsing mode 'rt'.
    """
    # Create configuration
    yamkix_configs = create_yamkix_config_from_typer_args(
        input_file=input_file,
        output_file=output_file,
        stdout=stdout,
        typ=typ.value,
        no_explicit_start=no_explicit_start,
        explicit_end=explicit_end,
        no_quotes_preserved=no_quotes_preserved,
        default_flow_style=default_flow_style,
        no_dash_inwards=no_dash_inwards,
        spaces_before_comment=spaces_before_comment,
        enforce_double_quotes=enforce_double_quotes,
        line_width=line_width,
        files=files,
    )
    console = get_stderr_console()
    for config in yamkix_configs:
        if not silent_mode:
            print_yamkix_config(config)
        try:
            # Process the file(s)
            round_trip_and_format(config)
        except InvalidYamlContentError as e:
            console.print(rf"Error processing \[{config.io_config.input_display_name}]: {e}", style="error")
            console.print(e.__cause__, style="error")


if __name__ == "__main__":
    app()  # pragma: no cover
