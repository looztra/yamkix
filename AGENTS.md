# Agent Instructions

This document provides context and instructions for AI agents working on this repository (`yamkix`).

## Project Overview

- **Repository**: [looztra/yamkix](https://github.com/looztra/yamkix)
- **Language**: Python (managed via `uv`)
- **Main Branch**: `main`

## Repository Structure

- `src/yamkix/` — package source: `_cli.py` (Typer app), `config.py` (`YamkixConfig`/`YamkixInputOutputConfig`), `yamkix.py` (core formatting), `yaml_writer.py` (ruamel.yaml setup), `comments.py` (comment handling), `helpers.py`, `errors.py`, `args.py`.
- `tests/` — unit tests (`test_*.py`) plus `tests/integration/` (marked `@pytest.mark.integration`, excluded from `poe test:cov`).
- `docs/` — mkdocs Diataxis site (`tutorials/`, `how-to/`, `reference/`, `explanation/`), published by `.github/workflows/publish_docs.yml`.
- `toolbox/mise/` and `toolbox/mk/` — shared `mise` task definitions and Makefile includes.
- `experiments/` — scratch/exploratory scripts, not part of the package or CI.

## Workflow & Standards

### Commit & Pull Requests

- **Conventional Commits**: ALWAYS use a scope. Format: `type(scope): description`.
  - Example: `feat(cli): add configurable line width`
  - Example: `fix(tests): resolve lint errors in tests`
- **Pull Requests**:
  - Title should match the commit format.
  - Link issues using `Fixes #<issue_number>`.
  - Provide a clear verification plan and results.

### Code Style & Quality

- **Markdown**: Follow GitHub's markdown instructions and `.markdownlint.yaml`.
- **Python**:
  - Follow PEP 8 & PEP 257.
  - **Docstrings**:
    - Use complete docstrings that follow the Google docstring style.
    - Modules must include a docstring and packages must have `__init__.py`.
  - **Strings**: Use f-strings for formatting (except when writing log statements).
  - **Imports**: Respect `import-outside-toplevel` (pylint) and `PLC0415` (ruff).
- **Tools**:
  - **Linting**: `ruff check` (or `poe ruff:lint`)
  - **Formatting**: `ruff format` (or `poe ruff:fmt:run`)
  - **Markdown Linting**: `pre-commit run --all-files markdownlint-cli2` or `poe lint:all` (if configured)
  - **Type Checking**: `pyright` & `ty`
- **Pre-check**: always run `poe lint:all` before submitting changes.

### Testing

- **Framework**: `pytest`
- **Location**: `tests/` (e.g., `tests/test_foo.py` for `foo.py`)
- **Conventions**:
  - Use `pytest.fixture` in `tests/conftest.py`.
  - Define fixtures using `@pytest.fixture(name="foo")` explicit naming.
  - Use `pytest.mark.parametrize` with `pytest.param(..., id="...")` for distinct test cases.
- **Running Tests**:
  - `pytest` (using `uv` environment)
  - `poe test`

## Task Runner (`poe`)

This project uses `poethepoet` for task management. Common tasks:

- `poe lint:all`: Run all linters (ruff, pyright, pylint, ty).
- `poe ruff:lint:fix`: Auto-fix ruff issues.
- `poe ruff:fmt:run`: Format code.
- `poe test`: Run tests.

## Specific Implementation Details

- **Configuration**: Managed in `src/yamkix/config.py`.
- **CLI**: Implemented using `typer` in `src/yamkix/_cli.py`.
- **YAML Handling**: Uses `ruamel.yaml` in `src/yamkix/yamkix.py` and `src/yamkix/yaml_writer.py`.

## CI/CD

- **`.github/workflows/code_checks.yml`**: pre-commit checks, Python lint+test (`mise run lint` / `mise run test`), distribution build check, mkdocs build check, integration tests, and release-please-driven publish to (Test)PyPI on release runs.
- **`.github/workflows/release_please.yml`**: drives `docs/changelog.md`, `version.txt`, and `.release-please-manifest.json` via conventional-commit history — never edit these by hand.
- **`.github/workflows/lint_pr_titles.yml`**: enforces conventional-commit PR titles (scope required, matching this file's commit convention).
- **`.github/workflows/codeql.yml`** and **`workflows_checks.yml`**: security/workflow linting (CodeQL, `zizmor`, `actionlint`).
- **Dependency updates**: `renovate.json5` covers Python/tool deps; `.github/dependabot.yml` covers GitHub Actions only (weekly).

## Adding a New CLI Flag

1. Add the `typer.Option` parameter to `main()` in `src/yamkix/_cli.py`.
2. Forward it as a kwarg to `create_yamkix_config_from_typer_args()` in `src/yamkix/config.py`.
3. Add/extend the corresponding field on `YamkixConfig` (or `YamkixInputOutputConfig` for I/O flags) in `config.py`.
4. Consume the field where formatting happens: `yaml_writer.py` (writer-level settings), `yamkix.py` (`round_trip_and_format`), or `comments.py` (comment behavior).
5. Add/extend tests in `tests/test_cli.py` (flag parsing) and `tests/test_config.py` (config construction).
6. Document the flag in `docs/reference/` and/or `docs/how-to/`.

## Common Pitfalls

- Don't hand-edit `version.txt` or `docs/changelog.md` — both are managed by `release-please`.
- `enforce_double_quotes` requires a two-pass round trip (see `yamkix.py`) — don't collapse it into a single pass.
- Integration tests are excluded from `poe test:cov` (`-m 'not integration'`); run them explicitly with `pytest -m integration` or `mise run test:integration`.
- `.python-version` (3.14) is the dev/CI runtime; `requires-python = ">=3.10"` and the trove classifiers (3.10–3.12) define supported runtimes — they are not the same thing.

## General Guidelines for Agents

1. **Read First**: Check `AGENTS.md` (this file) and `poe_tasks.toml` to understand available tools.
2. **Verify Often**: Run tests and linters frequently (e.g., after every significant edit).
3. **Be Explicit**: In PR descriptions and commit messages, explaining *why* a change was made is as important as *what* changed.
4. **Use `uv`**: Ensure you are using the `uv` managed environment (e.g., `.venv/bin/python` or `uv run`).
