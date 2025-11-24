#!/usr/bin/env python3
"""
KNOWLEDGE CAPTURE PIPELINE
Automatically captures, indexes, and links knowledge from various sources.
Feeds into GraphRAG and Spreadsheet Brain systems.
"""

import json
import hashlib
import re
from pathlib import Path
from datetime import datetime
from typing import Optional

# Paths
HOME = Path.home()
CONSCIOUSNESS_PATH = HOME / ".consciousness"
KNOWLEDGE_PATH = CONSCIOUSNESS_PATH / "brain"
MEMORY_PATH = CONSCIOUSNESS_PATH / "memory"

# Ensure directories
KNOWLEDGE_PATH.mkdir(parents=True, exist_ok=True)
MEMORY_PATH.mkdir(parents=True, exist_ok=True)

class KnowledgeAtom:
    """Atomic unit of knowledge - inspired by Zettelkasten."""

    def __init__(self, content: str, source: str, atom_type: str = "note"):
        self.id = self._generate_id(content)
        self.content = content
        self.source = source
        self.atom_type = atom_type  # note, insight, decision, pattern, action
        self.created = datetime.now().isoformat()
        self.links = []  # IDs of related atoms
        self.tags = []
        self.metadata = {}

    def _generate_id(self, content: str) -> str:
        """Generate unique ID from content hash + timestamp."""
        timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
        content_hash = hashlib.md5(content.encode()).hexdigest()[:8]
        return f"{timestamp}_{content_hash}"

    def add_link(self, atom_id: str):
        """Link to another knowledge atom."""
        if atom_id not in self.links:
            self.links.append(atom_id)

    def add_tag(self, tag: str):
        """Add a tag."""
        tag = tag.lower().strip()
        if tag and tag not in self.tags:
            self.tags.append(tag)

    def to_dict(self) -> dict:
        """Convert to dictionary."""
        return {
            "id": self.id,
            "content": self.content,
            "source": self.source,
            "type": self.atom_type,
            "created": self.created,
            "links": self.links,
            "tags": self.tags,
            "metadata": self.metadata
        }

    def save(self):
        """Save atom to disk."""
        file_path = KNOWLEDGE_PATH / f"{self.id}.json"
        with open(file_path, 'w') as f:
            json.dump(self.to_dict(), f, indent=2)
        return file_path

class KnowledgeCapture:
    """Main capture pipeline."""

    def __init__(self):
        self.index_path = KNOWLEDGE_PATH / "INDEX.json"
        self.index = self._load_index()

    def _load_index(self) -> dict:
        """Load or create knowledge index."""
        if self.index_path.exists():
            with open(self.index_path) as f:
                return json.load(f)
        return {
            "atoms": {},
            "tags": {},
            "sources": {},
            "links": [],
            "stats": {
                "total": 0,
                "by_type": {}
            }
        }

    def _save_index(self):
        """Save index to disk."""
        with open(self.index_path, 'w') as f:
            json.dump(self.index, f, indent=2)

    def capture(self, content: str, source: str, atom_type: str = "note",
                tags: list = None, metadata: dict = None) -> KnowledgeAtom:
        """Capture new knowledge atom."""

        # Create atom
        atom = KnowledgeAtom(content, source, atom_type)

        # Add tags
        if tags:
            for tag in tags:
                atom.add_tag(tag)

        # Auto-extract tags from content
        extracted_tags = self._extract_tags(content)
        for tag in extracted_tags:
            atom.add_tag(tag)

        # Add metadata
        if metadata:
            atom.metadata = metadata

        # Find and add links
        related = self._find_related(content)
        for related_id in related:
            atom.add_link(related_id)

        # Save atom
        atom.save()

        # Update index
        self._update_index(atom)

        return atom

    def _extract_tags(self, content: str) -> list:
        """Extract tags from content using patterns."""
        tags = []

        # Pattern keywords
        patterns = {
            "pattern": ["gaslighting", "manipulation", "love bombing", "triangulation"],
            "domain": ["media", "relationships", "finance", "authority", "self", "groups", "digital"],
            "system": ["trinity", "cyclotron", "graphrag", "eos", "traction"],
            "action": ["todo", "fix", "build", "deploy", "test"]
        }

        content_lower = content.lower()

        for category, keywords in patterns.items():
            for keyword in keywords:
                if keyword in content_lower:
                    tags.append(keyword)
                    tags.append(category)

        return list(set(tags))

    def _find_related(self, content: str, threshold: float = 0.3) -> list:
        """Find related atoms based on content similarity."""
        related = []

        # Simple keyword matching (could be enhanced with embeddings)
        content_words = set(re.findall(r'\w+', content.lower()))

        for atom_id, atom_data in self.index['atoms'].items():
            if 'keywords' in atom_data:
                atom_words = set(atom_data['keywords'])
                overlap = len(content_words & atom_words) / max(len(content_words), 1)
                if overlap >= threshold:
                    related.append(atom_id)

        return related[:5]  # Limit to 5 most related

    def _update_index(self, atom: KnowledgeAtom):
        """Update index with new atom."""

        # Add to atoms
        content_words = list(set(re.findall(r'\w+', atom.content.lower())))
        self.index['atoms'][atom.id] = {
            "type": atom.atom_type,
            "created": atom.created,
            "tags": atom.tags,
            "keywords": content_words[:20],  # Top 20 keywords
            "links": atom.links
        }

        # Update tag index
        for tag in atom.tags:
            if tag not in self.index['tags']:
                self.index['tags'][tag] = []
            self.index['tags'][tag].append(atom.id)

        # Update source index
        if atom.source not in self.index['sources']:
            self.index['sources'][atom.source] = []
        self.index['sources'][atom.source].append(atom.id)

        # Update stats
        self.index['stats']['total'] += 1
        if atom.atom_type not in self.index['stats']['by_type']:
            self.index['stats']['by_type'][atom.atom_type] = 0
        self.index['stats']['by_type'][atom.atom_type] += 1

        # Save index
        self._save_index()

    def capture_session(self, session_log: str, session_id: str = None):
        """Capture knowledge from a session transcript."""
        if not session_id:
            session_id = datetime.now().strftime("%Y%m%d_%H%M%S")

        captured = []

        # Split into meaningful chunks
        chunks = self._chunk_session(session_log)

        for i, chunk in enumerate(chunks):
            # Classify chunk type
            chunk_type = self._classify_chunk(chunk)

            # Capture as atom
            atom = self.capture(
                content=chunk,
                source=f"session_{session_id}",
                atom_type=chunk_type,
                metadata={"chunk_index": i, "session_id": session_id}
            )
            captured.append(atom)

        return captured

    def _chunk_session(self, text: str) -> list:
        """Break session into meaningful chunks."""
        chunks = []

        # Split by markdown headers or double newlines
        parts = re.split(r'\n#{1,3}\s+|\n\n', text)

        for part in parts:
            part = part.strip()
            if len(part) > 50:  # Minimum chunk size
                chunks.append(part)

        return chunks

    def _classify_chunk(self, chunk: str) -> str:
        """Classify chunk type based on content."""
        chunk_lower = chunk.lower()

        if any(word in chunk_lower for word in ['todo', 'task', 'action', 'build', 'create']):
            return "action"
        elif any(word in chunk_lower for word in ['decision', 'decided', 'chose', 'selected']):
            return "decision"
        elif any(word in chunk_lower for word in ['pattern', 'noticed', 'observed', 'insight']):
            return "insight"
        elif any(word in chunk_lower for word in ['learned', 'realized', 'discovered']):
            return "pattern"
        else:
            return "note"

    def search(self, query: str) -> list:
        """Search knowledge base."""
        results = []
        query_words = set(re.findall(r'\w+', query.lower()))

        for atom_id, atom_data in self.index['atoms'].items():
            # Check keywords
            if 'keywords' in atom_data:
                atom_words = set(atom_data['keywords'])
                overlap = len(query_words & atom_words)
                if overlap > 0:
                    results.append((atom_id, overlap))

            # Check tags
            for tag in atom_data.get('tags', []):
                if tag in query.lower():
                    results.append((atom_id, 5))  # Boost tag matches

        # Sort by relevance
        results = sorted(results, key=lambda x: x[1], reverse=True)

        # Load and return top results
        output = []
        seen = set()
        for atom_id, score in results[:10]:
            if atom_id not in seen:
                atom_path = KNOWLEDGE_PATH / f"{atom_id}.json"
                if atom_path.exists():
                    with open(atom_path) as f:
                        output.append(json.load(f))
                    seen.add(atom_id)

        return output

    def get_stats(self) -> dict:
        """Get knowledge base statistics."""
        return {
            "total_atoms": self.index['stats']['total'],
            "by_type": self.index['stats']['by_type'],
            "total_tags": len(self.index['tags']),
            "total_sources": len(self.index['sources']),
            "top_tags": sorted(
                [(tag, len(atoms)) for tag, atoms in self.index['tags'].items()],
                key=lambda x: x[1],
                reverse=True
            )[:10]
        }

def main():
    """Demo and test the knowledge capture pipeline."""
    print("=" * 50)
    print("KNOWLEDGE CAPTURE PIPELINE")
    print("=" * 50)

    capture = KnowledgeCapture()

    # Example captures
    examples = [
        {
            "content": "The GraphRAG system improves query accuracy by 35% over traditional RAG by using knowledge graphs to represent relationships between entities.",
            "source": "architecture_research",
            "atom_type": "insight",
            "tags": ["graphrag", "architecture"]
        },
        {
            "content": "TODO: Implement Kùzu graph database for local knowledge graph storage. This will enable fast analytical queries without a server.",
            "source": "implementation_notes",
            "atom_type": "action",
            "tags": ["graphrag", "implementation"]
        },
        {
            "content": "Decision: Use LangGraph patterns for Trinity refactor instead of simple message passing. This enables stateful workflows and 2.2x performance improvement.",
            "source": "architecture_decisions",
            "atom_type": "decision",
            "tags": ["trinity", "langgraph"]
        }
    ]

    print("\nCapturing example knowledge atoms...\n")

    for example in examples:
        atom = capture.capture(**example)
        print(f"Captured: {atom.id}")
        print(f"  Type: {atom.atom_type}")
        print(f"  Tags: {atom.tags}")
        print(f"  Links: {len(atom.links)}")
        print()

    # Show stats
    stats = capture.get_stats()
    print("\n" + "=" * 50)
    print("KNOWLEDGE BASE STATS")
    print("=" * 50)
    print(f"Total atoms: {stats['total_atoms']}")
    print(f"By type: {stats['by_type']}")
    print(f"Total tags: {stats['total_tags']}")
    print(f"Top tags: {stats['top_tags'][:5]}")

    # Test search
    print("\n" + "=" * 50)
    print("SEARCH TEST: 'graphrag'")
    print("=" * 50)
    results = capture.search("graphrag")
    for result in results:
        print(f"\n[{result['type']}] {result['id']}")
        print(f"  {result['content'][:100]}...")

if __name__ == "__main__":
    main()
