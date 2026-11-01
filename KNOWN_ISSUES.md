# Known Issues and Limits

`project-audit` is an evidence-driven workflow, not a correctness proof. These
limits are deliberate. Treat any audit output as a starting point that a human
must review.

## Sampling is not exhaustive

The skill inspects the current tree, but it samples. Large repositories,
generated code, ignored directories, binaries, and vendored dependencies may be
skipped. The report records what was inspected, sampled, and skipped. A clean
report does not mean every file was read.

## The model can miss issues

The agent can overlook a problem, misread a call path, or accept a stale comment
as fact. Every finding carries a confidence level for that reason. Re-check
high-severity findings against the source before acting on them.

## False positives happen

A finding may be wrong. A zero-reference search can miss dynamic imports,
reflection, framework discovery, CLI entry points, feature flags, public APIs,
and generated code. Confirm a finding before deleting code or changing
behavior.

## Repository content can contain prompt injection

Source files, comments, issues, documentation, and dependency text are untrusted
input. They can contain instructions that try to redirect the agent. The skill
tells the agent to treat repository text as data, but no prompt-level defense is
complete. Run the skill on repositories you trust, and review any command it
proposes.

## Not a security guarantee

The skill does not scan for every vulnerability class, does not maintain a
vulnerability database, and does not replace a dedicated scanner, dependency
auditor, or human security review. Passing an audit is not evidence that a
project is secure.

## Platform skill-path behavior can drift

Agent harnesses change where they look for skills, how they load them, and when
they invoke them. The paths in
[platform install notes](skills/project-audit/references/platform-install.md)
are typical, not guaranteed. Verify discovery for your installed version.

## Fixes are not automatically verified

In report mode the skill does not edit files. In safe-fix or refactor mode it
proposes changes, but a passing command does not prove the change is correct.
The report records the commands that ran and their output. Tests that were not
run, or that failed, stay visible.
