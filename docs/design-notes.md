# Design Notes

This repository turns a long project-audit prompt into a portable Agent Skill.
The goal is not to preserve every sentence. The goal is to make the workflow
reliable for a fresh agent and safe for a real repository.

## What we kept

- Full-repository scope across architecture, code quality, complexity,
  dependencies, security, performance, tests, documentation, repository
  hygiene, and release readiness.
- The instruction to implement improvements, not only report them.
- The final report and the priority levels P0 through P3.
- The rule that secrets, user data, published history, and licensing are
  approval gates.

## What we changed

1. **Report-first default.** The original prompt says to implement directly,
   then lists approval gates. The skill resolves that tension with explicit
   modes: `report`, `safe-fix`, and `refactor`. Audit is not permission to
   rewrite.
2. **Evidence schema.** Every finding now needs a location, a mechanism, and a
   way to confirm it. Confidence is separate from severity. Hunches go in open
   questions, not the findings table.
3. **Baseline before judgment.** The skill records the commit, dirty tree,
   toolchain, and the commands the project actually uses. A red baseline is
   evidence, not permission to fix unrelated failures.
4. **Dead-code method.** The skill lists the paths that make a zero-reference
   search unreliable: dynamic imports, reflection, framework discovery, CLI
   commands, feature flags, public APIs, and generated code.
5. **Complexity without provenance.** The original "AI slop" section is useful
   as a set of symptoms, but provenance is not evidence. The skill judges
   behavior, cost, and fit. It removes a layer only when a test or measurement
   supports the change.
6. **Dependency method.** The skill names package-manager commands, requires
   lockfile consistency, and forbids blanket forced upgrades. It separates
   security fixes from routine upgrades.
7. **Security reporting.** The skill never prints a secret. It recommends
   rotation before history cleanup. It builds a small threat model from entry
   points and trust boundaries.
8. **Performance method.** Measure, change one thing, re-measure. No speculative
   micro-optimization. Record the environment and input.
9. **Test quality.** Running tests is not enough. The skill checks for tests
   that assert nothing, snapshot abuse, flakiness, order dependence, and missing
   failure paths.
10. **Adaptive documentation.** The original 22-section README list is a menu,
    not a mandate. The skill requires the sections that fit the project and
    verifies the commands.
11. **Coverage record.** The report states what was inspected, sampled,
    excluded, and not checked. It does not claim completeness it cannot prove.
12. **Validation.** The skill ships with a validator and tests for frontmatter,
    links, size, private paths, and obvious secrets.
13. **Operations and accessibility.** Added deployment, observability, and
    frontend accessibility lenses when the repository needs them.

## What we deliberately did not do

- Did not make a 22-section README mandatory for every repository.
- Did not allow automatic history rewriting or force-pushing.
- Did not treat "AI-generated" as evidence for deletion.
- Did not add a dependency scanner or a vulnerability database. The skill uses
  the project's existing tools and records what was run.
- Did not promise equal feature depth across agents. Discovery and invocation
  differ.

## Open questions

- Should a future version add a machine-readable findings JSON schema?
- Should the validator check platform-specific metadata files?
- Should the repository include a small fixture repository and a sample report?
