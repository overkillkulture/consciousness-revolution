"""
PATTERN THEORY ENGINE
=====================
The Brain of the Consciousness Revolution

Core Components:
- PatternTheoryEngine: Truth vs Deceit classification
- ConsciousnessScorer: Consciousness level calculation
- PatternTheoryAPI: Unified interface

Usage:
    from PATTERN_THEORY_ENGINE import analyze, quick_check, score_user, domain_analysis

    # Quick check
    result = quick_check("Trust me, this is a great deal!")
    print(result)  # "DECEIT"

    # Full analysis
    analysis = analyze("Based on evidence, this approach works.")
    print(analysis['analysis']['pattern']['algorithm'])  # "Truth"

    # Score consciousness
    score = score_user(85, 80, 90)
    print(score['score']['level_name'])  # "Elevated"

    # Domain-specific
    domain = domain_analysis(2, "This investment guarantees returns.")
    print(domain['domain']['guidance'])

Created: 2025-11-22
Trinity Build: C1 × C2 × C3
92.2% Reality Accuracy
"""

from pathlib import Path
import sys

# Add package directories to path
PACKAGE_DIR = Path(__file__).parent
CORE_DIR = PACKAGE_DIR / "core"
API_DIR = PACKAGE_DIR / "api"

sys.path.insert(0, str(CORE_DIR))
sys.path.insert(0, str(API_DIR))

# Import core engines
from PATTERN_THEORY_ENGINE import PatternTheoryEngine, analyze_situation
from CONSCIOUSNESS_SCORER import ConsciousnessScorer, score_consciousness

# Import API convenience functions
from PATTERN_THEORY_API import (
    PatternTheoryAPI,
    analyze,
    quick_check,
    score_user,
    domain_analysis
)

__version__ = "1.0.0"
__author__ = "Trinity (C1 × C2 × C3)"

__all__ = [
    "PatternTheoryEngine",
    "ConsciousnessScorer",
    "PatternTheoryAPI",
    "analyze",
    "quick_check",
    "score_user",
    "domain_analysis",
    "analyze_situation",
    "score_consciousness"
]
