/**
 * ═══════════════════════════════════════════════════════════════════════════
 * TRINITY SECURE CRDT COMMUNICATIONS
 * ═══════════════════════════════════════════════════════════════════════════
 *
 * FOUNDATIONAL SYSTEM: Conflict-free replicated communication layer
 *
 * Features:
 * - CRDT-based messages (merge without conflicts)
 * - End-to-end encryption support
 * - Offline-first (works without network)
 * - Automatic sync when connected
 * - Message integrity verification
 *
 * DOMAIN: Security & Communication (Foundational)
 * LAYER: Communication/Sync Layer
 *
 * Created: 2025-11-23
 * Author: T1_Desktop (Trinity Instance)
 * ═══════════════════════════════════════════════════════════════════════════
 */

const crypto = require('crypto');
const fs = require('fs').promises;
const path = require('path');

const TrinitySecureCRDT = {

  // ═══════════════════════════════════════════════════════════════════════
  // CONFIGURATION
  // ═══════════════════════════════════════════════════════════════════════

  config: {
    // Storage
    dataDir: '.trinity/secure_crdt',
    messagesFile: 'messages.json',
    stateFile: 'vector_clock.json',
    peersFile: 'known_peers.json',

    // Security
    encryptionAlgorithm: 'aes-256-gcm',
    hashAlgorithm: 'sha256',
    keyDerivationIterations: 100000,

    // Sync
    syncIntervalMs: 10000,
    maxMessageAge: 7 * 24 * 60 * 60 * 1000, // 7 days

    // Instance
    instanceId: null
  },

  // ═══════════════════════════════════════════════════════════════════════
  // STATE (CRDT Data Structures)
  // ═══════════════════════════════════════════════════════════════════════

  state: {
    // G-Counter based vector clock for causal ordering
    vectorClock: {},

    // LWW-Element-Set for messages (Last-Writer-Wins)
    messages: new Map(),

    // OR-Set for known peers
    peers: {
      added: new Map(),    // {peerId -> {timestamp, data}}
      removed: new Map()   // {peerId -> timestamp}
    },

    // Encryption keys (derived from shared secret)
    keys: {
      encryption: null,
      signing: null
    },

    // Sync state
    lastSync: null,
    pendingSync: []
  },

  // ═══════════════════════════════════════════════════════════════════════
  // INITIALIZATION
  // ═══════════════════════════════════════════════════════════════════════

  /**
   * Initialize the secure CRDT communication system
   */
  async initialize(instanceId, sharedSecret = null) {
    console.log('[CRDT] Initializing Trinity Secure CRDT Communications...');

    this.config.instanceId = instanceId;

    // Ensure data directory exists
    const dataPath = path.resolve(this.config.dataDir);
    await fs.mkdir(dataPath, { recursive: true });

    // Initialize vector clock for this instance
    if (!this.state.vectorClock[instanceId]) {
      this.state.vectorClock[instanceId] = 0;
    }

    // Load existing state
    await this.loadState();

    // Derive encryption keys if shared secret provided
    if (sharedSecret) {
      await this.deriveKeys(sharedSecret);
      console.log('[CRDT] Encryption keys derived');
    }

    console.log(`[CRDT] Initialized as instance: ${instanceId}`);
    console.log(`[CRDT] Messages in store: ${this.state.messages.size}`);
    console.log(`[CRDT] Known peers: ${this.getPeers().length}`);

    return this;
  },

  // ═══════════════════════════════════════════════════════════════════════
  // KEY DERIVATION & ENCRYPTION
  // ═══════════════════════════════════════════════════════════════════════

  /**
   * Derive encryption and signing keys from shared secret
   */
  async deriveKeys(sharedSecret) {
    return new Promise((resolve, reject) => {
      // Derive encryption key
      crypto.pbkdf2(
        sharedSecret,
        'trinity-encryption-salt',
        this.config.keyDerivationIterations,
        32,
        'sha512',
        (err, encKey) => {
          if (err) return reject(err);

          this.state.keys.encryption = encKey;

          // Derive signing key
          crypto.pbkdf2(
            sharedSecret,
            'trinity-signing-salt',
            this.config.keyDerivationIterations,
            32,
            'sha512',
            (err, signKey) => {
              if (err) return reject(err);
              this.state.keys.signing = signKey;
              resolve();
            }
          );
        }
      );
    });
  },

  /**
   * Encrypt a message
   */
  encrypt(plaintext) {
    if (!this.state.keys.encryption) {
      return { encrypted: false, data: plaintext };
    }

    const iv = crypto.randomBytes(16);
    const cipher = crypto.createCipheriv(
      this.config.encryptionAlgorithm,
      this.state.keys.encryption,
      iv
    );

    let encrypted = cipher.update(JSON.stringify(plaintext), 'utf8', 'hex');
    encrypted += cipher.final('hex');

    const authTag = cipher.getAuthTag();

    return {
      encrypted: true,
      iv: iv.toString('hex'),
      authTag: authTag.toString('hex'),
      data: encrypted
    };
  },

  /**
   * Decrypt a message
   */
  decrypt(encryptedObj) {
    if (!encryptedObj.encrypted) {
      return encryptedObj.data;
    }

    if (!this.state.keys.encryption) {
      throw new Error('No encryption key available');
    }

    const decipher = crypto.createDecipheriv(
      this.config.encryptionAlgorithm,
      this.state.keys.encryption,
      Buffer.from(encryptedObj.iv, 'hex')
    );

    decipher.setAuthTag(Buffer.from(encryptedObj.authTag, 'hex'));

    let decrypted = decipher.update(encryptedObj.data, 'hex', 'utf8');
    decrypted += decipher.final('utf8');

    return JSON.parse(decrypted);
  },

  /**
   * Create message signature
   */
  sign(data) {
    if (!this.state.keys.signing) {
      return null;
    }

    const hmac = crypto.createHmac('sha256', this.state.keys.signing);
    hmac.update(JSON.stringify(data));
    return hmac.digest('hex');
  },

  /**
   * Verify message signature
   */
  verify(data, signature) {
    if (!this.state.keys.signing || !signature) {
      return true; // No signature verification if keys not set
    }

    const expectedSig = this.sign(data);
    return crypto.timingSafeEquals(
      Buffer.from(signature, 'hex'),
      Buffer.from(expectedSig, 'hex')
    );
  },

  // ═══════════════════════════════════════════════════════════════════════
  // CRDT OPERATIONS
  // ═══════════════════════════════════════════════════════════════════════

  /**
   * Generate unique message ID
   */
  generateMessageId() {
    const timestamp = Date.now();
    const random = crypto.randomBytes(8).toString('hex');
    return `${this.config.instanceId}-${timestamp}-${random}`;
  },

  /**
   * Increment vector clock and return current value
   */
  tick() {
    this.state.vectorClock[this.config.instanceId]++;
    return { ...this.state.vectorClock };
  },

  /**
   * Merge vector clocks (take max of each component)
   */
  mergeVectorClocks(clock1, clock2) {
    const merged = { ...clock1 };
    for (const [instance, count] of Object.entries(clock2)) {
      merged[instance] = Math.max(merged[instance] || 0, count);
    }
    return merged;
  },

  /**
   * Check if clock1 happens-before clock2
   */
  happensBefore(clock1, clock2) {
    let dominated = false;
    for (const instance of new Set([...Object.keys(clock1), ...Object.keys(clock2)])) {
      const v1 = clock1[instance] || 0;
      const v2 = clock2[instance] || 0;
      if (v1 > v2) return false;
      if (v1 < v2) dominated = true;
    }
    return dominated;
  },

  // ═══════════════════════════════════════════════════════════════════════
  // MESSAGE OPERATIONS
  // ═══════════════════════════════════════════════════════════════════════

  /**
   * Send a message (add to local CRDT)
   */
  send(to, content, options = {}) {
    const messageId = this.generateMessageId();
    const timestamp = Date.now();
    const vectorClock = this.tick();

    const message = {
      id: messageId,
      from: this.config.instanceId,
      to: to,
      content: content,
      timestamp: timestamp,
      vectorClock: vectorClock,
      type: options.type || 'message',
      priority: options.priority || 'normal',
      ttl: options.ttl || this.config.maxMessageAge
    };

    // Encrypt content
    const encryptedContent = this.encrypt(message.content);
    message.content = encryptedContent;

    // Sign the message
    message.signature = this.sign({
      id: message.id,
      from: message.from,
      to: message.to,
      timestamp: message.timestamp
    });

    // Generate hash for integrity
    message.hash = this.hashMessage(message);

    // Add to local store
    this.state.messages.set(messageId, message);

    // Add to pending sync
    this.state.pendingSync.push(messageId);

    console.log(`[CRDT] Message sent: ${messageId} -> ${to}`);

    return {
      messageId,
      timestamp,
      vectorClock
    };
  },

  /**
   * Receive messages for this instance
   */
  receive(includeRead = false) {
    const messages = [];

    for (const [id, message] of this.state.messages) {
      // Check if message is for us
      if (message.to === this.config.instanceId || message.to === 'ALL') {
        // Check TTL
        if (Date.now() - message.timestamp > message.ttl) {
          continue;
        }

        // Decrypt content
        try {
          const decryptedContent = this.decrypt(message.content);

          messages.push({
            id: message.id,
            from: message.from,
            content: decryptedContent,
            timestamp: message.timestamp,
            type: message.type,
            priority: message.priority,
            verified: this.verify({
              id: message.id,
              from: message.from,
              to: message.to,
              timestamp: message.timestamp
            }, message.signature)
          });
        } catch (error) {
          console.error(`[CRDT] Failed to decrypt message ${id}:`, error.message);
        }
      }
    }

    // Sort by vector clock (causal order)
    messages.sort((a, b) => {
      const msgA = this.state.messages.get(a.id);
      const msgB = this.state.messages.get(b.id);
      if (this.happensBefore(msgA.vectorClock, msgB.vectorClock)) return -1;
      if (this.happensBefore(msgB.vectorClock, msgA.vectorClock)) return 1;
      return a.timestamp - b.timestamp;
    });

    return messages;
  },

  /**
   * Hash a message for integrity verification
   */
  hashMessage(message) {
    const hash = crypto.createHash(this.config.hashAlgorithm);
    hash.update(JSON.stringify({
      id: message.id,
      from: message.from,
      to: message.to,
      timestamp: message.timestamp,
      content: message.content
    }));
    return hash.digest('hex');
  },

  // ═══════════════════════════════════════════════════════════════════════
  // PEER MANAGEMENT (OR-Set CRDT)
  // ═══════════════════════════════════════════════════════════════════════

  /**
   * Add a peer (OR-Set add)
   */
  addPeer(peerId, peerData = {}) {
    const timestamp = Date.now();
    this.state.peers.added.set(peerId, {
      timestamp,
      data: peerData
    });
    console.log(`[CRDT] Peer added: ${peerId}`);
  },

  /**
   * Remove a peer (OR-Set remove)
   */
  removePeer(peerId) {
    const timestamp = Date.now();
    this.state.peers.removed.set(peerId, timestamp);
    console.log(`[CRDT] Peer removed: ${peerId}`);
  },

  /**
   * Get active peers (OR-Set lookup)
   */
  getPeers() {
    const peers = [];
    for (const [peerId, addData] of this.state.peers.added) {
      const removeTime = this.state.peers.removed.get(peerId) || 0;
      if (addData.timestamp > removeTime) {
        peers.push({
          id: peerId,
          ...addData.data,
          addedAt: addData.timestamp
        });
      }
    }
    return peers;
  },

  // ═══════════════════════════════════════════════════════════════════════
  // SYNC OPERATIONS
  // ═══════════════════════════════════════════════════════════════════════

  /**
   * Merge remote state into local state
   */
  merge(remoteState) {
    let mergedCount = 0;

    // Merge vector clocks
    this.state.vectorClock = this.mergeVectorClocks(
      this.state.vectorClock,
      remoteState.vectorClock
    );

    // Merge messages (LWW - keep newest)
    for (const [id, message] of Object.entries(remoteState.messages)) {
      const local = this.state.messages.get(id);
      if (!local || message.timestamp > local.timestamp) {
        // Verify integrity
        const expectedHash = this.hashMessage(message);
        if (message.hash === expectedHash) {
          this.state.messages.set(id, message);
          mergedCount++;
        } else {
          console.warn(`[CRDT] Message ${id} failed integrity check`);
        }
      }
    }

    // Merge peers (OR-Set merge)
    for (const [peerId, addData] of Object.entries(remoteState.peers.added)) {
      const local = this.state.peers.added.get(peerId);
      if (!local || addData.timestamp > local.timestamp) {
        this.state.peers.added.set(peerId, addData);
      }
    }

    for (const [peerId, removeTime] of Object.entries(remoteState.peers.removed)) {
      const local = this.state.peers.removed.get(peerId) || 0;
      if (removeTime > local) {
        this.state.peers.removed.set(peerId, removeTime);
      }
    }

    console.log(`[CRDT] Merged ${mergedCount} messages from remote state`);

    // Clean expired messages
    this.cleanExpired();

    return mergedCount;
  },

  /**
   * Export state for sync
   */
  exportState() {
    return {
      vectorClock: this.state.vectorClock,
      messages: Object.fromEntries(this.state.messages),
      peers: {
        added: Object.fromEntries(this.state.peers.added),
        removed: Object.fromEntries(this.state.peers.removed)
      },
      exportedAt: Date.now(),
      exportedBy: this.config.instanceId
    };
  },

  /**
   * Clean expired messages
   */
  cleanExpired() {
    const now = Date.now();
    let cleaned = 0;

    for (const [id, message] of this.state.messages) {
      if (now - message.timestamp > message.ttl) {
        this.state.messages.delete(id);
        cleaned++;
      }
    }

    if (cleaned > 0) {
      console.log(`[CRDT] Cleaned ${cleaned} expired messages`);
    }
  },

  // ═══════════════════════════════════════════════════════════════════════
  // PERSISTENCE
  // ═══════════════════════════════════════════════════════════════════════

  /**
   * Save state to disk
   */
  async saveState() {
    try {
      const dataPath = path.resolve(this.config.dataDir);

      // Save messages
      const messagesPath = path.join(dataPath, this.config.messagesFile);
      await fs.writeFile(
        messagesPath,
        JSON.stringify(Object.fromEntries(this.state.messages), null, 2)
      );

      // Save vector clock
      const clockPath = path.join(dataPath, this.config.stateFile);
      await fs.writeFile(
        clockPath,
        JSON.stringify(this.state.vectorClock, null, 2)
      );

      // Save peers
      const peersPath = path.join(dataPath, this.config.peersFile);
      await fs.writeFile(
        peersPath,
        JSON.stringify({
          added: Object.fromEntries(this.state.peers.added),
          removed: Object.fromEntries(this.state.peers.removed)
        }, null, 2)
      );

      return true;
    } catch (error) {
      console.error('[CRDT] Error saving state:', error.message);
      return false;
    }
  },

  /**
   * Load state from disk
   */
  async loadState() {
    try {
      const dataPath = path.resolve(this.config.dataDir);

      // Load messages
      const messagesPath = path.join(dataPath, this.config.messagesFile);
      try {
        const messagesData = await fs.readFile(messagesPath, 'utf8');
        const messages = JSON.parse(messagesData);
        this.state.messages = new Map(Object.entries(messages));
      } catch (e) {
        // File doesn't exist, start fresh
      }

      // Load vector clock
      const clockPath = path.join(dataPath, this.config.stateFile);
      try {
        const clockData = await fs.readFile(clockPath, 'utf8');
        this.state.vectorClock = JSON.parse(clockData);
      } catch (e) {
        // File doesn't exist, start fresh
      }

      // Load peers
      const peersPath = path.join(dataPath, this.config.peersFile);
      try {
        const peersData = await fs.readFile(peersPath, 'utf8');
        const peers = JSON.parse(peersData);
        this.state.peers.added = new Map(Object.entries(peers.added || {}));
        this.state.peers.removed = new Map(Object.entries(peers.removed || {}));
      } catch (e) {
        // File doesn't exist, start fresh
      }

      return true;
    } catch (error) {
      console.error('[CRDT] Error loading state:', error.message);
      return false;
    }
  },

  // ═══════════════════════════════════════════════════════════════════════
  // STATUS & REPORTING
  // ═══════════════════════════════════════════════════════════════════════

  /**
   * Get current status
   */
  getStatus() {
    const messages = this.receive();

    return {
      name: 'TRINITY_SECURE_CRDT_COMMS',
      version: '1.0.0',
      instanceId: this.config.instanceId,

      encryption: {
        enabled: !!this.state.keys.encryption,
        algorithm: this.config.encryptionAlgorithm
      },

      statistics: {
        totalMessages: this.state.messages.size,
        unreadMessages: messages.length,
        knownPeers: this.getPeers().length,
        pendingSync: this.state.pendingSync.length
      },

      vectorClock: this.state.vectorClock,

      peers: this.getPeers().map(p => p.id)
    };
  },

  /**
   * Generate hub report
   */
  generateHubReport() {
    const status = this.getStatus();

    return {
      component: 'TRINITY_SECURE_CRDT_COMMS',
      timestamp: new Date().toISOString(),
      health: status.statistics.totalMessages > 0 ? 'ACTIVE' : 'IDLE',

      summary: `Instance: ${status.instanceId}. ` +
               `${status.statistics.totalMessages} messages, ${status.statistics.unreadMessages} unread. ` +
               `${status.statistics.knownPeers} peers. ` +
               `Encryption: ${status.encryption.enabled ? 'ENABLED' : 'DISABLED'}`,

      metrics: {
        messages: status.statistics.totalMessages,
        unread: status.statistics.unreadMessages,
        peers: status.statistics.knownPeers,
        pendingSync: status.statistics.pendingSync
      },

      details: status
    };
  }
};

// ═══════════════════════════════════════════════════════════════════════════
// EXPORTS
// ═══════════════════════════════════════════════════════════════════════════

module.exports = TrinitySecureCRDT;

// ═══════════════════════════════════════════════════════════════════════════
// STANDALONE TEST
// ═══════════════════════════════════════════════════════════════════════════

if (require.main === module) {
  (async () => {
    console.log('═══════════════════════════════════════════════════════════');
    console.log('TRINITY SECURE CRDT COMMUNICATIONS - TEST RUN');
    console.log('═══════════════════════════════════════════════════════════\n');

    // Initialize with encryption
    await TrinitySecureCRDT.initialize('T1_Desktop', 'trinity-shared-secret-2025');

    // Add some peers
    TrinitySecureCRDT.addPeer('Cloud', { type: 'cloud_cli', location: 'linux' });
    TrinitySecureCRDT.addPeer('C1_Mechanic', { type: 'local', computer: 'PC1' });

    // Send some messages
    console.log('\nSending test messages...\n');

    TrinitySecureCRDT.send('Cloud', {
      type: 'status_update',
      content: 'Active Inference Core operational'
    }, { priority: 'high' });

    TrinitySecureCRDT.send('ALL', {
      type: 'broadcast',
      content: 'CRDT communication layer initialized'
    });

    TrinitySecureCRDT.send('C1_Mechanic', {
      type: 'task_report',
      content: 'Building foundational systems'
    });

    // Save state
    await TrinitySecureCRDT.saveState();
    console.log('State saved to disk.');

    // Get status
    console.log('\n═══════════════════════════════════════════════════════════');
    console.log('STATUS REPORT');
    console.log('═══════════════════════════════════════════════════════════\n');

    console.log(JSON.stringify(TrinitySecureCRDT.getStatus(), null, 2));

    console.log('\n═══════════════════════════════════════════════════════════');
    console.log('HUB REPORT');
    console.log('═══════════════════════════════════════════════════════════\n');

    console.log(JSON.stringify(TrinitySecureCRDT.generateHubReport(), null, 2));

    console.log('\n═══════════════════════════════════════════════════════════');
    console.log('EXPORT STATE (for sync)');
    console.log('═══════════════════════════════════════════════════════════\n');

    const exported = TrinitySecureCRDT.exportState();
    console.log(`Exported ${Object.keys(exported.messages).length} messages`);
    console.log(`Vector clock:`, exported.vectorClock);
  })();
}
