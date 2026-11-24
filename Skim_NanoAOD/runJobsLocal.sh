#!/usr/bin/env bash
# Resolve paths independently of the caller's working directory.
set -euo pipefail
skim_dir=$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)
exec python3 "$skim_dir/runJobsLocal.py" "$@"
