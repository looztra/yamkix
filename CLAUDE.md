# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project

`yamkix` is an opinionated YAML formatter built on `ruamel.yaml`. It accepts YAML via file or stdin and writes formatted output in-place or to stdout.

## Commands

All commands assume the `uv`-managed virtualenv (`.venv`). Prefix with `uv run` or activate the venv first.

```bash
# Setup
uv sync                        # install/sync dependencies (same as make setup-venv)

# Tests
uv run poe test                # run all tests
uv run poe test:cov            # run tests with coverage (excludes integration)
uv run pytest tests/test_foo.py::test_bar  # run a single test
uv run pytest -m integration   # run only integration tests

# Lint & Format
uv run poe lint:all            # run all linters (ruff, ty, pylint, pyright) — run before submitting
uv run poe ruff:fmt:run        # format code
uv run poe ruff:lint:fix       # auto-fix ruff issues
```

## Architecture

The formatting pipeline flows: CLI → Config → Core → Output.

**`src/yamkix/_cli.py`** — Typer app; parses CLI args and delegates to `config.py` to build one or more `YamkixConfig` objects, then calls `round_trip_and_format()` for each.

**`src/yamkix/config.py`** — Two dataclasses: `YamkixConfig` (all formatting options) and `YamkixInputOutputConfig` (input/output file paths, `None` means stdin/stdout). `create_yamkix_config_from_typer_args()` is the main factory used by the CLI.

**`src/yamkix/yaml_writer.py`** — Configures a `ruamel.yaml` `YAML` instance with yamkix's opinionated indent settings (`mapping=2, sequence=4, offset=2`).

**`src/yamkix/yamkix.py`** — Core logic. `round_trip_and_format()` loads YAML, calls `yamkix_dump_all()`, and returns a `FileProcessingResult` indicating whether content changed. When `enforce_double_quotes=True` and `quotes_preserved=False`, a two-pass round-trip is used: first pass removes unnecessary quotes (converts to single); second pass re-parses with `preserve_quotes=True` and converts `SingleQuotedScalarString` → `DoubleQuotedScalarString`.

**`src/yamkix/comments.py`** — Monkey-patches `CommentedBase.yaml_add_eol_comment` to support configurable spacing before comments. `process_comments()` repositions EOL comments; `align_comments()` aligns them to the maximum column within each dict/list.

**`src/yamkix/helpers.py`** — Utility functions including `strip_leading_double_space` (used as ruamel.yaml `transform` for dash-inwards formatting) and `convert_single_to_double_quotes`.

## Code Conventions

- **Commits**: Conventional commits, **always with a scope** — e.g., `feat(cli): add flag`, `fix(comments): handle edge case`.
- **Docstrings**: Google style, required on all public modules, classes, and functions.
- **Strings**: f-strings for formatting; plain concatenation or `%` for log statements.
- **Ruff**: `ALL` rules selected, line length 119, target `py310`. See `ruff_defaults.toml` for ignores.
- **Tests**: Use `@pytest.fixture(name="foo")` explicit naming; parametrize with `pytest.param(..., id="...")`.
- **Type checking**: Both `pyright` and `ty` are enforced.
