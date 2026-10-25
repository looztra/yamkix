# OPT · Options and defaults
The opinionated defaults of yamkix and how options are turned into one formatting configuration, through the command line or the Python API (`get_yamkix_config_from_default`, used by kubesplit).

**Scope.** Read: `src/yamkix/config.py` (defaults, `get_yamkix_config_from_default`), the parser-mode option in `src/yamkix/_cli.py`, `src/yamkix/yaml_writer.py:27`, `tests/test_config.py`, `tests/test_cli.py`, and the yamkix imports of kubesplit 0.5.0 (installed by the integration test). Behaviour also observed by calling the API and the CLI. Not carded: the legacy argparse API (`src/yamkix/args.py`, `get_config_from_args`, `get_spaces_before_comment_from_args`, `get_input_output_config_from_args`), which nothing in the repository calls outside tests and kubesplit 0.5.0 no longer imports: dead code. The three option warnings are carded where their effect lives: QUO-R004, LAY-R008, FIL-R006.

## Other operating rules

### OPT-R001 · The default configuration
- **Kind:** rule · **Category:** derivation
- **Status:** active · **Confidence:** verified · **Audit:** passed
- **Verified at:** 3825235 (2026-10-25)

**Rule.** Unless told otherwise, yamkix uses round-trip parsing, writes `---` but not `...`, keeps block style, pushes dashes inwards, keeps quotes, does not force double quotes nor block style, leaves comment spacing and alignment alone, and folds lines at 2048 characters.

**Parameters.** `DEFAULT_LINE_WIDTH = 2048` — src/yamkix/config.py:12

**Evidence.**
- enforcement — src/yamkix/config.py:136-150 `get_default_yamkix_config`
- test — tests/test_config.py:162-173 `TestYamkixConfigFromArgs::test_default_values`
  `assert sut.dash_inwards is True`

**History.**
- 2026-10-25 · 3825235 · reanchored · lines shifted by the parser-mode, safe-mode warning and spacing fixes (uncommitted)
- 2026-10-25 · b6f1a4f · reanchored · test now asserts align_comments and enforce_double_quotes; open question resolved (uncommitted)
- 2026-10-24 · 823a0f3 · created

### OPT-R002 · The Python API overrides only the values it is given, and refuses an unknown parser mode
- **Kind:** rule · **Category:** derivation
- **Status:** changed · **Confidence:** verified · **Audit:** passed
- **Verified at:** 3825235 (2026-10-25)

**Rule.** `get_yamkix_config_from_default` builds a configuration where every value not given (left to `None`) takes its default from OPT-R001, and input and output default to STDIN and STDOUT; a parser mode other than `rt` or `safe`, in exactly that case, is refused with `InvalidTypValueError` when the configuration is built.

**Context.** Unlike the command line (OPT-R003), the check is case-sensitive: `"RT"` is refused, since the YAML library only knows the lowercase names. `enforce_double_quotes` defaults to `False` rather than `None`, so its fallback to the default is never used.

**Parameters.** `SUPPORTED_PARSING_MODES = ("rt", "safe")` — src/yamkix/config.py:15

**Evidence.**
- config — src/yamkix/config.py:15 `SUPPORTED_PARSING_MODES`
  `SUPPORTED_PARSING_MODES: Final = ("rt", "safe")`
- enforcement — src/yamkix/config.py:217-219 `get_yamkix_config_from_default`
  `if parsing_mode is not None and parsing_mode not in SUPPORTED_PARSING_MODES:`
- enforcement — src/yamkix/config.py:220-240 `get_yamkix_config_from_default`
  `parsing_mode=parsing_mode if parsing_mode is not None else default_config.parsing_mode,`
- test — tests/test_config.py:297-313 `TestGetYamkixConfigFromDefault::test_get_yamkix_config_from_default_parsing_mode`
  `assert sut.explicit_start == reference.explicit_start`
- test — tests/test_config.py:315-319 `TestGetYamkixConfigFromDefault::test_get_yamkix_config_from_default_refuses_invalid_parsing_mode`
  `with pytest.raises(InvalidTypValueError):`

**Edge cases.**
- **OPT-R002.E1** Given `parsing_mode="yolo"`, when the configuration is built, then `InvalidTypValueError` is raised. — verified — tests/test_config.py:315
- **OPT-R002.E2** Given `parsing_mode="RT"`, when the configuration is built, then `InvalidTypValueError` is raised. — verified — tests/test_config.py:315
- **OPT-R002.E3** Given `parsing_mode="safe"`, when the configuration is built, then it is kept and every other value is the default. — verified — tests/test_config.py:297

**History.**
- 2026-10-25 · 3825235 · changed · unknown parser mode accepted until the writer is built → refused when the configuration is built; E1 rewritten, E2 and E3 added, open question resolved (uncommitted)
- 2026-10-25 · dc86185 · reanchored · test lines shifted by added tests and imports (uncommitted)
- 2026-10-24 · 823a0f3 · created

### OPT-R003 · The command line accepts only the `rt` and `safe` parser modes, in any letter case
- **Kind:** rule · **Category:** validation
- **Status:** active · **Confidence:** verified · **Audit:** passed
- **Verified at:** 3825235 (2026-10-25)

**Rule.** `--typ` must be `rt` or `safe`, in any letter case; any other value is refused before any file is processed, with a non-zero exit code.

**Parameters.** `--typ` / `-t` — src/yamkix/_cli.py:104-113 (default `rt`)

**Evidence.**
- enforcement — src/yamkix/_cli.py:39-43 `SupportedYamlParserMode`
- enforcement — src/yamkix/_cli.py:104-113 `main`
  `case_sensitive=False,`
- test — tests/test_cli.py:70-72 `TestCli::test_invalid_typ`
  `assert "'safe', 'rt'" in result.output`

**History.**
- 2026-10-25 · 3825235 · reanchored · only the `--typ` help text changed; lines shifted (uncommitted)
- 2026-10-25 · dc86185 · reanchored · test lines shifted by added tests and imports (uncommitted)
- 2026-10-24 · 823a0f3 · created

### OPT-R004 · Safe mode re-emits the data, not the document
- **Kind:** rule · **Category:** derivation
- **Status:** active · **Confidence:** read · **Audit:** passed
- **Verified at:** 3825235 (2026-10-25)

**Rule.** With `--typ safe`, the output is rebuilt from the data alone: comments are dropped, original quotes and collection styles are forgotten, map keys are sorted alphabetically and literal blocks (`|`) become quoted strings.

**Context.** The parser mode is handed as is to the YAML library; only round-trip mode keeps the shape of the input. The per-topic effects are carded in CMT-R001, QUO-R001 and LAY-R006.

**Evidence.**
- enforcement — src/yamkix/yaml_writer.py:27 `get_opinionated_yaml_writer`
  `yaml = YAML(typ=yamkix_config.parsing_mode)`
- doc — src/yamkix/_cli.py:109-110 `main`
  `"comments, original quotes and collection styles are lost, and map keys are sorted."`

**Edge cases.**
- **OPT-R004.E1** Given keys `k1`, `l`, `n`, `b` in that order with `b: |` holding `'x'`, when formatted with `--typ safe`, then `b` comes first and is written `b: "'x'\n"`. — read — src/yamkix/yaml_writer.py:27

**History.**
- 2026-10-25 · 3825235 · reanchored · key sorting and the other losses now described in the `--typ` help; open question resolved (uncommitted)
- 2026-10-24 · 823a0f3 · created
