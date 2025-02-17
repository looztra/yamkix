"""Useful (I guess) helpers."""

from typing import Any

from yamkix import __version__

StreamType = Any  # Copied from ruamel.yaml compat.py line 58


def get_version_string() -> str:
    """Return the version string."""
    return "yamkix v" + __version__


def print_version() -> None:
    """Print version."""
    print(get_version_string())  # noqa: T201


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
