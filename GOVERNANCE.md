# Governance

## Maintainer

This project has a single maintainer: Engida Lishan (`@engida32`). The
maintainer reviews pull requests, merges changes, cuts releases, and handles
security reports.

## Changes go through pull requests when review helps

The maintainer may push a focused change directly to `main` when the change is
small, the checks pass, and no review is available. Larger behavior, schema,
installer, or security changes should land as a pull request with a focused
diff, a short explanation, and the checks below. A direct push still needs a
commit message that explains the change.

## Required checks

The `validate` workflow must pass before merge. It runs the skill validator and
the unit tests on Python 3.10 through 3.14, compiles the Python files, checks
the installer syntax, and runs an install smoke test.

## Versioning

Releases follow semantic versioning:

- `MAJOR` for a breaking change to documented behavior, the finding schema, or
  the installer interface.
- `MINOR` for new lenses, new reference material, or backward-compatible
  workflow changes.
- `PATCH` for fixes, documentation, and test-only changes.

## Changelog

Every user-visible change gets an entry in `CHANGELOG.md` under the appropriate
version. Keep entries short and describe the effect, not the implementation.

## Release steps

1. Confirm `main` is green in the `validate` workflow.
2. Update `CHANGELOG.md` and move unreleased notes under the new version.
3. Bump the version in the appropriate metadata if a version file exists.
4. Run the validator and tests locally.
5. Tag the release and publish release notes from the changelog.
6. Do not rewrite published history.

## Security reports

Do not discuss a vulnerability in a public issue. Use GitHub private
vulnerability reporting at
<https://github.com/engida32/project-audit-skill/security/advisories/new>.
Email to `engida32lishan@gmail.com` is the fallback. See `SECURITY.md`.

## Required repository settings

These settings are part of the governance model and must be enabled in the
GitHub repository:

- Branch protection on `main`, including a required `validate` status check and
  no force pushes.
- Private vulnerability reporting enabled, so the advisory link above works.
