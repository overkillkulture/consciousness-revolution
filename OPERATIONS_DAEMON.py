#!/usr/bin/env python3
"""
OPERATIONS DAEMON
Background service that coordinates all Consciousness Revolution automation.
Runs scheduled tasks, monitors health, and manages data lifecycle.
"""

import json
import time
import subprocess
import schedule
from pathlib import Path
from datetime import datetime
import threading

# Paths
HOME = Path.home()
DEPLOYMENT = HOME / "100X_DEPLOYMENT"
CONSCIOUSNESS = HOME / ".consciousness"
LOG_PATH = CONSCIOUSNESS / "daemon_log.json"

class OperationsDaemon:
    """Central operations coordinator."""

    def __init__(self):
        self.running = False
        self.log = []
        self.stats = {
            "started": None,
            "tasks_run": 0,
            "errors": 0,
            "last_run": {}
        }

    def start(self):
        """Start the daemon."""
        self.running = True
        self.stats["started"] = datetime.now().isoformat()

        print("=" * 50)
        print("OPERATIONS DAEMON STARTED")
        print("=" * 50)
        print(f"Time: {datetime.now()}")
        print()

        # Schedule tasks
        self._setup_schedule()

        # Main loop
        while self.running:
            schedule.run_pending()
            time.sleep(60)  # Check every minute

    def stop(self):
        """Stop the daemon."""
        self.running = False
        self._save_log()
        print("\nDaemon stopped.")

    def _setup_schedule(self):
        """Set up all scheduled tasks."""

        # Every hour
        schedule.every().hour.do(self._run_task, "health_check", self.health_check)

        # Every 6 hours
        schedule.every(6).hours.do(self._run_task, "data_rotation", self.data_rotation)

        # Daily at 6 AM
        schedule.every().day.at("06:00").do(self._run_task, "daily_automation", self.daily_automation)

        # Daily at 9 AM
        schedule.every().day.at("09:00").do(self._run_task, "scorecard_update", self.scorecard_update)

        # Monday at 8 AM (weekly)
        schedule.every().monday.at("08:00").do(self._run_task, "weekly_automation", self.weekly_automation)

        # Monday at 9 AM (L10 prep)
        schedule.every().monday.at("09:00").do(self._run_task, "l10_prep", self.l10_prep)

        print("Scheduled tasks:")
        print("  - Health check: Every hour")
        print("  - Data rotation: Every 6 hours")
        print("  - Daily automation: 6:00 AM")
        print("  - Scorecard update: 9:00 AM")
        print("  - Weekly automation: Monday 8:00 AM")
        print("  - L10 prep: Monday 9:00 AM")
        print()

    def _run_task(self, name: str, task_func):
        """Run a task with logging."""
        start_time = datetime.now()

        try:
            self._log(f"Starting task: {name}")
            result = task_func()
            self._log(f"Completed task: {name}", result)
            self.stats["tasks_run"] += 1
            self.stats["last_run"][name] = {
                "time": start_time.isoformat(),
                "status": "success",
                "result": result
            }
        except Exception as e:
            self._log(f"Error in task {name}: {str(e)}", error=True)
            self.stats["errors"] += 1
            self.stats["last_run"][name] = {
                "time": start_time.isoformat(),
                "status": "error",
                "error": str(e)
            }

        self._save_log()

    def _log(self, message: str, data=None, error=False):
        """Log a message."""
        entry = {
            "timestamp": datetime.now().isoformat(),
            "message": message,
            "data": data,
            "error": error
        }
        self.log.append(entry)

        # Print to console
        prefix = "❌" if error else "✅"
        print(f"{prefix} [{datetime.now().strftime('%H:%M:%S')}] {message}")

        # Keep log manageable
        if len(self.log) > 1000:
            self.log = self.log[-500:]

    def _save_log(self):
        """Save log to disk."""
        output = {
            "stats": self.stats,
            "log": self.log[-100:]  # Last 100 entries
        }
        with open(LOG_PATH, 'w') as f:
            json.dump(output, f, indent=2)

    # Task implementations

    def health_check(self) -> dict:
        """Check system health."""
        health = {
            "timestamp": datetime.now().isoformat(),
            "checks": {}
        }

        # Check critical directories
        critical_dirs = [
            HOME / ".consciousness",
            HOME / ".planning",
            HOME / ".archives",
            DEPLOYMENT
        ]

        for dir_path in critical_dirs:
            health["checks"][str(dir_path)] = dir_path.exists()

        # Check critical files
        critical_files = [
            HOME / ".planning" / "traction" / "SCORECARD_WEEKLY.json",
            HOME / ".planning" / "traction" / "ROCKS_Q4_2025.json"
        ]

        for file_path in critical_files:
            health["checks"][str(file_path)] = file_path.exists()

        # Calculate overall health
        total = len(health["checks"])
        healthy = sum(1 for v in health["checks"].values() if v)
        health["score"] = round(healthy / total * 100, 1)

        return health

    def data_rotation(self) -> dict:
        """Run temporal data rotation."""
        result = subprocess.run(
            ["python", str(DEPLOYMENT / "TEMPORAL_DATA_ROTATION.py")],
            capture_output=True, text=True, timeout=300
        )
        return {
            "returncode": result.returncode,
            "stdout_lines": len(result.stdout.split('\n'))
        }

    def daily_automation(self) -> dict:
        """Run daily automation suite."""
        results = {}

        # Scorecard
        result = subprocess.run(
            ["python", str(DEPLOYMENT / "SCORECARD_AUTOMATOR.py")],
            capture_output=True, text=True, timeout=120
        )
        results["scorecard"] = result.returncode == 0

        # Data rotation
        result = subprocess.run(
            ["python", str(DEPLOYMENT / "TEMPORAL_DATA_ROTATION.py")],
            capture_output=True, text=True, timeout=300
        )
        results["rotation"] = result.returncode == 0

        return results

    def scorecard_update(self) -> dict:
        """Update scorecard metrics."""
        result = subprocess.run(
            ["python", str(DEPLOYMENT / "SCORECARD_AUTOMATOR.py")],
            capture_output=True, text=True, timeout=120
        )
        return {
            "returncode": result.returncode,
            "output": result.stdout[-500:] if result.stdout else ""
        }

    def weekly_automation(self) -> dict:
        """Run weekly automation suite."""
        # Generate scorecard report
        result = subprocess.run(
            ["python", str(DEPLOYMENT / "SCORECARD_AUTOMATOR.py"), "report"],
            capture_output=True, text=True, timeout=120
        )
        return {"report_generated": result.returncode == 0}

    def l10_prep(self) -> dict:
        """Prepare L10 meeting materials."""
        result = subprocess.run(
            ["python", str(DEPLOYMENT / "L10_MEETING_AUTOMATION.py"), "agenda"],
            capture_output=True, text=True, timeout=120
        )
        return {
            "agenda_generated": result.returncode == 0
        }

def main():
    """Run the operations daemon."""
    import sys

    if len(sys.argv) > 1 and sys.argv[1] == "status":
        # Show daemon status
        if LOG_PATH.exists():
            with open(LOG_PATH) as f:
                data = json.load(f)
            print("\n📊 DAEMON STATUS\n")
            print(f"Started: {data['stats'].get('started', 'Unknown')}")
            print(f"Tasks run: {data['stats'].get('tasks_run', 0)}")
            print(f"Errors: {data['stats'].get('errors', 0)}")
            print("\nLast runs:")
            for task, info in data['stats'].get('last_run', {}).items():
                status = "✅" if info.get('status') == 'success' else "❌"
                print(f"  {status} {task}: {info.get('time', 'Never')}")
        else:
            print("Daemon has not been started yet.")
    else:
        # Start daemon
        daemon = OperationsDaemon()
        try:
            daemon.start()
        except KeyboardInterrupt:
            daemon.stop()

if __name__ == "__main__":
    main()
