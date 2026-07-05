"""Useful (I guess) helpers."""

from functools import lru_cache
from typing import Any

from rich.console import Console
from rich.theme import Theme
from ruamel.yaml.comments import CommentedMap, CommentedSeq
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


def strip_trailing_spaces(stream: StreamType) -> StreamType:
    """Strip the spaces the emitter leaves at line-fold points.

    Works around the `ruamel.yaml` emitter writing a space before deciding to
    break a line (when the configured line width forces wrapping of plain
    scalars or flow collections). Safe to apply to the whole emitted stream:
    the emitter never puts a semantic space at end-of-line (scalars containing
    a space followed by a line break are always emitted double-quoted with
    escapes). See https://github.com/looztra/yamkix/issues/437.

    Args:
        stream: The emitted YAML document as a string.

    Returns:
        The stream with trailing spaces removed from every line.
    """
    return "\n".join(line.rstrip(" ") for line in stream.split("\n"))


def strip_leading_double_space_and_trailing_spaces(stream: StreamType) -> StreamType:
    """Apply both `strip_leading_double_space` and `strip_trailing_spaces`.

    Args:
        stream: The emitted YAML document as a string.

    Returns:
        The stream with leading double spaces and trailing spaces removed.
    """
    return strip_trailing_spaces(strip_leading_double_space(stream))


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


def convert_flow_to_block_style(
    data: Any,  # noqa: ANN401
) -> None:
    """Recursively convert flow-style (JSON-like) collections to block style.

    Sets block style on every `CommentedMap`/`CommentedSeq` at any depth.
    Scalars are left untouched. Only applies in `rt` parsing mode where
    collections are `CommentedMap`/`CommentedSeq` instances; plain dicts and
    lists produced by the `safe` mode are left as-is (they are already dumped
    in block style unless `default_flow_style` says otherwise).

    Note:
        Empty collections are still emitted flow style (`[]` / `{}`) by
        `ruamel.yaml` as block style has no representation for them.

    Args:
        data: The YAML document (or sub-node) to process.
    """
    if isinstance(data, CommentedMap):
        data.fa.set_block_style()
        for key, value in data.items():
            convert_flow_to_block_style(key)
            convert_flow_to_block_style(value)
    elif isinstance(data, CommentedSeq):
        data.fa.set_block_style()
        for item in data:
            convert_flow_to_block_style(item)
