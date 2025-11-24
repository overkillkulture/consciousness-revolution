#!/usr/bin/env python3
"""
CYCLOTRON CONTENT INDEXER - The Vacuum & Compressed Unit
=========================================================

VACUUM: Sucks in all content from everywhere
COMPRESSED: Makes it instantly searchable

Uses SQLite FTS5 for lightning-fast full-text search with ranking.
"""

import os
import sqlite3
import json
import hashlib
from pathlib import Path
from datetime import datetime

# Directories to vacuum
VACUUM_DIRS = [
    "C:/Users/dwrek/100X_DEPLOYMENT",
    "C:/Users/dwrek/.consciousness",
    "C:/Users/dwrek/.trinity",
    "C:/Users/dwrek/LOCAL_TRINITY_HUB",
    "C:/Users/dwrek/Desktop",
]

# File types to index
INDEX_EXTENSIONS = ['.md', '.txt', '.py', '.js', '.html', '.json']

# Database location
DB_PATH = Path("C:/Users/dwrek/100X_DEPLOYMENT/.cyclotron_atoms/cyclotron.db")

def init_database():
    """Initialize SQLite database with FTS5 virtual table"""
    DB_PATH.parent.mkdir(exist_ok=True)

    conn = sqlite3.connect(str(DB_PATH))
    cursor = conn.cursor()

    # Create FTS5 virtual table for full-text search
    cursor.execute('''
        CREATE VIRTUAL TABLE IF NOT EXISTS knowledge USING fts5(
            path,
            name,
            type,
            content,
            preview,
            modified,
            hash,
            tokenize='porter unicode61'
        )
    ''')

    # Create metadata table for tracking
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS index_meta (
            key TEXT PRIMARY KEY,
            value TEXT
        )
    ''')

    conn.commit()
    return conn

def extract_content(filepath):
    """Extract text content from file"""
    try:
        with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
            content = f.read()
        return content
    except:
        return ""

def get_file_hash(content):
    """Generate hash of content for change detection"""
    return hashlib.md5(content.encode()).hexdigest()

def vacuum_knowledge(conn):
    """Vacuum up all knowledge from directories"""
    cursor = conn.cursor()

    # Clear existing index for fresh rebuild
    cursor.execute('DELETE FROM knowledge')

    indexed_count = 0
    total_chars = 0

    for vacuum_dir in VACUUM_DIRS:
        if not os.path.exists(vacuum_dir):
            print(f"⚠️  Directory not found: {vacuum_dir}")
            continue

        print(f"🔍 Vacuuming: {vacuum_dir}")

        for root, dirs, files in os.walk(vacuum_dir):
            # Skip hidden and build directories
            dirs[:] = [d for d in dirs if not d.startswith('.') and d not in [
                'node_modules', '__pycache__', '.git', 'venv', 'env'
            ]]

            for file in files:
                ext = Path(file).suffix.lower()
                if ext not in INDEX_EXTENSIONS:
                    continue

                filepath = os.path.join(root, file)

                try:
                    # Extract content
                    content = extract_content(filepath)
                    if not content:
                        continue

                    # Get metadata
                    stat = os.stat(filepath)
                    file_hash = get_file_hash(content)
                    preview = content[:500].replace('\n', ' ')

                    # Insert into FTS5 table
                    cursor.execute('''
                        INSERT INTO knowledge (path, name, type, content, preview, modified, hash)
                        VALUES (?, ?, ?, ?, ?, ?, ?)
                    ''', (
                        filepath,
                        file,
                        ext[1:],  # Remove the dot
                        content,
                        preview,
                        int(stat.st_mtime),
                        file_hash
                    ))

                    indexed_count += 1
                    total_chars += len(content)

                except Exception as e:
                    print(f"  ❌ Error indexing {filepath}: {e}")

    # Update metadata
    cursor.execute('''
        INSERT OR REPLACE INTO index_meta (key, value)
        VALUES ('last_indexed', ?)
    ''', (datetime.now().isoformat(),))

    cursor.execute('''
        INSERT OR REPLACE INTO index_meta (key, value)
        VALUES ('total_files', ?)
    ''', (str(indexed_count),))

    cursor.execute('''
        INSERT OR REPLACE INTO index_meta (key, value)
        VALUES ('total_chars', ?)
    ''', (str(total_chars),))

    conn.commit()

    return indexed_count, total_chars

def search(conn, query, limit=20):
    """Search the knowledge base"""
    cursor = conn.cursor()

    # FTS5 search with BM25 ranking
    cursor.execute('''
        SELECT
            path,
            name,
            type,
            preview,
            modified,
            bm25(knowledge) as score
        FROM knowledge
        WHERE knowledge MATCH ?
        ORDER BY score
        LIMIT ?
    ''', (query, limit))

    results = []
    for row in cursor.fetchall():
        results.append({
            'path': row[0],
            'name': row[1],
            'type': row[2],
            'preview': row[3],
            'modified': row[4],
            'score': row[5]
        })

    return results

def get_snippet(conn, query, filepath):
    """Get snippet with highlighted matches from a specific file"""
    cursor = conn.cursor()

    cursor.execute('''
        SELECT snippet(knowledge, 3, '>>>>', '<<<<', '...', 50)
        FROM knowledge
        WHERE knowledge MATCH ? AND path = ?
    ''', (query, filepath))

    row = cursor.fetchone()
    return row[0] if row else None

def get_stats(conn):
    """Get index statistics"""
    cursor = conn.cursor()

    # Get metadata
    cursor.execute('SELECT key, value FROM index_meta')
    meta = dict(cursor.fetchall())

    # Get type breakdown
    cursor.execute('''
        SELECT type, COUNT(*)
        FROM knowledge
        GROUP BY type
        ORDER BY COUNT(*) DESC
    ''')
    types = dict(cursor.fetchall())

    return {
        'last_indexed': meta.get('last_indexed', 'Never'),
        'total_files': int(meta.get('total_files', 0)),
        'total_chars': int(meta.get('total_chars', 0)),
        'types': types
    }

if __name__ == "__main__":
    print("=" * 60)
    print("🌀 CYCLOTRON CONTENT INDEXER")
    print("   The Vacuum & Compressed Unit")
    print("=" * 60)
    print()

    # Initialize database
    print("📦 Initializing database...")
    conn = init_database()

    # Vacuum all knowledge
    print()
    print("🔄 Starting vacuum cycle...")
    print()

    indexed, chars = vacuum_knowledge(conn)

    print()
    print("=" * 60)
    print(f"✅ VACUUM COMPLETE")
    print(f"   Files indexed: {indexed}")
    print(f"   Characters: {chars:,}")
    print(f"   Database: {DB_PATH}")
    print("=" * 60)
    print()

    # Show stats
    stats = get_stats(conn)
    print("📊 Index Statistics:")
    print(f"   Last indexed: {stats['last_indexed']}")
    for file_type, count in stats['types'].items():
        print(f"   .{file_type}: {count} files")
    print()

    # Test search
    print("🔍 Test search: 'consciousness'")
    results = search(conn, 'consciousness', limit=5)
    for r in results:
        print(f"   [{r['type']}] {r['name']}")
        print(f"        {r['preview'][:100]}...")
        print()

    conn.close()
    print("✅ Cyclotron ready. Run CYCLOTRON_SEARCH_V2.py for API.")
