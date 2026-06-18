---
name: notify-me
version: 1.2.0
description: "Send a Google Chat message to the user and wait for their reply. Use when you need human input, approval, or want to notify the user of progress."
metadata:
  requires:
    bins:
      - notify-me
      - jq
      - curl
---

# notify-me

Send a message to the user via Google Chat and optionally wait for their reply. All stdout is JSON.

## Modes

### New message + wait for reply

```bash
notify-me "Your question here"
```

### Reply in existing thread (fire-and-forget)

```bash
notify-me --reply THREAD_NAME "Follow-up message"
```

### Reply + wait for response

```bash
notify-me --reply-wait THREAD_NAME "Question in existing thread"
```

### Wait for next reply (no send)

```bash
notify-me --wait THREAD_NAME LAST_MESSAGE_ID
```

## Output

All modes that wait return:
```json
{"thread": "spaces/.../threads/...", "reply": "user's text", "message_id": "spaces/.../messages/..."}
```

Fire-and-forget `--reply` returns:
```json
{"thread": "spaces/.../threads/...", "message_id": "spaces/.../messages/..."}
```

## Typical agent flow

```bash
# Start conversation
RESULT=$(notify-me "Build done. Deploy to staging? (yes/no)")
THREAD=$(echo "$RESULT" | jq -r '.thread')
REPLY=$(echo "$RESULT" | jq -r '.reply')

# Continue in same thread
RESULT=$(notify-me --reply-wait "$THREAD" "Deployed. Run tests too?")
```

## Requirements

- `gws` CLI authenticated with `chat.messages` and `chat.spaces` scopes
- `jq` and `curl` on PATH
