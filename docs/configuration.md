# Configuration

- Explicit start of yaml docs by default (you can disable it with
  `--no-explicit-start`)
- Quotes preserved by default (you can disable it with
  `--no-quotes-preserved`)
- Arrays elements pushed inwards by default (you can disable it with
  `--no-dash-inwards`)
- Output file is input file by default
- Comments preserved by default thanks to
  [ruamel.yaml](https://pypi.python.org/pypi/ruamel.yaml) `round_trip`
  mode (you can disable it with `--typ safe`)

## To preserve or not to preserve quotes?

- *Quotes preserved* means : if there were quotes in the input, they
  will also be present in the output, and it will be the same type
  (single/double) of quotes
- *Quotes not preserved* means :
  - if quotes are not necessary (around *pure* strings), they will
    be removed
  - if quotes are present around booleans and numbers, they will be
    converted to default (single quotes)
  - if quotes are not present around booleans and numbers, there
    will be no quotes in the output too

**Note**: there is no option for the moment to force the usage of double
quotes when
<span class="title-ref">-q</span>/<span class="title-ref">--no-quotes-preserved</span>
is used.

### Quotes preserved (default behavior)

With input :

``` yaml
---
apiVersion: extensions/v1beta1 # with comment
kind: ReplicaSet
metadata:
  name: tname
  namespace: tns
  annotations:
    string_no_quotes: frontend
    string_single_quotes: 'frontend'
    string_double_quotes: "frontend"
    boolean_no_quotes: true
    boolean_single_quotes: 'true'
    boolean_double_quotes: "true"
    number_no_quotes: 1
    number_single_quotes: '1'
    number_double_quotes: "1"
```

the output will be the same as the input :

``` yaml
---
apiVersion: extensions/v1beta1 # with comment
kind: ReplicaSet
metadata:
  name: tname
  namespace: tns
  annotations:
    string_no_quotes: frontend
    string_single_quotes: 'frontend'
    string_double_quotes: "frontend"
    boolean_no_quotes: true
    boolean_single_quotes: 'true'
    boolean_double_quotes: "true"
    number_no_quotes: 1
    number_single_quotes: '1'
    number_double_quotes: "1"
```

### Quotes not preserved (using <span class="title-ref">-q/--no-quotes-preserved</span>)

With input :

``` yaml
---
apiVersion: extensions/v1beta1 # with comment
kind: ReplicaSet
metadata:
  name: tname
  namespace: tns
  annotations:
    string_no_quotes: frontend
    string_single_quotes: 'frontend'
    string_double_quotes: "frontend"
    boolean_no_quotes: true
    boolean_single_quotes: 'true'
    boolean_double_quotes: "true"
    number_no_quotes: 1
    number_single_quotes: '1'
    number_double_quotes: "1"
```

the output will be :

``` yaml
---
apiVersion: extensions/v1beta1 # with comment
kind: ReplicaSet
metadata:
  name: tname
  namespace: tns
  annotations:
    string_no_quotes: frontend
    string_single_quotes: frontend
    string_double_quotes: frontend
    boolean_no_quotes: true
    boolean_single_quotes: 'true'
    boolean_double_quotes: 'true'
    number_no_quotes: 1
    number_single_quotes: '1'
    number_double_quotes: '1'
```

**Note** : <span class="title-ref">kubesplit</span> is not fully
*Kubernetes* aware for the moment, so it does not try to enforce
this behaviour only on string sensible *kubernetes* resource fields
(<span class="title-ref">.metadata.annotations</span> and
<span class="title-ref">.spec.containers.environment</span> values)
