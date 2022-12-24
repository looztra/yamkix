"""Load a yaml file and save it formatted according to some rules."""
from __future__ import print_function

import sys
import os

from ruamel.yaml.scanner import ScannerError
from yamkix.config import print_yamkix_config, YamkixConfig
from yamkix.yaml_writer import get_opinionated_yaml_writer
from yamkix.args import parse_cli
from yamkix.comments import process_comments
from yamkix.helpers import (
    print_version,
    strip_leading_double_space,
)


def round_trip_and_format(yamkix_config: YamkixConfig):
    """Load a file and save it formated.

    FIXME
    """
    yaml = get_opinionated_yaml_writer(yamkix_config)
    yamkix_io_config = yamkix_config.io_config
    input_file = yamkix_io_config.input
    output_file = yamkix_io_config.output
    dash_inwards = yamkix_config.dash_inwards
    spaces_before_comment = yamkix_config.spaces_before_comment
    if input_file is not None:
        with open(input_file, mode="rt", encoding="UTF-8") as f_input:
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
        with open(output_file, mode="w", encoding="UTF-8") as _:
            pass
    for doc in one_or_more_items:
        if output_file is None:
            yamkix_dump_one(
                doc, yaml, dash_inwards, out, spaces_before_comment
            )
        else:
            with open(output_file, mode="a", encoding="UTF-8") as out:
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


def main():
    """(re)format yaml."""
    yamkix_config = parse_cli(sys.argv[1:])
    if yamkix_config.version:
        print_version()
    else:
        print_yamkix_config(yamkix_config)
        round_trip_and_format(yamkix_config)


if __name__ == "__main__":
    main()
