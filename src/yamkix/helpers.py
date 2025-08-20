"""Useful (I guess) helpers."""

from functools import lru_cache
from typing import Any

from rich.console import Console
from rich.theme import Theme
from ruamel.yaml.scalarstring import DoubleQuotedScalarString, SingleQuotedScalarString

from yamkix.__version__ import __version__

StreamType = Any  # Copied from ruamel.yaml compat.py line 58


def remove_all_linebreaks(comment: StreamType) -> StreamType:
    """Remove trailing linebreak."""
    return comment.replace("\n", "")


def string_is_comment(a_string: str) -> bool:
    """Is it a comment starting with a #."""
    return a_string[0] == "#"


def strip_leading_double_space(stream: StreamType) -> StreamType:
    """Strip the potential leading double spaces in CommentedSeq."""
    stream = stream.removeprefix("  ")
    return stream.replace("\n  ", "\n")


def get_yamkix_version() -> str:
    """Get the current Yamkix version.

    Returns:
        str: The current Yamkix version.
    """
    return __version__


def get_custom_theme() -> Theme:
    """Get the custom theme for the CLI.

    Returns:
        Theme: The custom theme for the CLI.
    """
    return Theme({"info": "dim cyan", "warning": "bold yellow", "error": "bold red"})


@lru_cache
def get_stderr_console() -> Console:
    """Return the CLI rich console."""
    custom_theme = get_custom_theme()
    return Console(theme=custom_theme, stderr=True)


@lru_cache
def get_stdout_console() -> Console:
    """Return the CLI rich console."""
    custom_theme = get_custom_theme()
    return Console(theme=custom_theme, stderr=False)


def convert_single_to_double_quotes(
    obj: Any,  # noqa: ANN401
) -> Any:  # noqa: ANN401
    """Recursively convert single quoted strings to double quoted."""
    if isinstance(obj, dict):
        for key, value in obj.items():
            obj[key] = convert_single_to_double_quotes(value)
    elif isinstance(obj, list):
        for i, item in enumerate(obj):
            obj[i] = convert_single_to_double_quotes(item)
    elif isinstance(obj, SingleQuotedScalarString):
        # Convert single quoted to double quoted
        return DoubleQuotedScalarString(str(obj))
    return obj
