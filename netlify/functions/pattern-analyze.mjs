// Pattern Theory Analysis API
// Analyze text for truth/deceit patterns

export default async (request, context) => {
  if (request.method !== 'POST') {
    return new Response(JSON.stringify({ error: 'POST required' }), {
      status: 405,
      headers: { 'Content-Type': 'application/json' }
    });
  }

  try {
    const { text, mode } = await request.json();

    if (!text) {
      return new Response(JSON.stringify({ error: 'text required' }), {
        status: 400,
        headers: { 'Content-Type': 'application/json' }
      });
    }

    // Pattern analysis
    const analysis = analyzePatterns(text, mode || 'full');

    return new Response(JSON.stringify(analysis), {
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

function analyzePatterns(text, mode) {
  const words = text.toLowerCase().split(/\s+/);
  const sentences = text.split(/[.!?]+/).filter(s => s.trim());

  // Truth indicators
  const truthIndicators = [
    'because', 'therefore', 'evidence', 'data', 'specifically',
    'measured', 'observed', 'documented', 'verified', 'tested'
  ];

  // Deceit indicators
  const deceitIndicators = [
    'trust me', 'believe me', 'honestly', 'to be honest',
    'everyone knows', 'obviously', 'clearly', 'simply',
    'just', 'only', 'always', 'never'
  ];

  // Manipulation patterns
  const manipulationPatterns = [
    'you should', 'you must', 'you need to', 'you have to',
    'dont you think', 'wouldnt you agree', 'surely you'
  ];

  let truthScore = 0;
  let deceitScore = 0;
  let manipulationScore = 0;

  // Count indicators
  truthIndicators.forEach(indicator => {
    if (text.toLowerCase().includes(indicator)) truthScore += 10;
  });

  deceitIndicators.forEach(indicator => {
    if (text.toLowerCase().includes(indicator)) deceitScore += 10;
  });

  manipulationPatterns.forEach(pattern => {
    if (text.toLowerCase().includes(pattern)) manipulationScore += 15;
  });

  // Calculate consciousness level
  const rawScore = truthScore - deceitScore - manipulationScore;
  const consciousnessLevel = Math.max(0, Math.min(100, 50 + rawScore));

  // Determine algorithm
  const algorithm = consciousnessLevel >= 50 ? 'TRUTH' : 'DECEIT';

  return {
    text_length: text.length,
    word_count: words.length,
    sentence_count: sentences.length,
    truth_score: truthScore,
    deceit_score: deceitScore,
    manipulation_score: manipulationScore,
    consciousness_level: consciousnessLevel,
    algorithm: algorithm,
    analysis: {
      truth_indicators_found: truthIndicators.filter(i => text.toLowerCase().includes(i)),
      deceit_indicators_found: deceitIndicators.filter(i => text.toLowerCase().includes(i)),
      manipulation_patterns_found: manipulationPatterns.filter(p => text.toLowerCase().includes(p))
    },
    recommendation: consciousnessLevel >= 70
      ? 'High consciousness - Truth algorithm dominant'
      : consciousnessLevel >= 50
      ? 'Moderate consciousness - Mixed patterns'
      : 'Low consciousness - Deceit patterns detected'
  };
}

export const config = {
  path: "/api/pattern-analyze"
};
