# Changelog

All notable changes to this project are documented here.

## [Unreleased]

### Added

- Resume and adopt an existing audit artifact before starting a new pass.
- Independent verification for P0 and P1 findings, with a `single-pass`
  fallback.
- Manual behavioral test scenarios and a small eval fixture with expected
  findings.
- Installer `--help`, `--force`, and `--uninstall` options with tests.
- CodeQL, Dependabot, issue and pull request templates, CODEOWNERS, governance,
  code of conduct, known issues, example report, and agent prompts.
- Cross-link with `agent-workflow-kit` for approved remediation.

### Changed

- CI now runs the validator and tests on Python 3.10 through 3.14, checks
  installer syntax, and runs an install smoke test.
- README documents status, limits, maintainers, release steps, and the workflow
  kit handoff.

## [0.1.0] - 2026-11-01

### Added

- Portable `project-audit` Agent Skill with report-first workflow.
- Architecture, code quality, complexity, dependency, security, performance,
  test, documentation, repository, and release lenses.
- Finding schema with severity, confidence, evidence, fix, risk, validation,
  and effort.
- Report template with baseline, findings, changes, verification, and release
  readiness.
- Safety gates for secrets, destructive commands, history rewrites, breaking
  changes, and publishing.
- Skill validator, unit tests, installer, and GitHub Actions workflow.
- MIT license, contribution guide, and security policy.
