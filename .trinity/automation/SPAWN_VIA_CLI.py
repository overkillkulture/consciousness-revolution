#!/usr/bin/env python3
"""
SPAWN VIA CLI
Creates task files that Claude Code instances can pick up.
Works with existing Max plan credits - no separate API key needed.
"""

import json
from datetime import datetime
from pathlib import Path
import subprocess

TRINITY_DIR = Path.home() / "100X_DEPLOYMENT" / ".trinity"
SPAWN_QUEUE = TRINITY_DIR / "spawn_queue"

class CLISpawner:
    def __init__(self):
        SPAWN_QUEUE.mkdir(parents=True, exist_ok=True)

    def create_spawn_task(self, task_description, task_id=None, priority="normal"):
        """
        Create a task file for a Cloud Code instance to pick up.
        The user (or phone) opens Claude Code and points it at this task.
        """
        if not task_id:
            task_id = f"spawn-{int(datetime.now().timestamp())}"

        task = {
            "id": task_id,
            "type": "cloud_spawn",
            "description": task_description,
            "priority": priority,
            "created_at": datetime.utcnow().isoformat() + "Z",
            "status": "pending",
            "instructions": f"""
=== CLOUD WORKER TASK ===

Task ID: {task_id}
Created: {datetime.now().strftime('%Y-%m-%d %H:%M')}

YOUR MISSION:
{task_description}

WHEN DONE:
1. Save output to: .trinity/cloud_outputs/{task_id}.md
2. Git commit with message: "cloud worker: {task_id} complete"
3. Git push

=== BEGIN WORK ===
"""
        }

        # Save task file
        task_file = SPAWN_QUEUE / f"{task_id}.json"
        task_file.write_text(json.dumps(task, indent=2))

        # Also create a markdown version for easy copy-paste
        md_file = SPAWN_QUEUE / f"{task_id}.md"
        md_file.write_text(task["instructions"])

        print(f"Spawn task created: {task_id}")
        print(f"  JSON: {task_file}")
        print(f"  Instructions: {md_file}")

        return task_id

    def create_swarm(self, tasks):
        """Create multiple spawn tasks"""
        ids = []
        for i, task in enumerate(tasks):
            task_id = self.create_spawn_task(
                task["description"],
                task.get("id", f"swarm-{i}"),
                task.get("priority", "normal")
            )
            ids.append(task_id)
        return ids

    def list_pending(self):
        """List pending spawn tasks"""
        tasks = []
        for f in SPAWN_QUEUE.glob("*.json"):
            task = json.loads(f.read_text())
            if task.get("status") == "pending":
                tasks.append(task)
        return tasks

    def git_sync(self):
        """Push spawn queue to git"""
        repo = Path.home() / "100X_DEPLOYMENT"
        subprocess.run(["git", "add", "-A"], cwd=repo)
        subprocess.run(["git", "commit", "-m", "spawn tasks queued"], cwd=repo)
        subprocess.run(["git", "push"], cwd=repo)
        print("Spawn queue synced to git")

def main():
    """Demo: Create spawn tasks for CBT chunks"""
    spawner = CLISpawner()

    # Create tasks for each CBT chunk
    tasks = [
        {
            "id": "chunk2-courses",
            "description": """
CHUNK 2 PART 1: Pattern Theory Courses

Create complete curriculum for 3-tier course system:

TIER 1 ($99):
- 10 video lesson outlines (300-500 words each)
- 20 quiz questions
- 1 PDF workbook outline

TIER 2 ($299):
- 20 additional lesson outlines
- 10 case studies
- Community structure design

TIER 3 ($999):
- Certification exam (50 questions)
- 1-on-1 consultation outline
- Business startup kit contents

Output as: tier1_curriculum.md, tier2_curriculum.md, tier3_curriculum.md
""",
            "priority": "high"
        },
        {
            "id": "chunk2-book",
            "description": """
CHUNK 2 PART 2: Book Manuscript

"Manipulation Immunity: The Pattern Theory Guide"

Create:
1. Full chapter outline (15 chapters)
2. Chapter 1 complete (2000 words) - The Problem
3. Chapter 3 complete (2500 words) - The Formula
4. Chapter 10 complete (2000 words) - The Five Phases

Include publishing plan for Amazon KDP.

Output as: book_outline.md, chapter_01.md, chapter_03.md, chapter_10.md
""",
            "priority": "high"
        },
        {
            "id": "chunk2-viral",
            "description": """
CHUNK 2 PART 3: Viral Content

Create 100 viral posts for Pattern Theory:
- 25 pattern explanations
- 15 federal case awareness
- 25 manipulation examples
- 10 success stories
- 25 call-to-action

Plus:
- Welcome email sequence (5 emails)
- Sales email sequence (7 emails)

Output as: viral_posts.md, email_sequences.md
""",
            "priority": "normal"
        }
    ]

    print("=== CREATING CBT CHUNK 2 SPAWN TASKS ===\n")

    for task in tasks:
        spawner.create_spawn_task(task["description"], task["id"], task["priority"])
        print()

    # Sync to git
    spawner.git_sync()

    print("\n=== SPAWN TASKS READY ===")
    print("\nTo execute:")
    print("1. Open Cloud Code (browser or phone)")
    print("2. git pull")
    print("3. Read task from .trinity/spawn_queue/")
    print("4. Complete the work")
    print("5. Commit and push output")
    print("\nOr open multiple Cloud Code instances for parallel work!")

if __name__ == "__main__":
    main()
