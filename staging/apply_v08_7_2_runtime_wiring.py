#!/usr/bin/env python3
"""
Apply script: v08.7.2 runtime wiring dry-run / apply.

Purpose
-------
Wires the v08.7.2 Soul/Evolutionary Canonical Topology candidate into the
runtime import surface and soul file-class allow-list, after the candidate has
already passed non-mutating container /tmp runtime verification.

Default is DRY-RUN. Nothing is written unless --apply is provided.

Edits
-----
Edit 1: lib_clarity_reasoning/lib_clarity_reasoning.metta
  Add one marked import block for:
    - v08.7.2 quantale engine
    - soul/evolutionary topology files
    - soul/durable.metta

Edit 2: soul/soul_kernel.metta
  Add one marked file-class block for:
    - /PeTTa/repos/omegaclaw/soul/durable.metta journal
    - /PeTTa/repos/omegaclaw/soul/evolutionary/*.metta journal append surfaces

Why journal?
------------
In v08.7.2, journal remains the mechanical append-permission class. Durable
canon status is still semantic and must be earned by the v08.7.2 lifecycle.
The soul/evolutionary/* files are process-memory/evidence surfaces, not canon.

Usage
-----
Dry-run:
    python3 staging/apply_v08_7_2_runtime_wiring.py

Apply:
    python3 staging/apply_v08_7_2_runtime_wiring.py --apply

Reverse dry-run:
    python3 staging/apply_v08_7_2_runtime_wiring.py --reverse

Reverse apply:
    python3 staging/apply_v08_7_2_runtime_wiring.py --reverse --apply

After apply
-----------
Rebuild/restart the container, then rerun the v08.7.2 harness. Expected next
state: kernel class HOLD clears if the import/class block is parsed by the live
runtime and the harness sees it in source.
"""
from __future__ import annotations

import argparse
import difflib
import sys
from pathlib import Path

# =============================================================================
# CONFIG
# =============================================================================

LIB_CR_PATH = Path("lib_clarity_reasoning/lib_clarity_reasoning.metta")
LIB_CR_BAK = Path("lib_clarity_reasoning/lib_clarity_reasoning.metta.bak.v08_7_2_wiring")

SOUL_KERNEL_PATH = Path("soul/soul_kernel.metta")
SOUL_KERNEL_BAK = Path("soul/soul_kernel.metta.bak.v08_7_2_wiring")

ENGINE_PATH = Path("lib_clarity_reasoning/lib_quantale_autopoietic_epistemic_dynamics_engine_v08_7_2_SOUL_EVOLUTIONARY_CANONICAL_TOPOLOGY.metta")

TOPOLOGY_FILES = [
    Path("soul/evolutionary/README.metta"),
    Path("soul/evolutionary/index.metta"),
    Path("soul/evolutionary/runtime.metta"),
    Path("soul/evolutionary/pending.metta"),
    Path("soul/evolutionary/validation.metta"),
    Path("soul/evolutionary/restart.metta"),
    Path("soul/evolutionary/rejected.metta"),
    Path("soul/evolutionary/archive/README.metta"),
    Path("soul/durable.metta"),
]

LIB_BLOCK_BEGIN = ";; BEGIN v08.7.2 soul-evolutionary quantale import block"
LIB_BLOCK_END = ";; END v08.7.2 soul-evolutionary quantale import block"

KERNEL_BLOCK_BEGIN = ";; BEGIN v08.7.2 soul-evolutionary file-class block"
KERNEL_BLOCK_END = ";; END v08.7.2 soul-evolutionary file-class block"

ENGINE_IMPORT = "!(import! &self (library omegaclaw ./lib_clarity_reasoning/lib_quantale_autopoietic_epistemic_dynamics_engine_v08_7_2_SOUL_EVOLUTIONARY_CANONICAL_TOPOLOGY))"

SOUL_IMPORTS = [
    "!(import! &self (library omegaclaw ./soul/evolutionary/README))",
    "!(import! &self (library omegaclaw ./soul/evolutionary/index))",
    "!(import! &self (library omegaclaw ./soul/evolutionary/runtime))",
    "!(import! &self (library omegaclaw ./soul/evolutionary/pending))",
    "!(import! &self (library omegaclaw ./soul/evolutionary/validation))",
    "!(import! &self (library omegaclaw ./soul/evolutionary/restart))",
    "!(import! &self (library omegaclaw ./soul/evolutionary/rejected))",
    "!(import! &self (library omegaclaw ./soul/evolutionary/archive/README))",
    "!(import! &self (library omegaclaw ./soul/durable))",
]

LIB_IMPORT_BLOCK = "\n".join([
    "",
    LIB_BLOCK_BEGIN,
    ";; v08.7.2: quantale durable evolutionary governance engine + soul-owned topology",
    ENGINE_IMPORT,
    *SOUL_IMPORTS,
    LIB_BLOCK_END,
    "",
])

# Prefer to insert after findings.metta journal if present; fallback to arc_log.md.
KERNEL_ANCHOR_CANDIDATES = [
    '!(add-atom &self (soul-file-class "/PeTTa/repos/omegaclaw/soul/findings.metta" journal))',
    '!(add-atom &self (soul-file-class "/PeTTa/repos/omegaclaw/soul/arc_log.md" journal))',
]

KERNEL_CLASS_LINES = [
    '!(add-atom &self (soul-file-class "/PeTTa/repos/omegaclaw/soul/durable.metta" journal))',
    '!(add-atom &self (soul-file-class "/PeTTa/repos/omegaclaw/soul/evolutionary/runtime.metta" journal))',
    '!(add-atom &self (soul-file-class "/PeTTa/repos/omegaclaw/soul/evolutionary/pending.metta" journal))',
    '!(add-atom &self (soul-file-class "/PeTTa/repos/omegaclaw/soul/evolutionary/validation.metta" journal))',
    '!(add-atom &self (soul-file-class "/PeTTa/repos/omegaclaw/soul/evolutionary/restart.metta" journal))',
    '!(add-atom &self (soul-file-class "/PeTTa/repos/omegaclaw/soul/evolutionary/rejected.metta" journal))',
]

KERNEL_CLASS_BLOCK = "\n".join([
    "",
    KERNEL_BLOCK_BEGIN,
    ";; v08.7.2: journal is mechanical append permission; durable canon remains semantic.",
    *KERNEL_CLASS_LINES,
    KERNEL_BLOCK_END,
    "",
])

# =============================================================================
# HELPERS
# =============================================================================

def code_aware_paren_count(text: str) -> tuple[int, int]:
    """Count parens excluding string literals and line comments."""
    opens = 0
    closes = 0
    in_string = False
    escape = False
    i = 0
    while i < len(text):
        ch = text[i]
        if in_string:
            if escape:
                escape = False
            elif ch == "\\":
                escape = True
            elif ch == '"':
                in_string = False
        else:
            if ch == '"':
                in_string = True
            elif ch == ";":
                while i < len(text) and text[i] != "\n":
                    i += 1
                continue
            elif ch == "(":
                opens += 1
            elif ch == ")":
                closes += 1
        i += 1
    return opens, closes


def check_balanced_metta(path: Path, label: str) -> bool:
    text = path.read_text()
    o, c = code_aware_paren_count(text)
    ok = o == c
    print(f"  {label} paren: opens={o} closes={c} delta={o-c} ({'OK' if ok else 'FAIL'})")
    return ok


def one_balanced_directive(line: str) -> bool:
    s = line.strip()
    if not s or s.startswith(";;"):
        return True
    if not s.startswith("!(add-atom &self "):
        return False
    o, c = code_aware_paren_count(s)
    return o == c


def validate_topology_files() -> bool:
    print("\n========== TOPOLOGY FILE VALIDATION ==========")
    ok = True
    paths = [ENGINE_PATH, *TOPOLOGY_FILES]
    for path in paths:
        if not path.exists():
            print(f"  MISSING: {path}")
            ok = False
        else:
            print(f"  present: {path} ({path.stat().st_size} bytes)")
    if not ok:
        return False

    for path in TOPOLOGY_FILES:
        bad = []
        for n, line in enumerate(path.read_text().splitlines(), start=1):
            if not one_balanced_directive(line):
                bad.append((n, line.strip()))
        if bad:
            print(f"  SERIALIZATION FAIL: {path}")
            for n, line in bad:
                print(f"    line {n}: {line}")
            ok = False
        else:
            print(f"  serialization OK: {path}")
    return ok


def exact_count(text: str, needle: str) -> int:
    count = 0
    start = 0
    while True:
        idx = text.find(needle, start)
        if idx == -1:
            return count
        count += 1
        start = idx + 1


def has_block(text: str, begin: str, end: str) -> bool:
    return begin in text and end in text


def remove_block(text: str, begin: str, end: str) -> str:
    start = text.find(begin)
    if start == -1:
        raise RuntimeError(f"begin marker not found: {begin}")
    # Include preceding blank line if present.
    if start > 0 and text[start - 1] == "\n":
        start -= 1
    finish = text.find(end, start)
    if finish == -1:
        raise RuntimeError(f"end marker not found: {end}")
    finish += len(end)
    # Include following newline(s)
    while finish < len(text) and text[finish] == "\n":
        finish += 1
    return text[:start] + text[finish:]


def insert_lib_block_forward(text: str) -> str:
    if has_block(text, LIB_BLOCK_BEGIN, LIB_BLOCK_END):
        raise RuntimeError("lib import block already present")
    if ENGINE_IMPORT in text:
        raise RuntimeError("engine import already present outside managed block")
    # EOF append is intentional: import manifests are order-tolerant for this pure library import.
    if not text.endswith("\n"):
        text += "\n"
    return text + LIB_IMPORT_BLOCK


def insert_lib_block_reverse(text: str) -> str:
    if not has_block(text, LIB_BLOCK_BEGIN, LIB_BLOCK_END):
        raise RuntimeError("lib import block not present")
    return remove_block(text, LIB_BLOCK_BEGIN, LIB_BLOCK_END)


def insert_kernel_block_forward(text: str) -> str:
    if has_block(text, KERNEL_BLOCK_BEGIN, KERNEL_BLOCK_END):
        raise RuntimeError("kernel file-class block already present")
    for line in KERNEL_CLASS_LINES:
        if line in text:
            raise RuntimeError(f"kernel class line already present outside managed block: {line}")

    for anchor in KERNEL_ANCHOR_CANDIDATES:
        if exact_count(text, anchor) == 1:
            return text.replace(anchor, anchor + KERNEL_CLASS_BLOCK.rstrip("\n"), 1)
    raise RuntimeError("no suitable kernel anchor found; expected findings.metta or arc_log.md journal class line")


def insert_kernel_block_reverse(text: str) -> str:
    if not has_block(text, KERNEL_BLOCK_BEGIN, KERNEL_BLOCK_END):
        raise RuntimeError("kernel file-class block not present")
    return remove_block(text, KERNEL_BLOCK_BEGIN, KERNEL_BLOCK_END)


def unified_preview(old: str, new: str, label: str, max_lines: int = 120) -> str:
    old_lines = old.splitlines(keepends=True)
    new_lines = new.splitlines(keepends=True)
    diff = list(difflib.unified_diff(old_lines, new_lines, fromfile=label + ".old", tofile=label + ".new"))
    if len(diff) > max_lines:
        diff = diff[:max_lines] + [f"... diff truncated at {max_lines} lines ...\n"]
    return "".join(diff) if diff else f"--- {label}: no changes ---\n"


def write_with_backup(path: Path, bak: Path, new_text: str) -> None:
    if bak.exists():
        print(f"  WARNING: overwriting backup {bak}")
    bak.write_text(path.read_text())
    path.write_text(new_text)
    print(f"  wrote {path}; backup {bak}")


def state_summary(lib_text: str, kernel_text: str) -> None:
    print("\n========== STATE SUMMARY ==========")
    print(f"  lib block present: {has_block(lib_text, LIB_BLOCK_BEGIN, LIB_BLOCK_END)}")
    print(f"  kernel block present: {has_block(kernel_text, KERNEL_BLOCK_BEGIN, KERNEL_BLOCK_END)}")
    for line in KERNEL_CLASS_LINES:
        print(f"  class line present: {line in kernel_text} :: {line}")
    print(f"  engine import present: {ENGINE_IMPORT in lib_text}")


def main() -> int:
    parser = argparse.ArgumentParser(description="v08.7.2 runtime wiring dry-run/apply script")
    parser.add_argument("--apply", action="store_true", help="write changes; default is dry-run")
    parser.add_argument("--reverse", action="store_true", help="remove managed v08.7.2 wiring blocks")
    args = parser.parse_args()

    print(f"\n========== v08.7.2 RUNTIME WIRING {'REVERSE' if args.reverse else 'FORWARD'} ==========")
    print("Mode:", "APPLY" if args.apply else "DRY-RUN")

    if not validate_topology_files():
        print("\nPRECHECK FAILED: missing or malformed candidate files.")
        return 1

    for path, label in [(LIB_CR_PATH, "lib_clarity_reasoning"), (SOUL_KERNEL_PATH, "soul_kernel")]:
        if not path.exists():
            print(f"ERROR: {label} not found at {path}. Run from repo root.")
            return 1
        if not check_balanced_metta(path, label):
            return 1

    lib_old = LIB_CR_PATH.read_text()
    kernel_old = SOUL_KERNEL_PATH.read_text()
    state_summary(lib_old, kernel_old)

    try:
        if args.reverse:
            lib_new = insert_lib_block_reverse(lib_old)
            kernel_new = insert_kernel_block_reverse(kernel_old)
        else:
            lib_new = insert_lib_block_forward(lib_old)
            kernel_new = insert_kernel_block_forward(kernel_old)
    except RuntimeError as exc:
        print(f"\nSIMULATION FAILED: {exc}")
        return 1

    # Paren checks post-simulation
    for label, text in [("lib_clarity_reasoning simulated", lib_new), ("soul_kernel simulated", kernel_new)]:
        o, c = code_aware_paren_count(text)
        print(f"  {label} paren: opens={o} closes={c} delta={o-c} ({'OK' if o == c else 'FAIL'})")
        if o != c:
            return 1

    print("\n========== DIFF PREVIEW ==========")
    print(unified_preview(lib_old, lib_new, str(LIB_CR_PATH)))
    print(unified_preview(kernel_old, kernel_new, str(SOUL_KERNEL_PATH)))

    if not args.apply:
        print("\n========== DRY-RUN COMPLETE ==========")
        print("All checks passed. Re-run with --apply to write managed blocks.")
        return 0

    print("\n========== WRITING ==========")
    write_with_backup(LIB_CR_PATH, LIB_CR_BAK, lib_new)
    write_with_backup(SOUL_KERNEL_PATH, SOUL_KERNEL_BAK, kernel_new)

    print("\n========== DISK VERIFICATION ==========")
    lib_disk = LIB_CR_PATH.read_text()
    kernel_disk = SOUL_KERNEL_PATH.read_text()
    state_summary(lib_disk, kernel_disk)
    if args.reverse:
        ok = not has_block(lib_disk, LIB_BLOCK_BEGIN, LIB_BLOCK_END) and not has_block(kernel_disk, KERNEL_BLOCK_BEGIN, KERNEL_BLOCK_END)
    else:
        ok = has_block(lib_disk, LIB_BLOCK_BEGIN, LIB_BLOCK_END) and has_block(kernel_disk, KERNEL_BLOCK_BEGIN, KERNEL_BLOCK_END)
        ok = ok and all(line in kernel_disk for line in KERNEL_CLASS_LINES) and ENGINE_IMPORT in lib_disk
    if not ok:
        print("DISK VERIFICATION FAILED.")
        return 1
    if not check_balanced_metta(LIB_CR_PATH, "lib_clarity_reasoning disk"):
        return 1
    if not check_balanced_metta(SOUL_KERNEL_PATH, "soul_kernel disk"):
        return 1

    print("\n========== v08.7.2 RUNTIME WIRING COMPLETE ==========")
    if not args.reverse:
        print("Next:")
        print("  1. Rebuild/restart container.")
        print("  2. Rerun quantale_v08_7_2_soul_evolutionary_topology_harness_v01_6.py.")
        print("  3. Expect the durable.metta journal class HOLD to clear if the kernel block is correct.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
