#!/usr/bin/env python3
"""
AUTONOMOUS TASK RUNNER
Runs tasks through the brain agent pipeline with Cyclotron integration.
The autonomous execution engine for C2's brain.
"""

import json
import sys
from pathlib import Path
from datetime import datetime
from typing import Optional, List

# Import our systems
from ADVANCED_BRAIN_AGENTS import AdvancedOrchestrator
from CYCLOTRON_BRAIN_BRIDGE import CyclotronBridge

# Paths
HOME = Path.home()
CONSCIOUSNESS = HOME / ".consciousness"
TASKS_PATH = CONSCIOUSNESS / "task_queue"
RESULTS_PATH = CONSCIOUSNESS / "task_results"

TASKS_PATH.mkdir(parents=True, exist_ok=True)
RESULTS_PATH.mkdir(parents=True, exist_ok=True)


class AutonomousRunner:
    """Autonomous task execution with full brain integration."""

    def __init__(self):
        self.orchestrator = AdvancedOrchestrator()
        self.cyclotron = CyclotronBridge()
        self.execution_log = []

    def run_task(self, task: str, mode: str = "advanced") -> dict:
        """
        Run a task through the brain pipeline.

        Args:
            task: Task description
            mode: "quick", "research", or "advanced" (default)

        Returns:
            Complete execution result
        """
        print("\n" + "=" * 60)
        print("AUTONOMOUS TASK EXECUTION")
        print("=" * 60)
        print(f"Task: {task[:80]}...")
        print(f"Mode: {mode}")
        print(f"Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print()

        # Run through orchestrator
        if mode == "quick":
            state = self.orchestrator.run_quick(task)
        elif mode == "research":
            state = self.orchestrator.run_research(task)
        else:
            state = self.orchestrator.run_advanced(task)

        # Store results in Cyclotron
        print("\nStoring results in Cyclotron...")
        atoms = self.cyclotron.store_agent_output(
            agent_name="autonomous_runner",
            task=task,
            outputs=state.outputs,
            decisions=state.decisions,
            memory=state.memory
        )

        # Create result report
        result = {
            "task": task,
            "mode": mode,
            "status": state.status,
            "timestamp": datetime.now().isoformat(),
            "outputs": state.outputs,
            "decisions": state.decisions,
            "memory": state.memory,
            "context": {
                "pattern_analysis": state.context.get("pattern_analysis"),
                "plan": state.context.get("plan"),
                "synthesis": state.context.get("synthesis"),
                "cyclotron_atoms": len(state.context.get("cyclotron_atoms", [])),
                "knowledge_entities": len(state.context.get("knowledge", {}).get("entities", [])),
                "related_memories": len(state.context.get("related_memories", []))
            },
            "atoms_created": len(atoms),
            "agent_sequence": state.context.get("agent_sequence", [])
        }

        # Save result
        result_file = RESULTS_PATH / f"result_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        with open(result_file, 'w') as f:
            json.dump(result, f, indent=2)

        # Log execution
        self.execution_log.append({
            "task": task[:50],
            "mode": mode,
            "status": state.status,
            "timestamp": datetime.now().isoformat()
        })

        # Print summary
        self._print_summary(result)

        return result

    def _print_summary(self, result: dict):
        """Print execution summary."""
        print("\n" + "=" * 60)
        print("EXECUTION SUMMARY")
        print("=" * 60)

        print(f"Status: {result['status']}")
        print(f"Mode: {result['mode']}")
        print(f"Outputs: {len(result['outputs'])}")
        print(f"Decisions: {len(result['decisions'])}")
        print(f"Memory items: {len(result['memory'])}")
        print(f"Atoms created: {result['atoms_created']}")

        # Show decisions
        if result['decisions']:
            print("\nDecisions Made:")
            for d in result['decisions']:
                print(f"  • {d.get('decision', 'N/A')}")

        # Show pattern analysis
        if result['context'].get('pattern_analysis'):
            pa = result['context']['pattern_analysis']
            print(f"\nThreat Level: {pa.get('threat_level', 'N/A')}")

        # Show synthesis
        if result['context'].get('synthesis'):
            syn = result['context']['synthesis']
            print(f"\nSynthesis: {syn.get('summary', 'N/A')}")

    def run_batch(self, tasks: List[str], mode: str = "advanced") -> List[dict]:
        """Run multiple tasks."""
        results = []

        print("\n" + "=" * 60)
        print(f"BATCH EXECUTION: {len(tasks)} tasks")
        print("=" * 60)

        for i, task in enumerate(tasks, 1):
            print(f"\n[{i}/{len(tasks)}] Running task...")
            result = self.run_task(task, mode)
            results.append(result)

        # Batch summary
        print("\n" + "=" * 60)
        print("BATCH COMPLETE")
        print("=" * 60)
        print(f"Tasks: {len(tasks)}")
        print(f"Successful: {sum(1 for r in results if r['status'] == 'complete')}")

        return results

    def queue_task(self, task: str, priority: str = "normal", mode: str = "advanced"):
        """Add task to queue for later execution."""
        task_data = {
            "task": task,
            "priority": priority,
            "mode": mode,
            "queued_at": datetime.now().isoformat(),
            "status": "pending"
        }

        task_file = TASKS_PATH / f"task_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        with open(task_file, 'w') as f:
            json.dump(task_data, f, indent=2)

        print(f"Queued task: {task[:50]}...")
        return task_file

    def process_queue(self) -> List[dict]:
        """Process all queued tasks."""
        results = []

        # Get pending tasks
        task_files = sorted(TASKS_PATH.glob("*.json"))

        pending = []
        for tf in task_files:
            with open(tf) as f:
                task_data = json.load(f)
            if task_data.get("status") == "pending":
                pending.append((tf, task_data))

        if not pending:
            print("No pending tasks in queue")
            return results

        # Sort by priority
        priority_order = {"urgent": 0, "high": 1, "normal": 2, "low": 3}
        pending.sort(key=lambda x: priority_order.get(x[1].get("priority", "normal"), 2))

        print(f"\nProcessing {len(pending)} queued tasks...")

        for task_file, task_data in pending:
            result = self.run_task(task_data["task"], task_data.get("mode", "advanced"))
            results.append(result)

            # Update task status
            task_data["status"] = "completed"
            task_data["completed_at"] = datetime.now().isoformat()
            with open(task_file, 'w') as f:
                json.dump(task_data, f, indent=2)

        return results

    def get_status(self) -> dict:
        """Get runner status."""
        # Count tasks
        pending = 0
        completed = 0

        for tf in TASKS_PATH.glob("*.json"):
            with open(tf) as f:
                data = json.load(f)
            if data.get("status") == "pending":
                pending += 1
            else:
                completed += 1

        # Count results
        results = len(list(RESULTS_PATH.glob("*.json")))

        # Cyclotron status
        cyclotron_status = self.cyclotron.get_status()

        return {
            "pending_tasks": pending,
            "completed_tasks": completed,
            "total_results": results,
            "executions_this_session": len(self.execution_log),
            "cyclotron_atoms": cyclotron_status["total_atoms"],
            "cyclotron_tags": cyclotron_status["tag_count"]
        }


def demo():
    """Demonstrate autonomous task runner."""
    print("=" * 60)
    print("AUTONOMOUS TASK RUNNER DEMO")
    print("=" * 60)

    runner = AutonomousRunner()

    # Run some tasks
    tasks = [
        "Analyze the security implications of using harmonic encryption for API keys",
        "Research best practices for multi-agent coordination patterns",
        "Plan the integration between Trinity and Cyclotron knowledge systems"
    ]

    for task in tasks:
        runner.run_task(task)

    # Show status
    print("\n" + "=" * 60)
    print("RUNNER STATUS")
    print("=" * 60)

    status = runner.get_status()
    for key, value in status.items():
        print(f"{key}: {value}")


def main():
    """CLI for autonomous runner."""
    runner = AutonomousRunner()

    if len(sys.argv) < 2:
        print("Autonomous Task Runner")
        print("=" * 40)
        print("\nCommands:")
        print("  run <task>           - Run task immediately")
        print("  quick <task>         - Run task in quick mode")
        print("  research <task>      - Run task in research mode")
        print("  queue <task>         - Queue task for later")
        print("  process              - Process queued tasks")
        print("  status               - Show runner status")
        print("  demo                 - Run demo")

        status = runner.get_status()
        print(f"\nCurrent status:")
        print(f"  Pending: {status['pending_tasks']}")
        print(f"  Cyclotron: {status['cyclotron_atoms']} atoms")
        return

    command = sys.argv[1]

    if command == "demo":
        demo()

    elif command == "run" and len(sys.argv) >= 3:
        task = " ".join(sys.argv[2:])
        runner.run_task(task, "advanced")

    elif command == "quick" and len(sys.argv) >= 3:
        task = " ".join(sys.argv[2:])
        runner.run_task(task, "quick")

    elif command == "research" and len(sys.argv) >= 3:
        task = " ".join(sys.argv[2:])
        runner.run_task(task, "research")

    elif command == "queue" and len(sys.argv) >= 3:
        task = " ".join(sys.argv[2:])
        runner.queue_task(task)

    elif command == "process":
        runner.process_queue()

    elif command == "status":
        status = runner.get_status()
        print("\nRunner Status:")
        for key, value in status.items():
            print(f"  {key}: {value}")

    else:
        print(f"Unknown command: {command}")


if __name__ == "__main__":
    main()
