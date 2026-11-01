#!/usr/bin/env sh
set -eu

ROOT=$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)
NAME=project-audit
DEFAULT_TARGET="$HOME/.agents/skills"

usage() {
  cat <<'EOF'
Usage: sh install.sh [OPTIONS] [TARGET]

Install the project-audit skill into TARGET.

Options:
  --force       Back up an existing install and replace it.
  --uninstall   Remove TARGET/project-audit if it contains SKILL.md.
  --help, -h    Show this help and exit.

TARGET defaults to $HOME/.agents/skills.
EOF
}

FORCE=0
UNINSTALL=0
TARGET=

while [ "$#" -gt 0 ]; do
  case "$1" in
    --help|-h)
      usage
      exit 0
      ;;
    --force)
      FORCE=1
      ;;
    --uninstall)
      UNINSTALL=1
      ;;
    --)
      shift
      break
      ;;
    -*)
      printf 'error: unknown option: %s\n' "$1" >&2
      printf "Try 'sh install.sh --help'.\n" >&2
      exit 2
      ;;
    *)
      if [ -n "$TARGET" ]; then
        printf 'error: unexpected argument: %s\n' "$1" >&2
        printf "Try 'sh install.sh --help'.\n" >&2
        exit 2
      fi
      TARGET=$1
      ;;
  esac
  shift
done

if [ "$#" -gt 0 ]; then
  if [ -n "$TARGET" ] || [ "$#" -gt 1 ]; then
    printf 'error: unexpected argument: %s\n' "$1" >&2
    printf "Try 'sh install.sh --help'.\n" >&2
    exit 2
  fi
  TARGET=$1
fi

[ -n "$TARGET" ] || TARGET=$DEFAULT_TARGET
DEST="$TARGET/$NAME"

if [ "$UNINSTALL" -eq 1 ]; then
  if [ ! -e "$DEST" ]; then
    printf 'error: %s is not installed\n' "$DEST" >&2
    exit 1
  fi
  if [ ! -d "$DEST" ] || [ ! -f "$DEST/SKILL.md" ]; then
    printf 'error: refusing to remove %s: no SKILL.md found\n' "$DEST" >&2
    exit 1
  fi
  rm -rf "$DEST"
  printf 'removed %s\n' "$DEST"
  exit 0
fi

if [ ! -f "$ROOT/skills/$NAME/SKILL.md" ]; then
  printf 'error: %s not found\n' "$ROOT/skills/$NAME/SKILL.md" >&2
  exit 1
fi

mkdir -p "$TARGET"

if [ -e "$DEST" ]; then
  if [ "$FORCE" -ne 1 ]; then
    printf 'error: %s already exists\n' "$DEST" >&2
    printf 'Remove it first, use --force to back it up and replace it, or install to a different target.\n' >&2
    exit 1
  fi
  BACKUP="$DEST.bak.$(date +%Y%m%d%H%M%S)"
  mv "$DEST" "$BACKUP"
  printf 'backed up existing install to %s\n' "$BACKUP"
fi

cp -R "$ROOT/skills/$NAME" "$DEST"
printf 'installed %s to %s\n' "$NAME" "$DEST"
