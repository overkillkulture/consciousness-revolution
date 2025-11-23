# WAKE TEST PROTOCOL - Cross-Computer Auto-Wake System

## Overview

The Auto-Wake System enables any computer in the Trinity network to wake another computer and automatically open Claude Code with a specific task.

---

## System Components

### 1. AUTO_WAKE_DAEMON.py
**Location:** `.trinity/automation/AUTO_WAKE_DAEMON.py`

**Functions:**
- Monitors git for wake signals every 30 seconds
- Detects wake signal for its PC in `.trinity/wake/`
- Opens Claude Code automatically when wake signal detected
- Archives wake signals for history
- Reports wake received status via heartbeat

### 2. Wake Signal Format
**Location:** `.trinity/wake/{PC_ID}.json`

```json
{
  "from": "PC1",
  "to": "PC2",
  "timestamp": "2025-11-23T15:45:00Z",
  "task": "process_spawn_queue",
  "message": "Work available in spawn queue",
  "working_directory": "C:\\Users\\darri\\100X_DEPLOYMENT"
}
```

### 3. Wake Archive
**Location:** `.trinity/wake_archive/`

All processed wake signals are archived with timestamps for auditing and debugging.

---

## Usage

### Option 1: Send Wake via Python Script

```bash
# Send wake to PC2
python .trinity/automation/AUTO_WAKE_DAEMON.py --send PC2 --task "process_queue" --message "New task available"

# Send wake to PC3
python .trinity/automation/AUTO_WAKE_DAEMON.py --send PC3 --task "build_system"
```

### Option 2: Send Wake via Manual File

```bash
# Create wake signal for PC2
echo '{
  "from": "PC1",
  "to": "PC2",
  "timestamp": "'$(date -Iseconds)'",
  "task": "autonomous_work",
  "message": "Continue work on project X"
}' > .trinity/wake/PC2.json

# Commit and push
git add .trinity/wake/PC2.json
git commit -m "wake PC2"
git push
```

### Option 3: Use Batch Script (Windows)

```batch
REM Send wake to PC2
call SEND_WAKE_SIGNAL.bat PC2 "process_queue" "Check spawn queue"
```

---

## Running the Daemon

### Foreground (for testing)

```bash
cd C:\Users\darri\100X_DEPLOYMENT
python .trinity/automation/AUTO_WAKE_DAEMON.py
```

**Output:**
```
2025-11-23 15:45:00 [INFO] AUTO WAKE DAEMON started for PC2
2025-11-23 15:45:00 [INFO] Monitoring: C:\Users\darri\100X_DEPLOYMENT\.trinity\wake
2025-11-23 15:45:00 [INFO] Check interval: 30s
2025-11-23 15:45:00 [INFO] Claude Code found at: C:\Users\darri\AppData\Local\Programs\claude-code\claude-code.exe
```

### Background (for production)

```batch
REM Start daemon in background
start "Auto Wake Daemon PC2" cmd /k "python .trinity\automation\AUTO_WAKE_DAEMON.py"
```

### With Windows Task Scheduler (recommended)

```batch
REM Schedule daemon to start on boot
schtasks /create /tn "Trinity Auto Wake PC2" /tr "python C:\Users\darri\100X_DEPLOYMENT\.trinity\automation\AUTO_WAKE_DAEMON.py" /sc onstart /ru SYSTEM
```

---

## Test Protocol: PC1 → PC2 → PC3 Chain

### Test 1: Single Wake (PC1 → PC2)

**On PC1:**
```bash
# 1. Verify PC2 daemon is running
ssh darri@100.85.71.74 "tasklist | findstr python"

# 2. Send wake signal to PC2
python .trinity/automation/AUTO_WAKE_DAEMON.py --send PC2 --task "test_wake" --message "Test from PC1"

# 3. Commit and push
git add .trinity/wake/PC2.json
git commit -m "test: wake PC2 from PC1"
git push

# 4. Wait 30-60 seconds for PC2 to pull and process

# 5. Check PC2 responded
git pull
cat .trinity/heartbeat/PC2.json
```

**Expected Result:**
- PC2 daemon detects wake signal within 30 seconds
- PC2 opens Claude Code automatically
- PC2 archives wake signal to `.trinity/wake_archive/`
- PC2 sends heartbeat confirming wake received

### Test 2: Chain Wake (PC1 → PC2 → PC3)

**On PC1:**
```bash
# Send wake to PC2 with instruction to wake PC3
python .trinity/automation/AUTO_WAKE_DAEMON.py --send PC2 \
  --task "wake_chain" \
  --message "Wake PC3 after you wake"

git add . && git commit -m "chain wake test" && git push
```

**On PC2 (after waking):**
```bash
# PC2 daemon wakes, opens Claude Code
# PC2 then sends wake to PC3
python .trinity/automation/AUTO_WAKE_DAEMON.py --send PC3 \
  --task "chain_complete" \
  --message "Wake chain from PC1 via PC2"

git add . && git commit -m "wake PC3 from PC2" && git push
```

**On PC3 (after waking):**
```bash
# PC3 daemon wakes, opens Claude Code
# PC3 confirms chain completion
echo '{"status":"chain_complete","wakened_by":"PC2","origin":"PC1"}' > .trinity/heartbeat/PC3.json
git add . && git commit -m "PC3 chain wake complete" && git push
```

### Test 3: All PCs Wake Each Other

**Scenario:** Round-robin wake test

1. PC1 wakes PC2
2. PC2 wakes PC3
3. PC3 wakes PC1
4. Cycle continues

**Setup:**
```bash
# On each PC, create scheduled wake
# PC1: Wake PC2 every hour
# PC2: Wake PC3 every hour (offset +20 min)
# PC3: Wake PC1 every hour (offset +40 min)
```

---

## Daemon Monitoring

### Check if Daemon is Running

```bash
# Windows
tasklist | findstr python

# Should show AUTO_WAKE_DAEMON.py process
```

### View Daemon Logs

```bash
# Realtime log monitoring
tail -f .trinity/logs/auto_wake_daemon.log

# Last 50 lines
tail -50 .trinity/logs/auto_wake_daemon.log
```

### Check Wake Signal History

```bash
# List archived wake signals
ls -lt .trinity/wake_archive/

# View most recent wake
cat .trinity/wake_archive/PC2_wake_*.json | tail -1
```

---

## Troubleshooting

### Problem: Daemon doesn't detect wake signal

**Check:**
1. Is daemon running? `tasklist | findstr python`
2. Is git pulling updates? Check logs
3. Is wake file created? `ls .trinity/wake/`
4. Check daemon logs: `tail .trinity/logs/auto_wake_daemon.log`

**Solution:**
```bash
# Restart daemon
taskkill /F /IM python.exe
python .trinity/automation/AUTO_WAKE_DAEMON.py
```

### Problem: Claude Code doesn't open

**Check:**
1. Is Claude Code installed?
2. Check path in logs
3. Test manual open: `claude-code C:\Users\darri\100X_DEPLOYMENT`

**Solution:**
```bash
# Update Claude Code path in AUTO_WAKE_DAEMON.py
# Or reinstall Claude Code
```

### Problem: Wake signal not syncing to other PCs

**Check:**
1. Git push successful? `git status`
2. Other PCs pulling? Check coordination daemon
3. Network connectivity? `ping 100.85.71.74`

**Solution:**
```bash
# Verify coordination daemon running
tasklist | findstr "CROSS_COMPUTER_DAEMON"

# Manual push if needed
git add . && git commit -m "wake signal" && git push
```

---

## Integration with Trinity System

### Auto-Start on Boot

Add to `TRIPLE_TRINITY_ORCHESTRATOR.bat`:

```batch
REM Start Auto Wake Daemon
echo [7/7] Starting Auto Wake Daemon...
start "Auto Wake Daemon %COMPUTER_ID%" cmd /k "python .trinity\automation\AUTO_WAKE_DAEMON.py"
```

### Coordination with Spawn Queue

When spawn queue has new tasks:
```bash
# Wake idle PC to process tasks
python .trinity/automation/AUTO_WAKE_DAEMON.py --send PC3 \
  --task "process_spawn_queue" \
  --message "New high-priority task available"
```

### Credit Exhaustion Handoff

When PC1 exhausts credits:
```bash
# Wake PC2 to continue work
python .trinity/automation/AUTO_WAKE_DAEMON.py --send PC2 \
  --task "handoff_from_pc1" \
  --message "PC1 credits exhausted, continue autonomous work"
```

---

## Performance Expectations

- **Wake Detection Time:** 0-30 seconds (based on git pull interval)
- **Claude Code Launch Time:** 2-5 seconds
- **End-to-End Wake Time:** 5-35 seconds total
- **Daemon CPU Usage:** <1% (mostly idle)
- **Daemon Memory Usage:** ~15-20 MB

---

## Security Considerations

### Wake Signal Authentication

Currently, wake signals are unauthenticated. Any commit to git can trigger a wake.

**Mitigation:**
- Only authorized users have git push access
- Wake signals archived for audit trail
- Daemon runs with user permissions (not SYSTEM)

### Future Enhancements

- [ ] Add digital signatures to wake signals
- [ ] Require confirmation before opening Claude Code
- [ ] Rate limiting on wake signals (prevent spam)
- [ ] Whitelist of allowed wake signal sources

---

## Advanced Usage

### Conditional Wake

Wake PC2 only if it's been idle for >1 hour:

```bash
# Check last activity timestamp
last_activity=$(cat .trinity/heartbeat/PC2.json | grep timestamp)

# Calculate time difference
# If > 1 hour, send wake
```

### Priority Wake

Different wake priorities:

```json
{
  "priority": "urgent",
  "from": "PC1",
  "to": "PC2",
  "task": "critical_bug_fix",
  "interrupt": true
}
```

### Scheduled Wake

Use Windows Task Scheduler to wake PCs on a schedule:

```batch
REM Wake PC2 every day at 9 AM
schtasks /create /tn "Daily PC2 Wake" /tr "python .trinity\automation\AUTO_WAKE_DAEMON.py --send PC2 --task daily_sync" /sc daily /st 09:00
```

---

## Success Metrics

**Wake System is Working If:**

✅ PC2 wakes within 30 seconds of signal
✅ Claude Code opens automatically
✅ Wake signal archived
✅ Heartbeat confirms wake received
✅ No errors in daemon logs
✅ Chain wake (PC1→PC2→PC3) completes in <2 minutes

---

## Next Steps

1. **Deploy to All PCs**
   - Install AUTO_WAKE_DAEMON.py on PC1, PC2, PC3
   - Start daemons on all machines
   - Test PC1→PC2 wake

2. **Schedule Auto-Start**
   - Add to Windows Task Scheduler
   - Set to start on boot
   - Verify persistence after reboot

3. **Test Wake Chain**
   - Run full PC1→PC2→PC3 chain test
   - Verify all wake signals processed
   - Check timing and reliability

4. **Integrate with Spawn Queue**
   - Auto-wake idle PCs when new tasks arrive
   - Round-robin task distribution
   - Load balancing across all PCs

---

**Status:** Ready for deployment and testing
**Priority:** HIGH - Foundational for autonomous operations
**Deployment:** Start with PC2, test, then PC1 and PC3
