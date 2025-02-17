"""Test helpers."""

from yamkix import __version__
from yamkix.helpers import get_version_string, remove_all_linebreaks, string_is_comment, strip_leading_double_space


def test_get_version_string() -> None:
    """Test get_version_string."""
    sut = get_version_string()
    assert sut == "yamkix v" + __version__


def test_remove_all_linebreaks() -> None:
    """Test remove_all_linebreaks.

    when there is a trailing linebreak
    """
    s_input = "yolo\n"
    sut = remove_all_linebreaks(s_input)
    assert sut == "yolo"


def test_remove_all_linebreaks_no_linebreak() -> None:
    """Test remove_all_linebreaks.

    when there is no trailing linebreak
    """
    s_input = "yolo"
    sut = remove_all_linebreaks(s_input)
    assert sut == "yolo"


def test_remove_all_linebreaks_more_than_one() -> None:
    """Test remove_all_linebreaks.

    when there is more than one linebreak
    """
    s_input = "line1\nline2\n"
    sut = remove_all_linebreaks(s_input)
    assert sut == "line1line2"


def test_string_is_comment() -> None:
    """Test string_is_comment.

    When it is a comment
    """
    s_input = "# I am a comment"
    assert string_is_comment(s_input)


def test_string_is_comment_when_not() -> None:
    """Test string_is_comment.

    When it is not a comment
    """
    s_input = "I am not a comment"
    assert not string_is_comment(s_input)


def test_string_is_comment_with_two_following_comment_tokens() -> None:
    """Test string_is_comment.

    When it is a comment with another #
    """
    s_input = "## I am a comment"
    assert string_is_comment(s_input)


def test_string_is_comment_with_two_comment_tokens() -> None:
    """Test string_is_comment.

    When it is a comment with another #
    """
    s_input = "# I am a comment #"
    assert string_is_comment(s_input)


def test_string_is_comment_when_not_because_not_leading() -> None:
    """Test string_is_comment.

    When it is not a comment
    """
    s_input = " # I am not a comment"
    assert not string_is_comment(s_input)


def test_string_is_comment_when_not_because_ending() -> None:
    """Test string_is_comment.

    When it is not a comment
    """
    s_input = "I am not a comment #"
    assert not string_is_comment(s_input)


def test_strip_leading_double_space() -> None:
    """Test strip_leading_double_space.

    when there are
    """
    stream = "  text1\n  text2"

    actual = strip_leading_double_space(stream)
    expected = "text1\ntext2"
    assert actual == expected


def test_strip_leading_double_space_mixed() -> None:
    """Test strip_leading_double_space.

    when there are but not everywhere
    """
    stream = "  text1\ntext2\n  text3\n"

    actual = strip_leading_double_space(stream)
    expected = "text1\ntext2\ntext3\n"
    assert actual == expected


def test_strip_leading_double_space_when_none() -> None:
    """Test strip_leading_double_space.

    when there are none
    """
    stream = "text1\ntext2\n"
    actual = strip_leading_double_space(stream)
    assert actual == stream
