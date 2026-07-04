# CLI options

Information-oriented reference for the `yamkix` command line. For guided examples, see the [how-to guides](../how-to/format-files.md).

## Synopsis

```text
yamkix [OPTIONS] [FILES]...
```

## Arguments

| Argument | Description |
| -------- | ----------- |
| `FILES...` | the files to process, cannot be used with `-i/--input` |

## Options

| Option | Short | Type | Default | Description |
| ------ | ----- | ---- | ------- | ----------- |
| `--input` | `-i` | TEXT | `None` (STDIN) | the single file to parse or `STDIN`. Cannot be used if the list of files to process is specified using arguments. |
| `--output` | `-o` | TEXT | `None` | the name of the file to generate (can be `STDOUT`). Will be the same as input file if not specified, and `STDOUT` if `STDIN` was specified as input. |
| `--stdout` | `-s` | flag | off | output is `STDOUT` whatever the value for input (`-i/--input`) and output (`-o/--output`). |
| `--typ` | `-t` | `safe`\|`rt` | `rt` | the yaml parser mode. Using `safe` will remove all comments. |
| `--no-explicit-start` | `-n` | flag | off | by default, explicit start of the yaml doc is 'On', you can disable it with this option. |
| `--explicit-end` | `-e` | flag | off | by default, explicit end of the yaml doc is 'Off', you can enable it with this option. |
| `--no-quotes-preserved` | `-q` | flag | off | by default, quotes are preserved, you can disable this with this option. |
| `--enforce-double-quotes` | `-E` | flag | off | enforce double quotes when `--no-quotes-preserved` is activated (by default, you get single quotes which is the recommended behavior). |
| `--default-flow-style` | `-f` | flag | off | enable the default flow style, 'Off' by default. In default flow style (with `--typ rt`), maps and lists are written like json. |
| `--enforce-block-style` | `-B` | flag | off | convert flow-style (JSON-like) maps and lists to block style. Overrides `--default-flow-style`. Empty collections (`[]` and `{}`) are kept as-is. |
| `--no-dash-inwards` | `-d` | flag | off | by default, dash are pushed inwards. Use `--no-dash-inwards` to have the dash start at the sequence level. |
| `--spaces-before-comment` | `-c` | INTEGER | `None` | specify the number of spaces between comments and content. If not specified, comments are left as is. |
| `--align-comments` | `-a` | flag | off | align EOL comments within each dict/list to the maximum column. |
| `--line-width` | `-w` | INTEGER | `2048` | specify the maximum line width. |
| `--silent` | `-S` | flag | off | silent mode, don't print config when processing file(s). |
| `--summary` | | flag | off | print a summary of the processing statistics after all files have been processed. |
| `--version` | `-v` | flag | | show yamkix version. |
| `--help` | `-h` | flag | | show the help message and exit. |

## Defaults summary

Running `yamkix` without any option applies the following configuration:

- `parsing_mode = rt` (comments preserved)
- `explicit_start = True` (`---` added)
- `explicit_end = False`
- `default_flow_style = False`
- `enforce_block_style = False` (input collection styles preserved)
- `dash_inwards = True`
- `quotes_preserved = True`
- `enforce_double_quotes = False`
- `spaces_before_comment = None` (comments left as is)
- `align_comments = False`
- `line_width = 2048`
- input `STDIN`, output `STDOUT` (or output = input file when `-i/--input` is a file)

## `--help` output

```text
 Usage: yamkix [OPTIONS] [FILES]...

 Format yaml input file.

 Yamkix formats YAML files with opinionated styling rules.
 By default, explicit_start is 'On', explicit_end is 'Off'
 and array elements are pushed inwards the start of the
 matching sequence. Comments are preserved if you use the default
 parsing mode 'rt'.

╭─ Arguments ──────────────────────────────────────────────────────────╮
│   files      [FILES]...  the files to process, cannot be used with   │
│                          -i/--input                                  │
╰──────────────────────────────────────────────────────────────────────╯
╭─ Options ────────────────────────────────────────────────────────────╮
│ --input                  -i      TEXT       the single file to parse │
│                                             or 'STDIN'.              │
│ --output                 -o      TEXT       the name of the file to  │
│                                             generate (can be         │
│                                             'STDOUT').               │
│ --stdout                 -s                 output is 'STDOUT'.      │
│ --typ                    -t      [safe|rt]  the yaml parser mode.    │
│                                             [default: rt]            │
│ --no-explicit-start      -n                 disable explicit start.  │
│ --explicit-end           -e                 enable explicit end.     │
│ --no-quotes-preserved    -q                 don't preserve quotes.   │
│ --enforce-double-quotes  -E                 enforce double quotes    │
│                                             with -q.                 │
│ --default-flow-style     -f                 enable the default flow  │
│                                             style.                   │
│ --enforce-block-style    -B                 convert flow-style       │
│                                             (JSON-like) maps and     │
│                                             lists to block style.    │
│ --no-dash-inwards        -d                 dash at sequence level.  │
│ --spaces-before-comment  -c      INTEGER    spaces between comments  │
│                                             and content.             │
│ --align-comments         -a                 align EOL comments.      │
│ --line-width             -w      INTEGER    maximum line width.      │
│                                             [default: 2048]          │
│ --silent                 -S                 silent mode.             │
│ --summary                                   print a processing       │
│                                             summary.                 │
│ --version                -v                 show yamkix version      │
│ --help                   -h                 Show this message and    │
│                                             exit.                    │
╰──────────────────────────────────────────────────────────────────────╯
```

Run `yamkix --help` locally for the authoritative, full-width output.
