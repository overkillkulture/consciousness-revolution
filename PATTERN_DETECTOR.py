#!/usr/bin/env python3
"""
PATTERN DETECTOR
Analyzes text for manipulation patterns across the 7 domains.
Core consciousness tool for manipulation immunity.
"""

import re
import json
from pathlib import Path
from datetime import datetime
from typing import Optional

# Pattern definitions by domain
MANIPULATION_PATTERNS = {
    "gaslighting": {
        "domain": "relationships",
        "severity": "high",
        "indicators": [
            r"you'?re (crazy|imagining|overreacting|too sensitive)",
            r"that never happened",
            r"you'?re making (things|this) up",
            r"i never said that",
            r"you'?re remembering (it )?wrong",
            r"no one else (thinks|feels|sees) that",
            r"you'?re being paranoid",
            r"it was just a joke"
        ],
        "description": "Making someone question their reality or memory"
    },
    "love_bombing": {
        "domain": "relationships",
        "severity": "medium",
        "indicators": [
            r"you'?re the only one who understands",
            r"i'?ve never felt this way",
            r"we'?re (soul ?mates|meant to be)",
            r"you'?re (perfect|amazing|incredible)",
            r"i can'?t live without you",
            r"let'?s (move in|get married) (right away|immediately)"
        ],
        "description": "Overwhelming affection to gain control"
    },
    "guilt_tripping": {
        "domain": "relationships",
        "severity": "medium",
        "indicators": [
            r"after (all|everything) i'?ve done",
            r"you owe me",
            r"if you (really )?loved me",
            r"i (sacrificed|gave up) everything",
            r"you'?re (so )?selfish",
            r"you never think about (me|my feelings)"
        ],
        "description": "Using guilt to control behavior"
    },
    "triangulation": {
        "domain": "relationships",
        "severity": "high",
        "indicators": [
            r"(everyone|they all) (agrees?|thinks?|says?)",
            r"(name) said you",
            r"(name) would never",
            r"other people think you",
            r"i talked to .+ and they said",
            r"you should be more like"
        ],
        "description": "Using third parties to manipulate"
    },
    "fear_mongering": {
        "domain": "media",
        "severity": "high",
        "indicators": [
            r"(crisis|disaster|emergency|catastrophe)",
            r"you (must|need to) act (now|immediately)",
            r"before it'?s too late",
            r"(threat|danger) to (your|our)",
            r"they'?re coming for",
            r"this could (destroy|ruin|end)"
        ],
        "description": "Using fear to control perception"
    },
    "scarcity_pressure": {
        "domain": "finance",
        "severity": "medium",
        "indicators": [
            r"limited (time|offer|availability)",
            r"only \d+ left",
            r"act (now|fast|quickly)",
            r"don'?t miss (out|this)",
            r"once in a lifetime",
            r"expires (soon|today|tonight)"
        ],
        "description": "Creating artificial urgency"
    },
    "authority_abuse": {
        "domain": "authority",
        "severity": "high",
        "indicators": [
            r"(experts?|scientists?|doctors?) (say|agree|confirm)",
            r"studies (show|prove)",
            r"it'?s (the law|required|mandatory)",
            r"you (have to|must) comply",
            r"because i said so",
            r"i'?m (your|the) (boss|authority)"
        ],
        "description": "Misusing authority for compliance"
    },
    "victim_playing": {
        "domain": "self",
        "severity": "medium",
        "indicators": [
            r"poor me",
            r"nothing (ever )?goes (right|my way)",
            r"everyone (always )?(hates|leaves|hurts) me",
            r"i (can'?t|never) (catch|get) a break",
            r"why does this always happen to me",
            r"i'?m the (real )?victim"
        ],
        "description": "Using victimhood to avoid accountability"
    },
    "future_faking": {
        "domain": "relationships",
        "severity": "medium",
        "indicators": [
            r"(soon|one day|eventually) (we'?ll|i'?ll)",
            r"i promise (i'?ll|to|we'?ll)",
            r"just (wait|be patient)",
            r"things will (get|be) better",
            r"next (time|month|year)",
            r"when i (get|have|finish)"
        ],
        "description": "Making promises with no intention to keep"
    },
    "silent_treatment": {
        "domain": "relationships",
        "severity": "high",
        "indicators": [
            r"i'?m not (talking|speaking) to you",
            r"you know what you did",
            r"figure it out yourself",
            r"i don'?t want to discuss",
            r"talk to the hand",
            r"whatever"
        ],
        "description": "Withdrawing communication as punishment"
    }
}

class PatternDetector:
    """Detect manipulation patterns in text."""

    def __init__(self):
        self.patterns = MANIPULATION_PATTERNS
        self.detection_history = []

    def analyze(self, text: str) -> dict:
        """
        Analyze text for manipulation patterns.

        Returns:
            Dict with detected patterns, scores, and recommendations
        """
        text_lower = text.lower()
        detections = []
        domain_scores = {domain: 0 for domain in [
            "media", "relationships", "finance", "authority", "self", "groups", "digital"
        ]}

        # Check each pattern
        for pattern_name, pattern_data in self.patterns.items():
            matches = []

            for indicator in pattern_data["indicators"]:
                found = re.findall(indicator, text_lower, re.IGNORECASE)
                if found:
                    matches.extend(found)

            if matches:
                severity_scores = {"low": 1, "medium": 2, "high": 3}
                score = severity_scores.get(pattern_data["severity"], 1) * len(matches)

                detection = {
                    "pattern": pattern_name,
                    "domain": pattern_data["domain"],
                    "severity": pattern_data["severity"],
                    "matches": len(matches),
                    "examples": matches[:3],  # First 3 examples
                    "description": pattern_data["description"],
                    "score": score
                }
                detections.append(detection)

                # Update domain score
                domain_scores[pattern_data["domain"]] += score

        # Calculate overall manipulation score
        total_score = sum(d["score"] for d in detections)
        max_possible = len(self.patterns) * 3 * 3  # All patterns, high severity, 3 matches

        # Determine threat level
        if total_score == 0:
            threat_level = "clean"
        elif total_score < 5:
            threat_level = "low"
        elif total_score < 15:
            threat_level = "medium"
        else:
            threat_level = "high"

        result = {
            "timestamp": datetime.now().isoformat(),
            "text_length": len(text),
            "detections": sorted(detections, key=lambda x: x["score"], reverse=True),
            "domain_scores": domain_scores,
            "total_score": total_score,
            "threat_level": threat_level,
            "patterns_detected": len(detections),
            "recommendations": self._generate_recommendations(detections, threat_level)
        }

        # Store in history
        self.detection_history.append(result)

        return result

    def _generate_recommendations(self, detections: list, threat_level: str) -> list:
        """Generate actionable recommendations based on detections."""
        recommendations = []

        if threat_level == "clean":
            recommendations.append("No manipulation patterns detected. Text appears clean.")
            return recommendations

        if threat_level == "high":
            recommendations.append("HIGH ALERT: Multiple manipulation patterns detected. Exercise extreme caution.")

        # Pattern-specific recommendations
        pattern_names = [d["pattern"] for d in detections]

        if "gaslighting" in pattern_names:
            recommendations.append("Document everything. Trust your memory. Seek external validation.")

        if "love_bombing" in pattern_names:
            recommendations.append("Slow down. Healthy relationships develop gradually. Watch for control tactics.")

        if "guilt_tripping" in pattern_names:
            recommendations.append("You are not responsible for others' emotions. Set clear boundaries.")

        if "fear_mongering" in pattern_names:
            recommendations.append("Verify claims independently. Fear is used to bypass critical thinking.")

        if "scarcity_pressure" in pattern_names:
            recommendations.append("Artificial urgency is a sales tactic. Take time to decide.")

        if "authority_abuse" in pattern_names:
            recommendations.append("Question credentials. True authority welcomes scrutiny.")

        if "victim_playing" in pattern_names:
            recommendations.append("Empathy is good but don't let it override accountability.")

        return recommendations

    def quick_check(self, text: str) -> str:
        """Quick one-line assessment."""
        result = self.analyze(text)
        return f"{result['threat_level'].upper()}: {result['patterns_detected']} patterns, score {result['total_score']}"

    def get_domain_report(self, text: str) -> dict:
        """Get breakdown by domain."""
        result = self.analyze(text)

        report = {
            "overall": result["threat_level"],
            "domains": {}
        }

        for domain, score in result["domain_scores"].items():
            if score > 0:
                if score >= 6:
                    level = "high"
                elif score >= 3:
                    level = "medium"
                else:
                    level = "low"

                report["domains"][domain] = {
                    "score": score,
                    "level": level
                }

        return report

def demo():
    """Demonstrate pattern detection."""
    print("=" * 50)
    print("PATTERN DETECTOR DEMO")
    print("=" * 50)

    detector = PatternDetector()

    # Test texts
    tests = [
        # Clean text
        "I appreciate your help with the project. Let me know if you need anything.",

        # Gaslighting
        "You're crazy if you think that happened. You're always imagining things and being too sensitive.",

        # Scarcity + Authority
        "Experts agree you must act now! Only 3 left and this limited time offer expires tonight!",

        # Multiple patterns
        "After everything I've sacrificed for you, you're being so selfish. Everyone thinks so. You should be more like Sarah. If you really loved me, you'd do this. Poor me, nothing ever goes right.",
    ]

    for i, text in enumerate(tests, 1):
        print(f"\n{'='*50}")
        print(f"TEST {i}")
        print(f"{'='*50}")
        print(f"Text: {text[:100]}...")

        result = detector.analyze(text)

        print(f"\nThreat Level: {result['threat_level'].upper()}")
        print(f"Score: {result['total_score']}")
        print(f"Patterns Detected: {result['patterns_detected']}")

        if result['detections']:
            print("\nDetections:")
            for d in result['detections']:
                print(f"  - {d['pattern']} ({d['severity']}): {d['matches']} matches")
                print(f"    Domain: {d['domain']}")
                if d['examples']:
                    print(f"    Examples: {d['examples']}")

        if result['recommendations']:
            print("\nRecommendations:")
            for rec in result['recommendations']:
                print(f"  • {rec}")

    # Domain report for last test
    print(f"\n{'='*50}")
    print("DOMAIN BREAKDOWN (Test 4)")
    print(f"{'='*50}")

    domain_report = detector.get_domain_report(tests[-1])
    print(f"Overall: {domain_report['overall']}")
    for domain, data in domain_report['domains'].items():
        print(f"  {domain}: {data['level']} (score: {data['score']})")

if __name__ == "__main__":
    demo()
