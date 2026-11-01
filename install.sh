#!/usr/bin/env sh
set -eu

ROOT=$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)
NAME=project-audit
TARGET=${1:-"$HOME/.agents/skills"}

if [ ! -f "$ROOT/skills/$NAME/SKILL.md" ]; then
  printf 'error: %s not found\n' "$ROOT/skills/$NAME/SKILL.md" >&2
  exit 1
fi

mkdir -p "$TARGET"

if [ -e "$TARGET/$NAME" ]; then
  printf 'error: %s already exists\n' "$TARGET/$NAME" >&2
  printf 'Remove it first, or install to a different target.\n' >&2
  exit 1
fi

cp -R "$ROOT/skills/$NAME" "$TARGET/$NAME"
printf 'installed %s to %s\n' "$NAME" "$TARGET/$NAME"
