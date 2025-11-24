#!/usr/bin/env python3
"""
COMMAND_CENTER_API.py - Trinity Network Control API

REST API backend for Trinity Command Center web dashboard.
Provides network-wide control, monitoring, and task execution.

Author: C1 T2 (PC2 - DESKTOP-MSMCFH2)
Created: 2025-11-24
"""

from flask import Flask, jsonify, request
from flask_cors import CORS
import json
import os
import time
from pathlib import Path
from datetime import datetime
from typing import Dict, Any, List

app = Flask(__name__)
CORS(app)

# Paths
BASE_DIR = Path(__file__).parent.parent.parent
TRINITY_DIR = BASE_DIR / ".trinity"
WAKE_DIR = TRINITY_DIR / "wake_signals"
MESSAGES_DIR = TRINITY_DIR / "messages"
HEARTBEAT_DIR = TRINITY_DIR / "heartbeat"
SPAWN_QUEUE = TRINITY_DIR / "spawn_queue" / "queue.json"
TODOS_FILE = TRINITY_DIR / "todos" / "kanban.json"

# Ensure directories exist
for dir_path in [WAKE_DIR, MESSAGES_DIR, HEARTBEAT_DIR]:
    dir_path.mkdir(parents=True, exist_ok=True)

# PC Configuration
PC_CONFIG = {
    "PC1": {"ip": "100.70.208.75", "name": "Laptop"},
    "PC2": {"ip": "100.85.71.74", "name": "Desktop (DESKTOP-MSMCFH2)"},
    "PC3": {"ip": "100.101.209.1", "name": "Third Computer"}
}

def get_timestamp():
    """Get current UTC timestamp."""
    return datetime.utcnow().isoformat() + "Z"

# ============= Health & Info =============

@app.route('/health')
def health():
    """Health check endpoint."""
    return jsonify({
        "status": "healthy",
        "service": "Trinity Command Center API",
        "timestamp": get_timestamp()
    })

@app.route('/api/info')
def get_info():
    """Get API info."""
    return jsonify({
        "name": "Trinity Command Center API",
        "version": "1.0.0",
        "endpoints": [
            "GET  /health",
            "GET  /api/info",
            "GET  /api/network/status",
            "GET  /api/heartbeats",
            "POST /api/wake",
            "GET  /api/spawn-queue",
            "POST /api/spawn-queue/run",
            "GET  /api/todos",
            "POST /api/message",
            "POST /api/consolidate"
        ]
    })

# ============= Network Status =============

@app.route('/api/network/status')
def network_status():
    """Get overall network status."""
    status = {
        "timestamp": get_timestamp(),
        "pcs": {}
    }

    for pc_id, pc_info in PC_CONFIG.items():
        heartbeat_file = HEARTBEAT_DIR / f"{pc_id}.json"

        if heartbeat_file.exists():
            try:
                with open(heartbeat_file, 'r') as f:
                    heartbeat = json.load(f)
                    status["pcs"][pc_id] = {
                        **pc_info,
                        "status": heartbeat.get("status", "unknown"),
                        "current_task": heartbeat.get("current_task", ""),
                        "last_seen": heartbeat.get("timestamp", ""),
                        "heartbeat": heartbeat
                    }
            except:
                status["pcs"][pc_id] = {
                    **pc_info,
                    "status": "error",
                    "current_task": "",
                    "last_seen": "",
                    "heartbeat": None
                }
        else:
            status["pcs"][pc_id] = {
                **pc_info,
                "status": "offline",
                "current_task": "",
                "last_seen": "",
                "heartbeat": None
            }

    return jsonify(status)

@app.route('/api/heartbeats')
def get_heartbeats():
    """Get all PC heartbeats."""
    heartbeats = {}

    for pc_id in PC_CONFIG.keys():
        heartbeat_file = HEARTBEAT_DIR / f"{pc_id}.json"

        if heartbeat_file.exists():
            try:
                with open(heartbeat_file, 'r') as f:
                    heartbeats[pc_id] = json.load(f)
            except:
                heartbeats[pc_id] = {"status": "error", "message": "Failed to read heartbeat"}
        else:
            heartbeats[pc_id] = {"status": "no_heartbeat"}

    return jsonify(heartbeats)

# ============= Wake Signals =============

@app.route('/api/wake', methods=['POST'])
def send_wake():
    """Send wake signal to PC."""
    data = request.get_json()
    target_pc = data.get('pc')

    if not target_pc or target_pc not in PC_CONFIG:
        return jsonify({"error": "Invalid PC specified"}), 400

    try:
        wake_file = WAKE_DIR / f"WAKE_{target_pc}_{int(time.time())}.txt"

        with open(wake_file, 'w') as f:
            f.write(f"Wake signal for {target_pc}\n")
            f.write(f"Triggered by: Command Center API\n")
            f.write(f"Time: {get_timestamp()}\n")

        return jsonify({
            "success": True,
            "message": f"Wake signal sent to {target_pc}",
            "timestamp": get_timestamp()
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 500

# ============= Spawn Queue =============

@app.route('/api/spawn-queue')
def get_spawn_queue():
    """Get spawn queue status."""
    if not SPAWN_QUEUE.exists():
        return jsonify({"error": "Spawn queue not found"}), 404

    try:
        with open(SPAWN_QUEUE, 'r') as f:
            queue_data = json.load(f)

        return jsonify(queue_data)

    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/spawn-queue/run', methods=['POST'])
def run_spawn_queue():
    """Trigger spawn queue processing."""
    try:
        msg_file = MESSAGES_DIR / f"TRIGGER_SPAWN_QUEUE_{int(time.time())}.md"

        with open(msg_file, 'w') as f:
            f.write("# SPAWN QUEUE TRIGGER\n\n")
            f.write(f"**Triggered by:** Command Center API\n")
            f.write(f"**Time:** {get_timestamp()}\n\n")
            f.write("Process all pending tasks in spawn queue.\n")

        return jsonify({
            "success": True,
            "message": "Spawn queue processing triggered",
            "timestamp": get_timestamp()
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 500

# ============= Todos =============

@app.route('/api/todos')
def get_todos():
    """Get todo list."""
    if not TODOS_FILE.exists():
        return jsonify({"error": "Todo list not found"}), 404

    try:
        with open(TODOS_FILE, 'r') as f:
            todos_data = json.load(f)

        return jsonify(todos_data)

    except Exception as e:
        return jsonify({"error": str(e)}), 500

# ============= Messages =============

@app.route('/api/message', methods=['POST'])
def send_message():
    """Send message to PC."""
    data = request.get_json()
    target_pc = data.get('pc', 'ALL')
    subject = data.get('subject', 'Message from Command Center')
    body = data.get('body', '')

    try:
        msg_file = MESSAGES_DIR / f"TO_{target_pc}_{int(time.time())}.md"

        with open(msg_file, 'w') as f:
            f.write(f"# {subject}\n\n")
            f.write(f"**To:** {target_pc}\n")
            f.write(f"**From:** Command Center API\n")
            f.write(f"**Time:** {get_timestamp()}\n\n")
            f.write(body)

        return jsonify({
            "success": True,
            "message": f"Message sent to {target_pc}",
            "timestamp": get_timestamp()
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 500

# ============= Operations =============

@app.route('/api/consolidate', methods=['POST'])
def trigger_consolidate():
    """Trigger consolidation."""
    try:
        msg_file = MESSAGES_DIR / f"TRIGGER_CONSOLIDATION_{int(time.time())}.md"

        with open(msg_file, 'w') as f:
            f.write("# CONSOLIDATION TRIGGER\n\n")
            f.write(f"**Triggered by:** Command Center API\n")
            f.write(f"**Time:** {get_timestamp()}\n\n")
            f.write("Run full Trinity consolidation across all PCs.\n")

        return jsonify({
            "success": True,
            "message": "Consolidation triggered",
            "timestamp": get_timestamp()
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/shutdown', methods=['POST'])
def trigger_shutdown():
    """Trigger graceful shutdown."""
    data = request.get_json()
    target_pc = data.get('pc', 'ALL')

    try:
        if target_pc == 'ALL':
            pcs_to_shutdown = list(PC_CONFIG.keys())
        else:
            pcs_to_shutdown = [target_pc]

        for pc in pcs_to_shutdown:
            msg_file = MESSAGES_DIR / f"SHUTDOWN_{pc}_{int(time.time())}.md"

            with open(msg_file, 'w') as f:
                f.write(f"# SHUTDOWN SIGNAL FOR {pc}\n\n")
                f.write(f"**Triggered by:** Command Center API\n")
                f.write(f"**Time:** {get_timestamp()}\n\n")
                f.write("Gracefully shutdown autonomous operations and save state.\n")

        return jsonify({
            "success": True,
            "message": f"Shutdown signals sent to {target_pc}",
            "timestamp": get_timestamp()
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 500

# ============= Main =============

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5004))

    print("=" * 60)
    print("TRINITY COMMAND CENTER API")
    print("=" * 60)
    print(f"Starting on port {port}")
    print("\nEndpoints:")
    print("  GET  /health - Health check")
    print("  GET  /api/info - API information")
    print("  GET  /api/network/status - Network status")
    print("  GET  /api/heartbeats - All PC heartbeats")
    print("  POST /api/wake - Send wake signal")
    print("  GET  /api/spawn-queue - Get spawn queue")
    print("  POST /api/spawn-queue/run - Run spawn queue")
    print("  GET  /api/todos - Get todo list")
    print("  POST /api/message - Send message to PC")
    print("  POST /api/consolidate - Trigger consolidation")
    print("  POST /api/shutdown - Trigger shutdown")
    print("=" * 60)

    app.run(debug=False, port=port, host='0.0.0.0')
