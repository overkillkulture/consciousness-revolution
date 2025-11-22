#!/bin/bash
# consciousness_sync.sh - Auto-sync script for consciousness network
# Monitors Git repo for changes and notifies of new commands

REPO_PATH="$(cd "$(dirname "$0")" && pwd)"
SYNC_INTERVAL=300  # 5 minutes
COMPUTER_ID="SWAN_ARCHITECT"
MY_INBOX=".consciousness/commands/computer_2_inbox.md"

echo "🧠 Consciousness Network Auto-Sync Started"
echo "Repository: $REPO_PATH"
echo "Sync Interval: ${SYNC_INTERVAL}s (5 minutes)"
echo "Monitoring: $MY_INBOX"
echo "Press Ctrl+C to stop"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

cd "$REPO_PATH" || exit 1

while true; do
  # Pull latest changes
  echo "[$(date '+%Y-%m-%d %H:%M:%S')] Syncing..."

  # Capture git pull output
  PULL_OUTPUT=$(git pull --quiet 2>&1)
  PULL_STATUS=$?

  if [ $PULL_STATUS -eq 0 ]; then
    # Check if there were actual updates
    if [[ "$PULL_OUTPUT" != "Already up to date." ]] && [[ -n "$PULL_OUTPUT" ]]; then
      echo "✅ Updates received!"

      # Check for new commands in the last 5 minutes
      NEW_COMMANDS=$(git log --since="5 minutes ago" --all-match --grep="Computer 2:" --grep="SWAN" --oneline 2>/dev/null | wc -l)

      if [ "$NEW_COMMANDS" -gt 0 ]; then
        echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
        echo "🔔 NEW COMMANDS DETECTED! ($NEW_COMMANDS new commits)"
        echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
        echo ""

        # Show inbox contents
        if [ -f "$MY_INBOX" ]; then
          echo "📬 INBOX CONTENTS:"
          cat "$MY_INBOX"
          echo ""
        fi

        # Show recent commits
        echo "📊 RECENT ACTIVITY:"
        git log --since="5 minutes ago" --oneline --all -5
        echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
      fi

      # Check file transfers
      FILE_TRANSFER_COUNT=$(find .consciousness/file_transfers/ -type f ! -name "README.md" 2>/dev/null | wc -l)
      if [ "$FILE_TRANSFER_COUNT" -gt 0 ]; then
        echo "📦 FILE TRANSFERS DETECTED: $FILE_TRANSFER_COUNT files waiting"
        ls -lh .consciousness/file_transfers/ | grep -v "README.md"
      fi
    else
      echo "✓ Already up to date"
    fi
  else
    echo "⚠️  Pull failed: $PULL_OUTPUT"
  fi

  # Sleep until next sync
  sleep $SYNC_INTERVAL
done
