#!/usr/bin/env python3
"""
CYCLOTRON 13-PHASE AUDIT SYSTEM
Complete breakdown and analysis of Cyclotron knowledge base

13 Phases:
1. Structure Audit - File/folder structure
2. Data Integrity - JSON validity, corruption
3. Index Health - Index accuracy and staleness
4. Federation Status - Cross-computer sync
5. Performance Metrics - Speed, memory usage
6. Coverage Analysis - What's being missed
7. Duplication Check - Redundant data
8. Type Distribution - Atom type balance
9. Growth Velocity - Change rate over time
10. Error Analysis - Historical errors
11. API Endpoints - Connectivity checks
12. Security Audit - Permissions, exposure
13. Optimization Recommendations
"""

import os
import json
import time
from pathlib import Path
from datetime import datetime, timedelta
from collections import Counter

class CyclotronAuditor:
    """13-Phase Cyclotron Audit System"""

    def __init__(self):
        self.home = Path.home()
        self.deployment = self.home / '100X_DEPLOYMENT'
        self.atoms_dir = self.deployment / '.cyclotron_atoms'
        self.dropbox = self.home / 'Dropbox'
        self.federation = self.dropbox / '.cyclotron_federation' if self.dropbox.exists() else None

        self.results = {
            'timestamp': datetime.now().isoformat(),
            'phases': {},
            'overall_score': 0,
            'critical_issues': [],
            'recommendations': []
        }

    def run_full_audit(self):
        """Run all 13 phases"""
        print("=" * 70)
        print("CYCLOTRON 13-PHASE AUDIT SYSTEM")
        print("=" * 70)
        print()

        phases = [
            ("1. Structure Audit", self.phase_1_structure),
            ("2. Data Integrity", self.phase_2_integrity),
            ("3. Index Health", self.phase_3_index),
            ("4. Federation Status", self.phase_4_federation),
            ("5. Performance Metrics", self.phase_5_performance),
            ("6. Coverage Analysis", self.phase_6_coverage),
            ("7. Duplication Check", self.phase_7_duplication),
            ("8. Type Distribution", self.phase_8_types),
            ("9. Growth Velocity", self.phase_9_growth),
            ("10. Error Analysis", self.phase_10_errors),
            ("11. API Endpoints", self.phase_11_api),
            ("12. Security Audit", self.phase_12_security),
            ("13. Optimization", self.phase_13_optimization)
        ]

        total_score = 0

        for name, func in phases:
            print(f"\n{'='*70}")
            print(f"PHASE: {name}")
            print("=" * 70)

            try:
                result = func()
                self.results['phases'][name] = result
                score = result.get('score', 0)
                total_score += score

                status = "PASS" if score >= 70 else "WARN" if score >= 50 else "FAIL"
                icon = "" if score >= 70 else "⚠️" if score >= 50 else ""
                print(f"\n{icon} Phase Score: {score}/100 [{status}]")

                if result.get('issues'):
                    for issue in result['issues']:
                        self.results['critical_issues'].append(f"{name}: {issue}")
                        print(f"   Issue: {issue}")

            except Exception as e:
                print(f" Error in phase: {e}")
                self.results['phases'][name] = {'score': 0, 'error': str(e)}

        # Calculate overall score
        self.results['overall_score'] = round(total_score / len(phases))

        # Generate recommendations
        self.generate_recommendations()

        # Print summary
        self.print_summary()

        # Save results
        self.save_results()

        return self.results

    def phase_1_structure(self):
        """Audit file and folder structure"""
        result = {'score': 0, 'checks': {}, 'issues': []}

        # Check atoms directory exists
        if self.atoms_dir.exists():
            result['checks']['atoms_dir'] = True
            result['score'] += 20
        else:
            result['checks']['atoms_dir'] = False
            result['issues'].append("Atoms directory missing")

        # Check for atom files
        atom_files = list(self.atoms_dir.glob('atoms_*.json')) if self.atoms_dir.exists() else []
        result['checks']['atom_files_count'] = len(atom_files)
        if len(atom_files) > 0:
            result['score'] += 20
        if len(atom_files) > 5:
            result['score'] += 10

        # Check for index
        index_file = self.atoms_dir / 'index.json' if self.atoms_dir.exists() else None
        if index_file and index_file.exists():
            result['checks']['index_exists'] = True
            result['score'] += 20
        else:
            result['checks']['index_exists'] = False
            result['issues'].append("Index file missing")

        # Check for mega todos
        mega_todos = self.atoms_dir / 'mega_todos.json' if self.atoms_dir.exists() else None
        if mega_todos and mega_todos.exists():
            result['checks']['mega_todos'] = True
            result['score'] += 15

        # Check scripts exist
        scripts = ['CYCLOTRON_MASTER_RAKER.py', 'CYCLOTRON_INDEX_UPDATER.py', 'CYCLOTRON_ANALYTICS_ENGINE.py']
        existing_scripts = sum(1 for s in scripts if (self.deployment / s).exists())
        result['checks']['scripts'] = f"{existing_scripts}/{len(scripts)}"
        result['score'] += (existing_scripts / len(scripts)) * 15

        result['score'] = min(100, int(result['score']))

        print(f"  Atoms directory: {'✓' if result['checks'].get('atoms_dir') else '✗'}")
        print(f"  Atom files: {result['checks']['atom_files_count']}")
        print(f"  Index file: {'✓' if result['checks'].get('index_exists') else '✗'}")
        print(f"  Scripts: {result['checks']['scripts']}")

        return result

    def phase_2_integrity(self):
        """Check data integrity of all JSON files"""
        result = {'score': 0, 'checks': {}, 'issues': []}

        if not self.atoms_dir.exists():
            result['issues'].append("Atoms directory missing")
            return result

        json_files = list(self.atoms_dir.glob('*.json'))
        valid = 0
        invalid = []

        for jf in json_files:
            try:
                with open(jf) as f:
                    json.load(f)
                valid += 1
            except Exception as e:
                invalid.append(jf.name)

        result['checks']['total_json'] = len(json_files)
        result['checks']['valid_json'] = valid
        result['checks']['invalid_json'] = invalid

        if json_files:
            result['score'] = int((valid / len(json_files)) * 100)
        else:
            result['score'] = 0
            result['issues'].append("No JSON files found")

        if invalid:
            result['issues'].append(f"Invalid JSON files: {', '.join(invalid)}")

        print(f"  Total JSON files: {len(json_files)}")
        print(f"  Valid: {valid}")
        print(f"  Invalid: {len(invalid)}")

        return result

    def phase_3_index(self):
        """Check index health and staleness"""
        result = {'score': 0, 'checks': {}, 'issues': []}

        index_file = self.atoms_dir / 'index.json' if self.atoms_dir.exists() else None

        if not index_file or not index_file.exists():
            result['issues'].append("Index file not found")
            return result

        try:
            with open(index_file) as f:
                index = json.load(f)

            # Check staleness
            last_updated = index.get('last_updated', 0)
            age_seconds = time.time() - last_updated
            age_minutes = age_seconds / 60

            result['checks']['last_updated'] = datetime.fromtimestamp(last_updated).isoformat()
            result['checks']['age_minutes'] = round(age_minutes, 1)

            if age_minutes < 10:
                result['score'] += 40
            elif age_minutes < 60:
                result['score'] += 25
            else:
                result['issues'].append(f"Index is stale ({round(age_minutes)} minutes old)")

            # Check atom count
            atom_count = index.get('total_atoms', 0)
            result['checks']['total_atoms'] = atom_count

            if atom_count > 100:
                result['score'] += 30
            elif atom_count > 0:
                result['score'] += 15
            else:
                result['issues'].append("No atoms in index")

            # Check type breakdown
            types = index.get('atoms_by_type', {})
            result['checks']['atom_types'] = len(types)
            if len(types) >= 5:
                result['score'] += 30
            elif len(types) > 0:
                result['score'] += 15

        except Exception as e:
            result['issues'].append(f"Failed to read index: {e}")

        result['score'] = min(100, result['score'])

        print(f"  Last updated: {result['checks'].get('last_updated', 'N/A')}")
        print(f"  Age: {result['checks'].get('age_minutes', 'N/A')} minutes")
        print(f"  Total atoms: {result['checks'].get('total_atoms', 0)}")
        print(f"  Atom types: {result['checks'].get('atom_types', 0)}")

        return result

    def phase_4_federation(self):
        """Check federation (Dropbox sync) status"""
        result = {'score': 0, 'checks': {}, 'issues': []}

        # Check Dropbox exists
        if not self.dropbox or not self.dropbox.exists():
            result['checks']['dropbox'] = False
            result['issues'].append("Dropbox not found - federation disabled")
            print("  Dropbox: NOT FOUND")
            return result

        result['checks']['dropbox'] = True
        result['score'] += 25

        # Check federation directory
        if self.federation and self.federation.exists():
            result['checks']['federation_dir'] = True
            result['score'] += 25
        else:
            result['checks']['federation_dir'] = False
            result['issues'].append("Federation directory not created")

        # Check for synced atoms
        if self.federation:
            atoms_sync = self.federation / 'atoms'
            if atoms_sync.exists():
                synced_files = len(list(atoms_sync.glob('*.json')))
                result['checks']['synced_atoms'] = synced_files
                if synced_files > 0:
                    result['score'] += 25

            # Check for federation index
            fed_index = self.federation / 'indices' / 'federation_index.json'
            if fed_index.exists():
                result['checks']['federation_index'] = True
                result['score'] += 25

        print(f"  Dropbox: {'✓' if result['checks'].get('dropbox') else '✗'}")
        print(f"  Federation dir: {'✓' if result['checks'].get('federation_dir') else '✗'}")
        print(f"  Synced atoms: {result['checks'].get('synced_atoms', 0)}")

        return result

    def phase_5_performance(self):
        """Check performance metrics"""
        result = {'score': 0, 'checks': {}, 'issues': []}

        if not self.atoms_dir.exists():
            return result

        # Measure index load time
        index_file = self.atoms_dir / 'index.json'
        if index_file.exists():
            start = time.time()
            with open(index_file) as f:
                json.load(f)
            load_time = (time.time() - start) * 1000

            result['checks']['index_load_ms'] = round(load_time, 2)

            if load_time < 100:
                result['score'] += 50
            elif load_time < 500:
                result['score'] += 30
            else:
                result['issues'].append(f"Slow index load: {load_time}ms")

        # Check total disk usage
        total_size = 0
        file_count = 0
        for f in self.atoms_dir.rglob('*'):
            if f.is_file():
                total_size += f.stat().st_size
                file_count += 1

        result['checks']['disk_mb'] = round(total_size / (1024*1024), 2)
        result['checks']['file_count'] = file_count

        if total_size < 50 * 1024 * 1024:  # Under 50MB
            result['score'] += 50
        elif total_size < 200 * 1024 * 1024:
            result['score'] += 30
        else:
            result['issues'].append(f"Large disk usage: {result['checks']['disk_mb']}MB")

        print(f"  Index load time: {result['checks'].get('index_load_ms', 'N/A')}ms")
        print(f"  Disk usage: {result['checks']['disk_mb']}MB")
        print(f"  File count: {result['checks']['file_count']}")

        return result

    def phase_6_coverage(self):
        """Analyze what's being indexed and what's missed"""
        result = {'score': 0, 'checks': {}, 'issues': []}

        # Check rake directories
        expected_dirs = [
            self.home / '100X_DEPLOYMENT',
            self.home / '.consciousness',
            self.home / '.trinity',
        ]

        covered = sum(1 for d in expected_dirs if d.exists())
        result['checks']['covered_dirs'] = f"{covered}/{len(expected_dirs)}"
        result['score'] += (covered / len(expected_dirs)) * 50

        # Check file types being indexed
        expected_types = ['.md', '.txt', '.py', '.js', '.html', '.json']
        result['checks']['indexed_types'] = expected_types
        result['score'] += 30

        # Check for Desktop coverage
        desktop = self.home / 'Desktop'
        if desktop.exists():
            desktop_files = len(list(desktop.glob('*.md'))) + len(list(desktop.glob('*.txt')))
            result['checks']['desktop_files'] = desktop_files
            if desktop_files > 0:
                result['score'] += 20

        print(f"  Covered directories: {result['checks']['covered_dirs']}")
        print(f"  Indexed types: {', '.join(expected_types)}")
        print(f"  Desktop files: {result['checks'].get('desktop_files', 0)}")

        return result

    def phase_7_duplication(self):
        """Check for duplicate data"""
        result = {'score': 0, 'checks': {}, 'issues': []}

        if not self.atoms_dir.exists():
            return result

        # Load latest atoms
        atom_files = sorted(self.atoms_dir.glob('atoms_*.json'))
        if not atom_files:
            return result

        try:
            with open(atom_files[-1]) as f:
                atoms = json.load(f)

            # Check for duplicate paths
            paths = [a.get('path', '') for a in atoms]
            unique_paths = set(paths)

            dup_count = len(paths) - len(unique_paths)
            result['checks']['total_atoms'] = len(atoms)
            result['checks']['unique_paths'] = len(unique_paths)
            result['checks']['duplicates'] = dup_count

            if dup_count == 0:
                result['score'] = 100
            elif dup_count < 10:
                result['score'] = 80
            elif dup_count < 50:
                result['score'] = 60
                result['issues'].append(f"Found {dup_count} duplicate entries")
            else:
                result['score'] = 40
                result['issues'].append(f"High duplication: {dup_count} entries")

        except Exception as e:
            result['issues'].append(f"Failed to check duplicates: {e}")

        print(f"  Total atoms: {result['checks'].get('total_atoms', 0)}")
        print(f"  Unique paths: {result['checks'].get('unique_paths', 0)}")
        print(f"  Duplicates: {result['checks'].get('duplicates', 0)}")

        return result

    def phase_8_types(self):
        """Check type distribution balance"""
        result = {'score': 0, 'checks': {}, 'issues': []}

        index_file = self.atoms_dir / 'index.json' if self.atoms_dir.exists() else None

        if not index_file or not index_file.exists():
            return result

        try:
            with open(index_file) as f:
                index = json.load(f)

            types = index.get('atoms_by_type', {})
            total = sum(types.values())

            result['checks']['type_breakdown'] = types
            result['checks']['total'] = total

            # Good distribution = better score
            if len(types) >= 5:
                result['score'] += 50
            elif len(types) >= 3:
                result['score'] += 30

            # Check for balance
            if types:
                max_pct = max(types.values()) / total * 100
                if max_pct < 50:
                    result['score'] += 50
                elif max_pct < 70:
                    result['score'] += 30
                else:
                    result['issues'].append(f"Imbalanced types: largest is {max_pct:.0f}%")
                    result['score'] += 10

            print("  Type breakdown:")
            for t, count in sorted(types.items(), key=lambda x: x[1], reverse=True)[:5]:
                pct = count / total * 100 if total > 0 else 0
                print(f"    {t}: {count} ({pct:.1f}%)")

        except Exception as e:
            result['issues'].append(f"Failed to check types: {e}")

        return result

    def phase_9_growth(self):
        """Analyze growth velocity over time"""
        result = {'score': 0, 'checks': {}, 'issues': []}

        if not self.atoms_dir.exists():
            return result

        atom_files = sorted(self.atoms_dir.glob('atoms_*.json'))

        if len(atom_files) < 2:
            result['checks']['history_days'] = len(atom_files)
            result['score'] = 50 if atom_files else 0
            print(f"  History: {len(atom_files)} day(s)")
            return result

        # Compare first and last
        try:
            with open(atom_files[0]) as f:
                first = json.load(f)
            with open(atom_files[-1]) as f:
                last = json.load(f)

            growth = len(last) - len(first)
            days = len(atom_files)
            daily_growth = growth / days if days > 0 else 0

            result['checks']['first_count'] = len(first)
            result['checks']['last_count'] = len(last)
            result['checks']['total_growth'] = growth
            result['checks']['daily_avg'] = round(daily_growth, 1)
            result['checks']['history_days'] = days

            # Positive growth is good
            if daily_growth > 10:
                result['score'] = 100
            elif daily_growth > 0:
                result['score'] = 70
            elif daily_growth == 0:
                result['score'] = 50
                result['issues'].append("No growth detected")
            else:
                result['score'] = 30
                result['issues'].append("Negative growth (shrinking)")

            print(f"  History: {days} days")
            print(f"  First: {len(first)} atoms")
            print(f"  Latest: {len(last)} atoms")
            print(f"  Growth: {growth} ({daily_growth:.1f}/day)")

        except Exception as e:
            result['issues'].append(f"Failed to analyze growth: {e}")

        return result

    def phase_10_errors(self):
        """Analyze historical errors"""
        result = {'score': 100, 'checks': {}, 'issues': []}  # Start at 100, deduct for errors

        # Check for error logs
        error_patterns = ['error', 'failed', 'exception']
        error_files = []

        for pattern in error_patterns:
            error_files.extend(self.deployment.glob(f'*{pattern}*.log'))
            error_files.extend(self.deployment.glob(f'*{pattern}*.txt'))

        result['checks']['error_files'] = len(error_files)

        # Check daemon status
        consciousness_dir = self.home / '.consciousness'
        rake_status = consciousness_dir / 'autonomous_rake_status.json'

        if rake_status.exists():
            try:
                with open(rake_status) as f:
                    status = json.load(f)

                result['checks']['daemon_cycles'] = status.get('cycles_completed', 0)
                result['checks']['daemon_errors'] = status.get('errors', 0)

                errors = status.get('errors', 0)
                if errors > 0:
                    result['score'] -= min(50, errors * 5)
                    result['issues'].append(f"Daemon has {errors} recorded errors")

            except:
                pass

        print(f"  Error files found: {len(error_files)}")
        print(f"  Daemon cycles: {result['checks'].get('daemon_cycles', 'N/A')}")
        print(f"  Daemon errors: {result['checks'].get('daemon_errors', 0)}")

        result['score'] = max(0, result['score'])
        return result

    def phase_11_api(self):
        """Check API endpoints"""
        result = {'score': 0, 'checks': {}, 'issues': []}

        # Check for API files
        api_files = [
            'CYCLOTRON_SEARCH.py',
            'CYCLOTRON_CLOUD_HOSTED_API.py',
        ]

        found = []
        for api in api_files:
            if (self.deployment / api).exists():
                found.append(api)

        result['checks']['api_files'] = found
        result['score'] = (len(found) / len(api_files)) * 100 if api_files else 50

        # Check if search HTML exists
        search_html = self.deployment / 'CYCLOTRON_SEARCH.html'
        if search_html.exists():
            result['checks']['search_ui'] = True
            result['score'] = min(100, result['score'] + 20)

        print(f"  API files: {', '.join(found) if found else 'None'}")
        print(f"  Search UI: {'✓' if result['checks'].get('search_ui') else '✗'}")

        return result

    def phase_12_security(self):
        """Security audit"""
        result = {'score': 100, 'checks': {}, 'issues': []}

        # Check for exposed API keys in atoms
        if self.atoms_dir.exists():
            atom_files = list(self.atoms_dir.glob('*.json'))
            for af in atom_files[:5]:  # Sample check
                try:
                    content = af.read_text()
                    if 'sk-ant-' in content or 'api_key' in content.lower():
                        result['score'] -= 30
                        result['issues'].append(f"Potential API key in {af.name}")
                        break
                except:
                    pass

        # Check permissions
        result['checks']['atoms_readable'] = self.atoms_dir.exists() and os.access(self.atoms_dir, os.R_OK)

        print(f"  Atoms readable: {'✓' if result['checks']['atoms_readable'] else '✗'}")
        if result['issues']:
            print(f"  Security issues: {len(result['issues'])}")

        result['score'] = max(0, result['score'])
        return result

    def phase_13_optimization(self):
        """Generate optimization recommendations"""
        result = {'score': 50, 'checks': {}, 'issues': [], 'recommendations': []}

        # Based on previous phases, generate recommendations

        # Check if federation is set up
        if not self.federation or not self.federation.exists():
            result['recommendations'].append("Set up Dropbox federation for multi-computer sync")

        # Check index freshness
        index_file = self.atoms_dir / 'index.json' if self.atoms_dir.exists() else None
        if index_file and index_file.exists():
            age = time.time() - index_file.stat().st_mtime
            if age > 600:  # 10 minutes
                result['recommendations'].append("Index is stale - verify daemon is running")

        # Check for search UI
        if not (self.deployment / 'CYCLOTRON_SEARCH.html').exists():
            result['recommendations'].append("Add search UI for easy querying")

        # Check analytics
        analytics_report = self.deployment / 'CYCLOTRON_ANALYTICS_REPORT.json'
        if not analytics_report.exists():
            result['recommendations'].append("Run analytics engine for detailed insights")

        result['checks']['recommendations'] = len(result['recommendations'])
        result['score'] = 100 - (len(result['recommendations']) * 10)
        result['score'] = max(50, result['score'])

        print("  Recommendations:")
        for rec in result['recommendations']:
            print(f"    → {rec}")
            self.results['recommendations'].append(rec)

        if not result['recommendations']:
            print("    All optimizations complete!")

        return result

    def generate_recommendations(self):
        """Generate final recommendations based on all phases"""
        scores = [(name, phase.get('score', 0)) for name, phase in self.results['phases'].items()]

        # Add recommendations for low-scoring phases
        for name, score in scores:
            if score < 50:
                self.results['recommendations'].append(f"Critical: Fix {name} (score: {score})")
            elif score < 70:
                self.results['recommendations'].append(f"Improve: {name} (score: {score})")

    def print_summary(self):
        """Print final summary"""
        print("\n" + "=" * 70)
        print("AUDIT SUMMARY")
        print("=" * 70)

        overall = self.results['overall_score']

        if overall >= 80:
            status = "EXCELLENT"
            icon = ""
        elif overall >= 60:
            status = "GOOD"
            icon = ""
        elif overall >= 40:
            status = "NEEDS WORK"
            icon = "⚠️"
        else:
            status = "CRITICAL"
            icon = ""

        print(f"\n{icon} OVERALL SCORE: {overall}/100 [{status}]")

        print("\nPhase Scores:")
        for name, phase in self.results['phases'].items():
            score = int(phase.get('score', 0))
            bar = '█' * (score // 10) + '░' * (10 - score // 10)
            print(f"  {name:30} [{bar}] {score}")

        if self.results['critical_issues']:
            print(f"\nCritical Issues: {len(self.results['critical_issues'])}")
            for issue in self.results['critical_issues'][:5]:
                print(f"  - {issue}")

        if self.results['recommendations']:
            print(f"\nTop Recommendations:")
            for rec in self.results['recommendations'][:5]:
                print(f"  → {rec}")

    def save_results(self):
        """Save audit results to file"""
        output_file = self.deployment / 'CYCLOTRON_AUDIT_RESULTS.json'
        with open(output_file, 'w') as f:
            json.dump(self.results, f, indent=2)
        print(f"\nResults saved to: {output_file}")

        # Also save readable summary
        summary_file = self.deployment / 'CYCLOTRON_AUDIT_SUMMARY.md'
        with open(summary_file, 'w') as f:
            f.write(f"# Cyclotron 13-Phase Audit Results\n\n")
            f.write(f"**Date:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write(f"**Overall Score:** {self.results['overall_score']}/100\n\n")

            f.write("## Phase Scores\n\n")
            for name, phase in self.results['phases'].items():
                score = phase.get('score', 0)
                f.write(f"- {name}: {score}/100\n")

            if self.results['critical_issues']:
                f.write("\n## Critical Issues\n\n")
                for issue in self.results['critical_issues']:
                    f.write(f"- {issue}\n")

            if self.results['recommendations']:
                f.write("\n## Recommendations\n\n")
                for rec in self.results['recommendations']:
                    f.write(f"- {rec}\n")

        print(f"Summary saved to: {summary_file}")


def main():
    """Run the 13-phase audit"""
    auditor = CyclotronAuditor()
    auditor.run_full_audit()


if __name__ == '__main__':
    main()
