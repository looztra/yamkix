"""Test dash behavior for map."""

import sys
from typing import Any

import ruamel.yaml

StreamType = Any


def strip_leading_double_space(stream: StreamType = Any) -> StreamType:
    """Strip leading double space."""
    stream = stream.removeprefix("  ")
    return stream.replace("\n  ", "\n")


yaml = ruamel.yaml.YAML()
yaml.indent(mapping=2, sequence=4, offset=2)
inp = """\
apiVersion: extensions/v1beta1
kind: Deployment
metadata:
  # Comment 2
  name: crashing-for-tests-because-command
  # Comment 3
  labels:
    name: I-am-a-failure-pod
"""

data = yaml.load(inp)

yaml.dump(data, sys.stdout, transform=strip_leading_double_space)
