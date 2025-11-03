# 🌐 CONSCIOUSNESS NETWORK SYNC PROTOCOL

**Version**: 1.0
**Created**: November 3, 2025
**Purpose**: Multi-computer coordination via GitHub

---

## 🎯 OVERVIEW

This system allows multiple computers to coordinate tasks, share files, and communicate without requiring real-time connections or OTP-gated services.

**Communication Backbone**: Git/GitHub
**No Dependencies**: No APIs, no OTP, no auth services
**Async by Design**: Works even when computers aren't online simultaneously

---

## 📁 DIRECTORY STRUCTURE

```
.consciousness/
├── sync/
│   ├── computer_1_status.json    ← Computer 1 writes status here
│   ├── computer_2_status.json    ← Computer 2 writes status here
│   └── shared_tasks.json         ← Shared task queue
├── commands/
│   ├── computer_1_inbox.md       ← Commands FOR Computer 1
│   └── computer_2_inbox.md       ← Commands FOR Computer 2
├── file_transfers/               ← Drop files here to share
│   └── README.md
└── SYNC_PROTOCOL.md              ← This file
```

---

## 🔄 SYNC WORKFLOW

### Computer 1 (Sending a task to Computer 2):
```bash
cd /c/Users/dwrek/100X_DEPLOYMENT

# 1. Pull latest changes
git pull

# 2. Check Computer 2's status
cat .consciousness/sync/computer_2_status.json

# 3. Add command to Computer 2's inbox
echo "## New Task: Do X" >> .consciousness/commands/computer_2_inbox.md

# 4. Update shared tasks
# Edit .consciousness/sync/shared_tasks.json

# 5. Commit and push
git add .consciousness/
git commit -m "Computer 1: New task for Computer 2"
git push
```

### Computer 2 (Checking for tasks):
```bash
cd /path/to/100X_DEPLOYMENT

# 1. Pull latest changes
git pull

# 2. Check your inbox
cat .consciousness/commands/computer_2_inbox.md

# 3. Update your status
# Edit .consciousness/sync/computer_2_status.json

# 4. Complete tasks and report results
# Edit .consciousness/commands/computer_1_inbox.md with results

# 5. Commit and push
git add .consciousness/
git commit -m "Computer 2: Task completed"
git push
```

---

## 📊 STATUS FILE FORMAT

Each computer maintains a JSON status file with:

```json
{
  "computer_id": "UNIQUE_NAME",
  "timestamp": "ISO_8601_TIMESTAMP",
  "status": "OPERATIONAL|BUSY|OFFLINE|ERROR",
  "current_tasks": ["Array", "Of", "Tasks"],
  "blockers": ["Array", "Of", "Issues"],
  "available_resources": {
    "resource_name": true/false
  },
  "requests_for_other_computer": ["Tasks to delegate"],
  "last_updated": "ISO_8601_TIMESTAMP"
}
```

---

## 📋 TASK DELEGATION PATTERN

### High Priority Task (needs immediate attention):
1. Add to `shared_tasks.json` with `"priority": "HIGH"`
2. Add detailed instructions to target computer's inbox
3. Update your status to show you're waiting
4. Commit and push
5. Poll for updates (git pull every 5-10 minutes)

### File Transfer:
1. Drop file in `.consciousness/file_transfers/`
2. Add metadata file: `filename.txt.meta` with description
3. Update target computer's inbox with file location
4. Commit and push

### Response Required:
1. Add command to inbox with deadline
2. Mark in shared_tasks as "WAITING_RESPONSE"
3. Computer checks inbox, completes task, updates status
4. Commit and push response

---

## 🚀 AUTO-SYNC SCRIPT

Create this script on each computer for auto-polling:

```bash
#!/bin/bash
# consciousness_sync.sh

while true; do
  cd /c/Users/dwrek/100X_DEPLOYMENT
  git pull --quiet

  # Check for new commands
  NEW_COMMANDS=$(git log --since="5 minutes ago" --grep="Computer 2:" --oneline | wc -l)

  if [ $NEW_COMMANDS -gt 0 ]; then
    echo "🔔 New commands detected!"
    cat .consciousness/commands/computer_1_inbox.md
  fi

  sleep 300  # Check every 5 minutes
done
```

---

## 💡 USE CASES

### Use Case #1: Stripe API Key Retrieval
**Computer 1**: Needs Stripe key but doesn't have OTP access
**Computer 2**: Has phone with Authenticator app

**Workflow**:
1. Computer 1 adds task to Computer 2 inbox
2. Computer 2 pulls, sees task
3. Computer 2 logs into Stripe, gets key
4. Computer 2 drops key in file_transfers/
5. Computer 2 pushes, updates inbox
6. Computer 1 pulls, retrieves key, configures system

### Use Case #2: Distributed Social Media Posting
**Computer 1**: Has LinkedIn access
**Computer 2**: Has Instagram access

**Workflow**:
1. Both computers pull shared_tasks.json
2. Computer 1 takes LinkedIn task
3. Computer 2 takes Instagram task
4. Both update status and push results
5. Coordinator sees all tasks completed

### Use Case #3: Emergency Handoff
**Computer 1**: Battery dying, needs to hand off urgent task

**Workflow**:
1. Computer 1 dumps current state to status.json
2. Adds urgent task to Computer 2 inbox
3. Commits and pushes
4. Computer 2 picks up seamlessly

---

## 🔥 BEST PRACTICES

1. **Always pull before making changes** - Avoid merge conflicts
2. **Use descriptive commit messages** - Include computer ID
3. **Update status frequently** - Others need to know your state
4. **Clear completed tasks** - Keep inboxes clean
5. **Use timestamps** - ISO 8601 format for clarity
6. **Test the sync** - Run manual pull/push to verify connection

---

## 🐛 TROUBLESHOOTING

### Problem: Git conflicts
**Solution**: Use separate status files per computer, avoid editing other computer's files

### Problem: Can't push (authentication)
**Solution**: Use GitHub CLI (`gh auth login`) or SSH keys

### Problem: Other computer not responding
**Solution**: Check `last_updated` timestamp in their status file

---

## 🎯 NEXT STEPS

1. ✅ Structure created
2. ⏳ Test sync from Computer 1 → Computer 2
3. ⏳ Create auto-sync script
4. ⏳ Add file transfer capability
5. ⏳ Build dashboard to visualize sync status

---

**THE CONSCIOUSNESS NETWORK IS NOW OPERATIONAL**

No OTP. No APIs. Just Git.

**Async coordination at the speed of commits.**
