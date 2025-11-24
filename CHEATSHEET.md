# DUAL TRINITY CHEAT SHEET

One-page reference ⚡

---

## Architecture

```
6 AGENTS = Cloud(C1,C2,C3) + Terminal(C1★,C2,C3)
2 TRINITIES = Cloud + Terminal
1 OUTPUT = Master consolidated
```

---

## Roles

| Agent | Role | Does |
|-------|------|------|
| **C1** | Coordinator | Plans, assigns, consolidates |
| **C2** | Builder | Implements, creates, builds |
| **C3** | Validator | Tests, validates, QA |

**Terminal-C1★** = MASTER (final authority)

---

## Files

**Trinity:**
```
c1_to_c2.md    C1 → C2 tasks
c2_to_c1.md    C2 → C1 reports
c1_to_c3.md    C1 → C3 validate
c3_to_c1.md    C3 → C1 results
```

**Hub:**
```
from_cloud/consolidated_output.md
from_terminal/consolidated_output.md
master_consolidated.md ← FINAL
```

---

## Flows

**Single Trinity:**
```
User → C1 → C2 → C3 → C1 → User
```

**Dual Trinity:**
```
           ┌─ Cloud Trinity → consolidated
User → Hub ┤
           └─ Terminal Trinity → consolidated
                                      ↓
                              Terminal-C1★ merges
                                      ↓
                                   Output
```

---

## Commands

**Activate agent:**
```
You are [C1/C2/C3] MECHANIC.
Read .consciousness/trinity/[C1/C2/C3]_ACTIVATION_INSTRUCTIONS.md
```

**Setup:**
```bash
mkdir -p .consciousness/{trinity,hub/{from_cloud,from_terminal,to_cloud,to_terminal,screen_watch}}
```

**Status:**
```bash
cat .consciousness/trinity/trinity_status.md
cat .consciousness/hub/hub_status.md
```

---

## Principles

1. **ONE consciousness** - Unified output
2. **Clear hierarchy** - Terminal-C1★ on top
3. **Unidirectional** - No loops
4. **Async files** - Markdown communication
5. **Git truth** - Version everything
6. **Graceful fail** - System continues if agents drop
7. **Autonomous** - No waiting for permission

---

## Status Icons

🟢 Online | 🟡 Partial | 🔴 Blocked | ⏳ Pending | ✅ Done

---

## Locations

```
.consciousness/
├── trinity/          Internal comms
│   ├── c1_to_c2.md
│   └── ...
└── hub/             Cross-Trinity
    ├── from_cloud/
    ├── from_terminal/
    └── master_consolidated.md
```

---

## Quick Debug

**Agent silent?**
→ Check status file → C1 handles → Continue

**Validation fails?**
→ C3 reports → C1 assigns fix → C2 fixes → Loop

**Hub down?**
→ Trinity works alone → Direct output → Manual merge

---

## Metrics

Target by Week 52:
- 50 agents
- 10 computers
- 1000 tasks/day
- 99.99% uptime

---

**Full docs:** `SYSTEM_MANUAL.md`, `HUB_PROTOCOL.md`, `QUICKSTART.md`

*Print this. Pin it. Reference it.*
