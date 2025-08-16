function diff_result_vs_expected() {
  local config=$1
  diff "$BATS_TMPDIR/result.yml" "test-assets/expected/${f_input}--${config}.yml"
}

function yamkix_to_stdout() {
  local f_input=$1
  uv run yamkix \
    --input "$BATS_TEST_DIRNAME/test-assets/source/${f_input}.yml" \
    --output STDOUT >"$BATS_TMPDIR/result.yml"
  diff_result_vs_expected default
}

function yamkix_stdin_default() {
  local f_input=$1
  cat "$BATS_TEST_DIRNAME/test-assets/source/${f_input}.yml" | uv run yamkix
}

function yamkix_stdin_dash_input() {
  local f_input=$1
  cat "$BATS_TEST_DIRNAME/test-assets/source/${f_input}.yml" | uv run yamkix --input=STDIN
}

function yamkix_stdin_dash_input_silent_mode() {
  local f_input=$1
  cat "$BATS_TEST_DIRNAME/test-assets/source/${f_input}.yml" | uv run yamkix --input=STDIN --silent
}
