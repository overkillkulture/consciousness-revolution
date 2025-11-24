#!/usr/bin/env python3
"""
L10 MEETING AUTOMATION
Automates preparation, facilitation, and follow-up for EOS Level 10 meetings.
"""

import json
import os
from pathlib import Path
from datetime import datetime, timedelta

# Paths
HOME = Path.home()
PLANNING_PATH = HOME / ".planning" / "traction"
ARCHIVES_PATH = HOME / ".archives" / "sessions"

class L10Meeting:
    """Manage L10 meeting workflow."""

    def __init__(self):
        self.meeting_date = datetime.now()
        self.meeting_id = self.meeting_date.strftime("%Y%m%d")

    def prepare(self) -> dict:
        """Prepare meeting materials by aggregating all EOS data."""
        print("=" * 50)
        print("L10 MEETING PREPARATION")
        print(f"Date: {self.meeting_date.strftime('%Y-%m-%d')}")
        print("=" * 50)

        preparation = {
            "meeting_id": self.meeting_id,
            "date": self.meeting_date.isoformat(),
            "scorecard": self._load_scorecard(),
            "rocks": self._load_rocks(),
            "issues": self._load_issues(),
            "previous_todos": self._load_previous_todos(),
            "generated_at": datetime.now().isoformat()
        }

        # Save preparation
        prep_file = PLANNING_PATH / f"L10_PREP_{self.meeting_id}.json"
        with open(prep_file, 'w') as f:
            json.dump(preparation, f, indent=2)

        print(f"\nPreparation saved to: {prep_file}")
        return preparation

    def _load_scorecard(self) -> dict:
        """Load current scorecard."""
        scorecard_file = PLANNING_PATH / "SCORECARD_WEEKLY.json"
        if scorecard_file.exists():
            with open(scorecard_file) as f:
                return json.load(f)
        return {}

    def _load_rocks(self) -> dict:
        """Load current rocks."""
        rocks_file = PLANNING_PATH / "ROCKS_Q4_2025.json"
        if rocks_file.exists():
            with open(rocks_file) as f:
                return json.load(f)
        return {}

    def _load_issues(self) -> dict:
        """Load issues list."""
        issues_file = PLANNING_PATH / "ISSUES_LIST.json"
        if issues_file.exists():
            with open(issues_file) as f:
                return json.load(f)
        return {}

    def _load_previous_todos(self) -> list:
        """Load todos from previous meeting."""
        # Find most recent meeting file
        meeting_files = sorted(PLANNING_PATH.glob("L10_MEETING_*.json"), reverse=True)
        if meeting_files:
            with open(meeting_files[0]) as f:
                data = json.load(f)
                return data.get('todos', [])
        return []

    def generate_agenda(self) -> str:
        """Generate meeting agenda markdown."""
        prep = self.prepare()

        agenda = f"""# L10 Meeting Agenda
**Date:** {self.meeting_date.strftime('%B %d, %Y')}
**Time:** 90 minutes

---

## 1. SEGUE (5 min)
Share personal/professional good news

---

## 2. SCORECARD (5 min)

| Metric | Goal | Actual | Status |
|--------|------|--------|--------|
"""
        # Add scorecard metrics
        for metric in prep.get('scorecard', {}).get('scorecard', {}).get('measurables', []):
            status = "✅" if metric.get('on_track') else "❌" if metric.get('on_track') is False else "⏳"
            agenda += f"| {metric['name']} | {metric.get('goal', '?')} | {metric.get('actual', '?')} | {status} |\n"

        agenda += """
**Off-track items to discuss:**
"""
        for metric in prep.get('scorecard', {}).get('scorecard', {}).get('measurables', []):
            if metric.get('on_track') is False:
                agenda += f"- {metric['name']}\n"

        agenda += """
---

## 3. ROCK REVIEW (5 min)

| Rock | Owner | Status |
|------|-------|--------|
"""
        # Add rocks
        for rock in prep.get('rocks', {}).get('rocks', []):
            status_emoji = {"complete": "✅", "on_track": "🟢", "off_track": "🔴", "not_started": "⏳", "in_progress": "🟡"}
            emoji = status_emoji.get(rock.get('status', ''), '❓')
            agenda += f"| {rock.get('rock', 'unnamed')[:40]}... | {rock.get('owner', '?')} | {emoji} |\n"

        agenda += """
---

## 4. CUSTOMER/EMPLOYEE HEADLINES (5 min)
-
-
-

---

## 5. TO-DO REVIEW (5 min)

**Previous todos:**
"""
        for todo in prep.get('previous_todos', []):
            status = "✅" if todo.get('done') else "❌"
            agenda += f"- [{status}] {todo.get('task', 'unnamed')} ({todo.get('owner', '?')})\n"

        if not prep.get('previous_todos'):
            agenda += "- No previous todos\n"

        agenda += """
---

## 6. IDS - IDENTIFY, DISCUSS, SOLVE (60 min)

**Issues to prioritize:**
"""
        # Short-term issues
        for issue in prep.get('issues', {}).get('issues', {}).get('short_term', []):
            priority_emoji = {"high": "🔴", "medium": "🟡", "low": "🟢", "critical": "⚫"}
            emoji = priority_emoji.get(issue.get('priority', ''), '⚪')
            agenda += f"- {emoji} {issue.get('issue', 'unnamed')}\n"

        agenda += """
**Top 3 to IDS this meeting:**
1.
2.
3.

### Issue 1: _______________
- **Identify:**
- **Discuss:**
- **Solve:**
  - To-Do:
  - Owner:
  - Due:

### Issue 2: _______________
- **Identify:**
- **Discuss:**
- **Solve:**
  - To-Do:
  - Owner:
  - Due:

### Issue 3: _______________
- **Identify:**
- **Discuss:**
- **Solve:**
  - To-Do:
  - Owner:
  - Due:

---

## 7. CONCLUDE (5 min)

**New Todos:**
- [ ]
- [ ]
- [ ]

**Cascading Messages:**
-

**Meeting Rating (1-10):**
- Commander: __
- C1: __
- C2: __
- C3: __

---

*Generated by L10 Meeting Automation*
"""

        # Save agenda
        agenda_file = PLANNING_PATH / f"L10_AGENDA_{self.meeting_id}.md"
        with open(agenda_file, 'w') as f:
            f.write(agenda)

        print(f"Agenda saved to: {agenda_file}")
        return agenda

    def save_meeting_results(self, results: dict):
        """Save meeting results including todos and decisions."""

        meeting_record = {
            "meeting_id": self.meeting_id,
            "date": self.meeting_date.isoformat(),
            "attendees": results.get('attendees', []),
            "todos": results.get('todos', []),
            "issues_resolved": results.get('issues_resolved', []),
            "decisions": results.get('decisions', []),
            "ratings": results.get('ratings', {}),
            "notes": results.get('notes', ''),
            "saved_at": datetime.now().isoformat()
        }

        # Save meeting record
        meeting_file = PLANNING_PATH / f"L10_MEETING_{self.meeting_id}.json"
        with open(meeting_file, 'w') as f:
            json.dump(meeting_record, f, indent=2)

        # Archive old meeting files
        self._archive_old_meetings()

        print(f"Meeting results saved to: {meeting_file}")
        return meeting_file

    def _archive_old_meetings(self, keep_recent: int = 4):
        """Archive meetings older than N weeks."""
        meeting_files = sorted(PLANNING_PATH.glob("L10_MEETING_*.json"))

        if len(meeting_files) > keep_recent:
            for old_file in meeting_files[:-keep_recent]:
                dest = ARCHIVES_PATH / old_file.name
                old_file.rename(dest)
                print(f"Archived: {old_file.name}")

    def generate_todo_reminders(self) -> list:
        """Generate reminders for incomplete todos."""
        todos = self._load_previous_todos()
        reminders = []

        for todo in todos:
            if not todo.get('done', False):
                due = todo.get('due')
                if due:
                    due_date = datetime.fromisoformat(due)
                    if due_date <= datetime.now():
                        reminders.append({
                            "type": "overdue",
                            "todo": todo,
                            "days_overdue": (datetime.now() - due_date).days
                        })
                    elif due_date <= datetime.now() + timedelta(days=2):
                        reminders.append({
                            "type": "due_soon",
                            "todo": todo,
                            "days_until": (due_date - datetime.now()).days
                        })

        return reminders

def main():
    """Run L10 meeting automation."""
    import sys

    meeting = L10Meeting()

    if len(sys.argv) > 1:
        command = sys.argv[1]

        if command == "prepare":
            meeting.prepare()
        elif command == "agenda":
            print(meeting.generate_agenda())
        elif command == "reminders":
            reminders = meeting.generate_todo_reminders()
            print("\n📋 TODO REMINDERS\n")
            for r in reminders:
                if r['type'] == 'overdue':
                    print(f"🔴 OVERDUE ({r['days_overdue']} days): {r['todo']['task']}")
                else:
                    print(f"🟡 Due soon ({r['days_until']} days): {r['todo']['task']}")
            if not reminders:
                print("No pending reminders!")
        else:
            print(f"Unknown command: {command}")
            print("Usage: python L10_MEETING_AUTOMATION.py [prepare|agenda|reminders]")
    else:
        # Default: generate agenda
        meeting.generate_agenda()
        print("\n✅ L10 Meeting materials prepared!")
        print("\nCommands:")
        print("  python L10_MEETING_AUTOMATION.py prepare   - Prepare all data")
        print("  python L10_MEETING_AUTOMATION.py agenda    - Generate agenda")
        print("  python L10_MEETING_AUTOMATION.py reminders - Show todo reminders")

if __name__ == "__main__":
    main()
