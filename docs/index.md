# Yamkix

## Why?

- Because I like my `yaml` file to be _nicely_ formatted and there is not _out of the box_ **default** format rules.
- Because
  <https://marketplace.visualstudio.com/items?itemName=redhat.vscode-yaml>
  does not add explicit start of documents and I don't like it this
  way
- Because I'm not a `js` / `typescript` dev so I don't want to go into a
  VSCode extension with client and server language

## What?

``` shell
╰─»  yamkix --help

 Usage: yamkix [OPTIONS] [FILES]...

 Format yaml input file.

 Yamkix formats YAML files with opinionated styling rules. By default, explicit_start is 'On', explicit_end is 'Off' and array elements are pushed inwards the start of the matching
 sequence. Comments are preserved if you use the default parsing mode 'rt'.

╭─ Arguments ─────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╮
│   files      [FILES]...  the files to process, cannot be used with -i/--input [default: None]                                                                                       │
╰─────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯
╭─ Options ───────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╮
│ --input                  -i      TEXT       the single file to parse or 'STDIN'. Defaults to 'STDIN' if not specified. Cannot be used if the list of files to process is specified  │
│                                             using arguments. If you need to specify multiple files, pass them as arguments instead of using this option. This flag will not be      │
│                                             honored if the input file(s) has/have been specify using arguments (and not -i/--input)                                                 │
│                                             [default: None]                                                                                                                         │
│ --output                 -o      TEXT       the name of the file to generate (can be 'STDOUT'). Will be the same as input file if not specified, and 'STDOUT' if 'STDIN' was        │
│                                             specified as input. This flag will not be honored if the input file(s) has/have been specify using arguments (and not -i/--input)       │
│                                             [default: None]                                                                                                                         │
│ --stdout                 -s                 output is 'STDOUT' whatever the value for input (-i/--input) and output (-o/--output). This flag will not be honored if the input       │
│                                             file(s) has/have been specify using arguments (and not -i/--input)                                                                      │
│ --typ                    -t      [safe|rt]  the yaml parser mode. Can be 'safe' or 'rt'. Using 'safe' will remove all comments. [default: rt]                                       │
│ --no-explicit-start      -n                 by default, explicit start of the yaml doc is 'On', you can disable it with this option.                                                │
│ --explicit-end           -e                 by default, explicit end of the yaml doc is 'Off', you can enable it with this option.                                                  │
│ --no-quotes-preserved    -q                 by default, quotes are preserved you can disable this with this option.                                                                 │
│ --enforce-double-quotes  -E                 enforce double quotes when --no-quotes-preserved is activated (by default, you get single quotes which is the recommended behavior)     │
│ --default-flow-style     -f                 enable the default flow style 'Off' by default. In default flow style (with --typ 'rt'), maps and lists are written like json.          │
│ --no-dash-inwards        -d                 by default, dash are pushed inwards. Use '--no-dash-inwards' to have the dash start at the sequence level.                              │
│ --spaces-before-comment  -c      INTEGER    specify the number of spaces between comments and content. If not specified, comments are left as is. [default: None]                   │
│ --silent                 -S                 silent mode, don't print config when processing file(s)                                                                                 │
│ --version                -v                 show yamkix version                                                                                                                     │
│ --help                   -h                 Show this message and exit.                                                                                                             │
╰─────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯
```

## Usage

You would basically use `yamkix` to enforce the format of a single or of multiple yaml files.

Check the [dedicated page](usage.md).

## Configuration

In order to better understand what you can do with the configuration provided, have a look at the dedicated [Configuration](configuration.md) page.

## Where does the name `yamkix` come from?

- Thanks to
  <http://online-generator.com/name-generator/product-name-generator.php>
  that suggested me `zamkix`. Just switched the starting `z` for the
  `y` of `yaml`
