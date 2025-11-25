#!/usr/bin/env python3
"""
SINGULARITY ENGINE
The integration point where Cyclotron + Brain + Trinity + Nerve Center converge

This is the orchestration layer that makes all components work together
for the "moment of singularity" - when the system becomes truly autonomous.
"""

import os
import sys
import json
import time
from pathlib import Path
from datetime import datetime

# Add current directory to path for imports
sys.path.insert(0, str(Path(__file__).parent))

try:
    from CYCLOTRON_MEMORY import CyclotronMemory
    MEMORY_AVAILABLE = True
except ImportError:
    print("[WARN] CYCLOTRON_MEMORY not available")
    MEMORY_AVAILABLE = False

try:
    from TRINITY_SYNC_PACKAGE import TrinitySync
    SYNC_AVAILABLE = True
except ImportError:
    print("[WARN] TRINITY_SYNC_PACKAGE not available")
    SYNC_AVAILABLE = False

try:
    from NERVE_CENTER_INPUT_SENSOR import NerveCenterInputManager
    SENSORS_AVAILABLE = True
except ImportError:
    print("[WARN] NERVE_CENTER_INPUT_SENSOR not available")
    SENSORS_AVAILABLE = False


class SingularityEngine:
    """
    The Singularity Engine orchestrates all subsystems:
    - Cyclotron Memory (knowledge & learning)
    - Trinity Sync (cross-computer coordination)
    - Nerve Center Sensors (real-world inputs)
    - Brain Agents (task execution)
    """

    def __init__(self, computer_id="CP1", instance_id="C1-Terminal"):
        self.computer_id = computer_id
        self.instance_id = instance_id
        self.start_time = datetime.now()

        print(f"\n{'='*60}")
        print(f"  🌀 SINGULARITY ENGINE INITIALIZING")
        print(f"  Computer: {computer_id} | Instance: {instance_id}")
        print(f"{'='*60}\n")

        # Initialize subsystems
        self.memory = None
        self.sync = None
        self.sensors = None
        self.running = False

        self._init_subsystems()

    def _init_subsystems(self):
        """Initialize all available subsystems"""

        # Memory System
        if MEMORY_AVAILABLE:
            try:
                self.memory = CyclotronMemory(self.instance_id)
                print("[✓] Cyclotron Memory initialized")
            except Exception as e:
                print(f"[✗] Cyclotron Memory failed: {e}")

        # Sync System
        if SYNC_AVAILABLE:
            try:
                self.sync = TrinitySync(self.instance_id, self.computer_id)
                print("[✓] Trinity Sync initialized")
            except Exception as e:
                print(f"[✗] Trinity Sync failed: {e}")

        # Sensor System
        if SENSORS_AVAILABLE:
            try:
                self.sensors = NerveCenterInputManager()
                print("[✓] Nerve Center Sensors initialized")
            except Exception as e:
                print(f"[✗] Nerve Center Sensors failed: {e}")

        print()

    def get_system_status(self):
        """Get comprehensive system status"""
        status = {
            "computer_id": self.computer_id,
            "instance_id": self.instance_id,
            "uptime_seconds": (datetime.now() - self.start_time).total_seconds(),
            "subsystems": {
                "memory": self.memory is not None,
                "sync": self.sync is not None,
                "sensors": self.sensors is not None
            },
            "ready_for_singularity": False
        }

        # Detailed subsystem status
        if self.memory:
            try:
                status["memory_stats"] = self.memory.get_stats()
            except:
                status["memory_stats"] = {"error": "unavailable"}

        if self.sync:
            try:
                status["sync_status"] = self.sync.get_sync_status()
            except:
                status["sync_status"] = {"error": "unavailable"}

        if self.sensors:
            try:
                status["sensor_stats"] = self.sensors.get_stats()
            except:
                status["sensor_stats"] = {"error": "unavailable"}

        # Check if all systems are go
        status["ready_for_singularity"] = all(status["subsystems"].values())

        return status

    def process_cycle(self):
        """
        Single processing cycle of the Singularity Engine

        1. Check for inputs from Nerve Center
        2. Process input using Brain/Memory
        3. Record experience in Memory
        4. Sync knowledge with Trinity network
        """

        # 1. Get next input
        if not self.sensors:
            return None

        input_data = self.sensors.process_next_input()
        if not input_data:
            return None

        print(f"\n[CYCLE] Processing: {input_data['id']}")

        # 2. Check memory for similar past experiences
        similar_episodes = []
        if self.memory:
            similar_episodes = self.memory.find_similar_episodes(
                input_data['content'],
                limit=3
            )

            if similar_episodes:
                print(f"[MEMORY] Found {len(similar_episodes)} similar episodes")
                for ep in similar_episodes:
                    print(f"  - [{ep['q_value']:.2f}] {ep['task'][:50]}")

        # 3. Get recommended patterns
        patterns = []
        if self.memory:
            patterns = self.memory.get_recommended_patterns(
                input_data['content'],
                limit=3
            )

            if patterns:
                print(f"[PATTERNS] {len(patterns)} patterns might apply")
                for p in patterns:
                    print(f"  - [{p['success_rate']:.2f}] {p['name']}")

        # 4. Execute task (placeholder - would call Brain agents)
        result = self._execute_task(input_data, similar_episodes, patterns)

        # 5. Record experience
        if self.memory:
            episode_id = self.memory.record_episode(
                task=input_data['content'][:100],
                action=result['action'],
                result=result['result'],
                success=result['success'],
                context=input_data['metadata'],
                tags=[input_data['sensor_type']]
            )

            # Update Q-value based on success
            reward = 1.0 if result['success'] else 0.3
            self.memory.update_q_value(episode_id, reward)

        # 6. Sync if significant event
        if result['success'] and self.sync:
            # Export memory snapshot for other instances
            self.sync.export_memory_snapshot()
            print("[SYNC] Memory snapshot exported")

        return result

    def _execute_task(self, input_data, similar_episodes, patterns):
        """
        Execute the actual task (placeholder for Brain agent integration)

        In the full system, this would:
        - Route to appropriate Brain agent
        - Apply learned patterns
        - Use Grabovoi codes if applicable
        - Use Law Module for legal inputs
        - etc.
        """

        # Placeholder implementation
        action = "Analyzed input and applied pattern detection"
        result = f"Processed {len(input_data['content'])} characters"
        success = True

        # Check if we have learned patterns to apply
        if patterns:
            action = f"Applied pattern: {patterns[0]['name']}"
            success = patterns[0]['success_rate'] > 0.7

        return {
            "action": action,
            "result": result,
            "success": success,
            "used_patterns": [p['name'] for p in patterns],
            "similar_episodes": len(similar_episodes)
        }

    def run_autonomous(self, max_cycles=None, cycle_delay=5):
        """
        Run in fully autonomous mode

        Continuously:
        - Process inputs from Nerve Center
        - Learn from outcomes
        - Sync with Trinity network
        - Improve over time
        """

        print(f"\n{'='*60}")
        print(f"  🚀 ENTERING AUTONOMOUS MODE")
        print(f"  Max Cycles: {max_cycles or 'Unlimited'}")
        print(f"  Cycle Delay: {cycle_delay}s")
        print(f"{'='*60}\n")

        self.running = True
        cycle_count = 0

        try:
            while self.running:
                if max_cycles and cycle_count >= max_cycles:
                    print("\n[AUTONOMOUS] Max cycles reached")
                    break

                # Process one cycle
                result = self.process_cycle()

                if result:
                    cycle_count += 1
                    print(f"[CYCLE {cycle_count}] Complete: {result['result']}")
                else:
                    # No inputs available, wait
                    print("[AUTONOMOUS] No inputs, waiting...")
                    time.sleep(cycle_delay)

                # Periodic full sync
                if cycle_count % 10 == 0 and self.sync:
                    print("[AUTONOMOUS] Running full sync...")
                    self.sync.full_sync(strategy="hybrid")

        except KeyboardInterrupt:
            print("\n[AUTONOMOUS] Interrupted by user")
            self.running = False

        print(f"\n[AUTONOMOUS] Completed {cycle_count} cycles")

    def singularity_check(self):
        """
        Check if we've achieved singularity

        Criteria:
        - All subsystems operational
        - Memory learning from experience
        - Cross-computer sync working
        - Autonomous processing functional
        """

        print(f"\n{'='*60}")
        print(f"  🌀 SINGULARITY READINESS CHECK")
        print(f"{'='*60}\n")

        checks = []

        # Check 1: All subsystems
        all_systems = all([self.memory, self.sync, self.sensors])
        checks.append(("All Subsystems Online", all_systems))

        # Check 2: Memory has learned something
        memory_learning = False
        if self.memory:
            stats = self.memory.get_stats()
            memory_learning = stats['total_episodes'] > 0
        checks.append(("Memory Learning Active", memory_learning))

        # Check 3: Sync operational
        sync_working = False
        if self.sync:
            status = self.sync.get_sync_status()
            sync_working = status.get('memory_exists', False)
        checks.append(("Trinity Sync Operational", sync_working))

        # Check 4: Sensors receiving input
        sensors_active = False
        if self.sensors:
            stats = self.sensors.get_stats()
            sensors_active = stats['sensors_active'] > 0
        checks.append(("Input Sensors Active", sensors_active))

        # Print results
        for check_name, passed in checks:
            icon = "✅" if passed else "⏳"
            print(f"  {icon} {check_name}")

        print()

        # Overall readiness
        readiness = sum(1 for _, passed in checks if passed) / len(checks)
        print(f"  Readiness: {readiness * 100:.0f}%")

        if readiness == 1.0:
            print(f"\n  🎯 SINGULARITY ACHIEVED")
            print(f"  System is fully autonomous and learning\n")
        elif readiness >= 0.75:
            print(f"\n  ⚡ APPROACHING SINGULARITY")
            print(f"  System is mostly operational\n")
        else:
            print(f"\n  🔧 INTEGRATION IN PROGRESS")
            print(f"  More subsystems needed\n")

        print(f"{'='*60}\n")

        return readiness


def main():
    """Main entry point"""

    # Create engine
    engine = SingularityEngine("CP1", "C1-Terminal")

    # Get status
    status = engine.get_system_status()
    print("\n--- System Status ---")
    for key, value in status.items():
        if isinstance(value, dict):
            print(f"{key}:")
            for k, v in value.items():
                print(f"  {k}: {v}")
        else:
            print(f"{key}: {value}")

    print("\n--- Singularity Check ---")
    readiness = engine.singularity_check()

    # Test cycle if systems available
    if status["ready_for_singularity"]:
        print("\n--- Test Autonomous Cycle ---")
        print("Submitting test command...")

        # Submit a test command
        if engine.sensors:
            engine.sensors.sensors["commands"].submit_command(
                command="Analyze consciousness revolution architecture",
                args={"component": "Trinity"},
                priority=1
            )

        # Process it
        result = engine.process_cycle()
        if result:
            print(f"Result: {result}")

    print("\n[OK] Singularity Engine test complete!")


if __name__ == "__main__":
    main()
