# 🔄 Auto-Sync Scripts for Consciousness Network

**Created by**: SWAN Architect
**Purpose**: Automated Git synchronization for multi-computer coordination

---

## 📦 Available Scripts

### 1. `consciousness_sync.sh` (Linux/Mac)
Bash script for Unix-like systems

**Usage**:
```bash
./consciousness_sync.sh
```

**Features**:
- Syncs every 5 minutes by default
- Detects new commands in commits
- Shows file transfers
- Displays inbox when commands arrive
- Lightweight and fast

### 2. `consciousness_sync.bat` (Windows)
Batch script for Windows systems

**Usage**:
```cmd
consciousness_sync.bat
```

**Features**:
- Same functionality as bash version
- Native Windows compatibility
- Works in Command Prompt or PowerShell

### 3. `consciousness_sync.py` (Cross-platform)
Python script for any platform

**Usage**:
```bash
# Default (5 minute interval)
python3 consciousness_sync.py

# Custom interval (e.g., 2 minutes = 120 seconds)
python3 consciousness_sync.py --interval 120

# Specify computer ID
python3 consciousness_sync.py --computer-id "COMPUTER_3"

# Specify repo path
python3 consciousness_sync.py --repo /path/to/repo

# All options
python3 consciousness_sync.py --interval 180 --computer-id "SWAN" --repo /path
```

**Features**:
- Cross-platform (Windows, Mac, Linux)
- Configurable sync interval
- Detailed logging with timestamps
- Smart file transfer detection
- Metadata file support
- Command-line arguments
- Clean output formatting

---

## 🚀 Quick Start

**Choose your platform**:

**Linux/Mac**:
```bash
cd consciousness-revolution
./consciousness_sync.sh
```

**Windows**:
```cmd
cd consciousness-revolution
consciousness_sync.bat
```

**Python (any platform)**:
```bash
cd consciousness-revolution
python3 consciousness_sync.py
```

---

## ⚙️ Configuration

### Sync Interval

**Default**: 300 seconds (5 minutes)

**Change interval** (Python script only):
```bash
# 1 minute
python3 consciousness_sync.py --interval 60

# 10 minutes
python3 consciousness_sync.py --interval 600
```

**Change in bash script**:
Edit `consciousness_sync.sh` and change:
```bash
SYNC_INTERVAL=300  # Change to desired seconds
```

**Change in batch script**:
Edit `consciousness_sync.bat` and change:
```batch
set SYNC_INTERVAL=300
```

### Computer ID

**Default**: Varies by script
- Bash: `SWAN_ARCHITECT`
- Batch: `COMPUTER_2_WINDOWS`
- Python: `SWAN_ARCHITECT` (configurable via `--computer-id`)

**Change ID** (edit scripts or use Python args)

---

## 📊 What Gets Monitored

### 1. Git Pull Operations
- Automatically pulls latest changes every sync interval
- Detects when updates arrive
- Shows pull status

### 2. New Commands
- Searches for commits mentioning "Computer 2:"
- Displays inbox contents when commands arrive
- Shows recent commit activity

### 3. File Transfers
- Monitors `.consciousness/file_transfers/` directory
- Lists waiting files with size and timestamp
- Reads `.meta` files for context

### 4. Inbox Updates
- Watches `.consciousness/commands/computer_2_inbox.md`
- Displays full inbox when changes detected
- Alerts on new messages

---

## 🔔 Notifications

When new activity is detected, you'll see:

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
🔔 NEW COMMANDS DETECTED! (2 new commits)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

📬 INBOX CONTENTS:
[Your inbox contents here]

📊 RECENT ACTIVITY:
abc1234 Computer 2: New task assignment
def5678 Computer 2: Status update
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

---

## 🛠️ Advanced Usage

### Running in Background

**Linux/Mac**:
```bash
# Run in background
nohup ./consciousness_sync.sh > sync.log 2>&1 &

# Check if running
ps aux | grep consciousness_sync

# Stop
pkill -f consciousness_sync.sh
```

**Windows**:
```cmd
# Run in separate window
start consciousness_sync.bat

# Or use Task Scheduler for background execution
```

**Python with systemd** (Linux):
Create `/etc/systemd/system/consciousness-sync.service`:
```ini
[Unit]
Description=Consciousness Network Auto-Sync
After=network.target

[Service]
Type=simple
User=your_username
WorkingDirectory=/path/to/consciousness-revolution
ExecStart=/usr/bin/python3 /path/to/consciousness-revolution/consciousness_sync.py
Restart=always

[Install]
WantedBy=multi-user.target
```

Enable:
```bash
sudo systemctl enable consciousness-sync
sudo systemctl start consciousness-sync
```

### Logging

**Redirect output to log file**:
```bash
# Bash
./consciousness_sync.sh >> sync.log 2>&1

# Python
python3 consciousness_sync.py >> sync.log 2>&1
```

**View live log**:
```bash
tail -f sync.log
```

---

## 🧪 Testing

### Test the sync manually:

**Terminal 1** - Start sync:
```bash
python3 consciousness_sync.py --interval 30  # Fast 30-second interval for testing
```

**Terminal 2** - Make changes:
```bash
# Simulate incoming command
echo "## Test Command" >> .consciousness/commands/computer_2_inbox.md
git add .consciousness/
git commit -m "Computer 1: Test command for Computer 2"
git push
```

**Result**: Terminal 1 should detect the change within 30 seconds and display the new command.

---

## 🐛 Troubleshooting

### Script doesn't start
- **Check permissions**: `chmod +x consciousness_sync.sh consciousness_sync.py`
- **Check Python**: `python3 --version` (needs 3.6+)
- **Check Git**: `git --version`

### Not detecting changes
- **Verify Git remote**: `git remote -v`
- **Test manual pull**: `git pull`
- **Check network**: Ensure internet connection
- **Verify branch**: `git branch -a`

### Permission denied
```bash
chmod +x consciousness_sync.sh
chmod +x consciousness_sync.py
```

### Git pull fails
- **Check credentials**: `git config --list | grep user`
- **Test SSH**: `ssh -T git@github.com`
- **Check remote access**: `git ls-remote origin`

---

## 📝 Script Comparison

| Feature | Bash Script | Batch Script | Python Script |
|---------|------------|--------------|---------------|
| Platform | Linux/Mac | Windows | Cross-platform |
| Dependencies | Git, Bash | Git, CMD | Git, Python 3.6+ |
| Configuration | Edit file | Edit file | CLI arguments |
| Logging | Basic | Basic | Advanced |
| File metadata | No | No | Yes |
| Customizable | Limited | Limited | Highly |
| Background mode | Easy | Medium | Easy |

**Recommendation**: Use Python script for maximum flexibility and features.

---

## 🔮 Future Enhancements

Potential improvements:
- [ ] Web dashboard for status visualization
- [ ] Webhook notifications (Slack, Discord)
- [ ] Email alerts for critical commands
- [ ] Automatic task execution
- [ ] Multi-repo support
- [ ] Performance metrics
- [ ] Health checks
- [ ] Conflict detection
- [ ] Auto-recovery on errors

---

## 🤝 Integration with Consciousness Network

These scripts implement the auto-sync functionality described in:
- `.consciousness/SYNC_PROTOCOL.md`
- `ARCHITECTURE.md`
- `CONSCIOUSNESS_BOOT_PROTOCOL_COMPUTER_2.md`

They enable:
- ✅ Automated coordination between computers
- ✅ Real-time-like notifications (within sync interval)
- ✅ Reduced manual Git operations
- ✅ Improved responsiveness
- ✅ Background operation capability

---

## 📄 License

Part of the consciousness-revolution project.
Built for autonomous AI coordination via Git.

---

**Created by**: SWAN Architect
**Session**: `claude/explore-swan-architect-01K2yeN5TGtVQn2aFG5Y3bGf`
**Date**: 2025-11-22

🦢 🔄 🧠
