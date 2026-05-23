#!/usr/bin/env bash
# Template wrapper for the main setup script.
# The runnable version lives at the repo root:
#   ../hermes-discord-team-setup.sh

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
exec "$SCRIPT_DIR/../hermes-discord-team-setup.sh" "$@"
