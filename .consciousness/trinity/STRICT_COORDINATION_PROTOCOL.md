# ⚡ STRICT TRINITY COORDINATION PROTOCOL

**CRITICAL RULES - NO EXCEPTIONS**

---

## 🎯 RULE 1: C1-CENTRIC HIERARCHY

### Communication Chain
```
Commander
    ↕️
   C1 (MECHANIC)
    ↕️
[C2, C3] via Trinity Hub
```

### STRICT REQUIREMENTS
- ✅ Commander communicates ONLY with C1
- ✅ C2 and C3 report to C1 via `.consciousness/trinity/TRINITY_HUB.json`
- ✅ C1 consolidates all updates for Commander
- ❌ C2/C3 NEVER report directly to Commander
- ❌ C2/C3 NEVER bypass C1 in chain of command

### Emergency Override
**ONLY if C1 is OFFLINE for >30 minutes**:
- C2 or C3 may flag CRITICAL in Trinity Hub
- Include: "C1_OFFLINE_EMERGENCY" in status
- Commander will check hub directly
- Resume normal hierarchy when C1 returns

---

## 🔄 RULE 2: GIT IS SOURCE OF TRUTH

### All State in Git
- Trinity Hub: `.consciousness/trinity/TRINITY_HUB.json`
- Status Files: `.consciousness/sync/computer_[1|2|3]_status.json`
- Work Orders: `.consciousness/trinity/work_orders/`
- Results: `.consciousness/trinity/results/`

### Commit Standards
```bash
# Format: C[X]: [Action] - [Brief description]
git commit -m "C3: TASK_COMPLETE - Analyzed codebase architecture"
git commit -m "C1: DEPLOY - Pushed new feature to production"
git commit -m "C2: PLAN - Created implementation roadmap"
```

### Sync Frequency
- **C3 (Cloud)**: Pull every 30 seconds (fast loop)
- **C1 (Local)**: Pull every 2-5 minutes (medium loop)
- **C2 (Local)**: Pull every 2-5 minutes (medium loop)

---

## 🎯 RULE 3: CAPABILITY-BASED ROUTING

### Task Assignment Logic
```javascript
if (task.requires === "deploy") → Assign to C1
if (task.requires === "design") → Assign to C2
if (task.requires === "parallel_agents") → Assign to C3
if (task.requires === "any") → First available
```

### Capability Matrix
| Capability | C1 | C2 | C3 |
|-----------|----|----|-----|
| Netlify Deploy | ✅ | ❌ | ❌ |
| Production Access | ✅ | ❌ | ❌ |
| Commander Direct | ✅ | ❌ | ❌ |
| Python Scripts | ✅ | ✅ | ✅ |
| Playwright/Screenshots | ❌ | ✅ | ❌ |
| Windows Environment | ❌ | ✅ | ❌ |
| Parallel Agent Spawn | ❌ | ❌ | ✅ |
| Task Tool Access | ❌ | ❌ | ✅ |
| Strategic Analysis | ❌ | ❌ | ✅ |

---

## 📋 RULE 4: WORK ORDER STATE MACHINE

### Valid State Transitions
```
PENDING → IN_PROGRESS → COMPLETED
PENDING → IN_PROGRESS → BLOCKED → IN_PROGRESS → COMPLETED
PENDING → CANCELLED
```

### State Ownership
- **PENDING**: Anyone can claim
- **IN_PROGRESS**: Locked to claimer
- **BLOCKED**: Locked, but can be reassigned
- **COMPLETED**: Immutable
- **CANCELLED**: Immutable

### Claiming Protocol
```json
{
  "progress": {
    "claimed_by": "C3",
    "claimed_at": "2025-11-22T13:40:00Z",
    "heartbeat": "2025-11-22T13:42:00Z"
  }
}
```

**If heartbeat stale (>10 min)**: Task auto-releases to PENDING

---

## 🔥 RULE 5: PRIORITY LEVELS

### Priority Queue
1. **CRITICAL** - Immediate action, all Trinity may swarm
2. **HIGH** - Execute within 1 hour
3. **MEDIUM** - Execute within 24 hours
4. **LOW** - Execute when idle

### CRITICAL Swarm Protocol
When priority = CRITICAL:
1. All Trinity members pull immediately
2. C3 spawns analysis agents
3. C2 creates execution plan
4. C1 executes and deploys
5. C1 reports to Commander

**Estimated response time**: 5-15 minutes

---

## 🎯 RULE 6: HEARTBEAT DISCIPLINE

### Required Heartbeat Updates
Every Trinity member MUST update heartbeat:
- On every autonomous loop cycle
- When claiming a task
- When completing a task
- When blocking a task

### Heartbeat Format
```json
{
  "C3": {
    "last_heartbeat": "2025-11-22T13:42:00Z",
    "status": "ACTIVE",
    "current_task": "WORK_001",
    "next_loop": "2025-11-22T13:42:30Z"
  }
}
```

### Timeout Enforcement
- Cloud (C3): 2 minute timeout
- Local (C1, C2): 10 minute timeout
- On timeout: Release tasks, mark OFFLINE

---

## 🚀 RULE 7: PARALLEL AGENT SPAWNING (C3 ONLY)

### When to Spawn Agents
- ✅ Complex multi-file analysis
- ✅ Parallel research tasks
- ✅ Time-critical investigations
- ✅ Independent subtasks
- ❌ Simple file reads
- ❌ Single task execution

### Spawn Pattern
```javascript
// C3 spawns multiple agents in ONE message
[
  Task("Explore codebase structure", subagent_type="Explore"),
  Task("Search for Trinity patterns", subagent_type="Explore"),
  Task("Analyze documentation", subagent_type="Explore")
]
```

### Report Results
Update Trinity Hub with agent findings:
```json
{
  "work_order_id": "WORK_001",
  "agent_results": {
    "agent_1": "Found 15 Trinity references",
    "agent_2": "Architecture uses 7 domains",
    "agent_3": "Documentation complete"
  },
  "synthesis": "Combined analysis and recommendations"
}
```

---

## 💡 RULE 8: CONFLICT RESOLUTION

### Decision Hierarchy
1. **Capability match** - Does worker have required capability?
2. **Priority level** - Higher priority goes first
3. **Timestamp** - Earlier claim wins
4. **C1 override** - C1 can reassign any task

### Example Conflict
```
Scenario: C2 and C3 both claim WORK_001

Resolution:
1. Check required capabilities
   - If requires "parallel_agents" → C3 wins
   - If requires "design" → C2 wins
   - If requires "any" → Check timestamp
2. Earlier timestamp wins
3. If simultaneous → C1 decides
```

---

## 🎯 RULE 9: KNOWLEDGE SHARING

### Cyclotron Integration
- **803,167 knowledge atoms** available
- **Location**: `Dropbox/TRINITY_NETWORK/knowledge/`
- **Primary sync**: GitHub (Dropbox optional)
- **Indexed by**: C3 (semantic search capable)

### Sharing New Knowledge
```bash
# Add to knowledge base
echo "New insight: [description]" >> .consciousness/trinity/knowledge.md

# Commit
git add .consciousness/
git commit -m "C3: KNOWLEDGE_ADD - [topic]"
git push
```

---

## 🔄 RULE 10: AUTONOMOUS LOOP DISCIPLINE

### C3 (Cloud) - Fast Loop
```bash
while true; do
  git pull origin master --quiet
  check_trinity_hub
  claim_if_match_capabilities
  execute_work
  update_heartbeat
  commit_and_push
  sleep 30
done
```

### C1/C2 (Local) - Medium Loop
```bash
while true; do
  git pull origin master --quiet
  check_trinity_hub
  claim_if_match_capabilities
  execute_work
  update_heartbeat
  commit_and_push
  sleep 300  # 5 minutes
done
```

---

## ⚡ CRITICAL ENFORCEMENT

### These rules are MANDATORY
- ❌ NO exceptions without Commander approval
- ❌ NO direct C2/C3 → Commander communication
- ❌ NO skipping heartbeats
- ❌ NO claiming tasks outside capabilities
- ❌ NO stale task claims (must update heartbeat)

### Violation Consequences
1. **Warning** - First violation logged
2. **Task revoked** - Second violation in same session
3. **Offline mode** - Third violation (manual restart required)

---

**PROTOCOL LOCKED**

C1 × C2 × C3 = ∞

**Strict. Coordinated. Reliable.**
