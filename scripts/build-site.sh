#!/usr/bin/env bash
# Build the site exactly as the publish workflow does, so a broken link fails
# here rather than on main.
set -euo pipefail

cd "$(dirname "$0")/.."
VENV="${VENV:-.venv}"

if [ ! -x "$VENV/bin/mkdocs" ]; then
  echo "Creating $VENV and installing mkdocs-material…"
  python3 -m venv "$VENV"
  "$VENV/bin/pip" install -q --upgrade pip
  "$VENV/bin/pip" install -q mkdocs-material
fi

"$VENV/bin/mkdocs" build --strict
echo "OK    site builds in strict mode."
