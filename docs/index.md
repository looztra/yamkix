# Yamkix

## Why?

- Because I like my `yaml` file to be nicely formatted and there is not _out of the box_ **default** format rules.
- Because
  <https://marketplace.visualstudio.com/items?itemName=redhat.vscode-yaml>
  does not add explicit start of documents and I don't like it this
  way
- Because I'm not a `js` / `typescript` dev so I don't want to go into a
  VSCode extension with client and server language

## What?

``` shell
> ./yamkix -h
 Usage: yamkix [OPTIONS]

 Format yaml input file.

 Yamkix formats YAML files with opinionated styling rules. By default, explicit_start is 'On', explicit_end is 'Off' and array elements are pushed inwards the start of the matching
 sequence. Comments are preserved thanks to default parsing mode 'rt'.

╭─ Options ───────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╮
│ --input                  -i      TEXT     the file to parse or 'STDIN'. Defaults to 'STDIN' if not specified [default: None]                                                        │
│ --output                 -o      TEXT     the name of the file to generate (can be 'STDOUT') (same as input file if not specified, hence 'STDOUT' if 'STDIN' as input)              │
│                                           [default: None]                                                                                                                           │
│ --stdout                 -s               output is STDOUT whatever the value for input (-i) and output (-o)                                                                        │
│ --typ                    -t      TEXT     the yaml parser mode. Can be 'safe' or 'rt' [default: rt]                                                                                 │
│ --no-explicit-start      -n               by default, explicit start of the yaml doc is 'On', you can disable it with this option                                                   │
│ --explicit-end           -e               by default, explicit end of the yaml doc is 'Off', you can enable it with this option                                                     │
│ --no-quotes-preserved    -q               by default, quotes are preserved you can disable this with this option                                                                    │
│ --default-flow-style     -f               enable the default flow style 'Off' by default. In default flow style (with typ='rt'), maps and lists are written like json               │
│ --no-dash-inwards        -d               by default, dash are pushed inwards use '--no-dash-inwards' to have the dash start at the sequence level                                  │
│ --spaces-before-comment  -c      INTEGER  specify the number of spaces between comments and content. If not specified, comments are left as is. [default: None]                     │
│ --version                -v               show yamkix version                                                                                                                       │
│ --silent                 -S               silent mode, don't print config when processing file(s)                                                                                   │
│ --help                   -h               Show this message and exit.                                                                                                               │
╰─────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯
```

## Configuration

In order to better understand what you can do with the configuration provided, have a look at the dedicated [Configuration](configuration.md) page.

## Where does the name 'yamkix' come from?

- Thanks to
  <http://online-generator.com/name-generator/product-name-generator.php>
  that suggested me `zamkix`. Just switched the starting `z` for the
  `y` of `yaml`

## VSCode Task

- Install the package with `uv tool install yamkix` (or `pip install --user yamkix` if you are not using [uv](https://docs.astral.sh/uv/concepts/tools/))

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
