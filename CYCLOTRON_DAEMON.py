#!/usr/bin/env python3
"""
CYCLOTRON DAEMON - Always-On Knowledge Indexing
Watches directories for changes and auto-indexes new/modified files.

Toyota Principles Applied:
- JIDOKA: Auto-stop on critical errors, alert and recover
- KAIZEN: Continuous incremental improvements to index
- KANBAN: Pull-based - only index what changed

Usage:
    python CYCLOTRON_DAEMON.py          # Start daemon
    python CYCLOTRON_DAEMON.py status   # Check status
    python CYCLOTRON_DAEMON.py vacuum   # Force full re-index
"""

import os
import sys
import time
import sqlite3
import hashlib
import json
import logging
from pathlib import Path
from datetime import datetime
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

# Configuration
VACUUM_DIRS = [
    "C:/Users/dwrek/100X_DEPLOYMENT",
    "C:/Users/dwrek/.consciousness",
    "C:/Users/dwrek/.trinity",
    "C:/Users/dwrek/LOCAL_TRINITY_HUB",
    "C:/Users/dwrek/Desktop",
]

INDEX_EXTENSIONS = ['.md', '.txt', '.py', '.js', '.html', '.json', '.bat', '.ps1', '.css']
DB_PATH = Path("C:/Users/dwrek/100X_DEPLOYMENT/.cyclotron_atoms/cyclotron.db")
STATUS_FILE = Path("C:/Users/dwrek/100X_DEPLOYMENT/.cyclotron_atoms/daemon_status.json")
LOG_FILE = Path("C:/Users/dwrek/100X_DEPLOYMENT/.cyclotron_atoms/daemon.log")

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(LOG_FILE),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

class CyclotronIndexer:
    """Handles all indexing operations"""

    def __init__(self):
        self.conn = None
        self.stats = {
            'files_indexed': 0,
            'files_updated': 0,
            'files_deleted': 0,
            'errors': 0,
            'last_vacuum': None,
            'started': datetime.now().isoformat()
        }
        self._init_db()

    def _init_db(self):
        """Initialize database connection"""
        DB_PATH.parent.mkdir(exist_ok=True)
        self.conn = sqlite3.connect(str(DB_PATH), check_same_thread=False)
        cursor = self.conn.cursor()

        # Create FTS5 table if not exists
        cursor.execute('''
            CREATE VIRTUAL TABLE IF NOT EXISTS knowledge USING fts5(
                path, name, type, content, preview, modified, hash,
                tokenize='porter unicode61'
            )
        ''')
        self.conn.commit()

    def should_index(self, path):
        """Check if file should be indexed"""
        p = Path(path)

        # Skip non-matching extensions
        if p.suffix.lower() not in INDEX_EXTENSIONS:
            return False

        # Skip hidden/system directories
        skip_dirs = ['.git', '__pycache__', 'node_modules', '.venv', 'venv']
        if any(skip in str(path) for skip in skip_dirs):
            return False

        # Skip very large files (>1MB)
        try:
            if p.stat().st_size > 1_000_000:
                return False
        except:
            return False

        return True

    def get_file_hash(self, path):
        """Get content hash for change detection"""
        try:
            with open(path, 'rb') as f:
                return hashlib.md5(f.read()).hexdigest()
        except:
            return None

    def index_file(self, path):
        """Index a single file"""
        if not self.should_index(path):
            return False

        try:
            p = Path(path)

            # Read content
            try:
                with open(path, 'r', encoding='utf-8', errors='ignore') as f:
                    content = f.read()
            except:
                return False

            # Get metadata
            file_hash = self.get_file_hash(path)
            modified = datetime.fromtimestamp(p.stat().st_mtime).isoformat()
            preview = content[:500].replace('\n', ' ').strip()

            # Check if already indexed with same hash
            cursor = self.conn.cursor()
            cursor.execute('SELECT hash FROM knowledge WHERE path = ?', (str(path),))
            existing = cursor.fetchone()

            if existing and existing[0] == file_hash:
                return False  # No change

            # Delete old entry if exists
            if existing:
                cursor.execute('DELETE FROM knowledge WHERE path = ?', (str(path),))
                self.stats['files_updated'] += 1
            else:
                self.stats['files_indexed'] += 1

            # Insert new entry
            cursor.execute('''
                INSERT INTO knowledge (path, name, type, content, preview, modified, hash)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            ''', (str(path), p.name, p.suffix, content, preview, modified, file_hash))

            self.conn.commit()
            return True

        except Exception as e:
            logger.error(f"Error indexing {path}: {e}")
            self.stats['errors'] += 1
            return False

    def delete_file(self, path):
        """Remove file from index"""
        try:
            cursor = self.conn.cursor()
            cursor.execute('DELETE FROM knowledge WHERE path = ?', (str(path),))
            if cursor.rowcount > 0:
                self.stats['files_deleted'] += 1
                self.conn.commit()
                return True
        except Exception as e:
            logger.error(f"Error deleting {path}: {e}")
        return False

    def vacuum(self):
        """Full re-index of all directories"""
        logger.info("Starting full vacuum...")
        start_time = time.time()

        for directory in VACUUM_DIRS:
            if not os.path.exists(directory):
                continue

            for root, dirs, files in os.walk(directory):
                # Skip hidden directories
                dirs[:] = [d for d in dirs if not d.startswith('.') and d not in ['node_modules', '__pycache__', 'venv']]

                for file in files:
                    path = os.path.join(root, file)
                    self.index_file(path)

        elapsed = time.time() - start_time
        self.stats['last_vacuum'] = datetime.now().isoformat()
        logger.info(f"Vacuum complete in {elapsed:.2f}s - {self.stats['files_indexed']} indexed, {self.stats['files_updated']} updated")

        return self.stats

    def get_stats(self):
        """Get current statistics"""
        cursor = self.conn.cursor()
        cursor.execute('SELECT COUNT(*) FROM knowledge')
        total = cursor.fetchone()[0]

        cursor.execute('SELECT SUM(LENGTH(content)) FROM knowledge')
        total_chars = cursor.fetchone()[0] or 0

        return {
            **self.stats,
            'total_files': total,
            'total_characters': total_chars,
            'db_path': str(DB_PATH)
        }


class CyclotronHandler(FileSystemEventHandler):
    """Watchdog event handler for file changes"""

    def __init__(self, indexer):
        self.indexer = indexer
        self.last_event = {}
        self.debounce_seconds = 1

    def _should_process(self, path):
        """Debounce rapid events on same file"""
        now = time.time()
        last = self.last_event.get(path, 0)
        if now - last < self.debounce_seconds:
            return False
        self.last_event[path] = now
        return True

    def on_created(self, event):
        if event.is_directory:
            return
        if self._should_process(event.src_path):
            if self.indexer.index_file(event.src_path):
                logger.info(f"Indexed new file: {event.src_path}")

    def on_modified(self, event):
        if event.is_directory:
            return
        if self._should_process(event.src_path):
            if self.indexer.index_file(event.src_path):
                logger.info(f"Re-indexed modified file: {event.src_path}")

    def on_deleted(self, event):
        if event.is_directory:
            return
        if self.indexer.delete_file(event.src_path):
            logger.info(f"Removed deleted file: {event.src_path}")

    def on_moved(self, event):
        if event.is_directory:
            return
        self.indexer.delete_file(event.src_path)
        if self.indexer.index_file(event.dest_path):
            logger.info(f"Moved file: {event.src_path} -> {event.dest_path}")


def save_status(indexer, running=True):
    """Save daemon status to file"""
    status = indexer.get_stats()
    status['running'] = running
    status['pid'] = os.getpid()
    status['updated'] = datetime.now().isoformat()

    with open(STATUS_FILE, 'w') as f:
        json.dump(status, f, indent=2)


def show_status():
    """Display current daemon status"""
    if not STATUS_FILE.exists():
        print("Daemon status: NOT RUNNING (no status file)")
        return

    with open(STATUS_FILE) as f:
        status = json.load(f)

    print("\n=== CYCLOTRON DAEMON STATUS ===")
    print(f"Running: {status.get('running', False)}")
    print(f"PID: {status.get('pid', 'N/A')}")
    print(f"Total Files: {status.get('total_files', 0):,}")
    print(f"Total Characters: {status.get('total_characters', 0):,}")
    print(f"Files Indexed: {status.get('files_indexed', 0)}")
    print(f"Files Updated: {status.get('files_updated', 0)}")
    print(f"Files Deleted: {status.get('files_deleted', 0)}")
    print(f"Errors: {status.get('errors', 0)}")
    print(f"Last Vacuum: {status.get('last_vacuum', 'Never')}")
    print(f"Last Update: {status.get('updated', 'N/A')}")
    print(f"Database: {status.get('db_path', 'N/A')}")
    print("=" * 32)


def run_daemon():
    """Run the daemon with file watching"""
    logger.info("Starting Cyclotron Daemon...")

    # Initialize indexer
    indexer = CyclotronIndexer()

    # Do initial vacuum
    logger.info("Performing initial vacuum...")
    indexer.vacuum()

    # Setup watchdog
    handler = CyclotronHandler(indexer)
    observer = Observer()

    # Watch all directories
    for directory in VACUUM_DIRS:
        if os.path.exists(directory):
            observer.schedule(handler, directory, recursive=True)
            logger.info(f"Watching: {directory}")

    # Start watching
    observer.start()
    logger.info("Daemon running - watching for changes...")

    try:
        while True:
            save_status(indexer, running=True)
            time.sleep(30)  # Update status every 30 seconds

    except KeyboardInterrupt:
        logger.info("Stopping daemon...")
        observer.stop()
        save_status(indexer, running=False)

    observer.join()
    logger.info("Daemon stopped")


if __name__ == '__main__':
    if len(sys.argv) > 1:
        cmd = sys.argv[1].lower()

        if cmd == 'status':
            show_status()

        elif cmd == 'vacuum':
            print("Running manual vacuum...")
            indexer = CyclotronIndexer()
            stats = indexer.vacuum()
            print(f"Vacuum complete: {stats['files_indexed']} indexed, {stats['files_updated']} updated")

        else:
            print(f"Unknown command: {cmd}")
            print("Usage: python CYCLOTRON_DAEMON.py [status|vacuum]")

    else:
        run_daemon()
