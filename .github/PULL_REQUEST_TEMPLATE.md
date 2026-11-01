# Pull request

## Summary

<!-- What changed, and why? Link the issue if there is one. -->

Fixes #

## How it was tested

<!-- Commands or manual checks you ran. -->

```text
python3 scripts/validate_skill.py skills/project-audit
python3 -m unittest discover -s tests -v
```

## Checklist

- [ ] One focused change, not several unrelated changes.
- [ ] The validator and unit tests pass locally.
- [ ] Installer changes are covered by `tests/test_install.py`.
- [ ] No secrets, credentials, absolute home paths, or private repository data.
- [ ] No unrelated edits or formatting-only churn.
- [ ] `CHANGELOG.md` is updated for user-visible changes.
