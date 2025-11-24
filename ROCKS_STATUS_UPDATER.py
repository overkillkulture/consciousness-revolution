#!/usr/bin/env python3
"""
ROCKS STATUS UPDATER
Update quarterly rock status and milestones from command line.
EOS tool for tracking execution.
"""

import json
from pathlib import Path
from datetime import datetime

# Paths
ROCKS_PATH = Path.home() / ".planning" / "traction" / "ROCKS_Q4_2025.json"

def load_rocks():
    """Load rocks data."""
    if ROCKS_PATH.exists():
        with open(ROCKS_PATH) as f:
            return json.load(f)
    return None

def save_rocks(data):
    """Save rocks data."""
    with open(ROCKS_PATH, 'w') as f:
        json.dump(data, f, indent=2)
    print(f"Saved to {ROCKS_PATH}")

def list_rocks():
    """List all rocks with status."""
    data = load_rocks()
    if not data:
        print("No rocks file found")
        return

    print("\n" + "=" * 60)
    print(f"Q4 2025 ROCKS")
    print("=" * 60)

    status_symbols = {
        "complete": "✅",
        "on_track": "🟢",
        "off_track": "🔴",
        "in_progress": "🟡",
        "not_started": "⏳"
    }

    for rock in data.get("rocks", []):
        symbol = status_symbols.get(rock.get("status", ""), "❓")
        milestone_done = sum(1 for m in rock.get("milestones", []) if m.get("done"))
        milestone_total = len(rock.get("milestones", []))

        print(f"\n{symbol} [{rock.get('id')}] {rock.get('rock', 'unnamed')[:50]}")
        print(f"   Owner: {rock.get('owner', '?')} | Status: {rock.get('status', '?')}")
        print(f"   Milestones: {milestone_done}/{milestone_total}")

        # Show milestones
        for i, m in enumerate(rock.get("milestones", []), 1):
            done = "✅" if m.get("done") else "⬜"
            print(f"     {done} W{m.get('week', i)}: {m.get('milestone', 'unnamed')}")

    print("\n" + "=" * 60)
    summary = data.get("summary", {})
    print(f"Total: {summary.get('total', len(data.get('rocks', [])))} | "
          f"Complete: {summary.get('complete', 0)} | "
          f"On Track: {summary.get('on_track', 0)} | "
          f"Not Started: {summary.get('not_started', 0)}")

def update_rock_status(rock_id: str, new_status: str):
    """Update a rock's status."""
    data = load_rocks()
    if not data:
        print("No rocks file found")
        return

    valid_statuses = ["complete", "on_track", "off_track", "in_progress", "not_started"]
    if new_status not in valid_statuses:
        print(f"Invalid status. Use: {', '.join(valid_statuses)}")
        return

    # Find rock
    for rock in data.get("rocks", []):
        if rock.get("id") == rock_id:
            old_status = rock.get("status")
            rock["status"] = new_status

            if new_status == "complete":
                rock["completed_date"] = datetime.now().isoformat()

            save_rocks(data)
            print(f"Updated {rock_id}: {old_status} → {new_status}")
            return

    print(f"Rock {rock_id} not found")

def complete_milestone(rock_id: str, week: int):
    """Mark a milestone as complete."""
    data = load_rocks()
    if not data:
        print("No rocks file found")
        return

    for rock in data.get("rocks", []):
        if rock.get("id") == rock_id:
            for milestone in rock.get("milestones", []):
                if milestone.get("week") == week:
                    milestone["done"] = True
                    milestone["completed_at"] = datetime.now().isoformat()

                    save_rocks(data)
                    print(f"Completed: {rock_id} Week {week} - {milestone.get('milestone')}")

                    # Check if all milestones done
                    all_done = all(m.get("done") for m in rock.get("milestones", []))
                    if all_done:
                        print(f"All milestones complete! Consider marking {rock_id} as complete.")
                    return

            print(f"Week {week} milestone not found in {rock_id}")
            return

    print(f"Rock {rock_id} not found")

def add_rock(rock_name: str, owner: str, milestones: list = None):
    """Add a new rock."""
    data = load_rocks()
    if not data:
        data = {"quarter": "Q4 2025", "rocks": [], "summary": {}}

    # Generate ID
    existing_ids = [r.get("id", "R0") for r in data.get("rocks", [])]
    max_num = max([int(id[1:]) for id in existing_ids if id.startswith("R")], default=0)
    new_id = f"R{max_num + 1}"

    # Default milestones if not provided
    if not milestones:
        milestones = [
            {"week": 1, "milestone": "Research and planning", "done": False},
            {"week": 2, "milestone": "Initial implementation", "done": False},
            {"week": 3, "milestone": "Testing and refinement", "done": False},
            {"week": 4, "milestone": "Deployment and documentation", "done": False}
        ]

    new_rock = {
        "id": new_id,
        "rock": rock_name,
        "owner": owner,
        "status": "not_started",
        "milestones": milestones,
        "notes": "",
        "completed_date": None
    }

    data["rocks"].append(new_rock)

    # Update summary
    data["summary"]["total"] = len(data["rocks"])
    data["summary"]["not_started"] = sum(1 for r in data["rocks"] if r.get("status") == "not_started")

    save_rocks(data)
    print(f"Added rock: {new_id} - {rock_name} (Owner: {owner})")

def update_summary():
    """Recalculate summary stats."""
    data = load_rocks()
    if not data:
        return

    rocks = data.get("rocks", [])

    data["summary"] = {
        "total": len(rocks),
        "complete": sum(1 for r in rocks if r.get("status") == "complete"),
        "on_track": sum(1 for r in rocks if r.get("status") in ["on_track", "in_progress"]),
        "off_track": sum(1 for r in rocks if r.get("status") == "off_track"),
        "not_started": sum(1 for r in rocks if r.get("status") == "not_started")
    }

    save_rocks(data)
    print("Summary updated")

def main():
    import sys

    if len(sys.argv) < 2:
        list_rocks()
        print("\nCommands:")
        print("  list                     - List all rocks")
        print("  status <id> <status>     - Update rock status")
        print("  milestone <id> <week>    - Complete a milestone")
        print("  add <name> <owner>       - Add new rock")
        print("  summary                  - Update summary stats")
        print("\nStatuses: complete, on_track, off_track, in_progress, not_started")
        return

    command = sys.argv[1]

    if command == "list":
        list_rocks()

    elif command == "status" and len(sys.argv) >= 4:
        rock_id = sys.argv[2].upper()
        new_status = sys.argv[3].lower()
        update_rock_status(rock_id, new_status)

    elif command == "milestone" and len(sys.argv) >= 4:
        rock_id = sys.argv[2].upper()
        week = int(sys.argv[3])
        complete_milestone(rock_id, week)

    elif command == "add" and len(sys.argv) >= 4:
        rock_name = sys.argv[2]
        owner = sys.argv[3]
        add_rock(rock_name, owner)

    elif command == "summary":
        update_summary()

    else:
        print(f"Unknown command or missing arguments: {command}")
        print("Run without arguments to see help")

if __name__ == "__main__":
    main()
