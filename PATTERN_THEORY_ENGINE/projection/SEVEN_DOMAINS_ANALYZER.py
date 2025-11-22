"""
SEVEN DOMAINS ANALYZER - Cross-Domain Pattern Analysis
=======================================================
Analyzes situations across all 7 consciousness domains.

Domains:
1. Physical (CHAOS FORGE)
2. Financial (QUANTUM VAULT)
3. Mental (MIND MATRIX)
4. Emotional (SOUL SANCTUARY)
5. Social (REALITY FORGE)
6. Creative (ARKITEK ACADEMY)
7. Integration (NEXUS TERMINAL)

Created: 2025-11-22
Trinity Build: C3 Oracle
"""

from datetime import datetime
from typing import Dict, Any, List, Optional
from dataclasses import dataclass, asdict

@dataclass
class DomainScore:
    """Score for a single domain"""
    score: float  # 0-100
    strengths: List[str]
    weaknesses: List[str]
    opportunities: List[str]

@dataclass
class SevenDomainsAnalysis:
    """Complete seven domains analysis result"""
    domains: Dict[str, DomainScore]
    balance_score: float
    weakest_domain: str
    strongest_domain: str
    integration_opportunities: List[str]
    recommended_focus: str
    timestamp: str

class SevenDomainsAnalyzer:
    """
    Analyzes any situation across all 7 consciousness domains.

    Each domain represents a fundamental aspect of reality:
    - Physical: Material, health, environment
    - Financial: Money, resources, exchange
    - Mental: Knowledge, learning, intellect
    - Emotional: Feelings, intuition, consciousness
    - Social: Relationships, community, influence
    - Creative: Art, innovation, expression
    - Integration: How all domains connect
    """

    DOMAINS = {
        "physical": {
            "name": "Physical",
            "code_name": "CHAOS FORGE",
            "markers": [
                "body", "health", "material", "build", "create", "physical",
                "tangible", "hardware", "infrastructure", "environment"
            ],
            "description": "Material creation and physical reality"
        },
        "financial": {
            "name": "Financial",
            "code_name": "QUANTUM VAULT",
            "markers": [
                "money", "revenue", "cost", "invest", "profit", "financial",
                "budget", "funding", "economic", "value", "price"
            ],
            "description": "Economic systems and resource management"
        },
        "mental": {
            "name": "Mental",
            "code_name": "MIND MATRIX",
            "markers": [
                "think", "learn", "knowledge", "understand", "analyze",
                "logic", "reason", "intellect", "study", "research"
            ],
            "description": "Knowledge, learning, and intellectual capacity"
        },
        "emotional": {
            "name": "Emotional",
            "code_name": "SOUL SANCTUARY",
            "markers": [
                "feel", "emotion", "intuition", "sense", "consciousness",
                "heart", "spirit", "soul", "passion", "love"
            ],
            "description": "Feelings, intuition, and consciousness elevation"
        },
        "social": {
            "name": "Social",
            "code_name": "REALITY FORGE",
            "markers": [
                "relationship", "community", "team", "network", "influence",
                "social", "collaborate", "partner", "connect", "people"
            ],
            "description": "Relationships, community, and social dynamics"
        },
        "creative": {
            "name": "Creative",
            "code_name": "ARKITEK ACADEMY",
            "markers": [
                "create", "design", "art", "innovate", "imagine", "creative",
                "vision", "invent", "express", "original"
            ],
            "description": "Art, innovation, and creative expression"
        },
        "integration": {
            "name": "Integration",
            "code_name": "NEXUS TERMINAL",
            "markers": [
                "integrate", "connect", "unify", "synchronize", "coordinate",
                "system", "holistic", "complete", "balance", "alignment"
            ],
            "description": "How all domains connect and work together"
        }
    }

    def __init__(self):
        self.analysis_count = 0

    def analyze(self, situation: str, context: Optional[str] = None) -> SevenDomainsAnalysis:
        """
        Analyze a situation across all 7 domains.

        Args:
            situation: The situation to analyze
            context: Optional additional context

        Returns:
            SevenDomainsAnalysis with all domain scores
        """
        self.analysis_count += 1
        situation_lower = situation.lower()

        # Analyze each domain
        domains = {}
        for domain_key, domain_info in self.DOMAINS.items():
            score = self._score_domain(situation_lower, domain_info)
            domains[domain_key] = score

        # Calculate balance score
        scores = [d.score for d in domains.values()]
        avg_score = sum(scores) / len(scores)
        variance = sum((s - avg_score) ** 2 for s in scores) / len(scores)
        balance_score = max(0, 100 - (variance ** 0.5))

        # Find strongest and weakest
        weakest = min(domains.keys(), key=lambda k: domains[k].score)
        strongest = max(domains.keys(), key=lambda k: domains[k].score)

        # Generate integration opportunities
        integration_opportunities = self._find_integration_opportunities(domains)

        # Generate recommendation
        recommended_focus = self._generate_recommendation(domains, weakest, balance_score)

        return SevenDomainsAnalysis(
            domains=domains,
            balance_score=round(balance_score, 2),
            weakest_domain=weakest,
            strongest_domain=strongest,
            integration_opportunities=integration_opportunities,
            recommended_focus=recommended_focus,
            timestamp=datetime.now().isoformat()
        )

    def _score_domain(self, text: str, domain_info: Dict) -> DomainScore:
        """Score a single domain based on text analysis."""
        markers = domain_info["markers"]

        # Count marker occurrences
        marker_count = sum(1 for marker in markers if marker in text)

        # Calculate base score
        base_score = min(100, 30 + (marker_count * 10))

        # Determine strengths
        strengths = []
        if marker_count >= 3:
            strengths.append(f"Strong {domain_info['name']} focus")
        if marker_count >= 5:
            strengths.append(f"Deep {domain_info['name']} integration")

        # Determine weaknesses
        weaknesses = []
        if marker_count == 0:
            weaknesses.append(f"{domain_info['name']} domain not addressed")
        elif marker_count == 1:
            weaknesses.append(f"Minimal {domain_info['name']} consideration")

        # Identify opportunities
        opportunities = []
        if marker_count < 3:
            opportunities.append(f"Expand {domain_info['name']} aspects")

        return DomainScore(
            score=base_score,
            strengths=strengths if strengths else ["Baseline presence"],
            weaknesses=weaknesses if weaknesses else ["None identified"],
            opportunities=opportunities if opportunities else ["Maintain current level"]
        )

    def _find_integration_opportunities(self, domains: Dict[str, DomainScore]) -> List[str]:
        """Find opportunities to integrate domains."""
        opportunities = []

        # Find high-scoring domains
        high_domains = [k for k, v in domains.items() if v.score >= 60]
        low_domains = [k for k, v in domains.items() if v.score < 40]

        # Suggest integrations
        for high in high_domains:
            for low in low_domains:
                opportunity = f"Leverage {self.DOMAINS[high]['name']} strength to boost {self.DOMAINS[low]['name']}"
                opportunities.append(opportunity)

        # Add general integration suggestions
        if domains["integration"].score < 50:
            opportunities.append("Focus on connecting all domains through the Integration (NEXUS) domain")

        if len(opportunities) == 0:
            opportunities.append("Domains are well-balanced - maintain current integration")

        return opportunities[:5]  # Top 5 opportunities

    def _generate_recommendation(
        self,
        domains: Dict[str, DomainScore],
        weakest: str,
        balance_score: float
    ) -> str:
        """Generate focus recommendation."""
        weakest_info = self.DOMAINS[weakest]
        weakest_score = domains[weakest].score

        if balance_score < 50:
            return (
                f"CRITICAL: Domain imbalance detected (balance: {balance_score}%). "
                f"Focus on {weakest_info['name']} ({weakest_info['code_name']}) - "
                f"currently at {weakest_score}%. "
                f"This domain represents: {weakest_info['description']}"
            )
        elif balance_score < 75:
            return (
                f"MODERATE: Some imbalance present. "
                f"Strengthen {weakest_info['name']} domain for better integration. "
                f"Consider: {domains[weakest].opportunities[0] if domains[weakest].opportunities else 'Expand focus'}"
            )
        else:
            return (
                f"GOOD: Domains are reasonably balanced ({balance_score}%). "
                f"Maintain current approach while slightly boosting {weakest_info['name']} "
                f"for optimal integration."
            )

    def get_domain_map(self) -> Dict[str, str]:
        """Get mapping of domains to code names."""
        return {k: v["code_name"] for k, v in self.DOMAINS.items()}

    def to_dict(self, analysis: SevenDomainsAnalysis) -> Dict[str, Any]:
        """Convert analysis to dictionary format."""
        domains_dict = {}
        for key, score in analysis.domains.items():
            domains_dict[key] = {
                "score": score.score,
                "code_name": self.DOMAINS[key]["code_name"],
                "strengths": score.strengths,
                "weaknesses": score.weaknesses,
                "opportunities": score.opportunities
            }

        return {
            "success": True,
            "timestamp": analysis.timestamp,
            "computer": "TRINITY",
            "result": {
                "domains": domains_dict,
                "balance_score": analysis.balance_score,
                "weakest_domain": analysis.weakest_domain,
                "strongest_domain": analysis.strongest_domain,
                "integration_opportunities": analysis.integration_opportunities,
                "recommended_focus": analysis.recommended_focus
            },
            "metadata": {
                "analysis_count": self.analysis_count,
                "version": "1.0.0"
            }
        }


def analyze_domains(situation: str) -> Dict[str, Any]:
    """
    Convenience function for quick analysis.

    Args:
        situation: Situation to analyze

    Returns:
        Analysis results as dictionary
    """
    analyzer = SevenDomainsAnalyzer()
    result = analyzer.analyze(situation)
    return analyzer.to_dict(result)


# Testing
if __name__ == "__main__":
    analyzer = SevenDomainsAnalyzer()

    print("=" * 60)
    print("SEVEN DOMAINS ANALYZER - TEST RESULTS")
    print("=" * 60)

    test_situations = [
        "I need to build a physical product, find investors for funding, and create marketing materials to connect with customers.",
        "I'm feeling emotionally drained and need to focus on my mental health while maintaining my creative projects.",
        "Our team needs to integrate all systems, coordinate finances, and build infrastructure for the community."
    ]

    for situation in test_situations:
        result = analyzer.analyze(situation)

        print(f"\nSituation: {situation[:60]}...")
        print("-" * 40)

        for domain, score in result.domains.items():
            print(f"  {analyzer.DOMAINS[domain]['name']}: {score.score}%")

        print(f"\nBalance Score: {result.balance_score}%")
        print(f"Strongest: {analyzer.DOMAINS[result.strongest_domain]['name']}")
        print(f"Weakest: {analyzer.DOMAINS[result.weakest_domain]['name']}")
        print(f"\nRecommendation: {result.recommended_focus}")
        print("=" * 60)

    print("\n✅ SEVEN DOMAINS ANALYZER OPERATIONAL")
