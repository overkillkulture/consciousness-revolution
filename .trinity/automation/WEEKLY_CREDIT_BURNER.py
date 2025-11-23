#!/usr/bin/env python3
"""
WEEKLY CREDIT BURNER
Automatically burns Max 20 credits productively each week across all computers.
Schedule this to run Sunday night on each computer.
"""

import os
import json
import subprocess
from datetime import datetime
from pathlib import Path

# Configuration
COMPUTER_ID = os.environ.get("COMPUTER_ID", "PC1")
TRINITY_DIR = Path.home() / "100X_DEPLOYMENT" / ".trinity"
TASKS_DIR = TRINITY_DIR / "tasks" / "pending"
OUTPUTS_DIR = TRINITY_DIR / "outputs" / COMPUTER_ID.lower()

# Weekly task allocation per computer
WEEKLY_TASKS = {
    "PC1": [
        {
            "id": "weekly-pc1-coord",
            "name": "Trinity Coordination Report",
            "prompt": "Analyze all .trinity files. Generate a weekly status report showing: completed tasks, active instances, system health, and recommendations for next week. Output as WEEKLY_REPORT_{date}.md",
            "credits": 5
        },
        {
            "id": "weekly-pc1-deploy",
            "name": "Deployment Pipeline Check",
            "prompt": "Review all pending deployments in outputs folder. Test each, fix issues, deploy to production. Document what was deployed.",
            "credits": 10
        },
        {
            "id": "weekly-pc1-optimize",
            "name": "System Optimization",
            "prompt": "Analyze codebase for: dead code, optimization opportunities, security issues. Fix top 5 issues. Commit fixes.",
            "credits": 5
        }
    ],
    "PC2": [
        {
            "id": "weekly-pc2-money",
            "name": "Opportunity Scanner",
            "prompt": "Research current crypto/market opportunities. Update opportunity_map.json with 5 new opportunities. Calculate ROI for each.",
            "credits": 10
        },
        {
            "id": "weekly-pc2-patterns",
            "name": "Pattern Detection Update",
            "prompt": "Analyze recent market data for new manipulation patterns. Add any new patterns to patterns.json. Test detection accuracy.",
            "credits": 10
        }
    ],
    "PC3": [
        {
            "id": "weekly-pc3-content",
            "name": "Content Generation",
            "prompt": "Generate 20 new viral posts for the week. Create 5 email sequences. Update content calendar. Push to content queue.",
            "credits": 10
        },
        {
            "id": "weekly-pc3-automation",
            "name": "Automation Health Check",
            "prompt": "Test all automation scripts. Fix any failures. Optimize slow processes. Document improvements.",
            "credits": 10
        }
    ]
}

def create_task_file(task):
    """Create a task file for the weekly work"""
    task_data = {
        "id": f"{task['id']}-{datetime.now().strftime('%Y%m%d')}",
        "name": task["name"],
        "prompt": task["prompt"],
        "estimated_credits": task["credits"],
        "computer": COMPUTER_ID,
        "created_at": datetime.utcnow().isoformat() + "Z",
        "status": "pending",
        "priority": "normal",
        "type": "weekly_burn"
    }

    TASKS_DIR.mkdir(parents=True, exist_ok=True)
    task_file = TASKS_DIR / f"{task_data['id']}.json"
    task_file.write_text(json.dumps(task_data, indent=2))
    print(f"Created task: {task_data['name']}")
    return task_file

def git_sync():
    """Sync with git repo"""
    repo_dir = Path.home() / "100X_DEPLOYMENT"
    subprocess.run(["git", "pull"], cwd=repo_dir)
    subprocess.run(["git", "add", "-A"], cwd=repo_dir)
    subprocess.run(["git", "commit", "-m", f"Weekly credit burn tasks for {COMPUTER_ID}"], cwd=repo_dir)
    subprocess.run(["git", "push"], cwd=repo_dir)

def main():
    print(f"=== WEEKLY CREDIT BURNER - {COMPUTER_ID} ===")
    print(f"Date: {datetime.now().strftime('%Y-%m-%d %H:%M')}")

    # Get tasks for this computer
    tasks = WEEKLY_TASKS.get(COMPUTER_ID, [])
    if not tasks:
        print(f"No tasks defined for {COMPUTER_ID}")
        return

    # Create task files
    total_credits = 0
    for task in tasks:
        create_task_file(task)
        total_credits += task["credits"]

    print(f"\nCreated {len(tasks)} tasks")
    print(f"Estimated credits: {total_credits}")

    # Sync to git
    git_sync()
    print("\nTasks synced to git. Ready for execution.")

    # Instructions
    print("\n=== NEXT STEPS ===")
    print("1. Open Claude Code terminal")
    print("2. Run: claude")
    print("3. Say: 'Check .trinity/tasks/pending and execute my weekly tasks'")
    print("4. Let it burn those credits productively!")

if __name__ == "__main__":
    main()
