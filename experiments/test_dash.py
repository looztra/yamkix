"""Test dash behavior."""

import sys
from typing import Any

import ruamel.yaml

StreamType = Any


def strip_leading_double_space(stream: StreamType) -> StreamType:
    """Strip leading double space."""
    stream = stream.removeprefix("  ")
    return stream.replace("\n  ", "\n")


yaml = ruamel.yaml.YAML()
yaml.indent(mapping=2, sequence=4, offset=2)
inp = """\
- op: replace
path: /x/y/z
value:
  - name: dummy
    property: fake

- op: replace
  path: /a/b/c
  value: roger
"""

data = yaml.load(inp)

yaml.dump(data, sys.stdout, transform=strip_leading_double_space)
