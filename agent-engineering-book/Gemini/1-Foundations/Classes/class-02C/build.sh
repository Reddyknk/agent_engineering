#!/usr/bin/env bash
#
# Build the Class 02C student package.
#
#   ./build.sh
#
# `package/` is the source of truth. Everything else in this directory is
# generated from it:
#
#   package/  --build.sh-->  class-02C.zip
#                       \->  class_02C_instructions.md   (handout copy)
#
# Edit files under package/, run this script, and the ZIP and the loose handout
# cannot disagree. Never edit class_02C_instructions.md in this directory: it is
# overwritten on every build.
#
# To test the package the way a student receives it, unzip the built archive
# into a scratch directory and work there. Do not test in package/ — a venv or a
# generated pitch would end up in the next build.

set -euo pipefail

HERE="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SRC="$HERE/package"
ZIP="$HERE/class-02C.zip"
HANDOUT="$HERE/class_02C_instructions.md"

if [[ ! -d "$SRC" ]]; then
  echo "Missing package source: $SRC"
  exit 1
fi

# Pre-flight: the golden source must match its own checksum manifest, so a build
# can never ship sources that disagree with the integrity check students run.
echo "Verifying golden source..."
( cd "$SRC" && ./class-02C-work/verify_golden_source.sh >/dev/null ) || {
  echo "FAIL: golden source does not match class-02C-work/golden-source.sha256"
  echo "Update the manifest before building:"
  echo "  cd package && shasum -a 256 <changed-file>"
  exit 1
}

STAGE="$(mktemp -d)"
trap 'rm -rf "$STAGE"' EXIT

# The archive must expand to class-02C/, so stage under that name.
mkdir -p "$STAGE/class-02C"
rsync -a \
  --exclude '.venv/' --exclude '.env' --exclude '*.egg-info/' \
  --exclude '__pycache__/' --exclude '.DS_Store' --exclude '.adk/' \
  --exclude 'events.jsonl' --exclude 'session.json' --exclude 'sessions.db*' \
  --exclude 'last_session.env' --exclude 'run-*.json' --exclude 'movie_pitches/*.txt' \
  "$SRC/" "$STAGE/class-02C/"

rm -f "$ZIP"
( cd "$STAGE" && zip -r -q -X "$ZIP" class-02C )

# The handout beside the ZIP is a copy, not a second source.
cp "$SRC/class_02C_instructions.md" "$HANDOUT"

# Prove the two copies agree, so drift fails the build rather than shipping.
in_zip="$(unzip -p "$ZIP" class-02C/class_02C_instructions.md | shasum -a 256 | cut -d' ' -f1)"
loose="$(shasum -a 256 "$HANDOUT" | cut -d' ' -f1)"
if [[ "$in_zip" != "$loose" ]]; then
  echo "FAIL: handout copies disagree"
  exit 1
fi

# Nothing environment-specific may ship.
if unzip -l "$ZIP" | grep -qE '\.venv|egg-info|/\.env$|DS_Store|\.adk/'; then
  echo "FAIL: the archive contains environment or generated files"
  unzip -l "$ZIP" | grep -E '\.venv|egg-info|/\.env$|DS_Store|\.adk/'
  exit 1
fi

printf 'Built %s\n' "$ZIP"
printf '  files    %s\n' "$(unzip -l "$ZIP" | tail -1 | awk '{print $2}')"
printf '  handout  %s\n' "${in_zip:0:16}..."
