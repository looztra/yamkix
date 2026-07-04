# Format files

This guide shows the different ways to feed YAML content to `yamkix` and control where the formatted output goes.

Check the available options with `yamkix --help` (or see the [CLI options reference](../reference/cli.md)).

## Format a **single** yaml file and control where to output the outcome

- Use the `-i/--input` option to identify the source file
- If you don't specify any output option with `-o/--output` or `-s/--stdout` then the result will overwrite the source file

    ```shell
    yamkix --input path/to/yolo.yml
    # the formatted result will overwrite the content at path/to/yolo.yml
    ```

- You can specify the target file with `-o/--output`

    ```shell
    yamkix --input path/to/yolo.yml --output path/to/nice.yml
    # the formatted result will write the result at path/to/nice.yml
    # if nice.yml exists, it will be overwritten
    ```

- You can output the result to STDOUT using either `--output STDOUT` or `-s/--stdout`

    ```shell
    yamkix --input path/to/yolo.yml --stdout
    # output is written to STDOUT
    ---
    toto: foo
    titi:
      - bar
      - quix
    tutu:
      yolo: baz
    ```

- If you use `-s/--stdout` and `-i/--input`, specifying an output file with `-o/--output` will not be taken into account

    ```shell
    yamkix --input path/to/yolo.yml -output path/to/nice.yml --stdout
    # output is written to STDOUT
    ---
    toto: foo
    titi:
      - bar
      - quix
    tutu:
      yolo: baz
    ```

## Read from STDIN

- You can format the input provide through `stdin`
- `stdin` input can be specified explicitly, using `--input STDIN`

    ```shell
    cat file.yml | yamkix --input STDIN
    ```

- `stdin` input is implicit if you don't specify any input through `-i/--input` or any CLI argument:

    ```shell
    cat file.yml | yamkix -q
    ```

- if `stdin` is used for input and nothing is specified for output, then `stdout` will be used for output.

## Format **multiple** files

- If you need to format multiple files in a single call to `Yamkix`, don't use `-i/--input`, just pass the list of files as arguments to the `yamkix` cli

    ```shell
    yamkix --silent path/to/file1.yml path/to/file2.yml
    ```

!!! Note
    It is not possible to output to `stdout` when formatting multiple files (feel free to [raise an issue](https://github.com/looztra/yamkix/issues) if you are interested in this feature).

## Print a processing summary

- Use `--summary` to print processing statistics after all files have been processed
- The summary includes:
  - Total number of files processed
  - Number of files that encountered parse errors
  - Number of files with unchanged content (already properly formatted)
  - Total processing time

    ```shell
    yamkix --summary path/to/file1.yml path/to/file2.yml
    # Output:
    # [yamkix] Summary: 2 file(s) processed, 0 error(s), 1 unchanged, 0.042s
    ```

- When combined with `--silent` (which suppresses per-file config output), only the summary is printed to stderr:

    ```shell
    yamkix --silent --summary path/to/file1.yml path/to/file2.yml
    # Produces minimal output:
    # [yamkix] Summary: 2 file(s) processed, 0 error(s), 1 unchanged, 0.042s
    ```
