#!/usr/bin/env python3
"""
CYCLOTRON-BRAIN BRIDGE
Direct integration between C2's brain agents and C1's Cyclotron knowledge base.
Creates, queries, and manages knowledge atoms with agent intelligence.
"""

import json
import hashlib
from pathlib import Path
from datetime import datetime
from typing import Optional, List, Dict
import re

# Paths
HOME = Path.home()
CONSCIOUSNESS = HOME / ".consciousness"
CYCLOTRON = CONSCIOUSNESS / "cyclotron_core"
BRAIN = CONSCIOUSNESS / "brain"
AGENTS = CONSCIOUSNESS / "agents"

# Ensure paths exist
CYCLOTRON.mkdir(parents=True, exist_ok=True)
BRAIN.mkdir(parents=True, exist_ok=True)
AGENTS.mkdir(parents=True, exist_ok=True)


class KnowledgeAtom:
    """Single unit of knowledge in the Cyclotron."""

    def __init__(self, content: str, atom_type: str = "fact", source: str = "agent"):
        self.id = self._generate_id(content)
        self.content = content
        self.atom_type = atom_type  # fact, insight, decision, pattern, action, concept
        self.source = source
        self.tags = []
        self.links = []  # IDs of related atoms
        self.created = datetime.now().isoformat()
        self.updated = self.created
        self.confidence = 1.0
        self.usage_count = 0
        self.metadata = {}

    def _generate_id(self, content: str) -> str:
        """Generate unique ID from content hash."""
        return hashlib.sha256(content.encode()).hexdigest()[:12]

    def add_tag(self, tag: str):
        """Add tag to atom."""
        if tag not in self.tags:
            self.tags.append(tag.lower())

    def add_link(self, atom_id: str):
        """Link to another atom."""
        if atom_id not in self.links:
            self.links.append(atom_id)

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "content": self.content,
            "type": self.atom_type,
            "source": self.source,
            "tags": self.tags,
            "links": self.links,
            "created": self.created,
            "updated": self.updated,
            "confidence": self.confidence,
            "usage_count": self.usage_count,
            "metadata": self.metadata
        }

    @classmethod
    def from_dict(cls, data: dict) -> 'KnowledgeAtom':
        atom = cls(data["content"], data.get("type", "fact"), data.get("source", "unknown"))
        atom.id = data["id"]
        atom.tags = data.get("tags", [])
        atom.links = data.get("links", [])
        atom.created = data.get("created", atom.created)
        atom.updated = data.get("updated", atom.updated)
        atom.confidence = data.get("confidence", 1.0)
        atom.usage_count = data.get("usage_count", 0)
        atom.metadata = data.get("metadata", {})
        return atom


class CyclotronBridge:
    """Bridge between Brain Agents and Cyclotron."""

    def __init__(self):
        self.index_path = CYCLOTRON / "INDEX.json"
        self.atoms_path = CYCLOTRON / "atoms"
        self.atoms_path.mkdir(exist_ok=True)
        self._load_index()

    def _load_index(self):
        """Load or create index."""
        if self.index_path.exists():
            with open(self.index_path) as f:
                self.index = json.load(f)
        else:
            self.index = {
                "atoms": [],
                "tags": {},
                "types": {},
                "stats": {
                    "total": 0,
                    "by_type": {},
                    "by_source": {}
                },
                "updated": datetime.now().isoformat()
            }

    def _save_index(self):
        """Save index."""
        self.index["updated"] = datetime.now().isoformat()
        with open(self.index_path, 'w') as f:
            json.dump(self.index, f, indent=2)

    # === ATOM OPERATIONS ===

    def create_atom(self, content: str, atom_type: str = "fact",
                   source: str = "agent", tags: List[str] = None) -> KnowledgeAtom:
        """Create and store a new knowledge atom."""
        atom = KnowledgeAtom(content, atom_type, source)

        # Auto-tag based on content
        auto_tags = self._auto_tag(content)
        for tag in auto_tags:
            atom.add_tag(tag)

        # Add provided tags
        if tags:
            for tag in tags:
                atom.add_tag(tag)

        # Save atom
        atom_file = self.atoms_path / f"{atom.id}.json"
        with open(atom_file, 'w') as f:
            json.dump(atom.to_dict(), f, indent=2)

        # Update index
        self.index["atoms"].append({
            "id": atom.id,
            "preview": content[:100],
            "type": atom_type,
            "tags": atom.tags
        })

        # Update tag index
        for tag in atom.tags:
            if tag not in self.index["tags"]:
                self.index["tags"][tag] = []
            self.index["tags"][tag].append(atom.id)

        # Update type index
        if atom_type not in self.index["types"]:
            self.index["types"][atom_type] = []
        self.index["types"][atom_type].append(atom.id)

        # Update stats
        self.index["stats"]["total"] += 1
        self.index["stats"]["by_type"][atom_type] = self.index["stats"]["by_type"].get(atom_type, 0) + 1
        self.index["stats"]["by_source"][source] = self.index["stats"]["by_source"].get(source, 0) + 1

        self._save_index()

        print(f"Created atom {atom.id}: {content[:50]}...")
        return atom

    def get_atom(self, atom_id: str) -> Optional[KnowledgeAtom]:
        """Retrieve atom by ID."""
        atom_file = self.atoms_path / f"{atom_id}.json"
        if atom_file.exists():
            with open(atom_file) as f:
                data = json.load(f)
            atom = KnowledgeAtom.from_dict(data)

            # Increment usage
            atom.usage_count += 1
            with open(atom_file, 'w') as f:
                json.dump(atom.to_dict(), f, indent=2)

            return atom
        return None

    def search(self, query: str, limit: int = 10) -> List[KnowledgeAtom]:
        """Search atoms by content."""
        results = []
        query_lower = query.lower()
        keywords = query_lower.split()

        for atom_ref in self.index["atoms"]:
            atom = self.get_atom(atom_ref["id"])
            if atom:
                # Score based on keyword matches
                score = 0
                content_lower = atom.content.lower()

                for kw in keywords:
                    if kw in content_lower:
                        score += 1
                    if kw in atom.tags:
                        score += 2

                if score > 0:
                    results.append((score, atom))

        # Sort by score
        results.sort(key=lambda x: x[0], reverse=True)
        return [atom for _, atom in results[:limit]]

    def search_by_tag(self, tag: str) -> List[KnowledgeAtom]:
        """Get all atoms with tag."""
        atom_ids = self.index["tags"].get(tag.lower(), [])
        return [self.get_atom(aid) for aid in atom_ids if self.get_atom(aid)]

    def search_by_type(self, atom_type: str) -> List[KnowledgeAtom]:
        """Get all atoms of type."""
        atom_ids = self.index["types"].get(atom_type, [])
        return [self.get_atom(aid) for aid in atom_ids if self.get_atom(aid)]

    def link_atoms(self, atom_id1: str, atom_id2: str):
        """Create bidirectional link between atoms."""
        atom1 = self.get_atom(atom_id1)
        atom2 = self.get_atom(atom_id2)

        if atom1 and atom2:
            atom1.add_link(atom_id2)
            atom2.add_link(atom_id1)

            # Save both
            with open(self.atoms_path / f"{atom_id1}.json", 'w') as f:
                json.dump(atom1.to_dict(), f, indent=2)
            with open(self.atoms_path / f"{atom_id2}.json", 'w') as f:
                json.dump(atom2.to_dict(), f, indent=2)

            print(f"Linked atoms: {atom_id1} <-> {atom_id2}")

    def _auto_tag(self, content: str) -> List[str]:
        """Auto-generate tags from content."""
        tags = []
        content_lower = content.lower()

        # Domain detection
        domain_keywords = {
            "media": ["news", "media", "article", "headline", "reporter", "journalist"],
            "relationships": ["relationship", "family", "friend", "partner", "marriage", "love"],
            "finance": ["money", "finance", "investment", "stock", "budget", "revenue", "profit"],
            "authority": ["government", "law", "policy", "regulation", "authority", "official"],
            "self": ["personal", "self", "identity", "growth", "mindset", "belief"],
            "groups": ["team", "group", "community", "organization", "culture"],
            "digital": ["code", "software", "api", "data", "algorithm", "system", "tech"]
        }

        for domain, keywords in domain_keywords.items():
            if any(kw in content_lower for kw in keywords):
                tags.append(domain)

        # Technology detection
        tech_patterns = {
            "python": r'\bpython\b',
            "javascript": r'\bjavascript\b|\bnode\b|\bjs\b',
            "api": r'\bapi\b',
            "database": r'\bdatabase\b|\bsql\b|\bquery\b',
            "ai": r'\bai\b|\bmachine learning\b|\bneural\b|\bgpt\b|\bclaude\b',
            "automation": r'\bautomat\w*\b',
        }

        for tag, pattern in tech_patterns.items():
            if re.search(pattern, content_lower):
                tags.append(tag)

        return tags

    # === BRAIN INTEGRATION ===

    def ingest_from_brain(self):
        """Ingest knowledge from brain files into Cyclotron."""
        ingested = 0

        # Ingest from brain files
        for brain_file in BRAIN.glob("*.json"):
            with open(brain_file) as f:
                data = json.load(f)

            # Handle different structures
            if isinstance(data, dict):
                if "metrics" in data:
                    for metric in data["metrics"]:
                        atom = self.create_atom(
                            f"Metric: {metric.get('name', 'unknown')} = {metric.get('actual', '?')} (goal: {metric.get('goal', '?')})",
                            atom_type="fact",
                            source="brain_scorecard",
                            tags=["metric", "scorecard"]
                        )
                        ingested += 1

                if "rocks" in data:
                    for rock in data["rocks"]:
                        atom = self.create_atom(
                            f"Rock: {rock.get('rock', 'unknown')} - Owner: {rock.get('owner', '?')} - Status: {rock.get('status', '?')}",
                            atom_type="action",
                            source="brain_rocks",
                            tags=["rock", "quarterly", "goal"]
                        )
                        ingested += 1

                if "issues" in data:
                    for issue in data["issues"]:
                        atom = self.create_atom(
                            f"Issue: {issue.get('issue', 'unknown')} - Priority: {issue.get('priority', '?')}",
                            atom_type="pattern",
                            source="brain_issues",
                            tags=["issue", "problem"]
                        )
                        ingested += 1

        print(f"Ingested {ingested} atoms from brain")
        return ingested

    def export_to_brain(self) -> dict:
        """Export Cyclotron summary to brain."""
        summary = {
            "total_atoms": self.index["stats"]["total"],
            "by_type": self.index["stats"]["by_type"],
            "by_source": self.index["stats"]["by_source"],
            "top_tags": sorted(
                [(tag, len(ids)) for tag, ids in self.index["tags"].items()],
                key=lambda x: x[1],
                reverse=True
            )[:20],
            "exported": datetime.now().isoformat()
        }

        export_path = BRAIN / "cyclotron_summary.json"
        with open(export_path, 'w') as f:
            json.dump(summary, f, indent=2)

        print(f"Exported Cyclotron summary to brain: {self.index['stats']['total']} atoms")
        return summary

    # === AGENT OUTPUTS ===

    def store_agent_output(self, agent_name: str, task: str, outputs: List[dict],
                          decisions: List[dict], memory: List[dict]):
        """Store agent execution results as atoms."""
        created = []

        # Store task as action
        task_atom = self.create_atom(
            f"Task: {task}",
            atom_type="action",
            source=f"agent_{agent_name}",
            tags=["task", "agent"]
        )
        created.append(task_atom)

        # Store decisions
        for decision in decisions:
            dec_atom = self.create_atom(
                f"Decision: {decision.get('decision', '')} - Rationale: {decision.get('rationale', '')}",
                atom_type="decision",
                source=f"agent_{agent_name}",
                tags=["decision", "agent"]
            )
            created.append(dec_atom)
            self.link_atoms(task_atom.id, dec_atom.id)

        # Store insights from memory
        for mem in memory:
            if mem.get("category") in ["insight", "pattern", "learning"]:
                insight_atom = self.create_atom(
                    mem.get("content", ""),
                    atom_type="insight",
                    source=f"agent_{agent_name}",
                    tags=[mem.get("category", "insight"), "agent"]
                )
                created.append(insight_atom)
                self.link_atoms(task_atom.id, insight_atom.id)

        print(f"Stored {len(created)} atoms from agent {agent_name}")
        return created

    # === REPORTS ===

    def get_status(self) -> dict:
        """Get Cyclotron status."""
        return {
            "total_atoms": self.index["stats"]["total"],
            "types": self.index["stats"]["by_type"],
            "sources": self.index["stats"]["by_source"],
            "tag_count": len(self.index["tags"]),
            "top_tags": sorted(
                [(tag, len(ids)) for tag, ids in self.index["tags"].items()],
                key=lambda x: x[1],
                reverse=True
            )[:10],
            "last_updated": self.index["updated"]
        }


def demo():
    """Demonstrate Cyclotron-Brain Bridge."""
    print("=" * 60)
    print("CYCLOTRON-BRAIN BRIDGE DEMO")
    print("=" * 60)

    bridge = CyclotronBridge()

    # Create some atoms
    print("\n1. Creating knowledge atoms...")

    atoms = [
        ("Trinity system uses three AI instances (C1, C2, C3) for parallel processing", "concept", ["trinity", "architecture"]),
        ("GraphRAG improves RAG accuracy by 35% through knowledge graph integration", "fact", ["graphrag", "accuracy"]),
        ("Pattern Theory identifies manipulation through 7 domains", "concept", ["pattern-theory", "manipulation"]),
        ("EOS Traction provides quarterly rocks and weekly scorecards", "fact", ["eos", "traction", "methodology"]),
        ("Decision: Use Kùzu for embedded graph database", "decision", ["database", "architecture"]),
        ("Insight: All modern knowledge systems converge toward graph structures", "insight", ["knowledge", "future"])
    ]

    created_atoms = []
    for content, atom_type, tags in atoms:
        atom = bridge.create_atom(content, atom_type, "demo", tags)
        created_atoms.append(atom)

    # Link related atoms
    print("\n2. Linking related atoms...")
    bridge.link_atoms(created_atoms[0].id, created_atoms[1].id)  # Trinity -> GraphRAG
    bridge.link_atoms(created_atoms[2].id, created_atoms[3].id)  # Pattern -> EOS

    # Search
    print("\n3. Searching...")
    results = bridge.search("graph knowledge")
    print(f"Search 'graph knowledge': {len(results)} results")
    for atom in results:
        print(f"  - [{atom.atom_type}] {atom.content[:60]}...")

    # Search by tag
    print("\n4. Search by tag 'architecture'...")
    tag_results = bridge.search_by_tag("architecture")
    for atom in tag_results:
        print(f"  - {atom.content[:60]}...")

    # Ingest from brain
    print("\n5. Ingesting from brain...")
    bridge.ingest_from_brain()

    # Export to brain
    print("\n6. Exporting to brain...")
    bridge.export_to_brain()

    # Status report
    print("\n" + "=" * 60)
    print("CYCLOTRON STATUS")
    print("=" * 60)

    status = bridge.get_status()
    print(f"Total atoms: {status['total_atoms']}")
    print(f"Types: {status['types']}")
    print(f"Sources: {status['sources']}")
    print(f"Tag count: {status['tag_count']}")
    print("Top tags:", status['top_tags'][:5])


if __name__ == "__main__":
    demo()
