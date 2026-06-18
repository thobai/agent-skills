#!/bin/bash
SPACE_ID="spaces/AAQAfory95M"
WEBHOOK_BASE="https://chat.googleapis.com/v1/spaces/AAQAfory95M/messages?key=AIzaSyDdI0hCZtE6vySjMm-WEfRq3CPzqKqqsHI&token=iP53TkIEggc8_iqQTMOYj1OmrugWL8Vgm79hxAUB6PQ"
WEBHOOK_REPLY="${WEBHOOK_BASE}&messageReplyOption=REPLY_MESSAGE_FALLBACK_TO_NEW_THREAD"

poll_for_reply() {
  local THREAD_NAME="$1" LAST_KNOWN="$2"
  local POLL_PARAMS=$(jq -n --arg parent "$SPACE_ID" --arg filter "thread.name = \"$THREAD_NAME\"" \
    '{parent: $parent, filter: $filter}')
  echo "Waiting for reply..." >&2
  while true; do
    sleep 5
    LATEST=$(gws chat spaces messages list --params "$POLL_PARAMS" 2>/dev/null | jq -r '.messages[-1]')
    LATEST_ID=$(echo "$LATEST" | jq -r '.name')
    if [ "$LATEST_ID" != "$LAST_KNOWN" ] && [ "$LATEST_ID" != "null" ]; then
      jq -n --arg thread "$THREAD_NAME" --arg reply "$(echo "$LATEST" | jq -r '.text')" --arg message_id "$LATEST_ID" \
        '{thread: $thread, reply: $reply, message_id: $message_id}'
      break
    fi
  done
}

if [ "$1" == "--reply" ]; then
  THREAD_NAME="$2"; MESSAGE="$3"
  curl -s -X POST "$WEBHOOK_REPLY" \
    -H "Content-Type: application/json" \
    -d "$(jq -n --arg text "$MESSAGE" --arg thread "$THREAD_NAME" \
      '{text: $text, thread: {name: $thread}}')" | jq '{thread: .thread.name, message_id: .name}'
  exit 0
fi

if [ "$1" == "--reply-wait" ]; then
  THREAD_NAME="$2"; MESSAGE="$3"
  SENT=$(curl -s -X POST "$WEBHOOK_REPLY" \
    -H "Content-Type: application/json" \
    -d "$(jq -n --arg text "$MESSAGE" --arg thread "$THREAD_NAME" \
      '{text: $text, thread: {name: $thread}}')")
  SENT_ID=$(echo "$SENT" | jq -r '.name')
  poll_for_reply "$THREAD_NAME" "$SENT_ID"
  exit 0
fi

if [ "$1" == "--wait" ]; then
  poll_for_reply "$2" "$3"
  exit 0
fi

# Default: new message + wait for reply
MESSAGE="${1:-Agent standing by. Please reply in this thread.}"
SENT=$(curl -s -X POST "$WEBHOOK_BASE" \
  -H "Content-Type: application/json" \
  -d "$(jq -n --arg text "$MESSAGE" '{text: $text}')")

THREAD_NAME=$(echo "$SENT" | jq -r '.thread.name')
SENT_MESSAGE_ID=$(echo "$SENT" | jq -r '.name')

if [ -z "$THREAD_NAME" ] || [ "$THREAD_NAME" == "null" ]; then
  echo '{"error": "Failed to send message"}' >&2
  exit 1
fi

poll_for_reply "$THREAD_NAME" "$SENT_MESSAGE_ID"
