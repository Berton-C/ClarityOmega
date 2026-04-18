#!/usr/bin/env python3
"""
soul_patch_dockerfile.py -- Remove chmod 0444 on prompt.txt from Dockerfile

Usage:
    python3 scripts/soul_patch_dockerfile.py [--dry-run]

Removes the line that locks prompt.txt to read-only (chmod 0444).
Line 111's find command already sets 0644 for all memory files,
which gives the runtime user (65534) read-write access.

Idempotent -- detects if already removed and skips.
"""

import sys
import os
import shutil
from datetime import datetime

DOCKERFILE = "Dockerfile"
BACKUP_SUFFIX = ".pre-soul-backup"
TARGET_LINE = " && chmod 0444 /PeTTa/repos/omegaclaw/memory/prompt.txt \\\n"
# Alternate form without trailing backslash (in case it is last in chain)
TARGET_LINE_ALT = " && chmod 0444 /PeTTa/repos/omegaclaw/memory/prompt.txt\n"

def read_file(path):
    with open(path, "r", encoding="utf-8") as f:
        return f.read()

def write_file(path, content):
    with open(path, "w", encoding="utf-8") as f:
        f.write(content)

def main():
    dry_run = "--dry-run" in sys.argv

    print("=" * 60)
    print("ClarityClaw Soul Patch -- Dockerfile")
    print(f"Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"Mode: {'DRY RUN' if dry_run else 'LIVE'}")
    print("=" * 60)

    if not os.path.exists(DOCKERFILE):
        print(f"\n  FATAL: {DOCKERFILE} not found. Run from repo root.")
        sys.exit(1)

    content = read_file(DOCKERFILE)

    if "chmod 0444" not in content:
        print(f"\n  chmod 0444 line already removed from {DOCKERFILE}. Skipping.")
        sys.exit(0)

    if TARGET_LINE in content:
        content = content.replace(TARGET_LINE, "")
        print(f"  Removed chmod 0444 line (with trailing backslash)")
    elif TARGET_LINE_ALT in content:
        content = content.replace(TARGET_LINE_ALT, "")
        print(f"  Removed chmod 0444 line (without trailing backslash)")
    else:
        # Try flexible match
        import re
        pattern = r' *&& *chmod 0444 /PeTTa/repos/omegaclaw/memory/prompt\.txt *\\?\n'
        if re.search(pattern, content):
            content = re.sub(pattern, '', content)
            print(f"  Removed chmod 0444 line (flexible match)")
        else:
            print(f"\n  WARNING: chmod 0444 found in file but pattern did not match exactly.")
            print(f"  Manual removal may be needed.")
            sys.exit(1)

    if dry_run:
        print(f"\n  DRY RUN -- no files modified.")
    else:
        if not os.path.exists(DOCKERFILE + BACKUP_SUFFIX):
            shutil.copy2(DOCKERFILE, DOCKERFILE + BACKUP_SUFFIX)
            print(f"  Backup created: {DOCKERFILE}{BACKUP_SUFFIX}")
        write_file(DOCKERFILE, content)
        print(f"\n  Dockerfile patched successfully.")

    print(f"\n{'=' * 60}")
    print("Done.")

if __name__ == "__main__":
    main()
