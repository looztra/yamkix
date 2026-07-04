# Formatting rules

This page explains the reasoning behind yamkix's opinionated defaults and the YAML concepts they rely on. For task-oriented instructions, see the [how-to guides](../how-to/format-files.md); for the exhaustive option list, see the [CLI options reference](../reference/cli.md).

## The opinionated defaults

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

These defaults exist because YAML has no single _out of the box_ canonical format: yamkix picks one and applies it consistently, while staying conservative about everything it does not have an opinion on (quotes, collection styles, comments).

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

See the [Control quotes](../how-to/control-quotes.md) guide for before/after examples.

### Should you use quotes for yaml strings?

!!! question "Should you use quotes for yaml strings?"

    If you are wondering if you should use quotes or not when writing yaml code, you can read this [awesome Stack Overflow thread](https://stackoverflow.com/questions/19109912/do-i-need-quotes-for-strings-in-yaml/69850618#69850618).

    Quoting the TLDR; section here:

    With that being said, according to the official YAML specification one should:

    - Whenever applicable use the unquoted style since it is the most readable.
    - Use the single-quoted style (') if characters such as " and \ are being used inside the string to avoid escaping them and therefore improve readability.
    - Use the double-quoted style (") when the first two options aren't sufficient, i.e. in scenarios where more complex line breaks are required or non-printable characters are needed.

## Flow style vs block style

YAML offers two ways to write collections:

- **Block style** uses indentation and one item per line — the style most people associate with YAML:

    ```yaml
    a_list:
      - a
      - b
    a_map:
      first: yolo
    ```

- **Flow style** uses explicit indicators — square brackets `[]` for sequences and curly braces `{}` for mappings — making YAML a superset of JSON:

    ```yaml
    a_list: [a, b]
    a_map: {first: yolo}
    ```

### Why `--default-flow-style` barely affects round-tripped content

In the default `rt` (round-trip) parsing mode, `ruamel.yaml` remembers the style of **each individual collection** it parsed, so it can re-emit your document as close to the input as possible. The writer-level `--default-flow-style` setting only applies to collections that don't carry that per-node memory (e.g. newly created ones) — which is why a flow-style map in your input stays flow style in the output, whatever the writer default says.

This per-node preservation is a feature (yamkix does not rewrite what you wrote), but it also means there was historically no way to *normalize* JSON-style collections to block style.

### Why `--enforce-block-style` exists

The `-B/--enforce-block-style` option ([issue #278](https://github.com/looztra/yamkix/issues/278)) fills that gap: it walks the parsed document and switches every collection's per-node style to block before dumping. Because the per-node style always wins over the writer default, this option also takes precedence over `--default-flow-style` (yamkix prints a warning if you combine them).

Two caveats worth understanding:

- **Empty collections stay flow style** (`[]` / `{}`): block style has no representation for an empty collection, so the emitter keeps the flow form.
- **Comments attached to flow collections** are re-emitted at their original column after the conversion, which can leave extra padding on the key line. Combining with `--spaces-before-comment` normalizes them — see the [how-to guide](../how-to/enforce-block-style.md#comments-attached-to-flow-collections).

## Output and Logging Options

- Use `--silent` to suppress the configuration information that is normally printed to stderr during processing
- Use `--summary` to print processing statistics (total files, errors, unchanged count, and elapsed time) after all files have been processed
- Both options can be combined: `--silent --summary` will only output the summary line without per-file configuration details
