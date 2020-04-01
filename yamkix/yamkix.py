#!/usr/bin/env python
"""Load a yaml file and save it formatted according to some rules"""
from __future__ import print_function
import argparse
import sys
import os
import pkg_resources
from ruamel.yaml import YAML
from ruamel.yaml.scanner import ScannerError
from ruamel.yaml.comments import NoComment, CommentedBase
from ruamel.yaml.tokens import CommentToken
from ruamel.yaml.error import CommentMark
from yamkix import __version__

YAMKIX_VERSION = pkg_resources.require("yamkix")[0].version


def parse_cli():
    """Parse the cli args"""

    parser = argparse.ArgumentParser(
        description="""Yamkix v{}.
            Format yaml input file.
            By default, explicit_start is `On`, explicit_end is `Off`
            and array elements are pushed inwards the start of the
            matching sequence. Comments are preserved thanks to default
            parsing mode `rt`.
        """.format(
            YAMKIX_VERSION
        )
    )
    parser.add_argument(
        "-i",
        "--input",
        required=False,
        help="the file to parse, or STDIN if not specified",
    )
    parser.add_argument(
        "-t",
        "--typ",
        required=False,
        default="rt",
        help="the yaml parser mode. Can be `safe` or `rt`",
    )
    parser.add_argument(
        "-o",
        "--output",
        required=False,
        help="the name of the file to generate \
                            (same as input file if not specied, \
                                hence STDOUT if STDIN as input)",
    )
    parser.add_argument(
        "-n",
        "--no-explicit-start",
        action="store_true",
        help="by default, explicit start of the yaml doc \
                                is `On`, you can disable it with this option",
    )
    parser.add_argument(
        "-e",
        "--explicit-end",
        action="store_true",
        help="by default, explicit end of the yaml doc \
                                is `Off`, you can enable it with this option",
    )
    parser.add_argument(
        "-q",
        "--no-quotes-preserved",
        action="store_true",
        help="by default, quotes are preserved \
                                you can disable this with this option",
    )
    parser.add_argument(
        "-f",
        "--default-flow-style",
        action="store_true",
        help="enable the default flow style \
                                `Off` by default. In default flow style \
                                (with typ=`rt`), maps and lists are written \
                                like json",
    )
    parser.add_argument(
        "-d",
        "--no-dash-inwards",
        action="store_true",
        help="by default, dash are pushed inwards \
                                use `--no-dash-inwards` to have the dash \
                                start at the sequence level",
    )
    parser.add_argument(
        "-s",
        "--stdout",
        action="store_true",
        help="output is STDOUT whatever the value for \
                        input (-i) and output (-o)",
    )

    parser.add_argument(
        "-c",
        "--spaces-before-comment",
        default=None,
        help="specify the number of spaces between comments and content. \
                        If not specified, comments are left as is.",
    )

    parser.add_argument(
        "-v", "--version", action="store_true", help="show yamkix version",
    )

    args = parser.parse_args()

    if args.version:
        my_args = dict()
        my_args["version"] = True
    else:
        my_args = get_input_output(args)
        if args.typ not in ["safe", "rt"]:
            raise ValueError(
                "'%s' is not a valid value for option --typ. "
                "Allowed values are 'safe' and 'rt'" % args.type
            )
        my_args["typ"] = args.typ
        my_args["explicit_start"] = not args.no_explicit_start
        my_args["explicit_end"] = args.explicit_end
        my_args["default_flow_style"] = args.default_flow_style
        my_args["dash_inwards"] = not args.no_dash_inwards
        my_args["quotes_preserved"] = not args.no_quotes_preserved
        if args.spaces_before_comment is None:
            my_args["spaces_before_comment"] = None
        else:
            try:
                my_args["spaces_before_comment"] = int(
                    args.spaces_before_comment
                )
            except ValueError:
                my_args["spaces_before_comment"] = None
        print(
            "[yamkix("
            + YAMKIX_VERSION
            + ")] Processing: input="
            + my_args["input_display_name"]
            + ", output="
            + my_args["output_display_name"]
            + ", typ="
            + my_args["typ"]
            + ", explicit_start="
            + str(my_args["explicit_start"])
            + ", explicit_end="
            + str(my_args["explicit_end"])
            + ", default_flow_style="
            + str(my_args["default_flow_style"])
            + ", quotes_preserved="
            + str(my_args["quotes_preserved"])
            + ", dash_inwards="
            + str(my_args["dash_inwards"])
            + ", spaces_before_comment="
            + str(my_args["spaces_before_comment"]),
            file=sys.stderr,
        )
    return my_args


def get_input_output(argparse_args):
    """Get input, output and associated labels."""
    my_args = dict()
    my_args["input_display_name"] = "STDIN"
    if argparse_args.input is None:
        my_args["input"] = None
    else:
        my_args["input"] = argparse_args.input
        my_args["input_display_name"] = my_args["input"]
    if argparse_args.stdout:
        my_args["output"] = None
    else:
        if (
            argparse_args.output is not None
            and argparse_args.output != "STDOUT"
        ):
            my_args["output"] = argparse_args.output
        else:
            if argparse_args.output == "STDOUT":
                my_args["output"] = None
            else:
                if my_args["input"] is None:
                    my_args["output"] = None
                else:
                    my_args["output"] = argparse_args.input
    if my_args["output"] is None:
        my_args["output_display_name"] = "STDOUT"
    else:
        my_args["output_display_name"] = my_args["output"]
    return my_args


def get_opinionated_yaml_parser(parser_args):
    """Configure a yaml parser/formatter the yamkix way."""
    yaml = YAML(typ=parser_args["typ"])
    yaml.width = 2048
    yaml.explicit_start = parser_args["explicit_start"]
    yaml.explicit_end = parser_args["explicit_end"]
    yaml.default_flow_style = parser_args["default_flow_style"]
    yaml.preserve_quotes = parser_args["quotes_preserved"]

    if parser_args["dash_inwards"]:
        yaml.indent(mapping=2, sequence=4, offset=2)
    return yaml


def strip_leading_double_space(stream):
    """Strip the potential leading double spaces in CommentedSeq."""
    if stream.startswith("  "):
        stream = stream[2:]
    return stream.replace("\n  ", "\n")


def format_yaml(parsed_args):
    """
    Load a file and save it formated :
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
    yaml = get_opinionated_yaml_parser(parsed_args)
    input_file = parsed_args["input"]
    output_file = parsed_args["output"]
    dash_inwards = parsed_args["dash_inwards"]
    spaces_before_comment = parsed_args["spaces_before_comment"]
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
    """Is it a comment starting with a #?"""
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
                    #
                    # Issue #29
                    # list: # this is a comment that kills it
                    #   - a
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
    """(re)format yaml"""
    parsed_args = parse_cli()
    if "version" in parsed_args and parsed_args["version"]:
        print_version()
    else:
        format_yaml(parsed_args)


if __name__ == "__main__":
    main()