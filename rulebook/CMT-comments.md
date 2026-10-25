# CMT · Comments
How yamkix keeps, spaces and aligns the end-of-line comments of a YAML document. Comments only survive in the round-trip (`rt`) parsing mode; the two comment options (`--spaces-before-comment`, `--align-comments`) only rework end-of-line comments, never full-line comments on their own.

**Scope.** Read: `src/yamkix/comments.py`, the comment calls in `src/yamkix/yamkix.py` (`yamkix_dump_all`, `yamkix_dump_one`), `src/yamkix/yaml_writer.py:27`, `tests/test_comments.py`, the comment cases of `tests/test_non_regression.py` and their fixtures. Behaviour also observed by running the CLI on a sample file. Not read: the internals of `ruamel.yaml` that place comments (slot layout of `ca.items`, emitter column handling).

## CMT-P01 · Formatting keeps the author's comments
- **Kind:** policy · **Nature:** product promise (yamkix documents "comments preserved by default")

**Statement.** Reformatting a YAML file must not lose or move the comments its author wrote.

### CMT-R001 · Comments are kept in round-trip mode and dropped in safe mode
- **Kind:** rule · **Category:** derivation · **Implements:** CMT-P01
- **Status:** active · **Confidence:** verified · **Audit:** passed
- **Verified at:** dc86185 (2026-10-25)

**Rule.** Comments are kept only when the parsing mode is `rt` (the default); with `--typ safe` every comment is removed from the output.

**Context.** The parsing mode chosen by the user is handed as is to the YAML library; the safe loader does not keep comments. The `--typ` help text warns about it. Only comments are lost: the data is the same, including a `#` inside a quoted value. Safe mode also changes the layout (OPT-R004).

**Evidence.**
- enforcement — src/yamkix/yaml_writer.py:27 `get_opinionated_yaml_writer`
  `yaml = YAML(typ=yamkix_config.parsing_mode)`
- test — tests/test_yamkix.py:262 `TestCommentsByParsingMode::test_comments_follow_parsing_mode`
  `assert [comment for comment in COMMENT_TEXTS if comment in output] == (COMMENT_TEXTS if comments_kept else [])`
- test — tests/test_yamkix.py:296-297 `TestCommentsByParsingMode::test_safe_mode_drops_comments_but_keeps_data`
  `assert safe_loader.load(output) == safe_loader.load(COMMENTED_DOCUMENT)`

**Edge cases.**
- **CMT-R001.E1** Given a document with a top-level full-line comment, a nested full-line comment and end-of-line comments on a map entry and a list item, when it is formatted in `rt` mode, then all four comments are kept. — verified — tests/test_yamkix.py:242
- **CMT-R001.E2** Given the same document, when it is formatted in `safe` mode, then none of the four comments is left. — verified — tests/test_yamkix.py:243
- **CMT-R001.E3** Given the same document with `url: "http://example.com/#anchor"`, when it is formatted in `safe` mode, then the loaded data is identical to the input's, `#anchor` included. — verified — tests/test_yamkix.py:267
- **CMT-R001.E4** Given `--spaces-before-comment 2` or `--align-comments` in `safe` mode, when the document is formatted, then the comment options have nothing to act on, no error is raised and no comment is written. — verified — tests/test_yamkix.py:268-269

**History.**
- 2026-10-25 · dc86185 · reanchored · test lines shifted by added tests and imports (uncommitted)
- 2026-10-24 · e9e0cca · changed · confidence read → verified, tests added in tests/test_yamkix.py
- 2026-10-24 · 823a0f3 · created

### CMT-R002 · Without a spacing option, comments keep their original column
- **Kind:** rule · **Category:** derivation · **Implements:** CMT-P01
- **Status:** active · **Confidence:** verified · **Audit:** passed
- **Verified at:** 01d0951 (2026-10-25)

**Rule.** When `--spaces-before-comment` is not given, end-of-line comments are written at the same column as in the input, so the gap before a comment grows or shrinks when the value before it is reformatted.

**Context.** Comment repositioning only runs when a number of spaces was given; otherwise the YAML library re-emits each comment at its original column. `--align-comments` is a separate option and can still move them (CMT-R005).

**Evidence.**
- enforcement — src/yamkix/yamkix.py:278-279 `yamkix_dump_one`
  `if spaces_before_comment is not None:`
- test — tests/test_non_regression.py:235 `TestNonRegression::test_config`
  `assert filecmp.cmp(expected_output_file, actual_output_file, shallow=True)`

**Edge cases.**
- **CMT-R002.E1** Given the `issue-259-01` file with comments one space after their value, when it is formatted with no option, then the comments stay one space after their value. — verified — tests/test_non_regression.py:165
- **CMT-R002.E2** Given `a:   1 # c1` (three spaces before the value, one before the comment), when it is formatted with no option, then the value is written `a: 1` and the comment keeps its column, three spaces after the value. — read — src/yamkix/yamkix.py:278

**History.**
- 2026-10-25 · 01d0951 · reanchored · source lines shifted by the block scalar, comment and atomic write fixes
- 2026-10-24 · 823a0f3 · created

### CMT-R004 · A comment on a key that opens a nested list stays on that key's line
- **Kind:** rule · **Category:** derivation · **Implements:** CMT-P01
- **Status:** active · **Confidence:** verified · **Audit:** passed
- **Verified at:** 01d0951 (2026-10-25)

**Rule.** When `--spaces-before-comment` is used, a comment written after a key whose value is a nested list (`list: # comment`) stays on the key line and the list items are not lost or moved.

**Context.** Fix for issue #29: yamkix clears the second comment slot the library keeps for such a key before re-adding the comment, so the comment is written once, on the key line.

**Evidence.**
- enforcement — src/yamkix/comments.py:48-49 `fix_for_issue29`
  `data.ca.items[key][3] = None`
- test — tests/test_non_regression.py:235 `TestNonRegression::test_config`
  `assert filecmp.cmp(expected_output_file, actual_output_file, shallow=True)`

**Edge cases.**
- **CMT-R004.E1** Given `list: # this is a comment that kills it` followed by three items, when it is formatted with `--spaces-before-comment 1`, then the comment stays on the `list:` line with one space before it and the three items follow. — verified — tests/test_non_regression.py:147

**History.**
- 2026-10-25 · 01d0951 · reanchored · source lines shifted by the block scalar, comment and atomic write fixes
- 2026-10-24 · 823a0f3 · created

## Other operating rules

### CMT-R003 · A fixed number of spaces is put before every end-of-line comment
- **Kind:** rule · **Category:** calculation
- **Status:** changed · **Confidence:** verified · **Audit:** passed
- **Verified at:** 01d0951 (2026-10-25)

**Rule.** With `--spaces-before-comment N`, every end-of-line comment of a map or a list is written exactly N spaces after its content; a value of 0 gives one space.

**Context.** The comment is re-added with N − 1 extra spaces in front of it, at column 0; for 0 nothing is added and the library still writes one separating space. Full-line comments are not re-spaced: the full-line comments and blank lines that follow an end-of-line comment are carried in the same comment token and are kept on their own lines.

**Parameters.** `--spaces-before-comment` / `-c` — src/yamkix/_cli.py:179-188 (no default: comments left as is)

**Evidence.**
- enforcement — src/yamkix/comments.py:25-28 `yamkix_add_eol_comment`
  `additional_spaces = 1 if org_col is None else org_col - 1`
- enforcement — src/yamkix/comments.py:37-43 `process_single_comment`
  `data.yaml_add_eol_comment(comment, key, column=column)`
- test — tests/test_yamkix.py:323 `TestCommentsFollowingAnEndOfLineComment::test_full_line_comments_and_blank_lines_are_kept`
- test — tests/test_non_regression.py:235 `TestNonRegression::test_config`
  `assert filecmp.cmp(expected_output_file, actual_output_file, shallow=True)`

**Edge cases.**
- **CMT-R003.E1** Given the `issue-11` file with comments one to four spaces after their value, when it is formatted with `--spaces-before-comment 2`, then every comment is two spaces after its value. — verified — tests/test_non_regression.py:93
- **CMT-R003.E2** Given the same file, when it is formatted with `--spaces-before-comment 0`, then every comment is one space after its value, as with 1. — verified — tests/test_non_regression.py:105
- **CMT-R003.E3** Given a commented line followed by a full-line comment and blank lines (`b: 22 # c2` then `# full line`), when it is formatted with `--spaces-before-comment 1` or `3`, then the end-of-line comment is re-spaced and the full-line comment and blank lines stay on their own lines. — verified — tests/test_yamkix.py:323
- **CMT-R003.E4** Given both `--align-comments` and `--spaces-before-comment 1`, when a file is formatted, then the fixed spacing wins and comments are not aligned. — read — src/yamkix/yamkix.py:279

**Open questions.** Should a value of 0 mean "no space" or be refused rather than behave as 1?

**History.**
- 2026-10-25 · 01d0951 · changed · E3: following full-line comments and blank lines are kept instead of glued; read → verified, open question resolved
- 2026-10-24 · 823a0f3 · created

### CMT-R005 · Comments of a map or a list are aligned on their rightmost comment
- **Kind:** rule · **Category:** calculation
- **Status:** changed · **Confidence:** verified · **Audit:** passed
- **Verified at:** 01d0951 (2026-10-25)

**Rule.** With `--align-comments`, the end-of-line comments of each map and of each list are moved to the column of the rightmost comment of that same map or list; each map and each list is aligned on its own.

**Context.** The target column is the rightmost comment already present, not "longest value plus one space": a comment pushed far right in the input pulls the others with it. Maps keep their end-of-line comments in slot `[2]` of their comment items, lists in slot `[0]`; items without a comment are skipped.

**Parameters.** `--align-comments` / `-a` — src/yamkix/_cli.py:189-196 (off by default)

**Evidence.**
- enforcement — src/yamkix/comments.py:89-104 `align_comments`
  `eol_comments = [comment[slot] for comment in d.ca.items.values() if comment[slot] is not None]`
- test — tests/test_non_regression.py:235 `TestNonRegression::test_config`
  `assert filecmp.cmp(expected_output_file, actual_output_file, shallow=True)`

**Edge cases.**
- **CMT-R005.E1** Given two maps `sub_key1` and `sub_key2` with comments one space after values of different lengths, when the file is formatted with `--align-comments`, then each map's comments line up on their own column, different for the two maps. — verified — tests/test_non_regression.py:159
- **CMT-R005.E2** Given a list whose items `a # c1` and `longer_value # c2` carry comments at different columns and a third item without a comment, when it is formatted with `--align-comments`, then both comments line up after `longer_value` and the third item is left as is. — verified — tests/test_comments.py:76

**History.**
- 2026-10-25 · 01d0951 · reanchored · source lines shifted by the block scalar, comment and atomic write fixes
- 2026-10-25 · dc86185 · changed · map comments only → map and list comments aligned (uncommitted)
- 2026-10-25 · b6f1a4f · changed · E2 read → verified, mocked sequence test replaced by a strict xfail on a real list (uncommitted)
- 2026-10-24 · 823a0f3 · created
