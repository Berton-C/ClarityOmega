#!/usr/bin/env python3
"""
Apply script: SOUL_UTILS LEGACY GATE RETIREMENT (Repair 1 root cause).
Namespace census 2026-06-10: soul_utils.metta Block 1 holds the legacy
string-based gate stubs (soul-is-metta-cmd? hardwired False, string-
contains-based namespace and lock checks, println side effects). They
collide with the committed native gate (soul_mutation_gate_corrected
.metta): both clause sets load, every gate predicate goes nondet in
production (P3 fork: false/true/true), and the string-based clause
bodies die on unbound variables (split_string/atom_string) -- the
2026-06-10 production crash.

Forward: replace the block with a retirement marker. The native gate
file becomes the single definition site for all six names.
Reverse: restore the block byte-identically.

Usage (repo root):
  Dry:     python3 staging/apply_soul_utils_gate_retirement.py
  Apply:   python3 staging/apply_soul_utils_gate_retirement.py --apply
  Reverse: python3 staging/apply_soul_utils_gate_retirement.py --reverse --apply
soul/ is bind-mounted; the standing rule still applies: rebuild
--no-cache before trusting any result. Backup: soul_utils.metta.bak.gateretire
Log: shared_files/gate_retirement_<mode>_<UTCstamp>.log
"""
from __future__ import annotations

import argparse
import datetime
import sys
from pathlib import Path

_STAMP = datetime.datetime.utcnow().strftime("%Y%m%d_%H%M%S")
LOG_DIR = Path("shared_files")
TARGET = Path("soul/soul_utils.metta")


class _Tee:
    def __init__(self, stream, logfile):
        self.stream, self.logfile = stream, logfile

    def write(self, d):
        self.stream.write(d)
        self.logfile.write(d)

    def flush(self):
        self.stream.flush()
        self.logfile.flush()


OLD_BLOCK = """;; ============================================================
;; Block 1: metta() Gate Detection Functions
;; ============================================================

;; soul-is-metta-cmd?: True if command is a metta() invocation
(= (soul-is-metta-cmd? $cmd) False)

;; soul-any-metta?: True if any command in list is a metta() call
(= (soul-any-metta? $cmds)
   (any (collapse (let $c (superpose $cmds) (progn (println! (SOUL-ANY-METTA-ITEM: $c)) (soul-is-metta-cmd? $c))))))

;; soul-extract-metta-arg: extracts the argument from a metta() command
(= (soul-extract-metta-arg (metta $arg)) $arg)

;; soul-metta-targets-soul-namespace?: True if metta() string targets soul atoms
(= (soul-metta-targets-soul-namespace? $cmd_str)
   (any (collapse (superpose (
     (string-contains $cmd_str "add-atom &self (soul-")
     (string-contains $cmd_str "add-atom &self (priority")
     (string-contains $cmd_str "add-atom &self (irreversible")
     (string-contains $cmd_str "add-atom &self (tension"))))))

;; soul-mutation-pending?: True if mutation lock is held
;; Uses string-contains on the lock state -- returns bare True/False
(= (soul-mutation-pending?)
   (string-contains (get-state &soul_mutation_lock) "LOCKED:"))"""

NEW_BLOCK = """;; ============================================================
;; Block 1: RETIRED 2026-06-10 (namespace census, Repair 1 root cause).
;; The legacy string-based gate stubs that lived here collided with the
;; committed native gate (soul_mutation_gate_corrected.metta): both
;; clause sets loaded, making every gate predicate nondeterministic in
;; production (P3 probe fork), and the string-based clause bodies died
;; on unbound variables (split_string) -- the 2026-06-10 crash. The
;; native gate file is now the single definition site for:
;;   soul-is-metta-cmd?  soul-any-metta?  soul-extract-metta-arg
;;   soul-metta-targets-soul-namespace?  soul-mutation-pending?
;; ============================================================"""


def code_aware_paren_count(text: str):
    opens = closes = 0
    in_string = False
    escape = False
    i, n = 0, len(text)
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


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--apply", action="store_true")
    ap.add_argument("--reverse", action="store_true")
    args = ap.parse_args()
    mode = ("reverse" if args.reverse else "forward") + ("_apply" if args.apply else "_dryrun")
    LOG_DIR.mkdir(parents=True, exist_ok=True)
    logf = open(LOG_DIR / f"gate_retirement_{mode}_{_STAMP}.log", "w")
    sys.stdout = _Tee(sys.__stdout__, logf)

    print(f"\n========== SOUL_UTILS GATE RETIREMENT: {mode.upper()} ==========")
    if not TARGET.exists():
        print(f"  ERROR: {TARGET} not found. Run from repo root.")
        return 1
    content = TARGET.read_text()
    pre_lines = len(content.splitlines())
    o, c = code_aware_paren_count(content)
    print(f"  Pre: {pre_lines} lines; parens {o}/{c} delta={o-c} ({'OK' if o == c else 'FAIL'})")
    if o != c:
        return 1

    old, new = (NEW_BLOCK, OLD_BLOCK) if args.reverse else (OLD_BLOCK, NEW_BLOCK)
    n_found = content.count(old)
    if n_found != 1:
        print(f"  STATE CHECK FAILED: anchor block found {n_found} times (need exactly 1).")
        print("  The on-disk block text differs from the expected verbatim text.")
        return 1
    sim = content.replace(old, new, 1)
    so, sc = code_aware_paren_count(sim)
    post_lines = len(sim.splitlines())
    print(f"  Post: {post_lines} lines (delta {post_lines - pre_lines}); parens {so}/{sc} delta={so-sc} ({'OK' if so == sc else 'FAIL'})")
    if so != sc:
        return 1

    if not args.apply:
        print("\n========== ACTION-SUMMARY (DRY-RUN) ==========")
        print("  Simulated clean. No writes. Re-run with --apply to write.")
        return 0

    if not args.reverse:
        bak = Path(str(TARGET) + ".bak.gateretire")
        bak.write_text(content)
        print(f"Backup written: {bak}")
    TARGET.write_text(sim)
    print(f"Wrote: {TARGET}")

    d = TARGET.read_text()
    vo, vc = code_aware_paren_count(d)
    marker_ok = ("RETIRED 2026-06-10" in d) != args.reverse
    legacy_ok = ("string-contains $cmd_str" in d) == args.reverse
    print(f"\n========== DISK VERIFICATION ==========")
    print(f"  parens {vo}/{vc} ({'OK' if vo == vc else 'FAIL'}); marker {'OK' if marker_ok else 'FAIL'}; legacy-clauses {'absent OK' if legacy_ok else 'FAIL'}")
    if vo != vc or not marker_ok or not legacy_ok:
        print("  RESTORE FROM .bak.gateretire")
        return 1
    print("\n========== ACTION-SUMMARY ==========")
    print(f"  Direction: {'REVERSE' if args.reverse else 'FORWARD'}. Block "
          f"{'restored' if args.reverse else 'retired'}; verified.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
