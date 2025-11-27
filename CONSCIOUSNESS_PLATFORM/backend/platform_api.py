"""
CONSCIOUSNESS PLATFORM API
============================
Main API for the Consciousness Platform.

Integrates Pattern Theory Engine and all platform features.

Created: 2025-11-22
Phase 3: Consciousness Platform
"""

import sys
from flask import Flask, jsonify, request
from flask_cors import CORS
from datetime import datetime
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Add paths (Railway-compatible)
import os
base_path = os.environ.get("PATTERN_ENGINE_PATH", "/app/PATTERN_THEORY_ENGINE")
sys.path.insert(0, base_path)
sys.path.insert(0, os.path.join(base_path, "core"))
sys.path.insert(0, os.path.join(base_path, "projection"))
sys.path.insert(0, os.path.dirname(__file__))

# Import Pattern Theory Engine
try:
    from PATTERN_THEORY_ENGINE import PatternTheoryEngine
    from CONSCIOUSNESS_SCORER import ConsciousnessScorer
    from MANIPULATION_DETECTOR import ManipulationDetector
    from TIMELINE_PROJECTOR import TimelineProjector
    from SEVEN_DOMAINS_ANALYZER import SevenDomainsAnalyzer
    ENGINES_AVAILABLE = True
except ImportError as e:
    print(f"Warning: Pattern Theory Engine not available: {e}")
    ENGINES_AVAILABLE = False

# Import platform features
from consciousness_bridge import ConsciousnessBridge

# Import auth routes
from auth_routes import auth_bp, init_oauth

app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('JWT_SECRET_KEY', 'change-this-secret-key-in-production')
CORS(app)

# Register auth blueprint
app.register_blueprint(auth_bp)

# Initialize OAuth
init_oauth(app)

# Initialize engines
if ENGINES_AVAILABLE:
    pattern_engine = PatternTheoryEngine()
    consciousness_scorer = ConsciousnessScorer()
    manipulation_detector = ManipulationDetector()
    timeline_projector = TimelineProjector()
    domains_analyzer = SevenDomainsAnalyzer()
else:
    pattern_engine = None
    consciousness_scorer = None
    manipulation_detector = None
    timeline_projector = None
    domains_analyzer = None

# Initialize platform features
consciousness_bridge = ConsciousnessBridge()

# Stats
stats = {
    "assessments_completed": 0,
    "analyses_run": 0,
    "detections_performed": 0
}

# ============= Health & Info =============

@app.route('/health')
def health():
    """Health check endpoint."""
    return jsonify({
        "status": "healthy",
        "service": "Consciousness Platform API",
        "version": "1.0.0",
        "engines_available": ENGINES_AVAILABLE,
        "timestamp": datetime.now().isoformat()
    })

@app.route('/stats')
def get_stats():
    """Get platform statistics."""
    return jsonify({
        "assessments_completed": stats["assessments_completed"],
        "analyses_run": stats["analyses_run"],
        "detections_performed": stats["detections_performed"],
        "bridge_assessments": consciousness_bridge.assessment_count
    })

# ============= Consciousness Bridge =============

@app.route('/api/bridge/questions')
def get_bridge_questions():
    """Get all Consciousness Bridge questions."""
    return jsonify({
        "success": True,
        "questions": consciousness_bridge.get_questions(),
        "total": len(consciousness_bridge.QUESTIONS)
    })

@app.route('/api/bridge/assess', methods=['POST'])
def assess_consciousness():
    """
    Run Consciousness Bridge assessment.

    Request body:
    {
        "answers": {
            "1": 2,  // question_id: selected_option_index
            "2": 1,
            ...
        }
    }
    """
    try:
        data = request.get_json()
        if not data or 'answers' not in data:
            return jsonify({"error": "Missing 'answers' field"}), 400

        # Convert string keys to int
        answers = {int(k): v for k, v in data['answers'].items()}

        result = consciousness_bridge.calculate_result(answers)
        stats["assessments_completed"] += 1

        return jsonify({
            "success": True,
            "result": consciousness_bridge.to_dict(result)
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 500

# ============= Pattern Theory Analysis =============

@app.route('/api/analyze', methods=['POST'])
def analyze_pattern():
    """
    Analyze text with Pattern Theory Engine.

    Request body:
    {
        "text": "Text to analyze",
        "context": "Optional context"
    }
    """
    if not ENGINES_AVAILABLE:
        return jsonify({"error": "Pattern Theory Engine not available"}), 503

    try:
        data = request.get_json()
        text = data.get("text", "")
        context = data.get("context")

        result = pattern_engine.analyze(text, context)
        stats["analyses_run"] += 1

        return jsonify({
            "success": True,
            "result": {
                "truth_score": result.truth_score,
                "deceit_score": result.deceit_score,
                "algorithm": result.algorithm,
                "pattern_type": result.pattern_type,
                "confidence": result.confidence,
                "recommendation": result.recommended_action
            }
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 500

# ============= Manipulation Detection =============

@app.route('/api/detect', methods=['POST'])
def detect_manipulation():
    """
    Detect manipulation in text.

    Request body:
    {
        "text": "Text to analyze"
    }
    """
    if not ENGINES_AVAILABLE:
        return jsonify({"error": "Manipulation Detector not available"}), 503

    try:
        data = request.get_json()
        text = data.get("text", "")

        result = manipulation_detector.detect(text)
        stats["detections_performed"] += 1

        return jsonify({
            "success": True,
            "result": {
                "m_score": result.m_score,
                "severity": result.severity,
                "techniques": result.techniques_detected,
                "counter_strategy": result.counter_strategy
            }
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 500

# ============= Timeline Projection =============

@app.route('/api/project', methods=['POST'])
def project_timeline():
    """
    Project future timelines.

    Request body:
    {
        "situation": "Current situation description"
    }
    """
    if not ENGINES_AVAILABLE:
        return jsonify({"error": "Timeline Projector not available"}), 503

    try:
        data = request.get_json()
        situation = data.get("situation", "")

        result = timeline_projector.project(situation)

        # Build timelines list from individual timeline attributes
        timelines = []
        for t in [result.timeline_a, result.timeline_b, result.timeline_c]:
            timelines.append({
                "name": t.name,
                "probability": t.success_probability,
                "outcome": t.consciousness_impact,
                "actions": t.key_events
            })

        return jsonify({
            "success": True,
            "result": {
                "timelines": timelines,
                "recommended": result.recommended,
                "consciousness_level": 500  # Default level
            }
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 500

# ============= Seven Domains Analysis =============

@app.route('/api/domains', methods=['POST'])
def analyze_domains():
    """
    Analyze Seven Domains balance.

    Request body:
    {
        "text": "Situation or context to analyze"
    }
    """
    if not ENGINES_AVAILABLE:
        return jsonify({"error": "Seven Domains Analyzer not available"}), 503

    try:
        data = request.get_json()
        text = data.get("text", "")

        result = domains_analyzer.analyze(text)

        return jsonify({
            "success": True,
            "result": {
                "balance_score": result.balance_score,
                "domain_scores": result.domain_scores,
                "strongest": result.strongest_domain,
                "weakest": result.weakest_domain,
                "integration_opportunities": result.integration_opportunities
            }
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 500

# ============= Main =============

if __name__ == "__main__":
    import os
    port = int(os.environ.get("PORT", 5002))

    print("=" * 60)
    print("CONSCIOUSNESS PLATFORM API")
    print("=" * 60)
    print(f"Pattern Theory Engine: {'Available' if ENGINES_AVAILABLE else 'Not Available'}")
    print(f"Starting on port {port}")
    print("\nCore Endpoints:")
    print("  GET  /health - Health check")
    print("  GET  /stats - Platform statistics")
    print("\nAuthentication:")
    print("  POST /api/auth/signup - Register new user")
    print("  POST /api/auth/login - Login with email/password")
    print("  POST /api/auth/refresh - Refresh access token")
    print("  GET  /api/auth/me - Get current user (requires token)")
    print("  GET  /api/auth/oauth/google - Google OAuth")
    print("  GET  /api/auth/oauth/github - GitHub OAuth")
    print("  POST /api/auth/change-password - Change password")
    print("  DEL  /api/auth/delete-account - Delete account")
    print("\nConsciousness Tools:")
    print("  GET  /api/bridge/questions - Get assessment questions")
    print("  POST /api/bridge/assess - Run consciousness assessment")
    print("  POST /api/analyze - Pattern Theory analysis")
    print("  POST /api/detect - Manipulation detection")
    print("  POST /api/project - Timeline projection")
    print("  POST /api/domains - Seven Domains analysis")
    print("=" * 60)

    app.run(debug=False, port=port, host='0.0.0.0')
