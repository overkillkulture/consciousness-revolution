#!/usr/bin/env python3
"""
CROSS-COMPUTER COORDINATION DAEMON
Runs on each computer to enable automatic wake-up and task coordination.
Uses git as the central nervous system.
"""

import os
import json
import time
import subprocess
from datetime import datetime
from pathlib import Path
import socket

# Configuration
COMPUTER_ID = os.environ.get("COMPUTER_ID", "PC1")
POLL_INTERVAL = 60  # seconds
TRINITY_DIR = Path.home() / "100X_DEPLOYMENT" / ".trinity"
HEARTBEAT_DIR = TRINITY_DIR / "heartbeats"
WAKE_DIR = TRINITY_DIR / "wake_signals"
TASKS_DIR = TRINITY_DIR / "tasks"

class CoordinationDaemon:
    def __init__(self):
        self.computer_id = COMPUTER_ID
        self.hostname = socket.gethostname()
        self.running = True

        # Create directories
        HEARTBEAT_DIR.mkdir(parents=True, exist_ok=True)
        WAKE_DIR.mkdir(parents=True, exist_ok=True)

    def update_heartbeat(self):
        """Update this computer's heartbeat file"""
        heartbeat = {
            "computer_id": self.computer_id,
            "hostname": self.hostname,
            "timestamp": datetime.utcnow().isoformat() + "Z",
            "status": "online",
            "ip": self.get_ip(),
            "tasks_pending": self.count_pending_tasks(),
            "last_git_sync": datetime.utcnow().isoformat() + "Z"
        }

        heartbeat_file = HEARTBEAT_DIR / f"{self.computer_id}.json"
        heartbeat_file.write_text(json.dumps(heartbeat, indent=2))

    def get_ip(self):
        """Get local IP address"""
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            s.connect(("8.8.8.8", 80))
            ip = s.getsockname()[0]
            s.close()
            return ip
        except:
            return "unknown"

    def count_pending_tasks(self):
        """Count pending tasks for this computer"""
        pending = TASKS_DIR / "pending"
        if not pending.exists():
            return 0
        count = 0
        for f in pending.glob("*.json"):
            task = json.loads(f.read_text())
            if task.get("computer") == self.computer_id or task.get("computer") is None:
                count += 1
        return count

    def check_wake_signals(self):
        """Check if another computer wants to wake us"""
        for signal_file in WAKE_DIR.glob(f"wake-{self.computer_id}-*.json"):
            signal = json.loads(signal_file.read_text())
            print(f"WAKE SIGNAL from {signal.get('from')}: {signal.get('reason')}")

            # Execute wake action
            self.handle_wake(signal)

            # Mark signal as processed
            signal_file.unlink()

    def handle_wake(self, signal):
        """Handle a wake signal"""
        action = signal.get("action", "notify")

        if action == "open_claude":
            # Open Claude Code terminal
            subprocess.Popen(["cmd", "/c", "start", "claude"], shell=True)
            print("Opened Claude Code terminal")

        elif action == "run_task":
            task_id = signal.get("task_id")
            print(f"Running task: {task_id}")
            # Could auto-execute task here

        elif action == "notify":
            # Just log it
            print(f"Notification: {signal.get('message')}")

    def send_wake_signal(self, target_computer, reason, action="notify"):
        """Send a wake signal to another computer"""
        signal = {
            "from": self.computer_id,
            "to": target_computer,
            "reason": reason,
            "action": action,
            "timestamp": datetime.utcnow().isoformat() + "Z"
        }

        signal_file = WAKE_DIR / f"wake-{target_computer}-{int(time.time())}.json"
        signal_file.write_text(json.dumps(signal, indent=2))

        # Git sync to propagate
        self.git_sync()
        print(f"Sent wake signal to {target_computer}")

    def git_sync(self):
        """Sync with git repo"""
        repo_dir = Path.home() / "100X_DEPLOYMENT"
        try:
            # Pull latest
            subprocess.run(["git", "pull", "--rebase"], cwd=repo_dir,
                         capture_output=True, timeout=30)

            # Push our changes
            subprocess.run(["git", "add", "-A"], cwd=repo_dir, timeout=10)
            result = subprocess.run(
                ["git", "commit", "-m", f"daemon: {self.computer_id} heartbeat"],
                cwd=repo_dir, capture_output=True, timeout=10
            )
            if result.returncode == 0:
                subprocess.run(["git", "push"], cwd=repo_dir, timeout=30)
        except Exception as e:
            print(f"Git sync error: {e}")

    def check_other_computers(self):
        """Check status of other computers"""
        for hb_file in HEARTBEAT_DIR.glob("*.json"):
            if hb_file.stem == self.computer_id:
                continue

            hb = json.loads(hb_file.read_text())
            last_seen = datetime.fromisoformat(hb["timestamp"].replace("Z", ""))
            age = (datetime.utcnow() - last_seen).total_seconds()

            if age > 300:  # 5 minutes
                print(f"WARNING: {hb_file.stem} last seen {int(age)}s ago")
            else:
                print(f"{hb_file.stem}: online, {hb.get('tasks_pending', 0)} tasks pending")

    def run(self):
        """Main daemon loop"""
        print(f"=== COORDINATION DAEMON - {self.computer_id} ===")
        print(f"Polling every {POLL_INTERVAL} seconds")
        print("Press Ctrl+C to stop\n")

        while self.running:
            try:
                # Update our heartbeat
                self.update_heartbeat()

                # Sync with git
                self.git_sync()

                # Check for wake signals
                self.check_wake_signals()

                # Check other computers
                self.check_other_computers()

                # Check for pending tasks
                pending = self.count_pending_tasks()
                if pending > 0:
                    print(f"\n{pending} tasks pending for {self.computer_id}")

                print(f"[{datetime.now().strftime('%H:%M:%S')}] Heartbeat sent")

            except KeyboardInterrupt:
                self.running = False
                print("\nDaemon stopped")
                break
            except Exception as e:
                print(f"Error: {e}")

            time.sleep(POLL_INTERVAL)

if __name__ == "__main__":
    daemon = CoordinationDaemon()
    daemon.run()
