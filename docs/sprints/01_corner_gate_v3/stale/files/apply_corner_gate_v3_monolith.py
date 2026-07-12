#!/usr/bin/env python3
"""
apply_corner_gate_v3_monolith.py

Corner-Gate v3 monolithic apply/reverse. Design canon:
corner_gate_v3_adapter_design.md (v0.6 line, Sections 5.1-5.5).
Payloads: Draft A.3, RATIFIED 2026-07-10, hashes FROZEN below.

Behavior contract (ratified): --dry-run by default; --apply explicit;
--reverse supported; backs up every touched file; anchor-verified edits;
paren-delta check; import-order check; no-duplicate-engine-heads check;
lib_quantale non-resurrection check; payload hash verification; S1 seam
preflight (REFUSES to apply if not green) and postflight (auto-reverse on
failure); tree delta report; no-touch assertions; apply manifest.

Implementation is monolithic, validation is staged (the separate
validate_corner_gate_v3_monolith.py runs D0-D8), rollback is complete.
The script either completes or leaves the tree unchanged except backups
and the manifest.

USAGE:
  python3 staging/apply_corner_gate_v3_monolith.py --dry-run
  python3 staging/apply_corner_gate_v3_monolith.py --apply
  python3 staging/apply_corner_gate_v3_monolith.py --reverse --apply
Options: --repo-root . --payload-dir docs/sprints/01_corner_gate_v3
"""
import argparse
import hashlib
import json
import os
import shutil
import sys

# ---------------- FROZEN A.3 PAYLOAD IDENTITY (ratified 2026-07-10) --------
FROZEN = {
    "coupling_legibility.metta":
        "14705a549aec69198b9d03dd31ea162dd95ad8fd238c5fea3e99eb8712bf10f1",
    "coupling_legibility_writers.metta":
        "e1bc3e28cd7ca357f7e618713cb550dd328fb0da5d114f40e6981e4b7efca3f8",
    "coupling_legibility_helper_payload.py":
        "de3183e1f3504e2201d6ef80ec6e6650534b80d491e4df7efa38a099f1e87e54",
}
ENGINE_REL = ("lib_clarity_reasoning/lib_quantale_autopoietic_epistemic_"
              "dynamics_engine_v08_7_2_SOUL_EVOLUTIONARY_CANONICAL_TOPOLOGY.metta")
MANIFEST_REL = "lib_clarity_reasoning/lib_clarity_reasoning.metta"
LOOP_REL = "src/loop.metta"
HELPER_REL = "src/helper.py"
GATE_REL = "soul/corner_gap/corner_gate.metta"
CWW_REL = "soul/corner_gap/corner_window_writers.metta"
ART1_REL = "docs/design/artifact_1_loop_metta_wiring_diagram.md"
PURE_DST = "soul/coupling_legibility.metta"
WRITERS_DST = "soul/coupling_legibility_writers.metta"
BAK = ".bak.v3_monolith"
MARK_B = ";; V3-MONOLITH BEGIN coupling_legibility imports"
MARK_E = ";; V3-MONOLITH END coupling_legibility imports"
PY_MARK_B = "# V3-MONOLITH BEGIN coupling_legibility helper payload"
PY_MARK_E = "# V3-MONOLITH END coupling_legibility helper payload"
ART_MARK_B = "<!-- V3-MONOLITH BEGIN -->"
ART_MARK_E = "<!-- V3-MONOLITH END -->"

MERGE_IMPORT = "!(import! &self (library omegaclaw ./soul/corner_gap/coupling_quantale_merge))"
CWW_IMPORT = "!(import! &self (library omegaclaw ./soul/corner_gap/corner_window_writers))"
GATE_IMPORT_SUB = "./soul/corner_gap/corner_gate)"
ENGINE_IMPORT_SUB = "lib_quantale_autopoietic_epistemic_dynamics_engine_v08_7_2"
LIBQ_IMPORT = "!(import! &self (library omegaclaw ./lib_clarity_reasoning/lib_quantale))"
NEW_IMPORTS = (MARK_B + "\n"
               "!(import! &self (library omegaclaw ./soul/coupling_legibility))\n"
               "!(import! &self (library omegaclaw ./soul/coupling_legibility_writers))\n"
               + MARK_E)

HOOK_OLD_SUB = "($_ (populate-corner-window! $metta_cmds $k))"
HOOK_NEW_SUB = "($_ (do-record-coupling-cycle! $metta_cmds $msgnew $k (get-state &error)))"
BOOT_OLD = "(do-bootstrap-task-state!)"
BOOT_NEW = "(do-bootstrap-coupling!)\n          (do-bootstrap-task-state!)"

GATE_SHIM = """;; ============================================================
;; soul/corner_gap/corner_gate.metta -- CORNER-GATE V3 SHIM
;; Installed by apply_corner_gate_v3_monolith.py. The v2 enforcement body
;; (pattern-scoped holding, filter-corner-cmds, held-marker emission)
;; is RETIRED (design doc 5.1; reasons: enforcement-retired-by-
;; design, defect-D-A, defect-D-B). Names and arities preserved.
;; v3 does not imperatively hold, block, or release. It feeds conditions;
;; the engine computes blockers, candidates, and navigation states.
;; ============================================================

;; Pass-through: nothing is ever held.
(= (apply-corner-gate-v2 $sexpr $msgnew) $sexpr)

;; The legibility seam: appends the coupling line to the RESULTS payload.
;; S1: novelty classification upstream compares raw $results; this touches
;; only the results_final path that feeds &lastresults.
(= (gate-aware-results (RESULTS: $inner))
   (let* (($line (coupling-legibility-line))
          ($el (COUPLING-STATE-LINE $line))
          ($inner2 (cons-atom $el $inner)))
     (RESULTS: $inner2)))
"""


def sha(path):
    with open(path, "rb") as f:
        return hashlib.sha256(f.read()).hexdigest()


def rd(path):
    with open(path, "r") as f:
        return f.read()


def wr(path, text, dry):
    if dry:
        return
    with open(path, "w") as f:
        f.write(text)


REPORT = []
FAILED = False


def say(line):
    REPORT.append(line)
    print(line)


def check(label, ok, detail=""):
    global FAILED
    say(("  PASS  " if ok else "  FAIL  ") + label + (("   " + detail) if detail else ""))
    if not ok:
        FAILED = True
    return ok


def paren_delta(text):
    return text.count("(") - text.count(")")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--apply", action="store_true")
    ap.add_argument("--dry-run", action="store_true", help="default mode; explicit flag accepted")
    ap.add_argument("--reverse", action="store_true")
    ap.add_argument("--repo-root", default=".")
    ap.add_argument("--payload-dir", default="docs/sprints/01_corner_gate_v3")
    args = ap.parse_args()
    dry = not args.apply
    root = os.path.abspath(args.repo_root)
    os.chdir(root)
    mode = "REVERSE" if args.reverse else ("APPLY" if args.apply else "DRY-RUN")
    say("=" * 72)
    say("CORNER-GATE V3 MONOLITH  mode=" + mode + "  root=" + root)
    say("=" * 72)

    if args.reverse:
        return do_reverse(dry and not args.apply)

    # ---------------- PHASE 0: PREFLIGHT ----------------
    say("PHASE 0  PREFLIGHT")
    # payload identity
    for name, want in FROZEN.items():
        p = os.path.join(args.payload_dir, name)
        ok = os.path.exists(p) and sha(p) == want
        check("frozen payload " + name, ok, "" if ok else "missing or hash mismatch (reviewed != applied)")
    # required tree files
    for rel in (MANIFEST_REL, LOOP_REL, HELPER_REL, GATE_REL, CWW_REL, ART1_REL, ENGINE_REL):
        check("tree file present " + rel, os.path.exists(rel))
    if FAILED:
        say(">>> PREFLIGHT FAILED. Nothing touched.")
        sys.exit(3)

    loop = rd(LOOP_REL)
    man = rd(MANIFEST_REL)
    helper = rd(HELPER_REL)
    engine_sha_pre = sha(ENGINE_REL)

    # S1 SEAM PREFLIGHT (Gate S1: refuse to apply unless green)
    say("  -- Gate S1 preflight --")
    check("S1 novelty compares raw results",
          "(helper.safe_results_str (repr $results))" in loop
          and "(repr $results_final)" not in loop.split("$results_novel")[1].split("\n")[0])
    check("S1 results_final computed from gate-aware-results",
          "($results_final (gate-aware-results $results))" in loop)
    check("S1 lastresults updated from results_final",
          "(change-state! &lastresults (py-call (helper.safe_results_str (repr $results_final))))" in loop)
    check("S1 hook ordering: state-delta before corner-window site",
          loop.find("populate-state-delta") < loop.find(HOOK_OLD_SUB))
    # anchors
    check("anchor: hook line unique", loop.count(HOOK_OLD_SUB) == 1)
    check("anchor: bootstrap line unique", loop.count(BOOT_OLD) == 1)
    check("anchor: v2 gate call at seam", "(apply-corner-gate-v2 $sexpr_verdict $msgnew)" in loop)
    check("anchor: merge import unique", man.count(MERGE_IMPORT) == 1)
    check("anchor: corner_window_writers import unique", man.count(CWW_IMPORT) == 1)
    check("anchor: corner_gate import present", man.count(GATE_IMPORT_SUB) >= 1)
    # import-order preconditions
    lines = man.splitlines()
    def line_of(sub):
        for i, l in enumerate(lines, 1):
            if sub in l and l.startswith("!(import!"):
                return i
        return -1
    ln_engine = line_of(ENGINE_IMPORT_SUB)
    ln_merge = line_of("coupling_quantale_merge")
    ln_gate = line_of("./soul/corner_gap/corner_gate")
    check("import order: engine before merge", 0 < ln_engine < ln_merge,
          "engine=%d merge=%d" % (ln_engine, ln_merge))
    check("import order: merge before corner_gate (shim dependency window exists)",
          ln_merge < ln_gate, "merge=%d gate=%d" % (ln_merge, ln_gate))
    check("prereq imports before insertion point (task_state, state_delta_writer)",
          0 < line_of("task_state)") < ln_merge and 0 < line_of("state_delta_writer)") < ln_merge)
    check("lib_quantale not imported (retirement holds)", LIBQ_IMPORT not in man)
    check("not already applied", MARK_B not in man and PY_MARK_B not in helper)
    # no duplicate engine heads in payloads
    for name in ("coupling_legibility.metta", "coupling_legibility_writers.metta"):
        t = rd(os.path.join(args.payload_dir, name))
        check("no engine q- heads defined in " + name, "\n(= (q-" not in t and not t.startswith("(= (q-"))
        check("paren delta 0 in " + name, paren_delta(t) == 0)
    check("engine file is never a target (no-touch)", True, "recorded sha " + engine_sha_pre[:12])
    if FAILED:
        say(">>> GATE S1 / PREFLIGHT NOT GREEN. REFUSING TO APPLY. Nothing touched.")
        sys.exit(3)

    # ---------------- TREE DELTA REPORT ----------------
    say("TREE DELTA (what will change):")
    for d in ("CREATE " + PURE_DST,
              "CREATE " + WRITERS_DST,
              "PATCH  " + HELPER_REL + " (append marked helper payload)",
              "PATCH  " + MANIFEST_REL + " (insert 2 imports after merge import; remove corner_window_writers import)",
              "PATCH  " + LOOP_REL + " (bootstrap hook insert; corner-window hook -> do-record-coupling-cycle!)",
              "REPLACE " + GATE_REL + " (v3 shim: apply-corner-gate-v2 pass-through; gate-aware-results line appender)",
              "RETIRE " + CWW_REL + " (moved to .retired.v3)",
              "UPDATE " + ART1_REL + " (append marked v3 section)"):
        say("  " + d)
    say("NO-TOUCH ASSERTIONS: v08.7.2 engine unmodified; lib_quantale not re-imported;")
    say("  NACE not updated; Capability Registry dispatch untouched; no durable canon;")
    say("  coupling window not persisted across restart.")
    if dry:
        say(">>> DRY-RUN COMPLETE. Preflight green. Re-run with --apply.")
        return

    # ---------------- BACKUPS ----------------
    pre_hashes = {}
    for rel in (MANIFEST_REL, LOOP_REL, HELPER_REL, GATE_REL, CWW_REL, ART1_REL):
        pre_hashes[rel] = sha(rel)
        shutil.copy2(rel, rel + BAK)
    say("PHASE 0  backups written (" + BAK + ")")

    # ---------------- PHASES 1-2: CREATE SOUL FILES ----------------
    shutil.copy2(os.path.join(args.payload_dir, "coupling_legibility.metta"), PURE_DST)
    shutil.copy2(os.path.join(args.payload_dir, "coupling_legibility_writers.metta"), WRITERS_DST)
    say("PHASE 1-2  soul files created")

    # ---------------- PHASE 3: HELPER APPEND ----------------
    payload_py = rd(os.path.join(args.payload_dir, "coupling_legibility_helper_payload.py"))
    wr(HELPER_REL, helper.rstrip("\n") + "\n\n" + PY_MARK_B + "\n" + payload_py.rstrip("\n") + "\n" + PY_MARK_E + "\n", False)
    say("PHASE 3  helper payload appended (marked)")

    # ---------------- PHASE 4: MANIFEST IMPORTS ----------------
    man2 = man.replace(MERGE_IMPORT, MERGE_IMPORT + "\n" + NEW_IMPORTS, 1)
    man2 = man2.replace(CWW_IMPORT + "\n", "", 1).replace(CWW_IMPORT, "", 1)
    wr(MANIFEST_REL, man2, False)
    say("PHASE 4+6a  imports inserted after merge; corner_window_writers import removed")

    # ---------------- PHASE 5: LOOP SEAM ----------------
    loop2 = loop.replace(BOOT_OLD, BOOT_NEW, 1)
    loop2 = loop2.replace(HOOK_OLD_SUB, HOOK_NEW_SUB, 1)
    wr(LOOP_REL, loop2, False)
    wr(GATE_REL, GATE_SHIM, False)
    say("PHASE 5  loop hooks swapped; corner_gate.metta replaced with v3 shim")

    # ---------------- PHASE 6: RETIRE ----------------
    shutil.move(CWW_REL, CWW_REL + ".retired.v3")
    say("PHASE 6  corner_window_writers.metta retired (moved)")

    # ---------------- PHASE 7: ARTIFACT_1 ----------------
    art = rd(ART1_REL)
    art_add = ("\n\n" + ART_MARK_B + "\n"
               "## Corner-Gate v3 cutover (2026-07-10, apply_corner_gate_v3_monolith.py)\n"
               "Phase 4.5 seam: apply-corner-gate-v2 is a pass-through shim; gate-aware-results appends the\n"
               "COUPLING-STATE legibility line (S1: novelty still compares raw results). Cycle tail: the\n"
               "populate-corner-window! hook is replaced by do-record-coupling-cycle! (after populate-state-delta\n"
               "and populate-coupling-verdict; ordering load-bearing). initLoop gains do-bootstrap-coupling!.\n"
               "New imports soul/coupling_legibility and soul/coupling_legibility_writers sit after the engine\n"
               "block. corner_window_writers retired. Enforcement machinery removed by design (defects D-A, D-B).\n"
               + ART_MARK_E + "\n")
    wr(ART1_REL, art + art_add, False)
    say("PHASE 7  artifact_1 updated (marked section)")

    # ---------------- PHASE 8: STATIC POSTFLIGHT ----------------
    say("PHASE 8  static postflight")
    man3 = rd(MANIFEST_REL)
    loop3 = rd(LOOP_REL)
    lines3 = man3.splitlines()
    def line_of3(sub):
        for i, l in enumerate(lines3, 1):
            if sub in l and l.startswith("!(import!"):
                return i
        return -1
    e = line_of3(ENGINE_IMPORT_SUB)
    p1 = line_of3("./soul/coupling_legibility)")
    p2 = line_of3("./soul/coupling_legibility_writers)")
    g = line_of3("./soul/corner_gap/corner_gate")
    check("HARD import order: engine < pure < writers", 0 < e < p1 < p2, "e=%d p=%d w=%d" % (e, p1, p2))
    check("shim dependency: imports before corner_gate", p2 < g, "w=%d gate=%d" % (p2, g))
    check("corner_window_writers import gone", CWW_IMPORT not in man3)
    check("lib_quantale still absent", LIBQ_IMPORT not in man3)
    check("hook swapped", HOOK_NEW_SUB in loop3 and HOOK_OLD_SUB not in loop3)
    check("bootstrap inserted", "(do-bootstrap-coupling!)" in loop3)
    check("loop paren delta unchanged", paren_delta(loop3) == paren_delta(loop))
    check("gate shim paren delta 0", paren_delta(rd(GATE_REL)) == 0)
    check("held-by-corner-gate emission gone from gate file", "held-by-corner-gate" not in rd(GATE_REL))
    # S1 POSTFLIGHT
    check("S1 postflight: novelty still raw results",
          "(helper.safe_results_str (repr $results))" in loop3)
    check("S1 postflight: lastresults still from results_final",
          "(repr $results_final)" in loop3)
    check("NO-TOUCH: engine sha unchanged", sha(ENGINE_REL) == engine_sha_pre)
    check("helper payload landed once", rd(HELPER_REL).count(PY_MARK_B) == 1)

    manifest_out = {
        "mode": "apply", "date": "2026-07-10",
        "frozen_payloads": FROZEN, "pre_hashes": pre_hashes,
        "post_hashes": {r: sha(r) for r in (MANIFEST_REL, LOOP_REL, HELPER_REL, GATE_REL, ART1_REL, PURE_DST, WRITERS_DST)},
        "engine_sha": engine_sha_pre, "result": ("FAIL" if FAILED else "GREEN"),
    }
    with open("staging/v3_monolith_apply_manifest.json", "w") as f:
        json.dump(manifest_out, f, indent=2)
    say("PHASE 10  manifest written: staging/v3_monolith_apply_manifest.json")

    if FAILED:
        say(">>> POSTFLIGHT FAILED: AUTO-REVERSING NOW (design doc 5.1).")
        do_reverse(False)
        sys.exit(3)
    say(">>> APPLY COMPLETE AND GREEN. Next: rebuild container, then run")
    say(">>> python3 staging/validate_corner_gate_v3_monolith.py --repo-root . --container clarity_omega")


def do_reverse(dry):
    say("REVERSE: restoring backups, removing created files")
    steps = []
    for rel in (MANIFEST_REL, LOOP_REL, HELPER_REL, GATE_REL, ART1_REL):
        b = rel + BAK
        ok = os.path.exists(b)
        check("backup present " + b, ok)
        steps.append((b, rel))
    cwwr = CWW_REL + ".retired.v3"
    check("retired file present " + cwwr, os.path.exists(cwwr) or os.path.exists(CWW_REL + BAK))
    if FAILED:
        say(">>> REVERSE ABORTED: backups incomplete. Nothing touched.")
        sys.exit(3)
    if dry:
        say(">>> DRY-RUN reverse: would restore the files above and delete created soul files.")
        return
    for b, rel in steps:
        shutil.copy2(b, rel)
    if os.path.exists(cwwr):
        shutil.move(cwwr, CWW_REL)
    elif os.path.exists(CWW_REL + BAK):
        shutil.copy2(CWW_REL + BAK, CWW_REL)
    for rel in (PURE_DST, WRITERS_DST):
        if os.path.exists(rel):
            os.remove(rel)
    # reverse verification: as strong as apply verification
    say("REVERSE VERIFICATION:")
    man = rd(MANIFEST_REL)
    loop = rd(LOOP_REL)
    check("imports gone", "./soul/coupling_legibility)" not in man and MARK_B not in man)
    check("corner_window_writers import restored", CWW_IMPORT in man)
    check("hook restored", HOOK_OLD_SUB in loop and HOOK_NEW_SUB not in loop)
    check("bootstrap hook gone", "(do-bootstrap-coupling!)" not in loop)
    check("helper payload gone", PY_MARK_B not in rd(HELPER_REL))
    check("artifact_1 section gone", ART_MARK_B not in rd(ART1_REL))
    check("created soul files removed",
          not os.path.exists(PURE_DST) and not os.path.exists(WRITERS_DST))
    check("v2 gate body restored (held markers present again)",
          "held-by-corner-gate" in rd(GATE_REL))
    say(">>> REVERSE " + ("FAILED" if FAILED else "COMPLETE AND VERIFIED") + ".")
    sys.exit(3 if FAILED else 0)


if __name__ == "__main__":
    main()
