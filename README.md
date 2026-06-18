# agent-skills

Reusable scripts for AI agent harnesses (Kiro, Claude Code, Codex, etc.).

## Install

```bash
git clone git@github.com:thobai/agent-skills.git
cd agent-skills
./install.sh
```

This:
1. Symlinks skill binaries to `~/.local/bin/`
2. Creates `~/.config/agent-skills/env` for configuration

Then add to your `~/.zshrc`:

```bash
[[ -f ~/.config/agent-skills/env ]] && source ~/.config/agent-skills/env
```

## Configuration

Edit `~/.config/agent-skills/env`:

```bash
export NOTIFY_ME_SPACE_ID="spaces/YOUR_SPACE_ID"
export NOTIFY_ME_WEBHOOK_URL="https://chat.googleapis.com/v1/spaces/YOUR_SPACE/messages?key=...&token=..."
```

## Skills

| Skill | Binary | Description |
|-------|--------|-------------|
| [notify-me](./notify-me/) | `notify-me` | Send a Google Chat message and wait for reply |

## Adding to your agent

Copy `<skill>/SKILL.md` into your agent's skill directory, or reference it directly.
