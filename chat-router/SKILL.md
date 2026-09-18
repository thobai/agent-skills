---
name: chat-router
version: 1.1.0
description: "Ask Thomas something in Google Chat without blocking. His reply arrives as a new prompt in this pane."
metadata:
  requires:
    bins:
      - chat-notify
      - herdr
---

# chat-router

```bash
chat-notify --session apm-123 "Batch or stream? (A/B) Batch is ~2h and reuses the existing job; stream needs a new consumer."
```

Returns immediately. `"routed": true` means his reply will come back to you as a
prompt starting `[chat:<session>]` — possibly mid-turn. Never poll, and do not
use `notify-me`, which blocks your turn until he answers.

`--session` is a ticket, branch or task name and owns one Chat thread. Reuse the
same id to answer him there — he reads Chat, not your terminal.

Write Markdown; it renders. Tables and `---` are fixed up for you, and every
heading level renders the same, as bold.

Send only when the answer is not in the code, the steering files or an approved
plan. Be decidable ("A or B, here is the trade-off") and keep it to four lines —
he is reading on a phone. No history, no recap of what you have done, no
explanation he did not ask for: the decision and what it hinges on, nothing else.

Needs a Herdr pane; outside Herdr use `notify-me`. If `chat-notify` is not
found, `export PATH="$HOME/.local/bin:$PATH"` — that is a PATH problem, not a
dead daemon. Never install, start or stop the daemon: if `chat-router daemon
status` reports 0 processes, tell Thomas and carry on without a round trip.

Operators: see [README](./README.md).
