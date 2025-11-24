/**
 * ═══════════════════════════════════════════════════════════════════════════
 * CYCLOTRON SWARM CLUSTERING ENGINE
 * ═══════════════════════════════════════════════════════════════════════════
 *
 * FOUNDATIONAL SYSTEM: Swarm intelligence for pattern organization
 *
 * Based on Particle Swarm Optimization (PSO):
 * - Each pattern is a particle seeking optimal cluster position
 * - Particles share information about best positions found
 * - Global organization emerges from local interactions
 * - No central controller - truly distributed intelligence
 *
 * DOMAIN: Data Storage & Flow (Foundational)
 * LAYER: Organization/Intelligence Layer
 *
 * Created: 2025-11-23
 * Author: T1_Desktop (Trinity Instance)
 * ═══════════════════════════════════════════════════════════════════════════
 */

const SwarmClustering = {

  // ═══════════════════════════════════════════════════════════════════════
  // CONFIGURATION
  // ═══════════════════════════════════════════════════════════════════════

  config: {
    // PSO Parameters
    numParticles: 100,           // Swarm size
    dimensions: 8,               // Feature dimensions
    maxIterations: 100,          // Max optimization iterations
    inertiaWeight: 0.7,          // Momentum
    cognitiveWeight: 1.5,        // Personal best attraction
    socialWeight: 1.5,           // Global best attraction

    // Clustering
    numClusters: 7,              // Number of clusters (7 domains)
    convergenceThreshold: 0.001, // Stop when change < this

    // Storage
    stateFile: '.consciousness/swarm_state.json',
    clustersFile: '.consciousness/pattern_clusters.json'
  },

  // ═══════════════════════════════════════════════════════════════════════
  // STATE
  // ═══════════════════════════════════════════════════════════════════════

  state: {
    // Particles (patterns being clustered)
    particles: [],

    // Cluster centroids
    centroids: [],

    // Best positions found
    globalBest: {
      position: null,
      fitness: Infinity
    },

    // Statistics
    iterations: 0,
    convergenceHistory: [],
    clusterAssignments: new Map()
  },

  // ═══════════════════════════════════════════════════════════════════════
  // PARTICLE CLASS
  // ═══════════════════════════════════════════════════════════════════════

  /**
   * Create a particle (pattern agent)
   */
  createParticle(id, features) {
    return {
      id: id,
      position: features.slice(),        // Current position in feature space
      velocity: this.randomVelocity(),   // Current velocity
      personalBest: {
        position: features.slice(),
        fitness: Infinity
      },
      cluster: -1,                       // Assigned cluster
      neighbors: []                      // Nearby particles
    };
  },

  /**
   * Generate random velocity
   */
  randomVelocity() {
    const velocity = [];
    for (let i = 0; i < this.config.dimensions; i++) {
      velocity.push((Math.random() - 0.5) * 0.1);
    }
    return velocity;
  },

  // ═══════════════════════════════════════════════════════════════════════
  // INITIALIZATION
  // ═══════════════════════════════════════════════════════════════════════

  /**
   * Initialize swarm with patterns
   */
  initialize(patterns) {
    console.log('[SWARM] Initializing Swarm Clustering Engine...');
    console.log(`[SWARM] Loading ${patterns.length} patterns`);

    // Create particles from patterns
    this.state.particles = patterns.map((pattern, i) => {
      // Extract features from pattern (or use provided features)
      const features = pattern.features || this.extractFeatures(pattern);
      return this.createParticle(pattern.id || `pattern_${i}`, features);
    });

    // Initialize cluster centroids using k-means++ initialization
    this.initializeCentroids();

    // Evaluate initial fitness
    for (const particle of this.state.particles) {
      const fitness = this.evaluateFitness(particle);
      particle.personalBest.fitness = fitness;

      if (fitness < this.state.globalBest.fitness) {
        this.state.globalBest.position = particle.position.slice();
        this.state.globalBest.fitness = fitness;
      }
    }

    console.log(`[SWARM] Initialized ${this.state.particles.length} particles`);
    console.log(`[SWARM] ${this.state.centroids.length} cluster centroids`);
    console.log(`[SWARM] Initial global best fitness: ${this.state.globalBest.fitness.toFixed(4)}`);

    return this;
  },

  /**
   * Extract features from a pattern object
   */
  extractFeatures(pattern) {
    // Default feature extraction - can be customized
    const features = new Array(this.config.dimensions).fill(0);

    if (typeof pattern === 'object') {
      // Extract from pattern properties
      const str = JSON.stringify(pattern);

      // Feature 1: Length
      features[0] = Math.min(str.length / 1000, 1);

      // Feature 2: Complexity (unique chars / length)
      features[1] = new Set(str).size / str.length;

      // Feature 3: Numeric ratio
      features[2] = (str.match(/\d/g) || []).length / str.length;

      // Feature 4: Nesting depth
      const depth = (str.match(/{/g) || []).length;
      features[3] = Math.min(depth / 10, 1);

      // Features 5-8: Hash-based pseudo-random (deterministic)
      let hash = 0;
      for (let i = 0; i < str.length; i++) {
        hash = ((hash << 5) - hash) + str.charCodeAt(i);
        hash |= 0;
      }
      for (let i = 4; i < 8; i++) {
        features[i] = Math.abs(Math.sin(hash * (i + 1)));
      }
    }

    return features;
  },

  /**
   * Initialize centroids using k-means++
   */
  initializeCentroids() {
    const centroids = [];
    const particles = this.state.particles;

    if (particles.length === 0) return;

    // First centroid: random particle
    const first = particles[Math.floor(Math.random() * particles.length)];
    centroids.push(first.position.slice());

    // Remaining centroids: probability proportional to distance squared
    while (centroids.length < this.config.numClusters) {
      const distances = particles.map(p => {
        const minDist = centroids.reduce((min, c) => {
          return Math.min(min, this.distance(p.position, c));
        }, Infinity);
        return minDist * minDist;
      });

      const totalDist = distances.reduce((a, b) => a + b, 0);
      let random = Math.random() * totalDist;

      for (let i = 0; i < particles.length; i++) {
        random -= distances[i];
        if (random <= 0) {
          centroids.push(particles[i].position.slice());
          break;
        }
      }
    }

    this.state.centroids = centroids;
  },

  // ═══════════════════════════════════════════════════════════════════════
  // PSO OPERATIONS
  // ═══════════════════════════════════════════════════════════════════════

  /**
   * Calculate Euclidean distance
   */
  distance(a, b) {
    let sum = 0;
    for (let i = 0; i < a.length; i++) {
      sum += (a[i] - b[i]) ** 2;
    }
    return Math.sqrt(sum);
  },

  /**
   * Evaluate fitness (lower is better)
   * Fitness = distance to nearest centroid
   */
  evaluateFitness(particle) {
    let minDist = Infinity;
    let nearestCluster = 0;

    for (let i = 0; i < this.state.centroids.length; i++) {
      const dist = this.distance(particle.position, this.state.centroids[i]);
      if (dist < minDist) {
        minDist = dist;
        nearestCluster = i;
      }
    }

    particle.cluster = nearestCluster;
    return minDist;
  },

  /**
   * Update particle velocity
   */
  updateVelocity(particle) {
    const inertia = this.config.inertiaWeight;
    const cognitive = this.config.cognitiveWeight;
    const social = this.config.socialWeight;

    for (let i = 0; i < this.config.dimensions; i++) {
      const r1 = Math.random();
      const r2 = Math.random();

      particle.velocity[i] =
        inertia * particle.velocity[i] +
        cognitive * r1 * (particle.personalBest.position[i] - particle.position[i]) +
        social * r2 * (this.state.globalBest.position[i] - particle.position[i]);

      // Clamp velocity
      particle.velocity[i] = Math.max(-0.5, Math.min(0.5, particle.velocity[i]));
    }
  },

  /**
   * Update particle position
   */
  updatePosition(particle) {
    for (let i = 0; i < this.config.dimensions; i++) {
      particle.position[i] += particle.velocity[i];

      // Clamp position to [0, 1]
      particle.position[i] = Math.max(0, Math.min(1, particle.position[i]));
    }
  },

  /**
   * Update cluster centroids based on assigned particles
   */
  updateCentroids() {
    const newCentroids = [];

    for (let c = 0; c < this.config.numClusters; c++) {
      const clusterParticles = this.state.particles.filter(p => p.cluster === c);

      if (clusterParticles.length > 0) {
        // Calculate mean position
        const mean = new Array(this.config.dimensions).fill(0);
        for (const particle of clusterParticles) {
          for (let i = 0; i < this.config.dimensions; i++) {
            mean[i] += particle.position[i];
          }
        }
        for (let i = 0; i < this.config.dimensions; i++) {
          mean[i] /= clusterParticles.length;
        }
        newCentroids.push(mean);
      } else {
        // Keep old centroid if no particles assigned
        newCentroids.push(this.state.centroids[c]);
      }
    }

    this.state.centroids = newCentroids;
  },

  /**
   * Run one iteration of swarm optimization
   */
  iterate() {
    let totalChange = 0;

    for (const particle of this.state.particles) {
      // Update velocity
      this.updateVelocity(particle);

      // Store old position
      const oldPos = particle.position.slice();

      // Update position
      this.updatePosition(particle);

      // Calculate change
      totalChange += this.distance(oldPos, particle.position);

      // Evaluate new fitness
      const fitness = this.evaluateFitness(particle);

      // Update personal best
      if (fitness < particle.personalBest.fitness) {
        particle.personalBest.position = particle.position.slice();
        particle.personalBest.fitness = fitness;

        // Update global best
        if (fitness < this.state.globalBest.fitness) {
          this.state.globalBest.position = particle.position.slice();
          this.state.globalBest.fitness = fitness;
        }
      }
    }

    // Update centroids
    this.updateCentroids();

    this.state.iterations++;
    const avgChange = totalChange / this.state.particles.length;

    this.state.convergenceHistory.push({
      iteration: this.state.iterations,
      globalBestFitness: this.state.globalBest.fitness,
      avgChange: avgChange
    });

    return avgChange;
  },

  /**
   * Run full optimization
   */
  optimize() {
    console.log('[SWARM] Starting optimization...');

    for (let i = 0; i < this.config.maxIterations; i++) {
      const change = this.iterate();

      // Log every 10 iterations
      if (i % 10 === 0 || i === this.config.maxIterations - 1) {
        console.log(`[SWARM] Iteration ${i + 1}: fitness=${this.state.globalBest.fitness.toFixed(4)}, change=${change.toFixed(6)}`);
      }

      // Check convergence
      if (change < this.config.convergenceThreshold) {
        console.log(`[SWARM] Converged at iteration ${i + 1}`);
        break;
      }
    }

    // Build cluster assignments
    this.buildClusterAssignments();

    return this.getResults();
  },

  /**
   * Build final cluster assignments map
   */
  buildClusterAssignments() {
    this.state.clusterAssignments.clear();

    for (let c = 0; c < this.config.numClusters; c++) {
      const members = this.state.particles
        .filter(p => p.cluster === c)
        .map(p => p.id);

      this.state.clusterAssignments.set(c, {
        members: members,
        centroid: this.state.centroids[c],
        size: members.length
      });
    }
  },

  // ═══════════════════════════════════════════════════════════════════════
  // RESULTS & REPORTING
  // ═══════════════════════════════════════════════════════════════════════

  /**
   * Get clustering results
   */
  getResults() {
    const clusters = [];

    for (const [clusterId, clusterData] of this.state.clusterAssignments) {
      clusters.push({
        id: clusterId,
        name: this.getClusterName(clusterId),
        size: clusterData.size,
        members: clusterData.members,
        centroid: clusterData.centroid
      });
    }

    return {
      clusters: clusters,
      iterations: this.state.iterations,
      finalFitness: this.state.globalBest.fitness,
      convergenceHistory: this.state.convergenceHistory.slice(-10)
    };
  },

  /**
   * Get cluster name (maps to Seven Domains)
   */
  getClusterName(clusterId) {
    const domainNames = [
      'CHAOS_FORGE (Physical)',
      'QUANTUM_VAULT (Financial)',
      'MIND_MATRIX (Mental)',
      'SOUL_SANCTUARY (Emotional)',
      'REALITY_FORGE (Social)',
      'ARKITEK_ACADEMY (Creative)',
      'NEXUS_TERMINAL (Integration)'
    ];
    return domainNames[clusterId] || `Cluster_${clusterId}`;
  },

  /**
   * Get status
   */
  getStatus() {
    return {
      name: 'CYCLOTRON_SWARM_CLUSTERING',
      version: '1.0.0',

      configuration: {
        particles: this.config.numParticles,
        clusters: this.config.numClusters,
        dimensions: this.config.dimensions
      },

      statistics: {
        totalParticles: this.state.particles.length,
        iterations: this.state.iterations,
        globalBestFitness: this.state.globalBest.fitness,
        clustersFormed: this.state.clusterAssignments.size
      },

      clusterSizes: Array.from(this.state.clusterAssignments.values())
        .map((c, i) => ({
          cluster: this.getClusterName(i),
          size: c.size
        }))
    };
  },

  /**
   * Generate hub report
   */
  generateHubReport() {
    const status = this.getStatus();

    return {
      component: 'CYCLOTRON_SWARM_CLUSTERING',
      timestamp: new Date().toISOString(),
      health: status.statistics.iterations > 0 ? 'OPERATIONAL' : 'IDLE',

      summary: `${status.statistics.totalParticles} patterns clustered into ${status.statistics.clustersFormed} groups. ` +
               `${status.statistics.iterations} iterations. ` +
               `Final fitness: ${status.statistics.globalBestFitness.toFixed(4)}`,

      metrics: {
        patterns: status.statistics.totalParticles,
        clusters: status.statistics.clustersFormed,
        iterations: status.statistics.iterations,
        fitness: status.statistics.globalBestFitness
      },

      details: status
    };
  },

  // ═══════════════════════════════════════════════════════════════════════
  // PERSISTENCE
  // ═══════════════════════════════════════════════════════════════════════

  /**
   * Save state
   */
  async saveState() {
    const fs = require('fs').promises;
    const path = require('path');

    try {
      const statePath = path.resolve(this.config.stateFile);
      const clustersPath = path.resolve(this.config.clustersFile);
      const dir = path.dirname(statePath);

      await fs.mkdir(dir, { recursive: true });

      // Save full state
      await fs.writeFile(statePath, JSON.stringify({
        centroids: this.state.centroids,
        globalBest: this.state.globalBest,
        iterations: this.state.iterations,
        convergenceHistory: this.state.convergenceHistory
      }, null, 2));

      // Save cluster assignments
      await fs.writeFile(clustersPath, JSON.stringify(
        Object.fromEntries(this.state.clusterAssignments),
        null, 2
      ));

      return true;
    } catch (error) {
      console.error('[SWARM] Error saving state:', error.message);
      return false;
    }
  }
};

// ═══════════════════════════════════════════════════════════════════════════
// EXPORTS
// ═══════════════════════════════════════════════════════════════════════════

module.exports = SwarmClustering;

// ═══════════════════════════════════════════════════════════════════════════
// STANDALONE TEST
// ═══════════════════════════════════════════════════════════════════════════

if (require.main === module) {
  (async () => {
    console.log('═══════════════════════════════════════════════════════════');
    console.log('CYCLOTRON SWARM CLUSTERING - TEST RUN');
    console.log('═══════════════════════════════════════════════════════════\n');

    // Generate test patterns
    const testPatterns = [];
    for (let i = 0; i < 50; i++) {
      testPatterns.push({
        id: `pattern_${i}`,
        type: ['query', 'access', 'error', 'sync'][i % 4],
        data: { value: Math.random(), category: i % 7 }
      });
    }

    // Initialize and run
    SwarmClustering.initialize(testPatterns);
    const results = SwarmClustering.optimize();

    // Save state
    await SwarmClustering.saveState();
    console.log('\nState saved to disk.');

    // Show results
    console.log('\n═══════════════════════════════════════════════════════════');
    console.log('CLUSTERING RESULTS');
    console.log('═══════════════════════════════════════════════════════════\n');

    for (const cluster of results.clusters) {
      console.log(`${cluster.name}: ${cluster.size} patterns`);
    }

    console.log('\n═══════════════════════════════════════════════════════════');
    console.log('HUB REPORT');
    console.log('═══════════════════════════════════════════════════════════\n');

    console.log(JSON.stringify(SwarmClustering.generateHubReport(), null, 2));
  })();
}
