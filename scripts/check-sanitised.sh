#!/usr/bin/env bash
# Fails if anything publishable contains a denylisted term or a drafting-only block.
# The denylist is confidential and is never committed. See CLAUDE.md.
set -uo pipefail
cd "$(dirname "$0")/.."

DENY=".sanitise-denylist"
FAIL=0
FILES=$(git ls-files '*.md' '*.yml' '*.yaml' 2>/dev/null | grep -v '^notes/' || true)
# Fall back to the working tree when nothing is committed yet.
if [ -z "$FILES" ]; then
  FILES=$(find . -path ./.git -prune -o -path ./notes -prune -o -path ./site -prune -o \
          \( -name '*.md' -o -name '*.yml' -o -name '*.yaml' \) -print | sed 's|^\./||')
fi
FILES=$(echo "$FILES" | grep -v 'sanitise-denylist' || true)

if [ ! -f "$DENY" ]; then
  echo "FAIL  no $DENY in this working copy."
  echo "      Copy .sanitise-denylist.example and fill it in. It is gitignored."
  exit 1
fi

# 1 — denylisted terms, case-insensitive, whole word where the term is a word.
while IFS= read -r term; do
  case "$term" in ''|'#'*) continue ;; esac
  hits=$(grep -rniE "(^|[^a-z0-9])${term}([^a-z0-9]|$)" $FILES 2>/dev/null || true)
  if [ -n "$hits" ]; then
    echo "FAIL  denylisted term: $term"
    echo "$hits" | sed 's/^/      /'
    FAIL=1
  fi
done < "$DENY"

# 2 — drafting-only blocks must not survive into a publish.
hits=$(grep -rn "DRAFTING ONLY" $FILES 2>/dev/null || true)
if [ -n "$hits" ]; then
  echo "WARN  drafting-only blocks still present (fine while drafting, not for publish):"
  echo "$hits" | sed 's/^/      /'
  [ "${STRICT:-0}" = "1" ] && FAIL=1
fi

# 3 — private repository paths that commonly leak.
hits=$(grep -rnE "/Users/|projects/clients/|\.claude/worktrees/" $FILES 2>/dev/null || true)
if [ -n "$hits" ]; then
  echo "FAIL  absolute or client-tree path:"
  echo "$hits" | sed 's/^/      /'
  FAIL=1
fi

[ "$FAIL" = "0" ] && echo "OK    nothing denylisted in publishable files."
exit $FAIL
