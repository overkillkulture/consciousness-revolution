#!/usr/bin/env python3
"""
CYCLOTRON SEARCH V2 - Full Content Search API
==============================================

Searches the actual CONTENT of files, not just filenames.
Returns relevant passages with context.
"""

import sqlite3
from pathlib import Path
from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

DB_PATH = Path.home() / '100X_DEPLOYMENT' / '.cyclotron_atoms' / 'cyclotron.db'

def get_db():
    """Get database connection"""
    if not DB_PATH.exists():
        return None
    return sqlite3.connect(str(DB_PATH))

@app.route('/api/search', methods=['GET'])
def api_search():
    """
    Full-text content search with relevance ranking

    Query params:
      q: search query (required)
      type: filter by file type
      limit: max results (default 20)
    """
    query = request.args.get('q', '')
    file_type = request.args.get('type', None)
    limit = int(request.args.get('limit', 20))

    if not query:
        return jsonify({'error': 'Query required', 'hint': 'Use ?q=your+search+terms'}), 400

    conn = get_db()
    if not conn:
        return jsonify({'error': 'Database not found', 'hint': 'Run CYCLOTRON_CONTENT_INDEXER.py first'}), 404

    cursor = conn.cursor()

    try:
        # Build query with optional type filter
        if file_type:
            cursor.execute('''
                SELECT
                    path,
                    name,
                    type,
                    snippet(knowledge, 3, '**', '**', '...', 64) as snippet,
                    modified,
                    bm25(knowledge) as score
                FROM knowledge
                WHERE knowledge MATCH ? AND type = ?
                ORDER BY score
                LIMIT ?
            ''', (query, file_type, limit))
        else:
            cursor.execute('''
                SELECT
                    path,
                    name,
                    type,
                    snippet(knowledge, 3, '**', '**', '...', 64) as snippet,
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
                'snippet': row[3],
                'modified': row[4],
                'score': round(abs(row[5]), 3)
            })

        return jsonify({
            'query': query,
            'count': len(results),
            'results': results
        })

    except Exception as e:
        return jsonify({'error': str(e)}), 500
    finally:
        conn.close()

@app.route('/api/ask', methods=['GET'])
def api_ask():
    """
    Natural language query - returns the most relevant knowledge

    This is for questions like "What do I know about manipulation immunity?"
    """
    question = request.args.get('q', '')
    limit = int(request.args.get('limit', 5))

    if not question:
        return jsonify({'error': 'Question required'}), 400

    conn = get_db()
    if not conn:
        return jsonify({'error': 'Database not found'}), 404

    cursor = conn.cursor()

    try:
        # Extract key terms from question (simple approach)
        # Remove common words
        stopwords = {'what', 'how', 'why', 'when', 'where', 'do', 'i', 'know', 'about', 'the', 'a', 'an', 'is', 'are', 'was', 'were', 'my', 'to', 'for'}
        terms = [w for w in question.lower().split() if w not in stopwords and len(w) > 2]
        search_query = ' OR '.join(terms) if terms else question

        cursor.execute('''
            SELECT
                path,
                name,
                snippet(knowledge, 3, '>>>', '<<<', '...', 100) as snippet,
                bm25(knowledge) as score
            FROM knowledge
            WHERE knowledge MATCH ?
            ORDER BY score
            LIMIT ?
        ''', (search_query, limit))

        results = []
        for row in cursor.fetchall():
            results.append({
                'source': row[1],
                'path': row[0],
                'answer': row[2],
                'relevance': round(abs(row[3]), 3)
            })

        return jsonify({
            'question': question,
            'search_terms': terms,
            'answers': results
        })

    except Exception as e:
        return jsonify({'error': str(e)}), 500
    finally:
        conn.close()

@app.route('/api/stats', methods=['GET'])
def api_stats():
    """Get index statistics"""
    conn = get_db()
    if not conn:
        return jsonify({'error': 'Database not found'}), 404

    cursor = conn.cursor()

    try:
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

        return jsonify({
            'status': 'operational',
            'last_indexed': meta.get('last_indexed', 'Never'),
            'total_files': int(meta.get('total_files', 0)),
            'total_characters': int(meta.get('total_chars', 0)),
            'files_by_type': types
        })

    except Exception as e:
        return jsonify({'error': str(e)}), 500
    finally:
        conn.close()

@app.route('/api/recent', methods=['GET'])
def api_recent():
    """Get most recently modified files"""
    limit = int(request.args.get('limit', 20))

    conn = get_db()
    if not conn:
        return jsonify({'error': 'Database not found'}), 404

    cursor = conn.cursor()

    try:
        cursor.execute('''
            SELECT path, name, type, preview, modified
            FROM knowledge
            ORDER BY modified DESC
            LIMIT ?
        ''', (limit,))

        results = []
        for row in cursor.fetchall():
            results.append({
                'path': row[0],
                'name': row[1],
                'type': row[2],
                'preview': row[3][:200],
                'modified': row[4]
            })

        return jsonify({
            'count': len(results),
            'files': results
        })

    except Exception as e:
        return jsonify({'error': str(e)}), 500
    finally:
        conn.close()

@app.route('/api/file', methods=['GET'])
def api_file():
    """Get full content of a specific file"""
    filepath = request.args.get('path', '')

    if not filepath:
        return jsonify({'error': 'Path required'}), 400

    conn = get_db()
    if not conn:
        return jsonify({'error': 'Database not found'}), 404

    cursor = conn.cursor()

    try:
        cursor.execute('''
            SELECT name, type, content, modified
            FROM knowledge
            WHERE path = ?
        ''', (filepath,))

        row = cursor.fetchone()
        if not row:
            return jsonify({'error': 'File not found in index'}), 404

        return jsonify({
            'name': row[0],
            'type': row[1],
            'content': row[2],
            'modified': row[3]
        })

    except Exception as e:
        return jsonify({'error': str(e)}), 500
    finally:
        conn.close()

@app.route('/api/health', methods=['GET'])
def api_health():
    """Health check"""
    conn = get_db()
    db_exists = conn is not None
    if conn:
        conn.close()

    return jsonify({
        'status': 'healthy' if db_exists else 'no database',
        'database': str(DB_PATH),
        'database_exists': db_exists
    })

if __name__ == '__main__':
    print("=" * 60)
    print("🌀 CYCLOTRON SEARCH V2 - Full Content Search")
    print("=" * 60)
    print()
    print("Endpoints:")
    print("  /api/search?q=<query>     - Search file contents")
    print("  /api/ask?q=<question>     - Ask a question")
    print("  /api/stats                - Index statistics")
    print("  /api/recent               - Recently modified")
    print("  /api/file?path=<path>     - Get file content")
    print("  /api/health               - Health check")
    print()
    print("Examples:")
    print("  /api/search?q=manipulation+immunity")
    print("  /api/ask?q=What+do+I+know+about+Trinity")
    print()

    app.run(host='0.0.0.0', port=6669, debug=True)
