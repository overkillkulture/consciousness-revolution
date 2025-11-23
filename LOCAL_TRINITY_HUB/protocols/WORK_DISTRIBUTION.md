# WORK DISTRIBUTION PROTOCOL
## How C1 Splits Tasks for C2 and C3

---

## WHEN C1 RECEIVES A WORKLOAD

### Step 1: ANALYZE
- What's the full scope?
- How many distinct tasks?
- What can run in parallel?
- What has dependencies?

### Step 2: SPLIT BY ROLE
| Task Type | Assign To | Why |
|-----------|-----------|-----|
| Building/Coding | C1 (self) | Mechanic |
| Architecture/Design | C2 | Architect |
| Research/Analysis | C3 | Oracle |
| Can be any | "any" | First to claim |

### Step 3: WRITE TO HUB
Create task files in:
```
LOCAL_TRINITY_HUB/inbox/
```

---

## TASK FILE FORMAT

Filename: `TASK_[ID]_[ASSIGNEE].md`

Example: `TASK_001_C2.md`

```markdown
# TASK: [Short Title]

## Assignment
- **ID:** TASK_001
- **Assigned To:** C2 (or C3, or "any")
- **Priority:** HIGH/MEDIUM/LOW
- **Created:** 2025-11-23 14:30
- **Deadline:** End of session

## Description
[Clear description of what needs to be done]

## Deliverable
[What should be produced - file, report, code, etc.]

## Output Location
LOCAL_TRINITY_HUB/outputs/TASK_001_OUTPUT.md

## Dependencies
- None (or list what must be done first)

## Context
[Any background info needed]
```

---

## C1 WORKFLOW

```python
def distribute_work(workload):
    # 1. Break into tasks
    tasks = analyze_and_split(workload)

    # 2. Assign each task
    for task in tasks:
        if task.type == "build":
            task.assign = "C1"  # Keep it
        elif task.type == "design":
            task.assign = "C2"
        elif task.type == "research":
            task.assign = "C3"
        else:
            task.assign = "any"

        # 3. Write to hub
        write_task_file(task, "LOCAL_TRINITY_HUB/inbox/")

    # 4. Notify
    print(f"Distributed {len(tasks)} tasks to hub")
    print("C2/C3: Report to hub")
```

---

## AFTER DISTRIBUTING

C1 should:
1. Keep own tasks and start working
2. Announce: "Tasks distributed to hub - C2/C3 report"
3. Monitor outputs folder for completions
4. Synthesize results when all done

---

## C2/C3 CLAIMING TASKS

When C2 or C3 checks hub:

1. Look in `LOCAL_TRINITY_HUB/inbox/`
2. Find files with their name or "any"
3. Claim by:
   - Moving file to `LOCAL_TRINITY_HUB/in_progress/`
   - Or renaming: `TASK_001_any.md` → `TASK_001_C2_CLAIMED.md`
4. Work on task
5. Write output to specified location
6. Move task to `LOCAL_TRINITY_HUB/completed/`

---

## FOLDER STRUCTURE

```
LOCAL_TRINITY_HUB/
├── inbox/           # New tasks waiting
├── in_progress/     # Tasks being worked on
├── outputs/         # Deliverables go here
└── completed/       # Finished tasks (archive)
```

---

## QUICK DISTRIBUTION TEMPLATE

When you have work to split, create files like:

**TASK_001_C2.md**
```markdown
# TASK: Design the flow testing protocol

## Assignment
- **Assigned To:** C2
- **Priority:** HIGH

## Description
Create a protocol for testing multi-screen coordination flow.

## Deliverable
FLOW_TEST_PROTOCOL.md

## Output Location
LOCAL_TRINITY_HUB/outputs/FLOW_TEST_PROTOCOL.md
```

**TASK_002_C3.md**
```markdown
# TASK: Research Cyclotron setup requirements

## Assignment
- **Assigned To:** C3
- **Priority:** HIGH

## Description
Find all requirements for setting up Cyclotron on each computer.

## Deliverable
CYCLOTRON_REQUIREMENTS.md

## Output Location
LOCAL_TRINITY_HUB/outputs/CYCLOTRON_REQUIREMENTS.md
```

---

## TIMING

1. C1 distributes tasks FIRST
2. THEN tell C2/C3 to report to hub
3. They find tasks waiting
4. No wasted trips

**Don't wake them before the food is on the table.**
