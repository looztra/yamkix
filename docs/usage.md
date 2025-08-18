# How to use Yamkix

## Standalone

- Just use `yamkix` like any other CLI
- Check the available options with `yamkix --help` (and have a look at the [configuration](configuration.md) documentation)

### Formatting a **single** yaml file and control where to output the outcome

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

### Reading from STDIN

- You can format the input provide through `stdin`
- `stdin` input can be specified explicitly, using `--input STDIN`

    ```shell
    cat file.yml | yamkix --input STDIN
    ```

- `stdin` input is implicit if you don't specify any input through `-i/--input` or any CLI argument:

    ```shell
    cat file.yml | yamkix -q
    ````

- if `stdin` is used for input and nothing is specified for output, then `stdout` will be used for output.

### Formatting **multiple** files

- If you need to format multiple files in a single call to `Yamkix`, don't use `-i/--input`, just pass the list of files as arguments to the `yamkix` cli

    ```shell
    yamkix --silent path/to/file1.yml path/to/file2.yml
    ```

!!! Note
    It is not possible to output to `stdout` when formatting multiple files (feel free to [raise an issue](https://github.com/looztra/yamkix/issues) if you are interested in this feature).

## Pre-commit hook

- Since `v0.12.0`, you can now use `yamkix` as a pre-commit hook:

    ```yaml
    repos:
      - repo: https://github.com/looztra/yamkix
      rev: v0.12.0
      hooks:
        - id: yamkix
    ```

- you can pass options to `yamkix`through the `args` key:

    ```yaml
    repos:
      - repo: https://github.com/looztra/yamkix
      rev: v0.12.0
      hooks:
        - id: yamkix
          args: [--no-quotes-preserved]
    ```

- you can control which files will be parsed with the `exclude` key:

    ```yaml
    repos:
      - repo: https://github.com/looztra/yamkix
      rev: v0.12.0
      hooks:
        - id: yamkix
          args: [--no-quotes-preserved]
          exclude: |
            (?x)^(
                test-assets/.*|
                tests/data/.*
            )$
    ```

!!! Note
    `args` and `exclude` are related to the [pre-commit framework](https://pre-commit.com/#pre-commit-configyaml---hooks), **not** to yamkix.

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
