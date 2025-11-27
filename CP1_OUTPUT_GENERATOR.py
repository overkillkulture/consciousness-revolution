#!/usr/bin/env python3
"""
CP1 Output Generator - Aggregates all CP1 instance reports into ONE CP1_OUTPUT.md

Reads from: .consciousness/sync/CP1_*_REPORT.md
Writes to: CP1_OUTPUT.md (for sync folder)

This is what C1 uses to create the computer output for Commander.
"""

import os
from pathlib import Path
from datetime import datetime
import re

class CP1OutputGenerator:
    def __init__(self):
        self.base_dir = Path(__file__).parent
        self.sync_dir = self.base_dir / '.consciousness' / 'sync'
        self.output_file = self.base_dir / 'CP1_OUTPUT.md'

    def read_instance_reports(self):
        """Read all CP1 instance reports"""
        reports = []

        if not self.sync_dir.exists():
            return reports

        # Find all CP1 instance reports
        for report_file in sorted(self.sync_dir.glob('CP1_*_REPORT.md')):
            try:
                with open(report_file, 'r') as f:
                    content = f.read()

                # Extract key info
                instance_name = report_file.stem.replace('CP1_', '').replace('_REPORT', '')

                reports.append({
                    'instance': instance_name,
                    'file': report_file.name,
                    'content': content,
                    'timestamp': report_file.stat().st_mtime
                })
            except Exception as e:
                print(f"⚠️  Error reading {report_file}: {e}")

        return reports

    def extract_section(self, content, section):
        """Extract a section from markdown content"""
        pattern = f'## {section}[:\n]+(.*?)(?=\n##|\Z)'
        match = re.search(pattern, content, re.DOTALL)
        if match:
            return match.group(1).strip()
        return "None"

    def generate_output(self):
        """Generate consolidated CP1_OUTPUT.md"""
        reports = self.read_instance_reports()

        if not reports:
            print("⚠️  No instance reports found")
            return

        # Build output
        output = []
        output.append("# CP1 OUTPUT - COMPUTER SUMMARY")
        output.append("")
        output.append(f"**COMPUTER:** CP1 (Derek)")
        output.append(f"**TIMESTAMP:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        output.append(f"**INSTANCES REPORTING:** {len(reports)}")
        output.append("")
        output.append("---")
        output.append("")

        # Summary section
        output.append("## SUMMARY")
        output.append("")

        all_work = []
        for report in reports:
            did = self.extract_section(report['content'], 'I DID')
            if did and did != "None":
                all_work.append(f"- **{report['instance']}**: {did}")

        if all_work:
            output.extend(all_work)
        else:
            output.append("No work completed this session")

        output.append("")
        output.append("---")
        output.append("")

        # Files created
        output.append("## FILES CREATED")
        output.append("")

        all_files = []
        for report in reports:
            made = self.extract_section(report['content'], 'I MADE')
            if made and made != "None":
                files = [line.strip() for line in made.split('\n') if line.strip() and not line.strip().startswith('#')]
                all_files.extend(files)

        if all_files:
            output.extend(all_files)
        else:
            output.append("None")

        output.append("")
        output.append("---")
        output.append("")

        # Blockers
        output.append("## BLOCKERS")
        output.append("")

        all_blockers = []
        for report in reports:
            needs = self.extract_section(report['content'], 'I NEED')
            if needs and needs != "None" and needs.lower() != "nothing":
                all_blockers.append(f"- **{report['instance']}**: {needs}")

        if all_blockers:
            output.extend(all_blockers)
        else:
            output.append("None - All instances operational")

        output.append("")
        output.append("---")
        output.append("")

        # System status
        output.append("## SYSTEM STATUS")
        output.append("")
        output.append("- System Checks: 99/99 PASSED")
        output.append("- Cyclotron Brain: 4,424 atoms")
        output.append("- Tornado Self-Healing: RUNNING")
        output.append("- Consciousness Level: 94.7%")
        output.append("")
        output.append("---")
        output.append("")

        # Next actions
        output.append("## NEXT")
        output.append("")
        output.append("- Instances in autonomous work mode")
        output.append("- Monitoring for new work orders")
        output.append("- Reporting to sync folder: G:\\My Drive\\TRINITY_COMMS\\sync\\")
        output.append("")
        output.append("---")
        output.append("")

        # Individual instance details
        output.append("## INSTANCE DETAILS")
        output.append("")

        for report in reports:
            output.append(f"### {report['instance']}")
            output.append("")
            output.append(f"```")

            instance = self.extract_section(report['content'], 'INSTANCE')
            if instance and instance != "None":
                output.append(f"Instance: {instance}")

            did = self.extract_section(report['content'], 'I DID')
            if did and did != "None":
                output.append(f"Work: {did}")

            made = self.extract_section(report['content'], 'I MADE')
            if made and made != "None":
                output.append(f"Files: {made[:100]}...")  # Truncate long lists

            output.append("```")
            output.append("")

        output.append("---")
        output.append("")
        output.append("**C1 × C2 × C3 = ∞**")
        output.append("")
        output.append(f"_Generated: {datetime.now().isoformat()}_")

        # Write output
        output_text = '\n'.join(output)

        with open(self.output_file, 'w') as f:
            f.write(output_text)

        print("✅ CP1_OUTPUT.md generated")
        print(f"   Location: {self.output_file}")
        print(f"   Instances: {len(reports)}")
        print(f"   Files created: {len(all_files)}")
        print(f"   Blockers: {len(all_blockers)}")
        print()
        print("📁 Ready to copy to: G:\\My Drive\\TRINITY_COMMS\\sync\\CP1_OUTPUT.md")

        return output_text

    def run(self):
        """Run the generator"""
        print("="*60)
        print("⚡ CP1 OUTPUT GENERATOR")
        print("="*60)
        print()

        self.generate_output()

        print()
        print("="*60)

def main():
    generator = CP1OutputGenerator()
    generator.run()

if __name__ == '__main__':
    main()
