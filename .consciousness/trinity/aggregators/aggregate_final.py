#!/usr/bin/env python3
"""
Trinity Final Aggregator: Combines Summary₁ + Summary₂ → Master Output
Exports to main computer via Git
"""

import json
import os
from datetime import datetime
from pathlib import Path
import hashlib

TRINITY_DIR = Path(".consciousness/trinity")
SUMMARIES_DIR = TRINITY_DIR / "summaries"
EXPORT_DIR = TRINITY_DIR / "export"

def load_summary(summary_type):
    """Load a summary file"""
    summary_file = SUMMARIES_DIR / f"{summary_type}_summary.json"

    if not summary_file.exists():
        return {
            "layer": summary_type.upper(),
            "status": "NO_SUMMARY",
            "timestamp": None,
            "health": {"health_percentage": 0}
        }

    with open(summary_file, 'r') as f:
        return json.load(f)

def generate_session_id():
    """Generate unique session ID"""
    timestamp = datetime.now().isoformat()
    hash_obj = hashlib.md5(timestamp.encode())
    return f"TRINITY_{hash_obj.hexdigest()[:8].upper()}"

def calculate_overall_health(claude_summary, terminal_summary):
    """Calculate overall system health"""
    claude_health = claude_summary.get("health", {}).get("health_percentage", 0)
    terminal_health = terminal_summary.get("health", {}).get("health_percentage", 0)

    # Weighted average (Claude 60%, Terminal 40%)
    overall = (claude_health * 0.6) + (terminal_health * 0.4)

    return {
        "ai_layer": claude_health,
        "system_layer": terminal_health,
        "overall": overall,
        "status": get_health_status(overall)
    }

def get_health_status(percentage):
    """Get health status from percentage"""
    if percentage >= 90:
        return "EXCELLENT"
    elif percentage >= 70:
        return "GOOD"
    elif percentage >= 50:
        return "DEGRADED"
    elif percentage >= 25:
        return "POOR"
    else:
        return "CRITICAL"

def create_executive_summary(claude_summary, terminal_summary):
    """Create executive summary"""
    return {
        "ai_insights": claude_summary.get("summary", {}).get("insights", [])[:3],  # Top 3
        "system_status": terminal_summary.get("system_status", {}).get("overall", "UNKNOWN"),
        "health": calculate_overall_health(claude_summary, terminal_summary),
        "timestamp": datetime.now().isoformat()
    }

def merge_completed_work(claude_summary, terminal_summary):
    """Merge completed work from both layers"""
    return {
        "ai_tasks": claude_summary.get("completed_tasks", []),
        "system_operations": terminal_summary.get("execution_logs", []),
        "total_ai_tasks": len(claude_summary.get("completed_tasks", [])),
        "total_system_ops": len(terminal_summary.get("execution_logs", []))
    }

def consolidate_blockers(claude_summary, terminal_summary):
    """Consolidate blockers from both layers"""
    return {
        "ai_blockers": claude_summary.get("blockers", []),
        "system_errors": terminal_summary.get("errors", []),
        "total_blockers": len(claude_summary.get("blockers", [])) + len(terminal_summary.get("errors", []))
    }

def create_recommendations(claude_summary, terminal_summary):
    """Create recommendations for Commander"""
    recommendations = {
        "immediate_actions": [],
        "next_steps": claude_summary.get("next_actions", []),
        "system_alerts": terminal_summary.get("alerts", [])
    }

    # Add immediate actions based on blockers
    ai_blockers = claude_summary.get("blockers", [])
    sys_errors = terminal_summary.get("errors", [])

    if ai_blockers:
        recommendations["immediate_actions"].append({
            "action": "RESOLVE_AI_BLOCKERS",
            "count": len(ai_blockers),
            "priority": "HIGH"
        })

    if sys_errors:
        recommendations["immediate_actions"].append({
            "action": "FIX_SYSTEM_ERRORS",
            "count": len(sys_errors),
            "priority": "CRITICAL"
        })

    return recommendations

def create_master_output():
    """Create master output for export to main computer"""

    # Load summaries
    claude_summary = load_summary("claude")
    terminal_summary = load_summary("terminal")

    # Create master output
    master_output = {
        "session_id": generate_session_id(),
        "timestamp": datetime.now().isoformat(),
        "version": "1.0.0",

        "executive_summary": create_executive_summary(claude_summary, terminal_summary),

        "layer_status": {
            "claude_layer": {
                "instances": claude_summary.get("instances", {}),
                "health": claude_summary.get("health", {})
            },
            "terminal_layer": {
                "instances": terminal_summary.get("instances", {}),
                "health": terminal_summary.get("health", {})
            }
        },

        "completed_work": merge_completed_work(claude_summary, terminal_summary),

        "current_blockers": consolidate_blockers(claude_summary, terminal_summary),

        "recommendations": create_recommendations(claude_summary, terminal_summary),

        "export_metadata": {
            "status": "READY",
            "method": "git_sync",
            "destination": "main_computer",
            "format": "json",
            "compressed": False,
            "encrypted": False
        },

        "raw_summaries": {
            "claude": claude_summary,
            "terminal": terminal_summary
        }
    }

    # Save master output
    EXPORT_DIR.mkdir(parents=True, exist_ok=True)
    output_file = EXPORT_DIR / "MASTER_OUTPUT.json"

    with open(output_file, 'w') as f:
        json.dump(master_output, f, indent=2)

    # Also create a compact version
    compact_file = EXPORT_DIR / "MASTER_OUTPUT_COMPACT.json"
    compact_output = {
        "session_id": master_output["session_id"],
        "timestamp": master_output["timestamp"],
        "health": master_output["executive_summary"]["health"]["overall"],
        "status": master_output["executive_summary"]["health"]["status"],
        "tasks_completed": master_output["completed_work"]["total_ai_tasks"],
        "blockers": master_output["current_blockers"]["total_blockers"],
        "recommendations": len(master_output["recommendations"]["immediate_actions"])
    }

    with open(compact_file, 'w') as f:
        json.dump(compact_output, f, indent=2)

    print(f"✅ Master output created: {output_file}")
    print(f"   Session ID: {master_output['session_id']}")
    print(f"   Overall Health: {master_output['executive_summary']['health']['overall']:.1f}%")
    print(f"   Status: {master_output['executive_summary']['health']['status']}")
    print(f"   Ready for export to main computer")

    return master_output

if __name__ == "__main__":
    create_master_output()
