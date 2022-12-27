"""Test helpers."""
import unittest

from yamkix import __version__
from yamkix.helpers import get_version_string, remove_all_linebreaks, string_is_comment, strip_leading_double_space


class TestHelpers(unittest.TestCase):
    """Provide unit tests for the helpers package."""

    def test_get_version_string(self):
        """Test get_version_string."""
        sut = get_version_string()
        self.assertEqual(sut, "yamkix v" + __version__)

    def test_remove_all_linebreaks(self):
        """Test remove_all_linebreaks.

        when there is a trailing linebreak
        """
        s_input = "yolo\n"
        sut = remove_all_linebreaks(s_input)
        self.assertEqual(sut, "yolo")

    def test_remove_all_linebreaks_no_linebreak(self):
        """Test remove_all_linebreaks.

        when there is no trailing linebreak
        """
        s_input = "yolo"
        sut = remove_all_linebreaks(s_input)
        self.assertEqual(sut, "yolo")

    def test_remove_all_linebreaks_more_than_one(self):
        """Test remove_all_linebreaks.

        when there is more than one linebreak
        """
        s_input = "line1\nline2\n"
        sut = remove_all_linebreaks(s_input)
        self.assertEqual(sut, "line1line2")

    def test_string_is_comment(self):
        """Test string_is_comment.

        When it is a comment
        """
        s_input = "# I am a comment"
        self.assertTrue(string_is_comment(s_input))

    def test_string_is_comment_when_not(self):
        """Test string_is_comment.

        When it is not a comment
        """
        s_input = "I am not a comment"
        self.assertFalse(string_is_comment(s_input))

    def test_string_is_comment_with_two_following_comment_tokens(self):
        """Test string_is_comment.

        When it is a comment with another #
        """
        s_input = "## I am a comment"
        self.assertTrue(string_is_comment(s_input))

    def test_string_is_comment_with_two_comment_tokens(self):
        """Test string_is_comment.

        When it is a comment with another #
        """
        s_input = "# I am a comment #"
        self.assertTrue(string_is_comment(s_input))

    def test_string_is_comment_when_not_because_not_leading(self):
        """Test string_is_comment.

        When it is not a comment
        """
        s_input = " # I am not a comment"
        self.assertFalse(string_is_comment(s_input))

    def test_string_is_comment_when_not_because_ending(self):
        """Test string_is_comment.

        When it is not a comment
        """
        s_input = "I am not a comment #"
        self.assertFalse(string_is_comment(s_input))

    def test_strip_leading_double_space(self):
        """Test strip_leading_double_space.

        when there are
        """
        stream = "  text1\n  text2"

        actual = strip_leading_double_space(stream)
        expected = "text1\ntext2"
        self.assertEqual(actual, expected)

    def test_strip_leading_double_space_mixed(self):
        """Test strip_leading_double_space.

        when there are but not everywhere
        """
        stream = "  text1\ntext2\n  text3\n"

        actual = strip_leading_double_space(stream)
        expected = "text1\ntext2\ntext3\n"
        self.assertEqual(actual, expected)

    def test_strip_leading_double_space_when_none(self):
        """Test strip_leading_double_space.

        when there are none
        """
        stream = "text1\ntext2\n"
        actual = strip_leading_double_space(stream)
        self.assertEqual(actual, stream)
