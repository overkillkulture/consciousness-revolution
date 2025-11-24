#!/usr/bin/env python3
"""
BRAIN AGENT FRAMEWORK
Foundation for specialized AI agents that reason, plan, and execute.
Integrates with Cyclotron, GraphRAG, and EOS systems.
"""

import json
import os
from pathlib import Path
from datetime import datetime
from typing import Optional, Callable
from abc import ABC, abstractmethod

# Paths
HOME = Path.home()
CONSCIOUSNESS = HOME / ".consciousness"
BRAIN = CONSCIOUSNESS / "brain"
AGENTS_PATH = CONSCIOUSNESS / "agents"

AGENTS_PATH.mkdir(parents=True, exist_ok=True)

class AgentState:
    """Shared state for agent execution."""

    def __init__(self, task: str):
        self.task = task
        self.context = {}
        self.memory = []
        self.outputs = []
        self.decisions = []
        self.started = datetime.now()
        self.status = "initialized"

    def add_memory(self, item: str, category: str = "observation"):
        """Add to agent memory."""
        self.memory.append({
            "content": item,
            "category": category,
            "timestamp": datetime.now().isoformat()
        })

    def add_output(self, output: str, agent: str):
        """Record agent output."""
        self.outputs.append({
            "agent": agent,
            "output": output,
            "timestamp": datetime.now().isoformat()
        })

    def add_decision(self, decision: str, rationale: str = ""):
        """Record a decision."""
        self.decisions.append({
            "decision": decision,
            "rationale": rationale,
            "timestamp": datetime.now().isoformat()
        })

    def to_dict(self) -> dict:
        return {
            "task": self.task,
            "context": self.context,
            "memory": self.memory,
            "outputs": self.outputs,
            "decisions": self.decisions,
            "started": self.started.isoformat(),
            "status": self.status
        }

class BrainAgent(ABC):
    """Base class for all brain agents."""

    def __init__(self, name: str, description: str):
        self.name = name
        self.description = description
        self.capabilities = []

    @abstractmethod
    def process(self, state: AgentState) -> AgentState:
        """Process the current state and return updated state."""
        pass

    def __repr__(self):
        return f"<{self.__class__.__name__}: {self.name}>"

class ReasoningAgent(BrainAgent):
    """Agent that reasons about problems and generates insights."""

    def __init__(self):
        super().__init__(
            name="Reasoner",
            description="Analyzes problems, identifies patterns, generates insights"
        )
        self.capabilities = ["analyze", "identify_patterns", "generate_insights"]

    def process(self, state: AgentState) -> AgentState:
        """Reason about the task and add insights."""
        task = state.task
        context = state.context

        # Analyze task structure
        insights = []

        # Check for complexity indicators
        if len(task) > 200:
            insights.append("Complex task - consider breaking into subtasks")

        # Check for ambiguity
        question_words = ["what", "how", "why", "when", "where", "which"]
        has_clear_directive = any(word in task.lower() for word in ["create", "build", "fix", "update", "delete"])

        if not has_clear_directive:
            insights.append("Task may need clarification - no clear action verb")

        # Check for dependencies
        dependency_words = ["after", "before", "then", "first", "requires"]
        if any(word in task.lower() for word in dependency_words):
            insights.append("Task has dependencies - sequence matters")

        # Pattern matching against known patterns
        if "api" in task.lower():
            insights.append("API work detected - consider rate limits and error handling")

        if "data" in task.lower():
            insights.append("Data work detected - consider backup and validation")

        if "user" in task.lower():
            insights.append("User-facing work - consider UX and error messages")

        # Add insights to state
        for insight in insights:
            state.add_memory(insight, "insight")

        state.add_output(
            f"Reasoning complete: {len(insights)} insights generated",
            self.name
        )

        return state

class PlanningAgent(BrainAgent):
    """Agent that creates execution plans."""

    def __init__(self):
        super().__init__(
            name="Planner",
            description="Creates structured execution plans with steps and dependencies"
        )
        self.capabilities = ["create_plan", "estimate_effort", "identify_risks"]

    def process(self, state: AgentState) -> AgentState:
        """Create a plan for the task."""
        task = state.task

        # Generate plan structure
        plan = {
            "goal": task,
            "steps": [],
            "risks": [],
            "estimated_effort": "medium"
        }

        # Break task into steps (simplified heuristic)
        task_lower = task.lower()

        # Standard phases
        if "build" in task_lower or "create" in task_lower:
            plan["steps"] = [
                {"step": 1, "action": "Research and gather requirements", "status": "pending"},
                {"step": 2, "action": "Design solution architecture", "status": "pending"},
                {"step": 3, "action": "Implement core functionality", "status": "pending"},
                {"step": 4, "action": "Test and validate", "status": "pending"},
                {"step": 5, "action": "Document and deploy", "status": "pending"}
            ]
        elif "fix" in task_lower or "debug" in task_lower:
            plan["steps"] = [
                {"step": 1, "action": "Reproduce the issue", "status": "pending"},
                {"step": 2, "action": "Identify root cause", "status": "pending"},
                {"step": 3, "action": "Implement fix", "status": "pending"},
                {"step": 4, "action": "Test fix", "status": "pending"},
                {"step": 5, "action": "Verify no regression", "status": "pending"}
            ]
        elif "analyze" in task_lower or "research" in task_lower:
            plan["steps"] = [
                {"step": 1, "action": "Define scope and questions", "status": "pending"},
                {"step": 2, "action": "Gather data sources", "status": "pending"},
                {"step": 3, "action": "Analyze data", "status": "pending"},
                {"step": 4, "action": "Synthesize findings", "status": "pending"},
                {"step": 5, "action": "Present conclusions", "status": "pending"}
            ]
        else:
            plan["steps"] = [
                {"step": 1, "action": "Understand requirements", "status": "pending"},
                {"step": 2, "action": "Execute task", "status": "pending"},
                {"step": 3, "action": "Verify completion", "status": "pending"}
            ]

        # Identify risks
        if "api" in task_lower:
            plan["risks"].append("API rate limits or downtime")
        if "data" in task_lower:
            plan["risks"].append("Data loss or corruption")
        if "deploy" in task_lower:
            plan["risks"].append("Deployment failures or rollback needed")

        # Store plan in context
        state.context["plan"] = plan

        # Add to memory
        state.add_memory(f"Plan created with {len(plan['steps'])} steps", "plan")

        state.add_output(
            f"Plan created: {len(plan['steps'])} steps, {len(plan['risks'])} risks identified",
            self.name
        )

        return state

class ExecutionAgent(BrainAgent):
    """Agent that executes planned steps."""

    def __init__(self):
        super().__init__(
            name="Executor",
            description="Executes plan steps and tracks progress"
        )
        self.capabilities = ["execute_step", "track_progress", "handle_errors"]

    def process(self, state: AgentState) -> AgentState:
        """Execute the plan."""
        plan = state.context.get("plan", {})

        if not plan:
            state.add_memory("No plan found - cannot execute", "error")
            return state

        # Simulate execution of steps
        executed = 0
        for step in plan.get("steps", []):
            if step["status"] == "pending":
                # Mark as in progress then complete (simulation)
                step["status"] = "complete"
                step["completed_at"] = datetime.now().isoformat()
                executed += 1

                state.add_memory(
                    f"Completed step {step['step']}: {step['action']}",
                    "execution"
                )

        # Update plan in context
        state.context["plan"] = plan

        state.add_output(
            f"Execution complete: {executed} steps executed",
            self.name
        )

        return state

class SynthesisAgent(BrainAgent):
    """Agent that synthesizes outputs from other agents."""

    def __init__(self):
        super().__init__(
            name="Synthesizer",
            description="Combines agent outputs into coherent results"
        )
        self.capabilities = ["synthesize", "summarize", "recommend"]

    def process(self, state: AgentState) -> AgentState:
        """Synthesize all outputs."""
        # Gather all outputs
        outputs = state.outputs
        memory = state.memory
        decisions = state.decisions

        # Create synthesis
        synthesis = {
            "task": state.task,
            "agents_involved": list(set(o["agent"] for o in outputs)),
            "insights_count": len([m for m in memory if m["category"] == "insight"]),
            "steps_executed": len([m for m in memory if m["category"] == "execution"]),
            "decisions_made": len(decisions),
            "status": "complete"
        }

        # Generate summary
        summary_parts = []

        if synthesis["insights_count"] > 0:
            summary_parts.append(f"{synthesis['insights_count']} insights generated")

        if synthesis["steps_executed"] > 0:
            summary_parts.append(f"{synthesis['steps_executed']} steps executed")

        if synthesis["decisions_made"] > 0:
            summary_parts.append(f"{synthesis['decisions_made']} decisions made")

        synthesis["summary"] = "; ".join(summary_parts) if summary_parts else "Task processed"

        state.context["synthesis"] = synthesis
        state.status = "complete"

        state.add_output(
            f"Synthesis complete: {synthesis['summary']}",
            self.name
        )

        return state

class AgentOrchestrator:
    """Orchestrates multiple agents to complete tasks."""

    def __init__(self):
        self.agents = {
            "reasoner": ReasoningAgent(),
            "planner": PlanningAgent(),
            "executor": ExecutionAgent(),
            "synthesizer": SynthesisAgent()
        }
        self.execution_log = []

    def run(self, task: str, agent_sequence: list = None) -> AgentState:
        """
        Run agents on a task.

        Args:
            task: The task to complete
            agent_sequence: List of agent names to run (default: all in order)

        Returns:
            Final agent state
        """
        # Default sequence
        if agent_sequence is None:
            agent_sequence = ["reasoner", "planner", "executor", "synthesizer"]

        # Initialize state
        state = AgentState(task)

        print(f"\n{'='*50}")
        print(f"AGENT ORCHESTRATOR")
        print(f"{'='*50}")
        print(f"Task: {task[:100]}...")
        print(f"Agents: {' → '.join(agent_sequence)}")
        print()

        # Run each agent
        for agent_name in agent_sequence:
            agent = self.agents.get(agent_name)
            if not agent:
                print(f"⚠️  Unknown agent: {agent_name}")
                continue

            print(f"Running {agent.name}...")
            state = agent.process(state)

            # Log execution
            self.execution_log.append({
                "agent": agent_name,
                "timestamp": datetime.now().isoformat()
            })

        # Save state
        self._save_state(state)

        print(f"\n{'='*50}")
        print("ORCHESTRATION COMPLETE")
        print(f"{'='*50}")
        print(f"Status: {state.status}")
        print(f"Memory items: {len(state.memory)}")
        print(f"Outputs: {len(state.outputs)}")

        return state

    def _save_state(self, state: AgentState):
        """Save state to disk."""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        state_file = AGENTS_PATH / f"state_{timestamp}.json"

        with open(state_file, 'w') as f:
            json.dump(state.to_dict(), f, indent=2)

        print(f"\nState saved to: {state_file}")

    def get_agent_capabilities(self) -> dict:
        """Get all agent capabilities."""
        return {
            name: agent.capabilities
            for name, agent in self.agents.items()
        }

def demo():
    """Demonstrate the brain agent framework."""
    orchestrator = AgentOrchestrator()

    # Test tasks
    tasks = [
        "Build a new pattern detector for social media manipulation",
        "Fix the bug in the scorecard automation script",
        "Research GraphRAG implementation patterns"
    ]

    for task in tasks:
        print("\n" + "="*60)
        state = orchestrator.run(task)

        # Show results
        print("\nResults:")
        for output in state.outputs:
            print(f"  [{output['agent']}] {output['output']}")

        if state.context.get("synthesis"):
            print(f"\nSynthesis: {state.context['synthesis']['summary']}")

if __name__ == "__main__":
    demo()
