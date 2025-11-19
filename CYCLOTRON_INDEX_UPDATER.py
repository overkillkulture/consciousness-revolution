#!/usr/bin/env python3
"""
Cyclotron Index Updater - Updates the searchable index
"""
import json
from pathlib import Path
from datetime import datetime

def update_index():
    """Update the cyclotron index from latest atoms"""
    atoms_dir = Path("C:/Users/dwrek/100X_DEPLOYMENT/.cyclotron_atoms")

    if not atoms_dir.exists():
        print("⚠️  No atoms directory found")
        return

    # Find latest atoms file
    atom_files = sorted(atoms_dir.glob("atoms_*.json"))
    if not atom_files:
        print("⚠️  No atom files found")
        return

    latest_atoms = atom_files[-1]

    # Load atoms
    with open(latest_atoms) as f:
        atoms = json.load(f)

    # Create index
    index = {
        'total_atoms': len(atoms),
        'last_updated': int(datetime.now().timestamp()),
        'atoms_by_type': {},
        'atoms': atoms
    }

    # Count by type
    for atom in atoms:
        atom_type = atom.get('type', 'unknown')
        index['atoms_by_type'][atom_type] = index['atoms_by_type'].get(atom_type, 0) + 1

    # Save index
    index_file = Path("C:/Users/dwrek/100X_DEPLOYMENT/.cyclotron_atoms/index.json")
    with open(index_file, 'w') as f:
        json.dump(index, f, indent=2)

    print(f"✅ Index updated: {len(atoms)} atoms")
    print(f"📊 By type: {index['atoms_by_type']}")

if __name__ == "__main__":
    print("📊 Updating cyclotron index...")
    update_index()
