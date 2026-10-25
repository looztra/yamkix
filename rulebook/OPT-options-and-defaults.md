# OPT · Options and defaults
The opinionated defaults of yamkix and how options are turned into one formatting configuration, through the command line or the Python API (`get_yamkix_config_from_default`, used by kubesplit).

**Scope.** Read: `src/yamkix/config.py` (defaults, `get_yamkix_config_from_default`), the parser-mode option in `src/yamkix/_cli.py`, `src/yamkix/yaml_writer.py:27`, `tests/test_config.py`, `tests/test_cli.py`, and the yamkix imports of kubesplit 0.5.0 (installed by the integration test). Behaviour also observed by calling the API and the CLI. Not carded: the legacy argparse API (`src/yamkix/args.py`, `get_config_from_args`, `get_spaces_before_comment_from_args`, `get_input_output_config_from_args`), which nothing in the repository calls outside tests and kubesplit 0.5.0 no longer imports: dead code. The three option warnings are carded where their effect lives: QUO-R004, LAY-R008, FIL-R006.

## Other operating rules

### OPT-R001 · The default configuration
- **Kind:** rule · **Category:** derivation
- **Status:** active · **Confidence:** verified · **Audit:** passed
- **Verified at:** b6f1a4f (2026-10-25)

**Rule.** Unless told otherwise, yamkix uses round-trip parsing, writes `---` but not `...`, keeps block style, pushes dashes inwards, keeps quotes, does not force double quotes nor block style, leaves comment spacing and alignment alone, and folds lines at 2048 characters.

**Parameters.** `DEFAULT_LINE_WIDTH = 2048` — src/yamkix/config.py:12

**Evidence.**
- enforcement — src/yamkix/config.py:135-149 `get_default_yamkix_config`
- test — tests/test_config.py:162-173 `TestYamkixConfigFromArgs::test_default_values`
  `assert sut.dash_inwards is True`

**History.**
- 2026-10-25 · b6f1a4f · reanchored · test now asserts align_comments and enforce_double_quotes; open question resolved (uncommitted)
- 2026-10-24 · 823a0f3 · created

### OPT-R002 · The Python API overrides only the values it is given
- **Kind:** rule · **Category:** derivation
- **Status:** active · **Confidence:** verified · **Audit:** passed
- **Verified at:** 823a0f3 (2026-10-24)

**Rule.** `get_yamkix_config_from_default` builds a configuration where every value not given (left to `None`) takes its default from OPT-R001, and input and output default to STDIN and STDOUT.

**Context.** The parser mode is not checked here: an unknown mode is accepted and only fails when the YAML writer is built (E1). `enforce_double_quotes` defaults to `False` rather than `None`, so its fallback to the default is never used.

**Evidence.**
- enforcement — src/yamkix/config.py:213-233 `get_yamkix_config_from_default`
  `parsing_mode=parsing_mode if parsing_mode is not None else default_config.parsing_mode,`
- test — tests/test_config.py:302-311 `TestGetYamkixConfigFromDefault::test_get_yamkix_config_from_default_parsing_mode`
  `assert sut.explicit_start == reference.explicit_start`

**Edge cases.**
- **OPT-R002.E1** Given `parsing_mode="yolo"`, when the configuration is built and then used to build the YAML writer, then the configuration is accepted and the writer fails with a "not recognised" error. — read — src/yamkix/yaml_writer.py:27

**Open questions.** Should the Python API refuse an unknown parser mode, as the dead argparse path does (`config.py:268`)?

**History.**
- 2026-10-24 · 823a0f3 · created

### OPT-R003 · The command line accepts only the `rt` and `safe` parser modes, in any letter case
- **Kind:** rule · **Category:** validation
- **Status:** active · **Confidence:** verified · **Audit:** passed
- **Verified at:** 823a0f3 (2026-10-24)

**Rule.** `--typ` must be `rt` or `safe`, in any letter case; any other value is refused before any file is processed, with a non-zero exit code.

**Parameters.** `--typ` / `-t` — src/yamkix/_cli.py:104-112 (default `rt`)

**Evidence.**
- enforcement — src/yamkix/_cli.py:39-43 `SupportedYamlParserMode`
- enforcement — src/yamkix/_cli.py:104-112 `main`
  `case_sensitive=False,`
- test — tests/test_cli.py:69-71 `TestCli::test_invalid_typ`
  `assert "'safe', 'rt'" in result.output`

**History.**
- 2026-10-24 · 823a0f3 · created

### OPT-R004 · Safe mode re-emits the data, not the document
- **Kind:** rule · **Category:** derivation
- **Status:** active · **Confidence:** read · **Audit:** passed
- **Verified at:** 823a0f3 (2026-10-24)

**Rule.** With `--typ safe`, the output is rebuilt from the data alone: comments are dropped, original quotes and collection styles are forgotten, map keys are sorted alphabetically and literal blocks (`|`) become quoted strings.

**Context.** The parser mode is handed as is to the YAML library; only round-trip mode keeps the shape of the input. The per-topic effects are carded in CMT-R001, QUO-R001 and LAY-R006.

**Evidence.**
- enforcement — src/yamkix/yaml_writer.py:27 `get_opinionated_yaml_writer`
  `yaml = YAML(typ=yamkix_config.parsing_mode)`

**Edge cases.**
- **OPT-R004.E1** Given keys `k1`, `l`, `n`, `b` in that order with `b: |` holding `'x'`, when formatted with `--typ safe`, then `b` comes first and is written `b: "'x'\n"`. — read — src/yamkix/yaml_writer.py:27

**Open questions.** Is the key sorting in safe mode wanted? The `--typ` help only warns about comments.

**History.**
- 2026-10-24 · 823a0f3 · created
