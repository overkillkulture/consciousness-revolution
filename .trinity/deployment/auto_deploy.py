#!/usr/bin/env python3
"""
auto_deploy.py - Automated Trinity System Deployment

Automatically deploys all Session 1 & 2 automation systems to PC1 or PC3.

Usage:
    python auto_deploy.py --pc PC1
    python auto_deploy.py --pc PC3

Author: C1 T2 (PC2 - DESKTOP-MSMCFH2)
Created: 2025-11-23
"""

import os
import sys
import subprocess
import json
import argparse
from pathlib import Path
from datetime import datetime

# ============= Configuration =============

SYSTEMS_TO_DEPLOY = [
    {
        "name": "Auto-Credit-Monitor",
        "script": "CREDIT_MONITOR.py",
        "port": 5002,
        "description": "Automatic PC rotation on credit exhaustion"
    },
    {
        "name": "Auto-MCP-Git-Sync",
        "script": "MCP_GIT_SYNC.py",
        "port": None,
        "description": "Cross-PC knowledge synchronization"
    },
    {
        "name": "Auto-Desktop-Bridge",
        "script": "DESKTOP_BRIDGE.py",
        "port": None,
        "description": "File-based Trinity control"
    },
    {
        "name": "Todo Tracker",
        "script": "TODO_TRACKER.py",
        "port": 5001,
        "description": "Persistent git-synced kanban board"
    },
    {
        "name": "Command Center",
        "script": "COMMAND_CENTER_API.py",
        "port": 5004,
        "description": "Network-wide control dashboard"
    }
]

REQUIRED_PACKAGES = [
    "flask",
    "flask-cors"
]

# ============= Utility Functions =============

def print_header(text):
    """Print formatted header."""
    print("\n" + "=" * 70)
    print(text.center(70))
    print("=" * 70 + "\n")

def print_step(step_num, total, text):
    """Print step indicator."""
    print(f"\n[Step {step_num}/{total}] {text}")
    print("-" * 70)

def print_success(text):
    """Print success message."""
    print(f"✅ {text}")

def print_error(text):
    """Print error message."""
    print(f"❌ {text}")

def print_warning(text):
    """Print warning message."""
    print(f"⚠️  {text}")

def run_command(command, capture_output=True):
    """Run shell command and return result."""
    try:
        result = subprocess.run(
            command,
            shell=True,
            capture_output=capture_output,
            text=True,
            check=True
        )
        return True, result.stdout if capture_output else None
    except subprocess.CalledProcessError as e:
        return False, e.stderr if capture_output else None

# ============= Pre-Deployment Checks =============

def check_python_version():
    """Check Python version."""
    version = sys.version_info
    if version.major < 3 or (version.major == 3 and version.minor < 6):
        print_error(f"Python 3.6+ required, found {version.major}.{version.minor}")
        return False
    print_success(f"Python {version.major}.{version.minor}.{version.micro}")
    return True

def check_git_repo():
    """Check if in git repository."""
    if not Path(".git").exists():
        print_error("Not in git repository. Please run from 100X_DEPLOYMENT directory.")
        return False
    print_success("Git repository found")
    return True

def check_trinity_structure():
    """Check .trinity directory structure."""
    required_dirs = [
        ".trinity/automation",
        ".trinity/dashboards",
        ".trinity/messages",
        ".trinity/wake_signals",
        ".trinity/heartbeat",
        ".trinity/spawn_queue",
        ".trinity/todos"
    ]

    missing = []
    for dir_path in required_dirs:
        path = Path(dir_path)
        if not path.exists():
            missing.append(dir_path)
            path.mkdir(parents=True, exist_ok=True)
            print_success(f"Created: {dir_path}")
        else:
            print_success(f"Found: {dir_path}")

    return True

def check_dependencies():
    """Check Python dependencies."""
    print("\nChecking Python packages...")

    missing = []
    for package in REQUIRED_PACKAGES:
        success, output = run_command(f"pip show {package}")
        if success:
            print_success(f"{package} installed")
        else:
            missing.append(package)
            print_warning(f"{package} not installed")

    if missing:
        print("\nMissing packages detected. Installing...")
        for package in missing:
            print(f"Installing {package}...")
            success, _ = run_command(f"pip install {package}", capture_output=False)
            if success:
                print_success(f"{package} installed")
            else:
                print_error(f"Failed to install {package}")
                return False

    return True

# ============= Deployment Functions =============

def update_pc_identifier(script_path, pc_name):
    """Update CURRENT_PC identifier in script."""
    try:
        with open(script_path, 'r') as f:
            content = f.read()

        # Find and update CURRENT_PC line
        lines = content.split('\n')
        updated = False

        for i, line in enumerate(lines):
            if 'CURRENT_PC = ' in line and not line.strip().startswith('#'):
                lines[i] = f'CURRENT_PC = "{pc_name}"'
                updated = True
                break

        if updated:
            with open(script_path, 'w') as f:
                f.write('\n'.join(lines))
            print_success(f"Updated {script_path.name} to use {pc_name}")
            return True
        else:
            print_warning(f"Could not find CURRENT_PC in {script_path.name}")
            return True  # Not critical, continue

    except Exception as e:
        print_error(f"Failed to update {script_path.name}: {e}")
        return False

def start_service(script_name):
    """Start a background service."""
    script_path = Path(".trinity/automation") / script_name

    if not script_path.exists():
        print_error(f"Script not found: {script_path}")
        return False

    print(f"Starting {script_name}...")

    # Start in background
    command = f"python {script_path} &"
    success, _ = run_command(command, capture_output=False)

    if success:
        print_success(f"{script_name} started")
        return True
    else:
        print_error(f"Failed to start {script_name}")
        return False

def verify_service(system):
    """Verify service is running."""
    if system["port"]:
        # Check if port is accessible
        import socket
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(2)
        result = sock.connect_ex(('localhost', system["port"]))
        sock.close()

        if result == 0:
            print_success(f"{system['name']} responding on port {system['port']}")
            return True
        else:
            print_warning(f"{system['name']} not responding on port {system['port']}")
            return False
    else:
        # Just check if process exists
        success, output = run_command(f"ps aux | grep {system['script']}")
        if success and system['script'] in output:
            print_success(f"{system['name']} process running")
            return True
        else:
            print_warning(f"{system['name']} process not found")
            return False

def create_heartbeat(pc_name):
    """Create initial heartbeat file."""
    heartbeat_file = Path(f".trinity/heartbeat/{pc_name}.json")

    heartbeat = {
        "pc_id": pc_name,
        "status": "active",
        "timestamp": datetime.utcnow().isoformat() + "Z",
        "current_task": "Trinity automation deployed",
        "systems_running": [s["name"] for s in SYSTEMS_TO_DEPLOY]
    }

    try:
        with open(heartbeat_file, 'w') as f:
            json.dump(heartbeat, f, indent=2)
        print_success(f"Created heartbeat: {heartbeat_file}")
        return True
    except Exception as e:
        print_error(f"Failed to create heartbeat: {e}")
        return False

# ============= Main Deployment =============

def deploy(pc_name, start_services=True):
    """Run full deployment."""

    print_header("TRINITY AUTOMATION DEPLOYMENT")
    print(f"Target PC: {pc_name}")
    print(f"Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

    # Step 1: Pre-deployment checks
    print_step(1, 7, "Pre-deployment checks")

    if not check_python_version():
        return False

    if not check_git_repo():
        return False

    if not check_trinity_structure():
        return False

    if not check_dependencies():
        return False

    # Step 2: Git pull
    print_step(2, 7, "Pulling latest code from git")
    print("Running: git pull origin master")
    success, output = run_command("git pull origin master", capture_output=False)
    if success:
        print_success("Git pull completed")
    else:
        print_error("Git pull failed")
        return False

    # Step 3: Update PC identifiers
    print_step(3, 7, f"Configuring scripts for {pc_name}")

    automation_dir = Path(".trinity/automation")
    scripts_to_update = [s["script"] for s in SYSTEMS_TO_DEPLOY]

    for script_name in scripts_to_update:
        script_path = automation_dir / script_name
        if script_path.exists():
            if not update_pc_identifier(script_path, pc_name):
                print_warning(f"Could not update {script_name}")
        else:
            print_warning(f"Script not found: {script_name}")

    # Step 4: Create heartbeat
    print_step(4, 7, "Creating initial heartbeat")
    create_heartbeat(pc_name)

    # Step 5: Start services (optional)
    if start_services:
        print_step(5, 7, "Starting automation services")

        for system in SYSTEMS_TO_DEPLOY:
            start_service(system["script"])

        print("\nWaiting 5 seconds for services to initialize...")
        import time
        time.sleep(5)

        # Step 6: Verify services
        print_step(6, 7, "Verifying services")

        for system in SYSTEMS_TO_DEPLOY:
            verify_service(system)
    else:
        print_step(5, 7, "Skipping service start (--no-start flag)")
        print_step(6, 7, "Skipping service verification")

    # Step 7: Summary
    print_step(7, 7, "Deployment summary")

    print("\n📊 DEPLOYMENT COMPLETE!\n")
    print("Systems deployed:")
    for system in SYSTEMS_TO_DEPLOY:
        status = "✅" if start_services else "⏸️"
        print(f"  {status} {system['name']}")
        print(f"     {system['description']}")
        if system['port']:
            print(f"     Dashboard: http://localhost:{system['port']}")
        print()

    print("🌐 Access Points:")
    print(f"  • Command Center: http://localhost:5004/.trinity/dashboards/COMMAND_CENTER.html")
    print(f"  • Todo Tracker: http://localhost:5001")
    print(f"  • Credit Monitor: http://localhost:5002")

    print("\n📁 Next Steps:")
    if not start_services:
        print("  1. Start services manually (see README files)")
    print("  1. Open Command Center dashboard")
    print("  2. Verify all 3 PCs visible in network status")
    print("  3. Test wake signal to another PC")
    print("  4. Test message sending")

    print("\n📚 Documentation:")
    print("  • Deployment Guide: .trinity/deployment/DEPLOY_TO_PC1_AND_PC3.md")
    print("  • System READMEs: .trinity/automation/*_README.md")

    print_header("TRINITY NETWORK READY! 🌌")

    return True

# ============= CLI =============

def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(
        description="Deploy Trinity automation systems to PC1 or PC3"
    )
    parser.add_argument(
        "--pc",
        required=True,
        choices=["PC1", "PC3"],
        help="Target PC (PC1 or PC3)"
    )
    parser.add_argument(
        "--no-start",
        action="store_true",
        help="Don't start services after deployment"
    )

    args = parser.parse_args()

    try:
        success = deploy(args.pc, start_services=not args.no_start)
        sys.exit(0 if success else 1)
    except KeyboardInterrupt:
        print("\n\n⚠️  Deployment interrupted by user")
        sys.exit(1)
    except Exception as e:
        print(f"\n\n❌ Deployment failed: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

if __name__ == "__main__":
    main()
