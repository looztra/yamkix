# Getting started with Yamkix

This tutorial walks you through installing `yamkix` and formatting your first YAML file. At the end, you will know how to run `yamkix` on a file and read its output.

## Step 1: Install yamkix

`Yamkix` is published on [pypi.org](https://pypi.org/project/yamkix/). Install it as a standalone tool with [uv](https://docs.astral.sh/uv/guides/tools/):

```shell
uv tool install yamkix
```

Check that it works:

```shell
yamkix --version
```

Other installation methods (like `mise`) are described in the [installation how-to guide](../how-to/install.md).

## Step 2: Create a YAML file to format

Create a file named `example.yml` with some inconsistently formatted YAML:

```yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name:   my-config
data:
  colors: [blue, green]
```

## Step 3: Format it

Run `yamkix` on the file:

```shell
yamkix example.yml
```

`yamkix` rewrites the file in place with its opinionated styling rules:

```yaml
---
apiVersion: v1
kind: ConfigMap
metadata:
  name: my-config
data:
  colors: [blue, green]
```

Notice what happened:

- An explicit document start marker (`---`) was added.
- The extra spaces after `name:` were normalized.
- Comments (if any) would be preserved, thanks to the default `rt` (round-trip) parsing mode.

## Step 4: Preview without overwriting

If you prefer to review the result before touching the file, send the output to `STDOUT`:

```shell
yamkix --input example.yml --stdout
```

## Where to go next

- Learn all the ways to feed files to yamkix in [Format files](../how-to/format-files.md).
- The flow-style list `[blue, green]` above was preserved as-is. yamkix can also convert JSON-style collections to block style — see [Convert flow style to block style](../how-to/enforce-block-style.md).
- Wire yamkix into your workflow with the [pre-commit hook](../how-to/pre-commit.md) or [editor integration](../how-to/editor-integration.md) guides.
- Understand the reasoning behind the default formatting in [Formatting rules](../explanation/formatting-rules.md).
