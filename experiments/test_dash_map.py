import sys

import ruamel.yaml


def strip_leading_double_space(stream):
    stream = stream.removeprefix("  ")
    return stream.replace("\n  ", "\n")


yaml = ruamel.yaml.YAML()
#
# yaml.indent(mapping=2, sequence=2, offset=0)
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
