import sys
import ruamel.yaml

yaml = ruamel.yaml.YAML()
yaml.indent(mapping=2, sequence=4, offset=2)
inp = """\
---
# Comment 1
apiVersion: extensions/v1beta1
kind: Deployment
metadata:
# Comment 2
  name: crashing-for-tests-because-command
  # Comment 3
  labels:
    name: I-am-a-failure-pod
spec:
  strategy:
    type: Recreate
            # Comment 5
  template:
    metadata:
      labels: # Comment 4
        name: I-am-a-failure-pod
    spec:
      containers:
      - name: crashy
        image: alpine:3.10.3
        command:
          - /bin/false
"""

data = yaml.load(inp)

yaml.dump(data, sys.stdout)
