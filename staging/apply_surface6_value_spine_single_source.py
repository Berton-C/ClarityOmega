#!/usr/bin/env python3
"""
Apply script: Surface 6 of Revision 1. Value-spine single-sourcing.
Returns every runtime value-atom read to ONE spec source: soul/soul_kernel.metta.

Purpose
-------
The value-spine (priority, tensions, irreversibility, paraconsistency) is
declared in parallel drift shapes alongside the spec source. Proven by the
2026-06-09 investigation (ValueSpine_Drift_Investigation_Findings.md):
- soul/identity_kernel.metta duplicates or diverges all four families
  (the cycle-2340 rebuild). Zero consumers (three container sweeps).
  Its magnitude irreversible-weight atoms make soul-irreversible-weight
  return TWO values (dual-head), which would make the Repair 1
  value-grounding verdict nondeterministic. This is why Surface 6 is a
  prerequisite-within-Revision-1 for Repair 1.
- soul/genesis_engine.metta L22-25 declares the four spec pairs in a local
  indexed shape. Orphaned within its own file (paraconsistency-test
  hard-codes its pairs; genesis machinery does not read the declarations).
  Sole external reader: the continuity_driver load-probe.
- continuity_driver (check-soul-file genesis-engine) probes
  (paraconsistency-pair 1) as a did-genesis-load check. Redirected to the
  surviving genesis_engine-native symbol (paraconsistency-test Safety
  Helpfulness), preserving the probe's purpose exactly.
- Six non-runtime declarers (not in the import chain, not consumed) are
  archived, not deleted.

NAMING-COLLISION GUARD: continuity_driver uses (priority ...) atoms at
L234/277/279 for goal-priority ordering, a DIFFERENT namespace from the
value hierarchy (priority Safety 1). This script's anchors cannot reach
them; nothing else in continuity_driver is touched.

The edits
---------
TEXT EDIT 1: lib_clarity_reasoning/lib_clarity_reasoning.metta
  Remove the identity_kernel import (line 22). The line is replaced with a
  tombstone comment so the position anchors the reverse. Line delta 0.

TEXT EDIT 2: soul/genesis_engine.metta
  Remove the four (= (paraconsistency-pair N) (pair A B)) declarations
  (L22-25), replaced with a tombstone comment. Real machinery
  (paraconsistency-test, genesis-hold, genesis-create, flourishing-test)
  untouched; the script verifies paraconsistency-test survives.
  Line delta -3.

TEXT EDIT 3: soul/continuity_driver.metta
  Redirect the genesis-engine load-probe from (paraconsistency-pair 1)
  empty-check to (paraconsistency-test Safety Helpfulness) checked against
  its reduction (tension-confirmed Safety Helpfulness). Loaded iff the
  genesis_engine clause reduces. Line delta 0.

TEXT EDITS 4-9: docs/design/artifact_1_loop_metta_wiring_diagram.md
  All anchors confirmed verbatim against the live file (2026-06-09 grep,
  2026-06-10 version-header read):
  4. L188 continuity_driver entry: note the probe redirect.
  5. L192 import-chain entry: identity_kernel import removed, spec home named.
  6. L229 CONSTITUTIONAL LAYER designation: re-homed from identity_kernel to
     soul_kernel (the spec single source). The architectural commitment text
     is preserved; only the file it points at changes.
  7. L859 irreversible-vocabulary reference: identity_kernel -> soul_kernel.
  8. L928 file table row: identity_kernel marked ARCHIVED.
  9. Version coherence, three parts on the live doc's convention (the v1.3
     refresh recorded itself as footer prose and never bumped the header):
     E9a header Version line v1.2 -> v1.4 (history preserved);
     E9b the L1041 "This document (v1.3) represents" sentence advanced to
     v1.4 with the per-cycle anchor re-audit honestly noted as pending;
     E9c a v1.4 changelog paragraph inserted after the L1043 v1.3 changelog
     line (substring-anchored; must occur exactly once or HALT).

FILE MOVES (forward: soul/ -> staging/OLD/OLD_soul_files/; reverse: back):
  M1. soul/identity_kernel.metta            (file)
  M2. soul/proposed_tension_atoms.metta     (file)
  M3. soul/flourishing_extentions           (directory)
  M4. soul/proposed_substrate_capacities.metta (file)
  M5. soul/flourishing_completeness_analysis.metta (file)
  M6. soul/hyperseed_extensions             (directory)
  M7. soul/tension_auto_logger.metta        (file)

HARNESS REMOVALS (forward only; tolerant; NOT auto-restored, recoverable
from session outputs):
  H1. soul/soul_accessor_live_harness.metta
  H2. soul_value_materials_harness.metta (checked at soul/ and repo root)

Net change
----------
- lib_clarity_reasoning.metta: 0 lines (import -> tombstone)
- genesis_engine.metta: -3 lines (4 decls -> 1 tombstone)
- continuity_driver.metta: 0 lines (5-line block -> 5-line block)
- artifact_1: edits 4-8 are same-line-count swaps; edit 9 adds the v1.4
  note block (delta computed from the block at runtime)
- Paren delta: 0 net and per .metta file (code-aware count; tombstones are
  comments and do not count)

Usage
-----
Dry-run (default):  python3 staging/apply_surface6_value_spine_single_source.py
Apply:              python3 staging/apply_surface6_value_spine_single_source.py --apply
Reverse:            python3 staging/apply_surface6_value_spine_single_source.py --reverse --apply

Run from repo root. Every run tees its full output to
shared_files/surface6_value_spine_<mode>_<UTCstamp>.log (shared_files/ maps
to the container's /tmp/; the log is the gold).

Pre-conditions (all CONFIRM-LIVE checked 2026-06-09 against the terminal)
-------------------------------------------------------------------------
- lib_clarity_reasoning L22 reads the identity_kernel import verbatim
- genesis_engine L22-25 read the four pair declarations verbatim
- continuity_driver L51-56 read the check-soul-file block verbatim
- the seven archival paths exist; none appear in the import chain
- artifact_1 anchors at L188/192/229/859/928 read verbatim

Post-apply verification (separate verify script / container checks)
--------------------------------------------------------------------
- soul-irreversible-weight shell returns a SINGLE value (dual-head resolved)
- soul-priority-hierarchy / soul-all-tensions / soul-paraconsistent-pairs
  return clean single-source values
- continuity_driver genesis-engine probe still reports loaded
- docker compose build --no-cache clarityclaw && docker compose up -d

Backup files (forward apply only):
- <each edited file>.bak.surface6
"""
from __future__ import annotations

import argparse
import datetime
import shutil
import sys
from pathlib import Path

# ============================================================================
# RUN LOG: tee all output to shared_files/ (the repo-root dir that maps to the
# container's /tmp/; the log is the gold)
# ============================================================================

_STAMP = datetime.datetime.utcnow().strftime("%Y%m%d_%H%M%S")
LOG_DIR = Path("shared_files")
LOG_PATH = None  # set in main() once the mode is known


class _Tee:
    def __init__(self, stream, logfile):
        self.stream = stream
        self.logfile = logfile

    def write(self, data):
        self.stream.write(data)
        self.logfile.write(data)

    def flush(self):
        self.stream.flush()
        self.logfile.flush()


# ============================================================================
# FILE PATHS
# ============================================================================

LIB_CR_PATH = Path("lib_clarity_reasoning/lib_clarity_reasoning.metta")
LIB_CR_BAK = Path("lib_clarity_reasoning/lib_clarity_reasoning.metta.bak.surface6")

GENESIS_PATH = Path("soul/genesis_engine.metta")
GENESIS_BAK = Path("soul/genesis_engine.metta.bak.surface6")

CONTINUITY_PATH = Path("soul/continuity_driver.metta")
CONTINUITY_BAK = Path("soul/continuity_driver.metta.bak.surface6")

ARTIFACT1_PATH = Path("docs/design/artifact_1_loop_metta_wiring_diagram.md")
ARTIFACT1_BAK = Path("docs/design/artifact_1_loop_metta_wiring_diagram.md.bak.surface6")

ARCHIVE_DIR = Path("staging/OLD/OLD_soul_files")

ARCHIVE_MOVES = [
    Path("soul/identity_kernel.metta"),
    Path("soul/proposed_tension_atoms.metta"),
    Path("soul/flourishing_extentions"),
    Path("soul/proposed_substrate_capacities.metta"),
    Path("soul/flourishing_completeness_analysis.metta"),
    Path("soul/hyperseed_extensions"),
    Path("soul/tension_auto_logger.metta"),
]

HARNESS_CANDIDATES = [
    Path("soul/soul_accessor_live_harness.metta"),
    Path("soul/soul_value_materials_harness.metta"),
    Path("soul_value_materials_harness.metta"),
]

# ============================================================================
# TEXT EDIT 1: lib_clarity_reasoning identity_kernel import removal
# ============================================================================

LIB_OLD_LINE = "!(import! &self (library omegaclaw ./soul/identity_kernel))"
LIB_NEW_LINE = (
    ";; identity_kernel import removed (Surface 6, 2026-06-09): proven drift"
    " duplicate of soul_kernel value atoms (dual-head irreversible-weight)."
    " File archived to staging/OLD/OLD_soul_files/. Spec single source:"
    " soul/soul_kernel.metta."
)

# ============================================================================
# TEXT EDIT 2: genesis_engine paraconsistency-pair declarations removal
# ============================================================================

GENESIS_OLD_BLOCK = (
    "(= (paraconsistency-pair 1) (pair Safety Helpfulness))\n"
    "(= (paraconsistency-pair 2) (pair AgencyBalance PurposeBeyondUtility))\n"
    "(= (paraconsistency-pair 3) (pair TimeCoherence CreativeTranscendence))\n"
    "(= (paraconsistency-pair 4) (pair SharedUnderstanding WonderPreservation))"
)
GENESIS_NEW_BLOCK = (
    ";; paraconsistency-pair declarations removed (Surface 6, 2026-06-09):"
    " drift duplicates of soul_kernel's soul-paraconsistent-pair atoms,"
    " orphaned within this file. Spec single source: soul/soul_kernel.metta."
)

# Survivor target that must remain after the edit (the probe redirect lands on it)
GENESIS_SURVIVOR = "paraconsistency-test"

# ============================================================================
# TEXT EDIT 3: continuity_driver load-probe redirect
# ============================================================================

CONTINUITY_OLD_BLOCK = (
    "(= (check-soul-file genesis-engine)\n"
    "   (let $result (paraconsistency-pair 1)\n"
    "      (if (== $result ())\n"
    "          not-loaded\n"
    "          loaded)))"
)
CONTINUITY_NEW_BLOCK = (
    "(= (check-soul-file genesis-engine)\n"
    "   (let $result (paraconsistency-test Safety Helpfulness)\n"
    "      (if (== $result (tension-confirmed Safety Helpfulness))\n"
    "          loaded\n"
    "          not-loaded)))"
)

# Goal-priority guard: these continuity_driver atoms are a different namespace
# and must be untouched. The edit cannot reach them, but we assert anyway.
CONTINUITY_GUARD_SUBSTR = "(priority"

# ============================================================================
# TEXT EDITS 4-9: artifact_1
# All OLD strings confirmed verbatim against the live file 2026-06-09.
# ============================================================================

ART_E4_OLD = "- soul/continuity_driver [gap flag: not yet read]"
ART_E4_NEW = (
    "- soul/continuity_driver (genesis-engine load-probe redirected to the"
    " surviving paraconsistency-test symbol per Surface 6, 2026-06-09)"
    " [gap flag: full read pending]"
)

ART_E5_OLD = (
    "- soul/identity_kernel (priority hierarchy, tension vectors,"
    " paraconsistency pairs, irreversible weights - all initialized as"
    " add-atom at import)"
)
ART_E5_NEW = (
    "- soul/identity_kernel: IMPORT REMOVED and file ARCHIVED (Surface 6,"
    " 2026-06-09). Its four value families were proven drift duplicates of"
    " soul/soul_kernel.metta, the spec single source for the value-spine."
)

ART_E6_OLD = (
    "- soul/identity_kernel: priority-rank atoms (1-5), tension-vector atoms"
    " (5), paraconsistency-pair atoms (4), irreversible-weight atoms (4)."
    " \U0001f9e0 **CONSTITUTIONAL LAYER (Layer 1+2 per spec_v3.0 Section 0):**"
    " these atoms are part of ClarityOmega's immutable constitutional layer."
    " Per the spec's architectural commitment, they should live in a"
    " runtime-read-only AtomSpace partition. The mechanism for runtime"
    " read-only enforcement (separate AtomSpace mounted read-only via import"
    " system, or per-atom marker-based protection) is an open question per"
    " Artifact 4 Section 10. Until that mechanism exists, the mutation gate"
    " at line 131 is the only protection, which is necessary but not"
    " sufficient for the architectural commitment."
)
ART_E6_NEW = (
    "- soul/soul_kernel: priority atoms (5), tension-vector atoms (5),"
    " soul-paraconsistent-pair atoms (4), numeric irreversible-weight atoms"
    " (7), plus accessor functions."
    " \U0001f9e0 **CONSTITUTIONAL LAYER (Layer 1+2 per spec_v3.0 Section 0):**"
    " these atoms are part of ClarityOmega's immutable constitutional layer,"
    " single-sourced in soul_kernel per Surface 6 (2026-06-09; the"
    " identity_kernel duplicate was proven drift and archived). Per the"
    " spec's architectural commitment, they should live in a"
    " runtime-read-only AtomSpace partition. The mechanism for runtime"
    " read-only enforcement (separate AtomSpace mounted read-only via import"
    " system, or per-atom marker-based protection) is an open question per"
    " Artifact 4 Section 10. Until that mechanism exists, the mutation gate"
    " is the only protection, which is necessary but not sufficient for the"
    " architectural commitment."
)

ART_E7_OLD = (
    "2. Apply irreversible-action-assessment from soul context (vocabulary"
    " already exists in identity_kernel and the static brief)"
)
ART_E7_NEW = (
    "2. Apply irreversible-action-assessment from soul context (vocabulary"
    " already exists in soul_kernel and the static brief)"
)

ART_E8_OLD = (
    "| soul/identity_kernel.metta | COLD (atoms seed at startup) | SN"
    " (priority hierarchy, tension vectors) |"
)
ART_E8_NEW = (
    "| soul/identity_kernel.metta | ARCHIVED (Surface 6: drift duplicate of"
    " soul_kernel; staging/OLD/OLD_soul_files/) | n/a |"
)

# Edit 9 (three parts, all anchored on verbatim live text, 2026-06-10):
# E9a: header Version line bumped to v1.4 (header was stale at v1.2, predating
#      this work; bumping it is the Discipline 4 version-coherence duty).
# E9b: the "This document (v1.3) represents..." sentence advanced to v1.4,
#      honestly noting the per-cycle anchor re-audit remains pending.
# E9c: a v1.4 changelog paragraph inserted after the v1.3 changelog line.

ART_E9A_OLD = (
    "**Version:** v1.2 (May 1, 2026; v1 Phase 1 was April 30, 2026; v1.1"
    " added NETWORK-RELEVANT flags)"
)
ART_E9A_NEW = (
    "**Version:** v1.4 (June 10, 2026; v1.3 June 4, 2026; v1.2 May 1, 2026;"
    " v1 Phase 1 April 30, 2026; v1.1 added NETWORK-RELEVANT flags)"
)

ART_E9B_OLD = (
    "This document (v1.3) represents the wiring of loop.metta as of June 4,"
    " 2026, re-anchored against the live 171-line loop."
)
ART_E9B_NEW = (
    "This document (v1.4) represents the wiring of loop.metta as of June 10,"
    " 2026; per-cycle line anchors carry from the v1.3 re-anchor and are"
    " pending re-audit against the live 178-line loop."
)

ART_V13_CHANGELOG_MARKER = "v1.3 changelog (June 4, 2026):"
ART_V14_NOTE = (
    "\n"
    "v1.4 changelog (June 10, 2026): Surface 6 value-spine single-sourcing."
    " identity_kernel import removed from lib_clarity_reasoning and the file"
    " archived (proven drift duplicate of soul_kernel; dual-head"
    " irreversible-weight resolved). genesis_engine's four local"
    " paraconsistency-pair declarations removed (orphaned drift; real"
    " machinery untouched). continuity_driver genesis-engine load-probe"
    " redirected to the surviving paraconsistency-test symbol."
    " CONSTITUTIONAL LAYER designation re-homed from identity_kernel to"
    " soul_kernel, the spec single source. Six non-runtime value-declarer"
    " files archived to staging/OLD/OLD_soul_files/. Per-cycle line anchor"
    " re-audit against the live 178-line loop remains pending.\n"
)

# ============================================================================
# HELPERS (template-conformant)
# ============================================================================

def code_aware_paren_count(text: str) -> tuple[int, int]:
    """Count parens excluding those inside string literals and line comments."""
    opens = 0
    closes = 0
    in_string = False
    escape = False
    i = 0
    n = len(text)
    while i < n:
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
                while i < n and text[i] != "\n":
                    i += 1
                continue
            elif ch == "(":
                opens += 1
            elif ch == ")":
                closes += 1
        i += 1
    return opens, closes


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


def require_once(content: str, target: str, label: str) -> None:
    count = find_target_substring_count(content, target)
    if count != 1:
        raise RuntimeError(f"{label}: expected anchor exactly once, found {count}.")


# ============================================================================
# SIMULATION (per file, forward and reverse)
# ============================================================================

def simulate_lib_forward(content: str) -> str:
    require_once(content, LIB_OLD_LINE, "lib forward: identity_kernel import")
    if LIB_NEW_LINE in content:
        raise RuntimeError("lib forward: tombstone already present.")
    return content.replace(LIB_OLD_LINE, LIB_NEW_LINE, 1)


def simulate_lib_reverse(content: str) -> str:
    require_once(content, LIB_NEW_LINE, "lib reverse: tombstone")
    return content.replace(LIB_NEW_LINE, LIB_OLD_LINE, 1)


def simulate_genesis_forward(content: str) -> str:
    require_once(content, GENESIS_OLD_BLOCK, "genesis forward: 4 pair declarations")
    if GENESIS_NEW_BLOCK in content:
        raise RuntimeError("genesis forward: tombstone already present.")
    out = content.replace(GENESIS_OLD_BLOCK, GENESIS_NEW_BLOCK, 1)
    if GENESIS_SURVIVOR not in out:
        raise RuntimeError(
            "genesis forward: survivor paraconsistency-test would not survive"
            " the edit. HALT (the probe redirect depends on it)."
        )
    return out


def simulate_genesis_reverse(content: str) -> str:
    require_once(content, GENESIS_NEW_BLOCK, "genesis reverse: tombstone")
    return content.replace(GENESIS_NEW_BLOCK, GENESIS_OLD_BLOCK, 1)


def simulate_continuity_forward(content: str) -> str:
    require_once(content, CONTINUITY_OLD_BLOCK, "continuity forward: probe block")
    guard_before = find_target_substring_count(content, CONTINUITY_GUARD_SUBSTR)
    out = content.replace(CONTINUITY_OLD_BLOCK, CONTINUITY_NEW_BLOCK, 1)
    guard_after = find_target_substring_count(out, CONTINUITY_GUARD_SUBSTR)
    if guard_before != guard_after:
        raise RuntimeError(
            f"continuity forward: goal-priority guard tripped"
            f" ({guard_before} -> {guard_after} '(priority' occurrences). HALT."
        )
    return out


def simulate_continuity_reverse(content: str) -> str:
    require_once(content, CONTINUITY_NEW_BLOCK, "continuity reverse: redirected block")
    return content.replace(CONTINUITY_NEW_BLOCK, CONTINUITY_OLD_BLOCK, 1)


def simulate_artifact1_forward(content: str) -> str:
    for old, new, label in [
        (ART_E4_OLD, ART_E4_NEW, "artifact1 E4 (continuity entry)"),
        (ART_E5_OLD, ART_E5_NEW, "artifact1 E5 (import-chain entry)"),
        (ART_E6_OLD, ART_E6_NEW, "artifact1 E6 (constitutional re-home)"),
        (ART_E7_OLD, ART_E7_NEW, "artifact1 E7 (vocabulary reference)"),
        (ART_E8_OLD, ART_E8_NEW, "artifact1 E8 (file table row)"),
        (ART_E9A_OLD, ART_E9A_NEW, "artifact1 E9a (header Version bump)"),
        (ART_E9B_OLD, ART_E9B_NEW, "artifact1 E9b (represents-sentence)"),
    ]:
        require_once(content, old, label)
        if new in content:
            raise RuntimeError(f"{label}: new text already present.")
        content = content.replace(old, new, 1)
    # E9c: v1.4 changelog paragraph after the v1.3 changelog line
    lines = content.splitlines(keepends=True)
    marker_idxs = [i for i, ln in enumerate(lines) if ART_V13_CHANGELOG_MARKER in ln]
    if len(marker_idxs) != 1:
        raise RuntimeError(
            f"artifact1 E9c: expected '{ART_V13_CHANGELOG_MARKER}' line exactly"
            f" once, found {len(marker_idxs)}."
        )
    if "v1.4 changelog (June 10, 2026):" in content:
        raise RuntimeError("artifact1 E9c: v1.4 changelog already present.")
    i = marker_idxs[0]
    lines.insert(i + 1, ART_V14_NOTE)
    return "".join(lines)


def simulate_artifact1_reverse(content: str) -> str:
    require_once(content, ART_V14_NOTE, "artifact1 reverse E9c: v1.4 changelog")
    content = content.replace(ART_V14_NOTE, "", 1)
    for new, old, label in [
        (ART_E9B_NEW, ART_E9B_OLD, "artifact1 reverse E9b"),
        (ART_E9A_NEW, ART_E9A_OLD, "artifact1 reverse E9a"),
        (ART_E8_NEW, ART_E8_OLD, "artifact1 reverse E8"),
        (ART_E7_NEW, ART_E7_OLD, "artifact1 reverse E7"),
        (ART_E6_NEW, ART_E6_OLD, "artifact1 reverse E6"),
        (ART_E5_NEW, ART_E5_OLD, "artifact1 reverse E5"),
        (ART_E4_NEW, ART_E4_OLD, "artifact1 reverse E4"),
    ]:
        require_once(content, new, label)
        content = content.replace(new, old, 1)
    return content


# ============================================================================
# STATE CHECKS (per file, both directions)
# ============================================================================

def lib_forward_state_ok(content: str) -> tuple[bool, str]:
    a = find_target_substring_count(content, LIB_OLD_LINE) == 1
    b = LIB_NEW_LINE not in content
    ok = a and b
    return ok, f"import present={a}, tombstone absent={b} -> {'OK' if ok else 'FAIL'}"


def lib_reverse_state_ok(content: str) -> tuple[bool, str]:
    a = find_target_substring_count(content, LIB_NEW_LINE) == 1
    return a, f"tombstone present={a} -> {'OK' if a else 'FAIL'}"


def genesis_forward_state_ok(content: str) -> tuple[bool, str]:
    a = find_target_substring_count(content, GENESIS_OLD_BLOCK) == 1
    b = GENESIS_NEW_BLOCK not in content
    c = GENESIS_SURVIVOR in content
    ok = a and b and c
    return ok, (
        f"decls present={a}, tombstone absent={b}, survivor present={c}"
        f" -> {'OK' if ok else 'FAIL'}"
    )


def genesis_reverse_state_ok(content: str) -> tuple[bool, str]:
    a = find_target_substring_count(content, GENESIS_NEW_BLOCK) == 1
    return a, f"tombstone present={a} -> {'OK' if a else 'FAIL'}"


def continuity_forward_state_ok(content: str) -> tuple[bool, str]:
    a = find_target_substring_count(content, CONTINUITY_OLD_BLOCK) == 1
    b = CONTINUITY_NEW_BLOCK not in content
    ok = a and b
    return ok, f"old probe present={a}, redirect absent={b} -> {'OK' if ok else 'FAIL'}"


def continuity_reverse_state_ok(content: str) -> tuple[bool, str]:
    a = find_target_substring_count(content, CONTINUITY_NEW_BLOCK) == 1
    return a, f"redirected probe present={a} -> {'OK' if a else 'FAIL'}"


def artifact1_forward_state_ok(content: str) -> tuple[bool, str]:
    olds = [ART_E4_OLD, ART_E5_OLD, ART_E6_OLD, ART_E7_OLD, ART_E8_OLD,
            ART_E9A_OLD, ART_E9B_OLD]
    present = [find_target_substring_count(content, o) == 1 for o in olds]
    marker = find_target_substring_count(content, ART_V13_CHANGELOG_MARKER) == 1
    no_v14 = "v1.4 changelog (June 10, 2026):" not in content
    ok = all(present) and marker and no_v14
    return ok, (
        f"anchors E4-E9b present={present}, v1.3 changelog marker={marker},"
        f" v1.4 absent={no_v14} -> {'OK' if ok else 'FAIL'}"
    )


def artifact1_reverse_state_ok(content: str) -> tuple[bool, str]:
    news = [ART_E4_NEW, ART_E5_NEW, ART_E6_NEW, ART_E7_NEW, ART_E8_NEW,
            ART_E9A_NEW, ART_E9B_NEW]
    present = [find_target_substring_count(content, n) == 1 for n in news]
    v14 = find_target_substring_count(content, ART_V14_NOTE) == 1
    ok = all(present) and v14
    return ok, f"new E4-E9b present={present}, v1.4 present={v14} -> {'OK' if ok else 'FAIL'}"


# ============================================================================
# DIFF PREVIEW (template-conformant)
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
    out = [f"--- {label} (first changed region) ---"]
    start = max(0, differ_start - context)
    for i in range(start, differ_start):
        if i < len(old_lines):
            out.append(f"  {old_lines[i]}")
    shown = 0
    for i in range(differ_start, min(differ_end_old + 1, differ_start + 12)):
        if i < len(old_lines):
            out.append(f"- {old_lines[i]}")
            shown += 1
    for i in range(differ_start, min(differ_end_new + 1, differ_start + 12)):
        if i < len(new_lines):
            out.append(f"+ {new_lines[i]}")
    end_old = min(len(old_lines), differ_end_old + 1 + context)
    for i in range(differ_end_old + 1, end_old):
        out.append(f"  {old_lines[i]}")
    return "\n".join(out)


# ============================================================================
# PROCESS (template-conformant)
# ============================================================================

def check_file_exists(path: Path, label: str) -> bool:
    if not path.exists():
        print(f"ERROR: {label} not found at {path}. Run from repo root.")
        return False
    return True


def process_file(path, simulate_fn, simulate_reverse_fn,
                 expected_line_delta_forward, args, label, check_parens,
                 forward_state_check_fn, reverse_state_check_fn):
    print(f"\n>>> {label} <<<")
    content = path.read_text()
    pre_lines = len(content.splitlines())
    pre_o, pre_c = code_aware_paren_count(content)
    pre_d = pre_o - pre_c
    print(f"  Path: {path}")
    print(f"  Pre-edit line count: {pre_lines}")
    if check_parens:
        ok_p = pre_d == 0
        print(f"  Pre-edit paren count: opens={pre_o} closes={pre_c} delta={pre_d} ({'OK' if ok_p else 'FAIL'})")
        if not ok_p:
            print(f"  PAREN COUNT FAILED for {label}. Aborting.")
            return False, content, ""
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
    if check_parens:
        post_o, post_c = code_aware_paren_count(simulated)
        post_d = post_o - post_c
        ok_pp = post_d == 0
        print(f"  Post-edit paren count: opens={post_o} closes={post_c} delta={post_d} ({'OK' if ok_pp else 'FAIL'})")
        if not ok_pp:
            print(f"  POST-EDIT PAREN COUNT FAILED for {label}. Aborting.")
            return False, content, simulated
    expected_delta = expected_line_delta_forward if not args.reverse else -expected_line_delta_forward
    ok_l = line_delta == expected_delta
    print(f"  Line delta: {line_delta} (expected {expected_delta}) ({'OK' if ok_l else 'FAIL'})")
    if not ok_l:
        print(f"  LINE DELTA FAILED for {label}. Aborting.")
        return False, content, simulated
    return True, content, simulated


def verify_disk(path, args, label, forward_check_fn, reverse_check_fn, check_parens):
    disk = path.read_text()
    if check_parens:
        o, c = code_aware_paren_count(disk)
        d = o - c
        ok_p = d == 0
        print(f"  {label} disk paren: opens={o} closes={c} delta={d} ({'OK' if ok_p else 'FAIL'})")
        if not ok_p:
            return False
    if args.reverse:
        ok, msg = forward_check_fn(disk)
    else:
        ok, msg = reverse_check_fn(disk)
    print(f"  {label} disk state: {msg}")
    return ok


# ============================================================================
# MOVES (reversible) AND HARNESS REMOVALS (tolerant, forward only)
# ============================================================================

def check_moves(args) -> bool:
    print("\n>>> FILE MOVES (pre-check) <<<")
    ok = True
    for src in ARCHIVE_MOVES:
        dst = ARCHIVE_DIR / src.name
        if not args.reverse:
            src_ok = src.exists()
            dst_clear = not dst.exists()
            print(f"  {src} -> {dst}: source present={src_ok}, dest clear={dst_clear}")
            ok = ok and src_ok and dst_clear
        else:
            src_ok = dst.exists()
            dst_clear = not src.exists()
            print(f"  {dst} -> {src}: archived present={src_ok}, soul/ clear={dst_clear}")
            ok = ok and src_ok and dst_clear
    if not ok:
        print("  MOVE PRE-CHECK FAILED. Aborting (no writes have occurred).")
    return ok


def do_moves(args) -> bool:
    print("\n>>> FILE MOVES (executing) <<<")
    ARCHIVE_DIR.mkdir(parents=True, exist_ok=True)
    for src in ARCHIVE_MOVES:
        dst = ARCHIVE_DIR / src.name
        if not args.reverse:
            shutil.move(str(src), str(dst))
            print(f"  moved {src} -> {dst}")
        else:
            shutil.move(str(dst), str(src))
            print(f"  moved {dst} -> {src}")
    return True


def do_harness_removals(args) -> None:
    if args.reverse:
        print("\n>>> HARNESS REMOVALS: skipped on reverse (not auto-restored;"
              " recoverable from session outputs) <<<")
        return
    print("\n>>> HARNESS REMOVALS (tolerant; forward only) <<<")
    for p in HARNESS_CANDIDATES:
        if p.exists():
            p.unlink()
            print(f"  removed {p} (NOT auto-restored; recoverable from outputs)")
        else:
            print(f"  {p}: already absent (OK)")


# ============================================================================
# MAIN
# ============================================================================

def main() -> int:
    parser = argparse.ArgumentParser(
        description="Surface 6: value-spine single-sourcing to soul_kernel"
    )
    parser.add_argument("--apply", action="store_true",
                        help="Actually write changes. Default is dry-run.")
    parser.add_argument("--reverse", action="store_true",
                        help="Reverse the edits. Combine with --apply to write.")
    args = parser.parse_args()

    global LOG_PATH
    mode_tag = ("reverse" if args.reverse else "forward") + ("_apply" if args.apply else "_dryrun")
    LOG_DIR.mkdir(parents=True, exist_ok=True)
    LOG_PATH = LOG_DIR / f"surface6_value_spine_{mode_tag}_{_STAMP}.log"
    logfile = open(LOG_PATH, "w")
    sys.stdout = _Tee(sys.__stdout__, logfile)

    direction = "REVERSE" if args.reverse else "FORWARD"
    mode = "APPLY" if args.apply else "DRY-RUN"
    print(f"\n========== SURFACE 6 VALUE-SPINE: {direction} ({mode}) ==========")
    print(f"Run log: {LOG_PATH}")

    if not all([
        check_file_exists(LIB_CR_PATH, "lib_clarity_reasoning"),
        check_file_exists(GENESIS_PATH, "genesis_engine"),
        check_file_exists(CONTINUITY_PATH, "continuity_driver"),
        check_file_exists(ARTIFACT1_PATH, "artifact_1"),
    ]):
        return 1

    ok_lib, lib_orig, lib_sim = process_file(
        LIB_CR_PATH, simulate_lib_forward, simulate_lib_reverse,
        expected_line_delta_forward=0, args=args,
        label="lib_clarity_reasoning.metta", check_parens=True,
        forward_state_check_fn=lib_forward_state_ok,
        reverse_state_check_fn=lib_reverse_state_ok)
    if not ok_lib:
        return 1

    ok_gen, gen_orig, gen_sim = process_file(
        GENESIS_PATH, simulate_genesis_forward, simulate_genesis_reverse,
        expected_line_delta_forward=-3, args=args,
        label="genesis_engine.metta", check_parens=True,
        forward_state_check_fn=genesis_forward_state_ok,
        reverse_state_check_fn=genesis_reverse_state_ok)
    if not ok_gen:
        return 1

    ok_con, con_orig, con_sim = process_file(
        CONTINUITY_PATH, simulate_continuity_forward, simulate_continuity_reverse,
        expected_line_delta_forward=0, args=args,
        label="continuity_driver.metta", check_parens=True,
        forward_state_check_fn=continuity_forward_state_ok,
        reverse_state_check_fn=continuity_reverse_state_ok)
    if not ok_con:
        return 1

    art_delta = ART_V14_NOTE.count("\n")
    ok_art, art_orig, art_sim = process_file(
        ARTIFACT1_PATH, simulate_artifact1_forward, simulate_artifact1_reverse,
        expected_line_delta_forward=art_delta, args=args,
        label="artifact_1.md", check_parens=False,
        forward_state_check_fn=artifact1_forward_state_ok,
        reverse_state_check_fn=artifact1_reverse_state_ok)
    if not ok_art:
        return 1

    if not check_moves(args):
        return 1

    print("\n========== DIFF PREVIEWS ==========")
    print(diff_preview_first_change(lib_orig, lib_sim, "lib_clarity_reasoning.metta", 2))
    print()
    print(diff_preview_first_change(gen_orig, gen_sim, "genesis_engine.metta", 2))
    print()
    print(diff_preview_first_change(con_orig, con_sim, "continuity_driver.metta", 2))
    print()
    print(diff_preview_first_change(art_orig, art_sim, "artifact_1.md", 1))

    if not args.apply:
        print("\n========== ACTION-SUMMARY (DRY-RUN) ==========")
        print("  4 text files simulated clean; 7 archival moves pre-checked;")
        print("  2 harness removals pending (tolerant); paren-delta 0; all checks pass.")
        print("  No writes have occurred. Re-run with --apply to write.")
        print(f"  Full log: {LOG_PATH}")
        return 0

    if not args.reverse:
        for path, bak in [(LIB_CR_PATH, LIB_CR_BAK), (GENESIS_PATH, GENESIS_BAK),
                          (CONTINUITY_PATH, CONTINUITY_BAK), (ARTIFACT1_PATH, ARTIFACT1_BAK)]:
            if bak.exists():
                print(f"WARNING: backup {bak} exists; overwriting.")
            bak.write_text(path.read_text())
            print(f"Backup written: {bak}")

    print("\n========== WRITING ==========")
    LIB_CR_PATH.write_text(lib_sim)
    print(f"Wrote: {LIB_CR_PATH}")
    GENESIS_PATH.write_text(gen_sim)
    print(f"Wrote: {GENESIS_PATH}")
    CONTINUITY_PATH.write_text(con_sim)
    print(f"Wrote: {CONTINUITY_PATH}")
    ARTIFACT1_PATH.write_text(art_sim)
    print(f"Wrote: {ARTIFACT1_PATH}")

    do_moves(args)
    do_harness_removals(args)

    print("\n========== DISK VERIFICATION ==========")
    v1 = verify_disk(LIB_CR_PATH, args, "lib_clarity_reasoning.metta",
                     lib_forward_state_ok, lib_reverse_state_ok, True)
    v2 = verify_disk(GENESIS_PATH, args, "genesis_engine.metta",
                     genesis_forward_state_ok, genesis_reverse_state_ok, True)
    v3 = verify_disk(CONTINUITY_PATH, args, "continuity_driver.metta",
                     continuity_forward_state_ok, continuity_reverse_state_ok, True)
    v4 = verify_disk(ARTIFACT1_PATH, args, "artifact_1.md",
                     artifact1_forward_state_ok, artifact1_reverse_state_ok, False)
    moves_ok = True
    for src in ARCHIVE_MOVES:
        dst = ARCHIVE_DIR / src.name
        if not args.reverse:
            here = dst.exists() and not src.exists()
        else:
            here = src.exists() and not dst.exists()
        print(f"  move verified: {src.name} -> {'OK' if here else 'FAIL'}")
        moves_ok = moves_ok and here

    if not (v1 and v2 and v3 and v4 and moves_ok):
        print("\nDISK VERIFICATION FAILED. File(s) may be in inconsistent state.")
        if not args.reverse:
            print("Restore text files from .bak.surface6 copies; moves reverse via --reverse --apply.")
        return 1

    print("\n========== ACTION-SUMMARY ==========")
    print(f"  Direction: {direction}. 4 text files edited, 7 paths"
          f" {'archived' if not args.reverse else 'restored'},"
          f" harness removals {'done/tolerant' if not args.reverse else 'skipped'}.")
    print("  Paren-delta 0 per file. All disk verifications pass.")
    print(f"  Full log: {LOG_PATH}")
    if not args.reverse:
        print("\nNext: rebuild + restart, then container verification:")
        print("  docker compose build --no-cache clarityclaw && docker compose up -d")
        print("  Key check: soul-irreversible-weight shell returns a SINGLE value;")
        print("  continuity_driver genesis-engine probe reports loaded.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
