#!/usr/bin/env bash
# soul_patch_all.sh -- Apply all ClarityClaw soul patches to OmegaClaw
#
# Usage:
#   cd /Users/bcb/Documents/ClarityClaw/clarityclaw-omega
#   bash scripts/soul_patch_all.sh [--dry-run]
#
# This script runs all soul patch scripts in the correct order.
# Each script is idempotent -- safe to run multiple times.
# Use --dry-run to preview changes without modifying files.
#
# Prerequisites:
#   - soul/ directory already copied into repo
#   - src/helper.py already merged with soul functions
#   - run.metta git-import line already removed
#   - memory/prompt.txt hand-edited with ClarityClaw identity
#
# Author: Berton Bennett / ClarityDAO

set -euo pipefail

MODE="${1:---live}"
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"

echo "============================================================"
echo "ClarityClaw Soul Patch -- Master Script"
echo "Date: $(date '+%Y-%m-%d %H:%M:%S')"
echo "Mode: $MODE"
echo "============================================================"

# Verify we are in the repo root
if [ ! -f "lib_omegaclaw.metta" ]; then
    echo ""
    echo "  FATAL: lib_omegaclaw.metta not found."
    echo "  Run this script from the clarityclaw-omega repo root."
    exit 1
fi

# Verify prerequisites
echo ""
echo "Checking prerequisites..."

if [ ! -d "soul" ]; then
    echo "  FATAL: soul/ directory not found. Copy it first."
    exit 1
fi
echo "  soul/ directory: OK"

if ! grep -q "CLARITYCLAW SOUL" src/helper.py 2>/dev/null; then
    echo "  FATAL: src/helper.py does not contain ClarityClaw soul functions."
    echo "  Replace src/helper.py with the merged version first."
    exit 1
fi
echo "  src/helper.py merged: OK"

if grep -q "git-import!" run.metta 2>/dev/null; then
    echo "  FATAL: run.metta still contains git-import! line."
    echo "  Remove it first."
    exit 1
fi
echo "  run.metta git-import removed: OK"

echo ""
echo "All prerequisites met. Applying patches..."

# Run patches in order
echo ""
echo "--- Patch 1/3: lib_omegaclaw.metta (soul imports) ---"
python3 "$SCRIPT_DIR/soul_patch_lib.py" $MODE

echo ""
echo "--- Patch 2/3: Dockerfile (remove chmod 0444) ---"
python3 "$SCRIPT_DIR/soul_patch_dockerfile.py" $MODE

echo ""
echo "--- Patch 3/3: src/loop.metta (soul intercepts 5a/5b/5c) ---"
python3 "$SCRIPT_DIR/soul_patch_loop.py" $MODE

echo ""
echo "============================================================"
echo "All patches complete."
echo ""
echo "Next steps:"
echo "  1. Review the patched files"
echo "  2. Hand-edit memory/prompt.txt (if not done)"
echo "  3. Build: docker compose build --no-cache"
echo "  4. Run: docker compose up -d"
echo "  5. Verify: docker logs [container] | grep SOUL-AUDIT"
echo "============================================================"
