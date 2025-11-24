#!/usr/bin/env python3
"""
TEMPORAL DATA ROTATION
Manages data lifecycle: Future → Present → Past
Automatically archives completed items and promotes ready items.
"""

import json
import shutil
from pathlib import Path
from datetime import datetime, timedelta

# Paths
HOME = Path.home()
ARCHIVES_PATH = HOME / ".archives"
CONSCIOUSNESS_PATH = HOME / ".consciousness"
PLANNING_PATH = HOME / ".planning"

# Ensure directories exist
for subdir in ['sessions', 'projects', 'decisions']:
    (ARCHIVES_PATH / subdir).mkdir(parents=True, exist_ok=True)

def archive_completed_sessions():
    """Move completed session files to archives."""
    archived = 0

    # Check consciousness state files
    state_files = list(CONSCIOUSNESS_PATH.glob("*_state*.json"))

    for state_file in state_files:
        try:
            with open(state_file) as f:
                data = json.load(f)

            # Check if session is complete
            if data.get('status') == 'complete' or data.get('completed'):
                # Move to archives
                archive_name = f"SESSION_{datetime.now().strftime('%Y%m%d_%H%M%S')}_{state_file.name}"
                dest = ARCHIVES_PATH / "sessions" / archive_name
                shutil.move(str(state_file), str(dest))
                archived += 1
                print(f"Archived: {state_file.name} → {archive_name}")
        except Exception as e:
            print(f"Error processing {state_file}: {e}")

    return archived

def archive_old_logs(days=30):
    """Archive log files older than N days."""
    archived = 0
    cutoff = datetime.now() - timedelta(days=days)

    # Find log files
    log_patterns = ["*_log*.json", "*_log*.txt", "*.log"]

    for pattern in log_patterns:
        for log_file in CONSCIOUSNESS_PATH.glob(pattern):
            try:
                mtime = datetime.fromtimestamp(log_file.stat().st_mtime)
                if mtime < cutoff:
                    archive_name = f"LOG_{mtime.strftime('%Y%m%d')}_{log_file.name}"
                    dest = ARCHIVES_PATH / "sessions" / archive_name
                    shutil.move(str(log_file), str(dest))
                    archived += 1
                    print(f"Archived old log: {log_file.name}")
            except Exception as e:
                print(f"Error archiving {log_file}: {e}")

    return archived

def promote_planned_to_active():
    """Move planned items with start_date <= today to active."""
    promoted = 0
    today = datetime.now().date()

    # Check planning files for items to promote
    for plan_file in PLANNING_PATH.glob("**/*.json"):
        try:
            with open(plan_file) as f:
                data = json.load(f)

            modified = False

            # Check for items with start dates
            if isinstance(data, dict):
                for key, value in data.items():
                    if isinstance(value, list):
                        for item in value:
                            if isinstance(item, dict) and 'start_date' in item:
                                start = datetime.fromisoformat(item['start_date']).date()
                                if start <= today and item.get('status') == 'planned':
                                    item['status'] = 'active'
                                    item['promoted_at'] = datetime.now().isoformat()
                                    modified = True
                                    promoted += 1
                                    print(f"Promoted: {item.get('name', item.get('rock', 'unnamed'))}")

            if modified:
                with open(plan_file, 'w') as f:
                    json.dump(data, f, indent=2)

        except Exception as e:
            print(f"Error processing {plan_file}: {e}")

    return promoted

def archive_completed_rocks():
    """Archive completed quarterly rocks."""
    archived = 0

    rocks_file = PLANNING_PATH / "traction" / "ROCKS_Q4_2025.json"

    if rocks_file.exists():
        try:
            with open(rocks_file) as f:
                data = json.load(f)

            completed_rocks = []
            remaining_rocks = []

            for rock in data.get('rocks', []):
                if rock.get('status') == 'complete':
                    rock['archived_at'] = datetime.now().isoformat()
                    completed_rocks.append(rock)
                    archived += 1
                else:
                    remaining_rocks.append(rock)

            # Save completed to archives
            if completed_rocks:
                archive_name = f"ROCKS_COMPLETED_{datetime.now().strftime('%Y%m%d')}.json"
                archive_path = ARCHIVES_PATH / "projects" / archive_name

                # Append to existing or create new
                existing = []
                if archive_path.exists():
                    with open(archive_path) as f:
                        existing = json.load(f)

                existing.extend(completed_rocks)

                with open(archive_path, 'w') as f:
                    json.dump(existing, f, indent=2)

                print(f"Archived {len(completed_rocks)} completed rocks")

            # Update rocks file
            data['rocks'] = remaining_rocks
            data['summary']['complete'] = 0  # Reset counter

            with open(rocks_file, 'w') as f:
                json.dump(data, f, indent=2)

        except Exception as e:
            print(f"Error processing rocks: {e}")

    return archived

def compress_old_archives(days=90):
    """Compress archives older than N days."""
    import zipfile

    compressed = 0
    cutoff = datetime.now() - timedelta(days=days)

    for archive_dir in ['sessions', 'projects', 'decisions']:
        dir_path = ARCHIVES_PATH / archive_dir

        for file_path in dir_path.glob("*"):
            if file_path.suffix == '.zip':
                continue

            try:
                mtime = datetime.fromtimestamp(file_path.stat().st_mtime)
                if mtime < cutoff:
                    # Compress file
                    zip_path = file_path.with_suffix(file_path.suffix + '.zip')
                    with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zf:
                        zf.write(file_path, file_path.name)

                    # Remove original
                    file_path.unlink()
                    compressed += 1
                    print(f"Compressed: {file_path.name}")

            except Exception as e:
                print(f"Error compressing {file_path}: {e}")

    return compressed

def generate_rotation_report():
    """Generate report of data rotation activity."""
    report = {
        'timestamp': datetime.now().isoformat(),
        'archives': {
            'sessions': len(list((ARCHIVES_PATH / 'sessions').glob('*'))),
            'projects': len(list((ARCHIVES_PATH / 'projects').glob('*'))),
            'decisions': len(list((ARCHIVES_PATH / 'decisions').glob('*')))
        },
        'planning': {
            'files': len(list(PLANNING_PATH.glob('**/*'))),
        },
        'consciousness': {
            'files': len(list(CONSCIOUSNESS_PATH.glob('*'))),
        }
    }

    report_path = ARCHIVES_PATH / f"ROTATION_REPORT_{datetime.now().strftime('%Y%m%d')}.json"
    with open(report_path, 'w') as f:
        json.dump(report, f, indent=2)

    return report

def main():
    """Run full data rotation."""
    print("=" * 50)
    print("TEMPORAL DATA ROTATION")
    print("=" * 50)
    print(f"Time: {datetime.now().isoformat()}\n")

    # Run rotation tasks
    print("📁 Archiving completed sessions...")
    sessions = archive_completed_sessions()

    print("\n📁 Archiving old logs...")
    logs = archive_old_logs()

    print("\n📁 Promoting planned to active...")
    promoted = promote_planned_to_active()

    print("\n📁 Archiving completed rocks...")
    rocks = archive_completed_rocks()

    print("\n📁 Compressing old archives...")
    compressed = compress_old_archives()

    # Generate report
    print("\n📊 Generating report...")
    report = generate_rotation_report()

    # Summary
    print("\n" + "=" * 50)
    print("ROTATION COMPLETE")
    print("=" * 50)
    print(f"Sessions archived: {sessions}")
    print(f"Logs archived: {logs}")
    print(f"Items promoted: {promoted}")
    print(f"Rocks archived: {rocks}")
    print(f"Files compressed: {compressed}")
    print(f"\nArchive totals:")
    print(f"  Sessions: {report['archives']['sessions']}")
    print(f"  Projects: {report['archives']['projects']}")
    print(f"  Decisions: {report['archives']['decisions']}")

if __name__ == "__main__":
    main()
