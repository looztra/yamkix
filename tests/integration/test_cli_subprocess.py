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

    def test_line_width_output_has_no_trailing_spaces(self, datadir: Path) -> None:
        """Test that wrapped lines produced by --line-width carry no trailing spaces (issue #437)."""
        # GIVEN
        source = datadir / "issue-437.yml"
        expected = datadir / "issue-437--line-width-80.yml"

        # WHEN
        result = run_yamkix(["--input", str(source), "--output", "STDOUT", "--line-width", "80"])

        # THEN
        assert result.returncode == 0
        assert result.stdout == expected.read_text()
        assert not any(line.endswith(" ") for line in result.stdout.splitlines())

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

    def test_list_modified_reports_reformatted_files(self, tmp_path: Path) -> None:
        """Test that --list-modified prints one stderr line per reformatted file (issue #477)."""
        # GIVEN
        formatted = tmp_path / "formatted.yml"
        formatted.write_text("---\nkey: value\n")
        unformatted = tmp_path / "unformatted.yml"
        unformatted.write_text("---\nkey:   value\n")

        # WHEN
        result = run_yamkix(["--silent", "--list-modified", str(formatted), str(unformatted)])

        # THEN
        assert result.returncode == 0
        assert result.stderr.splitlines() == [f"[yamkix] Modified: {unformatted}"]
        assert unformatted.read_text() == "---\nkey: value\n"

    def test_list_modified_is_opt_in(self, tmp_path: Path) -> None:
        """Do not print modified-file reports without the option."""
        source = tmp_path / "source.yml"
        source.write_text("key:   value\n")

        result = run_yamkix(["--silent", str(source)])

        assert result.returncode == 0
        assert result.stderr == ""
        assert source.read_text() == "---\nkey: value\n"

    def test_list_modified_precedes_summary_and_excludes_parse_errors(self, tmp_path: Path) -> None:
        """List successful writes before summary, without listing malformed inputs."""
        changed = tmp_path / "changed.yml"
        changed.write_text("key:   value\n")
        invalid = tmp_path / "invalid.yml"
        invalid.write_text("key: [\n")

        result = run_yamkix(["--silent", "--list-modified", "--summary", str(changed), str(invalid)])

        assert result.returncode == 0
        lines = result.stderr.splitlines()
        assert [line for line in lines if line.startswith("[yamkix] Modified:")] == [f"[yamkix] Modified: {changed}"]
        assert "Summary: 2 file(s) processed, 1 error(s)" in lines[-1]
        assert changed.read_text() == "---\nkey: value\n"
        assert invalid.read_text() == "key: [\n"

    def test_list_modified_reports_stdin_destination(self, tmp_path: Path) -> None:
        """Name the written output rather than the STDIN source."""
        destination = tmp_path / "destination.yml"

        result = run_yamkix(["--silent", "--list-modified", "--output", str(destination)], stdin="---\nkey: value\n")

        assert result.returncode == 0
        assert result.stderr.splitlines() == [f"[yamkix] Modified: {destination}"]
        assert destination.read_text() == "---\nkey: value\n"

    def test_list_modified_reports_written_destination(self, tmp_path: Path) -> None:
        """Report a newly created output file even when its source was already formatted."""
        source = tmp_path / "source.yml"
        source.write_text("---\nkey: value\n")
        destination = tmp_path / "destination.yml"

        result = run_yamkix(["--silent", "--list-modified", "--input", str(source), "--output", str(destination)])

        assert result.returncode == 0
        assert result.stderr.splitlines() == [f"[yamkix] Modified: {destination}"]
        assert destination.read_text() == source.read_text()

    def test_list_modified_skips_identical_destination(self, tmp_path: Path) -> None:
        """Do not report an unchanged output file or its unformatted source."""
        source = tmp_path / "source.yml"
        source.write_text("key:   value\n")
        destination = tmp_path / "destination.yml"
        destination.write_text("---\nkey: value\n")

        result = run_yamkix(["--silent", "--list-modified", "--input", str(source), "--output", str(destination)])

        assert result.returncode == 0
        assert result.stderr == ""
        assert source.read_text() == "key:   value\n"
        assert destination.read_text() == "---\nkey: value\n"

    def test_list_modified_skips_stdout(self, tmp_path: Path) -> None:
        """Formatting to stdout must not claim the input file was changed."""
        source = tmp_path / "source.yml"
        source.write_text("key:   value\n")

        result = run_yamkix(["--silent", "--list-modified", "--input", str(source), "--stdout"])

        assert result.returncode == 0
        assert result.stderr == ""
        assert result.stdout == "---\nkey: value\n"
        assert source.read_text() == "key:   value\n"

    def test_list_modified_survives_later_failure(self, tmp_path: Path) -> None:
        """Report an earlier write when a later input cannot be opened."""
        source = tmp_path / "source.yml"
        source.write_text("key:   value\n")

        result = run_yamkix(["--silent", "--list-modified", str(source), str(tmp_path / "missing.yml")])

        assert result.returncode != 0
        assert source.read_text() == "---\nkey: value\n"
        assert f"[yamkix] Modified: {source}" in result.stderr.splitlines()

    @pytest.mark.skipif(sys.platform == "win32", reason="Windows filenames cannot contain newlines")
    def test_list_modified_escapes_newline_in_filename(self, tmp_path: Path) -> None:
        """A filename must not create a second apparent modified-file line."""
        source = tmp_path / "first\n[yamkix] Modified: spoof.yml"
        source.write_text("key:   value\n")

        result = run_yamkix(["--silent", "--list-modified", str(source)])

        escaped_name = str(source).replace("\n", r"\n")
        assert result.returncode == 0
        assert result.stderr.splitlines() == [f"[yamkix] Modified: {escaped_name}"]
        assert source.read_text() == "---\nkey: value\n"
