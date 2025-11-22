// Seven Domains Analysis API
// Analyze and score across all 7 consciousness domains

export default async (request, context) => {
  if (request.method === 'GET') {
    // Return domain definitions
    return new Response(JSON.stringify(getDomainDefinitions()), {
      status: 200,
      headers: { 'Content-Type': 'application/json' }
    });
  }

  if (request.method !== 'POST') {
    return new Response(JSON.stringify({ error: 'GET or POST required' }), {
      status: 405,
      headers: { 'Content-Type': 'application/json' }
    });
  }

  try {
    const data = await request.json();
    const analysis = analyzeDomains(data);

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

function getDomainDefinitions() {
  return {
    domains: [
      {
        id: 1,
        name: 'Physical',
        code: 'CHAOS_FORGE',
        description: 'Material creation, health, environment',
        questions: ['Energy level?', 'Physical health?', 'Environment quality?']
      },
      {
        id: 2,
        name: 'Financial',
        code: 'QUANTUM_VAULT',
        description: 'Economic systems, resources, value creation',
        questions: ['Income stability?', 'Asset growth?', 'Value creation?']
      },
      {
        id: 3,
        name: 'Mental',
        code: 'MIND_MATRIX',
        description: 'Knowledge, AI, learning, cognition',
        questions: ['Learning rate?', 'Knowledge application?', 'AI integration?']
      },
      {
        id: 4,
        name: 'Emotional',
        code: 'SOUL_SANCTUARY',
        description: 'Consciousness, feelings, inner state',
        questions: ['Emotional stability?', 'Self-awareness?', 'Inner peace?']
      },
      {
        id: 5,
        name: 'Social',
        code: 'REALITY_FORGE',
        description: 'Relationships, influence, community',
        questions: ['Relationship quality?', 'Network strength?', 'Influence level?']
      },
      {
        id: 6,
        name: 'Creative',
        code: 'ARKITEK_ACADEMY',
        description: 'Design, art, innovation, expression',
        questions: ['Creative output?', 'Innovation rate?', 'Artistic expression?']
      },
      {
        id: 7,
        name: 'Integration',
        code: 'NEXUS_TERMINAL',
        description: 'Command center, coordination, synthesis',
        questions: ['System coordination?', 'Life integration?', 'Holistic balance?']
      }
    ]
  };
}

function analyzeDomains(data) {
  const domains = {
    physical: data.physical || 50,
    financial: data.financial || 50,
    mental: data.mental || 50,
    emotional: data.emotional || 50,
    social: data.social || 50,
    creative: data.creative || 50,
    integration: data.integration || 50
  };

  // Calculate totals
  const total = Object.values(domains).reduce((a, b) => a + b, 0);
  const average = total / 7;
  const max = Math.max(...Object.values(domains));
  const min = Math.min(...Object.values(domains));

  // Find strongest and weakest
  const strongest = Object.entries(domains).find(([k, v]) => v === max)[0];
  const weakest = Object.entries(domains).find(([k, v]) => v === min)[0];

  // Balance score (how evenly distributed)
  const variance = Object.values(domains).reduce((sum, val) =>
    sum + Math.pow(val - average, 2), 0) / 7;
  const balanceScore = Math.max(0, 100 - Math.sqrt(variance));

  // Overall consciousness projection
  const overallScore = (average * 0.7) + (balanceScore * 0.3);

  return {
    domains: domains,
    analysis: {
      total: Math.round(total),
      average: Math.round(average * 10) / 10,
      balance_score: Math.round(balanceScore * 10) / 10,
      overall_score: Math.round(overallScore * 10) / 10,
      strongest_domain: strongest,
      weakest_domain: weakest,
      spread: max - min
    },
    recommendations: [
      `Focus on ${weakest} domain for greatest impact`,
      balanceScore < 70 ? 'Work on balancing all domains more evenly' : 'Good domain balance maintained',
      average < 60 ? 'Overall consciousness expansion needed' : 'Solid foundation across domains'
    ],
    timestamp: new Date().toISOString()
  };
}

export const config = {
  path: "/api/seven-domains"
};
