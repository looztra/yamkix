# Convert flow style to block style

This guide shows how to convert JSON-style (flow) collections to block style with the `-B/--enforce-block-style` option.

By default, `yamkix` preserves the style of your collections: a list written `[a, b, c]` stays that way. If you want everything expanded to block style, opt in with `--enforce-block-style`.

## Basic usage

With input `example.yml`:

```yaml
---
a_list: [a, b, c]
a_map: {first: yolo, second: foo}
```

run:

```shell
yamkix --enforce-block-style example.yml
```

and the file becomes:

```yaml
---
a_list:
  - a
  - b
  - c
a_map:
  first: yolo
  second: foo
```

## Nested collections

The conversion is recursive — flow collections are converted at any depth:

```yaml
---
nested:
  outer: {inner: [1, 2, {deep: true}]}
```

becomes:

```yaml
---
nested:
  outer:
    inner:
      - 1
      - 2
      - deep: true
```

## Empty collections

Empty collections stay in flow style because block style has no representation for them:

```yaml
---
empty_list: []
empty_map: {}
```

is left unchanged.

## Comments attached to flow collections

An end-of-line comment attached to a flow collection survives the conversion, but it is re-emitted at its original column on the key line:

```yaml
---
a_list: [a, b] # eol comment
```

becomes:

```yaml
---
a_list:        # eol comment
  - a
  - b
```

!!! tip "Combine with `--spaces-before-comment`"
    Add `--spaces-before-comment 1` to reattach comments cleanly:

    ```yaml
    ---
    a_list: # eol comment
      - a
      - b
    ```

## Interactions with other options

!!! warning "`--enforce-block-style` overrides `--default-flow-style`"
    If both options are set, block style wins for the whole document and a warning is printed to stderr.

- With `--typ safe`, the option is a no-op: the `safe` parsing mode does not preserve per-node styles, and its output is already block style.
- Works fine together with `--no-quotes-preserved` / `--enforce-double-quotes`.

To understand *why* flow-style collections are normally preserved and what this option changes under the hood, read [Flow style vs block style](../explanation/formatting-rules.md#flow-style-vs-block-style).
