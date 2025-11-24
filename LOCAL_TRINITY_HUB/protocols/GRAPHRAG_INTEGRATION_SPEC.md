# GRAPHRAG INTEGRATION SPECIFICATION

## Overview

This specification defines how to integrate GraphRAG (Graph Retrieval Augmented Generation) into the Consciousness Revolution platform for 35%+ accuracy improvement over vector-only RAG.

---

## Architecture

```
┌─────────────────────────────────────────────────────┐
│                    QUERY LAYER                       │
│  User Query → Query Router → Response Generator      │
└─────────────────┬───────────────────────────────────┘
                  │
    ┌─────────────┼─────────────┐
    │             │             │
┌───▼───┐   ┌─────▼─────┐   ┌───▼───┐
│GLOBAL │   │  LOCAL    │   │ BASIC │
│SEARCH │   │  SEARCH   │   │SEARCH │
└───┬───┘   └─────┬─────┘   └───┬───┘
    │             │             │
    └─────────────┼─────────────┘
                  │
┌─────────────────▼───────────────────────────────────┐
│              KNOWLEDGE GRAPH LAYER                   │
│  Entities → Relationships → Communities → Summaries  │
└─────────────────┬───────────────────────────────────┘
                  │
┌─────────────────▼───────────────────────────────────┐
│               CYCLOTRON INDEX                        │
│  File atoms → Content extraction → Metadata          │
└─────────────────────────────────────────────────────┘
```

---

## Component Specifications

### 1. Graph Database Selection

**Recommended: Kùzu**
- Embeddable (no server needed)
- "DuckDB for graphs" - fast analytical queries
- Built-in vector similarity search
- Full-text search included
- Python-native integration

**Alternative: Neo4j**
- Industry standard
- Better visualization tools
- Larger community
- Higher resource requirements

**Installation:**
```bash
pip install kuzu
# or
pip install neo4j
```

### 2. Knowledge Graph Schema

```cypher
// NODE TYPES
(:Document {
  id: STRING,
  path: STRING,
  type: STRING,      // md, html, py, json
  created: DATETIME,
  modified: DATETIME,
  content_hash: STRING
})

(:Entity {
  id: STRING,
  name: STRING,
  type: STRING,      // person, tool, concept, pattern, domain
  description: STRING,
  embedding: FLOAT[]
})

(:Community {
  id: STRING,
  level: INT,        // hierarchy level
  summary: STRING,
  entity_count: INT
})

(:Chunk {
  id: STRING,
  content: STRING,
  embedding: FLOAT[],
  token_count: INT
})

// RELATIONSHIP TYPES
(:Document)-[:CONTAINS]->(:Chunk)
(:Chunk)-[:MENTIONS]->(:Entity)
(:Entity)-[:RELATES_TO {type: STRING}]->(:Entity)
(:Entity)-[:BELONGS_TO]->(:Community)
(:Community)-[:PARENT_OF]->(:Community)

// TEMPORAL RELATIONSHIPS
(:Entity)-[:EXISTED_AT {start: DATETIME, end: DATETIME}]->(:TimePoint)
(:Entity)-[:CHANGED_TO {date: DATETIME}]->(:Entity)
```

### 3. Entity Extraction Pipeline

```python
# GRAPHRAG_ENTITY_EXTRACTOR.py

from anthropic import Anthropic
import json

EXTRACTION_PROMPT = """
Extract entities and relationships from this text.

TEXT:
{text}

Return JSON:
{
  "entities": [
    {"name": "...", "type": "person|tool|concept|pattern|domain", "description": "..."}
  ],
  "relationships": [
    {"source": "...", "target": "...", "type": "uses|creates|detects|relates_to|part_of"}
  ]
}

Focus on:
- Consciousness tools and their purposes
- Pattern types and detection methods
- People and their roles
- Concepts from Pattern Theory
- Seven Domains relationships
"""

def extract_entities(text: str, client: Anthropic) -> dict:
    response = client.messages.create(
        model="claude-sonnet-4-20250514",
        max_tokens=2000,
        messages=[{
            "role": "user",
            "content": EXTRACTION_PROMPT.format(text=text)
        }]
    )
    return json.loads(response.content[0].text)
```

### 4. Community Detection

```python
# GRAPHRAG_COMMUNITY_BUILDER.py

def build_communities(graph):
    """
    Use Leiden algorithm for community detection.
    Build hierarchy: Level 0 (most granular) → Level N (most abstract)
    """

    # Level 0: Individual entities
    # Level 1: Small clusters (3-10 entities)
    # Level 2: Medium clusters (10-50 entities)
    # Level 3: Large clusters (50+ entities)

    from graspologic.partition import hierarchical_leiden

    communities = hierarchical_leiden(
        graph.adjacency_matrix(),
        max_cluster_size=50,
        resolution=1.0
    )

    return communities

def generate_community_summaries(communities, graph, client):
    """
    Generate natural language summaries for each community.
    These power Global Search.
    """
    summaries = {}

    for community_id, members in communities.items():
        # Get all entities in community
        entities = [graph.get_entity(m) for m in members]

        # Generate summary
        prompt = f"""
        Summarize this group of related entities:

        {json.dumps(entities, indent=2)}

        Describe:
        1. What these entities have in common
        2. Their collective purpose/function
        3. Key relationships between them
        """

        summary = client.messages.create(...)
        summaries[community_id] = summary

    return summaries
```

### 5. Query Routing

```python
# GRAPHRAG_QUERY_ROUTER.py

def route_query(query: str, client: Anthropic) -> str:
    """
    Determine which search mode to use:
    - GLOBAL: Holistic questions about themes, summaries
    - LOCAL: Specific entity questions, relationships
    - BASIC: Simple keyword/similarity search
    """

    routing_prompt = f"""
    Classify this query:

    "{query}"

    GLOBAL - Holistic questions (What are the main themes? How does X relate to everything?)
    LOCAL - Specific questions (What is X? How does X connect to Y?)
    BASIC - Simple lookup (Find files about X, Search for keyword)

    Return only: GLOBAL, LOCAL, or BASIC
    """

    response = client.messages.create(...)
    return response.content[0].text.strip()
```

### 6. Search Implementations

```python
# GRAPHRAG_SEARCH.py

def global_search(query: str, graph, client) -> str:
    """
    Use community summaries to answer holistic questions.
    Good for: "What are the main manipulation patterns?"
    """

    # Get all community summaries
    summaries = graph.get_all_community_summaries()

    # Map-reduce over summaries
    intermediate_answers = []
    for summary in summaries:
        answer = client.messages.create(
            messages=[{
                "role": "user",
                "content": f"Based on this context:\n{summary}\n\nAnswer: {query}"
            }]
        )
        intermediate_answers.append(answer)

    # Reduce to final answer
    final = client.messages.create(
        messages=[{
            "role": "user",
            "content": f"Synthesize these answers:\n{intermediate_answers}\n\nFinal answer to: {query}"
        }]
    )

    return final

def local_search(query: str, graph, client) -> str:
    """
    Start from specific entities and fan out to neighbors.
    Good for: "How does the Gaslighting Detector work?"
    """

    # Extract entities from query
    query_entities = extract_entities(query, client)

    # Find matching entities in graph
    matched = graph.find_entities(query_entities)

    # Get N-hop neighborhood
    context = []
    for entity in matched:
        neighbors = graph.get_neighbors(entity, hops=2)
        chunks = graph.get_related_chunks(entity)
        context.extend(neighbors + chunks)

    # Generate answer from context
    answer = client.messages.create(
        messages=[{
            "role": "user",
            "content": f"Context:\n{context}\n\nAnswer: {query}"
        }]
    )

    return answer

def basic_search(query: str, graph) -> str:
    """
    Vector similarity search on chunks.
    Good for: Simple keyword lookups
    """

    query_embedding = get_embedding(query)
    results = graph.vector_search(query_embedding, top_k=10)
    return results
```

---

## Integration with Existing Systems

### Cyclotron Integration

```python
# Cyclotron already indexes all files
# GraphRAG adds relationship layer on top

def cyclotron_to_graphrag(cyclotron_index: dict, graph):
    """
    Transform Cyclotron atoms into knowledge graph.
    """

    for atom in cyclotron_index['atoms']:
        # Create Document node
        doc = graph.create_node('Document', {
            'path': atom['path'],
            'type': atom['type'],
            'modified': atom['modified']
        })

        # Extract and create entities
        entities = extract_entities(atom['content'])
        for entity in entities:
            node = graph.create_node('Entity', entity)

        # Create relationships
        for rel in entities['relationships']:
            graph.create_relationship(rel['source'], rel['target'], rel['type'])
```

### Trinity Integration

```python
# Trinity agents use GraphRAG for queries

class TrinityAgent:
    def __init__(self, graph):
        self.graph = graph

    def query(self, question: str) -> str:
        # Route to appropriate search
        mode = route_query(question)

        if mode == 'GLOBAL':
            return global_search(question, self.graph)
        elif mode == 'LOCAL':
            return local_search(question, self.graph)
        else:
            return basic_search(question, self.graph)
```

### Temporal Data Integration

```python
# Add time dimension to all entities

def add_temporal_context(entity, graph):
    """
    Track when entities existed/changed.
    Enables: "What tools existed in October 2025?"
    """

    graph.create_relationship(
        entity,
        f"TimePoint_{datetime.now().isoformat()}",
        'EXISTED_AT',
        {'recorded': datetime.now()}
    )
```

---

## Implementation Roadmap

### Week 1: Foundation
- [ ] Install Kùzu
- [ ] Define schema
- [ ] Create basic CRUD operations
- [ ] Test with sample data

### Week 2: Entity Extraction
- [ ] Build extraction pipeline
- [ ] Process existing Cyclotron index
- [ ] Validate entity quality
- [ ] Tune extraction prompts

### Week 3: Community Building
- [ ] Implement Leiden algorithm
- [ ] Generate community summaries
- [ ] Build hierarchy visualization
- [ ] Test summary quality

### Week 4: Search Implementation
- [ ] Implement query router
- [ ] Build Global Search
- [ ] Build Local Search
- [ ] Integrate with Trinity

### Week 5: Production
- [ ] Performance optimization
- [ ] Incremental updates
- [ ] Monitoring/logging
- [ ] Documentation

---

## Performance Targets

| Metric | Target | Measurement |
|--------|--------|-------------|
| Query accuracy | 80%+ | vs baseline RAG |
| Query latency | <3s | p95 |
| Index freshness | <1hr | time to new content |
| Entity precision | 90%+ | manual validation |
| Community coherence | 85%+ | human rating |

---

## File Locations

```
C:/Users/dwrek/
├── .consciousness/
│   └── graphrag/
│       ├── kuzu_db/           # Graph database files
│       ├── embeddings/         # Cached embeddings
│       └── communities/        # Community summaries
│
├── 100X_DEPLOYMENT/
│   ├── GRAPHRAG_ENTITY_EXTRACTOR.py
│   ├── GRAPHRAG_COMMUNITY_BUILDER.py
│   ├── GRAPHRAG_QUERY_ROUTER.py
│   ├── GRAPHRAG_SEARCH.py
│   └── GRAPHRAG_TRINITY_INTEGRATION.py
```

---

## Dependencies

```
# requirements-graphrag.txt
kuzu>=0.3.0
anthropic>=0.18.0
numpy>=1.24.0
graspologic>=3.0.0
sentence-transformers>=2.2.0
```

---

## Expected Outcomes

1. **35% accuracy improvement** over current RAG
2. **Holistic query support** (themes, patterns across all docs)
3. **Relationship awareness** (how things connect)
4. **Temporal queries** (what existed when)
5. **Reduced hallucination** (grounded in graph structure)

---

## Connected Documents

- `CUTTING_EDGE_TECHNIQUES_SYNTHESIS.md` - Research foundation
- `DATA_ORGANIZATION_ARCHITECTURE.md` - Storage layer
- `CYCLOTRON_AUDIT_SUMMARY.md` - Existing index

---

*Specification Version: 1.0*
*Author: C2 Architect*
*Date: 2025-11-23*
*Status: READY FOR IMPLEMENTATION*
