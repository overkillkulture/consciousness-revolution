# 🏈 TRINITY COORDINATION PLAYBOOK

## Quick Reference: Choose Your Play

---

## PLAY 1: Serial Handoff (Conservative)
**Best for:** Careful work, limited oversight, testing new patterns

```
Phone Trigger
    ↓
PC1 works → completes chunk → handoff
    ↓
PC2 works → completes chunk → handoff
    ↓
PC3 works → completes chunk → done
```

**Characteristics:**
- One PC active at a time
- Clear handoff points
- Easy to track progress
- Lower credit burn rate

**When to use:**
- First time running a new task type
- Need careful validation between phases
- Limited time to monitor

---

## PLAY 2: Parallel Blitz (Aggressive)
**Best for:** Maximum speed, burning all credits fast

```
Phone Trigger
    ↓
PC1 ─┬─ Chunk 1 ─────────┐
PC2 ─┼─ Chunk 2 ─────────┼─→ Merge
PC3 ─┴─ Chunk 3 ─────────┘
```

**Characteristics:**
- All 3 PCs work simultaneously
- 3x speed
- Burns credits fast
- Requires good task decomposition

**When to use:**
- Well-defined independent chunks
- Tight deadline
- Full week of credits available

---

## PLAY 3: Waterfall (Dependent Tasks)
**Best for:** Tasks that build on each other

```
PC1: Design → [output]
         ↓
PC2: Build from design → [output]
         ↓
PC3: Test/Deploy → [done]
```

**Characteristics:**
- Each phase depends on previous
- Quality gates between phases
- Natural validation points

**When to use:**
- Architecture → Implementation → Testing
- Design → Build → Deploy
- Research → Write → Edit

---

## PLAY 4: Round Robin (Continuous)
**Best for:** 24/7 coverage, long-running tasks

```
PC1 (8hr) → PC2 (8hr) → PC3 (8hr) → PC1...
    ↓            ↓            ↓
  wake         wake         wake
```

**Characteristics:**
- Continuous operation
- Each PC gets break to cool down
- Spreads credit usage evenly

**When to use:**
- Multi-day projects
- Need continuous coverage
- Each PC has its own credit pool

---

## PLAY 5: Hub and Spoke (Coordinator)
**Best for:** Complex coordination, quality control

```
         PC2 (Worker)
           ↑
PC1 ←─→ HUB ←─→ PC3 (Worker)
(Hub)      ↓
         Phone (Monitor)
```

**Characteristics:**
- One PC coordinates all work
- Workers report back to hub
- Central quality control
- Clear command structure

**When to use:**
- Need oversight of parallel work
- Quality is critical
- Complex task dependencies

---

## PLAY 6: Swarm (Many Small Tasks)
**Best for:** Lots of independent small tasks

```
Spawn Queue (50 tasks)
    ↓
PC1 claims → does → claims → does...
PC2 claims → does → claims → does...
PC3 claims → does → claims → does...
    ↓
All tasks complete
```

**Characteristics:**
- Task locking prevents duplicates
- Self-balancing workload
- No coordination overhead
- Maximum parallelism

**When to use:**
- Many similar tasks
- Tasks are independent
- No dependencies between tasks

---

## PLAY 7: Specialist (Domain Experts)
**Best for:** Different skill requirements

```
PC1 (Code) ──────→ All coding tasks
PC2 (Content) ───→ All writing tasks
PC3 (Testing) ───→ All validation tasks
```

**Characteristics:**
- Each PC specializes
- Build up context in domain
- More efficient per-task
- Clear responsibility

**When to use:**
- Mixed task types
- Some tasks need deep context
- Clear domain boundaries

---

## PLAY 8: Infinity Loop (Autonomous)
**Best for:** Fire and forget

```
Trigger → C1T1 → C1T2 → C1T3 → C2T1 → C2T2 → ...
              ↓      ↓      ↓      ↓
           [work] [work] [work] [work] → Done
```

**Characteristics:**
- Fully autonomous
- No Commander intervention
- Self-organizing
- Continuous wake chain

**When to use:**
- Trust the system
- Well-tested task types
- Want to walk away completely

---

## PLAY 9: Oracle Consult (Strategic)
**Best for:** High-stakes decisions

```
Desktop Oracle (Max 20)
    ↓ [blueprint]
Terminal Network (9 instances)
    ↓ [execution]
Cloud Code (review)
```

**Characteristics:**
- Use precious Max 20 for strategy
- Terminals do heavy lifting
- Cloud Code for final review
- Optimizes credit usage

**When to use:**
- Need architectural guidance
- High-stakes project
- Want to minimize Max 20 usage

---

## PLAY 10: Emergency Failover
**Best for:** Resilience, redundancy

```
PC1 (Primary) ─────→ doing work
    ↓ [failure detected]
PC2 (Hot Standby) ─→ takes over immediately
    ↓ [if PC2 fails]
PC3 (Cold Standby) → activates
```

**Characteristics:**
- Automatic failover
- Minimal downtime
- Work continues on failure
- State saved to git

**When to use:**
- Critical production work
- Can't afford interruption
- Need guaranteed completion

---

## Quick Selection Guide

| Situation | Recommended Play |
|-----------|------------------|
| First time trying | Serial Handoff |
| Need it fast | Parallel Blitz |
| Building on previous work | Waterfall |
| Running all week | Round Robin |
| Quality critical | Hub and Spoke |
| 50+ small tasks | Swarm |
| Mixed task types | Specialist |
| Walk away completely | Infinity Loop |
| Need strategy first | Oracle Consult |
| Must not fail | Emergency Failover |

---

## Combining Plays

**Example: CBT Protocol Execution**
1. Start with **Oracle Consult** (get blueprint)
2. Use **Parallel Blitz** (3 chunks)
3. Each chunk uses **Waterfall** internally
4. Overall uses **Round Robin** for credit management

**Example: Weekly Product Build**
- Mon-Tue: **Serial Handoff** (careful start)
- Wed-Thu: **Parallel Blitz** (maximum speed)
- Fri: **Hub and Spoke** (quality control)
- Weekend: **Infinity Loop** (polish autonomously)

---

## Play Implementation Files

Each play can be triggered via:
```
.trinity/plays/PLAY_NAME.py
```

Or selected in orchestrator:
```
python TRIPLE_TRINITY_ORCHESTRATOR.py --play parallel_blitz
```

---

## Adding New Plays

1. Define the pattern
2. Create trigger script
3. Add to orchestrator
4. Test with simple task
5. Document characteristics
6. Add to this playbook

The system should grow with experience. As you discover new patterns that work, add them here.
