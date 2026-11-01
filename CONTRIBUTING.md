# Contributing

Thanks for improving Project Audit Skill.

## Before you change the skill

1. Read `skills/project-audit/SKILL.md` and the relevant reference file.
2. Check whether the change belongs in the main skill or in a reference. Keep
   `SKILL.md` scannable.
3. If the change affects behavior, describe the failure it prevents or the
   improvement it makes.
4. Do not add private paths, hostnames, credentials, or project-specific facts.

## Local checks

```sh
python3 scripts/validate_skill.py skills/project-audit
python3 -m unittest discover -s tests -v
python3 -m py_compile scripts/validate_skill.py tests/test_validate_skill.py
```

The validator must report zero errors. Warnings need a reason in the pull
request.

## Pull requests

- Keep one logical change per pull request.
- Update `CHANGELOG.md` for user-visible changes.
- Add or update a test when the validator or repository tooling changes.
- Explain what you verified and what you could not verify.
- Do not include generated files, local settings, or secrets.

## Skill content rules

- Frontmatter has `name` and `description`. The description starts with
  "Use when" and describes triggers, not the workflow.
- The name is lowercase hyphen-case and matches the folder name.
- `SKILL.md` stays under 500 lines.
- Relative links resolve inside the skill folder.
- Examples use placeholders such as `<repo>`, not a real home directory.
- Safety gates stay explicit. Do not soften a gate to make an example shorter.

## Reporting a problem

Open an issue with the commit hash, the agent and version, the prompt, and the
observed result. Remove secrets and private repository data before posting.

For a security-sensitive report, follow `SECURITY.md`.
