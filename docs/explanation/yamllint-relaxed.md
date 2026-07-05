# Comparison with yamllint

This page compares yamkix's opinionated defaults with [yamllint](https://yamllint.readthedocs.io/en/stable/)'s `relaxed` preset. For the reasoning behind yamkix's defaults, see [Formatting rules](formatting-rules.md); for yamllint's side, see its [configuration presets](https://yamllint.readthedocs.io/en/stable/configuration.html) and [detailed rules](https://yamllint.readthedocs.io/en/stable/rules.html) documentation.

A framing note first: the two are different kinds of tools. **yamllint** _checks_ YAML and reports problems; **yamkix** _rewrites_ it. So the meaningful question is not "do they have the same options" but: _does yamkix's default output satisfy the `relaxed` ruleset, and where do their opinions diverge?_

## yamkix defaults recap

| Setting | Default value |
| --- | --- |
| `parsing_mode` | `rt` (round-trip: preserves comments, anchors, key order) |
| `explicit_start` | `True` (emits `---`) |
| `explicit_end` | `False` |
| `default_flow_style` | `False` (block style for new collections; existing flow preserved in `rt`) |
| `dash_inwards` | `True` → indent `mapping=2, sequence=4, offset=2` |
| `quotes_preserved` | `True` |
| `spaces_before_comment` | `None` (comment spacing untouched) |
| `line_width` | `2048` |

## What the relaxed preset changes vs yamllint default

The `relaxed` preset `extends: default` and is deliberately more tolerant:

- **Disabled rules**: `comments`, `comments-indentation`, `document-start`, `truthy`
- **Downgraded to warning**: `braces`, `brackets` (both with `max-spaces-inside: 1`), `colons`, `commas`, `empty-lines`, `hyphens`, `indentation` (with `indent-sequences: consistent`), `line-length` (with `allow-non-breakable-inline-mappings: true`)
- **Still errors**: `anchors`, `key-duplicates`, `new-line-at-end-of-file`, `new-lines`, `trailing-spaces`
- **Already disabled in `default`**: `document-end`, `quoted-strings`, `octal-values`, `key-ordering`, `empty-values`, `float-values`

## What matches

| Concern | yamkix default | yamllint relaxed | Verdict |
| --- | --- | --- | --- |
| `document-end` (`...`) | `explicit_end=False` | rule disabled | Aligned |
| Quote style | preserved as-is | `quoted-strings` disabled | Aligned — both hands-off |
| Truthy values (`yes`/`on`…) | `rt` preserves scalars verbatim | disabled | Aligned |
| Comment spacing/indent | untouched by default | `comments`/`comments-indentation` disabled | Aligned — both hands-off |
| Indentation | consistent 2-space maps, dashes always indented | `spaces: consistent`, `indent-sequences: consistent` (warning) | Passes — yamkix output is consistent by construction |
| `hyphens` / `colons` / `commas` | ruamel emits `- x`, `key: v`, `[a, b]` — canonical single spaces | max 1 space (warnings) | Passes |
| `brackets` / `braces` | ruamel emits flow collections with no inner padding | up to 1 inner space tolerated | Passes |
| `new-lines` (unix), `new-line-at-end-of-file`, `trailing-spaces` | ruamel emitter guarantees all three | errors | Passes |
| `key-duplicates` | ruamel `rt` loader raises `DuplicateKeyError` | error | Aligned — yamkix is even stricter (refuses the input) |

## Divergences

1. **`document-start` — yamkix is _stricter_ than relaxed.** yamkix always adds `---` (`explicit_start=True`); relaxed does not care either way (rule disabled). No conflict — but yamkix here matches the **default** preset's opinion (warning if missing), not relaxed's indifference.

2. **`line-length` — the main real gap.** relaxed still warns at **80 characters** (softened by `allow-non-breakable-inline-mappings: true`). yamkix uses `line_width=2048`, i.e. it deliberately _never wraps_ — and it will not shorten long input lines either. yamkix output can freely trigger `line-length` warnings under relaxed. (Warning-level only, so `yamllint -d relaxed` still exits 0 unless `--strict` is used.) See [Can yamkix wrap long lines itself?](#can-yamkix-wrap-long-lines-itself) below before reaching for `--line-width`.

3. **`empty-lines` — unenforced by yamkix.** relaxed warns above 2 consecutive blank lines (`max: 2`, `max-start/end: 0`). ruamel's round-trip preserves blank-line runs attached to comments, so yamkix can pass through more than 2 blank lines untouched.

4. **`indent-sequences` philosophy.** relaxed merely requires _consistency_ (indented dashes or not — pick one). yamkix's `dash_inwards` actively **normalizes** to indented dashes (`offset=2`). The output is compatible, but yamkix imposes one of the two styles relaxed would accept — closer to yamllint default's `indent-sequences: true`.

5. **Scope difference.** yamkix normalizes things yamllint never even looks at in relaxed mode: it round-trips through a parser (so it _rejects_ invalid YAML outright, where yamllint reports syntax errors), and it can rewrite quote styles or flow style on demand.

## Can yamkix wrap long lines itself?

In theory, yes: the `-w/--line-width` option sets the wrap width (default `2048`, i.e. never wrap), so `yamkix -w 80` asks the emitter to fold lines at yamllint's limit:

```console
yamkix --input file.yml --line-width 80
```

!!! note "Fold-point trailing spaces: fixed since 1.1.0"

    The underlying `ruamel.yaml` emitter leaves a **trailing space at every fold point** when it wraps plain scalars and flow collections — and `trailing-spaces` is an **error-level** rule in both the `default` and `relaxed` presets. Since yamkix 1.1.0 this artifact is stripped from the output ([issue #437](https://github.com/looztra/yamkix/issues/437)), so wrapped output no longer trips `trailing-spaces`.

    Remaining caveats before reaching for `--line-width 80`: folded flow collections can trip the `indentation` rule (warning-level in relaxed), and non-breakable tokens (long URLs…) still exceed the width anyway (tolerated by yamllint thanks to `allow-non-breakable-words: true`). yamkix still ships with `line_width=2048` by default; if you prefer not to wrap, the yamllint side can be reconciled with the companion config below.

## Bottom line

yamkix default output passes `yamllint -d relaxed` cleanly except for two warning-level rules: `line-length` (lines over 80 characters, since yamkix never wraps) and potentially `empty-lines` (preserved blank-line runs). No error-level rule of the relaxed preset can be violated by yamkix output.

Interestingly, yamkix's temperament (mandatory `---`, forced dash indentation) sits closer to yamllint's **default** preset than to relaxed — it is an opinionated formatter whose output is roughly "yamllint default-compliant, minus the 80-character limit".

!!! tip "A yamllint config that exactly blesses yamkix output"

    ```yaml
    ---
    extends: relaxed
    rules:
      line-length: disable
    ```
