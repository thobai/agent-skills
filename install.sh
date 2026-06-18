#!/bin/bash
set -e

# Symlink skill binaries to ~/.local/bin
mkdir -p ~/.local/bin
for skill in */bin/*; do
  ln -sf "$(pwd)/$skill" ~/.local/bin/$(basename "$skill")
  echo "  ✓ $(basename "$skill") → ~/.local/bin/$(basename "$skill")"
done

# Create config file if it doesn't exist
CONFIG_DIR="${XDG_CONFIG_HOME:-$HOME/.config}/agent-skills"
CONFIG_FILE="$CONFIG_DIR/env"
if [ ! -f "$CONFIG_FILE" ]; then
  mkdir -p "$CONFIG_DIR"
  cat > "$CONFIG_FILE" << 'ENVEOF'
# agent-skills configuration
# export NOTIFY_ME_SPACE_ID="spaces/YOUR_SPACE_ID"
# export NOTIFY_ME_WEBHOOK_URL="https://chat.googleapis.com/v1/spaces/..."
ENVEOF
  echo ""
  echo "  ⚠  Created $CONFIG_FILE — edit it with your values."
fi

echo ""
echo "Done! Next steps:"
echo ""
echo "  1. Add to your shell rc (~/.zshrc):"
echo "     [[ -f ~/.config/agent-skills/env ]] && source ~/.config/agent-skills/env"
echo ""
echo "  2. Edit ~/.config/agent-skills/env with your Google Chat space and webhook URL"
echo ""
echo "  3. Ensure ~/.local/bin is on your PATH"
