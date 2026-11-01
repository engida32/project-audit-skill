# Findings and Severity

## Finding schema

Use one record per finding. Keep the ID stable across the report and the fix
plan.

| Field | Content |
| --- | --- |
| `id` | `AUD-001`, `AUD-002`, and so on |
| `title` | Short, specific, and searchable |
| `severity` | `P0`, `P1`, `P2`, or `P3` |
| `confidence` | `confirmed`, `likely`, or `unverified` |
| `verification` | `independent`, `single-pass`, or `not-required`; P0 and P1 require `independent` |
| `category` | Architecture, code quality, dependencies, security, performance, tests, docs, repository, release |
| `location` | `path:line`, command, or config key from the current tree |
| `evidence` | The code path, command output, measurement, or test that proves it |
| `impact` | What breaks, what it costs, or what risk it creates |
| `fix` | The smallest change that addresses the cause |
| `risk` | What could break, and how to contain it |
| `validation` | The command or test that proves the fix |
| `effort` | `S`, `M`, `L`, with a short reason |
| `dependencies` | Other findings that must land first |
| `status` | `open`, `planned`, `fixed`, `verified`, `wontfix`, `false-positive` |

## Severity

| Level | Meaning | Examples |
| --- | --- | --- |
| `P0` | Critical security, data loss, or application-breaking issue | Auth bypass, secret in a public artifact, destructive migration, crash on startup |
| `P1` | Major architecture or functional problem | Broken core workflow, data corruption risk, untested critical path, dependency with a known exploitable vulnerability |
| `P2` | Maintainability, reliability, or performance problem | Duplicate business rules, slow hot path, missing failure handling, fragile build |
| `P3` | Minor cleanup or polish | Naming, dead helper, stale comment, small doc drift |

When in doubt between two levels, choose the lower one and state the condition
that would raise it. Severity is about impact, not about how interesting the
finding is.

## Confidence

| Level | Meaning | Minimum evidence |
| --- | --- | --- |
| `confirmed` | Reproduced or read directly in the current tree | Code path plus command, test, or exact source lines |
| `likely` | Strong static evidence, not executed | Source lines and a clear mechanism |
| `unverified` | Needs a check before it can be a finding | A named command or source to inspect |

Do not put `unverified` items in the findings table as facts. Put them in "open
questions" with the check that would settle them.

## Prioritization

Order by:

1. `P0` before everything.
2. Impact and likelihood.
3. Findings that unblock other findings.
4. Effort, but only after the first three.

Prefer a small set of high-confidence findings over a long list of speculation.
If two findings have the same cause, merge them and keep one fix.

## Fix plan format

For each approved finding, write:

```text
AUD-003: Session lookup ignores expiry
Severity: P1
Confidence: confirmed
Verification: independent
Location: src/auth/session.ts:84
Cause: The lookup returns a row before checking expires_at.
Fix: Reject expired rows in the query and add a boundary test.
Risk: A clock-skew bug could reject valid sessions; use the database clock.
Validation: pnpm test -- auth/session; add a case for expires_at in the past.
Effort: S
Depends on: none
```

## Example finding

```text
AUD-001: Public build copies .env into the static bundle
Severity: P0
Confidence: confirmed
Verification: independent
Category: Security
Location: scripts/build.mjs:41
Evidence: The copy step includes every file matching .env*, and the output
  directory is served publicly. Running `npm run build` produced
  dist/.env.production.
Impact: Any secret in that file is exposed to every visitor.
Fix: Copy only an explicit allowlist of public variables, and fail the build if
  a server-only name appears in the client bundle.
Risk: A missing public variable can break the build; validate required names
  before the copy.
Validation: npm run build; inspect dist for .env*; add a test that fails when a
  server-only name is present.
Effort: S
Depends on: none
```

## Independent verification (P0 and P1)

A P0 or P1 finding is not independently verified until a second pass has checked
it. The second pass should see only:

1. The finding statement.
2. The cited file and lines.
3. The command output or reproduction.

Do not include the audit narrative, the suspected cause, or the proposed fix.
Those bias the check. The reviewer answers one question: does the evidence
support the claim at the stated severity?

If a separate reviewer or fresh context is unavailable, set
`verification: single-pass` and state that in the report's limitations. Never
describe a single-pass finding as independently verified. P2 and P3 findings use
`verification: not-required` unless you choose to check them.

## Reporting rules

- Do not include secret values. Quote the rule, path, and line only.
- Do not cite a document as proof of current behavior. Cite the tree.
- Do not claim a fix works until the validation command has run.
- If a finding is fixed, keep the record and change `status` to `fixed` or
  `verified`.
- If a finding is rejected, keep it with `status: wontfix` or `false-positive`
  and the reason.
