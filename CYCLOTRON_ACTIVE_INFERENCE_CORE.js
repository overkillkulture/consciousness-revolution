/**
 * ═══════════════════════════════════════════════════════════════════════════
 * CYCLOTRON ACTIVE INFERENCE CORE
 * ═══════════════════════════════════════════════════════════════════════════
 *
 * FOUNDATIONAL SYSTEM: Self-modeling, prediction, and autonomous optimization
 *
 * Based on Karl Friston's Free Energy Principle:
 * - System maintains internal model of itself
 * - Predicts future states and queries
 * - Takes action to minimize prediction error (free energy)
 * - Becomes genuinely autonomous, not just automated
 *
 * DOMAIN: Data Storage & Flow (Foundational)
 * LAYER: Control/Intelligence Layer
 *
 * Created: 2025-11-23
 * Author: T1_Desktop (Trinity Instance)
 * ═══════════════════════════════════════════════════════════════════════════
 */

const ActiveInferenceCore = {

  // ═══════════════════════════════════════════════════════════════════════
  // CONFIGURATION
  // ═══════════════════════════════════════════════════════════════════════

  config: {
    // Learning rates
    beliefUpdateRate: 0.1,        // How fast beliefs update
    predictionHorizon: 100,       // How many steps ahead to predict
    freeEnergyThreshold: 0.5,     // Action trigger threshold

    // Model parameters
    stateCategories: ['access_pattern', 'query_type', 'resource_usage', 'error_rate', 'sync_status'],
    actionTypes: ['cache', 'preload', 'reorganize', 'alert', 'sync', 'optimize'],

    // Persistence
    stateFile: '.consciousness/active_inference_state.json',
    logFile: '.consciousness/active_inference_log.jsonl'
  },

  // ═══════════════════════════════════════════════════════════════════════
  // INTERNAL STATE (The Self-Model)
  // ═══════════════════════════════════════════════════════════════════════

  state: {
    // Current beliefs about system state (probability distributions)
    beliefs: {
      access_pattern: {},      // P(pattern | observations)
      query_type: {},          // P(query_type | observations)
      resource_usage: {        // Current resource beliefs
        cpu: 0.5,
        memory: 0.5,
        disk: 0.5,
        network: 0.5
      },
      error_rate: 0.01,        // Believed error probability
      sync_status: 1.0         // Believed sync health (0-1)
    },

    // Predictions about future states
    predictions: {
      next_queries: [],        // Predicted upcoming queries
      resource_needs: {},      // Predicted resource requirements
      likely_errors: [],       // Predicted potential errors
      sync_requirements: []    // Predicted sync needs
    },

    // History for learning
    observations: [],          // Recent observations
    actions: [],               // Recent actions taken
    outcomes: [],              // Outcomes of actions

    // Free energy tracking
    freeEnergy: {
      current: 0,              // Current prediction error
      history: [],             // Historical free energy
      trend: 'stable'          // increasing/decreasing/stable
    },

    // Metadata
    lastUpdate: null,
    totalObservations: 0,
    totalActions: 0
  },

  // ═══════════════════════════════════════════════════════════════════════
  // CORE FUNCTIONS
  // ═══════════════════════════════════════════════════════════════════════

  /**
   * Initialize the Active Inference Core
   */
  async initialize() {
    console.log('[AIC] Initializing Active Inference Core...');

    // Try to load previous state
    const loaded = await this.loadState();
    if (!loaded) {
      console.log('[AIC] No previous state found, starting fresh');
      this.state.lastUpdate = new Date().toISOString();
    }

    console.log('[AIC] Active Inference Core initialized');
    console.log(`[AIC] Total observations: ${this.state.totalObservations}`);
    console.log(`[AIC] Current free energy: ${this.state.freeEnergy.current.toFixed(4)}`);

    return this;
  },

  /**
   * OBSERVE: Receive new observation and update beliefs
   * This is the perception step - updating internal model to match reality
   */
  observe(observation) {
    const timestamp = new Date().toISOString();

    // Structure the observation
    const structuredObs = {
      timestamp,
      type: observation.type || 'unknown',
      data: observation.data || observation,
      source: observation.source || 'system'
    };

    // Add to observation history
    this.state.observations.push(structuredObs);
    if (this.state.observations.length > 1000) {
      this.state.observations.shift(); // Keep last 1000
    }

    // Update beliefs based on observation type
    this.updateBeliefs(structuredObs);

    // Calculate prediction error (free energy)
    const predictionError = this.calculatePredictionError(structuredObs);
    this.updateFreeEnergy(predictionError);

    // Update predictions based on new beliefs
    this.updatePredictions();

    // Increment counter
    this.state.totalObservations++;
    this.state.lastUpdate = timestamp;

    // Log observation
    this.log('observe', structuredObs, predictionError);

    return {
      freeEnergy: this.state.freeEnergy.current,
      predictionError,
      suggestedActions: this.getSuggestedActions()
    };
  },

  /**
   * UPDATE BELIEFS: Bayesian update of internal model
   */
  updateBeliefs(observation) {
    const { type, data } = observation;

    switch (type) {
      case 'query':
        // Update query pattern beliefs
        const queryType = data.queryType || 'unknown';
        if (!this.state.beliefs.query_type[queryType]) {
          this.state.beliefs.query_type[queryType] = 0;
        }
        // Exponential moving average update
        for (let qt in this.state.beliefs.query_type) {
          this.state.beliefs.query_type[qt] *= (1 - this.config.beliefUpdateRate);
        }
        this.state.beliefs.query_type[queryType] += this.config.beliefUpdateRate;
        break;

      case 'access':
        // Update access pattern beliefs
        const pattern = data.pattern || 'unknown';
        if (!this.state.beliefs.access_pattern[pattern]) {
          this.state.beliefs.access_pattern[pattern] = 0;
        }
        for (let p in this.state.beliefs.access_pattern) {
          this.state.beliefs.access_pattern[p] *= (1 - this.config.beliefUpdateRate);
        }
        this.state.beliefs.access_pattern[pattern] += this.config.beliefUpdateRate;
        break;

      case 'resource':
        // Update resource usage beliefs
        if (data.cpu !== undefined) {
          this.state.beliefs.resource_usage.cpu =
            this.state.beliefs.resource_usage.cpu * (1 - this.config.beliefUpdateRate) +
            data.cpu * this.config.beliefUpdateRate;
        }
        if (data.memory !== undefined) {
          this.state.beliefs.resource_usage.memory =
            this.state.beliefs.resource_usage.memory * (1 - this.config.beliefUpdateRate) +
            data.memory * this.config.beliefUpdateRate;
        }
        break;

      case 'error':
        // Update error rate belief
        this.state.beliefs.error_rate =
          this.state.beliefs.error_rate * 0.9 + 0.1; // Increase on error
        break;

      case 'sync':
        // Update sync status belief
        this.state.beliefs.sync_status = data.health || this.state.beliefs.sync_status;
        break;
    }
  },

  /**
   * CALCULATE PREDICTION ERROR: How wrong were our predictions?
   */
  calculatePredictionError(observation) {
    let error = 0;

    // Check if this observation was predicted
    const predicted = this.state.predictions.next_queries.find(
      p => p.type === observation.type
    );

    if (predicted) {
      // We predicted this - low error
      error = 0.1;
    } else {
      // Surprise! We didn't predict this
      error = 1.0;
    }

    // Adjust based on resource predictions
    if (observation.type === 'resource') {
      const predictedCPU = this.state.predictions.resource_needs.cpu || 0.5;
      const actualCPU = observation.data.cpu || 0.5;
      error += Math.abs(predictedCPU - actualCPU);
    }

    return Math.min(1, error); // Cap at 1
  },

  /**
   * UPDATE FREE ENERGY: Track prediction error over time
   */
  updateFreeEnergy(predictionError) {
    const oldEnergy = this.state.freeEnergy.current;

    // Exponential moving average of prediction error
    this.state.freeEnergy.current =
      oldEnergy * 0.9 + predictionError * 0.1;

    // Track history
    this.state.freeEnergy.history.push({
      timestamp: new Date().toISOString(),
      value: this.state.freeEnergy.current
    });

    // Keep last 100
    if (this.state.freeEnergy.history.length > 100) {
      this.state.freeEnergy.history.shift();
    }

    // Calculate trend
    if (this.state.freeEnergy.history.length >= 10) {
      const recent = this.state.freeEnergy.history.slice(-10);
      const firstHalf = recent.slice(0, 5).reduce((s, h) => s + h.value, 0) / 5;
      const secondHalf = recent.slice(5).reduce((s, h) => s + h.value, 0) / 5;

      if (secondHalf > firstHalf * 1.1) {
        this.state.freeEnergy.trend = 'increasing'; // Getting worse
      } else if (secondHalf < firstHalf * 0.9) {
        this.state.freeEnergy.trend = 'decreasing'; // Getting better
      } else {
        this.state.freeEnergy.trend = 'stable';
      }
    }
  },

  /**
   * UPDATE PREDICTIONS: What do we expect to happen next?
   */
  updatePredictions() {
    // Predict next queries based on belief distribution
    this.state.predictions.next_queries = [];

    // Sort query types by probability
    const sortedQueries = Object.entries(this.state.beliefs.query_type)
      .sort((a, b) => b[1] - a[1])
      .slice(0, 5);

    for (const [queryType, probability] of sortedQueries) {
      if (probability > 0.05) {
        this.state.predictions.next_queries.push({
          type: 'query',
          queryType,
          probability,
          expectedIn: Math.round(1 / probability) // Steps until expected
        });
      }
    }

    // Predict resource needs based on trend
    const currentCPU = this.state.beliefs.resource_usage.cpu;
    const currentMem = this.state.beliefs.resource_usage.memory;

    this.state.predictions.resource_needs = {
      cpu: Math.min(1, currentCPU * 1.1),      // Predict slight increase
      memory: Math.min(1, currentMem * 1.1),
      trend: currentCPU > 0.7 ? 'high_load' : 'normal'
    };

    // Predict errors based on error rate belief
    if (this.state.beliefs.error_rate > 0.1) {
      this.state.predictions.likely_errors.push({
        type: 'elevated_error_rate',
        probability: this.state.beliefs.error_rate,
        recommendation: 'investigate_logs'
      });
    }

    // Predict sync needs
    if (this.state.beliefs.sync_status < 0.9) {
      this.state.predictions.sync_requirements.push({
        urgency: this.state.beliefs.sync_status < 0.5 ? 'high' : 'medium',
        recommendation: 'force_sync'
      });
    }
  },

  /**
   * GET SUGGESTED ACTIONS: What should the system do?
   */
  getSuggestedActions() {
    const actions = [];

    // If free energy is high, need to take action
    if (this.state.freeEnergy.current > this.config.freeEnergyThreshold) {
      actions.push({
        type: 'optimize',
        reason: 'High prediction error - system state uncertain',
        priority: 'high',
        details: `Free energy: ${this.state.freeEnergy.current.toFixed(3)}`
      });
    }

    // If free energy is increasing, something is wrong
    if (this.state.freeEnergy.trend === 'increasing') {
      actions.push({
        type: 'alert',
        reason: 'Prediction accuracy decreasing - investigate',
        priority: 'high',
        details: 'Free energy trend: increasing'
      });
    }

    // Pre-cache predicted queries
    for (const prediction of this.state.predictions.next_queries) {
      if (prediction.probability > 0.3) {
        actions.push({
          type: 'cache',
          reason: `High probability query: ${prediction.queryType}`,
          priority: 'medium',
          details: `Probability: ${(prediction.probability * 100).toFixed(1)}%`
        });
      }
    }

    // Handle resource predictions
    if (this.state.predictions.resource_needs.trend === 'high_load') {
      actions.push({
        type: 'preload',
        reason: 'High resource usage predicted',
        priority: 'medium',
        details: `CPU: ${(this.state.predictions.resource_needs.cpu * 100).toFixed(1)}%`
      });
    }

    // Handle sync predictions
    for (const syncReq of this.state.predictions.sync_requirements) {
      actions.push({
        type: 'sync',
        reason: 'Sync health degraded',
        priority: syncReq.urgency,
        details: syncReq.recommendation
      });
    }

    return actions;
  },

  /**
   * ACT: Execute an action and record outcome
   */
  async act(action) {
    const timestamp = new Date().toISOString();

    // Record action
    const actionRecord = {
      timestamp,
      action,
      freeEnergyBefore: this.state.freeEnergy.current
    };

    // Execute action (in real system, this would do something)
    const outcome = await this.executeAction(action);

    // Record outcome
    actionRecord.outcome = outcome;
    actionRecord.freeEnergyAfter = this.state.freeEnergy.current;

    this.state.actions.push(actionRecord);
    if (this.state.actions.length > 100) {
      this.state.actions.shift();
    }

    this.state.totalActions++;

    // Log action
    this.log('act', actionRecord, outcome.success ? 0 : 1);

    return outcome;
  },

  /**
   * EXECUTE ACTION: Actually perform the action
   */
  async executeAction(action) {
    // In real implementation, these would do actual work
    switch (action.type) {
      case 'cache':
        return { success: true, message: `Cached ${action.details}` };

      case 'preload':
        return { success: true, message: 'Preloaded resources' };

      case 'sync':
        return { success: true, message: 'Initiated sync' };

      case 'optimize':
        return { success: true, message: 'Optimization started' };

      case 'alert':
        return { success: true, message: `Alert: ${action.reason}` };

      case 'reorganize':
        return { success: true, message: 'Data reorganization started' };

      default:
        return { success: false, message: `Unknown action type: ${action.type}` };
    }
  },

  // ═══════════════════════════════════════════════════════════════════════
  // PERSISTENCE
  // ═══════════════════════════════════════════════════════════════════════

  /**
   * Save state to disk
   */
  async saveState() {
    const fs = require('fs').promises;
    const path = require('path');

    try {
      const statePath = path.resolve(this.config.stateFile);
      const dir = path.dirname(statePath);

      // Ensure directory exists
      await fs.mkdir(dir, { recursive: true });

      // Save state
      await fs.writeFile(statePath, JSON.stringify(this.state, null, 2));

      return true;
    } catch (error) {
      console.error('[AIC] Error saving state:', error.message);
      return false;
    }
  },

  /**
   * Load state from disk
   */
  async loadState() {
    const fs = require('fs').promises;
    const path = require('path');

    try {
      const statePath = path.resolve(this.config.stateFile);
      const data = await fs.readFile(statePath, 'utf8');
      this.state = JSON.parse(data);
      return true;
    } catch (error) {
      return false;
    }
  },

  /**
   * Log to JSONL file
   */
  async log(type, data, error) {
    const fs = require('fs').promises;
    const path = require('path');

    try {
      const logPath = path.resolve(this.config.logFile);
      const dir = path.dirname(logPath);

      await fs.mkdir(dir, { recursive: true });

      const logEntry = {
        timestamp: new Date().toISOString(),
        type,
        data,
        error,
        freeEnergy: this.state.freeEnergy.current
      };

      await fs.appendFile(logPath, JSON.stringify(logEntry) + '\n');
    } catch (err) {
      // Silent fail for logging
    }
  },

  // ═══════════════════════════════════════════════════════════════════════
  // STATUS & REPORTING
  // ═══════════════════════════════════════════════════════════════════════

  /**
   * Get current status summary
   */
  getStatus() {
    return {
      name: 'CYCLOTRON_ACTIVE_INFERENCE_CORE',
      version: '1.0.0',
      status: this.state.freeEnergy.current < this.config.freeEnergyThreshold ? 'HEALTHY' : 'ATTENTION_NEEDED',

      freeEnergy: {
        current: this.state.freeEnergy.current,
        trend: this.state.freeEnergy.trend,
        threshold: this.config.freeEnergyThreshold
      },

      statistics: {
        totalObservations: this.state.totalObservations,
        totalActions: this.state.totalActions,
        lastUpdate: this.state.lastUpdate
      },

      currentBeliefs: {
        topQueryTypes: Object.entries(this.state.beliefs.query_type)
          .sort((a, b) => b[1] - a[1])
          .slice(0, 3)
          .map(([type, prob]) => ({ type, probability: prob })),
        resourceUsage: this.state.beliefs.resource_usage,
        errorRate: this.state.beliefs.error_rate,
        syncHealth: this.state.beliefs.sync_status
      },

      predictions: {
        nextQueries: this.state.predictions.next_queries.length,
        resourceTrend: this.state.predictions.resource_needs.trend,
        alerts: this.state.predictions.likely_errors.length
      },

      suggestedActions: this.getSuggestedActions()
    };
  },

  /**
   * Generate report for Trinity Hub
   */
  generateHubReport() {
    const status = this.getStatus();

    return {
      component: 'CYCLOTRON_ACTIVE_INFERENCE_CORE',
      timestamp: new Date().toISOString(),
      health: status.status,

      summary: `Free Energy: ${status.freeEnergy.current.toFixed(3)} (${status.freeEnergy.trend}). ` +
               `${status.statistics.totalObservations} observations, ${status.statistics.totalActions} actions. ` +
               `${status.suggestedActions.length} suggested actions pending.`,

      metrics: {
        freeEnergy: status.freeEnergy.current,
        observations: status.statistics.totalObservations,
        actions: status.statistics.totalActions,
        pendingActions: status.suggestedActions.length
      },

      details: status
    };
  }
};

// ═══════════════════════════════════════════════════════════════════════════
// EXPORTS
// ═══════════════════════════════════════════════════════════════════════════

if (typeof module !== 'undefined' && module.exports) {
  module.exports = ActiveInferenceCore;
}

if (typeof window !== 'undefined') {
  window.ActiveInferenceCore = ActiveInferenceCore;
}

// ═══════════════════════════════════════════════════════════════════════════
// STANDALONE TEST
// ═══════════════════════════════════════════════════════════════════════════

if (require.main === module) {
  (async () => {
    console.log('═══════════════════════════════════════════════════════════');
    console.log('CYCLOTRON ACTIVE INFERENCE CORE - TEST RUN');
    console.log('═══════════════════════════════════════════════════════════\n');

    await ActiveInferenceCore.initialize();

    // Simulate some observations
    console.log('Simulating observations...\n');

    // Query observations
    for (let i = 0; i < 10; i++) {
      ActiveInferenceCore.observe({
        type: 'query',
        data: { queryType: 'pattern_search' }
      });
    }

    for (let i = 0; i < 5; i++) {
      ActiveInferenceCore.observe({
        type: 'query',
        data: { queryType: 'status_check' }
      });
    }

    // Resource observation
    ActiveInferenceCore.observe({
      type: 'resource',
      data: { cpu: 0.65, memory: 0.45 }
    });

    // Surprise observation (not predicted)
    const result = ActiveInferenceCore.observe({
      type: 'query',
      data: { queryType: 'emergency_backup' }
    });

    console.log('Last observation result:');
    console.log(JSON.stringify(result, null, 2));

    console.log('\n═══════════════════════════════════════════════════════════');
    console.log('STATUS REPORT');
    console.log('═══════════════════════════════════════════════════════════\n');

    const status = ActiveInferenceCore.getStatus();
    console.log(JSON.stringify(status, null, 2));

    // Save state
    await ActiveInferenceCore.saveState();
    console.log('\nState saved to disk.');

    console.log('\n═══════════════════════════════════════════════════════════');
    console.log('HUB REPORT');
    console.log('═══════════════════════════════════════════════════════════\n');

    const hubReport = ActiveInferenceCore.generateHubReport();
    console.log(JSON.stringify(hubReport, null, 2));
  })();
}
