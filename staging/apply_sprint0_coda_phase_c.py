#!/usr/bin/env python3
"""
Apply script: Sprint 0-Coda Phase C. Wires the capability-registry
skill-discovery dispatch into the live loop. Five coordinated changes land as
one commit. All or none.

Follows the apply_task_state_step2_wiring.py template: code-aware paren counting
(pre and post, delta 0), per-file forward/reverse state predicates, simulate
in memory then disk-verify after write, diff preview in dry-run, argparse with
--reverse gated behind --apply, backups on forward apply.

Deliberate deviation from the template: anchor matching is whitespace-tolerant
(exact tokens, any whitespace run collapses to \\s+) rather than byte-exact.
The template's anchors were copied verbatim from the live tree; these are
reconstructed, so byte-exact matching is fragile across indentation/line-ending
differences. Everything else follows the template.

The five changes
----------------
Change 0: soul/capability_registry.metta (in place)
  Wrap run-chain's (if ...) in (progn (add-atom (dispatch-result ...)) (if ...))
  so the handler result getContext reads is persisted. Anchor: the run-chain
  decision-anchor if-block. Paren delta 0 (balanced progn wrapper).

Change 1: soul/capabilities/skill_discovery.metta (NEW FILE)
  First production capability: 5-field registration + read-only handler +
  format-skill-set returning (getSkills) for Option (a) parity.

Change 2: lib_clarity_reasoning/lib_clarity_reasoning.metta
  Append imports for capability_registry and skill_discovery, each guarded so
  an already-present import is not duplicated.

Change 3: src/loop.metta (getContext, Phase 4.3)
  Wrap getContext body in a let* that fires dispatch, reads the dispatch-result
  skill-set, binds $skills-str and $skills-len, emits DIAG-CYCLE-DISPATCH, and
  substitutes $skills-str for (getSkills) in the prompt. getSkills DEFINITION
  in src/skills.metta is untouched (retained for Phase D parity).

Change 4: docs/design/artifact_1_loop_metta_wiring_diagram.md
  Insert a dispatch-insertion section before "## Document end" (Discipline 4).

Net change (paren delta 0 on every .metta file)
-----------------------------------------------
- capability_registry.metta: +progn wrapper + dispatch-result add-atom
- skill_discovery.metta: new, self-balanced
- lib_clarity_reasoning.metta: +import lines (balanced directives)
- loop.metta: getContext gains the let* dispatch block; getSkills -> $skills-str
- artifact_1.md: +documentation (markdown, no paren check)

Usage
-----
Dry-run (default):  python3 staging/apply_sprint0_coda_phase_c.py
Apply:              python3 staging/apply_sprint0_coda_phase_c.py --apply
Reverse (dry-run):  python3 staging/apply_sprint0_coda_phase_c.py --reverse
Reverse (write):    python3 staging/apply_sprint0_coda_phase_c.py --reverse --apply

Pre-conditions
--------------
- Run from repo root.
- Sprint 0 capability_registry.metta present at soul/capability_registry.metta.
- Container can be rebuilt after apply.

Backup files (forward apply only):
- soul/capability_registry.metta.bak.coda_phase_c
- lib_clarity_reasoning/lib_clarity_reasoning.metta.bak.coda_phase_c
- src/loop.metta.bak.coda_phase_c
- docs/design/artifact_1_loop_metta_wiring_diagram.md.bak.coda_phase_c
(skill_discovery.metta is new; reverse deletes it, no backup.)
"""
from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

# ============================================================================
# FILE PATHS
# ============================================================================

REGISTRY_PATH = Path("soul/capability_registry.metta")          # Change 0 DESTINATION
REGISTRY_BAK = Path("soul/capability_registry.metta.bak.coda_phase_c")
DRAFT_PATH = Path("soul/capability_registry_path_c_draft.metta")  # Change 0 SOURCE (Path C, ours)

SKILL_PATH = Path("soul/capabilities/skill_discovery.metta")  # NEW FILE

LIB_CR_PATH = Path("lib_clarity_reasoning/lib_clarity_reasoning.metta")
LIB_CR_BAK = Path("lib_clarity_reasoning/lib_clarity_reasoning.metta.bak.coda_phase_c")

LOOP_PATH = Path("src/loop.metta")
LOOP_BAK = Path("src/loop.metta.bak.coda_phase_c")

ARTIFACT1_PATH = Path("docs/design/artifact_1_loop_metta_wiring_diagram.md")
ARTIFACT1_BAK = Path("docs/design/artifact_1_loop_metta_wiring_diagram.md.bak.coda_phase_c")

# ============================================================================
# CHANGE 0: run-chain dispatch-result write (anchored, whitespace-tolerant)
# Wrapping a balanced (if ...) in (progn <balanced add-atom> <if>) keeps the
# paren delta at 0 by construction.
# ============================================================================

RUNCHAIN_OLD = """(if (== $result decision-anchor)
                             (add-atom &self
                               (dispatch-chain-anchored
                                 invocation-id: $invocation-id
                                 anchor-handler: $handler))
                             (run-chain $tail $input-atom $invocation-id))"""

RUNCHAIN_NEW = """(progn
                           (add-atom &self
                             (dispatch-result
                               invocation-id: $invocation-id
                               result: $result
                               handler: $handler))
                           (if (== $result decision-anchor)
                             (add-atom &self
                               (dispatch-chain-anchored
                                 invocation-id: $invocation-id
                                 anchor-handler: $handler))
                             (run-chain $tail $input-atom $invocation-id)))"""

# CHANGE 0 (retention): insert the per-cycle sweep into dispatch. The sweep
# definition lands just before dispatch, and a (sweep-dispatch-atoms!) call is
# inserted as the first progn step so the prior cycle's transient dispatch-*
# atoms are cleared before this cycle's are written. Proven by
# probe_dispatch_retention.py (A0 remove-on-zero no-op; sweep clears the real
# shapes; two swept cycles hold the atomspace at one cycle's worth). Touches
# ONLY transients; efficacy/observation atoms (the learning surface) are never
# swept (Clarity-confirmed boundary). Seam: NACE's per-cycle outcome extraction
# runs within the cycle after getContext, before the next cycle's dispatch sweep.
DISPATCH_SWEEP_OLD = """(= (dispatch $input-atom $invocation-id)
   (progn
      (add-atom &self
                (dispatch-invocation"""

DISPATCH_SWEEP_NEW = """;; Per-cycle retention: clear the prior cycle's transient dispatch records
;; before writing this cycle's, so dispatch-* atoms do not accumulate across the
;; loop's lifetime. Variable patterns clear all ids/counts (map remove-all,
;; self-healing). Touches ONLY transients; the efficacy/observation learning
;; surface is never swept. A0 (remove-on-zero) proven no-op, so the first-cycle
;; sweep on a clean state is safe.
(= (sweep-dispatch-atoms!)
   (let $_a (remove-atom &self (dispatch-invocation invocation-id: $i1 input-atom: $a1))
   (let $_b (remove-atom &self (capability-invoked invocation-id: $i2 handler: $h2 input-atom: $a2))
   (let $_c (remove-atom &self (dispatch-result invocation-id: $i3 result: $r3 handler: $h3))
   (let $_d (remove-atom &self (dispatch-chain-exhausted invocation-id: $i4))
   (let $_e (remove-atom &self (dispatch-chain-anchored invocation-id: $i5 anchor-handler: $h5))
   (let $_f (remove-atom &self (dispatch-fallback-activated invocation-id: $i6 input-atom: $a6 reason: $r6))
        swept)))))))

(= (dispatch $input-atom $invocation-id)
   (progn
      (sweep-dispatch-atoms!)
      (add-atom &self
                (dispatch-invocation"""

# ============================================================================
# CHANGE 1: skill_discovery.metta (new file, full content)
# ============================================================================

SKILL_DISCOVERY_CONTENT = """;; soul/capabilities/skill_discovery.metta
;; Sprint 0-Coda Phase C: first production capability + getContext skills accessor.
;;
;; Option (a): the registry consultation is wired and structurally present; the
;; emitted content is the existing hardcoded skill list (via getSkills), so the
;; LLM-facing content is unchanged while the dispatch path becomes its source.
;; Sprint 1 replaces format-skill-set's body with real (registered-capability)
;; formatting and retires getSkills after the Phase D P-4 parity check holds.

;; --- Lifecycle eligibility seed ------------------------------------------
;; eligible? (in the registry) matches (eligible-lifecycle $l). Without this
;; atom, lifecycle-filter-step drops every active capability and dispatch
;; always falls back. Seeding active as eligible is what lets skill-discovery
;; pass the filter pipeline and reach the handler.
(eligible-lifecycle active)

;; --- Registration (5-field, matches the Path C dispatcher's canonical schema)
(registered-capability
   schema: (skill-request cycle: $k)
   handler: skill-discovery
   priority: 100
   lifecycle: active
   metadata: ())

;; --- Handler (read-only; writes no atoms; returns one skill-set) ----------
(= (skill-discovery $request)
   (let* (($capabilities (collapse (match &self
                                          (registered-capability
                                            schema: $s
                                            handler: $h
                                            priority: $p
                                            lifecycle: active
                                            metadata: $m)
                                          ($s $h $p $m))))
          ($formatted (format-skill-set $capabilities)))
         (skill-set skills: $formatted)))

;; --- Formatter (Option a: emit current hardcoded skills via getSkills) ----
(= (format-skill-set $capabilities) (getSkills))

;; --- getContext-facing TOTAL skills accessor (the named hook) -------------
;; Fires dispatch for this cycle, reads this cycle's skill-set from
;; dispatch-result, and falls back to (getSkills) when the read is empty, so a
;; dispatch miss can NEVER crash prompt assembly. getContext calls this single
;; named function (Artifact 0 Discipline 1).
(= (dispatch-skills $k)
   (let $_ (dispatch (skill-request cycle: $k) $k)
        (first-skill-or-default
          (collapse (match &self
                          (dispatch-result
                            invocation-id: $k
                            result: (skill-set skills: $s)
                            handler: $_h)
                          $s)))))

;; Total over the collapsed result: skip () padding markers, return the first
;; real string, else (getSkills). (== x ()) is the registry's own empty-check
;; idiom (see the dispatch fn's eligible-empty branch).
(= (first-skill-or-default $strs)
   (if (== $strs ())
       (getSkills)
       (let $h (car-atom $strs)
            (if (== $h ())
                (first-skill-or-default (cdr-atom $strs))
                $h))))
"""

# ============================================================================
# CHANGE 2: manifest imports (each guarded; appended after the last import)
# ============================================================================

REGISTRY_IMPORT = "!(import! &self (library omegaclaw ./soul/capability_registry))"
SKILL_IMPORT = "!(import! &self (library omegaclaw ./soul/capabilities/skill_discovery))"

# ============================================================================
# CHANGE 3: getContext dispatch insertion (anchored, whitespace-tolerant)
# ============================================================================

GETCONTEXT_OLD = """(= (getContext $k)
   (string-safe (py-str ("PROMPT: " (getPrompt) " SKILLS: " (getSkills)
                         " " (output-format-guidance)
                         " YOUR_LAST_ACTION: " (your-last-action-block $k)
                         " " (task-state-block)
                         " " (idle-pattern-block)
                         " " (agency-balance-block)
                         " LAST_SKILL_USE_RESULTS: " (last_chars (get-state &lastresults) (maxFeedback)) " HISTORY: " (getHistory) " TIME: " (get_time_as_string)))))"""

GETCONTEXT_NEW = """(= (getContext $k)
   (let* (($skills-str (dispatch-skills $k))
          ($skills-len (size-atom $skills-str))
          ($_marker (println! (DIAG-CYCLE-DISPATCH invocation-id: $k skills-len: $skills-len))))
     (string-safe (py-str ("PROMPT: " (getPrompt) " SKILLS: " $skills-str
                         " " (output-format-guidance)
                         " YOUR_LAST_ACTION: " (your-last-action-block $k)
                         " " (task-state-block)
                         " " (idle-pattern-block)
                         " " (agency-balance-block)
                         " LAST_SKILL_USE_RESULTS: " (last_chars (get-state &lastresults) (maxFeedback)) " HISTORY: " (getHistory) " TIME: " (get_time_as_string))))))"""

# ============================================================================
# CHANGE 4: artifact_1 dispatch-insertion section (inserted before doc end)
# ============================================================================

ARTIFACT1_ANCHOR = "## Document end"

ARTIFACT1_SUBSECTION = (
    "## Sprint 0-Coda Phase C: capability-registry dispatch insertion (getContext)\n"
    "\n"
    "Added by Sprint 0-Coda Phase C (see docs/design/sprint_0_coda_phase_a_v6.md).\n"
    "\n"
    "Phase 4.3 (prompt assembly), getContext. getContext binds its skills slot to\n"
    "a single named accessor that consults the capability registry each cycle:\n"
    "\n"
    "- CALLS: (dispatch-skills $k) in soul/capabilities/skill_discovery.metta,\n"
    "  which fires (dispatch (skill-request cycle: $k) $k); invocation-id is the\n"
    "  loop iteration $k (monotonic, distinct per cycle; no counter atom).\n"
    "- READS (inside dispatch-skills): (dispatch-result invocation-id: $k\n"
    "  result: (skill-set skills: $s) handler: $_), this cycle's skill-set, and\n"
    "  falls back to (getSkills) via first-skill-or-default when the read is empty,\n"
    "  so a dispatch miss can never fail getContext as a goal.\n"
    "- WRITES (via dispatch -> run-chain): dispatch-invocation, capability-invoked,\n"
    "  dispatch-result, and dispatch-chain-exhausted / -anchored / fallback per\n"
    "  the chain outcome.\n"
    "- EMITS: (DIAG-CYCLE-DISPATCH invocation-id: $k skills-len: <int>) every cycle,\n"
    "  where skills-len is (size-atom $skills-str), the skill-set element count.\n"
    "  The skills value is a compound list, so a scalar string op (string_length)\n"
    "  throws on it per the Atom Operations Map read-instrument rule; size-atom is\n"
    "  compound-aware and returns a bare scalar that renders clean.\n"
    "  Phase D in-loop verification: P-2 distinct id, P-3 count > 0, P-4 stable.\n"
    "- SUBSTITUTES (dispatch-skills $k) for (getSkills) in the SKILLS slot. The\n"
    "  getSkills DEFINITION remains callable in src/skills.metta (it is the\n"
    "  fallback) until Phase D P-4 confirms parity; its removal is a later commit.\n"
    "- SEEDS (in skill_discovery.metta): (eligible-lifecycle active), required for\n"
    "  skill-discovery to pass lifecycle-filter-step and reach its handler.\n"
    "- NETWORK: SN (capability selection / skills surfacing).\n"
    "\n"
    "NOTE (follow-up, not done in this commit): the broader line-number drift fix\n"
    "across this document is deferred to a dedicated housekeeping pass.\n"
    "\n"
    "---\n"
    "\n"
)

ARTIFACT1_OLD_AT_ANCHOR = ARTIFACT1_ANCHOR
ARTIFACT1_NEW_AT_ANCHOR = ARTIFACT1_SUBSECTION + ARTIFACT1_ANCHOR


# ============================================================================
# HELPERS (code_aware_paren_count + find_target_substring_count reused verbatim
# from apply_task_state_step2_wiring.py; ws_* added for tolerant matching)
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


def ws_pattern(anchor: str) -> re.Pattern:
    """Whitespace-tolerant: exact tokens, any whitespace run -> \\s+."""
    return re.compile(r"\s+".join(re.escape(t) for t in anchor.split()))


def ws_count(text: str, anchor: str) -> int:
    return len(ws_pattern(anchor).findall(text))


def ws_replace_once(content: str, old: str, new: str, label: str) -> str:
    matches = list(ws_pattern(old).finditer(content))
    if len(matches) != 1:
        raise RuntimeError(
            "%s: expected exactly 1 whitespace-tolerant match, found %d."
            % (label, len(matches))
        )
    s, e = matches[0].span()
    return content[:s] + new + content[e:]


def dump_region(text: str, keyword: str, path: Path) -> None:
    lines = text.splitlines()
    idxs = [i for i, l in enumerate(lines) if keyword in l]
    print("  ---- live region of %s near %r ----" % (path, keyword))
    if idxs:
        a = max(0, idxs[0] - 8)
        b = min(len(lines), idxs[-1] + 6)
        for i in range(a, b):
            print("  %4d| %s" % (i + 1, lines[i]))
    else:
        print("  (keyword %r not present)" % keyword)
    print("  ---- end region ----")


# ============================================================================
# SIMULATION (forward + reverse, per file)
# ============================================================================

def simulate_registry_forward(content: str) -> str:
    return ws_replace_once(content, RUNCHAIN_OLD, RUNCHAIN_NEW, "registry forward run-chain")


def process_registry_promotion(args):
    """Change 0 is a PROMOTION: read the Path C draft (SOURCE), apply the
    run-chain dispatch-result edit, write to capability_registry.metta
    (DESTINATION). Forward validates the draft and returns the promoted content.
    Reverse restores the destination from its backup (handled in main)."""
    print("\n>>> Change 0: promote %s -> %s <<<" % (DRAFT_PATH, REGISTRY_PATH))
    if args.reverse:
        print("  Reverse: capability_registry.metta will be restored from backup.")
        return True, "", ""
    if not DRAFT_PATH.exists():
        print("  ERROR: draft source %s not found. Run from repo root." % DRAFT_PATH)
        return False, "", ""
    draft = DRAFT_PATH.read_text()
    # Source state: draft carries the run-chain anchor and has no dispatch-result yet.
    has_anchor = ws_count(draft, RUNCHAIN_OLD) == 1
    no_dr = "dispatch-result" not in draft
    print("  Draft source state: run-chain anchor=%s, dispatch-result absent=%s" % (has_anchor, no_dr))
    if not (has_anchor and no_dr):
        print("  SOURCE STATE FAILED. Aborting.")
        dump_region(draft, "decision-anchor", DRAFT_PATH)
        return False, draft, ""
    o, c = code_aware_paren_count(draft)
    print("  Draft pre-edit code-aware paren: opens=%d closes=%d delta=%d (%s)"
          % (o, c, o - c, "OK" if o == c else "FAIL"))
    if o != c:
        print("  DRAFT PAREN DELTA NONZERO. Aborting.")
        return False, draft, ""
    try:
        promoted = ws_replace_once(draft, RUNCHAIN_OLD, RUNCHAIN_NEW, "Change 0 run-chain")
    except RuntimeError as exc:
        print("  SIMULATION FAILED (run-chain): %s" % exc)
        return False, draft, ""
    try:
        promoted = ws_replace_once(promoted, DISPATCH_SWEEP_OLD, DISPATCH_SWEEP_NEW, "Change 0 sweep")
    except RuntimeError as exc:
        print("  SIMULATION FAILED (sweep): %s" % exc)
        return False, draft, promoted
    # After both edits: the run-chain ADD ("result: $result") lands once; the
    # sweep adds one more "dispatch-result" mention (its remove pattern) plus
    # sweep-dispatch-atoms!. Verify the add wrap, the sweep, and one call site.
    checks = {
        "run-chain dispatch-result add (result: $result)": promoted.count("result: $result") == 1,
        "sweep-dispatch-atoms! defined": "(= (sweep-dispatch-atoms!)" in promoted,
        "sweep call inserted in dispatch": "(sweep-dispatch-atoms!)\n      (add-atom" in promoted,
    }
    for label, ok in checks.items():
        print("  %s: %s" % (label, "OK" if ok else "FAIL"))
    if not all(checks.values()):
        print("  PROMOTION CONTENT CHECK FAILED. Aborting.")
        return False, draft, promoted
    o2, c2 = code_aware_paren_count(promoted)
    print("  Promoted post-edit code-aware paren: opens=%d closes=%d delta=%d (%s)"
          % (o2, c2, o2 - c2, "OK" if o2 == c2 else "FAIL"))
    if o2 != c2:
        print("  PROMOTED PAREN DELTA NONZERO. Aborting.")
        return False, draft, promoted
    return True, draft, promoted


def registry_disk_ok_forward(disk: str) -> tuple[bool, str]:
    o, c = code_aware_paren_count(disk)
    bal = o == c
    has_add = disk.count("result: $result") == 1          # run-chain dispatch-result ADD
    has_sweep = "(= (sweep-dispatch-atoms!)" in disk        # retention sweep present
    is_path_c = "walk-filter-steps" in disk
    ok = bal and has_add and has_sweep and is_path_c
    return ok, "paren delta=%d, dispatch-result-add=%s, sweep=%s, Path C marker=%s -> %s" % (
        o - c, has_add, has_sweep, is_path_c, "OK" if ok else "FAIL")


def simulate_loop_forward(content: str) -> str:
    return ws_replace_once(content, GETCONTEXT_OLD, GETCONTEXT_NEW, "loop forward getContext")


def simulate_loop_reverse(content: str) -> str:
    return ws_replace_once(content, GETCONTEXT_NEW, GETCONTEXT_OLD, "loop reverse getContext")


def _lib_block(imports: list[str]) -> str:
    return "\n;; Capability registry dispatch (Sprint 0-Coda Phase C)\n" + "\n".join(imports) + "\n"


def simulate_lib_cr_forward(content: str) -> str:
    """Append whichever of the two imports is absent, after the last import line."""
    additions = [imp for imp in (REGISTRY_IMPORT, SKILL_IMPORT) if imp not in content]
    if not additions:
        raise RuntimeError("lib_cr forward: both imports already present (already applied?).")
    block = _lib_block(additions)
    last = content.rfind("!(import!")
    if last == -1:
        return content.rstrip("\n") + "\n" + block
    eol = content.find("\n", last)
    eol = len(content) if eol == -1 else eol
    return content[: eol + 1] + block + content[eol + 1:]


def simulate_lib_cr_reverse(content: str) -> str:
    """Remove the exact Phase C block that forward inserted (exact inverse)."""
    present = [imp for imp in (REGISTRY_IMPORT, SKILL_IMPORT) if imp in content]
    if not present:
        raise RuntimeError("lib_cr reverse: Phase C imports not found.")
    block = _lib_block(present)
    if block not in content:
        raise RuntimeError("lib_cr reverse: exact Phase C block not found (manual edit?).")
    return content.replace(block, "", 1)


def simulate_artifact1_forward(content: str) -> str:
    count = find_target_substring_count(content, ARTIFACT1_OLD_AT_ANCHOR)
    if count != 1:
        raise RuntimeError(
            "artifact1 forward: expected 1 occurrence of %r, found %d."
            % (ARTIFACT1_ANCHOR, count)
        )
    return content.replace(ARTIFACT1_OLD_AT_ANCHOR, ARTIFACT1_NEW_AT_ANCHOR, 1)


def simulate_artifact1_reverse(content: str) -> str:
    count = find_target_substring_count(content, ARTIFACT1_NEW_AT_ANCHOR)
    if count != 1:
        raise RuntimeError("artifact1 reverse: expected 1 occurrence of new subsection block.")
    return content.replace(ARTIFACT1_NEW_AT_ANCHOR, ARTIFACT1_OLD_AT_ANCHOR, 1)


# ============================================================================
# STATE CHECK PREDICATES (forward: pre-edit state; reverse: post-forward state)
# ============================================================================

def registry_forward_state_ok(content: str) -> tuple[bool, str]:
    has_anchor = ws_count(content, RUNCHAIN_OLD) == 1
    no_new = "dispatch-result" not in content
    ok = has_anchor and no_new
    return ok, "run-chain anchor=%s, dispatch-result absent=%s -> %s" % (
        has_anchor, no_new, "OK" if ok else "FAIL")


def registry_reverse_state_ok(content: str) -> tuple[bool, str]:
    has_new = "dispatch-result" in content
    return has_new, "dispatch-result present=%s -> %s" % (has_new, "OK" if has_new else "FAIL")


def loop_forward_state_ok(content: str) -> tuple[bool, str]:
    has_anchor = ws_count(content, GETCONTEXT_OLD) == 1
    no_new = "DIAG-CYCLE-DISPATCH" not in content
    ok = has_anchor and no_new
    return ok, "getContext anchor=%s, marker absent=%s -> %s" % (
        has_anchor, no_new, "OK" if ok else "FAIL")


def loop_reverse_state_ok(content: str) -> tuple[bool, str]:
    has_new = "DIAG-CYCLE-DISPATCH" in content
    return has_new, "DIAG-CYCLE-DISPATCH present=%s -> %s" % (has_new, "OK" if has_new else "FAIL")


def lib_cr_forward_state_ok(content: str) -> tuple[bool, str]:
    has_skill = SKILL_IMPORT in content
    ok = not has_skill
    return ok, "skill_discovery import absent=%s -> %s" % (not has_skill, "OK" if ok else "FAIL")


def lib_cr_reverse_state_ok(content: str) -> tuple[bool, str]:
    has_skill = SKILL_IMPORT in content
    return has_skill, "skill_discovery import present=%s -> %s" % (has_skill, "OK" if has_skill else "FAIL")


def artifact1_forward_state_ok(content: str) -> tuple[bool, str]:
    has_anchor = find_target_substring_count(content, ARTIFACT1_ANCHOR) == 1
    no_new = "Sprint 0-Coda Phase C: capability-registry dispatch insertion" not in content
    ok = has_anchor and no_new
    return ok, "doc-end anchor=%s, section absent=%s -> %s" % (
        has_anchor, no_new, "OK" if ok else "FAIL")


def artifact1_reverse_state_ok(content: str) -> tuple[bool, str]:
    has_new = "Sprint 0-Coda Phase C: capability-registry dispatch insertion" in content
    return has_new, "section present=%s -> %s" % (has_new, "OK" if has_new else "FAIL")


# ============================================================================
# DIFF PREVIEW (reused verbatim from the template)
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
            return "--- %s: NO CHANGES DETECTED ---" % label
        differ_start = min(len(old_lines), len(new_lines))
    differ_end_old = len(old_lines) - 1
    differ_end_new = len(new_lines) - 1
    while differ_end_old > differ_start and differ_end_new > differ_start:
        if old_lines[differ_end_old] == new_lines[differ_end_new]:
            differ_end_old -= 1
            differ_end_new -= 1
        else:
            break
    out = ["--- %s (lines %d to %d) ---" % (label, differ_start + 1, max(differ_end_old, differ_end_new) + 1)]
    start = max(0, differ_start - context)
    for i in range(start, differ_start):
        if i < len(old_lines):
            out.append("  " + old_lines[i])
    for i in range(differ_start, differ_end_old + 1):
        if i < len(old_lines):
            out.append("- " + old_lines[i])
    for i in range(differ_start, differ_end_new + 1):
        if i < len(new_lines):
            out.append("+ " + new_lines[i])
    end_old = min(len(old_lines), differ_end_old + 1 + context)
    for i in range(differ_end_old + 1, end_old):
        out.append("  " + old_lines[i])
    return "\n".join(out)


# ============================================================================
# PROCESS
# ============================================================================

def check_file_exists(path: Path, label: str) -> bool:
    if not path.exists():
        print("ERROR: %s not found at %s. Run from repo root." % (label, path))
        return False
    return True


def process_file(path, simulate_fn, simulate_reverse_fn, args, label,
                 check_parens, forward_state_check_fn, reverse_state_check_fn,
                 keyword_for_dump):
    """Read, pre-check (paren delta 0 + state), simulate, post-check (paren
    delta 0). Returns (ok, original, simulated)."""
    print("\n>>> %s <<<" % label)
    content = path.read_text()
    pre_lines = len(content.splitlines())
    print("  Path: %s" % path)
    print("  Pre-edit line count: %d" % pre_lines)

    if check_parens:
        o, c = code_aware_paren_count(content)
        d = o - c
        verdict = "OK" if d == 0 else "FAIL"
        print("  Pre-edit code-aware paren: opens=%d closes=%d delta=%d (%s)" % (o, c, d, verdict))
        if d != 0:
            print("  PRE-EDIT PAREN DELTA NONZERO for %s. Aborting." % label)
            return False, content, ""

    if args.reverse:
        state_ok, state_msg = reverse_state_check_fn(content)
    else:
        state_ok, state_msg = forward_state_check_fn(content)
    print("  State check: %s" % state_msg)
    if not state_ok:
        print("  STATE CHECK FAILED for %s. Aborting." % label)
        if not args.reverse and keyword_for_dump:
            dump_region(content, keyword_for_dump, path)
        return False, content, ""

    try:
        simulated = simulate_reverse_fn(content) if args.reverse else simulate_fn(content)
    except RuntimeError as exc:
        print("  SIMULATION FAILED: %s" % exc)
        if not args.reverse and keyword_for_dump:
            dump_region(content, keyword_for_dump, path)
        return False, content, ""

    post_lines = len(simulated.splitlines())
    print("  Line delta: %d (informational; whitespace-tolerant matching)" % (post_lines - pre_lines))

    if check_parens:
        o2, c2 = code_aware_paren_count(simulated)
        d2 = o2 - c2
        verdict2 = "OK" if d2 == 0 else "FAIL"
        print("  Post-edit code-aware paren: opens=%d closes=%d delta=%d (%s)" % (o2, c2, d2, verdict2))
        if d2 != 0:
            print("  POST-EDIT PAREN DELTA NONZERO for %s. Aborting." % label)
            return False, content, simulated

    return True, content, simulated


def process_new_file(path, args):
    """skill_discovery.metta: forward creates it, reverse deletes it."""
    print("\n>>> %s (new file) <<<" % SKILL_PATH)
    if args.reverse:
        if not path.exists():
            print("  Already absent; nothing to reverse. OK")
            return True, None
        o, c = code_aware_paren_count(path.read_text())
        print("  Present, code-aware paren delta=%d. Will delete on --apply." % (o - c))
        return True, None
    # forward
    if path.exists():
        print("  STATE CHECK FAILED: %s already exists. Aborting." % path)
        return False, None
    o, c = code_aware_paren_count(SKILL_DISCOVERY_CONTENT)
    d = o - c
    verdict = "OK" if d == 0 else "FAIL"
    print("  New-file code-aware paren: opens=%d closes=%d delta=%d (%s)" % (o, c, d, verdict))
    if d != 0:
        print("  NEW-FILE PAREN DELTA NONZERO. Aborting.")
        return False, None
    print("  Lines to write: %d" % len(SKILL_DISCOVERY_CONTENT.splitlines()))
    return True, SKILL_DISCOVERY_CONTENT


# ============================================================================
# MAIN
# ============================================================================

def main() -> int:
    parser = argparse.ArgumentParser(
        description="Sprint 0-Coda Phase C: capability-registry dispatch wiring (5 changes)."
    )
    parser.add_argument("--apply", action="store_true", help="Write changes. Default is dry-run.")
    parser.add_argument("--reverse", action="store_true", help="Reverse the edits. Combine with --apply to write.")
    args = parser.parse_args()

    direction = "REVERSE" if args.reverse else "APPLY"
    print("\n========== SPRINT 0-CODA PHASE C: %s ==========" % direction)

    if not all([
        check_file_exists(REGISTRY_PATH, "capability_registry.metta"),
        check_file_exists(LIB_CR_PATH, "lib_clarity_reasoning.metta"),
        check_file_exists(LOOP_PATH, "loop.metta"),
        check_file_exists(ARTIFACT1_PATH, "artifact_1.md"),
    ]):
        return 1
    if not args.reverse and not check_file_exists(DRAFT_PATH, "capability_registry_path_c_draft.metta"):
        return 1

    ok_reg, reg_orig, reg_sim = process_registry_promotion(args)
    if not ok_reg:
        return 1

    ok_skill, skill_content = process_new_file(SKILL_PATH, args)
    if not ok_skill:
        return 1

    ok_lib, lib_orig, lib_sim = process_file(
        LIB_CR_PATH, simulate_lib_cr_forward, simulate_lib_cr_reverse, args,
        "lib_clarity_reasoning.metta", True,
        lib_cr_forward_state_ok, lib_cr_reverse_state_ok, "import!")
    if not ok_lib:
        return 1

    ok_loop, loop_orig, loop_sim = process_file(
        LOOP_PATH, simulate_loop_forward, simulate_loop_reverse, args,
        "loop.metta", True,
        loop_forward_state_ok, loop_reverse_state_ok, "getContext")
    if not ok_loop:
        return 1

    ok_art, art_orig, art_sim = process_file(
        ARTIFACT1_PATH, simulate_artifact1_forward, simulate_artifact1_reverse, args,
        "artifact_1.md", False,
        artifact1_forward_state_ok, artifact1_reverse_state_ok, ARTIFACT1_ANCHOR)
    if not ok_art:
        return 1

    print("\n========== DIFF PREVIEWS ==========")
    if not args.reverse:
        print(diff_preview_first_change(reg_orig, reg_sim, "capability_registry.metta (promoted from draft)", context=2))
    else:
        print("--- capability_registry.metta: WILL BE RESTORED FROM BACKUP ---")
    print()
    if not args.reverse:
        print("--- skill_discovery.metta: NEW FILE (%d lines) ---" % len(SKILL_DISCOVERY_CONTENT.splitlines()))
    else:
        print("--- skill_discovery.metta: WILL BE DELETED ---")
    print()
    print(diff_preview_first_change(lib_orig, lib_sim, "lib_clarity_reasoning.metta", context=2))
    print()
    print(diff_preview_first_change(loop_orig, loop_sim, "loop.metta", context=2))
    print()
    print(diff_preview_first_change(art_orig, art_sim, "artifact_1.md", context=1))

    if not args.apply:
        print("\n========== DRY-RUN COMPLETE ==========")
        print("All checks pass. Re-run with --apply to write%s." % (" the reverse" if args.reverse else ""))
        return 0

    # Forward: write backups (skill_discovery is new, no backup).
    if not args.reverse:
        for path, bak in [(REGISTRY_PATH, REGISTRY_BAK), (LIB_CR_PATH, LIB_CR_BAK),
                          (LOOP_PATH, LOOP_BAK), (ARTIFACT1_PATH, ARTIFACT1_BAK)]:
            if bak.exists():
                print("WARNING: backup %s exists; overwriting." % bak)
            bak.write_text(path.read_text())
            print("Backup written: %s" % bak)

    print("\n========== WRITING ==========")
    if args.reverse:
        if REGISTRY_BAK.exists():
            REGISTRY_PATH.write_text(REGISTRY_BAK.read_text())
            print("Restored from backup: %s" % REGISTRY_PATH)
        else:
            print("WARNING: no backup %s to restore capability_registry.metta from." % REGISTRY_BAK)
    else:
        REGISTRY_PATH.write_text(reg_sim)
        print("Wrote (promoted draft): %s" % REGISTRY_PATH)
    if args.reverse:
        if SKILL_PATH.exists():
            SKILL_PATH.unlink()
            print("Deleted: %s" % SKILL_PATH)
    else:
        SKILL_PATH.parent.mkdir(parents=True, exist_ok=True)
        SKILL_PATH.write_text(skill_content)
        print("Wrote: %s" % SKILL_PATH)
    LIB_CR_PATH.write_text(lib_sim)
    print("Wrote: %s" % LIB_CR_PATH)
    LOOP_PATH.write_text(loop_sim)
    print("Wrote: %s" % LOOP_PATH)
    ARTIFACT1_PATH.write_text(art_sim)
    print("Wrote: %s" % ARTIFACT1_PATH)

    print("\n========== DISK VERIFICATION ==========")
    all_ok = True
    # Change 0 (registry) verified on its own terms: forward expects the promoted
    # Path C content; reverse expects the restored backup.
    reg_disk = REGISTRY_PATH.read_text()
    if args.reverse:
        restored_match = REGISTRY_BAK.exists() and reg_disk == REGISTRY_BAK.read_text()
        print("  capability_registry.metta disk: restored-from-backup=%s (%s)"
              % (restored_match, "OK" if restored_match else "FAIL"))
        all_ok = all_ok and restored_match
    else:
        ok, msg = registry_disk_ok_forward(reg_disk)
        print("  capability_registry.metta disk: %s" % msg)
        all_ok = all_ok and ok
    for path, label, check_parens, fwd, rev in [
        (LIB_CR_PATH, "lib_clarity_reasoning.metta", True, lib_cr_forward_state_ok, lib_cr_reverse_state_ok),
        (LOOP_PATH, "loop.metta", True, loop_forward_state_ok, loop_reverse_state_ok),
        (ARTIFACT1_PATH, "artifact_1.md", False, artifact1_forward_state_ok, artifact1_reverse_state_ok),
    ]:
        disk = path.read_text()
        if check_parens:
            o, c = code_aware_paren_count(disk)
            dverdict = "OK" if o == c else "FAIL"
            print("  %s disk paren: opens=%d closes=%d delta=%d (%s)" % (label, o, c, o - c, dverdict))
            if o != c:
                all_ok = False
        # After forward the file should be in reverse-state; after reverse, forward-state.
        ok, msg = (fwd(disk) if args.reverse else rev(disk))
        print("  %s disk state: %s" % (label, msg))
        all_ok = all_ok and ok
    # skill_discovery disk check
    if args.reverse:
        sd_ok = not SKILL_PATH.exists()
        print("  skill_discovery.metta disk: absent=%s (%s)" % (sd_ok, "OK" if sd_ok else "FAIL"))
    else:
        sd_ok = SKILL_PATH.exists()
        if sd_ok:
            o, c = code_aware_paren_count(SKILL_PATH.read_text())
            sd_ok = (o == c)
            print("  skill_discovery.metta disk: present, paren delta=%d (%s)" % (o - c, "OK" if sd_ok else "FAIL"))
        else:
            print("  skill_discovery.metta disk: MISSING (FAIL)")
    all_ok = all_ok and sd_ok

    if not all_ok:
        print("\nDISK VERIFICATION FAILED. Restore from .bak.coda_phase_c backups.")
        return 1

    print("\n========== PHASE C %s COMPLETE ==========" % direction)
    if not args.reverse:
        print("All 5 changes applied. Next: rebuild + restart, then verify.")
        print("  docker compose build --no-cache clarityclaw && docker compose up -d clarityclaw")
        print("  python3 staging/verify_coda_phase_c_dispatch_result.py")
        print("  python3 staging/phase_d_coda_inloop_verification.py --mode verify")
    return 0


if __name__ == "__main__":
    sys.exit(main())
