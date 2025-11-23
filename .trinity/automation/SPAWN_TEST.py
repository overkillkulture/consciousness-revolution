#!/usr/bin/env python3
"""
Quick test of cloud spawning functionality
"""

import os
import sys

# Add parent to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from CLOUD_SPAWNER import CloudSpawner

def test_spawn():
    print("=== CLOUD SPAWNER TEST ===\n")

    try:
        spawner = CloudSpawner()
    except ValueError as e:
        print(f"ERROR: {e}")
        print("\nSet your API key:")
        print("  set ANTHROPIC_API_KEY=sk-ant-...")
        return

    # Simple test task
    task = """
    You are testing the Trinity cloud spawn system.

    Task: Generate a haiku about AI coordination.

    Then list 3 ways multiple AI instances could work together effectively.

    Keep response under 200 words.
    """

    print("Spawning test worker...\n")
    result = spawner.spawn(task, "haiku-test")

    if result:
        print("\n=== TEST PASSED ===")
        print("Cloud spawning is working!")
        print(f"\nOutput preview:\n{result[:300]}...")
    else:
        print("\n=== TEST FAILED ===")
        print("Check API key and try again")

if __name__ == "__main__":
    test_spawn()
