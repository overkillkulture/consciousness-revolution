#!/usr/bin/env python3
"""
Trinity Aggregator 2: Terminal Instance Aggregator
Combines outputs from T1, T2, T3 into Summary₂
"""

import json
import os
from datetime import datetime
from pathlib import Path

TRINITY_DIR = Path(".consciousness/trinity")
TERMINAL_DIR = TRINITY_DIR / "terminal"
SUMMARIES_DIR = TRINITY_DIR / "summaries"

def load_instance_output(instance_id):
    """Load output from a Terminal instance"""
    output_file = TERMINAL_DIR / f"{instance_id.lower()}_output.json"

    if not output_file.exists():
        return {
            "instance_id": instance_id,
            "status": "NO_OUTPUT",
            "timestamp": None,
            "commands_executed": [],
            "system_metrics": {},
            "errors": [],
            "logs": [],
            "alerts": []
        }

    with open(output_file, 'r') as f:
        return json.load(f)

def merge_logs(instances):
    """Merge logs from all terminal instances"""
    all_logs = []
    for instance in instances:
        instance_id = instance.get("instance_id", "UNKNOWN")
        logs = instance.get("logs", [])
        all_logs.extend([
            {"instance": instance_id, "log": log}
            for log in logs
        ])

    # Sort by timestamp if available
    return all_logs

def combine_status(instances):
    """Combine system status from all instances"""
    combined = {
        "overall": "HEALTHY",
        "instances": {}
    }

    for instance in instances:
        instance_id = instance.get("instance_id", "UNKNOWN")
        metrics = instance.get("system_metrics", {})
        combined["instances"][instance_id] = {
            "metrics": metrics,
            "status": instance.get("status", "UNKNOWN")
        }

    # Determine overall health
    active = sum(1 for i in instances if i.get("status") == "ACTIVE")
    if active == 0:
        combined["overall"] = "CRITICAL"
    elif active < 3:
        combined["overall"] = "DEGRADED"

    return combined

def consolidate_errors(instances):
    """Consolidate errors from all instances"""
    errors = {}
    for instance in instances:
        instance_id = instance.get("instance_id", "UNKNOWN")
        for error in instance.get("errors", []):
            if error not in errors:
                errors[error] = []
            errors[error].append(instance_id)

    return [
        {"error": error, "affected": instances}
        for error, instances in errors.items()
    ]

def aggregate_metrics(instances):
    """Aggregate system metrics from all instances"""
    metrics = {
        "cpu": [],
        "memory": [],
        "disk": []
    }

    for instance in instances:
        sys_metrics = instance.get("system_metrics", {})
        if "cpu" in sys_metrics:
            metrics["cpu"].append(sys_metrics["cpu"])
        if "memory" in sys_metrics:
            metrics["memory"].append(sys_metrics["memory"])
        if "disk" in sys_metrics:
            metrics["disk"].append(sys_metrics["disk"])

    # Calculate averages
    aggregated = {}
    for key, values in metrics.items():
        if values:
            aggregated[f"{key}_avg"] = sum(values) / len(values)
            aggregated[f"{key}_max"] = max(values)
            aggregated[f"{key}_min"] = min(values)

    return aggregated

def prioritize_alerts(instances):
    """Prioritize alerts from all instances"""
    all_alerts = []

    for instance in instances:
        instance_id = instance.get("instance_id", "UNKNOWN")
        alerts = instance.get("alerts", [])

        for alert in alerts:
            all_alerts.append({
                "alert": alert,
                "from": instance_id,
                "priority": get_alert_priority(alert)
            })

    # Sort by priority
    return sorted(all_alerts, key=lambda x: x["priority"], reverse=True)

def get_alert_priority(alert):
    """Get alert priority based on keywords"""
    alert_lower = alert.lower()
    if "critical" in alert_lower or "error" in alert_lower:
        return 3
    elif "warning" in alert_lower:
        return 2
    else:
        return 1

def aggregate_terminal_outputs():
    """Main aggregation function"""

    # Load outputs from all Terminal instances
    t1 = load_instance_output("T1")
    t2 = load_instance_output("T2")
    t3 = load_instance_output("T3")

    instances = [t1, t2, t3]

    # Create aggregated summary
    summary = {
        "timestamp": datetime.now().isoformat(),
        "layer": "TERMINAL_TRINITY",
        "instances": {
            "T1": t1.get("status", "UNKNOWN"),
            "T2": t2.get("status", "UNKNOWN"),
            "T3": t3.get("status", "UNKNOWN")
        },
        "execution_logs": merge_logs(instances),
        "system_status": combine_status(instances),
        "errors": consolidate_errors(instances),
        "metrics": aggregate_metrics(instances),
        "alerts": prioritize_alerts(instances),
        "health": {
            "instances_online": sum(1 for i in instances if i.get("status") != "NO_OUTPUT"),
            "total_instances": 3,
            "health_percentage": (sum(1 for i in instances if i.get("status") == "ACTIVE") / 3) * 100
        }
    }

    # Save summary
    SUMMARIES_DIR.mkdir(parents=True, exist_ok=True)
    summary_file = SUMMARIES_DIR / "terminal_summary.json"

    with open(summary_file, 'w') as f:
        json.dump(summary, f, indent=2)

    print(f"✅ Terminal summary created: {summary_file}")
    print(f"   Instances online: {summary['health']['instances_online']}/3")
    print(f"   Errors: {len(summary['errors'])}")
    print(f"   Alerts: {len(summary['alerts'])}")

    return summary

if __name__ == "__main__":
    aggregate_terminal_outputs()
