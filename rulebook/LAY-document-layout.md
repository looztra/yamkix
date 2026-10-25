# LAY · Document layout
How yamkix lays out every YAML document it writes: the start and end markers, how lists are indented, whether collections are written in flow (JSON-like) or block style, where long lines are folded, and the clean-up of trailing spaces. These are the house-style choices of the formatter; they are meant not to change the data a document holds (see LAY-R010.E3 for one exception).

**Scope.** Read: `src/yamkix/yaml_writer.py`, the layout parts of `src/yamkix/yamkix.py` (`yamkix_dump_all`, `yamkix_dump_one`), the layout helpers of `src/yamkix/helpers.py` (`strip_*`, `convert_flow_to_block_style`), `DEFAULT_LINE_WIDTH` in `src/yamkix/config.py`, `tests/test_yaml_writer.py`, `tests/test_helpers.py`, the layout cases of `tests/test_non_regression.py` and their fixtures. Behaviour also observed by running the CLI on sample files. Not read: how `ruamel.yaml` itself indents, folds and chooses styles. Quote handling (helpers `convert_single_to_double_quotes`) belongs to QUO; the malformed-YAML refusal in `yamkix.py` belongs to FIL.

## Other operating rules

### LAY-R001 · Every document starts with `---` unless disabled
- **Kind:** rule · **Category:** derivation
- **Status:** active · **Confidence:** verified · **Audit:** passed
- **Verified at:** 823a0f3 (2026-10-24)

**Rule.** Each output document begins with the explicit start marker `---`, whether or not the input had one; with `--no-explicit-start` no marker is written.

**Parameters.** `--no-explicit-start` / `-n` — src/yamkix/_cli.py:113-120 (marker on by default)

**Evidence.**
- enforcement — src/yamkix/yaml_writer.py:28 `get_opinionated_yaml_writer`
  `yaml.explicit_start = yamkix_config.explicit_start`
- test — tests/test_non_regression.py:235 `TestNonRegression::test_config`
  `assert filecmp.cmp(expected_output_file, actual_output_file, shallow=True)`

**Edge cases.**
- **LAY-R001.E1** Given the `no-start-no-end` file without a `---` marker, when it is formatted with no option, then the output starts with `---`. — verified — tests/test_non_regression.py:34
- **LAY-R001.E2** Given the same file, when it is formatted with `--no-explicit-start`, then the output has no `---` marker. — verified — tests/test_non_regression.py:39

**History.**
- 2026-10-24 · 823a0f3 · created

### LAY-R002 · Documents end with `...` only on request
- **Kind:** rule · **Category:** derivation
- **Status:** active · **Confidence:** verified · **Audit:** passed
- **Verified at:** 823a0f3 (2026-10-24)

**Rule.** No explicit end marker is written by default; with `--explicit-end` each document ends with `...`.

**Parameters.** `--explicit-end` / `-e` — src/yamkix/_cli.py:121-128 (off by default)

**Evidence.**
- enforcement — src/yamkix/yaml_writer.py:29 `get_opinionated_yaml_writer`
  `yaml.explicit_end = yamkix_config.explicit_end`
- test — tests/test_non_regression.py:235 `TestNonRegression::test_config`
  `assert filecmp.cmp(expected_output_file, actual_output_file, shallow=True)`

**Edge cases.**
- **LAY-R002.E1** Given the `no-start-no-end` file, when it is formatted with `--explicit-end`, then the output ends with a `...` line. — verified — tests/test_non_regression.py:45

**History.**
- 2026-10-24 · 823a0f3 · created

### LAY-R003 · List dashes are pushed inwards by default
- **Kind:** rule · **Category:** calculation
- **Status:** active · **Confidence:** verified · **Audit:** passed
- **Verified at:** 823a0f3 (2026-10-24)

**Rule.** By default, the items of a list nested under a key are indented by 2 spaces, the dash sits 2 spaces in from the key, and the item content 4 spaces in; nested maps are indented by 2 spaces.

**Context.** This is yamkix's main opinion and matches what `yamllint` expects by default. The three values are fixed in the code and cannot be changed by an option.

**Parameters.** `OPINIONATED_MAPPING_VALUE = 2` — src/yamkix/yaml_writer.py:7; `OPINIONATED_SEQUENCE_VALUE = 4` — src/yamkix/yaml_writer.py:8; `OPINIONATED_OFFSET_VALUE = 2` — src/yamkix/yaml_writer.py:9

**Evidence.**
- enforcement — src/yamkix/yaml_writer.py:33-36 `get_opinionated_yaml_writer`
  `if yamkix_config.dash_inwards:`
- test — tests/test_non_regression.py:235 `TestNonRegression::test_config`
  `assert filecmp.cmp(expected_output_file, actual_output_file, shallow=True)`
- test — tests/test_yaml_writer.py:131-133 `test_dash_inwards_enabled`
  `assert yaml_writer.sequence_indent == OPINIONATED_SEQUENCE_VALUE`

**Edge cases.**
- **LAY-R003.E1** Given the `dash-at-col0-1` file whose nested list under `value:` has its dash 2 spaces in, when it is formatted with no option, then the dash stays 2 spaces in from `value:`. — verified — tests/test_non_regression.py:28
- **LAY-R003.E2** Given the `dash-at-col2-1` file, when it is formatted with no option, then nested list dashes are 2 spaces in from their key. — verified — tests/test_non_regression.py:29

**History.**
- 2026-10-24 · 823a0f3 · created

### LAY-R004 · With `--no-dash-inwards`, dashes align with their parent key
- **Kind:** rule · **Category:** calculation
- **Status:** active · **Confidence:** verified · **Audit:** passed
- **Verified at:** 823a0f3 (2026-10-24)

**Rule.** With `--no-dash-inwards`, the dash of a nested list is written at the same column as its parent key, using the YAML library's default indentation.

**Parameters.** `--no-dash-inwards` / `-d` — src/yamkix/_cli.py:168-178 (off by default)

**Evidence.**
- enforcement — src/yamkix/yaml_writer.py:33 `get_opinionated_yaml_writer`
  `if yamkix_config.dash_inwards:`
- test — tests/test_non_regression.py:235 `TestNonRegression::test_config`
  `assert filecmp.cmp(expected_output_file, actual_output_file, shallow=True)`

**Edge cases.**
- **LAY-R004.E1** Given the `dash-at-col0-1` file whose nested list under `value:` has its dash 2 spaces in, when it is formatted with `--no-dash-inwards`, then the dash moves to the column of `value:`. — verified — tests/test_non_regression.py:22

**History.**
- 2026-10-24 · 823a0f3 · created

### LAY-R005 · A document that is a list keeps its dashes at column 0
- **Kind:** rule · **Category:** calculation
- **Status:** active · **Confidence:** verified · **Audit:** passed
- **Verified at:** 01d0951 (2026-10-25)

**Rule.** When a whole document is a list and dashes are pushed inwards, its top-level dashes are written at column 0 and the rest of the document is shifted 2 spaces left to match.

**Context.** The indentation of LAY-R003 would otherwise push the top-level dashes 2 spaces in; yamkix removes the first 2 spaces of every line of such a document after dumping it. With `--no-dash-inwards` the shift is not needed and not applied.

**Evidence.**
- enforcement — src/yamkix/yamkix.py:280-281 `yamkix_dump_one`
  `if dash_inwards and type(single_item).__name__ == "CommentedSeq":`
- enforcement — src/yamkix/helpers.py:28-29 `strip_leading_double_space`
  `return stream.replace("\n  ", "\n")`
- test — tests/test_non_regression.py:235 `TestNonRegression::test_config`
  `assert filecmp.cmp(expected_output_file, actual_output_file, shallow=True)`

**Edge cases.**
- **LAY-R005.E1** Given the `dash-at-col0-1` file, a list of maps at the top level, when it is formatted with no option, then its top-level dashes stay at column 0 while its nested list keeps its dash 2 spaces in. — verified — tests/test_non_regression.py:28
- **LAY-R005.E2** Given a top-level list parsed with `--typ safe`, when it is formatted, then the shift is not applied because the document is not a round-trip list. — inferred — src/yamkix/yamkix.py:280

**Open questions.** The check is on the class name `CommentedSeq`, which only round-trip mode produces; is the layout of top-level lists in safe mode what users expect?

**History.**
- 2026-10-25 · 01d0951 · reanchored · source lines shifted by the block scalar, comment and atomic write fixes
- 2026-10-24 · 823a0f3 · created

### LAY-R006 · Default flow style only shapes collections that have no style of their own
- **Kind:** rule · **Category:** derivation
- **Status:** active · **Confidence:** read · **Audit:** passed
- **Verified at:** 823a0f3 (2026-10-24)

**Rule.** Collections are written in block style by default; `--default-flow-style` switches to flow style only collections whose style the parser did not record, which in round-trip mode means it has almost no visible effect, while in safe mode the whole document is written in flow style.

**Context.** In round-trip mode each collection keeps the style it had in the input, so a flow list stays flow and a block map stays block whatever this option says. The safe parser keeps no style, so the option applies everywhere.

**Parameters.** `--default-flow-style` / `-f` — src/yamkix/_cli.py:146-156 (off by default)

**Evidence.**
- enforcement — src/yamkix/yaml_writer.py:30 `get_opinionated_yaml_writer`
  `yaml.default_flow_style = yamkix_config.default_flow_style`
- test — tests/test_non_regression.py:235 `TestNonRegression::test_config`
  `assert filecmp.cmp(expected_output_file, actual_output_file, shallow=True)`

**Edge cases.**
- **LAY-R006.E1** Given the `flow-style-collections` file mixing flow and block collections, when it is formatted with no option, then every collection keeps its input style. — verified — tests/test_non_regression.py:171
- **LAY-R006.E2** Given a file with a block map and a flow list, when it is formatted with `--default-flow-style` in round-trip mode, then the output is the same as without the option. — read — src/yamkix/yaml_writer.py:30
- **LAY-R006.E3** Given the same file, when it is formatted with `--typ safe --default-flow-style`, then the whole document is written on the `---` line in flow style. — read — src/yamkix/yaml_writer.py:30

**Open questions.** No test runs `--default-flow-style` alone; should its near-absence of effect in round-trip mode be pinned or documented in the option help?

**History.**
- 2026-10-24 · 823a0f3 · created

### LAY-R007 · `--enforce-block-style` turns every flow collection into block style
- **Kind:** rule · **Category:** calculation
- **Status:** active · **Confidence:** verified · **Audit:** passed
- **Verified at:** 01d0951 (2026-10-25)

**Rule.** With `--enforce-block-style` in round-trip mode, every map and list of the document, at any depth, is written in block style, except empty ones, which stay `[]` and `{}`.

**Context.** Block style has no way to write an empty collection. The conversion only touches round-trip collections; in safe mode it does nothing (E3).

**Parameters.** `--enforce-block-style` / `-B` — src/yamkix/_cli.py:157-167 (off by default)

**Evidence.**
- enforcement — src/yamkix/yamkix.py:225-226 `yamkix_dump_all`
  `if enforce_block_style_flag:`
- enforcement — src/yamkix/helpers.py:167-175 `convert_flow_to_block_style`
  `data.fa.set_block_style()`
- test — tests/test_non_regression.py:235 `TestNonRegression::test_config`
  `assert filecmp.cmp(expected_output_file, actual_output_file, shallow=True)`
- test — tests/test_helpers.py:444 `test_empty_collections_stay_flow`
  `assert self._round_trip(yaml_input) == yaml_input`

**Edge cases.**
- **LAY-R007.E1** Given the `flow-style-collections` file with flow lists and maps nested three levels deep, when it is formatted with `--enforce-block-style`, then all of them are in block style and `empty_list: []` and `empty_map: {}` are unchanged. — verified — tests/test_non_regression.py:177
- **LAY-R007.E2** Given `a-json-map: {key1: value1}`, when it is formatted with `--enforce-block-style`, then it is written as a block map under `a-json-map:`. — verified — tests/test_non_regression.py:207
- **LAY-R007.E3** Given the option with `--typ safe --default-flow-style`, when a file is formatted, then the whole document is still written in flow style. — read — src/yamkix/helpers.py:167

**History.**
- 2026-10-25 · 01d0951 · reanchored · source lines shifted by the block scalar, comment and atomic write fixes
- 2026-10-24 · 823a0f3 · created

### LAY-R008 · `--enforce-block-style` wins over `--default-flow-style`
- **Kind:** rule · **Category:** derivation
- **Status:** active · **Confidence:** verified · **Audit:** passed
- **Verified at:** 01d0951 (2026-10-25)

**Rule.** In round-trip mode, when both `--enforce-block-style` and `--default-flow-style` are given, every non-empty collection is written in block style, and a warning says so.

**Context.** The precedence comes from the order of operations: each collection is explicitly marked block before dumping, so the default style never applies. In safe mode the warning is printed but the output is flow style (LAY-R007.E3).

**Evidence.**
- enforcement — src/yamkix/yamkix.py:225-226 `yamkix_dump_all`
  `convert_flow_to_block_style(data=single_item)`
- enforcement — src/yamkix/config.py:323 `raise_enforce_block_style_warning_if_needed`
  `if enforce_block_style is True and default_flow_style is True:`
- test — tests/test_non_regression.py:235 `TestNonRegression::test_config`
  `assert filecmp.cmp(expected_output_file, actual_output_file, shallow=True)`

**Edge cases.**
- **LAY-R008.E1** Given the `flow-style-collections` file, when it is formatted with `--default-flow-style --enforce-block-style`, then the output is the same as with `--enforce-block-style` alone. — verified — tests/test_non_regression.py:183

**Open questions.** In safe mode the warning promises block style but the output is flow style: should the warning, or the conversion, take the parsing mode into account?

**History.**
- 2026-10-25 · 01d0951 · reanchored · source lines shifted by the block scalar, comment and atomic write fixes
- 2026-10-24 · 823a0f3 · created

### LAY-R009 · Lines are folded at 2048 characters by default
- **Kind:** rule · **Category:** calculation
- **Status:** active · **Confidence:** verified · **Audit:** passed
- **Verified at:** 823a0f3 (2026-10-24)

**Rule.** Long plain values and flow collections are folded onto several lines once a line would exceed 2048 characters, or the width given with `--line-width`.

**Context.** The default is wide enough that, in practice, yamkix does not fold lines unless asked. Literal blocks (`|`) are not refolded; long quoted strings are.

**Parameters.** `DEFAULT_LINE_WIDTH = 2048` — src/yamkix/config.py:12; `--line-width` / `-w` — src/yamkix/_cli.py:197-204

**Evidence.**
- enforcement — src/yamkix/yaml_writer.py:32 `get_opinionated_yaml_writer`
  `yaml.width = yamkix_config.line_width`
- test — tests/test_non_regression.py:235 `TestNonRegression::test_config`
  `assert filecmp.cmp(expected_output_file, actual_output_file, shallow=True)`

**Edge cases.**
- **LAY-R009.E1** Given the `issue-437` file with a 143-character value, when it is formatted with no option, then the line is kept whole. — verified — tests/test_non_regression.py:219
- **LAY-R009.E2** Given the same file, when it is formatted with `--line-width 80`, then the long value and the long flow list are folded onto continuation lines. — verified — tests/test_non_regression.py:213

**History.**
- 2026-10-24 · 823a0f3 · created

### LAY-R010 · No output line ends with a space, except inside block scalars
- **Kind:** rule · **Category:** calculation
- **Status:** changed · **Confidence:** verified · **Audit:** passed
- **Verified at:** 01d0951 (2026-10-25)

**Rule.** Every line yamkix writes has its trailing spaces removed, whatever the options, except the content lines of literal (`|`) and folded (`>`) block scalars, whose trailing spaces are part of the value and are kept.

**Context.** Works around the YAML library leaving a space where it folds a line (issue #437). A block scalar runs from its header line up to the first non-blank line indented less than its content. A line wrongly taken for a header (a plain value ending with ` |`) only leaves fold-point spaces in place; it never changes a value.

**Evidence.**
- enforcement — src/yamkix/helpers.py:16-18 `_BLOCK_SCALAR_HEADER`
- enforcement — src/yamkix/helpers.py:37-86 `strip_trailing_spaces`
- enforcement — src/yamkix/yamkix.py:280-283 `yamkix_dump_one`
- test — tests/test_helpers.py:130 `test_strip_trailing_spaces`
  `assert strip_trailing_spaces(stream) == expected`
- test — tests/test_yamkix.py:356-357 `TestBlockScalarTrailingSpaces::test_block_scalar_values_are_unchanged`
  `assert output == document`

**Edge cases.**
- **LAY-R010.E1** Given the `issue-437` file, when it is formatted with `--line-width 80`, then the folded lines have no trailing space. — verified — tests/test_non_regression.py:213
- **LAY-R010.E2** Given `quoted: "line one \nline two"` with an escaped line break after a space, when the trailing spaces are stripped, then the value is unchanged. — verified — tests/test_helpers.py:117
- **LAY-R010.E3** Given a literal block `s: |` whose first line is `a` followed by two spaces, when it is formatted, then the two spaces are kept and the loaded value stays `"a  \nb\n"`. — verified — tests/test_yamkix.py:356
- **LAY-R010.E4** Given a plain value ending with ` |` (`k: a |`) followed by a line with a trailing space, when the trailing spaces are stripped, then the next line is still stripped and no value changes. — verified — tests/test_helpers.py:125

**History.**
- 2026-10-25 · 01d0951 · changed · trailing spaces of block scalar lines are now kept; E3 read → verified, E4 added, open question resolved
- 2026-10-24 · 823a0f3 · created
