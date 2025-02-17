"""Play  with flow style."""

import sys

from ruamel.yaml import YAML

yaml = YAML()
yaml.default_flow_style = False

inp = """\
- op: replace
  path: /x/y/z
  value:
    - name: dummy
      property: fake

- op: replace
  path: /a/b/c
  value: roger

- {'a': [1, 2]}
"""

gna = """\
{'a': [1, 2]}
"""

data = yaml.load(inp)

yaml.dump(data, sys.stdout)
