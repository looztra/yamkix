# Align end-of-line comments

This guide shows how to align EOL comments to a consistent column with the `-a/--align-comments` option.

When using `--typ rt` (round-trip mode, which is the default), yamkix preserves comments in your YAML files. By default, comments remain at their original position. However, you can enable comment alignment using the `-a/--align-comments` option.

## Aligning comments (using `-a/--align-comments`)

With input :

    ``` yaml
    ---
    sub_key1:
      a: 1 # comment 1
      b: asdf # comment 2
      c: 3.3333 # comment 3
    sub_key2:
      a: long text # comment 4
      b: an even longer text # comment 5
    ```

the output with `--align-comments` will be:

    ``` yaml
    ---
    sub_key1:
      a: 1      # comment 1
      b: asdf   # comment 2
      c: 3.3333 # comment 3
    sub_key2:
      a: long text           # comment 4
      b: an even longer text # comment 5
    ```

The alignment works by:

- Finding the longest value in each dict/list
- Positioning all EOL comments in that container to align with the longest value
- Processing nested structures recursively

This feature is useful when you want consistent visual alignment of comments in your YAML files, making them more readable.
