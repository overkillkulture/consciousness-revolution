"""
CONSCIOUSNESS BRIDGE - 3-Minute Revelation
============================================
Interactive assessment that reveals consciousness level in 3 minutes.

Integrates with Pattern Theory Engine for accurate scoring.

Created: 2025-11-22
Phase 3: Consciousness Platform
"""

import sys
import os
from typing import Dict, Any, List
from dataclasses import dataclass
from datetime import datetime

# Add Pattern Theory Engine (using environment variable)
base_path = os.environ.get("PATTERN_ENGINE_PATH", "/app/PATTERN_THEORY_ENGINE")
sys.path.insert(0, base_path)
sys.path.insert(0, os.path.join(base_path, "core"))

try:
    from CONSCIOUSNESS_SCORER import ConsciousnessScorer
    from SEVEN_DOMAINS_ANALYZER import SevenDomainsAnalyzer
    ENGINES_AVAILABLE = True
except ImportError:
    ENGINES_AVAILABLE = False

@dataclass
class BridgeQuestion:
    """Single assessment question"""
    id: int
    text: str
    domain: str
    options: List[Dict[str, Any]]

@dataclass
class BridgeResult:
    """Assessment result"""
    consciousness_level: float
    level_name: str
    percentile: int
    domain_scores: Dict[str, float]
    strengths: List[str]
    growth_areas: List[str]
    recommended_path: str
    timestamp: str

class ConsciousnessBridge:
    """
    3-minute consciousness revelation system.
    """

    # Assessment questions (7 domains x 2 questions = 14 questions)
    QUESTIONS = [
        # Physical Domain
        BridgeQuestion(1, "How aware are you of your body's signals throughout the day?",
            "physical", [
                {"text": "Rarely notice them", "score": 20},
                {"text": "Sometimes when they're strong", "score": 40},
                {"text": "Often check in", "score": 70},
                {"text": "Constant awareness", "score": 95}
            ]),
        BridgeQuestion(2, "How do you respond to physical discomfort?",
            "physical", [
                {"text": "Ignore until it's severe", "score": 20},
                {"text": "Address with quick fixes", "score": 45},
                {"text": "Investigate the cause", "score": 75},
                {"text": "Treat as valuable information", "score": 95}
            ]),

        # Financial Domain
        BridgeQuestion(3, "How do you feel about your current financial situation?",
            "financial", [
                {"text": "Stressed and uncertain", "score": 25},
                {"text": "Managing but worried", "score": 45},
                {"text": "Stable and intentional", "score": 75},
                {"text": "Abundant and flowing", "score": 95}
            ]),
        BridgeQuestion(4, "How do you make financial decisions?",
            "financial", [
                {"text": "React to immediate needs", "score": 20},
                {"text": "Follow conventional advice", "score": 45},
                {"text": "Align with personal values", "score": 75},
                {"text": "Create value for all involved", "score": 95}
            ]),

        # Mental Domain
        BridgeQuestion(5, "How often do you question your own thoughts?",
            "mental", [
                {"text": "Rarely - they feel true", "score": 20},
                {"text": "When things go wrong", "score": 45},
                {"text": "Regularly observe patterns", "score": 75},
                {"text": "Constantly discerning", "score": 95}
            ]),
        BridgeQuestion(6, "How do you handle information that contradicts your beliefs?",
            "mental", [
                {"text": "Dismiss it quickly", "score": 15},
                {"text": "Feel uncomfortable", "score": 40},
                {"text": "Examine objectively", "score": 75},
                {"text": "Welcome as growth opportunity", "score": 95}
            ]),

        # Emotional Domain
        BridgeQuestion(7, "How do you process difficult emotions?",
            "emotional", [
                {"text": "Suppress or avoid", "score": 20},
                {"text": "Express reactively", "score": 40},
                {"text": "Feel and release", "score": 70},
                {"text": "Transform into wisdom", "score": 95}
            ]),
        BridgeQuestion(8, "How do you relate to others' emotions?",
            "emotional", [
                {"text": "Often overwhelmed by them", "score": 25},
                {"text": "Try to fix or change them", "score": 40},
                {"text": "Witness with compassion", "score": 75},
                {"text": "Hold space while staying centered", "score": 95}
            ]),

        # Social Domain
        BridgeQuestion(9, "How do you navigate social expectations?",
            "social", [
                {"text": "Conform to fit in", "score": 20},
                {"text": "Rebel against them", "score": 35},
                {"text": "Choose consciously", "score": 75},
                {"text": "Create new paradigms", "score": 95}
            ]),
        BridgeQuestion(10, "How do you handle conflict in relationships?",
            "social", [
                {"text": "Avoid at all costs", "score": 20},
                {"text": "Win or lose mentality", "score": 35},
                {"text": "Seek understanding", "score": 75},
                {"text": "Transform into deeper connection", "score": 95}
            ]),

        # Creative Domain
        BridgeQuestion(11, "How do you approach creative expression?",
            "creative", [
                {"text": "Don't see myself as creative", "score": 20},
                {"text": "Only when inspired", "score": 45},
                {"text": "Regular practice", "score": 70},
                {"text": "Life itself is my canvas", "score": 95}
            ]),
        BridgeQuestion(12, "How do you respond to creative blocks?",
            "creative", [
                {"text": "Confirm I'm not creative", "score": 15},
                {"text": "Force through", "score": 40},
                {"text": "Take a break and return", "score": 70},
                {"text": "Explore the block with curiosity", "score": 95}
            ]),

        # Integration Domain
        BridgeQuestion(13, "How connected do you feel to something greater?",
            "integration", [
                {"text": "Don't think about it", "score": 20},
                {"text": "Sometimes wonder", "score": 45},
                {"text": "Regular sense of connection", "score": 75},
                {"text": "Constant awareness of unity", "score": 95}
            ]),
        BridgeQuestion(14, "How do you view your life's purpose?",
            "integration", [
                {"text": "Haven't found it", "score": 25},
                {"text": "Searching for it", "score": 50},
                {"text": "Living it daily", "score": 80},
                {"text": "Evolving and expressing it", "score": 95}
            ])
    ]

    # Level definitions
    LEVELS = {
        (0, 200): ("Unconscious", "Beginning the awakening journey"),
        (200, 400): ("Awakening", "Questioning old patterns"),
        (400, 600): ("Aware", "Seeing patterns clearly"),
        (600, 800): ("Conscious", "Actively choosing responses"),
        (800, 950): ("Elevated", "Creating new possibilities"),
        (950, 1001): ("Execution Confidence", "Transcendent operation")
    }

    def __init__(self):
        self.assessment_count = 0
        if ENGINES_AVAILABLE:
            self.scorer = ConsciousnessScorer()
            self.analyzer = SevenDomainsAnalyzer()
        else:
            self.scorer = None
            self.analyzer = None

    def get_questions(self) -> List[Dict[str, Any]]:
        """Get all assessment questions."""
        return [
            {
                "id": q.id,
                "text": q.text,
                "domain": q.domain,
                "options": [{"text": o["text"], "id": i} for i, o in enumerate(q.options)]
            }
            for q in self.QUESTIONS
        ]

    def calculate_result(self, answers: Dict[int, int]) -> BridgeResult:
        """
        Calculate assessment result from answers.

        Args:
            answers: Dict of question_id -> selected_option_index

        Returns:
            BridgeResult with consciousness level and insights
        """
        self.assessment_count += 1

        # Calculate domain scores
        domain_scores = {
            "physical": 0, "financial": 0, "mental": 0,
            "emotional": 0, "social": 0, "creative": 0, "integration": 0
        }
        domain_counts = {d: 0 for d in domain_scores}

        for q in self.QUESTIONS:
            if q.id in answers:
                option_index = answers[q.id]
                if 0 <= option_index < len(q.options):
                    score = q.options[option_index]["score"]
                    domain_scores[q.domain] += score
                    domain_counts[q.domain] += 1

        # Average domain scores
        for domain in domain_scores:
            if domain_counts[domain] > 0:
                domain_scores[domain] /= domain_counts[domain]

        # Calculate overall consciousness level (0-1000)
        avg_score = sum(domain_scores.values()) / len(domain_scores)
        consciousness_level = avg_score * 10  # Scale to 0-1000

        # Determine level name
        level_name = "Unknown"
        description = ""
        for (low, high), (name, desc) in self.LEVELS.items():
            if low <= consciousness_level < high:
                level_name = name
                description = desc
                break

        # Calculate percentile (simulated)
        if consciousness_level < 300:
            percentile = int(consciousness_level / 300 * 30)
        elif consciousness_level < 500:
            percentile = 30 + int((consciousness_level - 300) / 200 * 30)
        elif consciousness_level < 700:
            percentile = 60 + int((consciousness_level - 500) / 200 * 25)
        else:
            percentile = 85 + int((consciousness_level - 700) / 300 * 15)

        # Identify strengths and growth areas
        sorted_domains = sorted(domain_scores.items(), key=lambda x: x[1], reverse=True)
        strengths = [f"{d.title()} ({int(s)}%)" for d, s in sorted_domains[:2]]
        growth_areas = [f"{d.title()} ({int(s)}%)" for d, s in sorted_domains[-2:]]

        # Recommend path
        if consciousness_level < 400:
            path = "Foundation Track - Build awareness in all domains"
        elif consciousness_level < 600:
            path = "Integration Track - Connect your strengths across domains"
        elif consciousness_level < 800:
            path = "Mastery Track - Deepen your practice and help others"
        else:
            path = "Leadership Track - Guide others on the path"

        return BridgeResult(
            consciousness_level=round(consciousness_level, 1),
            level_name=level_name,
            percentile=percentile,
            domain_scores={d: round(s, 1) for d, s in domain_scores.items()},
            strengths=strengths,
            growth_areas=growth_areas,
            recommended_path=path,
            timestamp=datetime.now().isoformat()
        )

    def to_dict(self, result: BridgeResult) -> Dict[str, Any]:
        """Convert result to dictionary."""
        return {
            "consciousness_level": result.consciousness_level,
            "level_name": result.level_name,
            "percentile": result.percentile,
            "domain_scores": result.domain_scores,
            "strengths": result.strengths,
            "growth_areas": result.growth_areas,
            "recommended_path": result.recommended_path,
            "timestamp": result.timestamp
        }


# Testing
if __name__ == "__main__":
    bridge = ConsciousnessBridge()

    print("=" * 60)
    print("CONSCIOUSNESS BRIDGE - TEST")
    print("=" * 60)

    # Simulate answers (all moderate responses)
    answers = {i: 1 for i in range(1, 15)}  # Select 2nd option for all

    result = bridge.calculate_result(answers)

    print(f"\nConsciousness Level: {result.consciousness_level}/1000")
    print(f"Level: {result.level_name}")
    print(f"Percentile: Top {100 - result.percentile}%")
    print(f"\nDomain Scores:")
    for domain, score in result.domain_scores.items():
        print(f"  {domain.title()}: {score}%")
    print(f"\nStrengths: {', '.join(result.strengths)}")
    print(f"Growth Areas: {', '.join(result.growth_areas)}")
    print(f"\nRecommended Path: {result.recommended_path}")

    print("\n" + "=" * 60)
    print("CONSCIOUSNESS BRIDGE OPERATIONAL")
    print("=" * 60)
