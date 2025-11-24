#!/usr/bin/env python3
"""
BRAIN INTEGRATION HOOKS
Connects C2's architecture work with C1's Cyclotron/Spreadsheet Brain.
Provides data flow between systems.
"""

import json
from pathlib import Path
from datetime import datetime
from typing import Optional

# Paths
HOME = Path.home()
CONSCIOUSNESS = HOME / ".consciousness"
BRAIN_PATH = CONSCIOUSNESS / "brain"
CYCLOTRON_PATH = CONSCIOUSNESS / "cyclotron_core"
PLANNING_PATH = HOME / ".planning"
DEPLOYMENT = HOME / "100X_DEPLOYMENT"

class BrainIntegration:
    """Integration layer between C2 architecture and C1 brain."""

    def __init__(self):
        self.brain_path = BRAIN_PATH
        self.cyclotron_path = CYCLOTRON_PATH
        self.ensure_paths()

    def ensure_paths(self):
        """Ensure all required paths exist."""
        self.brain_path.mkdir(parents=True, exist_ok=True)
        self.cyclotron_path.mkdir(parents=True, exist_ok=True)

    # === SCORECARD → BRAIN HOOKS ===

    def push_scorecard_to_brain(self):
        """Push scorecard metrics to brain for pattern analysis."""
        scorecard_path = PLANNING_PATH / "traction" / "SCORECARD_WEEKLY.json"

        if not scorecard_path.exists():
            return {"error": "Scorecard not found"}

        with open(scorecard_path) as f:
            scorecard = json.load(f)

        # Extract metrics for brain
        metrics = []
        for metric in scorecard.get("scorecard", {}).get("measurables", []):
            metrics.append({
                "name": metric["name"],
                "goal": metric.get("goal"),
                "actual": metric.get("actual"),
                "on_track": metric.get("on_track"),
                "timestamp": datetime.now().isoformat()
            })

        # Save to brain
        brain_metrics = self.brain_path / "scorecard_metrics.json"
        with open(brain_metrics, 'w') as f:
            json.dump({
                "metrics": metrics,
                "updated": datetime.now().isoformat()
            }, f, indent=2)

        print(f"Pushed {len(metrics)} metrics to brain")
        return {"pushed": len(metrics)}

    # === ROCKS → BRAIN HOOKS ===

    def push_rocks_to_brain(self):
        """Push rocks status to brain for tracking."""
        rocks_path = PLANNING_PATH / "traction" / "ROCKS_Q4_2025.json"

        if not rocks_path.exists():
            return {"error": "Rocks not found"}

        with open(rocks_path) as f:
            rocks_data = json.load(f)

        # Extract for brain
        rocks = []
        for rock in rocks_data.get("rocks", []):
            rocks.append({
                "id": rock.get("id"),
                "rock": rock.get("rock"),
                "owner": rock.get("owner"),
                "status": rock.get("status"),
                "milestone_progress": sum(1 for m in rock.get("milestones", []) if m.get("done")),
                "total_milestones": len(rock.get("milestones", []))
            })

        # Save to brain
        brain_rocks = self.brain_path / "rocks_status.json"
        with open(brain_rocks, 'w') as f:
            json.dump({
                "rocks": rocks,
                "quarter": rocks_data.get("quarter"),
                "updated": datetime.now().isoformat()
            }, f, indent=2)

        print(f"Pushed {len(rocks)} rocks to brain")
        return {"pushed": len(rocks)}

    # === ISSUES → BRAIN HOOKS ===

    def push_issues_to_brain(self):
        """Push issues for pattern analysis."""
        issues_path = PLANNING_PATH / "traction" / "ISSUES_LIST.json"

        if not issues_path.exists():
            return {"error": "Issues not found"}

        with open(issues_path) as f:
            issues_data = json.load(f)

        # Combine short and long term
        all_issues = []

        for issue in issues_data.get("issues", {}).get("short_term", []):
            issue["term"] = "short"
            all_issues.append(issue)

        for issue in issues_data.get("issues", {}).get("long_term", []):
            issue["term"] = "long"
            all_issues.append(issue)

        # Save to brain
        brain_issues = self.brain_path / "issues_active.json"
        with open(brain_issues, 'w') as f:
            json.dump({
                "issues": all_issues,
                "updated": datetime.now().isoformat()
            }, f, indent=2)

        print(f"Pushed {len(all_issues)} issues to brain")
        return {"pushed": len(all_issues)}

    # === GRAPHRAG → CYCLOTRON HOOKS ===

    def push_entities_to_cyclotron(self):
        """Push GraphRAG entities to Cyclotron index."""
        graphrag_path = CONSCIOUSNESS / "graphrag" / "MASTER_INDEX.json"

        if not graphrag_path.exists():
            return {"error": "GraphRAG index not found"}

        with open(graphrag_path) as f:
            graphrag = json.load(f)

        # Convert to Cyclotron atoms
        atoms = []
        for entity in graphrag.get("entities", []):
            atom = {
                "type": "entity",
                "name": entity.get("name"),
                "entity_type": entity.get("type"),
                "description": entity.get("description", ""),
                "sources": entity.get("sources", []),
                "indexed_at": datetime.now().isoformat()
            }
            atoms.append(atom)

        # Save to Cyclotron
        cyclotron_entities = self.cyclotron_path / "entities.json"
        with open(cyclotron_entities, 'w') as f:
            json.dump({
                "atoms": atoms,
                "total": len(atoms),
                "updated": datetime.now().isoformat()
            }, f, indent=2)

        print(f"Pushed {len(atoms)} entities to Cyclotron")
        return {"pushed": len(atoms)}

    # === KNOWLEDGE → BRAIN HOOKS ===

    def push_knowledge_to_brain(self):
        """Push knowledge atoms to brain for learning."""
        knowledge_index = BRAIN_PATH / "INDEX.json"

        if not knowledge_index.exists():
            return {"skipped": "No knowledge index yet"}

        with open(knowledge_index) as f:
            index = json.load(f)

        # Create summary for brain
        summary = {
            "total_atoms": index.get("stats", {}).get("total", 0),
            "by_type": index.get("stats", {}).get("by_type", {}),
            "top_tags": sorted(
                [(tag, len(atoms)) for tag, atoms in index.get("tags", {}).items()],
                key=lambda x: x[1],
                reverse=True
            )[:20],
            "sources": list(index.get("sources", {}).keys()),
            "updated": datetime.now().isoformat()
        }

        # Save summary
        brain_knowledge = self.brain_path / "knowledge_summary.json"
        with open(brain_knowledge, 'w') as f:
            json.dump(summary, f, indent=2)

        print(f"Pushed knowledge summary ({summary['total_atoms']} atoms) to brain")
        return summary

    # === SYNC ALL ===

    def sync_all(self):
        """Push all data to brain."""
        print("=" * 50)
        print("SYNCING ALL DATA TO BRAIN")
        print("=" * 50)

        results = {}

        print("\n1. Scorecard...")
        results["scorecard"] = self.push_scorecard_to_brain()

        print("\n2. Rocks...")
        results["rocks"] = self.push_rocks_to_brain()

        print("\n3. Issues...")
        results["issues"] = self.push_issues_to_brain()

        print("\n4. Entities...")
        results["entities"] = self.push_entities_to_cyclotron()

        print("\n5. Knowledge...")
        results["knowledge"] = self.push_knowledge_to_brain()

        print("\n" + "=" * 50)
        print("SYNC COMPLETE")
        print("=" * 50)

        return results

    # === BRAIN → EOS HOOKS (reverse direction) ===

    def pull_priorities_from_brain(self) -> list:
        """Get priorities from brain to influence EOS."""
        priorities_path = self.brain_path / "priorities.json"

        if priorities_path.exists():
            with open(priorities_path) as f:
                return json.load(f).get("priorities", [])
        return []

    def pull_patterns_from_brain(self) -> list:
        """Get recurring patterns/issues from brain."""
        patterns_path = self.brain_path / "recurring_issues.json"

        if patterns_path.exists():
            with open(patterns_path) as f:
                return json.load(f).get("issues", [])
        return []

    # === STATUS CHECK ===

    def get_integration_status(self) -> dict:
        """Check status of all integrations."""
        status = {
            "brain_files": len(list(self.brain_path.glob("*.json"))),
            "cyclotron_files": len(list(self.cyclotron_path.glob("*.json"))) if self.cyclotron_path.exists() else 0,
            "scorecard_exists": (PLANNING_PATH / "traction" / "SCORECARD_WEEKLY.json").exists(),
            "rocks_exists": (PLANNING_PATH / "traction" / "ROCKS_Q4_2025.json").exists(),
            "issues_exists": (PLANNING_PATH / "traction" / "ISSUES_LIST.json").exists(),
            "graphrag_exists": (CONSCIOUSNESS / "graphrag" / "MASTER_INDEX.json").exists(),
            "knowledge_exists": (BRAIN_PATH / "INDEX.json").exists(),
        }

        status["ready"] = all([
            status["scorecard_exists"],
            status["rocks_exists"],
            status["issues_exists"]
        ])

        return status

def main():
    """Run brain integration."""
    import sys

    integration = BrainIntegration()

    if len(sys.argv) > 1:
        command = sys.argv[1]

        if command == "status":
            status = integration.get_integration_status()
            print("\nBrain Integration Status:")
            for key, value in status.items():
                symbol = "✅" if value else "❌" if isinstance(value, bool) else value
                print(f"  {key}: {symbol}")

        elif command == "sync":
            integration.sync_all()

        elif command == "scorecard":
            integration.push_scorecard_to_brain()

        elif command == "rocks":
            integration.push_rocks_to_brain()

        elif command == "issues":
            integration.push_issues_to_brain()

        else:
            print(f"Unknown command: {command}")
    else:
        # Default: show status and sync
        print("Brain Integration Hooks")
        print("=" * 50)

        status = integration.get_integration_status()
        print("\nStatus:")
        for key, value in status.items():
            symbol = "✅" if value else "❌" if isinstance(value, bool) else value
            print(f"  {key}: {symbol}")

        if status["ready"]:
            print("\nRunning sync...")
            integration.sync_all()
        else:
            print("\nNot ready - missing EOS files")

if __name__ == "__main__":
    main()
