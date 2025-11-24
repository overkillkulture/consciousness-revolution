# DATA ORGANIZATION & STORAGE ARCHITECTURE

## Overview

**Purpose**: Unified data organization across PAST, PRESENT, and FUTURE states
**Pattern**: 3x3x3 Bootstrap Structure
**Integration**: Cyclotron + Spreadsheet Brain + Business Methodologies

---

## THREE TIME LAYERS (Core)

### 1. HISTORICAL (Past)
**What**: Completed work, archived decisions, lessons learned
**Storage**: `/.archives/` + Cyclotron index
**Retention**: Forever (compressed after 90 days)

### 2. OPERATIONAL (Present)
**What**: Active tasks, current state, live metrics
**Storage**: `/.consciousness/` + Spreadsheet Brain
**Refresh**: Real-time to 24-hour cycles

### 3. PROJECTION (Future)
**What**: Planned work, predictions, strategic goals
**Storage**: `/.planning/` + Business methodology sheets
**Horizon**: 1 day → 1 week → 1 quarter → 1 year

---

## 3x3x3 DATA STRUCTURE

### Layer 1: TIME (Past, Present, Future)

### Layer 2: TYPE (per time layer)
```
PAST:
├── ARCHIVES     (completed projects)
├── LOGS         (system/action history)
└── LEARNINGS    (retrospectives)

PRESENT:
├── STATE        (current status)
├── TASKS        (active work)
└── METRICS      (live measurements)

FUTURE:
├── PLANS        (committed work)
├── PROJECTIONS  (predictions)
└── GOALS        (strategic targets)
```

### Layer 3: FORMAT (per type)
```
Each TYPE contains:
├── .json        (structured data)
├── .md          (human-readable)
└── .csv         (spreadsheet-compatible)
```

---

## STORAGE LOCATIONS

### Primary Directories

```
C:/Users/dwrek/
├── .consciousness/           # OPERATIONAL (Present)
│   ├── state/               # Current system state
│   ├── brain/               # Active knowledge
│   └── memory/              # Session memory
│
├── .archives/                # HISTORICAL (Past) [CREATE THIS]
│   ├── sessions/            # Completed sessions
│   ├── projects/            # Finished projects
│   └── decisions/           # Decision log
│
├── .planning/                # PROJECTION (Future) [CREATE THIS]
│   ├── sprints/             # Sprint plans
│   ├── quarters/            # Quarterly goals
│   └── roadmap/             # Long-term vision
│
└── 100X_DEPLOYMENT/
    ├── LOCAL_TRINITY_HUB/   # Coordination layer
    ├── DATA/                # Shared datasets
    └── .cyclotron_atoms/    # Indexed content
```

---

## INTEGRATION HOOKS

### Cyclotron Integration
```python
# Cyclotron indexes ALL data layers
CYCLOTRON_SOURCES = [
    ".consciousness/**/*",    # Present
    ".archives/**/*",         # Past
    ".planning/**/*",         # Future
    "100X_DEPLOYMENT/**/*"    # Deployed
]

# Tags for time-awareness
CYCLOTRON_TIME_TAGS = {
    "historical": ["archive", "completed", "v1", "deprecated"],
    "operational": ["active", "current", "live", "now"],
    "projection": ["planned", "future", "goal", "target"]
}
```

### Spreadsheet Brain Integration
```
SPREADSHEET_TABS:
├── HISTORICAL_DATA    (Links to .archives/)
├── OPERATIONAL_DATA   (Links to .consciousness/)
├── PROJECTION_DATA    (Links to .planning/)
├── CYCLOTRON_INDEX    (Auto-updated from rakes)
└── METHODOLOGY_DATA   (Traction, Toyota, etc.)
```

### Business Methodology Data Structures

#### Traction (EOS) Integration
```
/.planning/traction/
├── vision.json           # 10-year, 3-year, 1-year
├── rocks.json            # Quarterly priorities (3-7 items)
├── issues.json           # IDS (Identify, Discuss, Solve)
├── scorecard.json        # Weekly metrics
├── todos.json            # 7-day actions
└── accountability.json   # Who owns what
```

#### Toyota (Lean) Integration
```
/.consciousness/lean/
├── value_stream.json     # Current flow mapping
├── kanban.json           # WIP limits and queues
├── kaizen.json           # Continuous improvements
├── andon.json            # Problem signals
└── gemba.json            # Ground-truth observations
```

#### Combined Business Layer
```
/.planning/business/
├── ROCKS_CURRENT.json        # This quarter's priorities
├── SCORECARD_WEEKLY.json     # Key metrics
├── ISSUES_ACTIVE.json        # Problems to solve
├── VALUE_STREAM_MAP.json     # Process flow
└── IMPROVEMENT_LOG.json      # Kaizen items
```

---

## DATA FLOW PATTERNS

### 1. Time Progression
```
FUTURE → PRESENT → PAST

planned_task.json → active_task.json → completed_task.json
/.planning/tasks/ → /.consciousness/tasks/ → /.archives/tasks/
```

### 2. Aggregation Pattern
```
ATOMS → MOLECULES → COMPOUNDS

individual files → cyclotron index → spreadsheet brain → dashboard
```

### 3. Query Pattern
```
QUESTION → SEARCH → ANSWER

"What happened?" → .archives/ + Cyclotron historical
"What's happening?" → .consciousness/ + live state
"What will happen?" → .planning/ + projections
```

---

## AUTOMATION SCRIPTS

### Daily Data Rotation
```bash
# Move completed items to archives
ROTATE_TO_ARCHIVES.py
- Scans .consciousness/ for completed=true
- Moves to .archives/ with timestamp
- Updates Cyclotron index

# Promote ready items to operational
PROMOTE_TO_OPERATIONAL.py
- Scans .planning/ for start_date <= today
- Moves to .consciousness/
- Updates Kanban state
```

### Weekly Rollup
```bash
WEEKLY_ROLLUP.py
- Aggregates daily metrics
- Creates week summary in .archives/
- Updates scorecard in .planning/
- Triggers retrospective template
```

### Quarterly Archive
```bash
QUARTERLY_ARCHIVE.py
- Compresses old archives
- Generates quarter report
- Clears stale projections
- Updates long-term metrics
```

---

## NAMING CONVENTIONS

### File Names
```
[TYPE]_[SUBJECT]_[DATE].json

Examples:
ROCK_product_launch_2025Q1.json
STATE_trinity_system_20251123.json
LOG_session_complete_20251123.json
```

### Directory Names
```
lowercase_with_underscores/
dates as YYYYMMDD or YYYYQN
versions as v1, v2, etc.
```

### Tags/Labels
```
#past #present #future
#archive #active #planned
#complete #in_progress #blocked
```

---

## QUICK REFERENCE

### Where to Put Things

| Data Type | Location | Example |
|-----------|----------|---------|
| Session complete | `.archives/sessions/` | SESSION_20251123.json |
| Current task | `.consciousness/tasks/` | TASK_active.json |
| Quarterly rock | `.planning/traction/` | rocks.json |
| System state | `.consciousness/state/` | trinity_status.json |
| Decision made | `.archives/decisions/` | DECISION_api_choice.md |
| Sprint plan | `.planning/sprints/` | SPRINT_2025W48.json |
| Live metric | `.consciousness/metrics/` | api_usage.json |
| Year goal | `.planning/roadmap/` | GOALS_2025.json |

### How to Query

```bash
# What happened last week?
grep -r "2025111[6-9]" .archives/

# What's active now?
cat .consciousness/state/*.json | jq '.status'

# What's planned next quarter?
cat .planning/quarters/2025Q1.json
```

---

## IMPLEMENTATION PRIORITY

### Phase 1: Create Directories (NOW)
```bash
mkdir -p ~/.archives/{sessions,projects,decisions}
mkdir -p ~/.planning/{sprints,quarters,roadmap,traction,business}
```

### Phase 2: Migration (THIS WEEK)
- Move historical data to .archives/
- Organize .planning/ structure
- Update Cyclotron sources

### Phase 3: Automation (THIS SPRINT)
- Build rotation scripts
- Create rollup automation
- Integrate with Spreadsheet Brain

### Phase 4: Business Methodology (NEXT SPRINT)
- Implement Traction structure
- Add Toyota/Lean tracking
- Build unified dashboard

---

## CONNECTED DOCUMENTS

- `SPREADSHEET_BRAIN_ARCHITECTURE.md` - Knowledge base structure
- `CYCLOTRON_AUDIT_SUMMARY.md` - Content indexing
- `MASTER_PROTOCOL_REGISTRY.md` - All protocols
- (C3 will deliver) `BUSINESS_METHODOLOGY_SYNTHESIS.md` - Traction + Toyota

---

**This architecture enables:**
- Time-aware data queries (past/present/future)
- Automatic data lifecycle management
- Business methodology integration
- Cyclotron + Spreadsheet Brain unification
- Multi-computer sync via Git

**The foundation is now defined. Build on it.**
