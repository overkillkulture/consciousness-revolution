"""
MANIPULATION DETECTOR - Real-Time Manipulation Detection
=========================================================
Detects 15-degree manipulation turns and generates counter-strategies.

M Score: 0-100 manipulation risk rating

Created: 2025-11-22
Trinity Build: C2 Architect
"""

from datetime import datetime
from typing import Dict, Any, List, Tuple
from dataclasses import dataclass, asdict

@dataclass
class ManipulationDetection:
    """Result of manipulation detection analysis"""
    m_score: float  # 0-100 manipulation risk
    manipulation_type: str
    turns_detected: List[Dict[str, str]]
    counter_strategy: str
    risk_level: str  # LOW/MEDIUM/HIGH/EXTREME
    red_flags: List[str]
    timestamp: str

class ManipulationDetector:
    """
    Real-time manipulation detection using Pattern Theory.

    Detects:
    - 15-degree turns (subtle pivots)
    - Emotional manipulation
    - Logical fallacies
    - Social engineering tactics
    - Fear/urgency exploitation
    """

    # 15-degree turn patterns
    FIFTEEN_DEGREE_TURNS = {
        "pivot_after_positive": {
            "markers": ["but", "however", "although", "yet", "still"],
            "description": "Starts positive then pivots to undermine",
            "counter": "Focus on the pivot, not the positive setup"
        },
        "false_agreement": {
            "markers": ["i agree, but", "you're right, however", "that's true, but"],
            "description": "Appears to agree while preparing contradiction",
            "counter": "Ask them to state their actual position directly"
        },
        "help_dependency": {
            "markers": ["let me help", "you need me", "without me", "i can fix"],
            "description": "Offers help to create dependency",
            "counter": "Assess if you can solve it independently first"
        },
        "emotional_projection": {
            "markers": ["you made me feel", "you hurt me", "you disappointed"],
            "description": "Projects emotions onto target for guilt",
            "counter": "Separate their emotions from your actions"
        },
        "false_urgency": {
            "markers": ["right now", "immediately", "don't wait", "last chance"],
            "description": "Creates artificial time pressure",
            "counter": "Real opportunities don't require panic decisions"
        },
        "social_proof_fake": {
            "markers": ["everyone thinks", "they all say", "nobody believes"],
            "description": "Uses fake social consensus",
            "counter": "Ask for specific names and verifiable sources"
        },
        "guilt_induction": {
            "markers": ["after all i've done", "i sacrificed", "you owe me"],
            "description": "Uses past actions to obligate future compliance",
            "counter": "Past favors don't create future obligations"
        },
        "gaslighting": {
            "markers": ["that never happened", "you're imagining", "you're too sensitive"],
            "description": "Denies reality to create self-doubt",
            "counter": "Trust your memory and seek external verification"
        }
    }

    # Risk level thresholds
    RISK_LEVELS = {
        (0, 20): "LOW",
        (20, 40): "MEDIUM",
        (40, 70): "HIGH",
        (70, 100): "EXTREME"
    }

    def __init__(self):
        self.detection_count = 0

    def detect(self, text: str, context: str = None) -> ManipulationDetection:
        """
        Analyze text for manipulation patterns.

        Args:
            text: Text to analyze
            context: Optional additional context

        Returns:
            ManipulationDetection with full analysis
        """
        self.detection_count += 1
        text_lower = text.lower()

        # Detect 15-degree turns
        turns_detected = []
        total_severity = 0

        for turn_type, turn_info in self.FIFTEEN_DEGREE_TURNS.items():
            for marker in turn_info["markers"]:
                if marker in text_lower:
                    turns_detected.append({
                        "type": turn_type,
                        "marker": marker,
                        "description": turn_info["description"],
                        "counter": turn_info["counter"]
                    })
                    total_severity += 15
                    break  # Only count each turn type once

        # Detect additional red flags
        red_flags = self._detect_red_flags(text_lower)
        total_severity += len(red_flags) * 10

        # Calculate M score (capped at 100)
        m_score = min(100, total_severity)

        # Determine risk level
        risk_level = self._get_risk_level(m_score)

        # Classify manipulation type
        manipulation_type = self._classify_manipulation(turns_detected, red_flags)

        # Generate counter-strategy
        counter_strategy = self._generate_counter_strategy(
            turns_detected, red_flags, m_score
        )

        return ManipulationDetection(
            m_score=round(m_score, 2),
            manipulation_type=manipulation_type,
            turns_detected=turns_detected,
            counter_strategy=counter_strategy,
            risk_level=risk_level,
            red_flags=red_flags,
            timestamp=datetime.now().isoformat()
        )

    def _detect_red_flags(self, text: str) -> List[str]:
        """Detect additional manipulation red flags."""
        red_flags = []

        # Check for pressure tactics
        if any(w in text for w in ["must", "have to", "need to", "should"]):
            red_flags.append("Pressure language detected")

        # Check for exclusivity claims
        if any(w in text for w in ["only", "exclusive", "special", "secret"]):
            red_flags.append("False exclusivity claim")

        # Check for appeal to authority
        if any(w in text for w in ["expert", "authority", "professional says"]):
            red_flags.append("Unverified authority appeal")

        # Check for absolutist language
        if any(w in text for w in ["always", "never", "everyone", "nobody"]):
            red_flags.append("Absolutist language")

        # Check for character attacks
        if any(w in text for w in ["stupid", "crazy", "wrong", "idiot"]):
            red_flags.append("Ad hominem attack")

        # Check for financial pressure
        if any(w in text for w in ["free", "discount", "deal", "save"]):
            if any(w in text for w in ["now", "today", "limited"]):
                red_flags.append("Financial pressure tactic")

        return red_flags

    def _get_risk_level(self, m_score: float) -> str:
        """Get risk level name from M score."""
        for (low, high), level in self.RISK_LEVELS.items():
            if low <= m_score < high:
                return level
        return "EXTREME"

    def _classify_manipulation(
        self,
        turns: List[Dict],
        red_flags: List[str]
    ) -> str:
        """Classify the primary manipulation type."""
        if not turns and not red_flags:
            return "None detected"

        # Check turn types for classification
        turn_types = [t["type"] for t in turns]

        if "gaslighting" in turn_types:
            return "Gaslighting - Reality Denial"
        elif "emotional_projection" in turn_types or "guilt_induction" in turn_types:
            return "Emotional Manipulation"
        elif "false_urgency" in turn_types:
            return "Urgency Manipulation"
        elif "help_dependency" in turn_types:
            return "Dependency Creation"
        elif "social_proof_fake" in turn_types:
            return "Social Engineering"
        elif "pivot_after_positive" in turn_types or "false_agreement" in turn_types:
            return "Conversational Manipulation"
        elif red_flags:
            return "General Manipulation Tactics"
        else:
            return "Subtle Manipulation"

    def _generate_counter_strategy(
        self,
        turns: List[Dict],
        red_flags: List[str],
        m_score: float
    ) -> str:
        """Generate counter-strategy based on detected manipulation."""
        if m_score < 20:
            return "LOW RISK - Monitor but no immediate action needed. Stay aware."

        strategies = []

        # Add specific counters from detected turns
        for turn in turns[:3]:  # Top 3 turns
            strategies.append(f"• {turn['counter']}")

        # Add general strategies based on risk level
        if m_score >= 70:
            strategies.append("• DISENGAGE - This is high-level manipulation. End interaction.")
            strategies.append("• DOCUMENT - Record this interaction for future reference.")
        elif m_score >= 40:
            strategies.append("• SLOW DOWN - Do not make any decisions under pressure.")
            strategies.append("• VERIFY - Check all claims with independent sources.")
        else:
            strategies.append("• QUESTION - Ask for specifics and clarification.")
            strategies.append("• BOUNDARIES - Maintain your position clearly.")

        return "\n".join(strategies) if strategies else "Stay alert and verify claims."

    def quick_scan(self, text: str) -> Tuple[float, str]:
        """
        Quick scan returning just M score and risk level.

        Args:
            text: Text to scan

        Returns:
            Tuple of (m_score, risk_level)
        """
        result = self.detect(text)
        return result.m_score, result.risk_level

    def to_dict(self, detection: ManipulationDetection) -> Dict[str, Any]:
        """Convert detection to dictionary format."""
        return {
            "success": True,
            "timestamp": detection.timestamp,
            "computer": "TRINITY",
            "result": asdict(detection),
            "metadata": {
                "detection_count": self.detection_count,
                "version": "1.0.0"
            }
        }


def detect_manipulation(text: str) -> Dict[str, Any]:
    """
    Convenience function for quick detection.

    Args:
        text: Text to analyze

    Returns:
        Detection results as dictionary
    """
    detector = ManipulationDetector()
    result = detector.detect(text)
    return detector.to_dict(result)


# Testing
if __name__ == "__main__":
    detector = ManipulationDetector()

    print("=" * 60)
    print("MANIPULATION DETECTOR - TEST RESULTS")
    print("=" * 60)

    test_cases = [
        "I think we should consider this option. Here's why it makes sense.",
        "I agree with you completely, but I think we need to do it my way.",
        "You need to decide right now! This is your last chance! Everyone else already signed up!",
        "After everything I've done for you, you're going to disappoint me like this? You made me feel terrible.",
        "That never happened. You're imagining things. You're being too sensitive about this."
    ]

    for i, test in enumerate(test_cases, 1):
        result = detector.detect(test)
        print(f"\nTest {i}:")
        print(f"Input: {test[:60]}...")
        print(f"M Score: {result.m_score}")
        print(f"Risk Level: {result.risk_level}")
        print(f"Type: {result.manipulation_type}")
        print(f"Turns: {len(result.turns_detected)}")
        print(f"Red Flags: {len(result.red_flags)}")
        print("-" * 60)

    print("\n✅ MANIPULATION DETECTOR OPERATIONAL")
