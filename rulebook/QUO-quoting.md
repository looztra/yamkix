# QUO · Quoting
Whether yamkix keeps, removes or rewrites the quotes around string values. By default quotes are kept exactly as written; on request, unnecessary quotes are dropped and the remaining ones are made single, or double.

**Scope.** Read: `get_opinionated_yaml_writer` in `src/yamkix/yaml_writer.py`, the double-quote pass in `src/yamkix/yamkix.py` (`round_trip_and_format`, `yamkix_dump_all`), `convert_single_to_double_quotes` in `src/yamkix/helpers.py`, `raise_enforce_double_quotes_warning_if_needed` in `src/yamkix/config.py`, the quote cases of `tests/test_non_regression.py` and their fixtures, `tests/test_config.py`. Behaviour also observed by running the CLI on a sample file. Not read: how `ruamel.yaml` decides which strings need quotes.

## QUO-P01 · A quoted value keeps its type
- **Kind:** policy · **Nature:** YAML specification (an unquoted `123` or `true` is a number or a boolean, not a string)

**Statement.** Removing quotes must never turn a string into a number, a boolean or another type.

### QUO-R002 · Without quote preservation, only the quotes a value needs are kept, as single quotes
- **Kind:** rule · **Category:** calculation · **Implements:** QUO-P01
- **Status:** active · **Confidence:** verified · **Audit:** passed
- **Verified at:** 3825235 (2026-10-25)

**Rule.** With `--no-quotes-preserved`, quotes around plain strings are removed, and strings that would otherwise read as another type (such as `"1.722"` or `"true"`) are written with single quotes.

**Context.** The YAML library decides which values need quotes; yamkix only switches off the memory of the original quotes. Keys are handled the same way.

**Parameters.** `--no-quotes-preserved` / `-q` — src/yamkix/_cli.py:130-137 (off by default)

**Evidence.**
- enforcement — src/yamkix/yaml_writer.py:31 `get_opinionated_yaml_writer`
  `yaml.preserve_quotes = yamkix_config.quotes_preserved`
- test — tests/test_non_regression.py:229 `TestNonRegression::test_config`
  `assert filecmp.cmp(expected_output_file, actual_output_file, shallow=True)`

**Edge cases.**
- **QUO-R002.E1** Given the `no-start-no-end` file with `"some string with double-quote"`, `"1.722"` and `"true"`, when it is formatted with `--no-quotes-preserved`, then the first loses its quotes and the other two become `'1.722'` and `'true'`. — verified — tests/test_non_regression.py:51

**History.**
- 2026-10-25 · 3825235 · reanchored · lines shifted by the parser-mode, safe-mode warning and spacing fixes (uncommitted)
- 2026-10-24 · 823a0f3 · created

## Other operating rules

### QUO-R001 · Quotes are kept as written by default
- **Kind:** rule · **Category:** derivation
- **Status:** active · **Confidence:** verified · **Audit:** passed
- **Verified at:** 3825235 (2026-10-25)

**Rule.** By default, in round-trip mode, every quoted value and key keeps its quotes and their kind (single or double), and unquoted values stay unquoted.

**Context.** In safe mode the original quotes are not remembered, so the output behaves as with `--no-quotes-preserved` (E2).

**Evidence.**
- enforcement — src/yamkix/yaml_writer.py:31 `get_opinionated_yaml_writer`
  `yaml.preserve_quotes = yamkix_config.quotes_preserved`
- test — tests/test_non_regression.py:229 `TestNonRegression::test_config`
  `assert filecmp.cmp(expected_output_file, actual_output_file, shallow=True)`

**Edge cases.**
- **QUO-R001.E1** Given the `no-start-no-end` file with double-quoted, single-quoted and unquoted strings, when it is formatted with no option, then each keeps its quoting. — verified — tests/test_non_regression.py:34
- **QUO-R001.E2** Given `"k2": '123'` and `s: 'say "hi"'`, when they are formatted with `--typ safe`, then the output is `k2: '123'` and `s: say "hi"`. — read — src/yamkix/yaml_writer.py:27

**History.**
- 2026-10-25 · 3825235 · reanchored · lines shifted by the parser-mode, safe-mode warning and spacing fixes (uncommitted)
- 2026-10-24 · 823a0f3 · created

### QUO-R003 · `--enforce-double-quotes` turns the remaining single quotes into double quotes
- **Kind:** rule · **Category:** calculation
- **Status:** active · **Confidence:** verified · **Audit:** passed
- **Verified at:** 3825235 (2026-10-25)

**Rule.** With both `--no-quotes-preserved` and `--enforce-double-quotes` in round-trip mode, every value still quoted after quote removal is written with double quotes instead of single quotes, including list items.

**Context.** Done in a second pass on each document: dump it once without the original quotes, read the result back with quotes remembered, swap single-quoted values for double-quoted ones, then dump again. In safe mode the second read keeps no quote kind, so nothing is converted (E3) and a warning says so (QUO-R005).

**Parameters.** `--enforce-double-quotes` / `-E` — src/yamkix/_cli.py:138-146 (off by default)

**Evidence.**
- enforcement — src/yamkix/yamkix.py:118-120 `round_trip_and_format`
  `if yamkix_config.quotes_preserved is False and yamkix_config.enforce_double_quotes:`
- enforcement — src/yamkix/yamkix.py:216-221 `yamkix_dump_all`
- enforcement — src/yamkix/helpers.py:137-146 `convert_single_to_double_quotes`
  `return DoubleQuotedScalarString(str(obj))`
- test — tests/test_non_regression.py:229 `TestNonRegression::test_config`
  `assert filecmp.cmp(expected_output_file, actual_output_file, shallow=True)`

**Edge cases.**
- **QUO-R003.E1** Given the `no-start-no-end` file, when it is formatted with `--no-quotes-preserved --enforce-double-quotes`, then `"1.722"` and `"true"` stay double-quoted and plain strings lose their quotes. — verified — tests/test_non_regression.py:57
- **QUO-R003.E2** Given `quoted_in_flow: ['123', "456"]`, when it is formatted with `--no-quotes-preserved --enforce-double-quotes --enforce-block-style`, then both items are written `"123"` and `"456"`. — verified — tests/test_non_regression.py:183
- **QUO-R003.E3** Given `n: 'true'`, when it is formatted with `--typ safe --no-quotes-preserved --enforce-double-quotes`, then it stays `n: 'true'`. — read — src/yamkix/helpers.py:143
- **QUO-R003.E4** Given a quoted key such as `'123': a`, when it is formatted with `--no-quotes-preserved --enforce-double-quotes`, then the key stays single-quoted: only values and list items are converted. — read — src/yamkix/helpers.py:138-139

**Open questions.** Should quoted keys also be converted to double quotes?

**History.**
- 2026-10-25 · 3825235 · reanchored · safe mode now warns (QUO-R005), that open question resolved; lines shifted (uncommitted)
- 2026-10-25 · 01d0951 · reanchored · source lines shifted by the block scalar, comment and atomic write fixes
- 2026-10-24 · 823a0f3 · created

### QUO-R004 · `--enforce-double-quotes` alone has no effect and triggers a warning
- **Kind:** rule · **Category:** validation
- **Status:** active · **Confidence:** verified · **Audit:** passed
- **Verified at:** 3825235 (2026-10-25)

**Rule.** When `--enforce-double-quotes` is given without `--no-quotes-preserved`, in either parsing mode, quotes are kept as written and a warning says the option is useless; the run continues.

**Evidence.**
- enforcement — src/yamkix/config.py:316-323 `raise_enforce_double_quotes_warning_if_needed`
  `if no_quotes_preserved is False:`
- enforcement — src/yamkix/yamkix.py:118 `round_trip_and_format`
- test — tests/test_config.py:915-918 `TestRaiseEnforceDoubleQuotesWarning::test_warning_is_raised`
  `"WARNING: Option '--enforce-double-quotes' is useless unless '--no-quotes-preserved' is also set."`

**Edge cases.**
- **QUO-R004.E1** Given both options set in round-trip mode, when the configuration is built, then no warning is printed. — verified — tests/test_config.py:942

**History.**
- 2026-10-25 · 3825235 · reanchored · same behaviour, the condition is split into an early return and a branch; lines shifted (uncommitted)
- 2026-10-25 · 01d0951 · reanchored · source lines shifted by the block scalar, comment and atomic write fixes
- 2026-10-25 · dc86185 · reanchored · test lines shifted by added tests and imports (uncommitted)
- 2026-10-24 · 823a0f3 · created

### QUO-R005 · `--enforce-double-quotes` in safe mode has no effect and triggers a warning
- **Kind:** rule · **Category:** validation
- **Status:** candidate · **Confidence:** verified
- **Verified at:** 3825235 (2026-10-25)

**Rule.** With `--typ safe`, `--no-quotes-preserved` and `--enforce-double-quotes`, no value is converted to double quotes and a warning says the option has no effect with `--typ safe`; the run continues.

**Context.** The safe parser keeps no quote kind, so the second pass of QUO-R003 finds nothing to convert (QUO-R003.E3). Without `--no-quotes-preserved`, QUO-R004's warning is printed instead, never both.

**Evidence.**
- enforcement — src/yamkix/config.py:324-328 `raise_enforce_double_quotes_warning_if_needed`
  `"WARNING: Option '--enforce-double-quotes' has no effect with '--typ safe'."`
- test — tests/test_config.py:921-937 `TestRaiseEnforceDoubleQuotesWarning::test_warning_is_raised_in_safe_mode`
  `assert "WARNING: Option '--enforce-double-quotes' has no effect with '--typ safe'." in args[0]`

**Edge cases.**
- **QUO-R005.E1** Given `--typ safe --no-quotes-preserved` without `--enforce-double-quotes`, when the command runs, then no warning is printed. — verified — tests/test_config.py:945

**History.**
- 2026-10-25 · 3825235 · created · safe mode used to ignore the option silently (uncommitted)
