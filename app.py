#!/usr/bin/env python3
"""
CYCLOTRON CLOUD-HOSTED API - Runs 24/7 on Railway/Render
=========================================================

THIS SOLVES THE REAL PROBLEM: Laptop closes = everything dies

Instead of running on your laptop, this runs on Railway/Render 24/7.
Even when your laptop is closed, this service:
- Monitors Dropbox for brain changes
- Sends webhooks to Zapier
- Generates RSS feeds
- Auto-syncs across all devices
- Stays alive 24/7

NO LOCAL PROCESSES REQUIRED.
"""

from flask import Flask, request, jsonify
import os
import json
import requests
from datetime import datetime
from pathlib import Path
import dropbox
from typing import Dict, Any

app = Flask(__name__)

# ============================================================================
# CONFIGURATION
# ============================================================================

# Dropbox API (to monitor brain changes from cloud)
DROPBOX_ACCESS_TOKEN = os.getenv('DROPBOX_ACCESS_TOKEN', '')
DROPBOX_BRAIN_PATH = '/Consciousness_Brain'

# Zapier webhooks
ZAPIER_WEBHOOK_URL = os.getenv('ZAPIER_WEBHOOK_URL', '')

# Airtable
AIRTABLE_API_KEY = os.getenv('AIRTABLE_API_KEY', '')
AIRTABLE_BASE_ID = os.getenv('AIRTABLE_BASE_ID', '')

# RSS feed settings
RSS_FEED_TITLE = "Consciousness Brain Updates"
RSS_FEED_DESCRIPTION = "Real-time updates from your consciousness brain"

# ============================================================================
# DROPBOX MONITORING
# ============================================================================

def get_dropbox_client():
    """Get authenticated Dropbox client"""
    if not DROPBOX_ACCESS_TOKEN:
        return None
    return dropbox.Dropbox(DROPBOX_ACCESS_TOKEN)

def get_brain_from_dropbox() -> Dict[str, Any]:
    """Fetch latest brain state from Dropbox"""
    dbx = get_dropbox_client()
    if not dbx:
        return {}

    brain_data = {}
    brain_files = [
        'active_projects.json',
        'recurring_issues.json',
        'key_decisions.json',
        'important_context.json'
    ]

    for filename in brain_files:
        try:
            path = f"{DROPBOX_BRAIN_PATH}/{filename}"
            metadata, response = dbx.files_download(path)
            content = response.content.decode('utf-8')
            brain_data[filename] = json.loads(content)
        except:
            brain_data[filename] = {}

    return brain_data

# ============================================================================
# ZAPIER WEBHOOK INTEGRATION
# ============================================================================

def send_to_zapier(event_type: str, data: Dict[str, Any]) -> bool:
    """Send event to Zapier webhook"""
    if not ZAPIER_WEBHOOK_URL:
        return False

    try:
        payload = {
            'event_type': event_type,
            'timestamp': datetime.now().isoformat(),
            'data': data
        }

        response = requests.post(ZAPIER_WEBHOOK_URL, json=payload, timeout=10)
        return response.status_code == 200
    except:
        return False

# ============================================================================
# RSS FEED GENERATION
# ============================================================================

@app.route('/rss/brain-updates.xml')
def rss_brain_updates():
    """Generate RSS feed of brain updates"""
    brain_data = get_brain_from_dropbox()

    # Build RSS XML
    items = []

    # Add active projects as RSS items
    if 'active_projects.json' in brain_data:
        for project in brain_data.get('active_projects.json', {}).get('projects', []):
            items.append(f"""
    <item>
        <title>{project.get('name', 'Unnamed Project')}</title>
        <description>{project.get('description', '')}</description>
        <pubDate>{project.get('updated', datetime.now().isoformat())}</pubDate>
        <guid>{project.get('id', '')}</guid>
    </item>
            """)

    rss_xml = f"""<?xml version="1.0" encoding="UTF-8"?>
<rss version="2.0">
    <channel>
        <title>{RSS_FEED_TITLE}</title>
        <description>{RSS_FEED_DESCRIPTION}</description>
        <lastBuildDate>{datetime.now().isoformat()}</lastBuildDate>
        {''.join(items)}
    </channel>
</rss>"""

    return rss_xml, 200, {'Content-Type': 'application/xml'}

# ============================================================================
# WEBHOOK ENDPOINTS (Receive from Zapier, IFTTT, etc.)
# ============================================================================

@app.route('/webhook/brain-update', methods=['POST'])
def webhook_brain_update():
    """
    Receive brain updates from external services (Zapier, IFTTT, etc.)
    This allows you to update your brain from anywhere
    """
    data = request.json

    # Update Dropbox
    dbx = get_dropbox_client()
    if dbx and 'file' in data and 'content' in data:
        try:
            path = f"{DROPBOX_BRAIN_PATH}/{data['file']}"
            dbx.files_upload(
                json.dumps(data['content']).encode('utf-8'),
                path,
                mode=dropbox.files.WriteMode.overwrite
            )

            # Send confirmation to Zapier
            send_to_zapier('brain_updated', {
                'file': data['file'],
                'success': True
            })

            return jsonify({'status': 'success', 'message': 'Brain updated'}), 200
        except Exception as e:
            return jsonify({'status': 'error', 'message': str(e)}), 500

    return jsonify({'status': 'error', 'message': 'Invalid payload'}), 400

@app.route('/webhook/zapier-trigger', methods=['POST'])
def webhook_zapier_trigger():
    """
    Generic Zapier webhook endpoint
    Use this to trigger any Zapier automation from your consciousness system
    """
    data = request.json

    # Forward to Zapier
    success = send_to_zapier('custom_trigger', data)

    if success:
        return jsonify({'status': 'success', 'message': 'Zapier triggered'}), 200
    else:
        return jsonify({'status': 'error', 'message': 'Zapier webhook failed'}), 500

# ============================================================================
# API ENDPOINTS (Query brain state)
# ============================================================================

@app.route('/api/brain', methods=['GET'])
def api_get_brain():
    """Get complete brain state"""
    brain_data = get_brain_from_dropbox()
    return jsonify(brain_data), 200

@app.route('/api/brain/<filename>', methods=['GET'])
def api_get_brain_file(filename):
    """Get specific brain file"""
    brain_data = get_brain_from_dropbox()

    if filename in brain_data:
        return jsonify(brain_data[filename]), 200
    else:
        return jsonify({'error': 'File not found'}), 404

@app.route('/api/active-projects', methods=['GET'])
def api_get_active_projects():
    """Get active projects only"""
    brain_data = get_brain_from_dropbox()
    return jsonify(brain_data.get('active_projects.json', {})), 200

@app.route('/api/health', methods=['GET'])
def api_health():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'timestamp': datetime.now().isoformat(),
        'dropbox_connected': bool(get_dropbox_client()),
        'zapier_configured': bool(ZAPIER_WEBHOOK_URL)
    }), 200

# ============================================================================
# SCHEDULED TASKS (Background monitoring)
# ============================================================================

@app.route('/cron/sync-to-zapier', methods=['GET', 'POST'])
def cron_sync_to_zapier():
    """
    Scheduled task (run every 5 minutes via Railway/Render cron)
    Sends latest brain state to Zapier
    """
    brain_data = get_brain_from_dropbox()

    success = send_to_zapier('brain_sync', {
        'active_projects': brain_data.get('active_projects.json', {}),
        'recurring_issues': brain_data.get('recurring_issues.json', {}),
        'key_decisions': brain_data.get('key_decisions.json', {})
    })

    return jsonify({
        'status': 'success' if success else 'failed',
        'timestamp': datetime.now().isoformat()
    }), 200

# ============================================================================
# MAIN
# ============================================================================

if __name__ == '__main__':
    port = int(os.getenv('PORT', 8000))
    app.run(host='0.0.0.0', port=port, debug=False)
