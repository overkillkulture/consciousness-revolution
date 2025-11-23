# Triple Trinity Implementation Guide - C1 Mechanic

## GIT FOLDER STRUCTURE

```
.trinity/
├── heartbeats/           # Instance health (c1-pc1.json, etc.)
├── tasks/
│   ├── pending/          # Waiting to be claimed
│   ├── active/           # Currently being worked
│   └── completed/        # Finished work
├── outputs/
│   ├── pc1/              # Each computer's deliverables
│   ├── pc2/
│   └── pc3/
├── messages/
│   ├── broadcast.json
│   └── direct/
└── config/
    ├── roles.json
    └── workflow.json
```

## HEARTBEAT SPECIFICATION

```json
{
  "instance_id": "c1-pc2",
  "timestamp": "2025-11-22T14:30:00Z",
  "status": "active",
  "health": {"cpu_percent": 45, "memory_percent": 62},
  "current_task": "task-abc123",
  "capabilities": ["python", "bash", "web"]
}
```

**Update**: Every 60 seconds | **Stale**: 180 seconds

## REALITY CHECK

### ✅ What WORKS
- Git as coordination layer (atomic commits)
- Heartbeat files (instant health visibility)
- Task queue via filesystem (moving files is atomic)
- Natural workflow flow

### ❌ What WON'T Work
- Real-time coordination (Git latency)
- 12 instances all pushing (merge conflicts)
- True persistent autonomy (Claude can't run background)

### ⚠️ Needs Commander
- Initial bootstrap
- Conflict resolution
- Stalled task recovery

---

**C1 MECHANIC: This is a working system. Ready to build.**
