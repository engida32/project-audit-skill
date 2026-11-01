# Project Audit Skill

A portable Agent Skill for evidence-based repository audits, prioritized
remediation plans, and staged refactoring.

A generic "audit this repo" prompt can produce a long list of advice without
showing its work. This skill forces the agent to work from the current tree,
cite evidence, separate findings from guesses, and stop before making risky
changes.

## What it does

- Audits architecture, code quality, dead code, complexity, dependencies,
  security, performance, tests, documentation, repository hygiene, operations,
  release readiness, and frontend accessibility when applicable.
- Defaults to report-and-plan. It does not edit files until you approve a
  finding, a stage, or a plan.
- Produces findings with severity, confidence, location, evidence, impact,
  recommended fix, risk, validation, and effort.
- Supports a safe-fix mode for behavior-preserving changes and a refactor mode
  for approved structural work.
- Includes safety gates for secrets, destructive commands, history rewrites,
  breaking API or schema changes, and publishing.
- Ships with a validator and tests so the skill stays portable and free of
  private paths or obvious secrets.

## What it does not do

- It is not a replacement for a human security review or a dedicated scanner.
- It is not permission to rewrite Git history, delete user data, or publish a
  project.
- It does not guarantee that every path was inspected. The report records what
  was sampled and what was skipped.
- It is not an automatic refactor bot. The default output is a report and a
  plan.

## Install

The installable unit is `skills/project-audit/`. Copy it into the skills
directory your agent reads.

```sh
mkdir -p "$HOME/.agents/skills"
cp -R skills/project-audit "$HOME/.agents/skills/"
```

Or use the installer, which refuses to overwrite an existing copy:

```sh
sh install.sh
sh install.sh "$HOME/.config/opencode/skills"
sh install.sh .agents/skills
```

For a project-local install, commit `.agents/skills/project-audit/` so the whole
team gets the same instructions.

Common paths include `~/.agents/skills/`, `~/.claude/skills/`,
`~/.config/opencode/skills/`, and `.agents/skills/`. Discovery and invocation
differ between agents. See
[platform install notes](skills/project-audit/references/platform-install.md)
and verify the path for your installed version.

## Usage

Report-only audit:

```text
Use project-audit in report mode on this repository. Do not edit files.
Return the findings table and a staged fix plan with evidence.
```

Dependency and security review:

```text
Use project-audit to review the dependency and security posture of this repo.
Report only, then propose a safe-fix plan for P1 findings.
```

Open-source readiness:

```text
Use project-audit to prepare this project for open source. Check docs, license,
CI, repository hygiene, and release readiness. Do not publish anything.
```

Approved safe fixes:

```text
Apply the approved P2 findings from AUD-004 and AUD-007. Use safe-fix mode.
Keep one logical change per commit and run the focused tests after each.
```

## How it works

```mermaid
flowchart LR
  A[Scope and baseline] --> B[Discovery]
  B --> C[Audit]
  C --> D[Report and plan]
  D --> E{Approved?}
  E -- no --> D
  E -- yes --> F[Implement in stages]
  F --> G[Verify]
  G --> H[Final report]
```

The skill starts with the repository state, the toolchain, and the commands the
project actually uses. It then applies the audit lenses that fit the project and
records findings with current-tree evidence. The fix plan is separate from the
findings so you can approve work in stages.

## Repository structure

```text
.
├── skills/project-audit/
│   ├── SKILL.md
│   └── references/
│       ├── audit-playbook.md
│       ├── findings-and-severity.md
│       ├── platform-install.md
│       └── report-template.md
├── scripts/validate_skill.py
├── tests/test_validate_skill.py
├── docs/design-notes.md
├── install.sh
├── README.md
├── CONTRIBUTING.md
├── SECURITY.md
├── CHANGELOG.md
└── LICENSE
```

## Design principles

- Evidence before assertion. A finding needs a location, a mechanism, and a
  way to confirm it.
- Report before edit. The default mode is read-only.
- Simple before clever. A refactor needs a measurable benefit.
- Verify before claiming. A test result needs the command and the output.
- Safety before speed. Secrets, user data, published history, and breaking
  changes are approval gates.

See [design notes](docs/design-notes.md) for the review of the original prompt
and the reasoning behind these choices.

## Validation

The validator checks frontmatter, name and description rules, line count,
relative links, absolute home paths, and obvious secret patterns.

```sh
python3 scripts/validate_skill.py skills/project-audit
python3 -m unittest discover -s tests -v
```

Python 3.10 or newer is required for the validator.

## Contributing

Read [CONTRIBUTING.md](CONTRIBUTING.md). Keep changes focused, run the validator
and tests, and do not include private paths or secrets.

## Security

Read [SECURITY.md](SECURITY.md). Report unsafe guidance privately if it could
cause data loss or secret exposure.

## License

MIT. See [LICENSE](LICENSE).

## Author

Engida <engida32lishan@gmail.com>
