# Use yamkix as a pre-commit hook

This guide shows how to run `yamkix` automatically on your YAML files with the [pre-commit framework](https://pre-commit.com/).

- Since `v0.12.0`, you can use `yamkix` as a pre-commit hook:

    ```yaml
    repos:
      - repo: https://github.com/looztra/yamkix
      rev: v1.0.0
      hooks:
        - id: yamkix
    ```

- you can pass options to `yamkix`through the `args` key:

    ```yaml
    repos:
      - repo: https://github.com/looztra/yamkix
      rev: v1.0.0
      hooks:
        - id: yamkix
          args: [--no-quotes-preserved, --silent]
    ```

- you can control which files will be parsed with the `exclude` key:

    ```yaml
    repos:
      - repo: https://github.com/looztra/yamkix
      rev: v1.0.0
      hooks:
        - id: yamkix
          args: [--no-quotes-preserved, --silent]
          exclude: |
            (?x)^(
                test-assets/.*|
                tests/data/.*
            )$
    ```

!!! Note
    `args` and `exclude` are related to the [pre-commit framework](https://pre-commit.com/#pre-commit-configyaml---hooks), **not** to yamkix.
