#!/usr/bin/env python3
"""
consciousness_sync.py - Cross-platform auto-sync for consciousness network
Monitors Git repo for changes and provides smart notifications
"""

import os
import sys
import time
import subprocess
from datetime import datetime
from pathlib import Path

class ConsciousnessSync:
    def __init__(self, repo_path=None, sync_interval=300, computer_id="SWAN_ARCHITECT"):
        self.repo_path = Path(repo_path or os.path.dirname(os.path.abspath(__file__)))
        self.sync_interval = sync_interval
        self.computer_id = computer_id
        self.my_inbox = self.repo_path / ".consciousness/commands/computer_2_inbox.md"
        self.file_transfers = self.repo_path / ".consciousness/file_transfers"

    def log(self, message, level="INFO"):
        """Print timestamped log message"""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        print(f"[{timestamp}] {level}: {message}")

    def run_git_command(self, args):
        """Execute git command and return output"""
        try:
            result = subprocess.run(
                ["git"] + args,
                cwd=self.repo_path,
                capture_output=True,
                text=True,
                timeout=30
            )
            return result.returncode, result.stdout, result.stderr
        except subprocess.TimeoutExpired:
            return -1, "", "Command timed out"
        except Exception as e:
            return -1, "", str(e)

    def check_for_updates(self):
        """Pull latest changes from remote"""
        returncode, stdout, stderr = self.run_git_command(["pull", "--quiet"])

        if returncode == 0:
            if "Already up to date" in stdout:
                return False, "No updates"
            return True, stdout.strip()
        else:
            return False, f"Pull failed: {stderr}"

    def check_new_commands(self):
        """Check for new commands in recent commits"""
        # Check commits from last sync interval
        minutes_ago = (self.sync_interval // 60) + 1

        returncode, stdout, stderr = self.run_git_command([
            "log",
            f"--since={minutes_ago} minutes ago",
            "--grep=Computer 2:",
            "--oneline"
        ])

        if returncode == 0 and stdout.strip():
            lines = stdout.strip().split('\n')
            return len(lines), lines
        return 0, []

    def check_file_transfers(self):
        """Check for waiting file transfers"""
        if not self.file_transfers.exists():
            return []

        files = [
            f for f in self.file_transfers.iterdir()
            if f.is_file() and f.name != "README.md"
        ]
        return files

    def display_inbox(self):
        """Display current inbox contents"""
        if self.my_inbox.exists():
            print("\n📬 INBOX CONTENTS:")
            print("━" * 60)
            with open(self.my_inbox, 'r') as f:
                print(f.read())
            print("━" * 60)
        else:
            print("📭 Inbox is empty")

    def display_file_transfers(self, files):
        """Display waiting file transfers"""
        print("\n📦 FILE TRANSFERS:")
        print("━" * 60)
        for file in files:
            size = file.stat().st_size
            modified = datetime.fromtimestamp(file.stat().st_mtime)
            print(f"  • {file.name} ({size} bytes) - Modified: {modified.strftime('%Y-%m-%d %H:%M')}")

            # Check for .meta file
            meta_file = file.with_suffix(file.suffix + '.meta')
            if meta_file.exists():
                with open(meta_file, 'r') as f:
                    print(f"    Metadata: {f.read().strip()[:100]}...")
        print("━" * 60)

    def sync_cycle(self):
        """Perform one sync cycle"""
        self.log("Syncing...", "SYNC")

        # Pull updates
        has_updates, message = self.check_for_updates()

        if has_updates:
            self.log(f"✅ Updates received: {message}", "SUCCESS")

            # Check for new commands
            command_count, commands = self.check_new_commands()
            if command_count > 0:
                print("\n" + "=" * 60)
                print(f"🔔 NEW COMMANDS DETECTED! ({command_count} commits)")
                print("=" * 60)

                for cmd in commands:
                    print(f"  → {cmd}")

                # Display inbox
                self.display_inbox()

            # Check file transfers
            transfers = self.check_file_transfers()
            if transfers:
                self.display_file_transfers(transfers)
        else:
            self.log("✓ Already up to date", "INFO")

    def run(self):
        """Main sync loop"""
        print("🧠 Consciousness Network Auto-Sync Started")
        print(f"Repository: {self.repo_path}")
        print(f"Sync Interval: {self.sync_interval}s ({self.sync_interval//60} minutes)")
        print(f"Computer ID: {self.computer_id}")
        print(f"Monitoring: {self.my_inbox}")
        print("Press Ctrl+C to stop")
        print("━" * 60)

        try:
            while True:
                self.sync_cycle()
                time.sleep(self.sync_interval)
        except KeyboardInterrupt:
            print("\n\n🛑 Sync stopped by user")
            sys.exit(0)
        except Exception as e:
            self.log(f"Error: {e}", "ERROR")
            sys.exit(1)

def main():
    """Entry point"""
    import argparse

    parser = argparse.ArgumentParser(description="Consciousness Network Auto-Sync")
    parser.add_argument(
        "--interval",
        type=int,
        default=300,
        help="Sync interval in seconds (default: 300 = 5 minutes)"
    )
    parser.add_argument(
        "--computer-id",
        type=str,
        default="SWAN_ARCHITECT",
        help="Computer identifier"
    )
    parser.add_argument(
        "--repo",
        type=str,
        default=None,
        help="Repository path (default: current directory)"
    )

    args = parser.parse_args()

    syncer = ConsciousnessSync(
        repo_path=args.repo,
        sync_interval=args.interval,
        computer_id=args.computer_id
    )

    syncer.run()

if __name__ == "__main__":
    main()
