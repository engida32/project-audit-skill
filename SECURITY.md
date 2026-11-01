# Security Policy

## Scope

This repository contains instructions and small validation scripts. The main
security risk is guidance that could cause an agent to expose a secret, delete
data, rewrite published history, or run a destructive command.

## Reporting

Do not open a public issue for a report that includes a secret, a private
repository path, or an exploitable technique. Send a private report to:

[Send a private email](mailto:engida32lishan@gmail.com)

Include:

- The affected file and line.
- The agent and version you used.
- The prompt or sequence that triggered the behavior.
- The observed result and the expected result.
- Whether any secret or user data was exposed.

Redact secret values. Describe the rule and location instead.

## What to expect

This is a small community project. Reports are reviewed on a best-effort basis.
If a report involves a leaked credential, rotate the credential first. History
cleanup is secondary to rotation.

## Safe use

- Run the skill on a branch or a disposable copy when you are not sure.
- Review proposed commands before approving a safe-fix or refactor stage.
- Do not run the skill against production systems or production data.
- Do not paste secrets into a report, prompt, or issue.
