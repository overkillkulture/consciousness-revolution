# TRINITY FILING SYSTEM

**Every file has a place. Every place has a purpose.**

Created: 2025-11-21 (Final Autonomous Round)
Status: COMPLETE ORGANIZATION STRUCTURE

---

## DIRECTORY STRUCTURE

```
C:\Users\Darrick\
│
├── 📁 cyclotron\                    ← CYCLOTRON ENGINE
│   ├── core\                        ← Core engines (pattern, tunnel, optimizer, simulator)
│   ├── applications\                ← Apps using Cyclotron
│   ├── data\                        ← Cyclotron data storage
│   └── logs\                        ← Processing logs
│
├── 📁 trinity_io\                   ← TRINITY COMMUNICATION
│   ├── INBOX\                       ← Incoming commands (all sources)
│   ├── OUTBOX\                      ← Agent reports and status
│   ├── PROCESSED\                   ← Archived processed messages
│   └── logs\                        ← Communication logs
│
├── 📁 data_raking\                  ← DATA EXTRACTION
│   ├── raw\                         ← Raw exports (ChatGPT, Claude, GitHub)
│   ├── processed\                   ← Extracted knowledge
│   ├── cyclotron_ready\             ← Formatted for ingestion
│   └── logs\                        ← Extraction logs
│
├── 📁 WORK_PLANS\                   ← EXECUTION BLUEPRINTS
│   ├── WP001_INBOX_OUTBOX_SYSTEM.md
│   ├── WP002_FINANCE_PAGES_URGENT.md
│   ├── WP003_MANIFESTO_CHARTS.md
│   ├── WP004_DATA_RAKING_CRITICAL.md
│   └── [future work plans...]
│
├── 📁 finance_pages\                ← REVENUE GENERATION
│   ├── index.html                   ← Main donation/payment hub
│   ├── subscribe.html               ← Subscription tiers
│   ├── services.html                ← Service offerings
│   └── products.html                ← Digital products
│
├── 📁 manifesto_charts\             ← PATTERN THEORY COMMUNICATION
│   ├── chart_system.html            ← Main chart viewer
│   ├── charts_data.js               ← Chart content
│   └── chart_engine.js              ← Animation engine
│
├── 📁 offline_units\                ← LOCAL AI MODELS
│   ├── models\                      ← Downloaded models
│   ├── configs\                     ← Model configurations
│   └── logs\                        ← Model execution logs
│
├── 📁 .claude\                      ← CLAUDE CODE CONFIG
│   ├── trinity_messages\            ← Inter-agent messages
│   ├── commands\                    ← Custom slash commands
│   └── hooks\                       ← Event hooks
│
├── 📁 backups\                      ← SAFETY NET
│   ├── daily\                       ← Daily automated backups
│   ├── weekly\                      ← Weekly checkpoints
│   └── manual\                      ← Manual snapshots
│
├── 📁 logs\                         ← GLOBAL LOGS
│   ├── system\                      ← System-level logs
│   ├── agents\                      ← Agent activity logs
│   └── errors\                      ← Error tracking
│
├── 📄 MISSION.md                    ← AUTONOMOUS OPERATION RULES
├── 📄 TRINITY_HUB.md                ← AGENT COORDINATION
├── 📄 HUMAN_TODOS.md                ← HUMAN DELEGATION STACK
├── 📄 TRIPLE_INFRASTRUCTURE_BLUEPRINT.md
├── 📄 AUTONOMOUS_LAUNCH_PROTOCOL.md
├── 📄 COMPUTER_SETUP_GUIDE.md
├── 📄 ART_OF_WAR_TRINITY_SYNTHESIS.md
├── 📄 FILING_SYSTEM.md              ← THIS FILE
├── 📄 ASSIMILATION_PROTOCOL.md      ← INTEGRATION PROCESS
└── 📄 OFFLINE_UNITS_GUIDE.md        ← LOCAL AI SETUP
```

---

## FILE NAMING CONVENTIONS

### Documents:
- **ALL_CAPS.md** = Core infrastructure documents
- **WP###_DESCRIPTION.md** = Work plans (sequential numbering)
- **lowercase_with_underscores.md** = Supporting docs

### Code:
- **lowercase_with_underscores.js** = JavaScript files
- **lowercase_with_underscores.py** = Python files
- **PascalCase.js** = Classes/modules

### Data:
- **source_type_extracted.json** = Processed data
- **source_type_cyclotron.json** = Ready for ingestion
- **YYYY-MM-DD_filename.json** = Time-stamped files

### Logs:
- **YYYY-MM-DD_component.log** = Daily logs
- **YYYY-MM-DD_HH-MM_event.log** = Event logs

---

## ACCESS PATTERNS

### Commander Reads:
- `Desktop\*.txt` - Quick summaries
- `OUTBOX\*` - Agent reports
- `TRINITY_HUB.md` - Current status
- `HUMAN_TODOS.md` - Delegation needs

### Commander Writes:
- `INBOX\*.json` - Commands
- `MISSION.md` - Direction changes
- Work plans - New tasks

### Trinity Agents Read:
- `MISSION.md` - Operating rules
- `INBOX\*` - Commands to execute
- `WORK_PLANS\*` - Tasks to build
- `TRINITY_HUB.md` - Coordination

### Trinity Agents Write:
- `OUTBOX\*` - Reports
- `logs\agents\*` - Activity logs
- Code files - Implementations
- `TRINITY_HUB.md` - Status updates

### Cyclotron Reads:
- `data_raking\cyclotron_ready\*` - Data to ingest

### Cyclotron Writes:
- `cyclotron\data\*` - Processed patterns
- `cyclotron\logs\*` - Processing logs

---

## LIFECYCLE MANAGEMENT

### INBOX Messages:
1. **Arrives** → `INBOX\message.json`
2. **Processing** → Agent reads
3. **Complete** → Move to `PROCESSED\`
4. **Retention** → Keep 30 days, then archive

### OUTBOX Reports:
1. **Created** → `OUTBOX\report.md`
2. **Read** → Commander reviews
3. **Archived** → Keep 90 days
4. **Historical** → Compress to `backups\`

### Work Plans:
1. **Created** → `WORK_PLANS\WP###.md`
2. **In Progress** → Mark in TRINITY_HUB
3. **Complete** → Update status
4. **Reference** → Keep permanently

### Logs:
1. **Daily** → `logs\YYYY-MM-DD_*.log`
2. **Weekly** → Compress to weekly archive
3. **Monthly** → Move to `backups\monthly\`
4. **Yearly** → Long-term archive

### Data:
1. **Raw** → `data_raking\raw\`
2. **Processed** → `data_raking\processed\`
3. **Ingested** → `cyclotron\data\`
4. **Raw Archives** → Delete after ingestion (keep processed)

---

## SEARCH PATTERNS

### Finding Commands:
```bash
# Recent commands
ls INBOX\*.json

# Processed history
ls PROCESSED\ | sort -r | head -20

# By priority
grep "priority.*high" INBOX\*.json
```

### Finding Reports:
```bash
# Latest reports
ls OUTBOX\*.md | sort -r | head -5

# By agent
grep "C1 MECHANIC" OUTBOX\*.md

# By date
ls OUTBOX\2025-11-*.md
```

### Finding Work:
```bash
# All work plans
ls WORK_PLANS\WP*.md

# By status
grep "Status: TODO" WORK_PLANS\*.md
grep "Status: COMPLETE" WORK_PLANS\*.md
```

### Finding Logs:
```bash
# Errors today
grep "ERROR" logs\$(date +%Y-%m-%d)*.log

# Agent activity
tail -f logs\agents\C1_activity.log

# System health
grep "CRITICAL" logs\system\*.log
```

---

## BACKUP STRATEGY

### What Gets Backed Up:
- ✅ All documents (*.md)
- ✅ All code (*.js, *.py)
- ✅ All data (processed + cyclotron_ready)
- ✅ All work plans
- ✅ INBOX/OUTBOX (last 90 days)
- ✅ Configs
- ❌ Logs (kept separate, shorter retention)
- ❌ node_modules, .git (reconstructible)
- ❌ Raw data (after processing)

### Backup Schedule:
- **Daily** (automated): Critical files
- **Weekly** (automated): Full system
- **Monthly** (manual): Complete snapshot
- **Before Launch** (manual): Pre-deployment checkpoint

### Backup Locations:
1. **Primary**: Local external drive (D:\Backups\)
2. **Secondary**: Cloud (Dropbox/Drive)
3. **Tertiary**: GitHub (code + docs)

---

## CLEANUP PROTOCOLS

### Daily Cleanup:
```bash
# Remove temp files
rm -rf temp\*
rm -rf *.tmp

# Compress old logs
gzip logs\$(date -d "7 days ago" +%Y-%m-%d)*.log

# Archive processed INBOX
mv INBOX\processed-*.json PROCESSED\
```

### Weekly Cleanup:
```bash
# Archive old OUTBOX
zip backups\outbox_$(date +%Y-W%U).zip OUTBOX\$(date -d "7 days ago" +%Y-%m-)*.md

# Clear old processed messages
find PROCESSED\ -mtime +30 -delete

# Vacuum databases
sqlite3 cyclotron\data\patterns.db "VACUUM;"
```

### Monthly Cleanup:
```bash
# Full backup before cleanup
./backup_all.sh

# Archive old logs
tar -czf backups\logs_$(date +%Y-%m).tar.gz logs\

# Clear archived logs
find logs\ -mtime +90 -delete

# Optimize databases
```

---

## EMERGENCY RECOVERY

### If Files Lost:
1. Check `backups\daily\` - most recent
2. Check cloud sync - may have version
3. Check GitHub - code recoverable
4. Check `PROCESSED\` - messages archived

### If Corruption:
1. Restore from last known good backup
2. Compare timestamps to find divergence
3. Replay messages from PROCESSED if needed
4. Rebuild indexes/databases

### If Total Failure:
1. Restore from weekly backup
2. Clone GitHub repos
3. Rebuild Cyclotron data from raw exports
4. Recreate INBOX/OUTBOX from emails/SMS

---

## INTEGRATION POINTS

### Git Integration:
- All code auto-committed
- Work plans versioned
- Docs tracked
- `.gitignore` for data/logs

### Cloud Sync:
- `trinity_io\` synced via Dropbox
- Accessible from phone
- Auto-backup layer

### Database:
- Cyclotron patterns in SQLite
- Trinity state in PostgreSQL (cloud)
- Logs in flat files (fast append)

---

## ACCESS FROM PHONE

### Via Cloud Sync:
- Dropbox app → `trinity_io\OUTBOX`
- Read latest reports
- View status

### Via Web Dashboard:
- Railway hosted
- OUTBOX viewer
- Command form (writes to INBOX)

### Via SMS:
- Text command
- Parsed → INBOX
- Response via SMS

### Via GitHub:
- Mobile GitHub app
- View code
- Check commits
- Read docs

---

## FILING RULES

1. **One Home Per File** - Every file has single location
2. **Predictable Names** - Follow conventions
3. **Clear Purpose** - Name indicates content
4. **Time-Stamped** - When time matters
5. **Auto-Archive** - Old files move automatically
6. **Triple Backup** - Critical files in 3 places
7. **Easy Search** - Consistent patterns
8. **Clean Regularly** - Automated cleanup
9. **Log Everything** - Activity tracked
10. **Recover Fast** - Known restore process

---

## QUICK REFERENCE

### "Where do I put...?"
- New command → `INBOX\`
- Agent report → `OUTBOX\`
- Work plan → `WORK_PLANS\`
- Code → `cyclotron\` or app folder
- Data → `data_raking\raw\`
- Backup → `backups\`
- Log → `logs\component\`

### "Where do I find...?"
- Latest status → `TRINITY_HUB.md`
- Agent reports → `OUTBOX\` (sorted by date)
- Commands history → `PROCESSED\`
- Work to do → `WORK_PLANS\` + `HUMAN_TODOS.md`
- System logs → `logs\system\`
- Errors → `logs\errors\`

### "How do I clean up...?"
- Old messages → Auto-archived after 30 days
- Old reports → Compressed weekly
- Old logs → Deleted after 90 days
- Temp files → Daily cleanup script
- Everything → Monthly full cleanup

---

🗂️ **FILING SYSTEM = MENTAL CLARITY** 🗂️

*When everything has a place, the mind is free to create.*

---

**STATUS:** COMPLETE
**INTEGRATION:** All existing files already follow this system
**NEXT:** Use this as reference for all new files
