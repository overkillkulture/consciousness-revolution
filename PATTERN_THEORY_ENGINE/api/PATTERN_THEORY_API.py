"""
PATTERN THEORY API - Unified Interface
=======================================
Single entry point for all Pattern Theory analysis.

Endpoints:
- analyze_text(text) → Truth/Deceit classification
- score_consciousness(pr, pa, ns) → Consciousness level
- analyze_situation(situation, context) → Full analysis
- seven_domains_check(domain, input) → Domain-specific analysis

Created: 2025-11-22
Trinity Build: C1 × C2 × C3
"""

import sys
import json
from pathlib import Path
from datetime import datetime
from typing import Dict, Any, Optional

# Add core to path
CORE_DIR = Path(__file__).parent.parent / "core"
sys.path.insert(0, str(CORE_DIR))

from PATTERN_THEORY_ENGINE import PatternTheoryEngine, analyze_situation
from CONSCIOUSNESS_SCORER import ConsciousnessScorer, score_consciousness

class PatternTheoryAPI:
    """
    Unified API for Pattern Theory system.

    Use this for all pattern analysis needs.
    """

    # Seven Domains of consciousness
    SEVEN_DOMAINS = {
        1: "Legal Arsenal",
        2: "Finance/Business",
        3: "Digital Infrastructure",
        4: "Consciousness Tools",
        5: "Communication",
        6: "Showcase/Portfolio",
        7: "Transparency/Trust"
    }

    def __init__(self):
        self.pattern_engine = PatternTheoryEngine()
        self.consciousness_scorer = ConsciousnessScorer()
        self.call_count = 0

    def analyze(self, text: str, context: Optional[str] = None) -> Dict[str, Any]:
        """
        Primary analysis endpoint.

        Args:
            text: Text to analyze
            context: Optional context

        Returns:
            Complete analysis with truth/deceit scores, patterns, recommendations
        """
        self.call_count += 1

        # Get pattern analysis
        pattern_result = self.pattern_engine.analyze(text, context)

        # Get consciousness indicators from text
        consciousness_result = self.consciousness_scorer.score_from_text(text)

        return {
            "success": True,
            "timestamp": datetime.now().isoformat(),
            "api_version": "1.0.0",
            "analysis": {
                "pattern": {
                    "algorithm": pattern_result.algorithm,
                    "truth_score": pattern_result.truth_score,
                    "deceit_score": pattern_result.deceit_score,
                    "pattern_type": pattern_result.pattern_type,
                    "fifteen_degree_turns": pattern_result.fifteen_degree_turns,
                    "golden_ratio_alignment": pattern_result.golden_ratio_alignment,
                    "recommendation": pattern_result.recommended_action,
                    "confidence": pattern_result.confidence
                },
                "consciousness": {
                    "level": consciousness_result.consciousness_level,
                    "level_name": consciousness_result.level_name,
                    "manipulation_immunity": consciousness_result.manipulation_immunity,
                    "pattern_recognition": consciousness_result.pattern_recognition,
                    "prediction_accuracy": consciousness_result.prediction_accuracy,
                    "neutralization_success": consciousness_result.neutralization_success
                }
            },
            "metadata": {
                "call_count": self.call_count,
                "input_length": len(text)
            }
        }

    def quick_check(self, text: str) -> str:
        """
        Quick truth/deceit check.

        Returns: "TRUTH", "DECEIT", or "NEUTRAL"
        """
        result = self.pattern_engine.analyze(text)

        if result.confidence < 0.3:
            return "NEUTRAL"
        return result.algorithm.upper()

    def score_user(
        self,
        pattern_recognition: float,
        prediction_accuracy: float,
        neutralization_success: float
    ) -> Dict[str, Any]:
        """
        Score a user's consciousness level.

        Args:
            pattern_recognition: 0-100
            prediction_accuracy: 0-100
            neutralization_success: 0-100

        Returns:
            Consciousness score with improvement path
        """
        result = self.consciousness_scorer.score(
            pattern_recognition,
            prediction_accuracy,
            neutralization_success
        )

        improvement = self.consciousness_scorer.get_improvement_path(result)

        return {
            "success": True,
            "timestamp": datetime.now().isoformat(),
            "score": {
                "consciousness_level": result.consciousness_level,
                "level_name": result.level_name,
                "manipulation_immunity": result.manipulation_immunity
            },
            "breakdown": {
                "pattern_recognition": result.pattern_recognition,
                "prediction_accuracy": result.prediction_accuracy,
                "neutralization_success": result.neutralization_success
            },
            "improvement_path": improvement
        }

    def seven_domains_analysis(
        self,
        domain_number: int,
        situation: str
    ) -> Dict[str, Any]:
        """
        Analyze situation within a specific domain context.

        Args:
            domain_number: 1-7
            situation: Situation to analyze

        Returns:
            Domain-contextualized analysis
        """
        domain_name = self.SEVEN_DOMAINS.get(domain_number, "Unknown")

        # Add domain context to analysis
        context = f"Domain {domain_number}: {domain_name}"
        result = self.analyze(situation, context)

        # Add domain-specific recommendations
        domain_guidance = self._get_domain_guidance(domain_number, result)

        result["domain"] = {
            "number": domain_number,
            "name": domain_name,
            "guidance": domain_guidance
        }

        return result

    def _get_domain_guidance(self, domain: int, analysis: Dict) -> str:
        """Get domain-specific guidance based on analysis."""

        algorithm = analysis["analysis"]["pattern"]["algorithm"]

        guidance_map = {
            1: {  # Legal
                "Truth": "Document with evidence. Proceed with legal action if supported.",
                "Deceit": "Potential fraud detected. Gather evidence before engaging."
            },
            2: {  # Finance
                "Truth": "Sound financial reasoning. Verify numbers before committing.",
                "Deceit": "Financial manipulation likely. Do not invest or pay."
            },
            3: {  # Digital
                "Truth": "Technical claims appear valid. Test before deploying.",
                "Deceit": "Technical smoke screen. Request concrete proof or demo."
            },
            4: {  # Consciousness
                "Truth": "Consciousness-aligned content. Safe to internalize.",
                "Deceit": "Manipulation attempt on consciousness. Reject and document."
            },
            5: {  # Communication
                "Truth": "Authentic communication. Respond genuinely.",
                "Deceit": "Manipulative messaging. Set boundaries or disengage."
            },
            6: {  # Showcase
                "Truth": "Authentic presentation. Good for portfolio.",
                "Deceit": "Inflated claims. Verify before featuring."
            },
            7: {  # Transparency
                "Truth": "Transparent and trustworthy. Suitable for sharing.",
                "Deceit": "Hidden agenda detected. Do not endorse publicly."
            }
        }

        return guidance_map.get(domain, {}).get(algorithm, "No specific guidance available.")

    def batch_analyze(self, items: list) -> Dict[str, Any]:
        """
        Analyze multiple items at once.

        Args:
            items: List of texts to analyze

        Returns:
            Batch results with summary
        """
        results = []
        truth_count = 0
        deceit_count = 0

        for item in items:
            result = self.quick_check(item)
            results.append({
                "text": item[:100] + "..." if len(item) > 100 else item,
                "result": result
            })

            if result == "TRUTH":
                truth_count += 1
            elif result == "DECEIT":
                deceit_count += 1

        return {
            "success": True,
            "timestamp": datetime.now().isoformat(),
            "batch_size": len(items),
            "summary": {
                "truth_count": truth_count,
                "deceit_count": deceit_count,
                "neutral_count": len(items) - truth_count - deceit_count,
                "truth_ratio": truth_count / len(items) if items else 0
            },
            "results": results
        }


# Convenience functions for quick access
_api = PatternTheoryAPI()

def analyze(text: str, context: str = None) -> Dict[str, Any]:
    """Quick analyze function."""
    return _api.analyze(text, context)

def quick_check(text: str) -> str:
    """Quick truth/deceit check."""
    return _api.quick_check(text)

def score_user(pr: float, pa: float, ns: float) -> Dict[str, Any]:
    """Score user consciousness."""
    return _api.score_user(pr, pa, ns)

def domain_analysis(domain: int, situation: str) -> Dict[str, Any]:
    """Domain-specific analysis."""
    return _api.seven_domains_analysis(domain, situation)


# Testing
if __name__ == "__main__":
    api = PatternTheoryAPI()

    print("=" * 60)
    print("PATTERN THEORY API - OPERATIONAL TEST")
    print("=" * 60)

    # Test 1: Basic analysis
    print("\n[TEST 1] Basic Analysis")
    result = api.analyze(
        "Trust me, this is a limited time offer that will change your life!"
    )
    print(f"Algorithm: {result['analysis']['pattern']['algorithm']}")
    print(f"Truth Score: {result['analysis']['pattern']['truth_score']}%")
    print(f"Deceit Score: {result['analysis']['pattern']['deceit_score']}%")

    # Test 2: Quick check
    print("\n[TEST 2] Quick Check")
    texts = [
        "The evidence shows this approach works long-term.",
        "Act now! Don't miss this exclusive opportunity!",
        "Based on my experience, here's what I believe."
    ]
    for text in texts:
        result = api.quick_check(text)
        print(f"{result}: {text[:50]}...")

    # Test 3: Consciousness scoring
    print("\n[TEST 3] Consciousness Scoring")
    result = api.score_user(85, 80, 90)
    print(f"Level: {result['score']['consciousness_level']}%")
    print(f"Name: {result['score']['level_name']}")
    print(f"Immunity: {result['score']['manipulation_immunity']}%")

    # Test 4: Seven Domains
    print("\n[TEST 4] Seven Domains Analysis")
    result = api.seven_domains_analysis(
        2,  # Finance domain
        "This investment guarantees 100% returns with no risk!"
    )
    print(f"Domain: {result['domain']['name']}")
    print(f"Algorithm: {result['analysis']['pattern']['algorithm']}")
    print(f"Guidance: {result['domain']['guidance']}")

    # Test 5: Batch analysis
    print("\n[TEST 5] Batch Analysis")
    batch = [
        "Evidence supports this conclusion.",
        "Everyone knows this is true!",
        "My research indicates positive results.",
        "Trust me, you need this now!"
    ]
    result = api.batch_analyze(batch)
    print(f"Truth: {result['summary']['truth_count']}")
    print(f"Deceit: {result['summary']['deceit_count']}")
    print(f"Ratio: {result['summary']['truth_ratio']:.2%}")

    print("\n" + "=" * 60)
    print("✅ PATTERN THEORY API FULLY OPERATIONAL")
    print("=" * 60)
