#!/bin/bash
# Trinity Quick Access Script
# Usage: ./trinity.sh [start|stop|status|report|dashboard]

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

case "$1" in
    start)
        python3 TRINITY_MASTER_ORCHESTRATOR.py start
        ;;
    stop)
        python3 TRINITY_MASTER_ORCHESTRATOR.py stop
        ;;
    status)
        python3 TRINITY_MASTER_ORCHESTRATOR.py status
        ;;
    report)
        python3 TRINITY_MASTER_ORCHESTRATOR.py report
        ;;
    dashboard)
        echo "Opening Trinity Dashboard..."
        if command -v xdg-open &> /dev/null; then
            xdg-open TRINITY_LIVE_DASHBOARD.html
        elif command -v open &> /dev/null; then
            open TRINITY_LIVE_DASHBOARD.html
        else
            echo "Please open TRINITY_LIVE_DASHBOARD.html manually"
        fi
        ;;
    *)
        echo "Trinity Quick Access"
        echo ""
        echo "Usage: ./trinity.sh [command]"
        echo ""
        echo "Commands:"
        echo "  start      - Start all Trinity systems"
        echo "  stop       - Stop all systems"
        echo "  status     - Show system status"
        echo "  report     - Generate CP1 output"
        echo "  dashboard  - Open live dashboard"
        echo ""
        echo "C1 × C2 × C3 = ∞"
        exit 1
        ;;
esac
