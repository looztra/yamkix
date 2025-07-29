"""Load a yaml file and save it formatted according to some rules."""

import sys
from pathlib import Path
from typing import TextIO

from ruamel.yaml import YAML
from ruamel.yaml.scanner import ScannerError

from yamkix.comments import process_comments
from yamkix.config import YamkixConfig
from yamkix.helpers import strip_leading_double_space
from yamkix.yaml_writer import get_opinionated_yaml_writer


def round_trip_and_format(yamkix_config: YamkixConfig) -> None:
    """Load a file and save it formatted.

    FIXME
    """
    yaml = get_opinionated_yaml_writer(yamkix_config)
    yamkix_io_config = yamkix_config.io_config
    input_file = yamkix_io_config.input
    output_file = yamkix_io_config.output
    dash_inwards = yamkix_config.dash_inwards
    spaces_before_comment = yamkix_config.spaces_before_comment
    if input_file is not None:
        with Path(input_file).open(encoding="UTF-8") as f_input:
            parsed = yaml.load_all(f_input.read())
    else:
        parsed = yaml.load_all(sys.stdin.read())
    ready_for_dump = []
    try:
        # Read the parsed content to force the scanner to issue errors if any
        ready_for_dump = list(parsed)

    except ScannerError as scanner_error:
        print("Something is wrong in the input file, got error from Scanner")  # noqa: T201
        print(scanner_error)  # noqa: T201
        return
    yamkix_dump_all(ready_for_dump, yaml, dash_inwards, output_file, spaces_before_comment)


def yamkix_dump_all(
    one_or_more_items: list, yaml: YAML, dash_inwards: bool, output_file: str | None, spaces_before_comment: int | None
) -> None:
    """Dump all the documents from the input structure."""
    # Clear the output file if it is a file and it exists
    if output_file is not None and (output_file_path := Path(output_file)).is_file:  # Walrus baby
        with output_file_path.open(mode="w", encoding="UTF-8") as _:
            pass
    for doc in one_or_more_items:
        if output_file is None:
            out = sys.stdout
            yamkix_dump_one(doc, yaml, dash_inwards, out, spaces_before_comment)
        else:
            with Path(output_file).open(mode="a", encoding="UTF-8") as out:
                yamkix_dump_one(doc, yaml, dash_inwards, out, spaces_before_comment)


def yamkix_dump_one(
    single_item: dict, yaml: YAML, dash_inwards: bool, out: TextIO, spaces_before_comment: int | None
) -> None:
    """Dump a single document."""
    if spaces_before_comment is not None:
        process_comments(single_item, column=spaces_before_comment)  # pyright: ignore[reportArgumentType]
    if dash_inwards and type(single_item).__name__ == "CommentedSeq":
        yaml.dump(single_item, out, transform=strip_leading_double_space)
    else:
        yaml.dump(single_item, out)
