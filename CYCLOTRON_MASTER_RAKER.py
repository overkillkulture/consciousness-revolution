#!/usr/bin/env python3
"""
Cyclotron Master Raker - Indexes knowledge across the entire system
"""
import os
import json
from pathlib import Path
from datetime import datetime

# Directories to rake
RAKE_DIRS = [
    "C:/Users/dwrek/100X_DEPLOYMENT",
    "C:/Users/dwrek/.consciousness",
    "C:/Users/dwrek/.trinity",
]

# File types to index
INDEX_EXTENSIONS = ['.md', '.txt', '.py', '.js', '.html', '.json']

def rake_knowledge():
    """Rake through directories and collect knowledge atoms"""
    atoms = []

    for rake_dir in RAKE_DIRS:
        if not os.path.exists(rake_dir):
            continue

        for root, dirs, files in os.walk(rake_dir):
            # Skip hidden and build directories
            dirs[:] = [d for d in dirs if not d.startswith('.') and d not in ['node_modules', '__pycache__']]

            for file in files:
                ext = Path(file).suffix
                if ext in INDEX_EXTENSIONS:
                    filepath = os.path.join(root, file)
                    try:
                        stat = os.stat(filepath)
                        atoms.append({
                            'path': filepath,
                            'name': file,
                            'type': ext[1:],
                            'size': stat.st_size,
                            'modified': int(stat.st_mtime)
                        })
                    except:
                        pass

    return atoms

if __name__ == "__main__":
    print(f"🔍 Raking knowledge atoms...")
    atoms = rake_knowledge()

    # Save to atoms directory
    output_dir = Path("C:/Users/dwrek/100X_DEPLOYMENT/.cyclotron_atoms")
    output_dir.mkdir(exist_ok=True)

    output_file = output_dir / f"atoms_{datetime.now().strftime('%Y%m%d')}.json"

    with open(output_file, 'w') as f:
        json.dump(atoms, f, indent=2)

    print(f"✅ Raked {len(atoms)} atoms")
    print(f"📁 Saved to {output_file}")
