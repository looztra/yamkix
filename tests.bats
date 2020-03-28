#!/usr/bin/env bats

load test-assets/test_yamkix

@test "dash at col0-1, no dash inwards" {
  yamkix_no_dash_inwards dash-at-col0-1
}

@test "dash at col2-1, no dash inwards" {
  yamkix_no_dash_inwards dash-at-col2-1
}

@test "multi-doc1, no dash inwards" {
  yamkix_no_dash_inwards multi-doc-1
}

@test "dash at col0-1, set dash inwards" {
  yamkix_set_dash_inwards dash-at-col0-1
}

@test "dash at col2-1, set dash inwards" {
  yamkix_set_dash_inwards dash-at-col2-1
}

@test "multi-doc1, set dash inwards" {
  yamkix_set_dash_inwards multi-doc-1
}

@test "no-start-no-end, default" {
  yamkix_default no-start-no-end
}

@test "no-start-no-end, no explicit start" {
  yamkix_no_explicit_start no-start-no-end
}

@test "no-start-no-end, set explicit end" {
  yamkix_set_explicit_end no-start-no-end
}

@test "no-start-no-end, no-quotes-preserved" {
  yamkix_no_quotes_preserved no-start-no-end
}

@test "check that output to stdout is not f* by a debug print statement that should not be there" {
  yamkix_to_stdout no-start-no-end
}
