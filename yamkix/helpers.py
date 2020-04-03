"""Useful (I guess) helpers."""
from yamkix import __version__


def print_version():
    """Print version."""
    print("yamkix v" + __version__)


def remove_trailing_linebreak(comment):
    """Remove trailing linebreak."""
    return comment.replace("\n", "")


def string_is_comment(a_string):
    """Is it a comment starting with a #."""
    return a_string[0] == "#"


def strip_leading_double_space(stream):
    """Strip the potential leading double spaces in CommentedSeq."""
    if stream.startswith("  "):
        stream = stream[2:]
    return stream.replace("\n  ", "\n")
