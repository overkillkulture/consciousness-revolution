"""
CRYPTO PATTERN DETECTOR - Manipulation Detection for Crypto Markets
====================================================================
Applies Pattern Theory to cryptocurrency market analysis

Built by: CP1C2 (Cloud)
Date: 2025-11-23
Based on: PATTERN_THEORY_ENGINE
"""

import json
from datetime import datetime
from typing import Dict, List, Any
from dataclasses import dataclass, asdict

@dataclass
class CryptoPatternAnalysis:
    """Analysis of crypto-related text/behavior"""
    manipulation_score: float
    legitimacy_score: float
    pattern_type: str
    warning_signals: List[str]
    recommendation: str
    confidence: float
    timestamp: str

class CryptoPatternDetector:
    """
    Detects manipulation patterns in crypto markets, social media, and announcements.

    Based on Pattern Theory principles adapted for cryptocurrency.
    """

    # Manipulation markers (crypto-specific)
    MANIPULATION_MARKERS = [
        # Pump & Dump
        "moon", "mooning", "10x", "100x", "1000x", "lambo", "🚀", "🌙",
        "guaranteed", "can't lose", "sure thing", "next bitcoin",

        # FOMO creation
        "last chance", "don't miss", "fomo", "limited", "exclusive",
        "get in now", "won't last", "running out", "hurry",

        # False authority
        "trust me bro", "insider info", "whale alert", "whales are buying",
        "smart money", "institutions loading", "hidden gem",

        # Urgency manipulation
        "urgent", "right now", "immediately", "asap", "quick",
        "before it's too late", "window closing", "act fast",

        # Social proof manipulation
        "everyone is buying", "massive demand", "going viral",
        "trending", "fomo is real", "don't be left behind",

        # Vague promises
        "huge announcement", "major partnership", "game changer",
        "revolutionary", "disrupting", "paradigm shift"
    ]

    # Legitimacy markers
    LEGITIMACY_MARKERS = [
        # Rational analysis
        "data shows", "chart indicates", "volume analysis", "fundamentals",
        "market cap", "tokenomics", "whitepaper", "roadmap",

        # Honest communication
        "in my opinion", "i think", "could be", "might", "possibly",
        "not financial advice", "dyor", "do your research", "risk",

        # Technical detail
        "blockchain", "consensus", "smart contract", "protocol",
        "github", "audit", "open source", "transparent",

        # Measured language
        "long-term", "sustainable", "gradual", "accumulation",
        "fundamentals", "utility", "adoption", "development"
    ]

    # Warning patterns
    WARNING_PATTERNS = [
        ("promise returns", "Guaranteed profit claims"),
        ("no risk", "False safety assurance"),
        ("insider", "Unverifiable information"),
        ("urgent + buy", "Pressure to act immediately"),
        ("100x", "Unrealistic expectations"),
        ("whale + buy", "False social proof"),
        ("hidden gem", "Manufactured scarcity")
    ]

    def __init__(self):
        self.analysis_count = 0

    def analyze(self, text: str, context: str = "social_media") -> CryptoPatternAnalysis:
        """
        Analyze crypto-related text for manipulation patterns.

        Args:
            text: The text to analyze (tweet, announcement, message, etc.)
            context: Where the text came from (social_media, official, news)

        Returns:
            CryptoPatternAnalysis with detection results
        """
        self.analysis_count += 1

        text_lower = text.lower()

        # Count markers
        manip_count = sum(1 for marker in self.MANIPULATION_MARKERS if marker in text_lower)
        legit_count = sum(1 for marker in self.LEGITIMACY_MARKERS if marker in text_lower)

        # Detect warning patterns
        warnings = []
        for keywords, warning in self.WARNING_PATTERNS:
            if all(word in text_lower for word in keywords.split(" + ")):
                warnings.append(warning)
            elif keywords in text_lower:
                warnings.append(warning)

        # Calculate scores
        total_markers = manip_count + legit_count
        if total_markers == 0:
            manipulation_score = 50.0
            legitimacy_score = 50.0
        else:
            manipulation_score = (manip_count / total_markers) * 100
            legitimacy_score = (legit_count / total_markers) * 100

        # Warning signals add to manipulation score
        warning_penalty = len(warnings) * 15
        manipulation_score = min(100, manipulation_score + warning_penalty)
        legitimacy_score = max(0, legitimacy_score - warning_penalty)

        # Normalize
        total = manipulation_score + legitimacy_score
        if total > 0:
            manipulation_score = (manipulation_score / total) * 100
            legitimacy_score = (legitimacy_score / total) * 100

        # Classify pattern
        pattern_type = self._classify_pattern(manipulation_score, warnings)

        # Generate recommendation
        recommendation = self._generate_recommendation(manipulation_score, warnings)

        # Calculate confidence
        confidence = abs(manipulation_score - legitimacy_score) / 100

        return CryptoPatternAnalysis(
            manipulation_score=round(manipulation_score, 2),
            legitimacy_score=round(legitimacy_score, 2),
            pattern_type=pattern_type,
            warning_signals=warnings,
            recommendation=recommendation,
            confidence=round(confidence, 3),
            timestamp=datetime.now().isoformat()
        )

    def _classify_pattern(self, manip_score: float, warnings: List[str]) -> str:
        """Classify the type of pattern detected."""
        if manip_score > 80:
            return "LIKELY SCAM - High manipulation detected"
        elif manip_score > 60:
            return "PUMP & DUMP - Classic manipulation"
        elif manip_score > 40:
            return "FOMO CREATION - Emotional manipulation"
        elif len(warnings) >= 3:
            return "MULTIPLE RED FLAGS - Proceed with caution"
        elif manip_score > 20:
            return "MILD HYPE - Some marketing language"
        else:
            return "APPEARS LEGITIMATE - Low manipulation signals"

    def _generate_recommendation(self, manip_score: float, warnings: List[str]) -> str:
        """Generate action recommendation based on analysis."""
        if manip_score > 80:
            return "🚨 AVOID - Do not engage. Likely scam or manipulation."
        elif manip_score > 60:
            return "⚠️  EXTREME CAUTION - Classic pump & dump patterns detected."
        elif manip_score > 40:
            return "⚠️  RESEARCH DEEPLY - FOMO tactics in use. DYOR required."
        elif len(warnings) >= 3:
            return "⚠️  VERIFY CLAIMS - Multiple red flags present."
        elif manip_score > 20:
            return "ℹ️  NORMAL MARKETING - Typical crypto hype. Still do research."
        else:
            return "✅ APPEARS SOUND - Low manipulation. Still verify fundamentals."

    def analyze_batch(self, texts: List[str]) -> List[CryptoPatternAnalysis]:
        """Analyze multiple texts at once."""
        return [self.analyze(text) for text in texts]

    def get_stats(self) -> Dict[str, Any]:
        """Get detector statistics."""
        return {
            "total_analyses": self.analysis_count,
            "detector_version": "1.0",
            "pattern_theory_based": True
        }


# CLI usage
if __name__ == "__main__":
    detector = CryptoPatternDetector()

    # Test examples
    test_texts = [
        "🚀🌙 This coin is going to 100x! Get in now before it's too late! Trust me bro!",
        "Interesting project with solid fundamentals. Whitepaper looks good. DYOR as always.",
        "URGENT! Whales are loading up! This is your last chance! Don't miss the moon!",
        "Long-term hold. Good tokenomics and active development. Not financial advice."
    ]

    print("CRYPTO PATTERN DETECTOR - Test Results\\n")
    for i, text in enumerate(test_texts, 1):
        result = detector.analyze(text)
        print(f"Test {i}: {text[:50]}...")
        print(f"Manipulation: {result.manipulation_score}%")
        print(f"Pattern: {result.pattern_type}")
        print(f"Recommendation: {result.recommendation}")
        print(f"Warnings: {', '.join(result.warning_signals) if result.warning_signals else 'None'}")
        print()
