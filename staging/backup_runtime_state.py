#!/usr/bin/env python3
"""
Backup script: ClarityOmega runtime continuity state (outside git).

Purpose
-------
Per the 2026-07-29 tracking decisions: chromadb/, promotions.db, and
history.metta stay OUT of git (churning binaries / large append-only text);
their continuity is served by dated archives instead. This script creates
one verified tar.gz per run in a destination OUTSIDE the repo and prunes
old archives beyond a retention count.

What is backed up
-----------------
- volumes/omegaclaw/memory/chromadb/          (semantic memory)
- volumes/omegaclaw/memory/promotions.db      (+ -wal / -shm if present)
- volumes/omegaclaw/memory/history.metta      (episode memory)

What is NOT backed up (and why)
-------------------------------
- findings.metta, idle_state.json, soul_audit_log.txt: tracked in git.
- *.backup, *.trimmed, prompt.txt: derived/transient, regenerable.

Consistency caveat
------------------
The live container writes these files. Archives taken mid-write can be
internally torn (especially sqlite). Including the -wal/-shm pair keeps
sqlite recoverable in most cases. For a guaranteed-consistent archive,
run at a quiet moment or stop the container first:
    docker compose stop clarityclaw && python3 staging/backup_runtime_state.py && docker compose up -d clarityclaw

Usage (from repo root)
----------------------
    python3 staging/backup_runtime_state.py
    python3 staging/backup_runtime_state.py --dest ../clarityomega_runtime_backups --keep 14

Verification
------------
After writing, the archive is re-read (tar listing) and the member count
is compared against the collected source list. Size and member count are
printed. Nonzero exit on any failure.
"""
from __future__ import annotations

import argparse
import datetime
import os
import sys
import tarfile
from pathlib import Path

MEMORY = Path("volumes/omegaclaw/memory")

SOURCES_REQUIRED = [
    MEMORY / "history.metta",
    MEMORY / "promotions.db",
    MEMORY / "chromadb",
]
SOURCES_OPTIONAL = [
    MEMORY / "promotions.db-wal",
    MEMORY / "promotions.db-shm",
]


def collect_members(paths):
    members = []
    for p in paths:
        if p.is_dir():
            for root, _dirs, files in os.walk(p):
                for f in files:
                    members.append(Path(root) / f)
        elif p.is_file():
            members.append(p)
    return members


def main() -> int:
    ap = argparse.ArgumentParser(description="Backup ClarityOmega runtime continuity state")
    ap.add_argument("--dest", default="../clarityomega_runtime_backups",
                    help="Destination directory OUTSIDE the repo (default ../clarityomega_runtime_backups)")
    ap.add_argument("--keep", type=int, default=14,
                    help="Retention: number of newest archives to keep (default 14)")
    args = ap.parse_args()

    # Preflight: repo root and sources.
    if not MEMORY.is_dir():
        print("ABORT: " + str(MEMORY) + " not found. Run from repo root.")
        return 2
    missing = [str(p) for p in SOURCES_REQUIRED if not p.exists()]
    if missing:
        print("ABORT: required source(s) missing: " + ", ".join(missing))
        return 2
    sources = list(SOURCES_REQUIRED) + [p for p in SOURCES_OPTIONAL if p.exists()]

    dest = Path(args.dest)
    dest.mkdir(parents=True, exist_ok=True)
    # Guard: destination must not be inside the repo working tree.
    repo_root = Path(".").resolve()
    if str(dest.resolve()).startswith(str(repo_root) + os.sep):
        print("ABORT: destination " + str(dest.resolve()) + " is inside the repo. Choose a path outside.")
        return 2

    stamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    archive = dest / ("clarityomega_runtime_" + stamp + ".tar.gz")
    n = 2
    while archive.exists():
        archive = dest / ("clarityomega_runtime_" + stamp + "_" + str(n) + ".tar.gz")
        n += 1

    expected_members = collect_members(sources)
    print("Sources: " + str(len(sources)) + " top-level, " + str(len(expected_members)) + " files total.")

    with tarfile.open(archive, "w:gz") as tf:
        for p in sources:
            tf.add(str(p))
    size_mb = archive.stat().st_size / (1024 * 1024)

    # Verify: re-read the archive, count file members.
    with tarfile.open(archive, "r:gz") as tf:
        archived_files = [m for m in tf.getmembers() if m.isfile()]
    ok = len(archived_files) == len(expected_members)
    print("Archive: " + str(archive))
    print("Size: %.1f MB. File members: %d (expected %d) -> %s"
          % (size_mb, len(archived_files), len(expected_members), "OK" if ok else "FAIL"))
    if not ok:
        print("VERIFICATION FAILED. Archive kept for inspection; do not trust it.")
        return 1

    # Retention prune, newest kept.
    archives = sorted(dest.glob("clarityomega_runtime_*.tar.gz"))
    excess = archives[:-args.keep] if args.keep > 0 else []
    for old in excess:
        old.unlink()
        print("Pruned: " + str(old))
    print("Retained: " + str(len(archives) - len(excess)) + " archive(s) in " + str(dest))
    print("BACKUP COMPLETE.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
