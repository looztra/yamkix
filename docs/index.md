# Yamkix

`Yamkix` is an opinionated yaml file formatter. It reads YAML from a file or `STDIN` and writes it back nicely formatted, preserving comments.

## Why?

- Because I like my `yaml` file to be _nicely_ formatted and there is not _out of the box_ **default** format rules.
- Because
  <https://marketplace.visualstudio.com/items?itemName=redhat.vscode-yaml>
  does not add explicit start of documents and I don't like it this
  way
- Because I'm not a `js` / `typescript` dev so I don't want to go into a
  VSCode extension with client and server language

## Documentation

The documentation follows the [Diátaxis](https://diataxis.fr/) framework:

- **[Tutorials](tutorials/getting-started.md)** — start here if you are new: install yamkix and format your first file.
- **How-to guides** — task-oriented recipes:
  [install](how-to/install.md),
  [format files](how-to/format-files.md),
  [convert flow style to block style](how-to/enforce-block-style.md),
  [control quotes](how-to/control-quotes.md),
  [align comments](how-to/align-comments.md),
  [pre-commit hook](how-to/pre-commit.md),
  [editor integration](how-to/editor-integration.md).
- **Reference** — information-oriented descriptions:
  [CLI options](reference/cli.md),
  [public API](reference/api.md),
  [changelog](changelog.md).
- **Explanation** — understanding-oriented background:
  [formatting rules](explanation/formatting-rules.md),
  [ecosystem](explanation/ecosystem.md).

## Where does the name `yamkix` come from?

- Thanks to
  <http://online-generator.com/name-generator/product-name-generator.php>
  that suggested me `zamkix`. Just switched the starting `z` for the
  `y` of `yaml`
