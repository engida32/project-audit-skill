# Example audit report

> Illustrative only. The repository, commit, commands, and findings below are
> fake. Do not treat this as a real audit or as evidence about any project.
> Values are redacted or invented.

## A. Executive summary

`example-service` is a small Node.js API with a build step that publishes static
assets. The audit found one P0 exposure in the build output, one P1 correctness
bug in session handling, and two smaller gaps in CI and cleanup. The report-only
pass changed no files. Ship after the P0 and P1 are fixed; the P2 and P3 can
follow.

## B. Scope and baseline

| Item | Value |
| --- | --- |
| Repository | `example-service` (illustrative) |
| Commit | `abc1234` (illustrative) |
| Branch | `main` |
| Working tree | clean |
| Mode | `report` |
| Included paths | `src/`, `scripts/`, `.github/`, `package.json` |
| Excluded paths | `vendor/`, `dist/`, `node_modules/` |
| Timebox | 90 minutes |
| Target | Production readiness |

Baseline:

```text
npm ci -> exit 0
npm test -> exit 0, 42 passed
npm run lint -> exit 0
npm run typecheck -> not run, no typecheck script in package.json
npm run build -> exit 0, dist/ created
```

## C. Findings

| ID | Severity | Confidence | Verification | Category | Title | Status |
| --- | --- | --- | --- | --- | --- | --- |
| AUD-001 | P0 | confirmed | independent | Security | Build copies `.env*` into the public output | open |
| AUD-002 | P1 | confirmed | independent | Architecture | Session lookup ignores expiry | open |
| AUD-003 | P2 | confirmed | not-required | Tests | CI does not run the test suite | open |
| AUD-004 | P3 | likely | not-required | Code quality | Date helper has no caller | open |

## AUD-001: Public build copies `.env*` into the static bundle

- **Location:** `scripts/build.mjs:41`
- **Evidence:** The copy step matches every `.env*` file, and `dist/` is served
  publicly. Running `npm run build` produced `dist/.env.production`.
- **Impact:** Any secret in that file is exposed to every visitor. A real value
  would need rotation, not just deletion.
- **Fix:** Copy an explicit allowlist of public variables and fail the build when
  a server-only name appears in the client bundle.
- **Risk:** A missing public variable can break the build. Validate required
  names before the copy.
- **Validation:** `npm run build`, then inspect `dist/` for `.env*`; add a test
  that fails when a server-only name is present.
- **Effort:** S
- **Depends on:** none

## AUD-002: Session lookup ignores expiry

- **Location:** `src/auth/session.ts:84`
- **Evidence:** The query returns a session row before checking `expires_at`.
  A test with an expired fixture session still authenticated.
- **Impact:** Expired sessions remain valid, which weakens logout and token
  rotation.
- **Fix:** Reject expired rows in the query and add a boundary test.
- **Risk:** A clock-skew bug could reject valid sessions. Compare against the
  database clock.
- **Validation:** `npm test -- auth/session`; add a case with `expires_at` in the
  past.
- **Effort:** S
- **Depends on:** none

## AUD-003: CI does not run the test suite

- **Location:** `.github/workflows/ci.yml:22`
- **Evidence:** The workflow installs dependencies and runs lint, then stops.
  No step invokes `npm test`.
- **Impact:** A failing test can merge behind a green check.
- **Fix:** Add `npm test` after install and make the job required.
- **Risk:** Existing flaky tests may block merges. Fix or quarantine them first.
- **Validation:** Open a pull request with a failing test and confirm the check
  fails.
- **Effort:** S
- **Depends on:** none

## AUD-004: Date helper has no caller

- **Location:** `src/format/date.ts:12`
- **Evidence:** Search and import graph show no caller. No dynamic import,
  public export, or test references it.
- **Impact:** Minor maintenance cost.
- **Fix:** Remove it in a focused change.
- **Risk:** An external consumer may import it. Check package exports first.
- **Validation:** `npm test` and `npm run build` after removal.
- **Effort:** S
- **Depends on:** none
- **Note:** P3, so no independent check was required.

## D. Staged plan

| Stage | Findings | Change | Validation |
| --- | --- | --- | --- |
| 1 | AUD-001 | Stop copying `.env*`; allowlist public values | Build, inspect `dist/`, new bundle test |
| 2 | AUD-002 | Reject expired sessions | Auth tests, boundary case |
| 3 | AUD-003, AUD-004 | Run tests in CI; remove dead helper | Full suite, CI check |

Stage 1 first. Do not combine the build change with the auth change.

## E. Changes made

Report-only; no files changed.

## F. Final status

| Area | Status | Evidence |
| --- | --- | --- |
| Build | pass | `npm run build` -> exit 0 |
| Tests | pass | `npm test` -> exit 0, 42 passed |
| Lint | pass | `npm run lint` -> exit 0 |
| Typecheck | not run | no script in `package.json` |
| Security | issues | AUD-001 |
| Documentation | gaps | build output not documented |
| Git tree | clean | `git status --short` empty |
| Release ready | no | P0 and P1 open |

## G. Coverage and limitations

Inspected `src/`, `scripts/`, `.github/`, and `package.json`. Sampled tests.
Did not inspect `vendor/`, `dist/`, or `node_modules/`. Typecheck was not run
because the project has no script. AUD-004 is P3, so no independent check was
required. Performance was not measured.
