#!/usr/bin/env python3
"""
Trinity Aggregator 1: Claude Code Instance Aggregator
Combines outputs from C1, C2, C3 into Summary₁
"""

import json
import os
from datetime import datetime
from pathlib import Path

TRINITY_DIR = Path(".consciousness/trinity")
CLAUDE_DIR = TRINITY_DIR / "claude"
SUMMARIES_DIR = TRINITY_DIR / "summaries"

def load_instance_output(instance_id):
    """Load output from a Claude Code instance"""
    output_file = CLAUDE_DIR / f"{instance_id.lower()}_output.json"

    if not output_file.exists():
        return {
            "instance_id": instance_id,
            "status": "NO_OUTPUT",
            "timestamp": None,
            "tasks_completed": [],
            "insights": [],
            "blockers": [],
            "decisions_made": [],
            "next_actions": []
        }

    with open(output_file, 'r') as f:
        return json.load(f)

def synthesize_insights(instances):
    """Combine insights from all instances"""
    all_insights = []
    for instance in instances:
        all_insights.extend(instance.get("insights", []))

    # Deduplicate similar insights
    unique_insights = list(set(all_insights))

    # Create synthesis
    synthesis = {
        "total_insights": len(all_insights),
        "unique_insights": len(unique_insights),
        "insights": unique_insights,
        "common_themes": extract_common_themes(all_insights)
    }

    return synthesis

def extract_common_themes(insights):
    """Extract common themes from insights"""
    # Simple keyword frequency analysis
    themes = {}
    for insight in insights:
        words = insight.lower().split()
        for word in words:
            if len(word) > 5:  # Filter short words
                themes[word] = themes.get(word, 0) + 1

    # Return top themes
    sorted_themes = sorted(themes.items(), key=lambda x: x[1], reverse=True)
    return [theme for theme, count in sorted_themes[:5]]

def merge_task_lists(instances):
    """Merge completed tasks from all instances"""
    all_tasks = []
    for instance in instances:
        instance_id = instance.get("instance_id", "UNKNOWN")
        tasks = instance.get("tasks_completed", [])
        all_tasks.extend([
            {"instance": instance_id, "task": task}
            for task in tasks
        ])
    return all_tasks

def consolidate_blockers(instances):
    """Consolidate blockers from all instances"""
    blockers = {}
    for instance in instances:
        instance_id = instance.get("instance_id", "UNKNOWN")
        for blocker in instance.get("blockers", []):
            if blocker not in blockers:
                blockers[blocker] = []
            blockers[blocker].append(instance_id)

    # Format as list with affected instances
    return [
        {"blocker": blocker, "affected": instances}
        for blocker, instances in blockers.items()
    ]

def prioritize_decisions(instances):
    """Prioritize decisions from all instances"""
    decisions = []
    for instance in instances:
        instance_id = instance.get("instance_id", "UNKNOWN")
        role = instance.get("role", "UNKNOWN")

        for decision in instance.get("decisions_made", []):
            decisions.append({
                "decision": decision,
                "by": instance_id,
                "role": role,
                "weight": get_decision_weight(role)
            })

    # Sort by weight (C1 decisions have highest weight)
    return sorted(decisions, key=lambda x: x["weight"], reverse=True)

def get_decision_weight(role):
    """Get decision weight based on role"""
    weights = {
        "MECHANIC": 3,  # C1 has final say
        "ARCHITECT": 2,  # C2 has design authority
        "ORACLE": 1      # C3 provides guidance
    }
    return weights.get(role, 0)

def create_action_plan(instances):
    """Create consolidated action plan"""
    all_actions = []
    for instance in instances:
        instance_id = instance.get("instance_id", "UNKNOWN")
        actions = instance.get("next_actions", [])
        all_actions.extend([
            {"instance": instance_id, "action": action}
            for action in actions
        ])

    return all_actions

def aggregate_claude_outputs():
    """Main aggregation function"""

    # Load outputs from all Claude instances
    c1 = load_instance_output("C1")
    c2 = load_instance_output("C2")
    c3 = load_instance_output("C3")

    instances = [c1, c2, c3]

    # Create aggregated summary
    summary = {
        "timestamp": datetime.now().isoformat(),
        "layer": "CLAUDE_CODE_TRINITY",
        "instances": {
            "C1": c1.get("status", "UNKNOWN"),
            "C2": c2.get("status", "UNKNOWN"),
            "C3": c3.get("status", "UNKNOWN")
        },
        "summary": synthesize_insights(instances),
        "completed_tasks": merge_task_lists(instances),
        "blockers": consolidate_blockers(instances),
        "decisions": prioritize_decisions(instances),
        "next_actions": create_action_plan(instances),
        "health": {
            "instances_online": sum(1 for i in instances if i.get("status") != "NO_OUTPUT"),
            "total_instances": 3,
            "health_percentage": (sum(1 for i in instances if i.get("status") == "ACTIVE") / 3) * 100
        }
    }

    # Save summary
    SUMMARIES_DIR.mkdir(parents=True, exist_ok=True)
    summary_file = SUMMARIES_DIR / "claude_summary.json"

    with open(summary_file, 'w') as f:
        json.dump(summary, f, indent=2)

    print(f"✅ Claude summary created: {summary_file}")
    print(f"   Instances online: {summary['health']['instances_online']}/3")
    print(f"   Tasks completed: {len(summary['completed_tasks'])}")
    print(f"   Blockers: {len(summary['blockers'])}")

    return summary

if __name__ == "__main__":
    aggregate_claude_outputs()
