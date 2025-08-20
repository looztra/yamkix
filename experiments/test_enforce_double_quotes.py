"""Experiment to enforce double quotes in YAML output."""

import io
import sys
from copy import deepcopy

from ruamel.yaml import YAML
from ruamel.yaml.scalarstring import DoubleQuotedScalarString, SingleQuotedScalarString


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
yaml = YAML(typ="rt")
yaml.preserve_quotes = False
double_quote_yaml = deepcopy(yaml)
double_quote_yaml.preserve_quotes = True

inp = """\
i-am-a-string-with-double-quotes: "some string with double-quote"
i-am-a-string-with-single-quotes: 'another-string-with-simple-quote'
i-am-a-string-without-quotes: look ma, no quotes!
i-am-a-real-number: 1.722
i-am-a-string-number: "1.722"
i-am-a-real-boolean: true
i-am-a-string-boolean: "true"
"""

first_rt_data = yaml.load(inp)

doc_after_first_rt_as_string = io.StringIO()
yaml.dump(first_rt_data, stream=doc_after_first_rt_as_string)
data = double_quote_yaml.load(doc_after_first_rt_as_string.getvalue())
data = convert_single_to_double_quotes(data)
double_quote_yaml.dump(data, sys.stdout)
