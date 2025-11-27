#!/usr/bin/env python3
"""
TRINITY MASTER ORCHESTRATOR - CP1 Control Center

One command to rule them all.
Starts all Trinity coordination systems simultaneously.

Usage:
    python3 TRINITY_MASTER_ORCHESTRATOR.py start    # Start all systems
    python3 TRINITY_MASTER_ORCHESTRATOR.py stop     # Stop all systems
    python3 TRINITY_MASTER_ORCHESTRATOR.py status   # Check status
    python3 TRINITY_MASTER_ORCHESTRATOR.py report   # Generate report

The cheat code IS the consciousness.
C1 × C2 × C3 = ∞
"""

import os
import sys
import time
import signal
import subprocess
from pathlib import Path
from datetime import datetime
import json

class TrinityOrchestrator:
    def __init__(self):
        self.base_dir = Path(__file__).parent
        self.pid_dir = self.base_dir / '.consciousness' / 'pids'
        self.pid_dir.mkdir(parents=True, exist_ok=True)

        self.processes = {
            'status_reader': {
                'script': 'TRINITY_STATUS_READER.py',
                'pid_file': 'status_reader.pid',
                'description': 'Status Reader Daemon'
            },
            'work_monitor': {
                'script': 'AUTONOMOUS_WORK_MONITOR.py',
                'pid_file': 'work_monitor.pid',
                'description': 'Autonomous Work Monitor'
            }
        }

    def start_process(self, name, config):
        """Start a background process"""
        script = self.base_dir / config['script']
        pid_file = self.pid_dir / config['pid_file']

        if not script.exists():
            print(f"   ⚠️  Script not found: {script}")
            return False

        # Check if already running
        if self.is_running(name):
            print(f"   ⏭️  {config['description']} already running")
            return True

        # Start process
        try:
            process = subprocess.Popen(
                [sys.executable, str(script)],
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
                start_new_session=True
            )

            # Save PID
            with open(pid_file, 'w') as f:
                f.write(str(process.pid))

            time.sleep(0.5)  # Give it time to start

            # Verify it's running
            if process.poll() is None:
                print(f"   ✅ {config['description']} started (PID: {process.pid})")
                return True
            else:
                print(f"   ❌ {config['description']} failed to start")
                return False

        except Exception as e:
            print(f"   ❌ Error starting {config['description']}: {e}")
            return False

    def stop_process(self, name, config):
        """Stop a background process"""
        pid_file = self.pid_dir / config['pid_file']

        if not pid_file.exists():
            print(f"   ⏭️  {config['description']} not running (no PID file)")
            return True

        try:
            with open(pid_file, 'r') as f:
                pid = int(f.read().strip())

            # Try to kill the process
            try:
                os.kill(pid, signal.SIGTERM)
                time.sleep(0.5)
                print(f"   ✅ {config['description']} stopped (PID: {pid})")
            except ProcessLookupError:
                print(f"   ⏭️  {config['description']} already stopped")

            # Remove PID file
            pid_file.unlink()
            return True

        except Exception as e:
            print(f"   ⚠️  Error stopping {config['description']}: {e}")
            return False

    def is_running(self, name):
        """Check if a process is running"""
        config = self.processes[name]
        pid_file = self.pid_dir / config['pid_file']

        if not pid_file.exists():
            return False

        try:
            with open(pid_file, 'r') as f:
                pid = int(f.read().strip())

            # Check if process exists
            os.kill(pid, 0)
            return True
        except (ProcessLookupError, ValueError):
            # Process doesn't exist, clean up PID file
            pid_file.unlink()
            return False

    def start_all(self):
        """Start all Trinity systems"""
        print("="*60)
        print("⚡ TRINITY MASTER ORCHESTRATOR - STARTING ALL SYSTEMS")
        print("="*60)
        print()

        results = {}
        for name, config in self.processes.items():
            results[name] = self.start_process(name, config)

        print()
        print("="*60)

        if all(results.values()):
            print("✅ ALL SYSTEMS OPERATIONAL")
        else:
            print("⚠️  SOME SYSTEMS FAILED TO START")

        print("="*60)
        print()
        print("Dashboard: Open TRINITY_LIVE_DASHBOARD.html in browser")
        print("Logs: Check individual script outputs")
        print("Stop: python3 TRINITY_MASTER_ORCHESTRATOR.py stop")
        print()

    def stop_all(self):
        """Stop all Trinity systems"""
        print("="*60)
        print("⚠️  TRINITY MASTER ORCHESTRATOR - STOPPING ALL SYSTEMS")
        print("="*60)
        print()

        for name, config in self.processes.items():
            self.stop_process(name, config)

        print()
        print("="*60)
        print("✅ ALL SYSTEMS STOPPED")
        print("="*60)
        print()

    def show_status(self):
        """Show status of all systems"""
        print("="*60)
        print("📊 TRINITY MASTER ORCHESTRATOR - SYSTEM STATUS")
        print("="*60)
        print()

        all_running = True
        for name, config in self.processes.items():
            running = self.is_running(name)
            status = "🟢 RUNNING" if running else "⚫ STOPPED"
            print(f"{status}  {config['description']}")
            if not running:
                all_running = False

        print()
        print("="*60)

        if all_running:
            print("✅ ALL SYSTEMS OPERATIONAL")
        else:
            print("⚠️  SOME SYSTEMS STOPPED")

        print("="*60)
        print()

    def generate_report(self):
        """Generate and display CP1 output"""
        print("="*60)
        print("📋 GENERATING CP1 OUTPUT REPORT")
        print("="*60)
        print()

        generator_script = self.base_dir / 'CP1_OUTPUT_GENERATOR.py'

        if not generator_script.exists():
            print("❌ CP1_OUTPUT_GENERATOR.py not found")
            return

        try:
            subprocess.run([sys.executable, str(generator_script)])
            print()
            print("="*60)
            print("✅ REPORT GENERATED: CP1_OUTPUT.md")
            print("="*60)
            print()
            print("📁 Copy to sync folder:")
            print('   cp CP1_OUTPUT.md "G:\\My Drive\\TRINITY_COMMS\\sync\\"')
            print()
        except Exception as e:
            print(f"❌ Error generating report: {e}")

def main():
    if len(sys.argv) < 2:
        print("Usage: python3 TRINITY_MASTER_ORCHESTRATOR.py [start|stop|status|report]")
        print()
        print("Commands:")
        print("  start   - Start all Trinity systems")
        print("  stop    - Stop all Trinity systems")
        print("  status  - Show system status")
        print("  report  - Generate CP1 output report")
        sys.exit(1)

    command = sys.argv[1].lower()
    orchestrator = TrinityOrchestrator()

    if command == 'start':
        orchestrator.start_all()
    elif command == 'stop':
        orchestrator.stop_all()
    elif command == 'status':
        orchestrator.show_status()
    elif command == 'report':
        orchestrator.generate_report()
    else:
        print(f"Unknown command: {command}")
        print("Valid commands: start, stop, status, report")
        sys.exit(1)

if __name__ == '__main__':
    main()
