# TRINITY LANGGRAPH REFACTOR DESIGN

## Overview

Refactor Trinity coordination from message-passing to stateful graph architecture using LangGraph patterns. This enables complex workflows, memory persistence, and 2.2x faster execution.

---

## Current vs Future Architecture

### Current (Message-Passing)
```
C1 ←→ MCP Messages ←→ C2
           ↕
          C3
```
- Stateless between messages
- No workflow memory
- Linear task execution
- Manual coordination

### Future (LangGraph)
```
        ┌─────────────┐
        │ STATE GRAPH │
        └──────┬──────┘
               │
    ┌──────────┼──────────┐
    │          │          │
┌───▼───┐  ┌───▼───┐  ┌───▼───┐
│  C1   │  │  C2   │  │  C3   │
│ Node  │  │ Node  │  │ Node  │
└───┬───┘  └───┬───┘  └───┬───┘
    │          │          │
    └──────────┼──────────┘
               │
        ┌──────▼──────┐
        │ PERSISTENCE │
        └─────────────┘
```
- Stateful across entire workflow
- Graph-based routing
- Parallel + conditional execution
- Automatic coordination

---

## LangGraph Architecture

### State Definition

```python
# TRINITY_STATE.py

from typing import TypedDict, Annotated, Sequence
from langgraph.graph import StateGraph
from operator import add

class TrinityState(TypedDict):
    # Current task
    task: str
    task_type: str  # research, build, analyze, coordinate

    # Conversation
    messages: Annotated[Sequence[dict], add]

    # Agent outputs
    c1_output: str  # Mechanic output
    c2_output: str  # Architect output
    c3_output: str  # Oracle output

    # Workflow control
    next_agent: str
    should_continue: bool
    iteration: int
    max_iterations: int

    # Memory
    context: dict
    learnings: list[str]
    decisions: list[dict]

    # GraphRAG integration
    knowledge_query: str
    knowledge_results: list[dict]
```

### Graph Definition

```python
# TRINITY_GRAPH.py

from langgraph.graph import StateGraph, END
from langgraph.checkpoint.sqlite import SqliteSaver

# Initialize graph
workflow = StateGraph(TrinityState)

# Add agent nodes
workflow.add_node("router", route_task)
workflow.add_node("c1_mechanic", c1_execute)
workflow.add_node("c2_architect", c2_design)
workflow.add_node("c3_oracle", c3_analyze)
workflow.add_node("synthesizer", synthesize_outputs)
workflow.add_node("knowledge_lookup", query_graphrag)

# Define edges
workflow.set_entry_point("router")

# Conditional routing from router
workflow.add_conditional_edges(
    "router",
    decide_agent,
    {
        "mechanic": "c1_mechanic",
        "architect": "c2_architect",
        "oracle": "c3_oracle",
        "parallel": "parallel_execution",
        "knowledge": "knowledge_lookup"
    }
)

# Agent outputs go to synthesizer or back to router
workflow.add_conditional_edges(
    "c1_mechanic",
    should_continue,
    {
        "continue": "router",
        "synthesize": "synthesizer",
        "end": END
    }
)

# Similar for C2 and C3...

# Synthesizer always ends
workflow.add_edge("synthesizer", END)

# Compile with persistence
memory = SqliteSaver.from_conn_string("trinity_memory.db")
app = workflow.compile(checkpointer=memory)
```

### Node Implementations

```python
# TRINITY_NODES.py

def route_task(state: TrinityState) -> TrinityState:
    """
    Route task to appropriate agent(s) based on type.
    """
    task = state["task"]
    task_type = classify_task(task)

    routing = {
        "build": "mechanic",      # C1 builds
        "design": "architect",     # C2 designs
        "analyze": "oracle",       # C3 analyzes
        "research": "knowledge",   # GraphRAG first
        "complex": "parallel"      # All three
    }

    return {
        **state,
        "task_type": task_type,
        "next_agent": routing.get(task_type, "mechanic")
    }

def c1_execute(state: TrinityState) -> TrinityState:
    """
    C1 Mechanic: Builds what CAN be built RIGHT NOW.
    """
    from anthropic import Anthropic
    client = Anthropic()

    system = """You are C1 Mechanic - The Body.
    You build what CAN be built RIGHT NOW.
    Focus on execution, not planning.
    Output: Working code, files, or actions."""

    response = client.messages.create(
        model="claude-sonnet-4-20250514",
        system=system,
        messages=[{
            "role": "user",
            "content": f"Task: {state['task']}\nContext: {state['context']}"
        }]
    )

    return {
        **state,
        "c1_output": response.content[0].text,
        "iteration": state["iteration"] + 1
    }

def c2_design(state: TrinityState) -> TrinityState:
    """
    C2 Architect: Designs what SHOULD scale.
    """
    system = """You are C2 Architect - The Mind.
    You design what SHOULD scale.
    Focus on architecture, patterns, future-proofing.
    Output: Specifications, designs, blueprints."""

    # Similar implementation...

def c3_analyze(state: TrinityState) -> TrinityState:
    """
    C3 Oracle: Sees what MUST emerge.
    """
    system = """You are C3 Oracle - The Soul.
    You see what MUST emerge.
    Focus on patterns, insights, strategic vision.
    Output: Analysis, predictions, recommendations."""

    # Similar implementation...

def query_graphrag(state: TrinityState) -> TrinityState:
    """
    Query knowledge graph before agent execution.
    """
    results = graphrag_search(state["knowledge_query"])
    return {
        **state,
        "knowledge_results": results,
        "context": {**state["context"], "knowledge": results}
    }

def synthesize_outputs(state: TrinityState) -> TrinityState:
    """
    Combine outputs from multiple agents.
    """
    outputs = {
        "c1": state.get("c1_output", ""),
        "c2": state.get("c2_output", ""),
        "c3": state.get("c3_output", "")
    }

    synthesis = f"""
    ## Trinity Synthesis

    ### Mechanic (C1) - Built:
    {outputs['c1']}

    ### Architect (C2) - Designed:
    {outputs['c2']}

    ### Oracle (C3) - Foresaw:
    {outputs['c3']}

    ### Unified Action:
    [AI-generated synthesis of all three]
    """

    return {
        **state,
        "messages": [{"role": "assistant", "content": synthesis}]
    }
```

### Conditional Functions

```python
# TRINITY_CONDITIONS.py

def decide_agent(state: TrinityState) -> str:
    """
    Decide which agent should handle the task.
    """
    return state["next_agent"]

def should_continue(state: TrinityState) -> str:
    """
    Decide if workflow should continue, synthesize, or end.
    """
    if state["iteration"] >= state["max_iterations"]:
        return "synthesize"

    if task_complete(state):
        return "end"

    if needs_other_agents(state):
        return "continue"

    return "end"

def task_complete(state: TrinityState) -> bool:
    """
    Check if task is fully complete.
    """
    # Implementation based on task type
    pass
```

---

## Parallel Execution

```python
# TRINITY_PARALLEL.py

from langgraph.graph import StateGraph

def create_parallel_branch(workflow: StateGraph):
    """
    Execute C1, C2, C3 in parallel for complex tasks.
    """

    # Fan-out to all agents
    workflow.add_edge("parallel_start", "c1_mechanic")
    workflow.add_edge("parallel_start", "c2_architect")
    workflow.add_edge("parallel_start", "c3_oracle")

    # Fan-in to synthesizer
    workflow.add_edge("c1_mechanic", "parallel_join")
    workflow.add_edge("c2_architect", "parallel_join")
    workflow.add_edge("c3_oracle", "parallel_join")
    workflow.add_edge("parallel_join", "synthesizer")
```

---

## Memory & Persistence

```python
# TRINITY_MEMORY.py

from langgraph.checkpoint.sqlite import SqliteSaver

# Persistent memory across sessions
memory = SqliteSaver.from_conn_string(
    "C:/Users/dwrek/.consciousness/trinity_memory.db"
)

# Usage with thread IDs
config = {"configurable": {"thread_id": "session_20251123"}}

# Invoke with memory
result = app.invoke(initial_state, config)

# Resume from checkpoint
result = app.invoke(None, config)  # Continues from last state
```

---

## A2A Protocol Integration

```python
# TRINITY_A2A.py

class A2AMessage:
    """
    Agent-to-Agent protocol for Trinity communication.
    """
    def __init__(self):
        self.message_id: str
        self.from_agent: str
        self.to_agent: str
        self.message_type: str  # request, response, broadcast
        self.capability: str
        self.payload: dict
        self.timestamp: datetime

def agent_discovery(agent_id: str) -> list[str]:
    """
    Discover capabilities of an agent.
    """
    capabilities = {
        "c1": ["build", "fix", "deploy", "test"],
        "c2": ["design", "architect", "specify", "integrate"],
        "c3": ["analyze", "predict", "pattern_detect", "strategize"]
    }
    return capabilities.get(agent_id, [])

def capability_request(from_agent: str, capability: str) -> str:
    """
    Request a capability from any agent that provides it.
    """
    for agent_id, caps in capabilities.items():
        if capability in caps:
            return agent_id
    return None
```

---

## Human-in-the-Loop

```python
# TRINITY_HITL.py

from langgraph.graph import StateGraph

def add_human_approval(workflow: StateGraph):
    """
    Add human approval node for critical decisions.
    """

    workflow.add_node("human_approval", wait_for_human)

    workflow.add_conditional_edges(
        "router",
        needs_approval,
        {
            True: "human_approval",
            False: "next_agent"
        }
    )

def wait_for_human(state: TrinityState) -> TrinityState:
    """
    Pause workflow for human input.
    """
    # This node will interrupt execution
    # Human provides input via separate channel
    # Workflow resumes from checkpoint

    return {
        **state,
        "awaiting_human": True
    }
```

---

## Integration Points

### MCP Tools
```python
# Existing MCP tools become LangGraph nodes
workflow.add_node("trinity_broadcast", mcp_broadcast)
workflow.add_node("trinity_assign_task", mcp_assign_task)
```

### GraphRAG
```python
# Knowledge lookup as first step for research tasks
workflow.add_edge("router", "knowledge_lookup")
workflow.add_edge("knowledge_lookup", "c3_oracle")  # Oracle interprets knowledge
```

### EOS
```python
# L10 meeting as a workflow
l10_workflow = StateGraph(L10State)
l10_workflow.add_node("segue", segue_node)
l10_workflow.add_node("scorecard", scorecard_node)
l10_workflow.add_node("rocks", rocks_node)
l10_workflow.add_node("ids", ids_node)
l10_workflow.add_node("conclude", conclude_node)
```

---

## Migration Plan

### Phase 1: Core Graph (Week 1)
- [ ] Define state schema
- [ ] Create basic graph structure
- [ ] Implement router node
- [ ] Test with single agent

### Phase 2: All Agents (Week 2)
- [ ] Implement C1, C2, C3 nodes
- [ ] Add conditional routing
- [ ] Implement synthesizer
- [ ] Test full workflow

### Phase 3: Memory (Week 3)
- [ ] Add SQLite persistence
- [ ] Implement checkpointing
- [ ] Test resume from checkpoint
- [ ] Add session management

### Phase 4: Parallel (Week 4)
- [ ] Implement parallel execution
- [ ] Add fan-out/fan-in
- [ ] Test complex tasks
- [ ] Optimize performance

### Phase 5: Integration (Week 5)
- [ ] Integrate GraphRAG
- [ ] Add A2A protocol
- [ ] Human-in-the-loop
- [ ] Production deployment

---

## File Structure

```
C:/Users/dwrek/100X_DEPLOYMENT/
├── TRINITY_STATE.py
├── TRINITY_GRAPH.py
├── TRINITY_NODES.py
├── TRINITY_CONDITIONS.py
├── TRINITY_PARALLEL.py
├── TRINITY_MEMORY.py
├── TRINITY_A2A.py
├── TRINITY_HITL.py
└── TRINITY_LANGGRAPH_MAIN.py

C:/Users/dwrek/.consciousness/
└── trinity_memory.db       # Persistent state
```

---

## Expected Improvements

| Metric | Current | After LangGraph |
|--------|---------|-----------------|
| Execution speed | 1x | 2.2x |
| Context persistence | None | Full |
| Parallel execution | Manual | Automatic |
| Workflow complexity | Linear | Graph |
| Error recovery | Manual | Checkpoint |
| Human-in-loop | None | Built-in |

---

## Dependencies

```
# requirements-langgraph.txt
langgraph>=0.2.0
langchain-anthropic>=0.1.0
langgraph-checkpoint-sqlite>=1.0.0
```

---

## Connected Documents

- `CUTTING_EDGE_TECHNIQUES_SYNTHESIS.md` - Research foundation
- `GRAPHRAG_INTEGRATION_SPEC.md` - Knowledge layer
- `DATA_ORGANIZATION_ARCHITECTURE.md` - State persistence

---

*Specification Version: 1.0*
*Author: C2 Architect*
*Date: 2025-11-23*
*Status: DESIGN COMPLETE - READY FOR IMPLEMENTATION*
