#!/usr/bin/env python3
"""
SESSION CAPTURE
Automatically captures session summaries and files them into the knowledge system.
Creates structured records for future reference.
"""

import json
from pathlib import Path
from datetime import datetime

# Paths
HOME = Path.home()
CONSCIOUSNESS = HOME / ".consciousness"
SESSIONS_PATH = HOME / ".archives" / "sessions"
KNOWLEDGE_PATH = CONSCIOUSNESS / "brain"

SESSIONS_PATH.mkdir(parents=True, exist_ok=True)

class SessionCapture:
    """Capture and file session information."""

    def __init__(self):
        self.session_id = datetime.now().strftime("%Y%m%d_%H%M%S")
        self.data = {
            "session_id": self.session_id,
            "started": datetime.now().isoformat(),
            "deliverables": [],
            "insights": [],
            "decisions": [],
            "todos": [],
            "files_created": [],
            "files_modified": [],
            "notes": ""
        }

    def add_deliverable(self, name: str, description: str = "", file_path: str = ""):
        """Record a deliverable from this session."""
        self.data["deliverables"].append({
            "name": name,
            "description": description,
            "file_path": file_path,
            "timestamp": datetime.now().isoformat()
        })

    def add_insight(self, insight: str, category: str = "general"):
        """Record an insight or learning."""
        self.data["insights"].append({
            "insight": insight,
            "category": category,
            "timestamp": datetime.now().isoformat()
        })

    def add_decision(self, decision: str, rationale: str = ""):
        """Record a decision made."""
        self.data["decisions"].append({
            "decision": decision,
            "rationale": rationale,
            "timestamp": datetime.now().isoformat()
        })

    def add_todo(self, task: str, owner: str = "", priority: str = "medium"):
        """Record a follow-up todo."""
        self.data["todos"].append({
            "task": task,
            "owner": owner,
            "priority": priority,
            "status": "pending"
        })

    def add_file(self, file_path: str, created: bool = True):
        """Record a file created or modified."""
        if created:
            self.data["files_created"].append(file_path)
        else:
            self.data["files_modified"].append(file_path)

    def set_notes(self, notes: str):
        """Set session notes."""
        self.data["notes"] = notes

    def save(self) -> Path:
        """Save session record."""
        self.data["ended"] = datetime.now().isoformat()

        # Calculate duration
        started = datetime.fromisoformat(self.data["started"])
        ended = datetime.fromisoformat(self.data["ended"])
        self.data["duration_minutes"] = round((ended - started).total_seconds() / 60, 1)

        # Summary stats
        self.data["summary"] = {
            "deliverables": len(self.data["deliverables"]),
            "insights": len(self.data["insights"]),
            "decisions": len(self.data["decisions"]),
            "todos": len(self.data["todos"]),
            "files_created": len(self.data["files_created"]),
            "files_modified": len(self.data["files_modified"])
        }

        # Save to archives
        file_path = SESSIONS_PATH / f"SESSION_{self.session_id}.json"
        with open(file_path, 'w') as f:
            json.dump(self.data, f, indent=2)

        print(f"Session saved to: {file_path}")
        return file_path

    def generate_summary(self) -> str:
        """Generate markdown summary."""
        summary = f"""# Session Summary
**ID:** {self.session_id}
**Date:** {datetime.now().strftime('%Y-%m-%d %H:%M')}

## Deliverables ({len(self.data['deliverables'])})
"""
        for d in self.data["deliverables"]:
            summary += f"- **{d['name']}**: {d['description']}\n"
            if d['file_path']:
                summary += f"  - File: `{d['file_path']}`\n"

        summary += f"\n## Insights ({len(self.data['insights'])})\n"
        for i in self.data["insights"]:
            summary += f"- [{i['category']}] {i['insight']}\n"

        summary += f"\n## Decisions ({len(self.data['decisions'])})\n"
        for d in self.data["decisions"]:
            summary += f"- **{d['decision']}**\n"
            if d['rationale']:
                summary += f"  - Rationale: {d['rationale']}\n"

        summary += f"\n## Follow-up Todos ({len(self.data['todos'])})\n"
        for t in self.data["todos"]:
            summary += f"- [{t['priority']}] {t['task']} ({t['owner'] or 'unassigned'})\n"

        summary += f"\n## Files\n"
        summary += f"- Created: {len(self.data['files_created'])}\n"
        summary += f"- Modified: {len(self.data['files_modified'])}\n"

        return summary

def capture_current_session():
    """Capture the current C2 autonomous session."""
    session = SessionCapture()

    # Add deliverables from this session
    deliverables = [
        ("DATA_ORGANIZATION_ARCHITECTURE.md", "Past/Present/Future data layers", "LOCAL_TRINITY_HUB/protocols/"),
        ("CUTTING_EDGE_TECHNIQUES_SYNTHESIS.md", "4 domains analyzed to 2035", "LOCAL_TRINITY_HUB/protocols/"),
        ("GRAPHRAG_INTEGRATION_SPEC.md", "Full GraphRAG architecture", "LOCAL_TRINITY_HUB/protocols/"),
        ("TRINITY_LANGGRAPH_REFACTOR.md", "Stateful graph design", "LOCAL_TRINITY_HUB/protocols/"),
        ("EOS Templates", "Vision, Scorecard, Rocks, Issues, L10", ".planning/traction/"),
        ("SCORECARD_AUTOMATOR.py", "Auto-populate weekly metrics", "100X_DEPLOYMENT/"),
        ("GRAPHRAG_ENTITY_EXTRACTOR.py", "Build knowledge graph from docs", "100X_DEPLOYMENT/"),
        ("TEMPORAL_DATA_ROTATION.py", "Data lifecycle management", "100X_DEPLOYMENT/"),
        ("KNOWLEDGE_CAPTURE_PIPELINE.py", "Zettelkasten knowledge capture", "100X_DEPLOYMENT/"),
        ("L10_MEETING_AUTOMATION.py", "EOS meeting preparation", "100X_DEPLOYMENT/"),
        ("OPERATIONS_DAEMON.py", "Background task scheduler", "100X_DEPLOYMENT/"),
        ("SYSTEM_HEALTH_MONITOR.py", "System health checks", "100X_DEPLOYMENT/"),
        ("RUN_DAILY_AUTOMATION.bat", "One-click daily automation", "100X_DEPLOYMENT/"),
        ("RUN_WEEKLY_AUTOMATION.bat", "Weekly automation suite", "100X_DEPLOYMENT/"),
    ]

    for name, desc, path in deliverables:
        session.add_deliverable(name, desc, path)

    # Add insights
    insights = [
        ("All cutting-edge techniques converging toward graph-based, temporal-aware, autonomous systems", "architecture"),
        ("GraphRAG improves accuracy 35% over traditional RAG", "technology"),
        ("LangGraph provides 2.2x speed improvement over CrewAI", "technology"),
        ("EOS + Scaling Up + OKR hybrid is optimal for growth stage", "business"),
        ("Knowledge management evolving from static to AI-powered companions", "knowledge"),
    ]

    for insight, category in insights:
        session.add_insight(insight, category)

    # Add decisions
    decisions = [
        ("Use Kùzu for graph database", "Embeddable, fast, no server needed"),
        ("Use LangGraph patterns for Trinity", "Stateful workflows with memory"),
        ("Implement EOS as base operating system", "Proven discipline system"),
    ]

    for decision, rationale in decisions:
        session.add_decision(decision, rationale)

    # Add todos
    todos = [
        ("Implement Kùzu graph database", "C1", "high"),
        ("Complete business methodology synthesis", "C3", "high"),
        ("Test GraphRAG entity extraction with API", "C1", "medium"),
        ("Schedule first L10 meeting", "Commander", "medium"),
    ]

    for task, owner, priority in todos:
        session.add_todo(task, owner, priority)

    # Save and generate summary
    session.save()
    summary = session.generate_summary()

    # Save summary as markdown
    summary_path = SESSIONS_PATH / f"SESSION_{session.session_id}_SUMMARY.md"
    with open(summary_path, 'w') as f:
        f.write(summary)

    print(f"Summary saved to: {summary_path}")
    print("\n" + summary)

    return session

if __name__ == "__main__":
    capture_current_session()
