"""Load a yaml file and save it formatted according to some rules."""

import sys
from copy import deepcopy
from io import StringIO
from pathlib import Path
from typing import TextIO

from ruamel.yaml import YAML
from ruamel.yaml.comments import CommentedBase
from ruamel.yaml.parser import ParserError
from ruamel.yaml.scanner import ScannerError

from yamkix.comments import process_comments
from yamkix.config import YamkixConfig
from yamkix.errors import InvalidYamlContentError
from yamkix.helpers import convert_single_to_double_quotes, strip_leading_double_space
from yamkix.yaml_writer import get_opinionated_yaml_writer


def round_trip_and_format(yamkix_config: YamkixConfig) -> None:
    """Load a file and save it formatted.

    Arguments:
        yamkix_config: The configuration for the Yamkix processing.

    Returns:
        None

    Raises:
        InvalidYamlContentError: If the YAML content is invalid.
    """
    double_quotes_yaml = None
    yaml = get_opinionated_yaml_writer(yamkix_config)
    if yamkix_config.quotes_preserved is False and yamkix_config.enforce_double_quotes:
        double_quotes_yaml = deepcopy(yaml)
        double_quotes_yaml.preserve_quotes = True
    yamkix_io_config = yamkix_config.io_config
    input_file = yamkix_io_config.input
    if input_file is not None:
        with Path(input_file).open(encoding="UTF-8") as f_input:
            parsed = yaml.load_all(f_input.read())
    else:
        parsed = yaml.load_all(sys.stdin.read())
    ready_for_dump = []
    try:
        # Read the parsed content to force the scanner to issue errors if any
        ready_for_dump = list(parsed)

    except (ScannerError, ParserError) as parsing_error:
        raise InvalidYamlContentError from parsing_error
    yamkix_dump_all(
        one_or_more_items=ready_for_dump,
        yaml=yaml,
        dash_inwards=yamkix_config.dash_inwards,
        output_file=yamkix_io_config.output,
        spaces_before_comment=yamkix_config.spaces_before_comment,
        double_quotes_yaml=double_quotes_yaml,
    )


def yamkix_dump_all(  # noqa: PLR0913
    one_or_more_items: list[CommentedBase],
    yaml: YAML,
    dash_inwards: bool,
    output_file: str | None,
    spaces_before_comment: int | None,
    double_quotes_yaml: YAML | None = None,
) -> None:
    """Dump all the documents from the input structure.

    Args:
        one_or_more_items: The YAML document(s) to dump. The result of a `yaml.load_all` call.
        yaml: The `YAML` writer to use. Configured from a `YamkixConfig` instance.
        dash_inwards: Whether to apply dash inwards formatting.
        output_file: The output file to write to. If `None`, write to stdout.
        spaces_before_comment: The number of spaces to use before comments.
        double_quotes_yaml: An optional `YAML` writer for double quotes management.
            This `YAML` instance should be configured like the `yaml` one but with `preserve` quotes set to `True`

    """
    # Clear the output file if it is a file and it exists
    if output_file is not None and (output_file_path := Path(output_file)).is_file():  # Walrus baby
        with output_file_path.open(mode="w", encoding="UTF-8") as _:
            pass
    for doc in one_or_more_items:
        # If we have a double_quotes_yaml instance, then proceed to an extra roundtrip
        # the first one, using the `yaml` instance, will remove unnecessary quotes
        # and convert all quotes to single quote
        # Then we read again the document, with a parser that preserve quotes
        # and we replace all SingleQuotedScalarString by DoubleQuotedScalarString
        # and we finally dump the transformed document
        if double_quotes_yaml is not None:
            doc_after_first_rt_as_string = StringIO()
            yaml.dump(data=doc, stream=doc_after_first_rt_as_string)
            single_item = double_quotes_yaml.load(doc_after_first_rt_as_string.getvalue())
            single_item = convert_single_to_double_quotes(single_item)
            yaml_instance = double_quotes_yaml
        else:
            yaml_instance = yaml
            single_item = doc
        if output_file is None:
            out = sys.stdout
            yamkix_dump_one(
                single_item=single_item,
                yaml=yaml_instance,
                dash_inwards=dash_inwards,
                out=out,
                spaces_before_comment=spaces_before_comment,
            )
        else:
            with Path(output_file).open(mode="a", encoding="UTF-8") as out:
                yamkix_dump_one(
                    single_item=single_item,
                    yaml=yaml_instance,
                    dash_inwards=dash_inwards,
                    out=out,
                    spaces_before_comment=spaces_before_comment,
                )


def yamkix_dump_one(
    single_item: CommentedBase,
    yaml: YAML,
    dash_inwards: bool,
    out: TextIO,
    spaces_before_comment: int | None,
) -> None:
    """Dump a single document.

    Args:
        single_item: The YAML document to dump.
            This is the result of a `yaml.load` call, or one of the items from a call to `yaml.load_all`.
        yaml: The YAML writer to use.
        dash_inwards: Whether to apply dash inwards formatting.
        out: The output stream to write to.
        spaces_before_comment: The number of spaces to use before comments.
    """
    if spaces_before_comment is not None:
        process_comments(data=single_item, column=spaces_before_comment)
    if dash_inwards and type(single_item).__name__ == "CommentedSeq":
        yaml.dump(data=single_item, stream=out, transform=strip_leading_double_space)
    else:
        yaml.dump(data=single_item, stream=out)
