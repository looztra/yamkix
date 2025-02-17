"""Test dash behavior."""

import sys

import ruamel.yaml


def strip_leading_double_space(stream):
    """Strip leading double space."""
    stream = stream.removeprefix("  ")
    return stream.replace("\n  ", "\n")


yaml = ruamel.yaml.YAML()
#
# yaml.indent(mapping=2, sequence=2, offset=0)
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
