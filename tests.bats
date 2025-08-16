#!/usr/bin/env bats
setup() {
  load 'test-assets/test_yamkix'
  load 'toolbox/bats-libs/bats-support/load'
  load 'toolbox/bats-libs/bats-assert/load'
}

# bats test_tags=output:stdout
@test "check that output to stdout is not f* by a debug print statement that should not be there" {
  yamkix_to_stdout no-start-no-end
}

# bats test_tags=input:stdin
@test "can read input from STDIN when --input is not specified" {
  bats_require_minimum_version 1.5.0
  run --separate-stderr yamkix_stdin_default simple
  [ "$status" -eq 0 ]
  assert_stderr --partial "input=STDIN"
  assert_stderr --partial "output=STDOUT"
  assert_output --stdin <<EOF
---
toto: foo
titi:
  - bar
  - quix
tutu:
  yolo: baz
EOF
}

# bats test_tags=input:stdin
@test "can read input from STDIN when --input is specified" {
  bats_require_minimum_version 1.5.0
  run --separate-stderr yamkix_stdin_dash_input simple
  [ "$status" -eq 0 ]
  assert_stderr --partial "input=STDIN"
  assert_stderr --partial "output=STDOUT"
  assert_output --stdin <<EOF
---
toto: foo
titi:
  - bar
  - quix
tutu:
  yolo: baz
EOF
}

# bats test_tags=input:stdin
@test "can read input from STDIN when --input is specified and no stderr because silent mode" {
  bats_require_minimum_version 1.5.0
  run --separate-stderr yamkix_stdin_dash_input_silent_mode simple
  [ "$status" -eq 0 ]
  refute_stderr --partial "input=STDIN"
  assert_output --stdin <<EOF
---
toto: foo
titi:
  - bar
  - quix
tutu:
  yolo: baz
EOF
}
