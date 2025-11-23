#!/usr/bin/env python3
"""
OLLAMA OFFLINE BRIDGE
Processes tasks locally when internet is down.
Uses Ollama for local AI processing.
"""

import json
import time
import requests
import subprocess
from datetime import datetime
from pathlib import Path

TRINITY_DIR = Path.home() / "100X_DEPLOYMENT" / ".trinity"
OFFLINE_QUEUE = TRINITY_DIR / "offline_queue"
OFFLINE_OUTPUTS = TRINITY_DIR / "offline_outputs"
OLLAMA_URL = "http://localhost:11434"

class OllamaBridge:
    def __init__(self, model="llama3.2"):
        self.model = model
        self.is_online = True
        OFFLINE_QUEUE.mkdir(parents=True, exist_ok=True)
        OFFLINE_OUTPUTS.mkdir(parents=True, exist_ok=True)

    def check_internet(self):
        """Check if we have internet connectivity"""
        try:
            requests.get("https://api.anthropic.com", timeout=5)
            return True
        except:
            return False

    def check_ollama(self):
        """Check if Ollama is running"""
        try:
            response = requests.get(f"{OLLAMA_URL}/api/tags", timeout=5)
            return response.status_code == 200
        except:
            return False

    def start_ollama(self):
        """Start Ollama if not running"""
        if not self.check_ollama():
            print("Starting Ollama...")
            subprocess.Popen(["ollama", "serve"],
                           stdout=subprocess.DEVNULL,
                           stderr=subprocess.DEVNULL)
            time.sleep(3)

    def process_with_ollama(self, prompt):
        """Send prompt to Ollama and get response"""
        try:
            response = requests.post(
                f"{OLLAMA_URL}/api/generate",
                json={
                    "model": self.model,
                    "prompt": prompt,
                    "stream": False
                },
                timeout=300  # 5 minute timeout for long responses
            )

            if response.status_code == 200:
                return response.json().get("response", "")
            else:
                return f"Error: {response.status_code}"

        except Exception as e:
            return f"Ollama error: {e}"

    def queue_task(self, task_id, description, priority="normal"):
        """Add task to offline queue"""
        task = {
            "id": task_id,
            "description": description,
            "priority": priority,
            "queued_at": datetime.utcnow().isoformat() + "Z",
            "status": "pending"
        }

        task_file = OFFLINE_QUEUE / f"{task_id}.json"
        task_file.write_text(json.dumps(task, indent=2))
        print(f"📥 Queued for offline: {task_id}")

    def process_queue(self):
        """Process all pending offline tasks"""
        pending = list(OFFLINE_QUEUE.glob("*.json"))

        if not pending:
            print("No offline tasks pending")
            return

        print(f"Processing {len(pending)} offline tasks...")

        for task_file in pending:
            task = json.loads(task_file.read_text())

            if task.get("status") != "pending":
                continue

            print(f"\n🔄 Processing: {task['id']}")

            # Build prompt for Ollama
            prompt = f"""You are a helpful AI assistant working offline via Ollama.

Task ID: {task['id']}
Task Description:
{task['description']}

Please complete this task thoroughly. Provide actionable output.
"""

            # Process with Ollama
            result = self.process_with_ollama(prompt)

            # Save output
            output = {
                "task_id": task['id'],
                "description": task['description'],
                "result": result,
                "processed_at": datetime.utcnow().isoformat() + "Z",
                "model": self.model,
                "processed_offline": True
            }

            output_file = OFFLINE_OUTPUTS / f"{task['id']}_output.json"
            output_file.write_text(json.dumps(output, indent=2))

            # Also save as markdown for easy reading
            md_file = OFFLINE_OUTPUTS / f"{task['id']}_output.md"
            md_file.write_text(f"""# Offline Output: {task['id']}

**Processed:** {output['processed_at']}
**Model:** {self.model}

## Task
{task['description']}

## Result
{result}
""")

            # Mark task as complete
            task['status'] = 'completed'
            task['completed_at'] = datetime.utcnow().isoformat() + "Z"
            task_file.write_text(json.dumps(task, indent=2))

            print(f"✅ Completed: {task['id']}")

    def sync_outputs_to_git(self):
        """When internet returns, sync outputs to git"""
        if not self.check_internet():
            print("Still offline, can't sync")
            return

        repo = Path.home() / "100X_DEPLOYMENT"
        try:
            subprocess.run(["git", "add", "-A"], cwd=repo)
            subprocess.run(
                ["git", "commit", "-m", "offline bridge: sync outputs"],
                cwd=repo
            )
            subprocess.run(
                ["git", "push", "overkor-tek", "HEAD:master"],
                cwd=repo
            )
            print("📡 Offline outputs synced to git")
        except Exception as e:
            print(f"Sync error: {e}")

    def monitor_mode(self):
        """
        Continuous monitoring:
        - Check internet status
        - Process offline queue when disconnected
        - Sync when back online
        """
        print("=" * 50)
        print("  OLLAMA OFFLINE BRIDGE - Monitor Mode")
        print("=" * 50)
        print()

        self.start_ollama()

        was_online = True

        while True:
            is_online = self.check_internet()

            # State change detection
            if was_online and not is_online:
                print("\n⚠️ INTERNET DOWN - Switching to offline mode")
                print("Ollama will process queued tasks")

            if not was_online and is_online:
                print("\n✅ INTERNET RESTORED - Syncing outputs")
                self.sync_outputs_to_git()

            # Process queue if offline
            if not is_online:
                self.process_queue()

            was_online = is_online
            time.sleep(60)  # Check every minute

def main():
    """Demo the offline bridge"""
    bridge = OllamaBridge()

    print("=" * 50)
    print("  OLLAMA OFFLINE BRIDGE")
    print("=" * 50)
    print()

    # Check systems
    print(f"Internet: {'✅ Online' if bridge.check_internet() else '❌ Offline'}")
    print(f"Ollama: {'✅ Running' if bridge.check_ollama() else '❌ Not running'}")
    print()

    # Demo: queue a task
    bridge.queue_task(
        "offline-test-001",
        "Write a short summary of how distributed AI systems can work together.",
        "normal"
    )

    # If offline, process it
    if not bridge.check_internet():
        print("\nOffline mode - processing with Ollama...")
        bridge.process_queue()
    else:
        print("\nOnline mode - task queued for later if internet drops")
        print("Run with --monitor to continuously watch for offline periods")

if __name__ == "__main__":
    import sys

    if "--monitor" in sys.argv:
        bridge = OllamaBridge()
        bridge.monitor_mode()
    else:
        main()
