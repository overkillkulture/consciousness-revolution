# COMPUTER HANDBOOK - COMPLETE SYSTEM REFERENCE

**One document. Everything you need.**

---

## SECTION 1: IDENTITY

### This Computer
- **Name**: PC1 (dwrekscpu)
- **Tailscale IP**: 100.70.208.75
- **AnyDesk ID**: 157-645-9360
- **Role**: Master coordinator, GitHub gatekeeper

### Network
- **PC2**: 100.85.71.74 (AnyDesk: 142-133-9914)
- **PC3**: 100.101.209.1 (AnyDesk: TBD)

---

## SECTION 2: FOLDER STRUCTURE

### The Only Folders That Matter

```
C:\Users\dwrek\
├── PC1_LOCAL_HUB/           ← ALL reporting goes here
├── 100X_DEPLOYMENT/         ← Git repo
├── Sync/                    ← Syncthing auto-sync
├── AUTO_ARCHIVE/            ← Old files go here
├── Downloads/               ← Cleaned weekly
└── Desktop/                 ← Cleaned daily
```

### Inside PC1_LOCAL_HUB/

```
PC1_LOCAL_HUB/
├── terminal_reports/        ← C1, C2, C3 report here
├── cloud_reports/           ← Cloud instances here
├── boot_down_inputs/        ← Boot downs go here
├── boot_down_archive/       ← Consolidated boot downs
├── consolidated/            ← Merged reports
├── outbound/                ← ONE output to GitHub
├── by_domain/               ← Files sorted by 7 domains
│   ├── infrastructure/
│   ├── pattern/
│   ├── business/
│   ├── consciousness/
│   ├── social/
│   ├── creative/
│   └── financial/
└── *.md, *.py               ← Protocols and scripts
```

---

## SECTION 3: FILE NAMING

### 7-Dimension Format
```
[DATE]_[COMPUTER]_[INSTANCE]_[DOMAIN]_[TYPE]_[PROJECT]_[VERSION].[ext]
```

### Examples
```
20251123_PC1_C1_infrastructure_report_hub-system_v1.md
20251123_PC1_consolidated_consciousness_bootdown_final.md
20251123_PC1_C2_pattern_task_cleanup-daemon_v1.py
```

---

## SECTION 4: COMMUNICATION PROTOCOLS

### Cross-Computer (5 Routes)

| # | Route | How | When |
|---|-------|-----|------|
| 1 | Local Hub | C2/C3 → PC1_LOCAL_HUB | Always |
| 2 | Syncthing | Auto file sync | Background |
| 3 | AnyDesk | Remote desktop | Manual control |
| 4 | Tailscale | Direct ping/SSH | Network ops |
| 5 | Git | C1 → GitHub only | Code/outputs |

### Reporting Flow
```
C1, C2, C3 ──► LOCAL HUB ──► consolidate.py ──► ONE OUTPUT
```

### GitHub Rule
**Only C1 pushes to GitHub.** C2/C3 report to local hub.

---

## SECTION 5: BOOT PROTOCOLS

### Boot Up (Every Session)
1. Read `~/PC1_LOCAL_HUB/BOOT_UP_PROTOCOL.md`
2. Check last boot down: `ls -t ~/PC1_LOCAL_HUB/boot_down_archive/*.md | head -1`
3. Check messages: `ls ~/PC1_LOCAL_HUB/terminal_reports/`
4. Send heartbeat

### Boot Down (End of Session)
1. Write to `~/PC1_LOCAL_HUB/boot_down_inputs/`
2. Run `python ~/PC1_LOCAL_HUB/boot_down_consolidator.py`
3. ONE file saved to archive

---

## SECTION 6: CLEANUP PROTOCOLS

### Automatic (Daemon)
```bash
python ~/PC1_LOCAL_HUB/MAINTENANCE_DAEMON.py
```

### Schedule
- **Daily**: Desktop (3 days), Downloads (7 days), Temp (1 day)
- **Weekly**: Git branches, Logs, Boot downs
- **Monthly**: Archives > 30 days

### Git Branch Cleanup
```bash
cd ~/100X_DEPLOYMENT
git branch --merged master | grep -v master | xargs git branch -d
git fetch --prune
```

---

## SECTION 7: INSTALLED SOFTWARE

### Required
- [ ] Claude Code CLI
- [ ] Git
- [ ] Node.js (v18+)
- [ ] Python (3.10+)
- [ ] Tailscale
- [ ] Syncthing
- [ ] AnyDesk

### Optional
- [ ] VS Code
- [ ] Netlify CLI
- [ ] GitHub CLI (gh)

---

## SECTION 8: API KEYS & CREDENTIALS

### Environment Variables
```bash
ANTHROPIC_API_KEY=sk-ant-...
GITHUB_TOKEN=ghp_...
STRIPE_API_KEY=sk_live_...
```

### Locations
- Keys: `~/.consciousness/` (encrypted)
- Tailscale: Logged in
- GitHub: `gh auth status`
- Netlify: `netlify status`

---

## SECTION 9: COMMANDS REFERENCE

### Daily Use
```bash
# Report to hub
echo '{...}' > ~/PC1_LOCAL_HUB/terminal_reports/C1_REPORT.json

# Consolidate
python ~/PC1_LOCAL_HUB/consolidate.py

# Push to GitHub (C1 only)
cd ~/100X_DEPLOYMENT && git add . && git commit -m "msg" && git push

# Run cleanup
python ~/PC1_LOCAL_HUB/MAINTENANCE_DAEMON.py

# Check Tailscale
tailscale status

# Sync check
ls ~/Sync/
```

### Troubleshooting
```bash
# Git push rejected
git fetch origin && git rebase origin/master && git push

# Find old files
find . -mtime +30 -type f

# Check disk space
df -h
```

---

## SECTION 10: CROSS-COMPUTER CONTROL

### From PC1, Control PC2/PC3

**Option 1: AnyDesk**
1. Open AnyDesk
2. Connect to 142-133-9914 (PC2)
3. Full remote control

**Option 2: Tailscale SSH**
```bash
ssh user@100.85.71.74
```

**Option 3: AutoIt/PyAutoGUI**
- Run VNC on PC2/PC3
- Control via automation script

### Remote Commands
```bash
# Run command on PC2 via SSH
ssh user@100.85.71.74 "python ~/PC2_LOCAL_HUB/consolidate.py"
```

---

## SECTION 11: THE SHAPE

**Everything follows the same funnel:**

```
INPUTS ──► LOCAL HUB ──► CONSOLIDATE ──► ONE OUTPUT

Applied to:
- Reporting: C1+C2+C3 → hub → one report
- Boot down: C1+C2+C3 → hub → one boot down
- Cross-PC: PC1+PC2+PC3 → master → one final
```

---

## SECTION 12: GAPS TO FILL

### Known Gaps
- [ ] PC3 credentials unknown
- [ ] No automated daemon scheduler yet
- [ ] Cyclotron mirror not deployed
- [ ] Round-robin protocol in design (C2 working on it)

### PC2/PC3 Need
- [ ] Create PC2_LOCAL_HUB / PC3_LOCAL_HUB
- [ ] Copy all protocols from PC1
- [ ] Set up Syncthing
- [ ] Verify API keys

---

## SECTION 13: EMERGENCY PROCEDURES

### If Communication Breaks
1. Check Tailscale: `tailscale status`
2. Ping other PC: `ping 100.85.71.74`
3. Check Syncthing folder: `ls ~/Sync/`
4. Use AnyDesk as fallback

### If Git Breaks
1. Stash changes: `git stash`
2. Pull: `git pull`
3. Apply: `git stash pop`
4. Commit and push

### If Instance Confused
1. Read this handbook
2. Check boot down archive
3. Report to hub asking for clarification

---

## SECTION 14: DO NOT

- ❌ Search for "hub", "trinity", "communications" (1,368 old files)
- ❌ Push to GitHub (unless you're C1)
- ❌ Create new protocols or folders
- ❌ Save files outside designated folders
- ❌ Skip the consolidation step

---

## SECTION 15: DO

- ✅ Read this handbook every session
- ✅ Use 7-dimension file naming
- ✅ Report to local hub
- ✅ Follow the funnel shape
- ✅ Run cleanup daemon regularly
- ✅ Push consolidated outputs only

---

**This is the one document. If something isn't here, it doesn't exist.**
