#!/usr/bin/env python3
"""
Apply script: pin Dockerfile build refs (PeTTa runtime, petta_lib_chromadb).

Purpose
-------
2026-07-30 boot-break root cause, PROVEN by two-sided image differential:
the fork's baked content is byte-identical across the broken and working
images (six md5-verified files including run.metta, lib_omegaclaw.metta,
loop.metta, helper.py), while the PeTTa runtime core differs comprehensively
(every src/*.pl changed, new ext_points.pl present only in the broken image,
lib_import.metta itself identical), and the identical boot command compiles
2779 prolog clauses on the working runtime versus 14 on the broken one.
Cause: ARG PETTA_REF=main floats, so the --no-cache rebuild silently pulled
upstream PeTTa main at 43705f5d, which fails to compile our manifest. The
working runtime is 6b7f52f0 (read from the restored 2026-07-29 image).
CHROMADB_REF=master floats identically; its working commit is 45638545.
FAISS_REF=v1.8.0 is a tag and is left alone.

git clone --branch accepts branches and tags only, never commit hashes, so
the pinned clones switch to the init / fetch-by-SHA / checkout pattern
(GitHub serves shallow fetches of reachable SHAs).

The four edits
--------------
Edit 1: ARG PETTA_REF=main -> pinned working commit (comment carries the
  provenance). Line delta 0.
Edit 2: ARG CHROMADB_REF=master -> pinned working commit. Line delta 0.
Edit 3: the PeTTa clone RUN -> init/fetch-by-SHA/checkout. Line delta +3.
Edit 4: the chromadb mkdir+clone RUN -> mkdir + init/fetch-by-SHA/checkout.
  Line delta +3.

Net change
----------
Dockerfile: +6 lines.

Mechanism
---------
Pinned SHAs make every rebuild reproduce the proven-working runtime, so
--no-cache rebuilds stop being silent upstream upgrades. Future PeTTa
upgrades become deliberate: change the pin, rebuild, verify, commit or
reverse.

Usage
-----
Dry-run (default):
    python3 staging/apply_dockerfile_ref_pins.py
Apply:
    python3 staging/apply_dockerfile_ref_pins.py --apply
Reverse (after apply):
    python3 staging/apply_dockerfile_ref_pins.py --reverse --apply

Pre-conditions
--------------
- Boot-break cause proven (the differential above); service currently on
  the retagged 2026-07-29 image
- Verification after apply IS the standard procedure:
      docker compose build --no-cache clarityclaw && docker compose up -d
  Build must succeed and the container must reach iterations (not the
  exit-0 restart loop).

Backup files (forward apply only)
---------------------------------
- Dockerfile.bak.ref_pins
"""
from __future__ import annotations

import argparse
import sys
from pathlib import Path

# ============================================================================
# FILE PATHS
# ============================================================================

DOCKERFILE_PATH = Path("Dockerfile")
DOCKERFILE_BAK = Path("Dockerfile.bak.ref_pins")

PETTA_PIN = "6b7f52f064bdbc82fabd0a0998404121fb01d52e"
CHROMADB_PIN = "456385457e4e99ee049c2c0966988a6cd7ff3705"

# ============================================================================
# EDIT 1: PETTA_REF pin
# ============================================================================

E1_OLD = "ARG PETTA_REF=main"
E1_NEW = ("ARG PETTA_REF=" + PETTA_PIN
          + "  # pinned 2026-07-30: floating main pulled 43705f5d which fails our boot; this is the proven-working runtime commit")

# ============================================================================
# EDIT 2: CHROMADB_REF pin
# ============================================================================

E2_OLD = "ARG CHROMADB_REF=master"
E2_NEW = ("ARG CHROMADB_REF=" + CHROMADB_PIN
          + "  # pinned 2026-07-30, same floating-ref class")

# ============================================================================
# EDIT 3: PeTTa fetch-by-SHA
# ============================================================================

E3_OLD = '''RUN git clone --depth 1 --branch "${PETTA_REF}" "${PETTA_REPO}" /PeTTa'''
E3_NEW = '''RUN git init /PeTTa \\
 && git -C /PeTTa remote add origin "${PETTA_REPO}" \\
 && git -C /PeTTa fetch --depth 1 origin "${PETTA_REF}" \\
 && git -C /PeTTa checkout FETCH_HEAD'''

# ============================================================================
# EDIT 4: chromadb fetch-by-SHA
# ============================================================================

E4_OLD = '''RUN mkdir -p /PeTTa/repos \\
 && git clone --depth 1 --branch "${CHROMADB_REF}" "${CHROMADB_REPO}" /PeTTa/repos/petta_lib_chromadb'''
E4_NEW = '''RUN mkdir -p /PeTTa/repos \\
 && git init /PeTTa/repos/petta_lib_chromadb \\
 && git -C /PeTTa/repos/petta_lib_chromadb remote add origin "${CHROMADB_REPO}" \\
 && git -C /PeTTa/repos/petta_lib_chromadb fetch --depth 1 origin "${CHROMADB_REF}" \\
 && git -C /PeTTa/repos/petta_lib_chromadb checkout FETCH_HEAD'''

EDITS = [
    ("edit 1 (PETTA_REF pin)", E1_OLD, E1_NEW),
    ("edit 2 (CHROMADB_REF pin)", E2_OLD, E2_NEW),
    ("edit 3 (PeTTa fetch-by-SHA)", E3_OLD, E3_NEW),
    ("edit 4 (chromadb fetch-by-SHA)", E4_OLD, E4_NEW),
]

# ============================================================================
# HELPERS (per apply_task_state_step2_wiring.py template)
# ============================================================================

def find_target_substring_count(text: str, target: str) -> int:
    count = 0
    start = 0
    while True:
        idx = text.find(target, start)
        if idx == -1:
            break
        count += 1
        start = idx + 1
    return count


# ============================================================================
# SIMULATION
# ============================================================================

def simulate_forward(content: str) -> str:
    for label, old, new in EDITS:
        if find_target_substring_count(content, old) != 1:
            raise RuntimeError(f"{label}: anchor not found exactly once (byte drift?).")
        content = content.replace(old, new, 1)
    return content


def simulate_reverse(content: str) -> str:
    for label, old, new in reversed(EDITS):
        if find_target_substring_count(content, new) != 1:
            raise RuntimeError(f"{label}: pinned form not found exactly once.")
        content = content.replace(new, old, 1)
    return content


# ============================================================================
# STATE CHECK PREDICATES
# ============================================================================

def forward_state_ok(content: str) -> tuple[bool, str]:
    olds = all(find_target_substring_count(content, o) == 1 for _, o, _ in EDITS)
    news = all(find_target_substring_count(content, n) == 0 for _, _, n in EDITS)
    ok = olds and news
    return ok, f"floating refs present={olds}, pins absent={news} -> {'OK' if ok else 'FAIL'}"


def reverse_state_ok(content: str) -> tuple[bool, str]:
    news = all(find_target_substring_count(content, n) == 1 for _, _, n in EDITS)
    return news, f"pinned forms present={news} -> {'OK' if news else 'FAIL'}"


# ============================================================================
# DIFF PREVIEW
# ============================================================================

def diff_preview_first_change(old: str, new: str, label: str, context: int = 3) -> str:
    old_lines = old.splitlines()
    new_lines = new.splitlines()
    differ_start = None
    for i in range(min(len(old_lines), len(new_lines))):
        if old_lines[i] != new_lines[i]:
            differ_start = i
            break
    if differ_start is None:
        if len(old_lines) == len(new_lines):
            return f"--- {label}: NO CHANGES DETECTED ---"
        differ_start = min(len(old_lines), len(new_lines))
    differ_end_old = len(old_lines) - 1
    differ_end_new = len(new_lines) - 1
    while differ_end_old > differ_start and differ_end_new > differ_start:
        if old_lines[differ_end_old] == new_lines[differ_end_new]:
            differ_end_old -= 1
            differ_end_new -= 1
        else:
            break
    out = [f"--- {label} (lines {differ_start + 1} to {max(differ_end_old, differ_end_new) + 1}) ---"]
    start = max(0, differ_start - context)
    for i in range(start, differ_start):
        if i < len(old_lines):
            out.append(f"  {old_lines[i]}")
    for i in range(differ_start, differ_end_old + 1):
        if i < len(old_lines):
            out.append(f"- {old_lines[i]}")
    for i in range(differ_start, differ_end_new + 1):
        if i < len(new_lines):
            out.append(f"+ {new_lines[i]}")
    end_old = min(len(old_lines), differ_end_old + 1 + context)
    for i in range(differ_end_old + 1, end_old):
        out.append(f"  {old_lines[i]}")
    return "\n".join(out)


# ============================================================================
# MAIN
# ============================================================================

def check_file_exists(path: Path, label: str) -> bool:
    if not path.exists():
        print(f"ERROR: {label} not found at {path}. Run from repo root.")
        return False
    return True


def process_file(path, bak_path, simulate_fn, simulate_reverse_fn,
                 expected_line_delta_forward, args, label, check_parens,
                 forward_state_check_fn, reverse_state_check_fn):
    print(f"\n>>> {label} <<<")
    content = path.read_text()
    pre_lines = len(content.splitlines())
    print(f"  Path: {path}")
    print(f"  Pre-edit line count: {pre_lines}")
    if args.reverse:
        state_ok, state_msg = reverse_state_check_fn(content)
    else:
        state_ok, state_msg = forward_state_check_fn(content)
    print(f"  State check: {state_msg}")
    if not state_ok:
        print(f"  STATE CHECK FAILED for {label}. Aborting.")
        return False, content, ""
    try:
        simulated = simulate_reverse_fn(content) if args.reverse else simulate_fn(content)
    except RuntimeError as exc:
        print(f"  SIMULATION FAILED: {exc}")
        return False, content, ""
    post_lines = len(simulated.splitlines())
    line_delta = post_lines - pre_lines
    expected_delta = expected_line_delta_forward if not args.reverse else -expected_line_delta_forward
    c_lines = "OK" if line_delta == expected_delta else "FAIL"
    print(f"  Line delta: {line_delta} (expected {expected_delta}) ({c_lines})")
    if c_lines != "OK":
        print(f"  LINE DELTA FAILED for {label}. Aborting.")
        return False, content, simulated
    return True, content, simulated


def verify_disk(path, args, label, forward_check_fn, reverse_check_fn):
    disk = path.read_text()
    if args.reverse:
        ok, msg = forward_check_fn(disk)
    else:
        ok, msg = reverse_check_fn(disk)
    print(f"  {label} disk state: {msg}")
    return ok


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Pin Dockerfile build refs to the proven-working runtime commits"
    )
    parser.add_argument("--apply", action="store_true",
                        help="Actually write changes. Default is dry-run.")
    parser.add_argument("--reverse", action="store_true",
                        help="Reverse the edits. Combine with --apply to write.")
    args = parser.parse_args()

    direction = "REVERSE" if args.reverse else "APPLY"
    print(f"\n========== DOCKERFILE REF PINS: {direction} ==========")

    if not check_file_exists(DOCKERFILE_PATH, "Dockerfile"):
        return 1

    ok, orig, sim = process_file(
        DOCKERFILE_PATH, DOCKERFILE_BAK,
        simulate_forward, simulate_reverse,
        expected_line_delta_forward=6,
        args=args, label="Dockerfile",
        check_parens=False,
        forward_state_check_fn=forward_state_ok,
        reverse_state_check_fn=reverse_state_ok,
    )
    if not ok:
        return 1

    print("\n========== DIFF PREVIEW ==========")
    print(diff_preview_first_change(orig, sim, "Dockerfile", context=2))

    if not args.apply:
        print("\n========== DRY-RUN COMPLETE ==========")
        print("All checks pass. Re-run with --apply to write.")
        return 0

    if not args.reverse:
        if DOCKERFILE_BAK.exists():
            print(f"WARNING: backup {DOCKERFILE_BAK} exists; overwriting.")
        DOCKERFILE_BAK.write_text(orig)
        print(f"Backup written: {DOCKERFILE_BAK}")

    print("\n========== WRITING ==========")
    DOCKERFILE_PATH.write_text(sim)
    print(f"Wrote: {DOCKERFILE_PATH}")

    print("\n========== DISK VERIFICATION ==========")
    v = verify_disk(DOCKERFILE_PATH, args, "Dockerfile", forward_state_ok, reverse_state_ok)
    if not v:
        print("\nDISK VERIFICATION FAILED.")
        if not args.reverse:
            print("Restore: cp " + str(DOCKERFILE_BAK) + " " + str(DOCKERFILE_PATH))
        return 1

    print("\n========== DOCKERFILE REF PINS COMPLETE ==========")
    print("All edits applied. All checks pass.")
    if not args.reverse:
        print("\nVerification is the standard procedure (build must succeed, boot must reach iterations):")
        print("  docker compose build --no-cache clarityclaw && docker compose up -d")
    return 0


if __name__ == "__main__":
    sys.exit(main())
