#!/usr/bin/env python3
"""
Cyclotron Search API - Query the knowledge base
"""

import json
import re
from pathlib import Path
from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

ATOMS_DIR = Path.home() / '100X_DEPLOYMENT' / '.cyclotron_atoms'

def load_index():
    """Load the current index"""
    index_file = ATOMS_DIR / 'index.json'
    if not index_file.exists():
        return None
    with open(index_file) as f:
        return json.load(f)

def search_atoms(query, atom_type=None, limit=50):
    """Search atoms by query string"""
    index = load_index()
    if not index:
        return []

    atoms = index.get('atoms', [])
    results = []

    query_lower = query.lower()

    for atom in atoms:
        # Search in name and path
        name = atom.get('name', '').lower()
        path = atom.get('path', '').lower()

        if query_lower in name or query_lower in path:
            # Filter by type if specified
            if atom_type and atom.get('type') != atom_type:
                continue

            results.append({
                'name': atom.get('name'),
                'path': atom.get('path'),
                'type': atom.get('type'),
                'size': atom.get('size'),
                'modified': atom.get('modified')
            })

            if len(results) >= limit:
                break

    return results

@app.route('/api/search', methods=['GET'])
def api_search():
    """Search endpoint"""
    query = request.args.get('q', '')
    atom_type = request.args.get('type', None)
    limit = int(request.args.get('limit', 50))

    if not query:
        return jsonify({'error': 'Query required'}), 400

    results = search_atoms(query, atom_type, limit)
    return jsonify({
        'query': query,
        'count': len(results),
        'results': results
    })

@app.route('/api/stats', methods=['GET'])
def api_stats():
    """Get index statistics"""
    index = load_index()
    if not index:
        return jsonify({'error': 'Index not found'}), 404

    return jsonify({
        'total_atoms': index.get('total_atoms', 0),
        'last_updated': index.get('last_updated', 0),
        'atoms_by_type': index.get('atoms_by_type', {})
    })

@app.route('/api/types', methods=['GET'])
def api_types():
    """Get all atom types"""
    index = load_index()
    if not index:
        return jsonify({'error': 'Index not found'}), 404

    return jsonify({
        'types': list(index.get('atoms_by_type', {}).keys())
    })

@app.route('/api/recent', methods=['GET'])
def api_recent():
    """Get most recently modified atoms"""
    limit = int(request.args.get('limit', 20))
    index = load_index()
    if not index:
        return jsonify({'error': 'Index not found'}), 404

    atoms = sorted(
        index.get('atoms', []),
        key=lambda x: x.get('modified', 0),
        reverse=True
    )[:limit]

    return jsonify({
        'count': len(atoms),
        'atoms': atoms
    })

if __name__ == '__main__':
    print("Cyclotron Search API")
    print("Endpoints:")
    print("  /api/search?q=<query>&type=<type>&limit=<n>")
    print("  /api/stats")
    print("  /api/types")
    print("  /api/recent?limit=<n>")
    app.run(host='0.0.0.0', port=6668, debug=True)
