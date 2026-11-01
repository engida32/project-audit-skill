# Platform Install

`project-audit` is a portable Agent Skill. The installable unit is the folder
`skills/project-audit/`, which contains `SKILL.md` and its references.

## Install by copying

Choose the skills directory your agent reads, then copy the folder into it.

```sh
mkdir -p "$HOME/.agents/skills"
cp -R skills/project-audit "$HOME/.agents/skills/"
```

For a project-local install:

```sh
mkdir -p .agents/skills
cp -R skills/project-audit .agents/skills/
```

The repository also includes an installer that refuses to overwrite an existing
copy:

```sh
sh install.sh
sh install.sh "$HOME/.config/opencode/skills"
sh install.sh .agents/skills
```

## Common paths

| Context | Typical path | Notes |
| --- | --- | --- |
| Portable user skills | `~/.agents/skills/` | Cross-agent alias used by several tools |
| Portable project skills | `.agents/skills/` | Commit this when the whole team should use it |
| Claude Code | `~/.claude/skills/` or `.claude/skills/` | Personal or project scope |
| OpenCode | `~/.config/opencode/skills/` or `.opencode/skills/` | OpenCode also reads compatibility paths |
| Cursor | `.cursor/skills/` or `.agents/skills/` | Verify global path behavior for your version |
| Codex | `~/.codex/skills/` or `.agents/skills/` | Verify the path for your installed version |

Agent discovery, permissions, and invocation differ. Check your agent's
documentation before claiming a path is supported. When in doubt, use the
portable `.agents/skills/` path.

## Verify the install

1. Start a new agent session so it reloads the skills directory.
2. Ask the agent to list its available skills, or invoke the skill by name.
3. Confirm the description matches the audit use case.
4. Run a small report-only audit on a throwaway repository.

Example prompts:

```text
Use project-audit in report mode on this repository. Do not edit files.
Return the findings table and a staged fix plan with evidence.
```

```text
Use project-audit to review the dependency and security posture of this repo.
Report only, then propose a safe-fix plan for P1 findings.
```

```text
Use project-audit to prepare this project for open source. Check docs, license,
CI, repository hygiene, and release readiness. Do not publish anything.
```

## Update

Replace the installed folder with the new version. Keep local changes outside
the skill folder, or fork the repository if you need to customize it.

## Uninstall

Remove the installed folder with your file manager, or with a verified path:

```sh
rm -r "$HOME/.agents/skills/project-audit"
```

Use the path you actually installed to. The command is destructive, so verify
the path first.
