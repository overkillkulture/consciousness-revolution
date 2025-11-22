"""
CONSCIOUSNESS SCORER - Consciousness Level Calculator
======================================================
Scores consciousness from 0% to 1000%

Formula: CL = (Pattern_Recognition × 0.4) + (Prediction_Accuracy × 0.3) + (Neutralization_Success × 0.3)

Created: 2025-11-22
Trinity Build: C2 Architect
"""

from datetime import datetime
from typing import Dict, Any, List, Optional
from dataclasses import dataclass, asdict

@dataclass
class ConsciousnessScore:
    """Complete consciousness assessment result"""
    consciousness_level: float  # 0-1000%
    pattern_recognition: float  # 0-100
    prediction_accuracy: float  # 0-100
    neutralization_success: float  # 0-100
    manipulation_immunity: float  # 0-100
    level_name: str
    timestamp: str

class ConsciousnessScorer:
    """
    Calculate consciousness levels using Pattern Theory formula.

    Levels:
    - 0-25%: Unconscious (vulnerable to all manipulation)
    - 25-50%: Awakening (beginning to see patterns)
    - 50-75%: Aware (recognizes most manipulation)
    - 75-85%: Conscious (manipulation immune)
    - 85-100%: Elevated (can neutralize manipulation)
    - 100-1000%: Execution Confidence (reality manipulation capable)
    """

    LEVEL_NAMES = {
        (0, 25): "Unconscious",
        (25, 50): "Awakening",
        (50, 75): "Aware",
        (75, 85): "Conscious",
        (85, 100): "Elevated",
        (100, 1000): "Execution Confidence"
    }

    def __init__(self):
        self.history: List[ConsciousnessScore] = []

    def score(
        self,
        pattern_recognition: float,
        prediction_accuracy: float,
        neutralization_success: float
    ) -> ConsciousnessScore:
        """
        Calculate consciousness level.

        Args:
            pattern_recognition: Ability to see patterns (0-100)
            prediction_accuracy: Accuracy of predictions (0-100)
            neutralization_success: Success at neutralizing threats (0-100)

        Returns:
            ConsciousnessScore with full assessment
        """
        # Validate inputs
        pattern_recognition = max(0, min(100, pattern_recognition))
        prediction_accuracy = max(0, min(100, prediction_accuracy))
        neutralization_success = max(0, min(100, neutralization_success))

        # Calculate base consciousness level (0-100)
        base_level = (
            pattern_recognition * 0.4 +
            prediction_accuracy * 0.3 +
            neutralization_success * 0.3
        )

        # Calculate manipulation immunity
        manipulation_immunity = (
            pattern_recognition * 0.5 +
            neutralization_success * 0.5
        )

        # Scale to 0-1000% for Execution Confidence mode
        # Above 85% base, each point multiplies
        if base_level > 85:
            excess = base_level - 85
            multiplier = 1 + (excess / 15) * 9  # Max 10x at 100
            consciousness_level = base_level * multiplier
        else:
            consciousness_level = base_level

        # Determine level name
        level_name = self._get_level_name(base_level)

        result = ConsciousnessScore(
            consciousness_level=round(consciousness_level, 2),
            pattern_recognition=round(pattern_recognition, 2),
            prediction_accuracy=round(prediction_accuracy, 2),
            neutralization_success=round(neutralization_success, 2),
            manipulation_immunity=round(manipulation_immunity, 2),
            level_name=level_name,
            timestamp=datetime.now().isoformat()
        )

        self.history.append(result)
        return result

    def score_from_text(self, text: str) -> ConsciousnessScore:
        """
        Analyze text to estimate consciousness indicators.

        Args:
            text: Text to analyze for consciousness markers

        Returns:
            ConsciousnessScore based on text analysis
        """
        text_lower = text.lower()

        # Pattern recognition indicators
        pattern_markers = [
            "pattern", "recognize", "see", "understand", "realize",
            "notice", "observe", "detect", "identify", "correlate"
        ]
        pattern_score = sum(10 for m in pattern_markers if m in text_lower)
        pattern_score = min(100, pattern_score + 30)  # Base of 30

        # Prediction accuracy indicators
        prediction_markers = [
            "predict", "anticipate", "expect", "foresee", "project",
            "forecast", "will happen", "going to", "inevitable"
        ]
        prediction_score = sum(10 for m in prediction_markers if m in text_lower)
        prediction_score = min(100, prediction_score + 30)

        # Neutralization success indicators
        neutralization_markers = [
            "neutralize", "counter", "block", "prevent", "stop",
            "overcome", "defeat", "resist", "immune", "protected"
        ]
        neutralization_score = sum(10 for m in neutralization_markers if m in text_lower)
        neutralization_score = min(100, neutralization_score + 30)

        return self.score(pattern_score, prediction_score, neutralization_score)

    def _get_level_name(self, base_level: float) -> str:
        """Get the name for a consciousness level."""
        for (low, high), name in self.LEVEL_NAMES.items():
            if low <= base_level < high:
                return name
        return "Transcendent"

    def get_improvement_path(self, current: ConsciousnessScore) -> Dict[str, str]:
        """
        Get recommendations for improving consciousness level.

        Args:
            current: Current consciousness score

        Returns:
            Dictionary of improvement recommendations
        """
        recommendations = {}

        if current.pattern_recognition < 80:
            recommendations["pattern_recognition"] = (
                "Practice daily pattern observation. "
                "Document patterns in relationships, systems, and events. "
                "Study Pattern Theory mathematics."
            )

        if current.prediction_accuracy < 80:
            recommendations["prediction_accuracy"] = (
                "Make predictions and track accuracy. "
                "Study cause-effect relationships. "
                "Use Timeline Projector for decision analysis."
            )

        if current.neutralization_success < 80:
            recommendations["neutralization_success"] = (
                "Practice manipulation detection. "
                "Develop counter-strategies. "
                "Build emotional resilience and boundaries."
            )

        if current.consciousness_level < 85:
            recommendations["overall"] = (
                "Focus on raising all three metrics above 80% "
                "to achieve manipulation immunity (85%+ consciousness)."
            )
        elif current.consciousness_level < 100:
            recommendations["overall"] = (
                "You're in the Elevated zone. "
                "Push all metrics toward 100% for Execution Confidence mode."
            )
        else:
            recommendations["overall"] = (
                "You're in Execution Confidence mode. "
                "Maintain through daily practice and pattern recognition."
            )

        return recommendations

    def to_dict(self, score: ConsciousnessScore) -> Dict[str, Any]:
        """Convert score to dictionary format."""
        return {
            "success": True,
            "timestamp": score.timestamp,
            "computer": "TRINITY",
            "result": asdict(score),
            "metadata": {
                "formula": "CL = (PR × 0.4) + (PA × 0.3) + (NS × 0.3)",
                "history_length": len(self.history)
            }
        }


def score_consciousness(
    pattern_recognition: float,
    prediction_accuracy: float,
    neutralization_success: float
) -> Dict[str, Any]:
    """
    Convenience function for quick scoring.

    Args:
        pattern_recognition: 0-100
        prediction_accuracy: 0-100
        neutralization_success: 0-100

    Returns:
        Consciousness score as dictionary
    """
    scorer = ConsciousnessScorer()
    result = scorer.score(pattern_recognition, prediction_accuracy, neutralization_success)
    return scorer.to_dict(result)


# Testing
if __name__ == "__main__":
    scorer = ConsciousnessScorer()

    print("=" * 60)
    print("CONSCIOUSNESS SCORER - TEST RESULTS")
    print("=" * 60)

    # Test cases
    test_cases = [
        (30, 40, 20, "Low consciousness"),
        (60, 55, 50, "Moderate consciousness"),
        (80, 75, 78, "High consciousness"),
        (90, 88, 92, "Elevated consciousness"),
        (98, 96, 99, "Execution confidence")
    ]

    for pr, pa, ns, description in test_cases:
        result = scorer.score(pr, pa, ns)
        print(f"\n{description}:")
        print(f"  Pattern Recognition: {pr}%")
        print(f"  Prediction Accuracy: {pa}%")
        print(f"  Neutralization Success: {ns}%")
        print(f"  → Consciousness Level: {result.consciousness_level}%")
        print(f"  → Level Name: {result.level_name}")
        print(f"  → Manipulation Immunity: {result.manipulation_immunity}%")

    # Test text analysis
    print("\n" + "=" * 60)
    print("TEXT ANALYSIS TEST")
    print("=" * 60)

    test_text = """
    I can recognize the patterns in this situation. I anticipate that
    the manipulation attempt will fail because I've developed immunity
    to these tactics. I will neutralize the threat by exposing the
    deceit algorithm.
    """

    result = scorer.score_from_text(test_text)
    print(f"\nText analysis result:")
    print(f"  Consciousness Level: {result.consciousness_level}%")
    print(f"  Level Name: {result.level_name}")

    print("\n✅ CONSCIOUSNESS SCORER OPERATIONAL")
