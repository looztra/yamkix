"""Deal with comments."""
from ruamel.yaml.comments import CommentedBase, NoComment
from ruamel.yaml.tokens import CommentToken
from ruamel.yaml.error import CommentMark
from yamkix.helpers import (
    remove_all_linebreaks,
    string_is_comment,
)


def yamkix_add_eol_comment(self, comment, key=NoComment, column=None):
    """Custom add_eol_comment function.

    We need to be able to tune the number of spaces between
    the content and the comment for CommentedSeqs and CommentedMaps
    see https://stackoverflow.com/q/60915926
    """
    # pylint: disable=protected-access
    org_col = column
    if column is None:
        try:
            column = self._yaml_get_column(key)
        except AttributeError:
            column = 0
    if comment[0] != "#":
        comment = "# " + comment
    if (
        org_col != 0
    ):  # only do this if the specified column is not the beginning of the line
        if comment[0] == "#":
            additional_spaces = 1 if org_col is None else org_col - 1
            comment = " " * additional_spaces + comment
            column = 0
    start_mark = CommentMark(column)
    comment_as_list = [CommentToken(comment, start_mark, None), None]
    self._yaml_add_eol_comment(comment_as_list, key=key)


CommentedBase.yaml_add_eol_comment = yamkix_add_eol_comment


def process_single_comment(data, comment, key, column):
    """Process a single comment."""
    comment = remove_all_linebreaks(comment)
    data.yaml_add_eol_comment(comment, key, column=column)


def fix_for_issue29(data, key):
    """Fix issue#29."""
    if data.ca.items[key][3] is not None:
        data.ca.items[key][3] = None


def process_comments(data, column=None):
    """Reposition comments."""
    if isinstance(data, dict):
        if data.ca and data.ca.items:
            # print("CommentedMap " + str(data.ca.items), file=sys.stderr)
            for key in data.ca.items.keys():
                if data.ca.items[key][2]:
                    comment = data.ca.items[key][2].value
                    fix_for_issue29(data, key)
                    if string_is_comment(comment):
                        process_single_comment(data, comment, key, column)
        for key, val in data.items():
            process_comments(key, column=column)
            process_comments(val, column=column)
    elif isinstance(data, list):
        if data.ca and data.ca.items:
            # print("CommentedSeq " + str(data.ca.items), file=sys.stderr)
            for key in data.ca.items.keys():
                if data.ca.items[key][0]:
                    comment = data.ca.items[key][0].value
                    if string_is_comment(comment):
                        process_single_comment(data, comment, key, column)
        for elem in data:
            process_comments(elem, column=column)
