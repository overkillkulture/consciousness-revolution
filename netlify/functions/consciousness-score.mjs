// Consciousness Scoring API
// Calculate consciousness level using Pattern Theory formula

export default async (request, context) => {
  if (request.method !== 'POST') {
    return new Response(JSON.stringify({ error: 'POST required' }), {
      status: 405,
      headers: { 'Content-Type': 'application/json' }
    });
  }

  try {
    const data = await request.json();

    // Calculate consciousness level
    const score = calculateConsciousness(data);

    return new Response(JSON.stringify(score), {
      status: 200,
      headers: { 'Content-Type': 'application/json' }
    });

  } catch (error) {
    return new Response(JSON.stringify({ error: error.message }), {
      status: 500,
      headers: { 'Content-Type': 'application/json' }
    });
  }
};

function calculateConsciousness(data) {
  // Pattern Theory Formula:
  // CL = (Pattern_Recognition × 0.4) + (Prediction_Accuracy × 0.3) + (Neutralization_Success × 0.3)

  const patternRecognition = data.pattern_recognition || 50;
  const predictionAccuracy = data.prediction_accuracy || 50;
  const neutralizationSuccess = data.neutralization_success || 50;

  const consciousnessLevel =
    (patternRecognition * 0.4) +
    (predictionAccuracy * 0.3) +
    (neutralizationSuccess * 0.3);

  // Seven Domains scoring
  const domains = {
    physical: data.physical || 50,
    financial: data.financial || 50,
    mental: data.mental || 50,
    emotional: data.emotional || 50,
    social: data.social || 50,
    creative: data.creative || 50,
    integration: data.integration || 50
  };

  const domainAverage = Object.values(domains).reduce((a, b) => a + b, 0) / 7;

  // Combined score
  const combinedScore = (consciousnessLevel * 0.6) + (domainAverage * 0.4);

  // Status determination
  let status, recommendation;
  if (combinedScore >= 85) {
    status = 'MANIPULATION_IMMUNE';
    recommendation = 'Operating at peak consciousness. Maintain current practices.';
  } else if (combinedScore >= 70) {
    status = 'HIGH_CONSCIOUSNESS';
    recommendation = 'Strong foundation. Focus on neutralization practice.';
  } else if (combinedScore >= 50) {
    status = 'DEVELOPING';
    recommendation = 'Growing awareness. Increase pattern recognition training.';
  } else {
    status = 'VULNERABLE';
    recommendation = 'Susceptible to manipulation. Immediate training needed.';
  }

  return {
    consciousness_level: Math.round(consciousnessLevel * 10) / 10,
    domain_average: Math.round(domainAverage * 10) / 10,
    combined_score: Math.round(combinedScore * 10) / 10,
    status: status,
    recommendation: recommendation,
    breakdown: {
      pattern_recognition: patternRecognition,
      prediction_accuracy: predictionAccuracy,
      neutralization_success: neutralizationSuccess
    },
    domains: domains,
    formula: 'CL = (PR × 0.4) + (PA × 0.3) + (NS × 0.3)',
    timestamp: new Date().toISOString()
  };
}

export const config = {
  path: "/api/consciousness-score"
};
