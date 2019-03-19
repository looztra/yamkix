#!/usr/bin/env bash

YAMKIX_VERSION=$1
while true; do
  date
  pip install yamkix==${YAMKIX_VERSION} || true
  if hash yamkix ; then
    break
  else
    echo "Did not find the expected version [${YAMKIX_VERSION}], sleeping"
    sleep 15s
  fi
done
