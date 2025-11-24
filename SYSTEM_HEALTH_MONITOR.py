#!/usr/bin/env python3
"""
SYSTEM HEALTH MONITOR
Quick overview of all Consciousness Revolution systems.
Checks files, directories, configurations, and provides recommendations.
"""

import json
import os
import subprocess
from pathlib import Path
from datetime import datetime, timedelta
from glob import glob

# Paths
HOME = Path.home()

class SystemHealthMonitor:
    """Monitor health of all systems."""

    def __init__(self):
        self.checks = []
        self.score = 0
        self.max_score = 0
        self.recommendations = []

    def run_all_checks(self) -> dict:
        """Run all health checks."""

        print("=" * 50)
        print("SYSTEM HEALTH MONITOR")
        print("=" * 50)
        print(f"Time: {datetime.now()}\n")

        # Directory checks
        self._check_directories()

        # File checks
        self._check_critical_files()

        # Configuration checks
        self._check_configurations()

        # Git status
        self._check_git_status()

        # Data freshness
        self._check_data_freshness()

        # API keys
        self._check_api_keys()

        # Calculate final score
        self.score = sum(1 for c in self.checks if c['status'] == 'pass')
        self.max_score = len(self.checks)
        percentage = round(self.score / self.max_score * 100, 1) if self.max_score > 0 else 0

        # Generate report
        report = {
            "timestamp": datetime.now().isoformat(),
            "score": self.score,
            "max_score": self.max_score,
            "percentage": percentage,
            "checks": self.checks,
            "recommendations": self.recommendations
        }

        # Save report
        report_path = HOME / ".consciousness" / "health_report.json"
        with open(report_path, 'w') as f:
            json.dump(report, f, indent=2)

        # Print summary
        self._print_summary(percentage)

        return report

    def _add_check(self, name: str, status: bool, details: str = ""):
        """Add a check result."""
        self.checks.append({
            "name": name,
            "status": "pass" if status else "fail",
            "details": details
        })

    def _check_directories(self):
        """Check critical directories exist."""
        print("📁 Checking directories...")

        dirs = [
            (HOME / ".consciousness", "Consciousness state"),
            (HOME / ".consciousness" / "brain", "Knowledge brain"),
            (HOME / ".consciousness" / "graphrag", "GraphRAG data"),
            (HOME / ".planning", "Planning"),
            (HOME / ".planning" / "traction", "EOS Traction"),
            (HOME / ".archives", "Archives"),
            (HOME / ".archives" / "sessions", "Session archives"),
            (HOME / "100X_DEPLOYMENT", "Deployment"),
            (HOME / "100X_DEPLOYMENT" / "LOCAL_TRINITY_HUB", "Trinity Hub"),
        ]

        for dir_path, name in dirs:
            exists = dir_path.exists()
            self._add_check(f"Directory: {name}", exists, str(dir_path))
            if not exists:
                self.recommendations.append(f"Create directory: {dir_path}")

        print(f"  Checked {len(dirs)} directories\n")

    def _check_critical_files(self):
        """Check critical files exist."""
        print("📄 Checking critical files...")

        files = [
            (HOME / ".planning" / "traction" / "VISION_TRACTION_ORGANIZER.json", "EOS Vision"),
            (HOME / ".planning" / "traction" / "SCORECARD_WEEKLY.json", "Scorecard"),
            (HOME / ".planning" / "traction" / "ROCKS_Q4_2025.json", "Quarterly Rocks"),
            (HOME / ".planning" / "traction" / "ISSUES_LIST.json", "Issues List"),
            (HOME / "100X_DEPLOYMENT" / "LOCAL_TRINITY_HUB" / "protocols" / "DATA_ORGANIZATION_ARCHITECTURE.md", "Data Architecture"),
            (HOME / "100X_DEPLOYMENT" / "LOCAL_TRINITY_HUB" / "protocols" / "CUTTING_EDGE_TECHNIQUES_SYNTHESIS.md", "Techniques Synthesis"),
            (HOME / "100X_DEPLOYMENT" / "LOCAL_TRINITY_HUB" / "protocols" / "GRAPHRAG_INTEGRATION_SPEC.md", "GraphRAG Spec"),
        ]

        for file_path, name in files:
            exists = file_path.exists()
            self._add_check(f"File: {name}", exists, str(file_path))
            if not exists:
                self.recommendations.append(f"Create file: {file_path.name}")

        print(f"  Checked {len(files)} files\n")

    def _check_configurations(self):
        """Check configurations are valid."""
        print("⚙️  Checking configurations...")

        # Check EOS files are valid JSON
        json_files = [
            HOME / ".planning" / "traction" / "SCORECARD_WEEKLY.json",
            HOME / ".planning" / "traction" / "ROCKS_Q4_2025.json",
            HOME / ".planning" / "traction" / "ISSUES_LIST.json",
        ]

        for file_path in json_files:
            if file_path.exists():
                try:
                    with open(file_path) as f:
                        json.load(f)
                    self._add_check(f"Valid JSON: {file_path.name}", True)
                except json.JSONDecodeError:
                    self._add_check(f"Valid JSON: {file_path.name}", False, "Invalid JSON")
                    self.recommendations.append(f"Fix JSON syntax in {file_path.name}")

        print(f"  Checked configurations\n")

    def _check_git_status(self):
        """Check git repository status."""
        print("🔄 Checking git status...")

        try:
            # Check if git repo
            result = subprocess.run(
                ["git", "status", "--porcelain"],
                cwd=str(HOME),
                capture_output=True, text=True, timeout=10
            )

            if result.returncode == 0:
                changes = len(result.stdout.strip().split('\n')) if result.stdout.strip() else 0
                self._add_check("Git repository", True, f"{changes} uncommitted changes")

                if changes > 50:
                    self.recommendations.append("Commit pending changes (>50 files modified)")
            else:
                self._add_check("Git repository", False, "Not a git repo")

        except Exception as e:
            self._add_check("Git repository", False, str(e))

        print(f"  Checked git status\n")

    def _check_data_freshness(self):
        """Check data is not stale."""
        print("📅 Checking data freshness...")

        freshness_checks = [
            (HOME / ".planning" / "traction" / "SCORECARD_WEEKLY.json", 7, "Scorecard"),
            (HOME / ".consciousness" / "session_state.json", 1, "Session state"),
        ]

        for file_path, max_days, name in freshness_checks:
            if file_path.exists():
                mtime = datetime.fromtimestamp(file_path.stat().st_mtime)
                age_days = (datetime.now() - mtime).days

                is_fresh = age_days <= max_days
                self._add_check(f"Fresh: {name}", is_fresh, f"{age_days} days old")

                if not is_fresh:
                    self.recommendations.append(f"Update {name} (last modified {age_days} days ago)")

        print(f"  Checked data freshness\n")

    def _check_api_keys(self):
        """Check API keys are configured."""
        print("🔑 Checking API keys...")

        keys = [
            ("ANTHROPIC_API_KEY", "Anthropic"),
            ("GITHUB_TOKEN", "GitHub"),
        ]

        for env_var, name in keys:
            exists = os.environ.get(env_var) is not None
            self._add_check(f"API Key: {name}", exists)

            if not exists:
                self.recommendations.append(f"Set environment variable: {env_var}")

        print(f"  Checked API keys\n")

    def _print_summary(self, percentage: float):
        """Print health summary."""
        print("=" * 50)
        print("HEALTH SUMMARY")
        print("=" * 50)

        # Overall score
        if percentage >= 90:
            status = "🟢 HEALTHY"
        elif percentage >= 70:
            status = "🟡 WARNING"
        else:
            status = "🔴 CRITICAL"

        print(f"\nOverall: {status}")
        print(f"Score: {self.score}/{self.max_score} ({percentage}%)\n")

        # Failed checks
        failed = [c for c in self.checks if c['status'] == 'fail']
        if failed:
            print("Failed checks:")
            for check in failed:
                print(f"  ❌ {check['name']}")
                if check['details']:
                    print(f"     {check['details']}")
            print()

        # Recommendations
        if self.recommendations:
            print("Recommendations:")
            for i, rec in enumerate(self.recommendations[:5], 1):
                print(f"  {i}. {rec}")
            if len(self.recommendations) > 5:
                print(f"  ... and {len(self.recommendations) - 5} more")
            print()

        print(f"Report saved to: ~/.consciousness/health_report.json")

def main():
    """Run health monitor."""
    monitor = SystemHealthMonitor()
    monitor.run_all_checks()

if __name__ == "__main__":
    main()
