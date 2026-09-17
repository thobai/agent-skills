---
name: chat-router
version: 1.0.0
description: "Ask Thomas a question in Google Chat without blocking. His reply is injected back into this pane as a new prompt by a background router."
metadata:
  requires:
    bins:
      - chat-notify
      - chat-router
      - herdr
      - gws
      - jq
---

# chat-router

Send a question to Thomas in Google Chat and **end your turn**. You do not poll
and you do not wait. A background daemon watches the Chat space and injects his
reply into this pane as a new prompt.

Use this instead of `notify-me`, whose wait loop blocks your turn for as long as
Thomas takes to answer.

Requires a Herdr pane (`HERDR_ENV=1`). Outside Herdr there is nowhere to inject
a reply — use `notify-me` there.

## Ask a question

```bash
chat-notify --session <session-id> "Batch or stream? (A/B) Batch is ~2h and reuses
the existing job; stream needs a new consumer."
```

Pick a stable, meaningful `--session` (ticket id, branch, or task name). It owns
one Chat thread, so a session's whole conversation stays in one place and Thomas
can run many sessions without cross-talk. Omitting `--session` falls back to the
Herdr agent name, then the pane id.

The call returns immediately:

```json
{"session":"apm-123","thread":"spaces/.../threads/X","target":"wJ:p37","routed":true}
```

`routed: true` means the reply will come back. Then, in the same turn:

1. State plainly which decision is parked and that you are waiting.
2. Stop. Do not start unrelated work that the answer might invalidate.

His reply arrives later as a prompt beginning `[chat-router] Thomas replied in
Google Chat (session <id>)`. Treat it as his direct answer and continue.

## Answer him back

When he asks something rather than answers, reply in the same thread:

```bash
chat-notify --session <session-id> "Done — MR !5968 is up."
```

He is reading Chat, not your terminal, so an answer that only appears in the
terminal never reaches him.

## Message rules

- Be decidable: "A or B, here's the trade-off", not "what should I do?"
- Include what you already tried and what you need to proceed.
- Four lines maximum. He is reading on a phone.
- Only send when the answer is not in the codebase, the steering files, or the
  approved plan.

## The daemon

One per machine. Install it once — launchd on macOS so it survives reboots,
tmux elsewhere:

```bash
chat-router daemon install          # launchd on macOS, tmux otherwise
chat-router daemon install --tmux   # force tmux
chat-router daemon status           # running? how many? where are the logs?
chat-router daemon uninstall
tail -f ~/.local/state/chat-router/router.log
```

`install` retires the other flavour first, so you cannot end up with two
supervisors. If the daemon is down, `chat-notify` still delivers the message to
Chat, but no reply comes back — `daemon status` says so explicitly.

## Inspecting and cleaning up

```bash
chat-router list                     # sessions, target panes, live/STALE
chat-router unregister --stale       # drop entries whose panes are gone
chat-router unregister --session <id>
```

## Behaviour worth knowing

- **Sender filter.** Messages posted by the webhook are BOT-sent and ignored, so
  an agent is never fed its own output.
- **Stale targets.** A pane id plus the terminal id captured at registration must
  both still be live. Herdr keeps a pane's id when its agent is replaced, so the
  terminal id is what proves the session still occupies the pane. On a mismatch
  the entry is dropped and a note is posted in the thread — the message is not
  silently lost.
- **Whitespace is collapsed** in injected text, because a newline in a prompt
  submits it early and would split his reply into fragments.
- **Unthreaded messages** (Thomas starts a new Chat message instead of replying)
  go to the most recently active session. Run the daemon with `--fallback none`
  to drop them instead.
- **Mid-turn arrival.** A reply that arrives while you are working is surfaced by
  kiro-cli as live steering, so it can interrupt the current turn rather than
  waiting for it to end. Act on it in the turn you are in.
- **Every message is labelled** `[session · repo]`, which is what identifies the
  asking agent in Chat's thread previews. Pass `--no-label` to suppress it.

## State

| Path | Contents |
|------|----------|
| `~/.local/state/chat-router/registry.json` | session → thread, pane, terminal id, watermark |
| `~/.local/state/chat-router/router.log` | deliveries, stale drops, poll errors |

## Configuration

Shares `notify-me`'s config in `~/.config/agent-skills/env`:

```bash
export NOTIFY_ME_SPACE_ID="spaces/..."
export NOTIFY_ME_WEBHOOK_URL="https://chat.googleapis.com/v1/spaces/..."
```

`chat-router` reads that file directly, so it works in the non-interactive
shells agents run in.
