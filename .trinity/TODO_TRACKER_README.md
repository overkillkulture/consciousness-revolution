# TODO TRACKER - Persistent Kanban System

**Never lose your todos again!** This Kanban-style todo tracker syncs via git so all PCs see the same todos.

---

## Quick Start

### View Dashboard (Visual Kanban Board)
```bash
# Open in browser
start .trinity/dashboards/TODO_DASHBOARD.html
```

### Add Todo
```bash
python .trinity/automation/TODO_TRACKER.py add "Task description" --priority high

# With more details
python .trinity/automation/TODO_TRACKER.py add "Build feature X" \
  --priority high \
  --description "Detailed description here" \
  --assigned-to "C1_T2"
```

### Show Kanban Board (Terminal)
```bash
python .trinity/automation/TODO_TRACKER.py board
```

### Move Todo
```bash
# Start working on todo #5
python .trinity/automation/TODO_TRACKER.py move 5 --column in_progress

# Mark todo #5 as done
python .trinity/automation/TODO_TRACKER.py complete 5
```

### List All Todos
```bash
# All todos
python .trinity/automation/TODO_TRACKER.py list

# Only "todo" column
python .trinity/automation/TODO_TRACKER.py list --column todo
```

---

## Priority Levels

- `low` - 🔵 Nice to have
- `normal` - ⚪ Standard priority (default)
- `high` - 🟡 Important
- `urgent` - 🔴 Critical/blocking

---

## Kanban Columns

- `todo` - 📝 Not started
- `in_progress` - 🔄 Currently working on
- `done` - ✅ Completed

---

## Examples

### Session Planning
```bash
# Add all tasks for next session
python .trinity/automation/TODO_TRACKER.py add "auto-desktop-bridge" --priority normal
python .trinity/automation/TODO_TRACKER.py add "auto-command-center" --priority normal
python .trinity/automation/TODO_TRACKER.py add "chunk2-courses" --priority high
```

### Working on Task
```bash
# Start working
python .trinity/automation/TODO_TRACKER.py move 2 --column in_progress

# Complete
python .trinity/automation/TODO_TRACKER.py complete 2
```

### Cleanup
```bash
# Delete old completed todos
python .trinity/automation/TODO_TRACKER.py delete 15
```

---

## Data Location

- **JSON Data:** `.trinity/todos/kanban.json` (syncs via git)
- **HTML Dashboard:** `.trinity/dashboards/TODO_DASHBOARD.html`

All todos automatically sync across PC1, PC2, and PC3!

---

## Integration with Claude Code Sessions

The todos persist in git, so:
- ✅ Survive session restarts
- ✅ Visible across all PCs
- ✅ Version controlled (git history)
- ✅ Can be edited manually if needed

---

## Current Status

**Todos:** 9 total
- 📝 TODO: 6 tasks
- 🔄 IN PROGRESS: 0 tasks
- ✅ DONE: 3 tasks

View live status: `python .trinity/automation/TODO_TRACKER.py board`
