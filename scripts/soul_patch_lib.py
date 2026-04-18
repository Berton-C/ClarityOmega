#!/usr/bin/env python3
"""
soul_patch_lib.py -- Add ClarityClaw soul imports to lib_omegaclaw.metta

Usage:
    python3 scripts/soul_patch_lib.py [--dry-run]

Adds three soul import lines after the src/memory import in lib_omegaclaw.metta.
Idempotent -- detects if already applied and skips.
"""

import sys
import os
import re
import shutil
from datetime import datetime

LIB_FILE = "lib_omegaclaw.metta"
BACKUP_SUFFIX = ".pre-soul-backup"
SOUL_MARKER = "soul/soul_kernel"

def read_file(path):
    with open(path, "r", encoding="utf-8") as f:
        return f.read()

def write_file(path, content):
    with open(path, "w", encoding="utf-8") as f:
        f.write(content)

def main():
    dry_run = "--dry-run" in sys.argv

    print("=" * 60)
    print("ClarityClaw Soul Patch -- lib_omegaclaw.metta")
    print(f"Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"Mode: {'DRY RUN' if dry_run else 'LIVE'}")
    print("=" * 60)

    if not os.path.exists(LIB_FILE):
        print(f"\n  FATAL: {LIB_FILE} not found. Run from repo root.")
        sys.exit(1)

    content = read_file(LIB_FILE)

    if SOUL_MARKER in content:
        print(f"\n  Soul imports already present in {LIB_FILE}. Skipping.")
        sys.exit(0)

    # Anchor: the src/memory import line
    anchor = '!(import! &self (library omegaclaw ./src/memory))'
    if anchor not in content:
        print(f"\n  FATAL: Anchor not found: {repr(anchor)}")
        print(f"  lib_omegaclaw.metta structure has changed.")
        sys.exit(1)

    # Insert soul imports after the memory import line
    soul_imports = """
;; CLARITYCLAW SOUL imports
!(import! &self (library omegaclaw ./soul/soul_kernel))
!(import! &self (library omegaclaw ./soul/soul_utils))
!(import! &self (library omegaclaw ./soul/soul_memory))"""

    insert_pos = content.find(anchor) + len(anchor)
    content = content[:insert_pos] + "\n" + soul_imports + content[insert_pos:]

    if dry_run:
        print(f"\n  DRY RUN -- would write:")
        print(content)
    else:
        if not os.path.exists(LIB_FILE + BACKUP_SUFFIX):
            shutil.copy2(LIB_FILE, LIB_FILE + BACKUP_SUFFIX)
            print(f"  Backup created: {LIB_FILE}{BACKUP_SUFFIX}")
        write_file(LIB_FILE, content)
        print(f"\n  Soul imports added to {LIB_FILE}")

    print(f"\n{'=' * 60}")
    print("Done.")

if __name__ == "__main__":
    main()
