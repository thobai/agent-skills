# chat-router

Non-blocking Google Chat questions for agents running in Herdr panes. Sessions
register their pane and Chat thread; one daemon injects each human reply into the
right pane as a new prompt. Agent-facing instructions are in [SKILL.md](./SKILL.md)
and deliberately short — every word costs context in every session that loads it.

## Setup

One daemon per machine. launchd on macOS so it survives reboots, tmux elsewhere:

```bash
chat-router daemon install          # launchd on macOS, tmux otherwise
chat-router daemon install --tmux   # force tmux
chat-router daemon status           # flavour, process count, log path
chat-router daemon uninstall
```

`install` is idempotent: if that flavour already runs it reports
`already_running` and changes nothing, so several agents onboarding at once
cannot tear down a working daemon. `--force` reinstalls.

Config is shared with `notify-me` in `~/.config/agent-skills/env`
(`NOTIFY_ME_SPACE_ID`, `NOTIFY_ME_WEBHOOK_URL`). `chat-router` reads that file
directly, so it works in the non-interactive shells agents get.

## Inspect and clean up

```bash
chat-router list                     # sessions, panes, live/STALE
chat-router unregister --stale       # drop entries whose panes are gone
chat-router unregister --session <id>
tail -f ~/.local/state/chat-router/router.log
```

| Path | Contents |
|------|----------|
| `~/.local/state/chat-router/registry.json` | session → thread, pane, terminal id, watermark |
| `~/.local/state/chat-router/router.log` | deliveries, stale drops, poll errors |

## How it works

- **Routing** is by Chat thread. Each session owns one thread, keyed by session
  id, so replies land in the pane that asked.
- **Sender filter.** Webhook messages are BOT-sent and ignored, so an agent is
  never fed its own output. Only `HUMAN` messages route.
- **Stale targets.** The pane id *and* the terminal id captured at registration
  must both still be live. Herdr keeps a pane's id when its agent is replaced, so
  the terminal id is what proves the session still occupies the pane. On a
  mismatch the entry is dropped and a note is posted in the thread, rather than
  the message vanishing.
- **Whitespace is collapsed** in injected text: a newline in a prompt submits it
  early and would fragment the reply.
- **Unmatched threads.** A message in a thread no session owns — a retired
  session's thread, or a brand new message — is held, not delivered. The router
  replies asking who it is for and lists the five most recently active sessions.
  Answer with a name (`orchestrator`, or an unambiguous abbreviation like
  `orch`) and it binds that thread to that session, forwards everything it held,
  and confirms. Anything you wrote alongside the name is forwarded too. From
  then on the session sends and receives in that thread. An ambiguous or unknown
  name is asked again rather than guessed, and `--fallback last` restores the old
  guess-the-most-recent behaviour.
- **Markdown** is sent with `markupSyntax: MARKUP_SYNTAX_MARKDOWN`. Tables are
  wrapped in a code fence first, because Chat concatenates their cells and eats
  the following line; `---` rules are stripped, because Chat discards them.
- **Labels.** Every message is prefixed `[session · repo]` so thread previews
  identify the asking agent. `--no-label` suppresses it.
- **Duplicate routers** are safe but pointless: the registry lock serialises
  processing, so a message is delivered once. `daemon status` warns.

## Troubleshooting

| Symptom | Cause |
|---|---|
| `chat-router: command not found` | agent shell never sourced the rc file; add `~/.local/bin` to PATH. Not a dead daemon. |
| `poll error` in the log | usually transient TLS interception by a VPN or proxy. The daemon recovers on the next poll. |
| Reply never arrived | `chat-router list` shows the session STALE, or `daemon status` reports 0 processes. |

## Tests

```bash
python3 chat-router/test_format.py
```
