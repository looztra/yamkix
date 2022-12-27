# yamkix

[![Pypi](https://img.shields.io/pypi/v/yamkix.svg)](https://pypi.python.org/pypi/yamkix)

## Why?

- Because I like my yaml file to be nicely formatted
- Because
  <https://marketplace.visualstudio.com/items?itemName=adamvoss.yaml>
  creates (valid) yaml not compatible for kubernetes (and I mainly
  edit yaml files for kubernetes)
- Because
  <https://marketplace.visualstudio.com/items?itemName=redhat.vscode-yaml>
  does not add explicit start of documents and I don't like it this
  way
- Because I'm not a js/typescript dev so I don't want to go into a
  VSCode extension with client and server language

## What?

``` shell
> ./yamkix -h
usage: yamkix [-h] -i INPUT [-t TYP] [-o OUTPUT] [-n] [-e] [-q] [-f] [-d]

Format yaml input file. By default, explicit_start is `On`, explicit_end is
`Off` and array elements are pushed inwards the start of the matching
sequence. Comments are preserved thanks to default parsing mode `rt`.

optional arguments:
  -h, --help            show this help message and exit
  -i INPUT, --input INPUT
                        the file to parse
  -t TYP, --typ TYP     the yaml parser mode. Can be `safe` or `rt`
  -o OUTPUT, --output OUTPUT
                        the name of the file to generate (same as input file
                        if not specied)
  -n, --no-explicit-start
                        by default, explicit start of the yaml doc is `On`,
                        you can disable it with this option
  -e, --explicit-end    by default, explicit end of the yaml doc is `Off`, you
                        can enable it with this option
  -q, --no-quotes-preserved
                        by default, quotes are preserverd you can disable this
                        with this option
  -f, --default-flow-style
                        enable the default flow style `Off` by default. In
                        default flow style (with typ=`rt`), maps and lists are
                        written like json
  -d, --no-dash-inwards
                        by default, dash are pushed inwards use `--no-dash-inwards` to have the dash start at the sequence level
```

## Config

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

## Where does the name 'yamkix' come from?

- Thanks to
  <http://online-generator.com/name-generator/product-name-generator.php>
  that suggested me `zamkix`. Just switched the starting `z` for the
  `y` of `yaml`

## Usage

- Install the package with `pip install --user yamkix`
- Sample **vscode** task :

<!-- end list -->

``` json
{
  "label": "format yaml with yamkix",
  "type": "shell",
  "command": "yamkix --input ${file}",
  "group": "build",
  "presentation": {
    "reveal": "always",
    "panel": "shared"
  },
  "problemMatcher": []
}
```

## Hack

See our [CONTRIBUTING](CONTRIBUTING.md) guide.
