#!/usr/bin/env python3
from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

NAME_RE = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")
LINK_RE = re.compile(r"\[[^\]]+\]\(([^)]+)\)")
ABSOLUTE_HOME_RE = re.compile(r"(?:/home/[A-Za-z0-9._-]+/|/Users/[A-Za-z0-9._-]+/|[A-Za-z]:\\Users\\)")
SECRET_PATTERNS = (
    re.compile(r"-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----"),
    re.compile(r"\bAKIA[0-9A-Z]{16}\b"),
    re.compile(r"\bghp_[A-Za-z0-9]{36}\b"),
    re.compile(r"\bxox[baprs]-[A-Za-z0-9-]{10,}\b"),
    re.compile(r"\bsk-[A-Za-z0-9]{32,}\b"),
)
TEXT_SUFFIXES = {".md", ".py", ".sh", ".yml", ".yaml", ".json", ".toml"}


def parse_frontmatter(text: str) -> tuple[dict[str, str] | None, str]:
    if not text.startswith("---\n"):
        return None, text
    end = text.find("\n---\n", 3)
    if end == -1:
        return None, text
    raw = text[4:end]
    body = text[end + 5 :]
    data: dict[str, str] = {}
    for line in raw.splitlines():
        if not line.strip() or line.lstrip().startswith("#"):
            continue
        if ":" not in line:
            continue
        key, value = line.split(":", 1)
        data[key.strip()] = value.strip().strip("\"'")
    return data, body


def iter_links(text: str) -> list[str]:
    return [match.group(1).strip() for match in LINK_RE.finditer(text)]


def resolve_link(target: str) -> str | None:
    if target.startswith("<") and target.endswith(">"):
        target = target[1:-1].strip()
    target = target.split("#", 1)[0].strip()
    if not target:
        return None
    if target.startswith(("http://", "https://", "mailto:")):
        return None
    return target


def validate_skill(skill_dir: Path) -> tuple[list[str], list[str]]:
    errors: list[str] = []
    warnings: list[str] = []
    skill_dir = skill_dir.resolve()
    skill_file = skill_dir / "SKILL.md"

    if not skill_dir.is_dir():
        return [f"skill directory not found: {skill_dir}"], warnings
    if not skill_file.is_file():
        return [f"missing SKILL.md: {skill_file}"], warnings

    text = skill_file.read_text(encoding="utf-8")
    frontmatter, body = parse_frontmatter(text)
    if frontmatter is None:
        errors.append("SKILL.md must start with YAML frontmatter delimited by ---")
        frontmatter = {}

    name = frontmatter.get("name", "")
    description = frontmatter.get("description", "")

    if not name:
        errors.append("frontmatter is missing name")
    elif len(name) > 64:
        errors.append("name must be 64 characters or fewer")
    elif not NAME_RE.fullmatch(name):
        errors.append("name must use lowercase letters, numbers, and single hyphens")
    elif name != skill_dir.name:
        errors.append(f"name '{name}' must match directory name '{skill_dir.name}'")

    if not description:
        errors.append("frontmatter is missing description")
    else:
        if len(description) > 1024:
            errors.append("description must be 1024 characters or fewer")
        if not description.lower().startswith("use when"):
            errors.append("description must start with 'Use when'")

    extra = sorted(set(frontmatter) - {"name", "description"})
    if extra:
        warnings.append(f"frontmatter has extra keys: {', '.join(extra)}")

    total_lines = len(text.splitlines())
    if total_lines > 500:
        errors.append(f"SKILL.md is {total_lines} lines; keep it under 500")

    if not re.search(r"^# \S", body, re.MULTILINE):
        warnings.append("SKILL.md has no level-one title")

    for source in sorted(skill_dir.rglob("*")):
        if not source.is_file() or source.suffix not in TEXT_SUFFIXES:
            continue
        content = source.read_text(encoding="utf-8", errors="replace")
        relative_source = source.relative_to(skill_dir)

        for target in iter_links(content):
            target = resolve_link(target)
            if target is None:
                continue
            if target.startswith("/"):
                errors.append(f"{relative_source}: absolute link target {target}")
                continue
            resolved = (source.parent / target).resolve()
            try:
                resolved.relative_to(skill_dir)
            except ValueError:
                errors.append(f"{relative_source}: link escapes skill directory: {target}")
                continue
            if not resolved.exists():
                errors.append(f"{relative_source}: broken link: {target}")

        if ABSOLUTE_HOME_RE.search(content):
            errors.append(f"{relative_source}: contains an absolute home path")
        for pattern in SECRET_PATTERNS:
            if pattern.search(content):
                errors.append(f"{relative_source}: contains a possible secret")
                break

    return errors, warnings


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Validate an Agent Skill directory.")
    parser.add_argument(
        "path",
        nargs="?",
        default="skills/project-audit",
        help="path to the skill directory",
    )
    args = parser.parse_args(argv)

    errors, warnings = validate_skill(Path(args.path))
    for warning in warnings:
        print(f"WARN  {warning}")
    for error in errors:
        print(f"ERROR {error}")

    if errors:
        print(f"FAIL  {args.path}: {len(errors)} error(s), {len(warnings)} warning(s)")
        return 1

    print(f"OK    {args.path}: 0 errors, {len(warnings)} warning(s)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
