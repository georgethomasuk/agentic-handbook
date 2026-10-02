#!/usr/bin/env bash
# Runs the kit's tests, and the kit's own check against the example plan.
# The tests build every plan they use in a temporary directory, so a fresh checkout passes.
set -euo pipefail
cd "$(dirname "$0")/../kit"

if command -v uv >/dev/null 2>&1; then
  RUN=(uv run --quiet --with 'pyyaml>=6' python)
else
  RUN=(python3)
fi

"${RUN[@]}" -m unittest test_plan

scratch="$(mktemp -d)"
trap 'rm -rf "$scratch"' EXIT
git init -q -b main "$scratch"
"${RUN[@]}" plan.py init "$scratch" --example >/dev/null
(cd "$scratch" && "${RUN[@]}" "$OLDPWD/plan.py" check)

echo "OK    the kit's tests pass, and the example plan checks clean."
