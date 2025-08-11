#!/usr/bin/env bash

# Exit on error. Append "|| true" if you expect an error.
set -o errexit

# Exit on error inside any functions or subshells.
set -o errtrace

# Do not allow use of undefined vars. Use ${VAR:-} to use an undefined VAR
set -o nounset

# Catch the error in case mysqldump fails (but gzip succeeds) in `mysqldump |gzip`
set -o pipefail

# Turn on traces, useful while debugging but commented out by default
# set -o xtrace

# Set magic variables for current file, directory, os, etc.
__dir="$(cd "$(dirname "${BASH_SOURCE[${__b3bp_tmp_source_idx:-0}]}")" && pwd)"
__file="${__dir}/$(basename "${BASH_SOURCE[${__b3bp_tmp_source_idx:-0}]}")"
__base="$(basename "${__file}" .sh)"

for yaml_file in "$@"; do
  yamkix --no-quotes-preserved --input "$yaml_file"
done
