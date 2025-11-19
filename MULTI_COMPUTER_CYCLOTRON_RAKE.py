"""
MULTI-COMPUTER CYCLOTRON RAKE - Federation via Dropbox

Each computer runs this to:
1. Rake all local knowledge (brain, deployment, docs, code)
2. Upload atoms to Dropbox/.cyclotron_federation/
3. Sync shared index across all computers
4. Unified knowledge base accessible from any computer

Commander's 3 computers + beta testers = ONE GIANT BRAIN
"""

import os
import json
import time
from pathlib import Path
from datetime import datetime
import hashlib

class FederatedCyclotronRake:
    """Rake local computer and sync to Dropbox cloud"""

    def __init__(self):
        self.home = Path.home()

        # Local paths
        self.deployment = self.home / '100X_DEPLOYMENT'
        self.consciousness = self.home / '.consciousness'

        # Dropbox federation path
        self.dropbox = self.home / 'Dropbox'
        self.federation = self.dropbox / '.cyclotron_federation'

        # Computer identity
        self.computer_id = self.get_computer_id()

        # Create federation structure
        self.setup_federation()

        print(f"🌐 Federated Cyclotron Rake")
        print(f"📍 Computer ID: {self.computer_id}")
        print(f"☁️  Federation: {self.federation}")
        print()

    def get_computer_id(self):
        """Generate unique computer ID"""
        import socket
        hostname = socket.gethostname()

        # Clean hostname for filename
        computer_id = hostname.lower().replace(' ', '_').replace('-', '_')

        return computer_id

    def setup_federation(self):
        """Create Dropbox federation structure"""

        # Main folders
        (self.federation / 'atoms').mkdir(parents=True, exist_ok=True)
        (self.federation / 'indices').mkdir(parents=True, exist_ok=True)
        (self.federation / 'computers').mkdir(parents=True, exist_ok=True)
        (self.federation / 'shared_knowledge').mkdir(parents=True, exist_ok=True)

        print(f"✅ Federation structure ready at: {self.federation}")

    def rake_local_knowledge(self):
        """Rake all knowledge from this computer"""

        print("🔍 Raking local knowledge...")
        print()

        atoms = []
        sources_checked = 0

        # Source 1: Brain files
        brain_dir = self.consciousness / 'brain'
        if brain_dir.exists():
            for brain_file in brain_dir.glob('*.json'):
                atom = self.atomize_file('brain', brain_file)
                if atom:
                    atoms.append(atom)
                    sources_checked += 1

        # Source 2: Deployment docs
        if self.deployment.exists():
            for doc in self.deployment.glob('*.md'):
                atom = self.atomize_file('deployment_docs', doc)
                if atom:
                    atoms.append(atom)
                    sources_checked += 1

        # Source 3: Python files
        if self.deployment.exists():
            for py_file in self.deployment.glob('*.py'):
                atom = self.atomize_file('deployment_code', py_file)
                if atom:
                    atoms.append(atom)
                    sources_checked += 1

        # Source 4: Session summaries
        summaries = self.consciousness / 'session_summaries'
        if summaries.exists():
            for summary in summaries.glob('*.md'):
                atom = self.atomize_file('session_summary', summary)
                if atom:
                    atoms.append(atom)
                    sources_checked += 1

        print(f"📊 Raked {len(atoms)} atoms from {sources_checked} sources")
        print()

        return atoms

    def atomize_file(self, source_type, file_path):
        """Convert file into knowledge atom"""

        try:
            content = file_path.read_text(encoding='utf-8', errors='ignore')

            # Skip empty files
            if not content.strip():
                return None

            # Create atom
            atom = {
                'id': hashlib.md5(str(file_path).encode()).hexdigest(),
                'source_type': source_type,
                'source_file': str(file_path),
                'computer_id': self.computer_id,
                'content': content[:10000],  # First 10k chars
                'size': len(content),
                'timestamp': datetime.now().isoformat(),
                'file_name': file_path.name
            }

            return atom

        except Exception as e:
            print(f"⚠️  Error atomizing {file_path.name}: {e}")
            return None

    def upload_to_federation(self, atoms):
        """Upload atoms to Dropbox federation"""

        print(f"☁️  Uploading {len(atoms)} atoms to federation...")

        # Computer-specific atom file
        atom_file = self.federation / 'atoms' / f'{self.computer_id}_atoms.json'

        # Write atoms
        with open(atom_file, 'w') as f:
            json.dump(atoms, f, indent=2)

        print(f"✅ Uploaded to: {atom_file}")
        print()

        return atom_file

    def update_federation_index(self):
        """Update shared federation index"""

        print("📇 Updating federation index...")

        # Read all computer atom files
        all_atoms = []
        computers = []

        atoms_dir = self.federation / 'atoms'
        for atom_file in atoms_dir.glob('*_atoms.json'):
            try:
                with open(atom_file) as f:
                    computer_atoms = json.load(f)
                    all_atoms.extend(computer_atoms)

                    # Extract computer ID from filename
                    comp_id = atom_file.stem.replace('_atoms', '')
                    computers.append(comp_id)
            except Exception as e:
                print(f"⚠️  Error reading {atom_file.name}: {e}")

        # Create unified index
        index = {
            'total_atoms': len(all_atoms),
            'computers': computers,
            'last_updated': datetime.now().isoformat(),
            'atoms_by_computer': {},
            'atoms_by_type': {}
        }

        # Count by computer
        for computer in computers:
            count = sum(1 for a in all_atoms if a.get('computer_id') == computer)
            index['atoms_by_computer'][computer] = count

        # Count by type
        for atom in all_atoms:
            source_type = atom.get('source_type', 'unknown')
            index['atoms_by_type'][source_type] = index['atoms_by_type'].get(source_type, 0) + 1

        # Save index
        index_file = self.federation / 'indices' / 'federation_index.json'
        with open(index_file, 'w') as f:
            json.dump(index, f, indent=2)

        print(f"✅ Federation index updated: {len(all_atoms)} total atoms")
        print(f"   Computers in network: {len(computers)}")
        print()

        for comp_id, count in index['atoms_by_computer'].items():
            print(f"   {comp_id}: {count} atoms")

        print()

        return index

    def register_computer(self):
        """Register this computer in federation"""

        import socket
        import platform

        computer_info = {
            'computer_id': self.computer_id,
            'hostname': socket.gethostname(),
            'platform': platform.system(),
            'last_seen': datetime.now().isoformat(),
            'dropbox_path': str(self.dropbox),
            'status': 'active'
        }

        # Save computer registration
        computer_file = self.federation / 'computers' / f'{self.computer_id}.json'
        with open(computer_file, 'w') as f:
            json.dump(computer_info, f, indent=2)

        print(f"✅ Computer registered in federation")

    def run_full_rake(self):
        """Run complete rake and federation sync"""

        print("="*70)
        print("🌐 MULTI-COMPUTER CYCLOTRON RAKE - FEDERATION MODE")
        print("="*70)
        print()

        # Register this computer
        self.register_computer()
        print()

        # Rake local knowledge
        atoms = self.rake_local_knowledge()

        if not atoms:
            print("⚠️  No atoms raked. Check source directories.")
            return

        # Upload to federation
        self.upload_to_federation(atoms)

        # Update shared index
        index = self.update_federation_index()

        print("="*70)
        print("✅ FEDERATION RAKE COMPLETE")
        print("="*70)
        print()
        print(f"This computer contributed: {len(atoms)} atoms")
        print(f"Federation total: {index['total_atoms']} atoms")
        print(f"Computers in network: {len(index['computers'])}")
        print()
        print("☁️  All knowledge synced to Dropbox")
        print("🌐 Other computers can now access this knowledge")
        print()


def main():
    """Run federated cyclotron rake"""

    rake = FederatedCyclotronRake()
    rake.run_full_rake()


if __name__ == '__main__':
    main()
