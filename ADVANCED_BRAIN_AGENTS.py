#!/usr/bin/env python3
"""
ADVANCED BRAIN AGENTS
Specialized agents that integrate with Cyclotron, Pattern Theory, and Knowledge Systems.
Extension of BRAIN_AGENT_FRAMEWORK for deep system integration.
"""

import json
import os
from pathlib import Path
from datetime import datetime
from typing import Optional, List
import re

# Import base framework
from BRAIN_AGENT_FRAMEWORK import BrainAgent, AgentState, AgentOrchestrator

# Paths
HOME = Path.home()
CONSCIOUSNESS = HOME / ".consciousness"
BRAIN = CONSCIOUSNESS / "brain"
CYCLOTRON = CONSCIOUSNESS / "cyclotron_core"
DEPLOYMENT = HOME / "100X_DEPLOYMENT"

class CyclotronAgent(BrainAgent):
    """Agent that interfaces with C1's Cyclotron brain."""

    def __init__(self):
        super().__init__(
            name="Cyclotron",
            description="Queries and updates Cyclotron knowledge atoms"
        )
        self.capabilities = ["query_atoms", "create_atom", "link_atoms", "search_knowledge"]
        self.cyclotron_path = CYCLOTRON

    def process(self, state: AgentState) -> AgentState:
        """Query Cyclotron for relevant knowledge."""
        task = state.task.lower()

        # Load Cyclotron index
        index = self._load_index()
        if not index:
            state.add_memory("Cyclotron index not found - operating without knowledge base", "warning")
            return state

        # Extract keywords from task
        keywords = self._extract_keywords(task)

        # Search for relevant atoms
        relevant_atoms = []
        for atom in index.get("atoms", []):
            atom_text = f"{atom.get('content', '')} {' '.join(atom.get('tags', []))}".lower()
            if any(kw in atom_text for kw in keywords):
                relevant_atoms.append(atom)

        # Add to context
        state.context["cyclotron_atoms"] = relevant_atoms[:10]  # Top 10
        state.context["cyclotron_keywords"] = keywords

        state.add_memory(
            f"Found {len(relevant_atoms)} relevant Cyclotron atoms for keywords: {keywords}",
            "knowledge"
        )

        state.add_output(
            f"Cyclotron query complete: {len(relevant_atoms)} atoms found",
            self.name
        )

        return state

    def _load_index(self) -> dict:
        """Load Cyclotron index."""
        index_path = self.cyclotron_path / "INDEX.json"
        if index_path.exists():
            with open(index_path) as f:
                return json.load(f)
        return {}

    def _extract_keywords(self, text: str) -> list:
        """Extract meaningful keywords from text."""
        # Remove common words
        stop_words = {'the', 'a', 'an', 'is', 'are', 'was', 'were', 'be', 'been',
                     'being', 'have', 'has', 'had', 'do', 'does', 'did', 'will',
                     'would', 'could', 'should', 'may', 'might', 'must', 'shall',
                     'to', 'of', 'in', 'for', 'on', 'with', 'at', 'by', 'from',
                     'as', 'into', 'through', 'during', 'before', 'after', 'and',
                     'but', 'or', 'nor', 'so', 'yet', 'both', 'either', 'neither',
                     'not', 'only', 'own', 'same', 'than', 'too', 'very', 'just'}

        words = re.findall(r'\b[a-z]{3,}\b', text.lower())
        keywords = [w for w in words if w not in stop_words]

        return list(set(keywords))[:10]


class PatternAgent(BrainAgent):
    """Agent that detects patterns using Pattern Theory."""

    def __init__(self):
        super().__init__(
            name="PatternDetector",
            description="Analyzes input for manipulation and behavioral patterns"
        )
        self.capabilities = ["detect_manipulation", "classify_domain", "assess_threat"]

        # Import pattern detector
        try:
            from PATTERN_DETECTOR import PatternDetector
            self.detector = PatternDetector()
        except ImportError:
            self.detector = None

    def process(self, state: AgentState) -> AgentState:
        """Analyze task for patterns."""
        if not self.detector:
            state.add_memory("Pattern detector not available", "warning")
            return state

        task = state.task

        # Analyze for manipulation patterns
        result = self.detector.analyze(task)

        # Store results
        state.context["pattern_analysis"] = {
            "threat_level": result["threat_level"],
            "patterns_detected": result["patterns_detected"],
            "domain_scores": result["domain_scores"],
            "recommendations": result["recommendations"]
        }

        # Add insights
        if result["threat_level"] != "clean":
            for detection in result["detections"]:
                state.add_memory(
                    f"Pattern detected: {detection['pattern']} ({detection['severity']}) in {detection['domain']} domain",
                    "pattern"
                )

        state.add_output(
            f"Pattern analysis: {result['threat_level']} threat, {result['patterns_detected']} patterns",
            self.name
        )

        return state


class KnowledgeAgent(BrainAgent):
    """Agent that manages and queries knowledge graphs."""

    def __init__(self):
        super().__init__(
            name="KnowledgeGraph",
            description="Manages entities, relationships, and knowledge queries"
        )
        self.capabilities = ["query_entities", "find_relationships", "traverse_graph", "summarize_knowledge"]
        self.brain_path = BRAIN

    def process(self, state: AgentState) -> AgentState:
        """Query knowledge graph for task context."""
        task = state.task.lower()

        # Load brain knowledge
        knowledge = self._load_brain_knowledge()

        # Find relevant entities
        entities = []
        relationships = []

        if "entities" in knowledge:
            for entity in knowledge["entities"]:
                if any(kw in entity.get("name", "").lower() for kw in task.split()):
                    entities.append(entity)

        # Store in context
        state.context["knowledge"] = {
            "entities": entities[:5],
            "total_entities": len(knowledge.get("entities", [])),
            "knowledge_summary": knowledge.get("summary", {})
        }

        state.add_memory(
            f"Knowledge graph query: {len(entities)} relevant entities found",
            "knowledge"
        )

        state.add_output(
            f"Knowledge query complete: {len(entities)} entities",
            self.name
        )

        return state

    def _load_brain_knowledge(self) -> dict:
        """Load brain knowledge index."""
        knowledge = {}

        # Load entities
        entities_path = CONSCIOUSNESS / "graphrag" / "entities"
        if entities_path.exists():
            knowledge["entities"] = []
            for f in entities_path.glob("*.json"):
                with open(f) as file:
                    knowledge["entities"].extend(json.load(file).get("entities", []))

        # Load summary
        summary_path = self.brain_path / "knowledge_summary.json"
        if summary_path.exists():
            with open(summary_path) as f:
                knowledge["summary"] = json.load(f)

        return knowledge


class DecisionAgent(BrainAgent):
    """Agent that makes autonomous decisions based on context."""

    def __init__(self):
        super().__init__(
            name="DecisionMaker",
            description="Makes decisions based on patterns, knowledge, and priorities"
        )
        self.capabilities = ["evaluate_options", "assess_risk", "recommend_action", "prioritize"]

    def process(self, state: AgentState) -> AgentState:
        """Make decisions based on gathered context."""
        # Gather all context
        cyclotron = state.context.get("cyclotron_atoms", [])
        patterns = state.context.get("pattern_analysis", {})
        knowledge = state.context.get("knowledge", {})
        plan = state.context.get("plan", {})

        # Decision factors
        factors = {
            "knowledge_available": len(cyclotron) > 0 or len(knowledge.get("entities", [])) > 0,
            "threat_level": patterns.get("threat_level", "clean"),
            "has_plan": bool(plan),
            "complexity": "high" if len(state.task) > 200 else "medium" if len(state.task) > 50 else "low"
        }

        # Generate decisions
        decisions = []

        # Risk assessment
        if factors["threat_level"] in ["medium", "high"]:
            decisions.append({
                "type": "risk_mitigation",
                "action": "Apply pattern recommendations before proceeding",
                "priority": "high",
                "rationale": f"Threat level is {factors['threat_level']}"
            })

        # Knowledge utilization
        if factors["knowledge_available"]:
            decisions.append({
                "type": "knowledge_application",
                "action": "Leverage existing knowledge atoms and entities",
                "priority": "medium",
                "rationale": "Relevant knowledge found in Cyclotron/Brain"
            })
        else:
            decisions.append({
                "type": "knowledge_creation",
                "action": "Create new knowledge atoms from task results",
                "priority": "medium",
                "rationale": "No existing knowledge - build new"
            })

        # Execution approach
        if factors["complexity"] == "high":
            decisions.append({
                "type": "execution_strategy",
                "action": "Break into subtasks and execute iteratively",
                "priority": "high",
                "rationale": "High complexity requires decomposition"
            })
        else:
            decisions.append({
                "type": "execution_strategy",
                "action": "Execute directly with standard pipeline",
                "priority": "low",
                "rationale": "Manageable complexity"
            })

        # Store decisions
        state.context["decisions"] = decisions

        for decision in decisions:
            state.add_decision(
                decision["action"],
                decision["rationale"]
            )

        state.add_output(
            f"Decision analysis complete: {len(decisions)} decisions made",
            self.name
        )

        return state


class MemoryAgent(BrainAgent):
    """Agent that manages persistent memory across sessions."""

    def __init__(self):
        super().__init__(
            name="Memory",
            description="Stores and retrieves cross-session memories"
        )
        self.capabilities = ["store_memory", "recall_memory", "consolidate", "forget"]
        self.memory_path = CONSCIOUSNESS / "memory"
        self.memory_path.mkdir(parents=True, exist_ok=True)

    def process(self, state: AgentState) -> AgentState:
        """Manage task memory."""
        # Load relevant memories
        memories = self._load_memories()

        # Find related past tasks
        related = []
        for memory in memories:
            if any(word in memory.get("task", "").lower() for word in state.task.lower().split()[:5]):
                related.append(memory)

        state.context["related_memories"] = related[:5]

        if related:
            state.add_memory(
                f"Found {len(related)} related past tasks",
                "memory"
            )

            # Learn from past
            for mem in related[:3]:
                if mem.get("success"):
                    state.add_memory(
                        f"Past success: {mem.get('task', '')[:50]}...",
                        "learning"
                    )

        state.add_output(
            f"Memory recall: {len(related)} related memories",
            self.name
        )

        return state

    def _load_memories(self) -> list:
        """Load all stored memories."""
        memories = []
        for f in self.memory_path.glob("*.json"):
            with open(f) as file:
                memories.append(json.load(file))
        return sorted(memories, key=lambda x: x.get("timestamp", ""), reverse=True)

    def store(self, state: AgentState, success: bool = True):
        """Store task memory for future recall."""
        memory = {
            "task": state.task,
            "success": success,
            "outputs": state.outputs,
            "decisions": state.decisions,
            "timestamp": datetime.now().isoformat()
        }

        filename = f"memory_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        with open(self.memory_path / filename, 'w') as f:
            json.dump(memory, f, indent=2)


class AdvancedOrchestrator(AgentOrchestrator):
    """Extended orchestrator with advanced agents."""

    def __init__(self):
        super().__init__()

        # Add advanced agents
        self.agents.update({
            "cyclotron": CyclotronAgent(),
            "pattern": PatternAgent(),
            "knowledge": KnowledgeAgent(),
            "decision": DecisionAgent(),
            "memory": MemoryAgent()
        })

    def run_advanced(self, task: str) -> AgentState:
        """
        Run full advanced pipeline.

        Pipeline:
        1. Memory - recall related past tasks
        2. Cyclotron - query knowledge base
        3. Knowledge - query entities
        4. Pattern - detect manipulation
        5. Reasoner - analyze task
        6. Planner - create plan
        7. Decision - make decisions
        8. Executor - execute
        9. Synthesizer - combine results
        """
        sequence = [
            "memory",
            "cyclotron",
            "knowledge",
            "pattern",
            "reasoner",
            "planner",
            "decision",
            "executor",
            "synthesizer"
        ]

        return self.run(task, sequence)

    def run_quick(self, task: str) -> AgentState:
        """Quick pipeline for simple tasks."""
        sequence = ["reasoner", "planner", "executor", "synthesizer"]
        return self.run(task, sequence)

    def run_research(self, task: str) -> AgentState:
        """Research pipeline without execution."""
        sequence = ["memory", "cyclotron", "knowledge", "pattern", "reasoner", "synthesizer"]
        return self.run(task, sequence)


def demo():
    """Demonstrate advanced brain agents."""
    print("=" * 60)
    print("ADVANCED BRAIN AGENTS DEMO")
    print("=" * 60)

    orchestrator = AdvancedOrchestrator()

    # Test advanced pipeline
    tasks = [
        "Build integration between Trinity and Cyclotron for real-time knowledge sync",
        "Analyze this message for manipulation: 'After everything I've done for you, you owe me this'",
        "Research GraphRAG patterns for multi-agent knowledge sharing"
    ]

    for i, task in enumerate(tasks, 1):
        print(f"\n{'='*60}")
        print(f"TASK {i}: {task[:50]}...")
        print("=" * 60)

        if i == 1:
            state = orchestrator.run_advanced(task)
        elif i == 2:
            state = orchestrator.run(task, ["pattern", "decision", "synthesizer"])
        else:
            state = orchestrator.run_research(task)

        # Show results
        print("\nResults Summary:")
        print(f"  Status: {state.status}")
        print(f"  Memory items: {len(state.memory)}")
        print(f"  Decisions made: {len(state.decisions)}")

        if state.decisions:
            print("\nDecisions:")
            for d in state.decisions:
                print(f"  • {d['decision']}")

        if state.context.get("pattern_analysis"):
            pa = state.context["pattern_analysis"]
            print(f"\nPattern Analysis:")
            print(f"  Threat: {pa['threat_level']}")
            print(f"  Patterns: {pa['patterns_detected']}")

        if state.context.get("synthesis"):
            print(f"\nSynthesis: {state.context['synthesis'].get('summary', 'N/A')}")

    print("\n" + "=" * 60)
    print("AGENT CAPABILITIES")
    print("=" * 60)

    for name, agent in orchestrator.agents.items():
        print(f"\n{name}: {agent.description}")
        print(f"  Capabilities: {', '.join(agent.capabilities)}")


if __name__ == "__main__":
    demo()
