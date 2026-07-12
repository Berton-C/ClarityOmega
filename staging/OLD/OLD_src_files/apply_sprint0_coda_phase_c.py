#!/usr/bin/env python3
"""
apply_sprint0_coda_phase_c.py

Sprint 0-Coda Phase C: wire the capability registry's skill-discovery dispatch
into the live loop. ONE reversible commit, five coordinated changes (Discipline 4)
plus the DIAG-CYCLE-DISPATCH marker.

  Change 0  soul/capability_registry.metta        copy certified Path C draft,
                                                  add run-chain dispatch-result write
  Change 1  soul/capabilities/skill_discovery.metta   new capability (handler + reg)
  Change 2  lib_clarity_reasoning/lib_clarity_reasoning.metta   two import lines
  Change 3  src/loop.metta                         getContext dispatch insertion + marker
  Change 4  docs/design/artifact_1_loop_metta_wiring_diagram.md   dispatch-insertion note

USAGE (run from repo root /PeTTa/repos/omegaclaw/):
  python3 apply_sprint0_coda_phase_c.py            # dry-run (default): shows the plan
  python3 apply_sprint0_coda_phase_c.py --apply    # write changes
  python3 apply_sprint0_coda_phase_c.py --reverse  # restore from backups

DISCIPLINE:
  - dry-run default; nothing written without --apply
  - content-anchored (no line numbers); any missing/ambiguous anchor ABORTS
    before a single byte is written (all-or-none)
  - per-file backup .bak.coda_phase_c ; --reverse restores them
  - paren-balance verified on every modified .metta file post-edit
  - surgical: touches only the five files above
"""

import os
import shutil
import sys

REPO = os.getcwd()
BAK = ".bak.coda_phase_c"

STAGING_DRAFT = "staging/capability_registry_path_c_draft.metta"
REGISTRY = "soul/capability_registry.metta"
SKILL_DISCOVERY = "soul/capabilities/skill_discovery.metta"
MANIFEST = "lib_clarity_reasoning/lib_clarity_reasoning.metta"
LOOP = "src/loop.metta"
ARTIFACT1 = "docs/design/artifact_1_loop_metta_wiring_diagram.md"

# ---------------------------------------------------------------------------
# Change 0: run-chain edit (anchored). OLD must be present verbatim in the
# staging draft; NEW wraps the existing (if ...) in a (progn ...) that writes
# the dispatch-result atom getContext reads. Wrapping a balanced (if ...) in a
# (progn <balanced-add-atom> <if>) preserves paren balance by construction.
# ---------------------------------------------------------------------------
RUNCHAIN_OLD = """                         (if (== $result decision-anchor)
                             (add-atom &self
                               (dispatch-chain-anchored
                                 invocation-id: $invocation-id
                                 anchor-handler: $handler))
                             (run-chain $tail $input-atom $invocation-id))"""

RUNCHAIN_NEW = """                         (progn
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

# ---------------------------------------------------------------------------
# Change 1: the new capability file (full content).
# ---------------------------------------------------------------------------
SKILL_DISCOVERY_CONTENT = """;; soul/capabilities/skill_discovery.metta
;; Sprint 0-Coda Phase C: first production capability (registration + handler).
;;
;; Option (a): the registry consultation is wired and structurally present, but
;; the emitted content is the existing hardcoded skill list (via getSkills), so
;; the LLM-facing content is unchanged while the dispatch path becomes its
;; source. Sprint 1 replaces format-skill-set's body with real
;; (registered-capability ...) formatting and retires getSkills after the
;; Phase D P-4 parity check holds.

;; --- Registration ---------------------------------------------------------
;; EXACTLY 5 fields, matching the dispatcher's canonical schema. A sixth field
;; (e.g. success-criterion) would break the 5-field matcher, so the
;; success-criterion is deferred to Phase B per the spec. Efficacy defaults to
;; 1.0 in the filter pipeline (>= 0.3), so no efficacy atom is needed to
;; dispatch; lifecycle: active is eligible; priority 100 establishes the scale.
(registered-capability
   schema: (skill-request cycle: $k)
   handler: skill-discovery
   priority: 100
   lifecycle: active
   metadata: ())

;; --- Handler --------------------------------------------------------------
;; Read-only against the atomspace; writes no atoms; returns one (skill-set ...).
;; It consults the active registered-capability atoms (structural presence of
;; the registry path) and emits the current skills via format-skill-set.
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

;; --- Formatter ------------------------------------------------------------
;; Option (a): emit the current hardcoded skills unchanged. getSkills is a pure
;; MeTTa function in src/skills.metta (no py-str, no Python boundary), so calling
;; it here is render-safe. $capabilities is consulted by the handler above but
;; does not yet drive content; Sprint 1 formats $capabilities here directly.
(= (format-skill-set $capabilities) (getSkills))
"""

# ---------------------------------------------------------------------------
# Change 2: manifest import lines (appended once, after an idempotency check).
# ---------------------------------------------------------------------------
MANIFEST_BLOCK = """
;; Capability Registry (Sprint 0 deliverable, wired by Sprint 0-Coda Phase C)
!(import! &self (library omegaclaw ./soul/capability_registry))

;; skill-discovery capability (Sprint 0-Coda first production registration)
!(import! &self (library omegaclaw ./soul/capabilities/skill_discovery))
"""
MANIFEST_SENTINEL = "./soul/capabilities/skill_discovery"

# ---------------------------------------------------------------------------
# Change 3: getContext insertion (anchored block replace).
# OLD is the current getContext body; NEW wraps it in a let* that fires
# dispatch, reads the dispatch-result skill-set, binds $skills-str and
# $skills-len, emits the DIAG-CYCLE-DISPATCH marker, and substitutes
# $skills-str for (getSkills) in the prompt. getSkills DEFINITION is untouched
# (it stays callable in src/skills.metta for Phase D parity).
# ---------------------------------------------------------------------------
GETCONTEXT_OLD = """(= (getContext $k)
   (string-safe (py-str ("PROMPT: " (getPrompt) " SKILLS: " (getSkills)
                         " " (output-format-guidance)
                         " YOUR_LAST_ACTION: " (your-last-action-block $k)
                         " " (task-state-block)
                         " " (idle-pattern-block)
                         " " (agency-balance-block)
                         " LAST_SKILL_USE_RESULTS: " (last_chars (get-state &lastresults) (maxFeedback)) " HISTORY: " (getHistory) " TIME: " (get_time_as_string)))))"""

GETCONTEXT_NEW = """(= (getContext $k)
   (let* (($_dispatch (dispatch (skill-request cycle: $k) $k))
          ($results (collapse (match &self (dispatch-result invocation-id: $_id result: (skill-set skills: $s) handler: $_h) $s)))
          ($skills-str (car-atom $results))
          ($skills-len (string_length $skills-str))
          ($_marker (println! (DIAG-CYCLE-DISPATCH invocation-id: $k skills-len: $skills-len))))
     (string-safe (py-str ("PROMPT: " (getPrompt) " SKILLS: " $skills-str
                         " " (output-format-guidance)
                         " YOUR_LAST_ACTION: " (your-last-action-block $k)
                         " " (task-state-block)
                         " " (idle-pattern-block)
                         " " (agency-balance-block)
                         " LAST_SKILL_USE_RESULTS: " (last_chars (get-state &lastresults) (maxFeedback)) " HISTORY: " (getHistory) " TIME: " (get_time_as_string))))))"""

# ---------------------------------------------------------------------------
# Change 4: artifact_1 dispatch-insertion note (appended once).
# Scoped to documenting the new hook; the broader line-number drift sweep is
# noted as a follow-up rather than attempted blind in this commit.
# ---------------------------------------------------------------------------
ARTIFACT1_BLOCK = """

## Sprint 0-Coda Phase C: capability-registry dispatch insertion (getContext)

Added by Sprint 0-Coda Phase C (see docs/design/sprint_0_coda_phase_a_v6.md).

Phase 4.3 (prompt assembly), getContext. getContext now opens with a let* that,
each cycle, fires the capability registry before assembling the prompt:

- CALLS: (dispatch (skill-request cycle: $k) $k). invocation-id is the loop
  iteration $k (monotonic, distinct per cycle; no counter atom).
- READS: (dispatch-result invocation-id: $_ result: (skill-set skills: $s)
  handler: $_), binding the skills string $s; $skills-str = (car-atom $results).
- WRITES (via dispatch -> run-chain): dispatch-invocation, capability-invoked,
  dispatch-result, and dispatch-chain-exhausted / dispatch-chain-anchored /
  dispatch-fallback-activated per the chain outcome.
- EMITS: (DIAG-CYCLE-DISPATCH invocation-id: $k skills-len: <int>) every cycle,
  for the Phase D in-loop verification (P-2 distinct id, P-3 non-empty payload,
  P-4 parity against the retained getSkills length).
- SUBSTITUTES $skills-str for (getSkills) in the SKILLS slot of the prompt.
  The getSkills DEFINITION remains callable in src/skills.metta until Phase D
  Criterion P-4 confirms parity; its removal is a separate later commit.
- NETWORK: SN (capability selection / skills surfacing).

NOTE (follow-up, not done in this commit): the broader line-number drift fix
across this document (diagnostic-print and Phase-1-merge drift) is deferred to a
dedicated housekeeping pass to avoid a blind large-scale edit here.
"""
ARTIFACT1_SENTINEL = "Sprint 0-Coda Phase C: capability-registry dispatch insertion"


# ===========================================================================
# Mechanics
# ===========================================================================
def fail(msg):
    print("ABORT: " + msg)
    sys.exit(1)


def read(path):
    with open(path, "r", encoding="utf-8") as f:
        return f.read()


def write(path, text):
    os.makedirs(os.path.dirname(path) or ".", exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        f.write(text)


def paren_balance(text, path):
    o = text.count("(")
    c = text.count(")")
    if o != c:
        fail("paren imbalance in %s after edit: %d '(' vs %d ')'" % (path, o, c))


def require(path):
    if not os.path.exists(path):
        fail("expected file missing: %s" % path)


def require_once(text, anchor, path, label):
    n = text.count(anchor)
    if n == 0:
        fail("%s anchor not found in %s (file may have drifted)" % (label, path))
    if n > 1:
        fail("%s anchor not unique in %s (%d matches)" % (label, n, path))


# ---- preflight: verify every anchor before writing anything (all-or-none) ----
def preflight():
    for p in [STAGING_DRAFT, MANIFEST, LOOP, ARTIFACT1]:
        require(p)
    draft = read(STAGING_DRAFT)
    require_once(draft, RUNCHAIN_OLD, STAGING_DRAFT, "Change 0 run-chain")
    if "dispatch-result" in draft:
        fail("Change 0: staging draft already contains 'dispatch-result' "
             "(already patched?). Refusing to double-apply.")
    loop = read(LOOP)
    require_once(loop, GETCONTEXT_OLD, LOOP, "Change 3 getContext")
    if os.path.exists(SKILL_DISCOVERY):
        fail("Change 1: %s already exists. Refusing to overwrite." % SKILL_DISCOVERY)
    man = read(MANIFEST)
    if MANIFEST_SENTINEL in man:
        fail("Change 2: manifest already imports skill_discovery. Already applied?")
    print("Preflight OK: all five anchors present and unambiguous; no prior application detected.")
    return draft, loop, man


def backup(path):
    if os.path.exists(path):
        shutil.copy2(path, path + BAK)


def do_apply():
    draft, loop, man = preflight()

    # Change 0: certified draft -> registry, then the run-chain dispatch-result write.
    backup(REGISTRY)
    new_registry = draft.replace(RUNCHAIN_OLD, RUNCHAIN_NEW)
    if new_registry.count("dispatch-result") != 1:
        fail("Change 0: expected exactly one 'dispatch-result' after edit, got %d"
             % new_registry.count("dispatch-result"))
    paren_balance(new_registry, REGISTRY)
    write(REGISTRY, new_registry)
    print("Change 0: wrote %s (Path C draft + run-chain dispatch-result write)." % REGISTRY)

    # Change 1: new capability file.
    paren_balance(SKILL_DISCOVERY_CONTENT, SKILL_DISCOVERY)
    write(SKILL_DISCOVERY, SKILL_DISCOVERY_CONTENT)
    print("Change 1: wrote %s." % SKILL_DISCOVERY)

    # Change 2: append imports.
    backup(MANIFEST)
    write(MANIFEST, man.rstrip("\n") + "\n" + MANIFEST_BLOCK)
    print("Change 2: appended registry + skill_discovery imports to %s." % MANIFEST)

    # Change 3: getContext insertion.
    backup(LOOP)
    new_loop = loop.replace(GETCONTEXT_OLD, GETCONTEXT_NEW)
    paren_balance(new_loop, LOOP)
    write(LOOP, new_loop)
    print("Change 3: wired dispatch + DIAG-CYCLE-DISPATCH marker into getContext in %s." % LOOP)

    # Change 4: artifact_1 note.
    backup(ARTIFACT1)
    art = read(ARTIFACT1)
    if ARTIFACT1_SENTINEL not in art:
        write(ARTIFACT1, art.rstrip("\n") + "\n" + ARTIFACT1_BLOCK)
        print("Change 4: appended dispatch-insertion section to %s." % ARTIFACT1)
    else:
        print("Change 4: section already present; skipped.")

    print("\nAPPLIED. Next: rebuild (docker compose build --no-cache clarityclaw), "
          "restart, then run the verify script.")


def do_reverse():
    restored = 0
    for path in [REGISTRY, MANIFEST, LOOP, ARTIFACT1]:
        b = path + BAK
        if os.path.exists(b):
            shutil.copy2(b, path)
            os.remove(b)
            restored += 1
            print("Reversed: restored %s" % path)
    if os.path.exists(SKILL_DISCOVERY):
        os.remove(SKILL_DISCOVERY)
        print("Reversed: removed %s" % SKILL_DISCOVERY)
    # remove the registry backup created when REGISTRY did not pre-exist is N/A;
    # if soul/capabilities is now empty, leave the dir (harmless).
    if restored == 0 and not os.path.exists(SKILL_DISCOVERY + BAK):
        print("Nothing to reverse (no backups found).")
    else:
        print("Reverse complete.")


def do_dryrun():
    draft, loop, man = preflight()
    print("\nDRY-RUN plan (no files written). Run with --apply to execute.\n")
    print("Change 0  %s" % REGISTRY)
    print("          copy %s, wrap run-chain (if ...) in (progn (add-atom dispatch-result ...) (if ...))" % STAGING_DRAFT)
    print("Change 1  %s  (new file, %d lines)" % (SKILL_DISCOVERY, SKILL_DISCOVERY_CONTENT.count(chr(10))))
    print("Change 2  %s  (+2 import lines)" % MANIFEST)
    print("Change 3  %s  (getContext: +let* dispatch/read/marker, getSkills -> $skills-str)" % LOOP)
    print("Change 4  %s  (+dispatch-insertion section)" % ARTIFACT1)
    # Paren preview on the would-be results.
    paren_balance(draft.replace(RUNCHAIN_OLD, RUNCHAIN_NEW), REGISTRY + " (preview)")
    paren_balance(loop.replace(GETCONTEXT_OLD, GETCONTEXT_NEW), LOOP + " (preview)")
    paren_balance(SKILL_DISCOVERY_CONTENT, SKILL_DISCOVERY + " (preview)")
    print("\nParen-balance preview passed on all three .metta results.")


if __name__ == "__main__":
    if REPO.rstrip("/").split("/")[-1] not in ("omegaclaw",) and not os.path.exists(STAGING_DRAFT):
        fail("run from repo root (expected %s to exist)" % STAGING_DRAFT)
    arg = sys.argv[1] if len(sys.argv) > 1 else "--dry-run"
    if arg == "--apply":
        do_apply()
    elif arg == "--reverse":
        do_reverse()
    elif arg == "--dry-run":
        do_dryrun()
    else:
        fail("unknown arg %r (use --dry-run | --apply | --reverse)" % arg)
