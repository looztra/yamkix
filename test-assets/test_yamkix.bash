function diff_result_vs_expected() {
  local config=$1
  diff "$BATS_TMPDIR/result.yml" "test-assets/expected/${f_input}--${config}.yml"
}

function yamkix_no_dash_inwards() {
  local f_input=$1
  uv run yamkix \
    --input "$BATS_TEST_DIRNAME/test-assets/source/${f_input}.yml" \
    --output "$BATS_TMPDIR/result.yml" \
    --no-dash-inwards
  diff_result_vs_expected no-dash-inwards
}

function yamkix_set_dash_inwards() {
  local f_input=$1
  uv run yamkix \
    --input "$BATS_TEST_DIRNAME/test-assets/source/${f_input}.yml" \
    --output "$BATS_TMPDIR/result.yml"
  diff_result_vs_expected set-dash-inwards
}

function yamkix_default() {
  local f_input=$1
  uv run yamkix \
    --input "$BATS_TEST_DIRNAME/test-assets/source/${f_input}.yml" \
    --output "$BATS_TMPDIR/result.yml"
  diff_result_vs_expected default
}

function yamkix_no_explicit_start() {
  local f_input=$1
  uv run yamkix \
    --input "$BATS_TEST_DIRNAME/test-assets/source/${f_input}.yml" \
    --output "$BATS_TMPDIR/result.yml" \
    --no-explicit-start
  diff_result_vs_expected no-explicit-start
}

function yamkix_set_explicit_end() {
  local f_input=$1
  uv run yamkix \
    --input "$BATS_TEST_DIRNAME/test-assets/source/${f_input}.yml" \
    --output "$BATS_TMPDIR/result.yml" \
    --explicit-end
  diff_result_vs_expected set-explicit-end
}

function yamkix_no_quotes_preserved() {
  local f_input=$1
  uv run yamkix \
    --input "$BATS_TEST_DIRNAME/test-assets/source/${f_input}.yml" \
    --output "$BATS_TMPDIR/result.yml" \
    --no-quotes-preserved
  diff_result_vs_expected no-quotes-preserved
}

function yamkix_to_stdout() {
  local f_input=$1
  uv run yamkix \
    --input "$BATS_TEST_DIRNAME/test-assets/source/${f_input}.yml" \
    --output STDOUT >"$BATS_TMPDIR/result.yml"
  diff_result_vs_expected default
}

function yamkix_spaces_before_comment() {
  local f_input=$1
  local spaces_before_comment=$2
  uv run yamkix \
    --input "$BATS_TEST_DIRNAME/test-assets/source/${f_input}.yml" \
    --output "$BATS_TMPDIR/result.yml" \
    --spaces-before-comment "${spaces_before_comment}"
  diff_result_vs_expected "spaces-before-comment-${spaces_before_comment}"
}

function yamkix_spaces_before_comment_and_no_dash_inwards() {
  local f_input=$1
  local spaces_before_comment=$2
  uv run yamkix \
    --input "$BATS_TEST_DIRNAME/test-assets/source/${f_input}.yml" \
    --output "$BATS_TMPDIR/result.yml" \
    --spaces-before-comment "${spaces_before_comment}" \
    --no-dash-inwards
  diff_result_vs_expected "spaces-before-comment-${spaces_before_comment}--no-dash-inwards"
}

function yamkix_stdin() {
  local f_input=$1
  cat "$BATS_TEST_DIRNAME/test-assets/source/${f_input}.yml" | uv run yamkix
}
