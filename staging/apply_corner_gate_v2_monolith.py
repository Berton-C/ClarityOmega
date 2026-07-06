#!/usr/bin/env python3
"""
Apply script: corner-gate v2 monolithic repair. All edits land as one
coordinated change. All or none.

Purpose
-------
Delivers the blessed corner-gate v2 (roadmap v1.2, design v1.3) in one apply:
channel hygiene, graded quantale detection, pattern-scoped enforcement with
structural release. Supersedes the interim mothball (the v1 latch never
returns). Every behavior in this script was probe-proven in throwaway
containers on 2026-07-06 (probe battery B1-B7, output preserved in project
knowledge "Untitled 37.txt"; filter fixtures P1-P4 passed earlier same day).

Probe evidence per behavior:
- Graded firing: B1 (corner-shaped window -> corner-confirmed-core true)
- Thin-data immunity: B2 (one action -> intention pbit (mk-pbit 1 0.2),
  confirmed false)
- STRUCTURAL RELEASE: B3 (one forward state-delta -> confirmed false)
- Composure on silence: B4 (zero emission -> confirmed false)
- Pattern scoping: B6 (recorded (shell "ls") dropped, novel (shell "pwd")
  passed) which subsumes B5's member/novel discrimination
- Person-window exemption: B6 (msgnew True passes everything)
- Results shaping: B7 mixed (real return kept verbatim, prose echo replaced
  by mechanical marker); P1-P4 (empty, real, prose, bare-symbol fixtures)
- Chain reducibility on loaded operators: probe A (emission (mk-pbit 1.0 0.9),
  outcome-flat (mk-pbit 1.0 0.7), core (mk-pbit 1.0 0.7)); q-geq resolves
  from lib_self_continuity.metta:14 (imported, manifest line 7, single
  definition site verified by tree grep)

The edits (numbered, all-or-none)
---------------------------------
FILE 1: soul/corner_gap/corner_gate.metta (3 edits)
  Edit 1A: the MOTHBALLED apply-corner-gate block (3 lines) is replaced by
    apply-corner-gate-v2 (8 lines): pattern-scoped, msgnew-exempt, fires on
    corner-confirmed-core. The mothball is retired by SUPERSESSION per
    roadmap Section 7; the v1 latch body never returns.
  Edit 1B: gate-aware-results body (4 lines) replaced by the probe-B7 body
    (8 lines): real command returns pass; prose echoes become
    (COMMAND_RETURN: (non-command-element not-executed)); an empty batch
    yields (held-by-corner-gate) when the graded corner is confirmed, else
    (no-commands-executed-this-cycle). Marker text is Clarity's to amend.
  Edit 1C: append the pure filter functions (probe-proven bodies verbatim):
    allowed-heads, head-in-list?, real-return?, filter-returns,
    cmd-in-corner-window?, filter-corner-cmds.
  NOT touched: corner-gate-active (mothballed False, now vestigial, no
  consumers per the T1 full-tree grep); corner-gate-feedback (the v1
  stillness text, defined but unused; retirement is a housekeeping item).

FILE 2: soul/corner_gap/corner_window_writers.metta (CREATED forward,
  DELETED reverse)
  The confirmation-scoped ephemeral command record: do-clear-corner-window!
  (ADR-005 superpose clear), do-record-corner-window! (probe B5/B6 body),
  populate-corner-window! (record while corner-confirmed-core, clear
  otherwise; if-dispatch composition of probed parts). Never persistent,
  never a disposition surface (design v1.3).

FILE 3: lib_clarity_reasoning/lib_clarity_reasoning.metta (1 edit)
  The corner_gate import line gains coupling_quantale_merge BEFORE it and
  corner_window_writers AFTER it, with role comments. This is what makes
  quantale gating LIVE. Zero new math: q-geq already loaded via
  lib_self_continuity (manifest line 7).

FILE 4: src/loop.metta (2 edits, hook checklist run, artifact_1 same commit)
  Edit L1 (Phase 4.5, line 166): ($sexpr_gated (apply-corner-gate
    $sexpr_verdict)) becomes ($sexpr_gated (apply-corner-gate-v2
    $sexpr_verdict $msgnew)). $msgnew is in scope (bound line 74; &prevmsg
    overwritten line 75, so no state-side recomputation exists; passing the
    binding is the only clean path). Single named call, no inline logic.
  Edit L2 (Phase 4.5 cycle tail, after line 176): one hook line
    ($_ (populate-corner-window! $metta_cmds $k)) after
    populate-coupling-verdict. Record-after-verdict ordering: the gate
    filters against the PRIOR cycle's record, which is the correct meaning
    of "commands that already produced no outcome."
  NOT touched: line 168 (gate-aware-results keeps its name and arity 1; the
  body swap in Edit 1B makes the call sites correct without a loop edit;
  the earlier arity-3 proposal was retracted as unnecessary).
  PRE-CHECK REQUIRED before apply: grep -n "metta_cmds" src/loop.metta must
  show the $metta_cmds binding (expected ~line 140). If the binding name
  differs, STOP and re-anchor; the dry-run cannot catch a wrong variable
  name inside an inserted line.

FILE 5: docs/design/artifact_1_loop_metta_wiring_diagram.md (1 edit)
  Appended Phase 4.5 addendum documenting L1 and L2 and the import changes
  (Discipline 4, same commit).

Net change (computed and checked per file at runtime)
-----------------------------------------------------
- corner_gate.metta: 1A +5, 1B +4, 1C +37 tail lines (delta +46)
- corner_window_writers.metta: created, 36 lines
- lib_clarity_reasoning.metta: +4 (two imports, two comments)
- loop.metta: L1 +0 (in-place), L2 +1
- artifact_1: appended block (delta computed from the block)
- Paren delta: 0 for every .metta file (verified by code-aware count)

Usage
-----
Dry-run (default):  python3 staging/apply_corner_gate_v2_monolith.py
Apply:              python3 staging/apply_corner_gate_v2_monolith.py --apply
Reverse:            python3 staging/apply_corner_gate_v2_monolith.py --reverse --apply

Pre-conditions
--------------
- Mothball state on disk in corner_gate.metta (commit 3cf608f)
- gate-aware-results original body on disk (T1 grep, lines 86-88)
- coupling_quantale_merge.metta on disk in soul/corner_gap/ (89 lines)
- Container rebuild possible after apply (manifest is baked; hotspot
  workaround for the network trap)

Supersession note
-----------------
This script supersedes the standalone staging/apply_fix_a_results_filter.py
(its Edit is folded in as 1B/1C). Do NOT run that script; if placed, it
stays unused.

Backup files (forward apply only)
---------------------------------
- soul/corner_gap/corner_gate.metta.bak.v2_monolith
- lib_clarity_reasoning/lib_clarity_reasoning.metta.bak.v2_monolith
- src/loop.metta.bak.v2_monolith
- docs/design/artifact_1_loop_metta_wiring_diagram.md.bak.v2_monolith
"""
from __future__ import annotations

import argparse
import sys
from pathlib import Path

# ============================================================================
# FILE PATHS
# ============================================================================

GATE_PATH = Path("soul/corner_gap/corner_gate.metta")
GATE_BAK = Path("soul/corner_gap/corner_gate.metta.bak.v2_monolith")

WW_PATH = Path("soul/corner_gap/corner_window_writers.metta")

LIB_PATH = Path("lib_clarity_reasoning/lib_clarity_reasoning.metta")
LIB_BAK = Path("lib_clarity_reasoning/lib_clarity_reasoning.metta.bak.v2_monolith")

LOOP_PATH = Path("src/loop.metta")
LOOP_BAK = Path("src/loop.metta.bak.v2_monolith")

ART1_PATH = Path("docs/design/artifact_1_loop_metta_wiring_diagram.md")
ART1_BAK = Path("docs/design/artifact_1_loop_metta_wiring_diagram.md.bak.v2_monolith")

MARKER = "V2-MONOLITH 2026-07-06"

# ============================================================================
# EDIT 1A: apply-corner-gate mothball -> apply-corner-gate-v2 (probe B6)
# ============================================================================

E1A_OLD = (
    ";; MOTHBALLED 2026-07-06 (interim until v2 lands): enforcement off, detectors keep observing.\n"
    ";; Original body: (if (== (corner-confirmed) True) () $sexpr)\n"
    "(= (apply-corner-gate $sexpr) $sexpr)"
)
E1A_NEW = (
    ";; V2-MONOLITH 2026-07-06: mothball superseded by apply-corner-gate-v2 (probes B1-B6).\n"
    ";; Pattern-scoped: only exact repeats recorded in the confirmed-corner window are\n"
    ";; held; novel commands pass and execute, so forward-outcome is observable and the\n"
    ";; gate releases on evidence (probe B3). Person windows are never gated (probe B6).\n"
    "(= (apply-corner-gate-v2 $sexpr $msgnew)\n"
    "   (if (== $msgnew True)\n"
    "       $sexpr\n"
    "       (if (== (corner-confirmed-core) True)\n"
    "           (filter-corner-cmds $sexpr)\n"
    "           $sexpr)))"
)

# ============================================================================
# EDIT 1B: gate-aware-results -> probe-B7 body (name and arity kept)
# ============================================================================

E1B_OLD = (
    "(= (gate-aware-results $exec-results)\n"
    "   (if (== (corner-gate-active) True)\n"
    "       (RESULTS: (corner-gate-feedback))\n"
    "       $exec-results))"
)
E1B_NEW = (
    ";; V2-MONOLITH 2026-07-06: results echo filter (probes B7, P1-P4). Real command\n"
    ";; returns pass verbatim; prose echoes become a mechanical marker; empty batches\n"
    ";; yield a factual non-empty line. Marker text is Clarity's to amend.\n"
    "(= (gate-aware-results $exec-results)\n"
    "   (let (RESULTS: $lst) $exec-results\n"
    "        (if (== $lst ())\n"
    "            (if (== (corner-confirmed-core) True)\n"
    "                (RESULTS: ((COMMAND_RETURN: (held-by-corner-gate))))\n"
    "                (RESULTS: ((COMMAND_RETURN: (no-commands-executed-this-cycle)))))\n"
    "            (RESULTS: (filter-returns $lst)))))"
)

# ============================================================================
# EDIT 1C: appended pure filter functions (probe-proven bodies)
# ============================================================================

E1C_TAIL = (
    "\n"
    ";; ================================================================\n"
    ";; V2-MONOLITH 2026-07-06 pure filter functions. Probe-proven:\n"
    ";; filter fixtures P1-P4 (empty, real, prose, bare symbol) and\n"
    ";; battery B5/B6 (repr store-and-match, keep-order filtering).\n"
    ";; Maintenance: new skills must be added to allowed-heads or their\n"
    ";; returns get markered (fail-safe information loss, never poison).\n"
    ";; Single-head recursion, if-dispatch on () (P3 fork precedent),\n"
    ";; C12-safe (matches live in their own readers).\n"
    ";; ================================================================\n"
    "(= (allowed-heads)\n"
    "   (send metta shell read-file write-file append-file query remember\n"
    "    pin promote demote tavily-search technical-analysis agentverse progn))\n"
    "\n"
    "(= (head-in-list? $x $lst)\n"
    "   (if (== $lst ())\n"
    "       False\n"
    "       (let* (($h (car-atom $lst))\n"
    "              ($t (cdr-atom $lst)))\n"
    "             (if (== $h $x) True (head-in-list? $x $t)))))\n"
    "\n"
    "(= (real-return? $el)\n"
    "   (let (COMMAND_RETURN: ($s $r)) $el\n"
    "        (head-in-list? (car-atom $s) (allowed-heads))))\n"
    "\n"
    "(= (filter-returns $lst)\n"
    "   (if (== $lst ())\n"
    "       ()\n"
    "       (let* (($h (car-atom $lst))\n"
    "              ($t (filter-returns (cdr-atom $lst))))\n"
    "             (if (== (real-return? $h) True)\n"
    "                 (cons-atom $h $t)\n"
    "                 (cons-atom (COMMAND_RETURN: (non-command-element not-executed)) $t)))))\n"
    "\n"
    "(= (cmd-in-corner-window? $cmd)\n"
    "   (let $r (repr $cmd)\n"
    "        (> (size-atom (collapse (match &self (corner-window-cmd $c $r) $c))) 0)))\n"
    "\n"
    "(= (filter-corner-cmds $cmds)\n"
    "   (if (== $cmds ())\n"
    "       ()\n"
    "       (let* (($h (car-atom $cmds))\n"
    "              ($t (filter-corner-cmds (cdr-atom $cmds))))\n"
    "             (if (== (cmd-in-corner-window? $h) True)\n"
    "                 $t\n"
    "                 (cons-atom $h $t)))))\n"
)

# ============================================================================
# FILE 2: corner_window_writers.metta (created forward, deleted reverse)
# ============================================================================

WW_CONTENT = (
    ";; corner_window_writers.metta -- confirmed-corner command record (writers)\n"
    ";; V2-MONOLITH 2026-07-06. Discipline 6A: pure readers (cmd-in-corner-window?,\n"
    ";; filter-corner-cmds) live in corner_gate.metta; writers live here.\n"
    ";; Record is CONFIRMATION-SCOPED and EPHEMERAL: written while the graded\n"
    ";; corner is confirmed, cleared on any non-confirmed cycle. Never persistent,\n"
    ";; never a disposition surface (design v1.3 SSI correction).\n"
    ";; Probe evidence: record body B5/B6; clear per ADR-005 superpose iteration;\n"
    ";; the populate driver is if-dispatch composition of the probed parts.\n"
    "\n"
    "(= (do-clear-corner-window!)\n"
    "   (let $olds (collapse (match &self (corner-window-cmd $c $r) (corner-window-cmd $c $r)))\n"
    "        (let $o (superpose $olds)\n"
    "             (if (== $o ())\n"
    "                 ()\n"
    "                 (remove-atom &self $o)))))\n"
    "\n"
    "(= (do-record-corner-window! $cmds $cycle-id)\n"
    "   (let $c (superpose $cmds)\n"
    "        (if (== $c ())\n"
    "            ()\n"
    "            (let $r (repr $c)\n"
    "                 (add-atom &self (corner-window-cmd $cycle-id $r))))))\n"
    "\n"
    ";; Cycle driver. Hook ordering: AFTER populate-coupling-verdict (loop line 176),\n"
    ";; so the gate always filters against the PRIOR cycle's record.\n"
    "(= (populate-corner-window! $cmds $cycle-id)\n"
    "   (if (== (corner-confirmed-core) True)\n"
    "       (do-record-corner-window! $cmds $cycle-id)\n"
    "       (do-clear-corner-window!)))\n"
)

# ============================================================================
# FILE 3: manifest imports
# ============================================================================

LIB_OLD = "!(import! &self (library omegaclaw ./soul/corner_gap/corner_gate))"
LIB_NEW = (
    ";; V2-MONOLITH 2026-07-06: graded corner detection (quantale merge, probe A/B1-B4)\n"
    "!(import! &self (library omegaclaw ./soul/corner_gap/coupling_quantale_merge))\n"
    "!(import! &self (library omegaclaw ./soul/corner_gap/corner_gate))\n"
    ";; V2-MONOLITH 2026-07-06: confirmed-corner window record (writers, probe B5/B6)\n"
    "!(import! &self (library omegaclaw ./soul/corner_gap/corner_window_writers))"
)

# ============================================================================
# FILE 4: loop.metta hooks
# ============================================================================

L1_OLD = "                                       ($sexpr_gated (apply-corner-gate $sexpr_verdict))"
L1_NEW = "                                       ($sexpr_gated (apply-corner-gate-v2 $sexpr_verdict $msgnew))"

L2_OLD = "                                       ($_ (populate-coupling-verdict $k))"
L2_NEW = (
    "                                       ($_ (populate-coupling-verdict $k))\n"
    "                                       ($_ (populate-corner-window! $metta_cmds $k))"
)

# ============================================================================
# FILE 5: artifact_1 addendum
# ============================================================================

ART1_BLOCK = (
    "\n"
    "### Addendum (2026-07-06, V2-MONOLITH): corner-gate v2 wiring\n"
    "\n"
    "Phase 4.5 changes. Line 166: the gate call is now (apply-corner-gate-v2\n"
    "$sexpr_verdict $msgnew); pattern-scoped filtering with person-window\n"
    "exemption, firing on corner-confirmed-core (graded quantale verdict from\n"
    "coupling_quantale_merge, now imported). Line 168 unchanged in the loop:\n"
    "gate-aware-results kept its name and arity, its body (in corner_gate.metta)\n"
    "is now the results echo filter (real command returns pass, prose echoes\n"
    "become mechanical markers, empty batches yield factual non-empty lines).\n"
    "Cycle tail: one new hook after populate-coupling-verdict,\n"
    "(populate-corner-window! $metta_cmds $k), recording proposed command reprs\n"
    "while the graded corner is confirmed and clearing otherwise, so the gate\n"
    "filters against the prior cycle's record. Manifest gains\n"
    "coupling_quantale_merge and corner_window_writers imports in the corner_gap\n"
    "block. The v1 boolean detector writers keep running unchanged as\n"
    "observability. Probe evidence in project knowledge (battery B1-B7).\n"
)

# ============================================================================
# ENGINE
# ============================================================================


def code_aware_paren_count(text: str) -> tuple[int, int]:
    opens = closes = 0
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


def count_block(text: str, block: str) -> int:
    count = 0
    start = 0
    while True:
        idx = text.find(block, start)
        if idx == -1:
            break
        count += 1
        start = idx + 1
    return count


def replace_once(content: str, old: str, new: str, label: str) -> str:
    c = count_block(content, old)
    if c != 1:
        raise RuntimeError(f"{label}: expected exactly 1 occurrence of anchor, found {c}. "
                           f"Paste the file so anchors can be re-grounded.")
    return content.replace(old, new, 1)


def diff_preview(old: str, new: str, label: str, context: int = 2) -> str:
    ol, nl_ = old.splitlines(), new.splitlines()
    out = [f"--- diff preview: {label} ---"]
    i = j = 0
    hunks = 0
    while i < len(ol) and j < len(nl_):
        if ol[i] == nl_[j]:
            i += 1
            j += 1
            continue
        hunks += 1
        for k in range(max(0, i - context), i):
            out.append(f"  {ol[k]}")
        oi = i
        while oi < len(ol) and ol[oi] not in nl_[j:j + 12]:
            out.append(f"- {ol[oi]}")
            oi += 1
        nj = j
        while nj < len(nl_) and (oi >= len(ol) or nl_[nj] != ol[oi]):
            out.append(f"+ {nl_[nj]}")
            nj += 1
        for k in range(oi, min(len(ol), oi + context)):
            out.append(f"  {ol[k]}")
        i, j = oi, nj
        if hunks >= 6:
            out.append("  (further hunks exist; inspect file after apply)")
            break
    if j < len(nl_) and i >= len(ol):
        for k in range(j, len(nl_)):
            out.append(f"+ {nl_[k]}")
    return "\n".join(out)


class FileEdit:
    def __init__(self, path, bak, label, fwd_fn, rev_fn,
                 fwd_state_fn, rev_state_fn, check_parens):
        self.path, self.bak, self.label = path, bak, label
        self.fwd_fn, self.rev_fn = fwd_fn, rev_fn
        self.fwd_state_fn, self.rev_state_fn = fwd_state_fn, rev_state_fn
        self.check_parens = check_parens
        self.orig = None
        self.sim = None


def gate_fwd(c):
    c = replace_once(c, E1A_OLD, E1A_NEW, "Edit 1A")
    c = replace_once(c, E1B_OLD, E1B_NEW, "Edit 1B")
    if not c.endswith("\n"):
        c += "\n"
    return c + E1C_TAIL


def gate_rev(c):
    c = replace_once(c, E1A_NEW, E1A_OLD, "Edit 1A reverse")
    c = replace_once(c, E1B_NEW, E1B_OLD, "Edit 1B reverse")
    return replace_once(c, E1C_TAIL, "", "Edit 1C reverse")


def gate_fwd_ok(c):
    ok = (count_block(c, E1A_OLD) == 1 and count_block(c, E1B_OLD) == 1
          and MARKER not in c)
    return ok, f"mothball+original present, marker absent -> {'OK' if ok else 'FAIL'}"


def gate_rev_ok(c):
    ok = (count_block(c, E1A_NEW) == 1 and count_block(c, E1B_NEW) == 1
          and count_block(c, E1C_TAIL) == 1)
    return ok, f"v2 bodies+tail present exactly once -> {'OK' if ok else 'FAIL'}"


def lib_fwd(c):
    return replace_once(c, LIB_OLD + "\n", LIB_NEW + "\n", "Manifest edit")


def lib_rev(c):
    return replace_once(c, LIB_NEW + "\n", LIB_OLD + "\n", "Manifest reverse")


def lib_fwd_ok(c):
    ok = (count_block(c, LIB_OLD) == 1 and "coupling_quantale_merge" not in c
          and "corner_window_writers" not in c)
    return ok, f"corner_gate import sole, v2 imports absent -> {'OK' if ok else 'FAIL'}"


def lib_rev_ok(c):
    ok = count_block(c, LIB_NEW) == 1
    return ok, f"v2 import block present exactly once -> {'OK' if ok else 'FAIL'}"


def loop_fwd(c):
    c = replace_once(c, L1_OLD + "\n", L1_NEW + "\n", "Edit L1")
    return replace_once(c, L2_OLD + "\n", L2_NEW + "\n", "Edit L2")


def loop_rev(c):
    c = replace_once(c, L1_NEW + "\n", L1_OLD + "\n", "Edit L1 reverse")
    return replace_once(c, L2_NEW + "\n", L2_OLD + "\n", "Edit L2 reverse")


def loop_fwd_ok(c):
    ok = (count_block(c, L1_OLD) == 1 and count_block(c, L2_OLD) == 1
          and "apply-corner-gate-v2" not in c and "populate-corner-window!" not in c)
    return ok, f"anchors present, v2 calls absent -> {'OK' if ok else 'FAIL'}"


def loop_rev_ok(c):
    ok = count_block(c, L1_NEW) == 1 and count_block(c, L2_NEW) == 1
    return ok, f"v2 hook lines present exactly once -> {'OK' if ok else 'FAIL'}"


def art1_fwd(c):
    if ART1_BLOCK in c:
        raise RuntimeError("artifact_1: addendum already present.")
    return c + ART1_BLOCK


def art1_rev(c):
    return replace_once(c, ART1_BLOCK, "", "artifact_1 reverse")


def art1_fwd_ok(c):
    ok = "V2-MONOLITH): corner-gate v2 wiring" not in c
    return ok, f"addendum absent -> {'OK' if ok else 'FAIL'}"


def art1_rev_ok(c):
    ok = count_block(c, ART1_BLOCK) == 1
    return ok, f"addendum present exactly once -> {'OK' if ok else 'FAIL'}"


def main() -> int:
    parser = argparse.ArgumentParser(description="Corner-gate v2 monolithic repair")
    parser.add_argument("--apply", action="store_true",
                        help="Actually write changes. Default is dry-run.")
    parser.add_argument("--reverse", action="store_true",
                        help="Reverse all edits. Combine with --apply to write.")
    args = parser.parse_args()

    direction = "REVERSE" if args.reverse else "APPLY"
    print(f"\n========== CORNER-GATE V2 MONOLITH: {direction} ==========")

    edits = [
        FileEdit(GATE_PATH, GATE_BAK, "corner_gate.metta", gate_fwd, gate_rev,
                 gate_fwd_ok, gate_rev_ok, True),
        FileEdit(LIB_PATH, LIB_BAK, "lib_clarity_reasoning.metta", lib_fwd, lib_rev,
                 lib_fwd_ok, lib_rev_ok, True),
        FileEdit(LOOP_PATH, LOOP_BAK, "loop.metta", loop_fwd, loop_rev,
                 loop_fwd_ok, loop_rev_ok, True),
        FileEdit(ART1_PATH, ART1_BAK, "artifact_1.md", art1_fwd, art1_rev,
                 art1_fwd_ok, art1_rev_ok, False),
    ]

    for e in edits:
        if not e.path.exists():
            print(f"ERROR: {e.path} not found. Run from repo root.")
            return 1

    # New-file state check
    if args.reverse:
        if not WW_PATH.exists():
            print(f"ERROR reverse: {WW_PATH} not found (expected to delete it).")
            return 1
    else:
        if WW_PATH.exists():
            print(f"ERROR forward: {WW_PATH} already exists.")
            return 1

    print("\n========== PRE-EDIT CHECKS ==========")
    for e in edits:
        e.orig = e.path.read_text()
        if e.check_parens:
            o, c = code_aware_paren_count(e.orig)
            st = "OK" if o == c else "FAIL"
            print(f"  {e.label} paren pre: opens={o} closes={c} ({st})")
            if o != c:
                print("Aborting: unbalanced file pre-edit.")
                return 1
        ok, msg = (e.rev_state_fn if args.reverse else e.fwd_state_fn)(e.orig)
        print(f"  {e.label} state: {msg}")
        if not ok:
            print("\nPre-check failed. Aborting; no disk write.")
            return 1

    print("\n========== SIMULATION ==========")
    for e in edits:
        try:
            e.sim = (e.rev_fn if args.reverse else e.fwd_fn)(e.orig)
        except RuntimeError as exc:
            print(f"  {e.label} simulation FAILED: {exc}")
            return 1
        if e.check_parens:
            o, c = code_aware_paren_count(e.sim)
            st = "OK" if o == c else "FAIL"
            print(f"  {e.label} paren post: opens={o} closes={c} ({st})")
            if o != c:
                print("Aborting; no disk write.")
                return 1
        delta = len(e.sim.splitlines()) - len(e.orig.splitlines())
        print(f"  {e.label} line delta: {delta:+d}")
        ok, msg = (e.fwd_state_fn if args.reverse else e.rev_state_fn)(e.sim)
        print(f"  {e.label} simulated end state: {msg}")
        if not ok:
            print("Aborting; no disk write.")
            return 1

    # Window writers file simulation
    if not args.reverse:
        o, c = code_aware_paren_count(WW_CONTENT)
        st = "OK" if o == c else "FAIL"
        print(f"  corner_window_writers.metta (new): {len(WW_CONTENT.splitlines())} "
              f"lines, paren opens={o} closes={c} ({st})")
        if o != c:
            print("Aborting; no disk write.")
            return 1

    print("\n========== DIFF PREVIEWS ==========")
    for e in edits:
        print(diff_preview(e.orig, e.sim, e.label))
        print()
    if not args.reverse:
        print(f"--- new file: {WW_PATH} ({len(WW_CONTENT.splitlines())} lines, "
              f"full content in this script's WW_CONTENT) ---")
    else:
        print(f"--- file to DELETE: {WW_PATH} ---")

    if not args.apply:
        print("\n========== DRY-RUN COMPLETE ==========")
        print("All checks pass. Re-run with --apply to write.")
        return 0

    if not args.reverse:
        for e in edits:
            if e.bak.exists():
                print(f"WARNING: backup {e.bak} exists; overwriting.")
            e.bak.write_text(e.orig)
            print(f"Backup written: {e.bak}")

    print("\n========== WRITING ==========")
    for e in edits:
        e.path.write_text(e.sim)
        print(f"Wrote: {e.path}")
    if args.reverse:
        WW_PATH.unlink()
        print(f"Deleted: {WW_PATH}")
    else:
        WW_PATH.write_text(WW_CONTENT)
        print(f"Created: {WW_PATH}")

    print("\n========== DISK VERIFICATION ==========")
    all_ok = True
    for e in edits:
        disk = e.path.read_text()
        if e.check_parens:
            o, c = code_aware_paren_count(disk)
            if o != c:
                print(f"  {e.label} disk paren FAIL")
                all_ok = False
                continue
        ok, msg = (e.fwd_state_fn if args.reverse else e.rev_state_fn)(disk)
        print(f"  {e.label} disk state: {msg}")
        all_ok = all_ok and ok
    ww_ok = WW_PATH.exists() != args.reverse
    print(f"  corner_window_writers.metta {'present' if WW_PATH.exists() else 'absent'} "
          f"-> {'OK' if ww_ok else 'FAIL'}")
    all_ok = all_ok and ww_ok

    if not all_ok:
        print("\nDISK VERIFICATION FAILED. Restore:")
        for e in edits:
            print(f"  cp {e.bak} {e.path}")
        print(f"  rm -f {WW_PATH}")
        return 1

    print("\n========== V2 MONOLITH COMPLETE ==========")
    print("All edits applied. All checks pass.")
    if not args.reverse:
        print("\nNext: commit, then rebuild (manifest is baked; hotspot for the")
        print("network trap), then restart, then natural-operation verification:")
        print("  docker compose build --no-cache clarityclaw && docker compose up -d")
        print("  docker logs clarity_omega 2>&1 | grep -E 'iteration|Syntax error|ERROR' | head")
        print("  docker logs clarity_omega 2>&1 | grep 'RESULTS-CONTENT' | tail -3")
    return 0


if __name__ == "__main__":
    sys.exit(main())
