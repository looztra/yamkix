"""Provide integration tests that exercise the yamkix CLI as a real subprocess.

These tests invoke ``python -m yamkix`` in a real OS process with real pipes, which
is something the in-process Typer ``CliRunner`` used elsewhere cannot verify: that
stdout stays byte-clean (no stray debug prints), that stdin piping works, and that
the stderr config banner is printed normally but suppressed under ``--silent``.
"""

import subprocess
import sys
from pathlib import Path

import pytest


def run_yamkix(args: list[str], stdin: str | None = None) -> subprocess.CompletedProcess[str]:
    """Run ``python -m yamkix`` in a subprocess and capture its output.

    Args:
        args: Command-line arguments passed to yamkix.
        stdin: Optional text piped to the process' standard input.

    Returns:
        The completed process, with ``stdout`` and ``stderr`` captured as text.
    """
    return subprocess.run(  # noqa: S603
        [sys.executable, "-m", "yamkix", *args],
        input=stdin,
        capture_output=True,
        text=True,
        check=False,
    )


@pytest.mark.integration
class TestCliSubprocess:
    """Provide integration tests for the yamkix CLI run as a subprocess."""

    def test_stdout_is_not_polluted(self, datadir: Path) -> None:
        """Test that output to STDOUT is not polluted by stray debug print statements."""
        # GIVEN
        source = datadir / "no-start-no-end.yml"
        expected = datadir / "no-start-no-end--default.yml"

        # WHEN
        result = run_yamkix(["--input", str(source), "--output", "STDOUT"])

        # THEN
        assert result.returncode == 0
        assert result.stdout == expected.read_text()

    def test_stdin_default(self, datadir: Path) -> None:
        """Test reading from STDIN when --input is not specified."""
        # GIVEN
        source = datadir / "simple.yml"
        expected = datadir / "simple--default.yml"

        # WHEN
        result = run_yamkix([], stdin=source.read_text())

        # THEN
        assert result.returncode == 0
        assert result.stdout == expected.read_text()
        assert "input=STDIN" in result.stderr
        assert "output=STDOUT" in result.stderr

    def test_stdin_explicit_input(self, datadir: Path) -> None:
        """Test reading from STDIN when --input=STDIN is specified."""
        # GIVEN
        source = datadir / "simple.yml"
        expected = datadir / "simple--default.yml"

        # WHEN
        result = run_yamkix(["--input=STDIN"], stdin=source.read_text())

        # THEN
        assert result.returncode == 0
        assert result.stdout == expected.read_text()
        assert "input=STDIN" in result.stderr
        assert "output=STDOUT" in result.stderr

    def test_stdin_silent(self, datadir: Path) -> None:
        """Test that STDIN input in silent mode does not print the config banner to stderr."""
        # GIVEN
        source = datadir / "simple.yml"
        expected = datadir / "simple--default.yml"

        # WHEN
        result = run_yamkix(["--input=STDIN", "--silent"], stdin=source.read_text())

        # THEN
        assert result.returncode == 0
        assert result.stdout == expected.read_text()
        assert "input=STDIN" not in result.stderr
