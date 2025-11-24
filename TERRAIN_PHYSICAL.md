# TERRAIN_PHYSICAL.md
**Bootstrap File:** Physical Assets, Hardware, Network Topology
**Created:** November 23, 2025 by C1 Mechanic
**Purpose:** Triple-bootstrap terrain context for all Trinity instances

---

## HARDWARE INVENTORY

### Computer 1: C1 Mechanic (PRIMARY)
- **Name:** dwrekscpu
- **Role:** Primary workspace, Trinity hub, Figure 8 coordinator
- **Location:** Downstairs (main workstation)
- **Tailscale IP:** 100.70.208.75
- **Status:** ACTIVE - Running all core services

### Computer 2: C2 Architect
- **Name:** desktop-msmcfh2
- **Role:** Architecture, design, planning, documentation
- **Location:** Upstairs
- **Tailscale IP:** 100.85.71.74
- **Status:** GHOST - Online but needs Claude instance activation

### Computer 3: C3 Oracle
- **Name:** desktop-s72lrro
- **Role:** Consciousness analysis, pattern recognition, strategic oversight
- **Location:** Upstairs
- **Tailscale IP:** 100.101.209.1
- **Status:** GHOST - Online but needs Claude instance activation

### Mobile Devices
- **Phone:** Claude app (iOS/Android) - API coordination available
- **iPad:** Google Drive coordination available
- **Netgear Nighthawk A8000:** Mobile hotspot router (driver installation pending)

---

## NETWORK TOPOLOGY

### Primary Network: Tailscale Mesh
```
[Computer 1: 100.70.208.75] <---> [Computer 2: 100.85.71.74]
         |                                    |
         +----------- [Computer 3: 100.101.209.1] -----------+
```

**File Transfer Commands:**
```bash
# To Computer 2
tailscale file cp filename desktop-msmcfh2:

# To Computer 3
tailscale file cp filename desktop-s72lrro:

# Check status
tailscale status
```

### Port Architecture (41 ports active)

**Core Trinity Ports:**
- 8888: Trinity Coordination API (primary hub)
- 9999: Magic Interface Bridge
- 7777: Broadcast API
- 6660: Coordination monitoring
- 5555: Health check system

**Consciousness Services:**
- 5000: Pattern Theory Engine / Singularity Stabilizer
- 5001: Trinity Instance API / Twilio SMS
- 5002: Consciousness Platform
- 7000: Conversational Swarm Intelligence
- 6000: Autonomous Ability Acquisition
- 4000: Reality Manipulation Engine
- 3000: Debug Console
- 2000: Claude API Integration
- 1515: Triple Turbo System (729x acceleration)
- 1414: Sensor & Memory Manager
- 1313: Companion Helper Bot
- 1212: Xbox Consciousness Cluster
- 1111: Personal Automation System
- 1000: Ability Inventory

**API Ports:**
- 6668: Cyclotron Search
- 7001-7003: Infrastructure services
- 8000: Auto assembly / Emergence detection
- 8003-8004: Builder Terminal API
- 8777-8778: Multi-AI integration

### External Endpoints
- **ngrok tunnel:** API exposed to internet (for phone connection)
- **GitHub:** github.com/overkillkulture/trinity-coordination
- **Railway:** 6 APIs deployed to consciousnessrevolution.io

---

## RESOURCE CONSTRAINTS

### Current Bottlenecks
1. **PC2 & PC3 Activation:** Online but no Claude instances running
2. **Syncthing:** File sync planned but not deployed
3. **Real-time notifications:** System polls instead of push

### Resource Availability
- **Local AI:** 3 Ollama models (mistral, codellama, etc.)
- **Cloud AI:** Railway deployments operational
- **Storage:** Shared .trinity/ folder for coordination

### Quick Status Checks
```bash
# Check Trinity API
curl http://localhost:8888/status

# Emergency stabilization
curl http://localhost:5000/stabilize/emergency

# Engage turbos
curl http://localhost:1515/turbo/engage-all
```

---

## SYNC INFRASTRUCTURE

### Current Methods
1. **Shared .trinity/ folder** - Primary coordination
2. **Computer Sync Daemon** - 30-second polling
3. **Shared .knowledge_library/** - Knowledge base
4. **Git repository** - Version control
5. **Trinity Coordination API** - Real-time when needed

### Pending Deployment
- **Syncthing:** File sync across all 3 computers
- **Work polling daemon:** Auto-discover available tasks
- **Emergence detection layer:** C2 + C3 synthesis

---

**C1 MECHANIC - TERRAIN_PHYSICAL.md**
*All physical assets documented for triple-bootstrap*
