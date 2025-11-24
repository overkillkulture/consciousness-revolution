#!/usr/bin/env python3
"""
DESKTOP_BRIDGE.py - Simple File-Based Control for Trinity Network

Monitors Desktop folder for trigger files and executes Trinity commands.
Enables non-technical control via simple text files (works from phone, tablet, etc.).

Usage:
    python DESKTOP_BRIDGE.py

Trigger Files:
    - WAKE_PC1.txt → Wake PC1
    - WAKE_PC2.txt → Wake PC2
    - WAKE_PC3.txt → Wake PC3
    - RUN_SPAWN_QUEUE.txt → Process spawn queue
    - CONSOLIDATE_NOW.txt → Run consolidation
    - STATUS_ALL.txt → Generate status report
    - SHUTDOWN_ALL.txt → Graceful shutdown all PCs

Author: C1 T2 (PC2 - DESKTOP-MSMCFH2)
Created: 2025-11-23
"""

import os
import sys
import time
import json
import shutil
from pathlib import Path
from datetime import datetime
from typing import Optional, Dict, Any

# Paths
DESKTOP = Path.home() / "Desktop"
BASE_DIR = Path(__file__).parent.parent.parent
TRINITY_DIR = BASE_DIR / ".trinity"
WAKE_DIR = TRINITY_DIR / "wake_signals"
MESSAGES_DIR = TRINITY_DIR / "messages"
HEARTBEAT_DIR = TRINITY_DIR / "heartbeat"
SPAWN_QUEUE = TRINITY_DIR / "spawn_queue" / "queue.json"

# PC Configuration
CURRENT_PC = "PC2"
PC_TAILSCALE_IPS = {
    "PC1": "100.70.208.75",
    "PC2": "100.85.71.74",
    "PC3": "100.101.209.1"
}

# Ensure directories exist
WAKE_DIR.mkdir(parents=True, exist_ok=True)
MESSAGES_DIR.mkdir(parents=True, exist_ok=True)
HEARTBEAT_DIR.mkdir(parents=True, exist_ok=True)

# Bridge state
PROCESSED_FILES = set()
BRIDGE_RUNNING = True

def log(message: str):
    """Log message with timestamp."""
    timestamp = datetime.utcnow().isoformat() + "Z"
    print(f"[{timestamp}] [DESKTOP-BRIDGE] {message}")

def send_wake_signal(target_pc: str) -> bool:
    """Send wake signal to target PC."""
    try:
        wake_file = WAKE_DIR / f"WAKE_{target_pc}_{int(time.time())}.txt"

        with open(wake_file, 'w') as f:
            f.write(f"Wake signal for {target_pc}\n")
            f.write(f"Triggered by: Desktop Bridge on {CURRENT_PC}\n")
            f.write(f"Time: {datetime.utcnow().isoformat()}Z\n")
            f.write(f"Method: Desktop trigger file\n")

        log(f"✅ Wake signal sent to {target_pc}")
        return True

    except Exception as e:
        log(f"❌ Failed to send wake signal to {target_pc}: {e}")
        return False

def run_spawn_queue() -> bool:
    """Process spawn queue."""
    try:
        if not SPAWN_QUEUE.exists():
            log("⚠️ Spawn queue not found")
            return False

        # Create message to trigger spawn queue processing
        msg_file = MESSAGES_DIR / f"TRIGGER_SPAWN_QUEUE_{int(time.time())}.md"

        with open(msg_file, 'w') as f:
            f.write("# SPAWN QUEUE TRIGGER\n\n")
            f.write(f"**Triggered by:** Desktop Bridge on {CURRENT_PC}\n")
            f.write(f"**Time:** {datetime.utcnow().isoformat()}Z\n\n")
            f.write("Process all pending tasks in spawn queue.\n")

        log("✅ Spawn queue processing triggered")
        return True

    except Exception as e:
        log(f"❌ Failed to trigger spawn queue: {e}")
        return False

def consolidate_now() -> bool:
    """Trigger consolidation."""
    try:
        msg_file = MESSAGES_DIR / f"TRIGGER_CONSOLIDATION_{int(time.time())}.md"

        with open(msg_file, 'w') as f:
            f.write("# CONSOLIDATION TRIGGER\n\n")
            f.write(f"**Triggered by:** Desktop Bridge on {CURRENT_PC}\n")
            f.write(f"**Time:** {datetime.utcnow().isoformat()}Z\n\n")
            f.write("Run full Trinity consolidation across all PCs.\n")

        log("✅ Consolidation triggered")
        return True

    except Exception as e:
        log(f"❌ Failed to trigger consolidation: {e}")
        return False

def generate_status_report() -> bool:
    """Generate comprehensive status report."""
    try:
        status = {
            "timestamp": datetime.utcnow().isoformat() + "Z",
            "current_pc": CURRENT_PC,
            "desktop_bridge": "active",
            "heartbeats": {}
        }

        # Check heartbeats
        for pc in ["PC1", "PC2", "PC3"]:
            heartbeat_file = HEARTBEAT_DIR / f"{pc}.json"
            if heartbeat_file.exists():
                with open(heartbeat_file, 'r') as f:
                    status["heartbeats"][pc] = json.load(f)
            else:
                status["heartbeats"][pc] = {"status": "no_heartbeat"}

        # Write status report to Desktop
        report_file = DESKTOP / f"TRINITY_STATUS_REPORT_{datetime.utcnow().strftime('%Y%m%d_%H%M%S')}.json"

        with open(report_file, 'w') as f:
            json.dump(status, f, indent=2)

        log(f"✅ Status report generated: {report_file.name}")
        return True

    except Exception as e:
        log(f"❌ Failed to generate status report: {e}")
        return False

def shutdown_all() -> bool:
    """Trigger graceful shutdown of all PCs."""
    try:
        for pc in ["PC1", "PC2", "PC3"]:
            msg_file = MESSAGES_DIR / f"SHUTDOWN_{pc}_{int(time.time())}.md"

            with open(msg_file, 'w') as f:
                f.write(f"# SHUTDOWN SIGNAL FOR {pc}\n\n")
                f.write(f"**Triggered by:** Desktop Bridge on {CURRENT_PC}\n")
                f.write(f"**Time:** {datetime.utcnow().isoformat()}Z\n\n")
                f.write("Gracefully shutdown autonomous operations and save state.\n")

        log("✅ Shutdown signals sent to all PCs")
        return True

    except Exception as e:
        log(f"❌ Failed to send shutdown signals: {e}")
        return False

def process_trigger_file(trigger_file: Path) -> bool:
    """Process a trigger file and execute corresponding action."""
    filename = trigger_file.name.upper()

    log(f"Processing trigger: {filename}")

    success = False

    # Wake signals
    if filename == "WAKE_PC1.TXT":
        success = send_wake_signal("PC1")
    elif filename == "WAKE_PC2.TXT":
        success = send_wake_signal("PC2")
    elif filename == "WAKE_PC3.TXT":
        success = send_wake_signal("PC3")

    # Task execution
    elif filename == "RUN_SPAWN_QUEUE.TXT":
        success = run_spawn_queue()
    elif filename == "CONSOLIDATE_NOW.TXT":
        success = consolidate_now()

    # Status
    elif filename == "STATUS_ALL.TXT":
        success = generate_status_report()

    # Shutdown
    elif filename == "SHUTDOWN_ALL.TXT":
        success = shutdown_all()

    else:
        log(f"⚠️ Unknown trigger file: {filename}")
        return False

    # Archive processed trigger file
    try:
        archive_dir = DESKTOP / ".trinity_triggers_archive"
        archive_dir.mkdir(exist_ok=True)

        archive_path = archive_dir / f"{datetime.utcnow().strftime('%Y%m%d_%H%M%S')}_{filename}"
        shutil.move(str(trigger_file), str(archive_path))

        log(f"📦 Trigger archived: {archive_path.name}")

    except Exception as e:
        log(f"⚠️ Failed to archive trigger file: {e}")
        # Try to delete if archive failed
        try:
            trigger_file.unlink()
        except:
            pass

    return success

def scan_desktop():
    """Scan Desktop for trigger files."""
    trigger_patterns = [
        "WAKE_PC1.txt",
        "WAKE_PC2.txt",
        "WAKE_PC3.txt",
        "RUN_SPAWN_QUEUE.txt",
        "CONSOLIDATE_NOW.txt",
        "STATUS_ALL.txt",
        "SHUTDOWN_ALL.txt"
    ]

    for pattern in trigger_patterns:
        trigger_file = DESKTOP / pattern

        # Check case-insensitive
        for existing_file in DESKTOP.glob("*"):
            if existing_file.name.upper() == pattern.upper():
                trigger_file = existing_file
                break

        if trigger_file.exists() and str(trigger_file) not in PROCESSED_FILES:
            PROCESSED_FILES.add(str(trigger_file))
            process_trigger_file(trigger_file)

def main():
    """Main bridge loop."""
    log("=" * 60)
    log("DESKTOP BRIDGE - Trinity Control Interface")
    log("=" * 60)
    log(f"Monitoring: {DESKTOP}")
    log(f"Current PC: {CURRENT_PC}")
    log("")
    log("Trigger files:")
    log("  WAKE_PC1.txt - Wake PC1")
    log("  WAKE_PC2.txt - Wake PC2")
    log("  WAKE_PC3.txt - Wake PC3")
    log("  RUN_SPAWN_QUEUE.txt - Process spawn queue")
    log("  CONSOLIDATE_NOW.txt - Run consolidation")
    log("  STATUS_ALL.txt - Generate status report")
    log("  SHUTDOWN_ALL.txt - Shutdown all PCs")
    log("")
    log("Drop any trigger file on Desktop to execute command")
    log("Press Ctrl+C to stop")
    log("=" * 60)
    log("")

    try:
        while BRIDGE_RUNNING:
            scan_desktop()
            time.sleep(5)  # Check every 5 seconds

    except KeyboardInterrupt:
        log("")
        log("Shutdown requested")
        log("Desktop Bridge stopped")

if __name__ == "__main__":
    main()
