# Agent Instructions

This document provides context and instructions for AI agents working on this repository (`yamkix`).

## Project Overview

- **Repository**: [looztra/yamkix](https://github.com/looztra/yamkix)
- **Language**: Python (managed via `uv`)
- **Main Branch**: `main`

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
- **Python**: Follow PEP 8 & PEP 257.
- **Tools**:
  - **Linting**: `ruff check` (or `poe ruff:lint`)
  - **Formatting**: `ruff format` (or `poe ruff:fmt:run`)
  - **Type Checking**: `pyright` & `ty`
- **Pre-check**: always run `poe lint:all` before submitting changes.

### Testing
- **Framework**: `pytest`
- **Location**: `tests/` (e.g., `tests/test_foo.py` for `foo.py`)
- **Conventions**:
  - Use `pytest.fixture` in `tests/conftest.py`.
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

## General Guidelines for Agents

1.  **Read First**: Check `AGENTS.md` (this file) and `poe_tasks.toml` to understand available tools.
2.  **Verify Often**: Run tests and linters frequently (e.g., after every significant edit).
3.  **Be Explicit**: In PR descriptions and commit messages, explaining *why* a change was made is as important as *what* changed.
4.  **Use `uv`**: Ensure you are using the `uv` managed environment (e.g., `.venv/bin/python` or `uv run`).
