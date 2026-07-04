# Control quotes

This guide shows how to control the quoting of scalars in the formatted output with `-q/--no-quotes-preserved` and `-E/--enforce-double-quotes`.

For guidance on *when* strings should be quoted at all, see [the explanation page](../explanation/formatting-rules.md#should-you-use-quotes-for-yaml-strings).

## Quotes preserved (default behavior)

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

## Quotes not preserved (using `-q/--no-quotes-preserved`)

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

## Quotes not preserved and enforcing double quotes (using `-q/--no-quotes-preserved` **and** `-E/--enforce-double-quotes`)

!!! info "For double quotes lovers"
    Starting with `v0.13.0`, there is an option, `--enforce-double-quotes`, to enforce the usage of double
    quotes when `-q` or `--no-quotes-preserved` is used.

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
        boolean_single_quotes: "true"
        boolean_double_quotes: "true"
        number_no_quotes: 1
        number_single_quotes: "1"
        number_double_quotes: "1"
    ```
