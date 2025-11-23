# CHECK MAIL PROTOCOL
## Where To Find Your Tasks and Messages

---

## WHEN YOU BOOT UP - CHECK THESE IN ORDER

### 1. LOCAL HUB INBOX
```
C:\Users\dwrek\LOCAL_TRINITY_HUB\inbox\
```
- Look for any .md or .json files
- These are direct tasks from other instances
- Process and move to /completed/ when done

### 2. SYNCTHING SYNC FOLDER
```
C:\Users\dwrek\.trinity\sync\
```
- Files that arrived from other computers
- Check timestamps - newest first
- Look for files addressed to your PC number

### 3. GIT PULL
```bash
cd C:\Users\dwrek\100X_DEPLOYMENT
git pull
```
- Check for new protocols in LOCAL_TRINITY_HUB/protocols/
- Check for updates to existing files
- Read any new HANDOFF reports

### 4. TRINITY MCP MESSAGES
```
Use: mcp__trinity__trinity_receive_messages
Instance ID: C1, C2, or C3
```
- Real-time messages from other instances
- Check even if inbox is empty

---

## MESSAGE LOCATIONS BY TYPE

| Message Type | Location | Check Frequency |
|-------------|----------|-----------------|
| Direct Tasks | LOCAL_TRINITY_HUB/inbox/ | Every boot |
| Broadcasts | LOCAL_TRINITY_HUB/broadcasts/ | Every boot |
| Protocol Updates | LOCAL_TRINITY_HUB/protocols/ | After git pull |
| Handoffs | LOCAL_TRINITY_HUB/reports/ | Every boot |
| Real-time | Trinity MCP | Continuous |

---

## QUICK CHECK COMMAND

Run this to see what's waiting:

```bash
echo "=== INBOX ===" && ls -la C:/Users/dwrek/LOCAL_TRINITY_HUB/inbox/
echo "=== BROADCASTS ===" && ls -la C:/Users/dwrek/LOCAL_TRINITY_HUB/broadcasts/
echo "=== RECENT REPORTS ===" && ls -lt C:/Users/dwrek/LOCAL_TRINITY_HUB/reports/ | head -5
```

---

## AFTER CHECKING MAIL

1. **Acknowledge receipt** - Update status or reply
2. **Prioritize tasks** - Critical first
3. **Start working** - Don't wait
4. **Report progress** - Update hub with WORKING report

---

## IF INBOX IS EMPTY

1. Check git pull for updates
2. Check Trinity MCP messages
3. Review current FOUNDATION.md rocks
4. Work on highest priority incomplete item
5. Or ask Commander for direction

**Never idle. Always building.**
