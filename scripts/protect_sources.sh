#!/usr/bin/env bash
set -euo pipefail

repo_root="$(git rev-parse --show-toplevel)"
sources_dir="$repo_root/sources"

if [[ ! -f "$repo_root/config/corpus-manifest.json" ]]; then
  echo "Refusing to protect sources/: create and commit config/corpus-manifest.json first" >&2
  exit 1
fi

chmod -R a-w "$sources_dir"
echo "Removed write permissions from $sources_dir"

