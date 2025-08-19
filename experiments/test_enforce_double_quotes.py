"""Experiment to enforce double quotes in YAML output."""

import io
import sys

from ruamel.yaml import YAML
from ruamel.yaml.scalarstring import DoubleQuotedScalarString, SingleQuotedScalarString


def preserved_quotes_yaml() -> YAML:
    """Create a YAML instance that enforces double quotes for all quoted strings."""
    yaml = YAML(typ="rt")
    yaml.preserve_quotes = True
    return yaml


def convert_single_to_double_quotes(obj):  # noqa: ANN001, ANN201
    """Recursively convert single quoted strings to double quoted."""
    if isinstance(obj, dict):
        for key, value in obj.items():
            obj[key] = convert_single_to_double_quotes(value)
    elif isinstance(obj, list):
        for i, item in enumerate(obj):
            obj[i] = convert_single_to_double_quotes(item)
    elif isinstance(obj, SingleQuotedScalarString):
        # Convert single quoted to double quoted
        return DoubleQuotedScalarString(str(obj))
    return obj


# Test the implementation
single_quote_yaml = YAML(typ="rt")
single_quote_yaml.preserve_quotes = False
double_quote_yaml = preserved_quotes_yaml()

inp = """\
i-am-a-string-with-double-quotes: "some string with double-quote"
i-am-a-string-with-single-quotes: 'another-string-with-simple-quote'
i-am-a-string-without-quotes: look ma, no quotes!
i-am-a-real-number: 1.722
i-am-a-string-number: "1.722"
i-am-a-real-boolean: true
i-am-a-string-boolean: "true"
"""

first_rt_data = single_quote_yaml.load(inp)
string_io = io.StringIO()
single_quote_yaml.dump(first_rt_data, stream=string_io)
data = double_quote_yaml.load(string_io.getvalue())
data = convert_single_to_double_quotes(data)
double_quote_yaml.dump(data, sys.stdout)
