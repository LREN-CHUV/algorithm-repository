#!/usr/bin/env bash
set -e

if [[ $NO_SUDO || -n "$CIRCLECI" ]]; then
  CAPTAIN="captain"
elif groups $USER | grep &>/dev/null '\bdocker\b'; then
  CAPTAIN="captain"
else
  CAPTAIN="sudo captain"
fi

BUILD_DATE=$(date -Iseconds) \
  VCS_REF=$(git describe --tags --dirty) \
  VERSION=$(git describe --tags --dirty) \
  $CAPTAIN build
