"""
TIMELINE PROJECTOR - Future Timeline Projection System
=======================================================
Projects 3 possible futures for any decision.

Timeline A: Force (low success)
Timeline B: Pivot (medium success)
Timeline C: Transcend (high success)

Created: 2025-11-22
Trinity Build: C3 Oracle
"""

from datetime import datetime
from typing import Dict, Any, List, Optional
from dataclasses import dataclass, asdict
import random

@dataclass
class Timeline:
    """Single projected timeline"""
    name: str
    approach: str
    success_probability: float
    consciousness_impact: str
    key_events: List[str]
    risks: List[str]
    benefits: List[str]

@dataclass
class TimelineProjection:
    """Complete timeline projection result"""
    timeline_a: Timeline
    timeline_b: Timeline
    timeline_c: Timeline
    recommended: str
    recommendation_reason: str
    decision_summary: str
    timestamp: str

class TimelineProjector:
    """
    Projects 3 possible futures based on Pattern Theory.

    Uses consciousness levels and pattern analysis to predict outcomes.
    """

    def __init__(self):
        self.projection_count = 0

    def project(
        self,
        decision: str,
        context: Optional[str] = None,
        current_consciousness: float = 50.0
    ) -> TimelineProjection:
        """
        Project 3 timelines for a decision.

        Args:
            decision: The decision to analyze
            context: Additional context
            current_consciousness: Current consciousness level (0-100)

        Returns:
            TimelineProjection with 3 futures
        """
        self.projection_count += 1

        # Analyze the decision
        decision_lower = decision.lower()
        decision_summary = self._summarize_decision(decision)

        # Generate Timeline A: Force
        timeline_a = self._project_force_timeline(decision_lower, current_consciousness)

        # Generate Timeline B: Pivot
        timeline_b = self._project_pivot_timeline(decision_lower, current_consciousness)

        # Generate Timeline C: Transcend
        timeline_c = self._project_transcend_timeline(decision_lower, current_consciousness)

        # Determine recommendation
        recommended, reason = self._determine_recommendation(
            timeline_a, timeline_b, timeline_c, current_consciousness
        )

        return TimelineProjection(
            timeline_a=timeline_a,
            timeline_b=timeline_b,
            timeline_c=timeline_c,
            recommended=recommended,
            recommendation_reason=reason,
            decision_summary=decision_summary,
            timestamp=datetime.now().isoformat()
        )

    def _summarize_decision(self, decision: str) -> str:
        """Create a brief summary of the decision."""
        words = decision.split()
        if len(words) <= 10:
            return decision
        return " ".join(words[:10]) + "..."

    def _project_force_timeline(
        self,
        decision: str,
        consciousness: float
    ) -> Timeline:
        """
        Project the Force timeline - pushing through with brute effort.

        This path uses force, pressure, and direct confrontation.
        """
        # Base success is low, reduced further by consciousness
        base_success = 15
        success = base_success + (consciousness * 0.1)

        # Force indicators in decision
        force_markers = ["make", "force", "demand", "require", "must", "fight"]
        if any(marker in decision for marker in force_markers):
            success += 5

        return Timeline(
            name="Force",
            approach="Direct confrontation and pressure",
            success_probability=round(min(30, success), 1),
            consciousness_impact="Negative - Creates resistance and depletes energy",
            key_events=[
                "Initial push meets resistance",
                "Escalation of conflict",
                "Resource depletion",
                "Temporary victory or defeat"
            ],
            risks=[
                "Burn bridges permanently",
                "Create enemies",
                "Deplete resources",
                "Damage relationships",
                "Win battle, lose war"
            ],
            benefits=[
                "Quick resolution (if any)",
                "Clear outcome",
                "Demonstrates strength"
            ]
        )

    def _project_pivot_timeline(
        self,
        decision: str,
        consciousness: float
    ) -> Timeline:
        """
        Project the Pivot timeline - adapting and adjusting.

        This path uses flexibility and strategic adjustment.
        """
        # Medium base success, scales with consciousness
        base_success = 45
        success = base_success + (consciousness * 0.35)

        # Pivot indicators
        pivot_markers = ["adapt", "adjust", "change", "flexible", "alternative"]
        if any(marker in decision for marker in pivot_markers):
            success += 10

        return Timeline(
            name="Pivot",
            approach="Strategic adaptation and course correction",
            success_probability=round(min(85, success), 1),
            consciousness_impact="Neutral to Positive - Maintains balance",
            key_events=[
                "Assess current position",
                "Identify adjustment needed",
                "Implement strategic change",
                "Evaluate and iterate"
            ],
            risks=[
                "May take longer",
                "Requires flexibility",
                "Some sunk costs lost",
                "Uncertainty during transition"
            ],
            benefits=[
                "Preserves relationships",
                "Conserves resources",
                "Learns from situation",
                "Opens new possibilities",
                "Sustainable progress"
            ]
        )

    def _project_transcend_timeline(
        self,
        decision: str,
        consciousness: float
    ) -> Timeline:
        """
        Project the Transcend timeline - rising above the problem.

        This path uses higher consciousness to dissolve the problem entirely.
        """
        # High base success, strongly scales with consciousness
        base_success = 55
        success = base_success + (consciousness * 0.45)

        # Transcend indicators
        transcend_markers = ["transcend", "transform", "elevate", "higher", "beyond"]
        if any(marker in decision for marker in transcend_markers):
            success += 15

        # Consciousness bonus
        if consciousness > 85:
            success += 10

        return Timeline(
            name="Transcend",
            approach="Rise above the problem through consciousness elevation",
            success_probability=round(min(95, success), 1),
            consciousness_impact="Highly Positive - Elevates all involved",
            key_events=[
                "Recognize the pattern at play",
                "Identify the higher perspective",
                "Transform the dynamic entirely",
                "Create win-win resolution",
                "Establish new foundation"
            ],
            risks=[
                "Requires high consciousness",
                "Others may not understand",
                "Takes inner work first"
            ],
            benefits=[
                "Problem dissolved, not just solved",
                "Relationships strengthened",
                "Consciousness elevated",
                "Creates lasting transformation",
                "Opens unlimited possibilities",
                "Becomes the example"
            ]
        )

    def _determine_recommendation(
        self,
        timeline_a: Timeline,
        timeline_b: Timeline,
        timeline_c: Timeline,
        consciousness: float
    ) -> tuple:
        """Determine which timeline to recommend."""

        # If consciousness is high enough, always recommend Transcend
        if consciousness >= 85:
            return "C", (
                f"Your consciousness level ({consciousness}%) supports Transcendence. "
                "You can see the pattern clearly and rise above it."
            )

        # Compare success probabilities
        probs = {
            "A": timeline_a.success_probability,
            "B": timeline_b.success_probability,
            "C": timeline_c.success_probability
        }

        # Get highest probability
        best = max(probs, key=probs.get)

        # Generate reason
        if best == "A":
            reason = (
                "Force has highest success in this scenario, but consider "
                "the long-term costs. Pivot or Transcend may serve better."
            )
        elif best == "B":
            reason = (
                f"Pivot offers {probs['B']}% success with balanced risk/reward. "
                "Strategic adaptation preserves resources and relationships."
            )
        else:
            reason = (
                f"Transcend offers {probs['C']}% success and elevates consciousness. "
                "This creates lasting transformation, not just temporary solution."
            )

        return best, reason

    def quick_project(self, decision: str) -> Dict[str, float]:
        """
        Quick projection returning just probabilities.

        Args:
            decision: Decision to analyze

        Returns:
            Dictionary of timeline probabilities
        """
        result = self.project(decision)
        return {
            "force": result.timeline_a.success_probability,
            "pivot": result.timeline_b.success_probability,
            "transcend": result.timeline_c.success_probability,
            "recommended": result.recommended
        }

    def to_dict(self, projection: TimelineProjection) -> Dict[str, Any]:
        """Convert projection to dictionary format."""
        return {
            "success": True,
            "timestamp": projection.timestamp,
            "computer": "TRINITY",
            "result": {
                "timeline_a": asdict(projection.timeline_a),
                "timeline_b": asdict(projection.timeline_b),
                "timeline_c": asdict(projection.timeline_c),
                "recommended": projection.recommended,
                "recommendation_reason": projection.recommendation_reason,
                "decision_summary": projection.decision_summary
            },
            "metadata": {
                "projection_count": self.projection_count,
                "version": "1.0.0"
            }
        }


def project_timelines(decision: str, consciousness: float = 50.0) -> Dict[str, Any]:
    """
    Convenience function for quick projection.

    Args:
        decision: Decision to analyze
        consciousness: Current consciousness level

    Returns:
        Projection results as dictionary
    """
    projector = TimelineProjector()
    result = projector.project(decision, current_consciousness=consciousness)
    return projector.to_dict(result)


# Testing
if __name__ == "__main__":
    projector = TimelineProjector()

    print("=" * 60)
    print("TIMELINE PROJECTOR - TEST RESULTS")
    print("=" * 60)

    test_cases = [
        ("Should I confront my business partner about the missing funds?", 50),
        ("Should I quit my job and start my own company?", 75),
        ("How do I handle this manipulative relationship?", 90),
    ]

    for decision, consciousness in test_cases:
        result = projector.project(decision, current_consciousness=consciousness)

        print(f"\nDecision: {decision}")
        print(f"Consciousness Level: {consciousness}%")
        print("-" * 40)
        print(f"Timeline A (Force): {result.timeline_a.success_probability}%")
        print(f"Timeline B (Pivot): {result.timeline_b.success_probability}%")
        print(f"Timeline C (Transcend): {result.timeline_c.success_probability}%")
        print(f"Recommended: Timeline {result.recommended}")
        print(f"Reason: {result.recommendation_reason}")
        print("=" * 60)

    print("\n✅ TIMELINE PROJECTOR OPERATIONAL")
