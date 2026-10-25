# FIL · Files and runs
Which files yamkix reads and overwrites, what happens when one of them cannot be processed, and what yamkix reports about a run (configuration line, modified files, summary).

**Scope.** Read: `main` in `src/yamkix/_cli.py`, `round_trip_and_format` and the file handling of `yamkix_dump_all` in `src/yamkix/yamkix.py`, the input/output parts of `src/yamkix/config.py` (`create_yamkix_config_from_typer_args`, `get_input_output_config_from_args`, `raise_input_output_warning_if_needed`, `YamkixInputOutputConfig`), `tests/test_cli.py`, `tests/test_config.py`, `tests/test_yamkix.py`. Behaviour also observed by running the CLI on sample files. Not read: Typer's own argument parsing, the integration tests under `tests/integration/`. Validation of `--typ` belongs to OPT.

## FIL-P01 · A file the user cannot recover is never damaged on purpose
- **Kind:** policy · **Nature:** product decision (an in-place formatter must not destroy the files it is given)

**Statement.** A file that cannot be formatted must be left as it was.

### FIL-R008 · A file with a YAML syntax error is reported, left untouched, and the run goes on
- **Kind:** rule · **Category:** validation · **Implements:** FIL-P01
- **Status:** active · **Confidence:** verified · **Audit:** passed
- **Verified at:** 01d0951 (2026-10-25)

**Rule.** When a file has a YAML syntax error (scanner or parser error), yamkix prints an error naming it, does not write its output, counts it as an error, goes on with the next file, and still ends with exit code 0.

**Context.** The whole input is parsed before the output is opened, so a syntax error can never truncate the file. Other invalid YAML, such as a duplicate key or an undefined alias, is not caught here and stops the run (FIL-R009).

**Evidence.**
- enforcement — src/yamkix/yamkix.py:133-138 `round_trip_and_format`
  `raise InvalidYamlContentError from parsing_error`
- enforcement — src/yamkix/_cli.py:275-284 `main`
- test — tests/test_cli.py:403-408 `TestCli::test_list_modified_precedes_summary_and_excludes_parse_errors`
  `assert invalid.read_text() == "key: [\n"`

**Edge cases.**
- **FIL-R008.E1** Given a changed file and a file containing `key: [`, when both are formatted with `--list-modified --summary`, then the first is rewritten and listed, the second keeps `key: [`, the summary says `2 file(s) processed, 1 error(s)` and the exit code is 0. — verified — tests/test_cli.py:403
- **FIL-R008.E2** Given a file with a duplicate key (`a: 1` then `a: 2`) followed by a valid file, when both are formatted, then the run stops with a traceback and the second file is not formatted. — verified — tests/test_cli.py:487

**Open questions.** Should a malformed file make the run exit with a non-zero code, so CI and pre-commit hooks fail on it?

**History.**
- 2026-10-25 · 01d0951 · reanchored · source lines shifted by the block scalar, comment and atomic write fixes
- 2026-10-25 · dc86185 · changed · E2 read → verified, CLI test added (uncommitted)
- 2026-10-24 · 823a0f3 · created

### FIL-R010 · An output file is replaced only once its new content is fully written
- **Kind:** rule · **Category:** state-transition · **Implements:** FIL-P01
- **Status:** changed · **Confidence:** verified · **Audit:** passed
- **Verified at:** 01d0951 (2026-10-25)

**Rule.** Once every document is formatted, the output is written to a temporary file next to the destination, flushed to disk, then moved over the destination; if anything fails before the move, the destination keeps its previous content and the temporary file is removed. Symlinks are followed and permission bits are kept; special files such as `/dev/null` or a FIFO are written directly.

**Context.** Standard output is still written document by document. The destination directory must be writable, the replaced file belongs to the user running yamkix, and hard links are not preserved.

**Evidence.**
- enforcement — src/yamkix/yamkix.py:71-100 `_write_output_file`
  `temporary.replace(target)`
- enforcement — src/yamkix/yamkix.py:207-208 `yamkix_dump_all`
  `rendered = StringIO()`
- enforcement — src/yamkix/yamkix.py:254-258 `yamkix_dump_all`
  `_write_output_file(Path(output_file), content)`
- test — tests/test_cli.py:608-611 `TestCli::test_failed_write_leaves_file_untouched_and_unlisted`
  `assert source.read_text() == original`

**Edge cases.**
- **FIL-R010.E1** Given a file whose write fails with "no space left on device", when it is formatted in place, then it keeps its previous content and no temporary file is left. — verified — tests/test_cli.py:610
- **FIL-R010.E2** Given an existing output file with mode `0640`, when it is rewritten, then it keeps mode `0640`. — verified — tests/test_yamkix.py:398
- **FIL-R010.E3** Given an output path that is a symlink, when it is rewritten, then it stays a symlink and its target receives the content. — verified — tests/test_yamkix.py:418

**Open questions.** Should the owner and the hard links of a replaced file be preserved?

**History.**
- 2026-10-25 · 01d0951 · changed · emptied then appended → written to a temporary file and moved into place; E1 read → verified, E2 and E3 added
- 2026-10-24 · 823a0f3 · created

## Other operating rules

### FIL-R001 · Input is a file, or STDIN when none is given
- **Kind:** rule · **Category:** derivation
- **Status:** active · **Confidence:** verified · **Audit:** passed
- **Verified at:** dc86185 (2026-10-25)

**Rule.** Without files as arguments, yamkix reads the file given with `--input`, or standard input when `--input` is absent or is `STDIN` in any letter case.

**Evidence.**
- enforcement — src/yamkix/config.py:391 `create_yamkix_config_from_typer_args`
  `f_input = None if (input_file is None or input_file.lower() == STDIN_DISPLAY_NAME.lower()) else input_file`
- test — tests/test_config.py:726-727 `TestCreateYamkixConfigFromTyperArgs::test_create_yamkix_config_io_logic_with_explicit_stdin_as_input`
  `assert configs[0].io_config.input is None`

**Edge cases.**
- **FIL-R001.E1** Given `--input StDin`, when the configuration is built, then input is read from STDIN. — verified — tests/test_config.py:726

**History.**
- 2026-10-25 · dc86185 · reanchored · test lines shifted by added tests and imports (uncommitted)
- 2026-10-24 · 823a0f3 · created

### FIL-R002 · A file given with `--input` is formatted in place by default
- **Kind:** rule · **Category:** derivation
- **Status:** active · **Confidence:** verified · **Audit:** passed
- **Verified at:** dc86185 (2026-10-25)

**Rule.** When an input file is given and neither `--output` nor `--stdout` is, the formatted result overwrites the input file.

**Evidence.**
- enforcement — src/yamkix/config.py:403-404 `create_yamkix_config_from_typer_args`
  `f_output = f_input`
- test — tests/test_config.py:652-653 `TestCreateYamkixConfigFromTyperArgs::test_create_yamkix_config_io_logic_with_input_file`
  `assert configs[0].io_config.output == "input.yaml"`

**History.**
- 2026-10-25 · dc86185 · reanchored · test lines shifted by added tests and imports (uncommitted)
- 2026-10-24 · 823a0f3 · created

### FIL-R003 · Reading from STDIN writes to STDOUT unless an output file is given
- **Kind:** rule · **Category:** derivation
- **Status:** active · **Confidence:** verified · **Audit:** passed
- **Verified at:** dc86185 (2026-10-25)

**Rule.** When input comes from STDIN, the result goes to standard output, unless `--output` names a file, in which case that file is written.

**Evidence.**
- enforcement — src/yamkix/config.py:399-402 `create_yamkix_config_from_typer_args`
  `output_file is None and f_input is None`
- test — tests/test_config.py:696-697 `TestCreateYamkixConfigFromTyperArgs::test_create_yamkix_config_io_logic_with_input_none_and_output_none`
  `assert configs[0].io_config.output is None`
- test — tests/test_config.py:674-675 `TestCreateYamkixConfigFromTyperArgs::test_create_yamkix_config_io_logic_with_output_file`
  `assert configs[0].io_config.output == "output.yaml"`

**History.**
- 2026-10-25 · dc86185 · reanchored · test lines shifted by added tests and imports (uncommitted)
- 2026-10-24 · 823a0f3 · created

### FIL-R004 · `--stdout` sends the result to standard output whatever `--output` says
- **Kind:** rule · **Category:** derivation
- **Status:** active · **Confidence:** verified · **Audit:** passed
- **Verified at:** dc86185 (2026-10-25)

**Rule.** With `--stdout`, the result is written to standard output even when `--output` names a file, and the input file is not modified.

**Evidence.**
- enforcement — src/yamkix/config.py:393-394 `create_yamkix_config_from_typer_args`
  `if stdout:`
- test — tests/test_config.py:575 `TestCreateYamkixConfigFromTyperArgs::test_create_yamkix_config_stdout_override`
  `assert configs[0].io_config.output is None  # Should be None due to stdout=True`
- test — tests/test_cli.py:461-462 `TestCli::test_list_modified_skips_stdout`
  `assert source.read_text() == "key:   value\n"`

**History.**
- 2026-10-25 · dc86185 · reanchored · test lines shifted by added tests and imports (uncommitted)
- 2026-10-24 · 823a0f3 · created

### FIL-R005 · `--output STDOUT` in any letter case means standard output
- **Kind:** rule · **Category:** derivation
- **Status:** active · **Confidence:** verified · **Audit:** passed
- **Verified at:** dc86185 (2026-10-25)

**Rule.** An `--output` value equal to `STDOUT`, in any letter case, sends the result to standard output instead of creating a file of that name.

**Context.** As a consequence, a file literally named `stdout` cannot be written with `--output`.

**Evidence.**
- enforcement — src/yamkix/config.py:396-402 `create_yamkix_config_from_typer_args`
  `elif output_file is not None and output_file.lower() != STDOUT_DISPLAY_NAME.lower():`
- test — tests/test_config.py:756-757 `TestCreateYamkixConfigFromTyperArgs::test_create_yamkix_config_io_logic_with_explicit_stdout_as_output`
  `assert configs[0].io_config.output is None`

**Edge cases.**
- **FIL-R005.E1** Given `--input input.yaml --output StDout`, when the configuration is built, then the output is standard output. — verified — tests/test_config.py:756

**History.**
- 2026-10-25 · dc86185 · reanchored · test lines shifted by added tests and imports (uncommitted)
- 2026-10-24 · 823a0f3 · created

### FIL-R006 · Files passed as arguments are each formatted in place, ignoring `-i`, `-o` and `-s`
- **Kind:** rule · **Category:** derivation
- **Status:** active · **Confidence:** verified · **Audit:** passed
- **Verified at:** dc86185 (2026-10-25)

**Rule.** When files are given as arguments, each one is formatted in place in the given order; `--input`, `--output` and `--stdout` are then ignored, with a warning when any of them was given.

**Evidence.**
- enforcement — src/yamkix/config.py:378-389 `create_yamkix_config_from_typer_args`
  `if files is not None:`
- enforcement — src/yamkix/config.py:339 `raise_input_output_warning_if_needed`
  `if files is not None and (input_file is not None or output_file is not None or stdout):`
- test — tests/test_config.py:802-806 `TestCreateYamkixConfigFromTyperArgs::test_create_yamkix_config_io_logic_with_two_arguments`
  `assert configs[1].io_config.output == str(test_file2)`
- test — tests/test_config.py:1019-1025 `TestRaiseInputOutputWarningIfNeeded::test_warning_is_raised`
  `assert "not honored" in args[0]`

**Edge cases.**
- **FIL-R006.E1** Given `--input a.yml b.yml`, when yamkix runs, then a warning is printed, `b.yml` is formatted in place and `a.yml` is not touched. — read — src/yamkix/config.py:378

**History.**
- 2026-10-25 · dc86185 · reanchored · test lines shifted by added tests and imports (uncommitted)
- 2026-10-24 · 823a0f3 · created

### FIL-R007 · The legacy argparse path resolves input and output the same way, but case-sensitively
- **Kind:** rule · **Category:** derivation
- **Status:** retired · **Confidence:** verified · **Audit:** passed
- **Verified at:** 823a0f3 (2026-10-24)

**Rule.** For tools that build yamkix options with argparse (such as kubesplit), input is STDIN when absent or exactly `STDIN`; output is standard output with `stdout` set, when output is exactly `STDOUT`, or when input is STDIN and no output is given; otherwise the named output, or the input file itself.

**Context.** Same precedence as FIL-R001 to FIL-R005, but `stdin` or `Stdout` in lower or mixed case are taken as file names here. Retired: nothing in this repository calls this path outside tests, and kubesplit 0.5.0, its former user, no longer imports it; it is dead code.

**Evidence.**
- enforcement — src/yamkix/config.py:251-261 `get_input_output_config_from_args`
  `f_input = None if (args.input is None or args.input == STDIN_DISPLAY_NAME) else args.input`
- test — tests/test_config.py:54-56 `TestYamkixInputOutputConfig::test_get_io_config_when_file_input_provided`
  `assert sut.output == f_input`
- test — tests/test_config.py:122-124 `TestYamkixInputOutputConfig::test_get_io_config_when_file_input_and_output_provided_and_stdout`
  `assert sut.output is None`

**Edge cases.**
- **FIL-R007.E1** Given `input = "stdin"` (lower case) on the argparse path, when the configuration is built, then a file named `stdin` is read. — read — src/yamkix/config.py:251

**Open questions.** Should the argparse path accept `STDIN` and `STDOUT` in any case, like the CLI?

**History.**
- 2026-10-24 · 823a0f3 · retired · dead code, no caller left (kubesplit 0.5.0 uses get_yamkix_config_from_default)
- 2026-10-24 · 823a0f3 · created

### FIL-R009 · Any other failure stops the whole run
- **Kind:** rule · **Category:** validation
- **Status:** active · **Confidence:** verified · **Audit:** passed
- **Verified at:** 01d0951 (2026-10-25)

**Rule.** A failure other than malformed YAML (missing file, unreadable file, write error) stops the run immediately with a non-zero exit code and a traceback; the following files are not processed and no summary is printed.

**Evidence.**
- enforcement — src/yamkix/_cli.py:269-284 `main`
  `except InvalidYamlContentError as e:`
- test — tests/test_cli.py:471-473 `TestCli::test_list_modified_survives_later_failure`
  `assert result.exit_code != 0`

**Edge cases.**
- **FIL-R009.E1** Given `a.yml missing.yml b.yml`, when they are formatted with `--summary`, then `a.yml` is rewritten, the run fails on `missing.yml`, `b.yml` is left unformatted and no summary is printed. — verified — tests/test_cli.py:502

**Open questions.** Should a missing file be reported like a malformed one and the run continue with the other files?

**History.**
- 2026-10-25 · 01d0951 · reanchored · only malformed YAML is caught; the explicit re-raise was removed
- 2026-10-25 · dc86185 · changed · E1 read → verified, CLI test added (uncommitted)
- 2026-10-24 · 823a0f3 · created

### FIL-R011 · A file is "unchanged" only if the output bytes equal the input bytes
- **Kind:** rule · **Category:** derivation
- **Status:** active · **Confidence:** verified · **Audit:** passed
- **Verified at:** 01d0951 (2026-10-25)

**Rule.** A file counts as unchanged in the summary only when the bytes yamkix would write, with the platform's line endings, are identical to the input bytes; for STDIN the text is compared.

**Context.** Output is written with the platform line separator, so on Linux a CRLF file is always rewritten and never counts as unchanged.

**Evidence.**
- enforcement — src/yamkix/yamkix.py:168-169 `round_trip_and_format`
  `unchanged = written_bytes == input_bytes if input_file is not None else formatted == raw_input`
- test — tests/test_yamkix.py:153 `TestRoundTripAndFormat::test_crlf_input_is_not_unchanged`
  `assert result.unchanged is False`
- test — tests/test_yamkix.py:93 `TestRoundTripAndFormat::test_returns_unchanged_true_when_content_not_modified`
  `assert result.unchanged is True`
- test — tests/test_cli.py:569-571 `TestCli::test_list_modified_and_summary_agree_on_crlf`
  `assert "0 unchanged" in result.stderr`

**Edge cases.**
- **FIL-R011.E1** Given `---\r\nkey: value\r\n`, when it is formatted in place, then it is rewritten as `---\nkey: value\n` and not counted as unchanged. — verified — tests/test_cli.py:569

**History.**
- 2026-10-25 · 01d0951 · reanchored · source lines shifted by the block scalar, comment and atomic write fixes
- 2026-10-25 · dc86185 · reanchored · test lines shifted; positive unchanged case now asserted, open question resolved (uncommitted)
- 2026-10-24 · e9e0cca · reanchored · test moved to tests/test_yamkix.py:152 after tests were added above it
- 2026-10-24 · 823a0f3 · created

### FIL-R012 · An output counts as modified when it is created or its bytes change
- **Kind:** rule · **Category:** derivation
- **Status:** active · **Confidence:** verified · **Audit:** passed
- **Verified at:** 01d0951 (2026-10-25)

**Rule.** An output file counts as modified when it did not exist, when its new bytes differ from its previous bytes, or when its previous content could not be read; standard output and special files such as `/dev/null` never count.

**Evidence.**
- enforcement — src/yamkix/yamkix.py:141-152 `round_trip_and_format`
  `track_output = output_file is not None and not _is_special_file(Path(output_file))`
- enforcement — src/yamkix/yamkix.py:171 `round_trip_and_format`
  `output_changed = track_output and (not previous_output_readable or written_bytes != previous_output)`
- test — tests/test_yamkix.py:138 `TestRoundTripAndFormat::test_output_changed_for_separate_destination`
  `assert result.output_changed is expected_changed`

**Edge cases.**
- **FIL-R012.E1** Given an already formatted destination identical to the result, when an unformatted source is formatted into it, then it is not reported. — verified — tests/test_cli.py:447-448
- **FIL-R012.E2** Given an output of `/dev/null`, when a file is formatted with `--list-modified`, then nothing is reported. — verified — tests/test_cli.py:537-538
- **FIL-R012.E3** Given a destination that cannot be read before writing, when a file is formatted into it, then it is reported as modified. — verified — tests/test_cli.py:559-560
- **FIL-R012.E4** Given an output on standard output, when a file is formatted, then nothing is reported. — verified — tests/test_yamkix.py:167

**History.**
- 2026-10-25 · 01d0951 · reanchored · source lines shifted by the block scalar, comment and atomic write fixes
- 2026-10-25 · dc86185 · reanchored · test lines shifted by added tests and imports (uncommitted)
- 2026-10-24 · e9e0cca · reanchored · tests moved to tests/test_yamkix.py:137 and :166 after tests were added above them
- 2026-10-24 · 823a0f3 · created

### FIL-R013 · `--list-modified` prints one line per modified output, even when the run fails
- **Kind:** rule · **Category:** derivation
- **Status:** changed · **Confidence:** verified · **Audit:** passed
- **Verified at:** 01d0951 (2026-10-25)

**Rule.** With `--list-modified`, after processing (and before the summary), yamkix prints `[yamkix] Modified: <output name>` to standard error for each modified output (FIL-R012); names that are not printable or start with `"` are quoted with escapes.

**Context.** Printing happens in a `finally` block, so files rewritten before a fatal error are still listed. Malformed inputs are never listed because their output was not written, and an output whose write failed keeps its previous content (FIL-R010), so it is not listed either.

**Parameters.** `--list-modified` — src/yamkix/_cli.py:220-226 (off by default)

**Evidence.**
- enforcement — src/yamkix/_cli.py:273-274 `main`
  `if list_modified_mode and result.output_changed:`
- enforcement — src/yamkix/_cli.py:285-294 `main`
- enforcement — src/yamkix/_cli.py:59-64 `_format_report_name`
  `if name.isprintable() and not name.startswith('"'):`
- test — tests/test_cli.py:419 `TestCli::test_list_modified_reports_stdin_destination`
  `assert result.stderr.splitlines() == [f"[yamkix] Modified: {destination}"]`

**Edge cases.**
- **FIL-R013.E1** Given a file and a missing file, when both are formatted with `--list-modified`, then the run fails and the first file is still listed. — verified — tests/test_cli.py:473
- **FIL-R013.E2** Given a file whose name contains a line break, when it is listed, then its name is printed quoted with `\n` escaped. — verified — tests/test_cli.py:515
- **FIL-R013.E3** Given the option is not set, when a file is rewritten, then nothing is printed to standard error. — verified — tests/test_cli.py:391
- **FIL-R013.E4** Given a file whose write fails, when it is formatted with `--list-modified`, then it is not listed. — verified — tests/test_cli.py:609

**History.**
- 2026-10-25 · 01d0951 · changed · outputs whose write failed are no longer listed (atomic write); E4 added
- 2026-10-25 · dc86185 · reanchored · test lines shifted by added tests and imports (uncommitted)
- 2026-10-24 · 823a0f3 · created

### FIL-R014 · `--summary` prints the counts of files, errors and unchanged files
- **Kind:** rule · **Category:** calculation
- **Status:** active · **Confidence:** verified · **Audit:** passed
- **Verified at:** 01d0951 (2026-10-25)

**Rule.** With `--summary`, once all files are processed, yamkix prints to standard error the number of files processed, of malformed files, of unchanged files, and the elapsed time in seconds with 3 decimals.

**Context.** Not printed when the run stops on a fatal error (FIL-R009).

**Parameters.** `--summary` — src/yamkix/_cli.py:213-219 (off by default)

**Evidence.**
- enforcement — src/yamkix/_cli.py:295-304 `main`
  `f"[yamkix] Summary: {total} file(s) processed, {errors} error(s), {unchanged} unchanged, {elapsed:.3f}s"`
- test — tests/test_cli.py:379-381 `TestCli::test_summary_mode_counts_errors_and_unchanged`
  `assert "1 error(s)" in summary_text`

**History.**
- 2026-10-25 · 01d0951 · reanchored · source lines shifted by the block scalar, comment and atomic write fixes
- 2026-10-25 · dc86185 · reanchored · test lines shifted by added tests and imports (uncommitted)
- 2026-10-24 · 823a0f3 · created

### FIL-R015 · The configuration of each file is printed unless `--silent`
- **Kind:** rule · **Category:** derivation
- **Status:** active · **Confidence:** verified · **Audit:** passed
- **Verified at:** dc86185 (2026-10-25)

**Rule.** Before processing each file, yamkix prints its input, output and formatting options to standard error, unless `--silent` is given.

**Parameters.** `--silent` / `-S` — src/yamkix/_cli.py:205-212 (off by default)

**Evidence.**
- enforcement — src/yamkix/_cli.py:267-268 `main`
  `if not silent_mode:`
- test — tests/test_cli.py:199 `TestCli::test_silent_mode`
  `mock_print_config.assert_not_called()`

**History.**
- 2026-10-25 · dc86185 · reanchored · test lines shifted by added tests and imports (uncommitted)
- 2026-10-24 · 823a0f3 · created
