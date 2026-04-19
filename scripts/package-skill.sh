#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
SKILL_DIR="$ROOT_DIR/.claude/skills/youtube-downloader"
DIST_DIR="$ROOT_DIR/dist"
ZIP_PATH="$DIST_DIR/youtube-downloader-skill.zip"

if [[ ! -f "$SKILL_DIR/SKILL.md" ]]; then
  echo "SKILL.md not found at expected path: $SKILL_DIR/SKILL.md" >&2
  exit 1
fi

mkdir -p "$DIST_DIR"
rm -f "$ZIP_PATH"

(
  cd "$SKILL_DIR"
  zip -r "$ZIP_PATH" SKILL.md scripts references >/dev/null
)

echo "Created skill zip: $ZIP_PATH"
