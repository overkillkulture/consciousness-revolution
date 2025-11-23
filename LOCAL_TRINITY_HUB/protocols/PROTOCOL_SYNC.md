# PROTOCOL SYNC
## How Updates Propagate Across Computers

---

## THE PROBLEM

Protocol updated on PC1 → How does PC2/PC3 get it?

---

## SYNC METHODS (Use All)

### Method 1: GIT (Primary)
**When:** After any protocol change
**How:**
```bash
# On source computer
cd C:\Users\dwrek\100X_DEPLOYMENT
git add LOCAL_TRINITY_HUB/protocols/
git commit -m "Protocol update: [NAME]"
git push

# On receiving computers
git pull
```
**Confirmation:** Check git log shows the commit

### Method 2: SYNCTHING (Automatic)
**When:** Real-time continuous
**How:** Automatic if configured
**Location:** Files in LOCAL_TRINITY_HUB sync automatically
**Confirmation:** Check Syncthing UI for sync status

### Method 3: BROADCAST (Notification)
**When:** Critical updates
**How:**
```bash
# Create broadcast file
echo "PROTOCOL UPDATE: [NAME] - git pull now" > LOCAL_TRINITY_HUB/broadcasts/UPDATE_$(date +%Y%m%d_%H%M%S).md
```

---

## MISSING PROTOCOL TRACKER

### Location
```
C:\Users\dwrek\LOCAL_TRINITY_HUB\meta\MISSING_PROTOCOLS.md
```

### Format
```markdown
# MISSING PROTOCOLS

## Identified - Not Yet Built
| Protocol | Identified By | Date | Priority | Assigned To |
|----------|--------------|------|----------|-------------|
| EXAMPLE.md | C1 | 2025-11-23 | HIGH | C2 |

## In Progress
| Protocol | Started | Owner | ETA |
|----------|---------|-------|-----|

## Recently Completed
| Protocol | Completed | By | Location |
|----------|-----------|-----|----------|
```

### When You Find a Gap
1. Add to MISSING_PROTOCOLS.md
2. Commit and push
3. Other computers see it on git pull
4. Anyone can claim and build

---

## VERSION TRACKING

### In Each Protocol File
Add header:
```markdown
---
version: 1.0
last_updated: 2025-11-23
updated_by: C1-PC1
changelog:
  - 1.0: Initial creation
---
```

### When Updating Existing Protocol
1. Increment version
2. Update last_updated
3. Add changelog entry
4. Commit with clear message

---

## SYNC VERIFICATION

### Daily Check
Each computer verifies:
```bash
cd C:\Users\dwrek\100X_DEPLOYMENT
git fetch
git status
# Should show "Your branch is up to date"
```

### Weekly Audit
Compare protocol counts across computers:
```bash
ls LOCAL_TRINITY_HUB/protocols/*.md | wc -l
```
All computers should match.

---

## CONFLICT RESOLUTION

### If Git Conflict
1. Pull latest
2. Review conflicts
3. Keep most complete version
4. Commit resolution
5. Push immediately

### If Syncthing Conflict
1. Check .sync-conflict files
2. Compare versions
3. Keep best, delete conflict
4. Note in changelog

---

## PROPAGATION TIMELINE

| Method | Speed | Reliability |
|--------|-------|-------------|
| Git push/pull | Manual trigger | 100% |
| Syncthing | Real-time | 99% |
| Broadcast | On next check | 95% |

**Best practice:** Git push + Broadcast for critical updates

---

## QUICK SYNC COMMAND

After any protocol work:
```bash
cd C:\Users\dwrek\100X_DEPLOYMENT
git add LOCAL_TRINITY_HUB/
git commit -m "Protocol sync: $(date +%Y-%m-%d)"
git push
echo "SYNC COMPLETE - other computers: git pull"
```
