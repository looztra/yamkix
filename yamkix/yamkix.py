"""Load a yaml file and save it formatted according to some rules."""
from __future__ import print_function

import sys
import os

from ruamel.yaml.scanner import ScannerError
from ruamel.yaml.comments import CommentedBase, NoComment
from ruamel.yaml.tokens import CommentToken
from ruamel.yaml.error import CommentMark
from yamkix import __version__
from yamkix.config import print_yamkix_config, YamkixConfig
from yamkix.yaml_writer import get_opinionated_yaml_writer
from yamkix.args import parse_cli


def strip_leading_double_space(stream):
    """Strip the potential leading double spaces in CommentedSeq."""
    if stream.startswith("  "):
        stream = stream[2:]
    return stream.replace("\n  ", "\n")


def format_yaml(yamkix_config: YamkixConfig):
    """Load a file and save it formated.

    :param input_file: the input file
    :param output_file: the output file
    :param explicit_start: write the start of the yaml doc even when there is \
                            only one done in the file
    :param default_flow_style: if False, block style will be used for nested \
                            arrays/maps
    :param dash_inwards: push dash inwards if True
    :param quotes_preserved: preserve quotes if True
    :param parsing_typ: safe or roundtrip (rt) more
    """
    yaml = get_opinionated_yaml_writer(yamkix_config)
    yamkix_io_config = yamkix_config.io_config
    input_file = yamkix_io_config.input
    output_file = yamkix_io_config.output
    dash_inwards = yamkix_config.dash_inwards
    spaces_before_comment = yamkix_config.spaces_before_comment
    if input_file is not None:
        with open(input_file, "rt") as f_input:
            parsed = yaml.load_all(f_input.read())
    else:
        parsed = yaml.load_all(sys.stdin.read())
    ready_for_dump = []
    try:
        # Read the parsed content to force the scanner to issue errors if any
        for data in parsed:
            ready_for_dump.append(data)

    except ScannerError as scanner_error:
        print("Something is wrong in the input file, got error from Scanner")
        print(scanner_error)
        return
    yamkix_dump_all(
        ready_for_dump, yaml, dash_inwards, output_file, spaces_before_comment
    )


def yamkix_dump_all(
    one_or_more_items, yaml, dash_inwards, output_file, spaces_before_comment
):
    """Dump all the documents from the input structure."""
    if output_file is None:
        out = sys.stdout

    # Clear the output file if it is a file and it exists
    if output_file is not None and os.path.isfile(output_file):
        open(output_file, "w").close()
    for doc in one_or_more_items:
        if output_file is None:
            yamkix_dump_one(
                doc, yaml, dash_inwards, out, spaces_before_comment
            )
        else:
            with open(output_file, "a") as out:
                yamkix_dump_one(
                    doc, yaml, dash_inwards, out, spaces_before_comment
                )


def yamkix_dump_one(
    single_item, yaml, dash_inwards, out, spaces_before_comment
):
    """Dump a single document."""
    if spaces_before_comment is not None:
        process_comments(single_item, column=spaces_before_comment)
    if dash_inwards and type(single_item).__name__ == "CommentedSeq":
        yaml.dump(single_item, out, transform=strip_leading_double_space)
    else:
        yaml.dump(single_item, out)


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
    ):  # only do this if the specified colunn is not the beginning of the line
        if comment[0] == "#":
            additional_spaces = 1 if org_col is None else org_col - 1
            comment = " " * additional_spaces + comment
            column = 0
    start_mark = CommentMark(column)
    comment_as_list = [CommentToken(comment, start_mark, None), None]
    self._yaml_add_eol_comment(comment_as_list, key=key)


CommentedBase.yaml_add_eol_comment = yamkix_add_eol_comment


def string_is_comment(a_string):
    """Is it a comment starting with a #."""
    return a_string[0] == "#"


def remove_trailing_linebreak(comment):
    """Remove trailing linebreak."""
    return comment.replace("\n", "")


def process_single_comment(data, comment, key, column):
    """Process a single comment."""
    comment = remove_trailing_linebreak(comment)
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


def print_version():
    """Print version."""
    print("yamkix v" + __version__)


def main():
    """(re)format yaml."""
    yamkix_config = parse_cli(sys.argv[1:])
    if yamkix_config.version:
        print_version()
    else:
        print_yamkix_config(yamkix_config)
        format_yaml(yamkix_config)


if __name__ == "__main__":
    main()
