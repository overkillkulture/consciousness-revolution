#!/usr/bin/env python3
"""
CLOUD SPAWNER
Actually spawns cloud Claude instances via API.
Each spawned instance works on a task and commits results to git.
"""

import os
import json
import anthropic
from datetime import datetime
from pathlib import Path

# Configuration
ANTHROPIC_API_KEY = os.environ.get("ANTHROPIC_API_KEY")
TRINITY_DIR = Path.home() / "100X_DEPLOYMENT" / ".trinity"
OUTPUTS_DIR = TRINITY_DIR / "cloud_outputs"

class CloudSpawner:
    def __init__(self):
        if not ANTHROPIC_API_KEY:
            raise ValueError("ANTHROPIC_API_KEY not set")
        self.client = anthropic.Anthropic(api_key=ANTHROPIC_API_KEY)
        OUTPUTS_DIR.mkdir(parents=True, exist_ok=True)

    def spawn(self, task_description, task_id=None):
        """
        Spawn a cloud worker to complete a task.
        Returns the worker's output.
        """
        if not task_id:
            task_id = f"cloud-{int(datetime.now().timestamp())}"

        print(f"Spawning cloud worker: {task_id}")
        print(f"Task: {task_description[:100]}...")

        # Build the system prompt
        system_prompt = """You are a Cloud Worker in the Trinity system.
Your job is to complete the assigned task thoroughly and return structured output.

RULES:
1. Complete the task fully
2. Return output as markdown
3. Be specific and actionable
4. Include any code, data, or artifacts requested
5. Note any issues or blockers encountered

OUTPUT FORMAT:
Start with a brief summary, then provide detailed results.
End with "TASK COMPLETE" when done."""

        # Call Claude API
        try:
            response = self.client.messages.create(
                model="claude-sonnet-4-20250514",
                max_tokens=8000,
                system=system_prompt,
                messages=[
                    {"role": "user", "content": task_description}
                ]
            )

            output = response.content[0].text

            # Save output
            output_file = OUTPUTS_DIR / f"{task_id}.md"
            output_file.write_text(f"# Cloud Worker Output: {task_id}\n\n"
                                  f"**Task:** {task_description}\n\n"
                                  f"**Completed:** {datetime.now().isoformat()}\n\n"
                                  f"---\n\n{output}")

            print(f"Output saved to: {output_file}")

            # Log usage
            usage = {
                "task_id": task_id,
                "input_tokens": response.usage.input_tokens,
                "output_tokens": response.usage.output_tokens,
                "timestamp": datetime.now().isoformat()
            }
            print(f"Tokens used: {usage['input_tokens']} in, {usage['output_tokens']} out")

            return output

        except Exception as e:
            print(f"Spawn error: {e}")
            return None

    def spawn_swarm(self, tasks):
        """
        Spawn multiple workers in sequence.
        (True parallel would need async/threading)
        """
        results = []
        for i, task in enumerate(tasks):
            print(f"\n=== Worker {i+1}/{len(tasks)} ===")
            result = self.spawn(task["description"], task.get("id"))
            results.append({
                "task": task,
                "output": result,
                "success": result is not None
            })
        return results

def main():
    """Test the spawner"""
    spawner = CloudSpawner()

    # Test task
    test_task = """
    Analyze the CBT Protocol v2.0 concept:
    - 3 computers working in parallel
    - Each with Trinity instances
    - Coordinated via git

    Provide:
    1. Three potential failure modes
    2. Three optimization opportunities
    3. One creative enhancement idea

    Be concise but specific.
    """

    result = spawner.spawn(test_task, "test-spawn-001")

    if result:
        print("\n=== SPAWN SUCCESSFUL ===")
        print(result[:500] + "...")
    else:
        print("\n=== SPAWN FAILED ===")

if __name__ == "__main__":
    main()
