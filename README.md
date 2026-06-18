# agent-skills

Reusable scripts for AI agent harnesses (Kiro, Claude Code, Codex, etc.).

## Install

```bash
git clone git@github.com:thobai/agent-skills.git
cd agent-skills
./install.sh
```

This symlinks all skill binaries to `~/.local/bin/`. Ensure `~/.local/bin` is on your `$PATH`.

## Skills

| Skill | Binary | Description |
|-------|--------|-------------|
| [notify-me](./notify-me/) | `notify-me` | Send a Google Chat message and wait for reply |

## Adding to your agent

Copy `notify-me/SKILL.md` into your agent's skill directory (e.g., `~/.kiro/skills/notify-me/SKILL.md`), or reference it directly.
