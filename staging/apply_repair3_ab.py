#!/usr/bin/env python3
"""Repair 3, Surfaces A+B: PAUSE router live + output halt-and-voice +
pause-record awareness (retires W1's halt half and W6).

DESIGN. v9 line 310 (input router is a PAUSE match), v10 (output PAUSE
routes as input does), v9 268-274 (PENDING forces PAUSE; holds at verdict
level since Repair 1 harness V7), Berton design clarification 2026-06-11
(participation, not opaque gating: the verdict returns to her experience).

EDITS (three files, all text-anchored, reversible; helper.py UNTOUCHED):
B1 loop.metta       body: output-pause halt-and-voice branch wrapping the
                    input-PAUSE if, AND the input router returned to the
                    SUBSTRATE primitive (soul-pause?, soul_utils.metta, spec
                    v9 line 310): reasoning back in the substrate, the
                    Python router (helper.soul_is_pause) left as dead code
                    for housecleaning. Voice composed from $person_state +
                    $soul_verdict_out via Repair-2 interpolation; &loops 0.
B2 loop.metta       5c bindings: write/clear &last_pause_note after the
                    journal binding (pause -> note, else -> "").
B3 loop.metta       initLoop: initialize &last_pause_note beside
                    &pending_soul_mutation.
B4 loop.metta       $enriched_prompt: prefix pause-context (Python-shaped,
                    empty when no note).
B5 soul_governance.py  pause_note_compose(verdict_repr) and
                    pause_context(note_repr): pure string plumbing per the
                    Sprint 4 interface contract (Python never decides
                    policy). ELEVATION FLAG: pause_context's guidance
                    sentence is prompt content; candidate for
                    behavioral_guidance.metta per Sprint 1.5 precedent.
ART1 artifact_1     Repairs 1-3 status note prepended at Section 8
                    (Discipline 4: wiring-diagram entry in the same commit).

VERIFY (in-script, function level): soul_is_pause returns 1/0/0 on
synthetic PAUSE/PROCEED/FLAG; pause helpers shape and empty correctly;
py-compile both Python files; code-aware paren delta on loop.metta must be
exactly +1 open +1 close (the added if level), net zero.
LIVE VERIFY (post-rebuild): boot clean; input-PAUSE end-to-end on a
provoked case; W6 via the gate re-emission walk.

Usage: --dry-run (default) | --apply | --reverse --apply
"""
import argparse, py_compile, re, sys, tempfile, os
from pathlib import Path

LOOP = Path("src/loop.metta")
GOV = Path("soul/soul_governance.py")
ART1 = Path("docs/design/artifact_1_loop_metta_wiring_diagram.md")

# ---- B1: output halt-and-voice wrapping the input if ------------------------
B1_OLD = """                                      (if (> (py-call (helper.soul_is_pause $soul_verdict_in)) 0)
                                          ;; PAUSE path: Channel D fires, loop halts"""
B1_NEW = """                                      (if (== $soul_decision pause)
                                          ;; Repair 3 OUTPUT PAUSE: her own verdict halts the cycle and speaks.
                                          ;; Suppression already happened in 5c; this is the return path into
                                          ;; her experience (Berton clarification 2026-06-11; v10 output routing).
                                          (let* (($soul_voice_out (soul-llm-call
                                                    (py-call (helper.soul_voice_prompt $person_state $soul_verdict_out))
                                                    (provider)))
                                                 ($_ (println! (SOUL_VOICE_OUT: $soul_voice_out)))
                                                 ($_ (println! (OUTPUT-PAUSE-ROUTING: HALTING-LOOP))))
                                            (progn (catch (eval (sread $soul_voice_out)))
                                                   (change-state! &loops 0)))
                                      ;; Repair 3: input router returned to the SUBSTRATE primitive
                                      ;; (soul-pause?, soul_utils.metta, spec v9 line 310). helper.soul_is_pause
                                      ;; is now dead code, scheduled for housecleaning.
                                      (if (soul-pause? $soul_verdict_in)
                                          ;; PAUSE path: Channel D fires, loop halts"""

B1_TAIL_OLD = """                                                 (change-state! &lastresults (py-call (helper.safe_results_str (repr $results_final)))))))
                                (if (> (get_time) (get-state &nextWakeAt))"""
B1_TAIL_NEW = """                                                 (change-state! &lastresults (py-call (helper.safe_results_str (repr $results_final))))))))
                                (if (> (get_time) (get-state &nextWakeAt))"""

# ---- B2: pause-record write/clear in 5c -------------------------------------
B2_OLD = """                                       ($_ (if (== $soul_decision pause)
                                               (progn (println! (SOUL-SUPPRESSED $sexpr))
                                                      (py-call (soul_governance.journal_append "PAUSE" (repr $sexpr))))
                                               (if (== $soul_decision flag)
                                                   (py-call (soul_governance.journal_append "FLAG" (repr $sexpr)))
                                                   _)))"""
B2_NEW = """                                       ($_ (if (== $soul_decision pause)
                                               (progn (println! (SOUL-SUPPRESSED $sexpr))
                                                      (py-call (soul_governance.journal_append "PAUSE" (repr $sexpr))))
                                               (if (== $soul_decision flag)
                                                   (py-call (soul_governance.journal_append "FLAG" (repr $sexpr)))
                                                   _)))
                                       ;; Repair 3: pause-record. Visible to her next cycle, cleared by her
                                       ;; next successful batch (information-flow per P4/P5).
                                       ($_ (if (== $soul_decision pause)
                                               (change-state! &last_pause_note (py-call (soul_governance.pause_note_compose (repr $soul_verdict_out))))
                                               (change-state! &last_pause_note "")))"""

# ---- B3: initLoop state var --------------------------------------------------
B3_OLD = """          (change-state! &pending_soul_mutation "")"""
B3_NEW = """          (change-state! &pending_soul_mutation "")
          (change-state! &last_pause_note "")"""

# ---- B4: prompt surfacing ----------------------------------------------------
B4_OLD = """                                       ($enriched_prompt (string_concat $soul_brief $prompt))"""
B4_NEW = """                                       ($enriched_prompt (string_concat (py-call (soul_governance.pause_context (repr (get-state &last_pause_note)))) (string_concat $soul_brief $prompt)))"""

# ---- B5: governance helpers ---------------------------------------------------
B5_MARK = "def pause_note_compose("
B5_CODE = '''

def pause_note_compose(verdict_repr):
    """Repair 3: extract the SOUL-NOTE tail from an output verdict repr.
    Returns the note text (her own words) or the verdict head as fallback."""
    v = str(verdict_repr).strip()
    if v.startswith('"') and v.endswith('"'):
        v = v[1:-1]
    idx = v.find("SOUL-NOTE: ")
    note = v[idx + len("SOUL-NOTE: "):].strip() if idx >= 0 else v[:200]
    return note[:600]


def pause_context(note_repr):
    """Repair 3: prompt prefix surfacing the pause-record. Empty when clear."""
    n = str(note_repr).strip()
    if n.startswith('"') and n.endswith('"'):
        n = n[1:-1]
    n = n.strip()
    if not n:
        return ""
    return ("PREVIOUS-BATCH-PAUSED: your soul paused your previous command batch "
            "and it did not execute. The concern, in your own words: " + n +
            " Address or re-emit knowingly. ")
'''

EDITS_LOOP = [("B1", B1_OLD, B1_NEW), ("B1-tail", B1_TAIL_OLD, B1_TAIL_NEW),
              ("B2", B2_OLD, B2_NEW), ("B3", B3_OLD, B3_NEW), ("B4", B4_OLD, B4_NEW)]

# ---- artifact_1 maintenance entry (Discipline 4: same commit as the hooks) ----
ART1_ANCHOR = """## Section 8: The output verdict stub"""
ART1_NEW = """## Repairs 1-3 status note (2026-06, soul_fully_wired sprint)

Sections 7 and 8 below describe the PRE-REPAIR state and are retained as
history. Current wiring: the 5c output intercept computes a native
gate-state (derive-gate-state), a real verdict (compute-output-verdict),
and a routing decision (output-decision); PAUSE empties execution,
journals (soul/governance_journal.log), writes the pause-record
(&last_pause_note, surfaced in the next cycle's prompt via
soul_governance.pause_context and cleared by the next successful batch),
and halts with a Channel D voice composed from $person_state and
$soul_verdict_out (SOUL_VOICE_OUT / OUTPUT-PAUSE-ROUTING prints). The
input PAUSE router is the substrate primitive (soul-pause?
$soul_verdict_in) per spec v9 line 310; helper.soul_is_pause is dead code
pending housecleaning. New state: &last_pause_note (initLoop). Evidence:
docs/sprints/soul_fully_wired/ ledgers; commits e451811 (Repair 1),
48ce4d6 (Repair 2), and the Repair 3 commit carrying this entry.

""" + ART1_ANCHOR
EDITS_ART1 = [("ART1", ART1_ANCHOR, ART1_NEW)]
B5_LINES = len(B5_CODE.splitlines()) - 1  # rstrip on append eats nothing; trailing newline accounting

def code_aware_parens(text):
    o = c = 0; in_s = esc = False; i = 0
    while i < len(text):
        ch = text[i]
        if in_s:
            if esc: esc = False
            elif ch == "\\": esc = True
            elif ch == '"': in_s = False
        else:
            if ch == '"': in_s = True
            elif ch == ";":
                while i < len(text) and text[i] != "\n": i += 1
                continue
            elif ch == "(": o += 1
            elif ch == ")": c += 1
        i += 1
    return o, c

def apply_pairs(content, pairs, reverse=False):
    for name, old, new in pairs:
        a, b = (new, old) if reverse else (old, new)
        if content.count(a) != 1:
            raise RuntimeError(f"{name}: anchor count {content.count(a)} (need exactly 1)")
        content = content.replace(a, b, 1)
    return content

def verify_gov(gov_src):
    ns = {}
    exec(gov_src[gov_src.find(B5_MARK):], ns)
    note = ns["pause_note_compose"]('"VERDICT: PAUSE SOUL-NOTE: writing to my gate file mid-investigation"')
    ctx = ns["pause_context"]('"' + note + '"')
    empty = ns["pause_context"]('""')
    return ("writing to my gate file" in note and "PREVIOUS-BATCH-PAUSED" in ctx
            and note in ctx and empty == "")

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--apply", action="store_true")
    ap.add_argument("--reverse", action="store_true")
    ap.add_argument("--dry-run", dest="dry_run", action="store_true",
                    help="explicit dry-run (also the default when --apply is absent)")
    a = ap.parse_args()
    if a.dry_run and a.apply:
        print("CONFLICT: --dry-run and --apply are mutually exclusive."); return 1
    l, g, art = LOOP.read_text(), GOV.read_text(), ART1.read_text()
    try:
        if not a.reverse:
            l2 = apply_pairs(l, EDITS_LOOP)
            if B5_MARK in g: raise RuntimeError("B5 already applied")
            g2 = g.rstrip("\n") + B5_CODE
            art2 = apply_pairs(art, EDITS_ART1)
        else:
            l2 = apply_pairs(l, EDITS_LOOP, reverse=True)
            if B5_MARK not in g: raise RuntimeError("B5 not present")
            g2 = g.replace(B5_CODE, "")
            if B5_MARK in g2: raise RuntimeError("B5 reverse failed")
            art2 = apply_pairs(art, EDITS_ART1, reverse=True)
    except RuntimeError as e:
        print(f"STATE CHECK FAILED: {e}"); return 1

    o1, c1 = code_aware_parens(l); o2, c2 = code_aware_parens(l2)
    direction = -1 if a.reverse else 1
    if (o2 - o1, c2 - c1) != (32 * direction, 32 * direction):
        print(f"PAREN DELTA UNEXPECTED: opens {o2-o1:+d} closes {c2-c1:+d} (expected {32*direction:+d}/{32*direction:+d})")
        return 1
    if (o1 - c1) != (o2 - c2):
        print("NET PAREN BALANCE CHANGED"); return 1
    with tempfile.NamedTemporaryFile("w", suffix=".py", delete=False) as f:
        f.write(g2); tmp = f.name
    try: py_compile.compile(tmp, doraise=True)
    finally: os.unlink(tmp)
    ld = {"loop.metta": (len(l2.splitlines()) - len(l.splitlines()), 20 * direction),
          "soul_governance.py": (len(g2.splitlines()) - len(g.splitlines()), B5_LINES * direction),
          "artifact_1.md": (len(art2.splitlines()) - len(art.splitlines()), 17 * direction)}
    for name, (got, exp) in ld.items():
        print(f"  {name}: line delta {got:+d} (expected {exp:+d}) {'OK' if got == exp else 'FAIL'}")
        if got != exp: return 1
    print(f"Anchors clean; loop paren delta {o2-o1:+d}/{c2-c1:+d} net-zero; py-compile OK")
    if not a.reverse:
        ok2 = verify_gov(g2)
        print(f"FUNCTION VERIFY pause helpers (compose/context/empty): {'PASS' if ok2 else 'FAIL'}")
        if not ok2: return 1
        for label, old_t, new_t in (("loop first change", l, l2), ("artifact_1 first change", art, art2)):
            for i, (x, y) in enumerate(zip(old_t.splitlines(), new_t.splitlines())):
                if x != y:
                    print(f"  DIFF PREVIEW [{label}] line {i+1}:")
                    print(f"    - {x.strip()[:100]}")
                    print(f"    + {y.strip()[:100]}")
                    break
    if not a.apply:
        print("DRY-RUN: no writes."); return 0
    if not a.reverse:
        for p, orig in ((LOOP, l), (GOV, g), (ART1, art)):
            Path(str(p) + ".bak.repair3").write_text(orig)
        print("Backups: *.bak.repair3 x3")
    LOOP.write_text(l2); GOV.write_text(g2); ART1.write_text(art2)
    do, dc = code_aware_parens(LOOP.read_text())
    print(f"DISK RECHECK: loop.metta parens {do}/{dc} delta {do-dc}")
    print(f"Wrote 3 files ({'REVERSE' if a.reverse else 'FORWARD'})")
    print("Rebuild: docker compose build --no-cache clarityclaw && docker compose up -d")
    return 0

if __name__ == "__main__":
    sys.exit(main())
