#!/usr/bin/env bash

YAMKIX_VERSION=$1
while true; do
  date
  pip install "yamkix==${YAMKIX_VERSION}" || true
  if hash yamkix; then
    echo "Found expected version, let's go on"
    break
  else
    echo "Did not find the expected version [${YAMKIX_VERSION}], sleeping 15s"
    sleep 15s
  fi
done
