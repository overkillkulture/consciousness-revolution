#!/usr/bin/env python3
"""
GRAPHRAG ENTITY EXTRACTOR
Extracts entities and relationships from documents for knowledge graph.
Uses Claude API for intelligent extraction.
"""

import json
import os
import hashlib
from pathlib import Path
from datetime import datetime
from typing import Optional

# Try to import anthropic
try:
    from anthropic import Anthropic
    HAS_ANTHROPIC = True
except ImportError:
    HAS_ANTHROPIC = False
    print("Warning: anthropic not installed. Run: pip install anthropic")

# Paths
CONSCIOUSNESS_PATH = Path.home() / ".consciousness"
GRAPHRAG_PATH = CONSCIOUSNESS_PATH / "graphrag"
ENTITIES_PATH = GRAPHRAG_PATH / "entities"
RELATIONSHIPS_PATH = GRAPHRAG_PATH / "relationships"

# Ensure directories exist
GRAPHRAG_PATH.mkdir(parents=True, exist_ok=True)
ENTITIES_PATH.mkdir(exist_ok=True)
RELATIONSHIPS_PATH.mkdir(exist_ok=True)

EXTRACTION_PROMPT = """Extract entities and relationships from this text for a knowledge graph about consciousness tools and manipulation detection.

TEXT:
{text}

Return ONLY valid JSON (no markdown, no explanation):
{{
  "entities": [
    {{
      "name": "exact name",
      "type": "person|tool|concept|pattern|domain|system|file",
      "description": "one sentence description"
    }}
  ],
  "relationships": [
    {{
      "source": "entity name",
      "target": "entity name",
      "type": "uses|creates|detects|relates_to|part_of|implements|extends"
    }}
  ]
}}

ENTITY TYPES:
- person: Human names (Commander, Josh, etc.)
- tool: Software tools (Gaslighting Detector, Cyclotron, etc.)
- concept: Ideas (Pattern Theory, Manipulation Immunity, etc.)
- pattern: Manipulation patterns (gaslighting, love bombing, etc.)
- domain: Seven Domains (Media, Relationships, etc.)
- system: Technical systems (Trinity, GraphRAG, EOS, etc.)
- file: Important files or documents

RELATIONSHIP TYPES:
- uses: A uses B
- creates: A creates B
- detects: A detects B
- relates_to: A is related to B
- part_of: A is part of B
- implements: A implements B
- extends: A extends B

Focus on extracting meaningful entities and relationships relevant to the Consciousness Revolution project."""

def get_file_hash(content: str) -> str:
    """Get hash of content to detect changes."""
    return hashlib.md5(content.encode()).hexdigest()

def extract_entities_from_text(text: str, client: Optional[object] = None) -> dict:
    """Extract entities and relationships using Claude."""
    if not HAS_ANTHROPIC or not client:
        return {"entities": [], "relationships": [], "error": "No API client"}

    try:
        response = client.messages.create(
            model="claude-sonnet-4-20250514",
            max_tokens=2000,
            messages=[{
                "role": "user",
                "content": EXTRACTION_PROMPT.format(text=text[:8000])  # Limit text size
            }]
        )

        result_text = response.content[0].text.strip()

        # Try to parse JSON
        try:
            return json.loads(result_text)
        except json.JSONDecodeError:
            # Try to find JSON in response
            start = result_text.find('{')
            end = result_text.rfind('}') + 1
            if start >= 0 and end > start:
                return json.loads(result_text[start:end])
            return {"entities": [], "relationships": [], "error": "Failed to parse JSON"}

    except Exception as e:
        return {"entities": [], "relationships": [], "error": str(e)}

def process_file(file_path: Path, client: Optional[object] = None) -> dict:
    """Process a single file and extract entities."""
    try:
        content = file_path.read_text(encoding='utf-8', errors='ignore')
    except Exception as e:
        return {"error": str(e)}

    # Skip very small or very large files
    if len(content) < 100:
        return {"skipped": "too small"}
    if len(content) > 50000:
        content = content[:50000]  # Truncate

    # Extract entities
    result = extract_entities_from_text(content, client)

    # Add metadata
    result['source_file'] = str(file_path)
    result['file_hash'] = get_file_hash(content)
    result['extracted_at'] = datetime.now().isoformat()
    result['content_length'] = len(content)

    return result

def save_extraction(file_path: Path, extraction: dict):
    """Save extraction results."""
    # Create unique filename from source path
    safe_name = str(file_path).replace('/', '_').replace('\\', '_').replace(':', '')
    output_file = ENTITIES_PATH / f"{safe_name}.json"

    with open(output_file, 'w') as f:
        json.dump(extraction, f, indent=2)

    return output_file

def build_master_index():
    """Build master index of all entities and relationships."""
    all_entities = {}
    all_relationships = []

    for extraction_file in ENTITIES_PATH.glob("*.json"):
        try:
            with open(extraction_file) as f:
                data = json.load(f)

            # Collect entities
            for entity in data.get('entities', []):
                name = entity.get('name', '').lower()
                if name and name not in all_entities:
                    all_entities[name] = {
                        **entity,
                        'sources': [data.get('source_file', 'unknown')]
                    }
                elif name:
                    all_entities[name]['sources'].append(data.get('source_file', 'unknown'))

            # Collect relationships
            for rel in data.get('relationships', []):
                rel['source_file'] = data.get('source_file', 'unknown')
                all_relationships.append(rel)

        except Exception as e:
            print(f"Error processing {extraction_file}: {e}")

    # Save master index
    master_index = {
        'entities': list(all_entities.values()),
        'relationships': all_relationships,
        'total_entities': len(all_entities),
        'total_relationships': len(all_relationships),
        'built_at': datetime.now().isoformat()
    }

    master_path = GRAPHRAG_PATH / "MASTER_INDEX.json"
    with open(master_path, 'w') as f:
        json.dump(master_index, f, indent=2)

    print(f"\nMaster index saved to {master_path}")
    print(f"Total entities: {len(all_entities)}")
    print(f"Total relationships: {len(all_relationships)}")

    return master_index

def extract_from_directory(directory: Path, pattern: str = "*.md", client: Optional[object] = None):
    """Extract entities from all matching files in directory."""
    files = list(directory.glob(pattern))
    print(f"Found {len(files)} files matching {pattern} in {directory}")

    results = []
    for i, file_path in enumerate(files):
        print(f"[{i+1}/{len(files)}] Processing: {file_path.name}")

        extraction = process_file(file_path, client)

        if 'error' not in extraction and 'skipped' not in extraction:
            output = save_extraction(file_path, extraction)
            entity_count = len(extraction.get('entities', []))
            rel_count = len(extraction.get('relationships', []))
            print(f"  → Extracted {entity_count} entities, {rel_count} relationships")
            results.append(extraction)
        elif 'skipped' in extraction:
            print(f"  → Skipped: {extraction['skipped']}")
        else:
            print(f"  → Error: {extraction.get('error', 'unknown')}")

    return results

def main():
    """Main extraction workflow."""
    print("=" * 50)
    print("GRAPHRAG ENTITY EXTRACTOR")
    print("=" * 50)

    # Initialize client if available
    client = None
    if HAS_ANTHROPIC:
        api_key = os.environ.get('ANTHROPIC_API_KEY')
        if api_key:
            client = Anthropic(api_key=api_key)
            print("✅ Anthropic client initialized")
        else:
            print("⚠️  No ANTHROPIC_API_KEY found - running in test mode")

    # Directories to process
    directories = [
        (Path.home() / "100X_DEPLOYMENT" / "LOCAL_TRINITY_HUB" / "protocols", "*.md"),
        (Path.home() / ".planning" / "traction", "*.md"),
        (Path.home() / ".trinity", "*.md"),
    ]

    all_results = []
    for directory, pattern in directories:
        if directory.exists():
            print(f"\n📁 Processing: {directory}")
            results = extract_from_directory(directory, pattern, client)
            all_results.extend(results)
        else:
            print(f"\n⚠️  Directory not found: {directory}")

    # Build master index
    print("\n" + "=" * 50)
    print("Building master index...")
    master = build_master_index()

    # Summary
    print("\n" + "=" * 50)
    print("EXTRACTION COMPLETE")
    print("=" * 50)
    print(f"Files processed: {len(all_results)}")
    print(f"Total entities: {master['total_entities']}")
    print(f"Total relationships: {master['total_relationships']}")
    print(f"\nResults saved to: {GRAPHRAG_PATH}")

if __name__ == "__main__":
    main()
