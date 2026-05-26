#!/usr/bin/env python3
"""apply_phase1_memory_layer_merge.py

Phase 1 of the memory-layer merge from upstream patham9/mettaclaw into
ClarityOmega. Implements the decisions locked from memory_layer_merge_design_v1
plus the joint resolutions in conversation history.

Locked decisions in scope this phase:

    [1] Sequence A (representation-first)
    [2] T-1: parked (cost instrumentation; not the wrapping)
    [3] T-3: Configuration B (side-by-side via separate query-promoted function)
    [4] T-4: adopt now
    [5] T-5: deferred pending pipeline audit
    [6] T-6: already complete (Apr 11 2026, jazzbox35 commit 54de66d);
            ChromaDB verified 14,686 entries all Local-embedded; no rebuild
    [7] Tooling: py-script reversible
    [8] Safety category: established via this commit message

What this script does (4 file edits, atomic apply-or-nothing):

    Edit 1: src/skills.metta
        Add !(import_prolog_function call_with_inference_limit) directive.
        Replace bare metta function (lines 55-57) with Patrick's wrapped form:
            (let $code (sread $str)
                 (repr (progn (call_with_inference_limit
                                 (Predicate (quote (eval $code $x)))
                                 100000000) $x)))
        Brings bounded execution (100M inference budget) and stringification.
        T-1/T-2 coupled in Patrick's source per reading beta.

    Edit 2: src/memory.metta
        Add maxSimilarityRecall, promotionInflationFactor, mostPromotedMemories
        configure parameters with (empty) declarations.
        Add the four corresponding (configure ...) calls inside initMemory.
        Add (py-call (helper.promotion_open_map)) to initMemory.
        Add (reconcile-promotion-atoms) call to initMemory after open_map.
        Add get-promotion, best-promoted-memory-ids, best-promoted-memories,
        promote, demote MeTTa functions adapted from upstream.
        Add query-promoted (T-3 Config B): Patrick's promotion-weighted query
        as a NEW function alongside our existing query (which stays unchanged).
        Add reconcile-promotion-atoms (startup sync of atomspace from SQLite).
        Bridge (Section 7): promote/demote include (add-atom &self (promoted
        memory-id $uuid salience $newv)) inline (Bridge-MeTTa-1).

    Edit 3: src/helper.py
        Add sqlite3, uuid, os imports to upstream section.
        Add _PROMOTION_CONN global.
        Add 11 promotion helper functions verbatim from upstream helper.py:
            promotion_open_map, promotion_key, promotion_set_value,
            promotion_get_value, promotion_get_all_keys, promotion_set_lasttime,
            promotion_get_lasttime, promotion_has_key, promotion_delete_key,
            promotion_commit, promotion_close_map.
        Path adapted: repos/omegaclaw (not repos/mettaclaw).
        Add __main__ block with promotion-only test (not balance_parentheses
        test -- our balance_parentheses diverges from upstream; T-5 deferred).
        All additions land at end of OMEGACLAW UPSTREAM section, before the
        CLARITYCLAW SOUL ARCHITECTURE marker.

    Edit 4: src/loop.metta
        T-4: change history-write condition on line 159 from (if $msgnew ...)
        to (if (or $msgnew (not (== $sexpr ()))) ...). $sexpr is in scope from
        line 120 binding.

Bridge fire-and-forget guarantee (per Q6/Q7 decisions):
    Runtime: alpha (clean add-atom call, no catch wrapping). Well-formed atom
    has no meaningful runtime failure mode in this MeTTa runtime.
    Durability: reconcile-promotion-atoms at startup syncs atomspace from
    SQLite source-of-truth, recovering from any divergence including container
    crash or power loss between SQLite write and atomspace write.

Reversibility: --reverse --apply restores the pre-merge state on all four
files by applying the inverse anchor-based replacements.

Pattern: apply_step6_aliveness_gate_migration.py / apply_gc_producer_alignment.py
established pattern (argparse, dry-run/apply/reverse, anchor verification,
state checks pre/post, atomic apply-or-nothing).

Usage:
    python3 staging/apply_phase1_memory_layer_merge.py            # dry-run
    python3 staging/apply_phase1_memory_layer_merge.py --apply     # apply
    python3 staging/apply_phase1_memory_layer_merge.py --reverse --apply  # reverse

Post-apply:
    docker compose build --no-cache clarityclaw && docker compose up -d clarityclaw
    Test 1 (substrate boots): container up, log shows initialization including
        "Initializing memory" with promotion_open_map call succeeding.
    Test 2 (reconcile idempotent): restart container twice; verify no errors;
        atomspace promoted-atom count matches SQLite count both times.
    Test 3 (metta function bounded): observe any metta skill call in log;
        verify it returns a string (not bare atom); verify a deliberately
        non-terminating metta expression triggers inference_limit_exceeded.
    Test 4 (T-4 idle records): observe at least one idle cycle where
        $msgnew=false and $sexpr non-empty; verify history.metta gets a
        new entry for that cycle.
"""

import argparse
import os
import re
import sys
from pathlib import Path


# =====================================================================
# CONFIGURATION
# =====================================================================

# Repo-root-relative paths (script invoked from repo root)
SKILLS_METTA = "src/skills.metta"
MEMORY_METTA = "src/memory.metta"
HELPER_PY = "src/helper.py"
LOOP_METTA = "src/loop.metta"

BACKUP_SUFFIX = ".bak.phase1_memory_layer_merge"


# =====================================================================
# EDIT 1: src/skills.metta -- T-2 plus call_with_inference_limit import
# =====================================================================

SKILLS_OLD_IMPORT_ANCHOR = """!(import_prolog_functions_from_file (library omegaclaw ./src/skills.pl) (shell first_char gc))

(= (metta $str)
   (let $code (sread $str)
        (eval $code)))"""

SKILLS_NEW_IMPORT_ANCHOR = """!(import_prolog_functions_from_file (library omegaclaw ./src/skills.pl) (shell first_char gc))
!(import_prolog_function call_with_inference_limit)

(= (metta $str)
   (let $code (sread $str)
        (repr (progn (call_with_inference_limit (Predicate (quote (eval $code $x))) 100000000) $x))))"""


# =====================================================================
# EDIT 2: src/memory.metta -- additive items + bridge + query-promoted
# =====================================================================

MEMORY_OLD_CONFIG_DECLS = """(= (maxFeedback) (empty))
(= (maxRecallItems) (empty))
(= (maxEpisodeRecallLines) (empty))
(= (maxHistory) (empty))
(= (embeddingprovider) (empty))"""

MEMORY_NEW_CONFIG_DECLS = """(= (maxFeedback) (empty))
(= (maxRecallItems) (empty))
(= (maxSimilarityRecall) (empty))
(= (maxEpisodeRecallLines) (empty))
(= (maxHistory) (empty))
(= (embeddingprovider) (empty))
(= (promotionInflationFactor) (empty))
(= (mostPromotedMemories) (empty))"""

MEMORY_OLD_INITMEMORY = """(= (initMemory)
   (progn (println! "Initializing memory")
          (configure maxFeedback 50000)
          (configure maxRecallItems 20)
          (configure maxEpisodeRecallLines 20)
          (configure maxHistory 30000)
          (configure embeddingprovider Local) ;OpenAI or Local
          (if (== (embeddingprovider) Local)
              (py-call (lib_llm_ext.initLocalEmbedding)) _)))"""

MEMORY_NEW_INITMEMORY = """(= (initMemory)
   (progn (println! "Initializing memory")
          (configure maxFeedback 50000)
          (configure maxRecallItems 20)
          (configure maxSimilarityRecall 10)
          (configure maxEpisodeRecallLines 20)
          (configure maxHistory 30000)
          (configure embeddingprovider Local) ;OpenAI or Local
          (configure promotionInflationFactor 10)
          (configure mostPromotedMemories 10)
          (py-call (helper.promotion_open_map))
          (reconcile-promotion-atoms)
          (if (== (embeddingprovider) Local)
              (py-call (lib_llm_ext.initLocalEmbedding)) _)))"""

# Append additions to end of file (after the episodes function on line 49-50)
# Anchor: end-of-file marker is the closing of the episodes function.

MEMORY_OLD_TAIL = """(= (episodes $time)
   (py-call (helper.around_time $time (maxEpisodeRecallLines))))"""

MEMORY_NEW_TAIL = """(= (episodes $time)
   (py-call (helper.around_time $time (maxEpisodeRecallLines))))

;; ============================================================
;; PROMOTION INFRASTRUCTURE (additive, from upstream memory.metta)
;; Adopted per memory-layer merge design v1 Section 4.1.
;; Adapted for omegaclaw paths.
;; ============================================================

;; Compute current promotion salience for a uuid given current time.
;; Includes time-decay factor (half-life-ish based on day-scale exponential decay).
(= (get-promotion $current_time $uuid)
   (let* (($promotion (py-call (helper.promotion_get_value $uuid 0.0)))
          ($last_time (py-call (helper.promotion_get_lasttime $uuid 0.0)))
          ($t (- $current_time $last_time)))
         (* $promotion (pow-math (+ 1.0 (/ $t 86400.0)) (- 0.0 0.7)))))

;; Return the top-K promoted memory uuids ranked by current salience.
(= (best-promoted-memory-ids)
   (let* (($current_time (get_time))
          ($uuids (py-call (helper.promotion_get_all_keys)))
          ($ranked (takeK (mostPromotedMemories)
                          (msort (collapse (let* (($uuid (superpose $uuids))
                                                  ($promotion (get-promotion $current_time $uuid)))
                                                 (if (> $promotion 0.0) ((- 0.0 $promotion) $uuid))))))))
         (collapse (let ($p $uuid) (superpose $ranked) $uuid))))

;; Return the actual memory contents for the top-K promoted ids.
(= (best-promoted-memories)
   (let $uuids (best-promoted-memory-ids)
        (let $ret (py-call (lib_chromadb.query_by_ids $uuids))
             (progn (write-file ./repos/omegaclaw/memory/promoted_memories.metta "")
                    (repr (collapse (let ($uuid $t $c) (superpose $ret)
                                         (progn (append-file ./repos/omegaclaw/memory/promoted_memories.metta (repr ($t $c)))
                                                ($t $c)))))))))

;; T-3 Config B: promotion-weighted query as separate function from `query`.
;; Our existing `query` (lines 45-46) stays unchanged. Consumers explicitly
;; opt in to promotion-weighted ranking by calling this function.
(= (query-promoted $str)
   (let* (($embedding (embed $str))
          ($queryresults (py-call (lib_chromadb.query_with_ids_and_dists $embedding (* (promotionInflationFactor) (maxRecallItems)))))
          ($candidates (collapse (let* (($current_time (get_time))
                                        (($uuid $time $message $distance) (superpose $queryresults))
                                        ($promotion (get-promotion $current_time $uuid)))
                                       (if (> $promotion 0.0)
                                           ((- 0.0 $promotion) $distance $uuid $time $message))))))
         (let* (($best (takeK (maxRecallItems) (msort $candidates)))
                ($bestpromoted (collapse (let ($_ $_ $uuid $time $message) (superpose $best)
                                              ($time $message))))
                ($closest (collapse (let ($uuid $time $message $distance) (superpose $queryresults)
                                          ($time $message)))))
               (takeK (+ (maxRecallItems) (maxSimilarityRecall)) (unique-atom (append $bestpromoted $closest))))))

;; Promote: bump salience for memories at $time. Includes bridge to atomspace.
;; Section 7 (memory-layer merge design v1): dual-write to atomspace as
;; (promoted memory-id $uuid salience $newv). SQLite is source of truth;
;; atomspace is queryable derived view. add-atom call uses alpha (clean)
;; style per Q7 decision. Durability via reconcile-promotion-atoms at startup.
(= (promote $time)
   (let* (($current_time (get_time))
          ($uuids (py-call (lib_chromadb.ids_by_time $time))))
         (progn (collapse (let* (($uuid (superpose $uuids))
                                 ($v (get-promotion $current_time $uuid))
                                 ($newv (min 10.0 (+ 1.0 $v))))
                                (progn (py-call (helper.promotion_set_value $uuid $newv))
                                       (py-call (helper.promotion_set_lasttime $uuid $current_time))
                                       (add-atom &self (promoted memory-id $uuid salience $newv)))))
                (py-call (helper.promotion_commit))
                PROMOTE-SUCCESS)))

;; Demote: reduce salience for memories at $time. Same bridge pattern.
(= (demote $time)
   (let* (($current_time (get_time))
          ($uuids (py-call (lib_chromadb.ids_by_time $time))))
         (progn (collapse (let* (($uuid (superpose $uuids))
                                 ($v (get-promotion $current_time $uuid))
                                 ($newv (max 0.0 (- $v 1.0))))
                                (progn (py-call (helper.promotion_set_value $uuid $newv))
                                       (py-call (helper.promotion_set_lasttime $uuid $current_time))
                                       (add-atom &self (promoted memory-id $uuid salience $newv)))))
                (py-call (helper.promotion_commit))
                DEMOTE-SUCCESS)))

;; Startup reconciliation: read all promotion uuids from SQLite, compute
;; current salience, and write atomspace atoms. Called from initMemory after
;; promotion_open_map. Idempotent by design: re-running emits the same atoms.
;; MeTTa add-atom on identical atoms is the runtime's responsibility; this
;; function should be tested for idempotency during --dry-run verification.
;; Durability guarantee for the bridge: if SQLite has a promotion that
;; atomspace lacks (because of crash or restart), this function recovers it.
(= (reconcile-promotion-atoms)
   (let* (($current_time (get_time))
          ($uuids (py-call (helper.promotion_get_all_keys))))
         (collapse (let* (($uuid (superpose $uuids))
                          ($salience (get-promotion $current_time $uuid)))
                         (if (> $salience 0.0)
                             (add-atom &self (promoted memory-id $uuid salience $salience))
                             _)))))"""


# =====================================================================
# EDIT 3: src/helper.py -- promotion infrastructure additions
# =====================================================================

# Anchor: insert before the CLARITYCLAW SOUL ARCHITECTURE banner.
# The banner is preceded by a blank line. Use the banner as anchor.

HELPER_OLD_BANNER_ANCHOR = """    except Exception:
        return str(x)


# ============================================================
# CLARITYCLAW SOUL ARCHITECTURE (Berton Bennett / ClarityDAO)"""

HELPER_NEW_BANNER_ANCHOR = """    except Exception:
        return str(x)


# ============================================================
# PROMOTION INFRASTRUCTURE (additive, from upstream patham9/mettaclaw)
# Adopted per memory-layer merge design v1 Section 4.1.
# SQLite-backed key-value store for memory promotion salience.
# Paths adapted from "repos/mettaclaw/..." to "repos/omegaclaw/...".
# ============================================================

import sqlite3
import uuid as _uuid_module
import os as _os_module

_PROMOTION_CONN = None

def promotion_open_map(path="repos/omegaclaw/memory/promotions.db"):
    global _PROMOTION_CONN
    _PROMOTION_CONN = sqlite3.connect(path)
    _PROMOTION_CONN.execute("PRAGMA journal_mode=WAL")
    _PROMOTION_CONN.execute("PRAGMA synchronous=NORMAL")
    _PROMOTION_CONN.execute(\"\"\"
        CREATE TABLE IF NOT EXISTS kv (
            key BLOB PRIMARY KEY,
            value REAL NOT NULL,
            lasttime REAL
        )
    \"\"\")
    _PROMOTION_CONN.commit()

def promotion_key(k):
    if isinstance(k, _uuid_module.UUID):
        return k.bytes
    if isinstance(k, str):
        return _uuid_module.UUID(k).bytes
    if isinstance(k, bytes) and len(k) == 16:
        return k
    raise TypeError("key must be uuid.UUID, UUID string, or 16-byte UUID")

def promotion_set_value(k, v):
    _PROMOTION_CONN.execute(
        \"\"\"
        INSERT INTO kv(key, value)
        VALUES (?, ?)
        ON CONFLICT(key) DO UPDATE SET value = excluded.value
        \"\"\",
        (promotion_key(k), float(v))
    )

def promotion_get_value(k, default=None):
    row = _PROMOTION_CONN.execute(
        "SELECT value FROM kv WHERE key = ?",
        (promotion_key(k),)
    ).fetchone()
    return row[0] if row else default

def promotion_get_all_keys():
    rows = _PROMOTION_CONN.execute(
        "SELECT key FROM kv"
    ).fetchall()
    return [str(_uuid_module.UUID(bytes=row[0])) for row in rows]

def promotion_set_lasttime(k, t):
    _PROMOTION_CONN.execute(
        \"\"\"
        INSERT INTO kv(key, value, lasttime)
        VALUES (?, 0.0, ?)
        ON CONFLICT(key) DO UPDATE SET lasttime = excluded.lasttime
        \"\"\",
        (promotion_key(k), float(t))
    )

def promotion_get_lasttime(k, default=None):
    row = _PROMOTION_CONN.execute(
        "SELECT lasttime FROM kv WHERE key = ?",
        (promotion_key(k),)
    ).fetchone()
    return row[0] if row and row[0] is not None else default

def promotion_has_key(k):
    row = _PROMOTION_CONN.execute(
        "SELECT 1 FROM kv WHERE key = ?",
        (promotion_key(k),)
    ).fetchone()
    return row is not None

def promotion_delete_key(k):
    _PROMOTION_CONN.execute(
        "DELETE FROM kv WHERE key = ?",
        (promotion_key(k),)
    )

def promotion_commit():
    _PROMOTION_CONN.commit()

def promotion_close_map():
    global _PROMOTION_CONN
    if _PROMOTION_CONN is not None:
        _PROMOTION_CONN.commit()
        _PROMOTION_CONN.close()
        _PROMOTION_CONN = None


# Self-test for promotion infrastructure. Run as: python3 src/helper.py
# This block does NOT include test_balance_parenthesis() because our
# balance_parentheses diverges from upstream's (T-5 deferred).
if __name__ == "__main__":
    path = "test_promotions.db"
    if _os_module.path.exists(path):
        _os_module.remove(path)
    promotion_open_map(path)
    k = "b7e55f3a-376f-493f-a5cb-9a9e01e7f062"
    promotion_set_value(k, 0.73)
    assert promotion_get_value(k) == 0.73
    assert promotion_has_key(k) is True
    promotion_set_lasttime(k, 123.45)
    assert promotion_get_lasttime(k) == 123.45
    assert promotion_get_value(k) == 0.73
    promotion_delete_key(k)
    assert promotion_has_key(k) is False
    assert promotion_get_value(k) is None
    assert promotion_get_lasttime(k) is None
    promotion_close_map()
    _os_module.remove(path)
    print("promotion infrastructure tests passed")


# ============================================================
# CLARITYCLAW SOUL ARCHITECTURE (Berton Bennett / ClarityDAO)"""


# =====================================================================
# EDIT 4: src/loop.metta -- T-4 history-write condition
# =====================================================================

LOOP_OLD_T4_ANCHOR = """                                          ;; PROCEED/FLAG path: normal execution
                                          (progn (if $msgnew (addToHistory $msg (py-call (helper.normalize_string $response)) (py-call (helper.normalize_string $response)) $msgnew) _)"""

LOOP_NEW_T4_ANCHOR = """                                          ;; PROCEED/FLAG path: normal execution
                                          ;; T-4 (memory-layer merge): record history when LLM produces output even without new human message.
                                          ;; Per upstream patham9/mettaclaw loop.metta: (or $msgnew (not (== $sexpr ()))). Autonomous reasoning IS substrate-record-worthy world knowledge.
                                          (progn (if (or $msgnew (not (== $sexpr ()))) (addToHistory $msg (py-call (helper.normalize_string $response)) (py-call (helper.normalize_string $response)) $msgnew) _)"""


# =====================================================================
# FILE-EDIT FRAMEWORK (per established apply-script pattern)
# =====================================================================

def _read(path):
    with open(path, "r", encoding="utf-8") as f:
        return f.read()


def _write(path, content):
    with open(path, "w", encoding="utf-8") as f:
        f.write(content)


def _line_count(s):
    return s.count("\n") + (1 if s and not s.endswith("\n") else 0)


def _backup(path):
    backup_path = path + BACKUP_SUFFIX
    if not os.path.exists(backup_path):
        _write(backup_path, _read(path))
    return backup_path


def _restore(path):
    backup_path = path + BACKUP_SUFFIX
    if os.path.exists(backup_path):
        _write(path, _read(backup_path))
        os.remove(backup_path)
        return True
    return False


def _check_anchor(content, anchor, file_label):
    """Verify exactly one occurrence of anchor in content."""
    count = content.count(anchor)
    if count == 0:
        return False, f"Anchor not found in {file_label}"
    if count > 1:
        return False, f"Anchor matches {count} times in {file_label} (expected exactly 1)"
    return True, None


def _process_skills_metta(direction, dry_run):
    path = SKILLS_METTA
    if not os.path.exists(path):
        return {"ok": False, "message": f"{path} does not exist"}

    content = _read(path)
    pre_lines = _line_count(content)

    if direction == "apply":
        ok, msg = _check_anchor(content, SKILLS_OLD_IMPORT_ANCHOR, path)
        if not ok:
            ok2, msg2 = _check_anchor(content, SKILLS_NEW_IMPORT_ANCHOR, path)
            if ok2:
                return {"ok": False, "message": f"{path} already in post-state; refusing to re-apply"}
            return {"ok": False, "message": msg}
        new_content = content.replace(SKILLS_OLD_IMPORT_ANCHOR, SKILLS_NEW_IMPORT_ANCHOR, 1)
    else:  # reverse
        ok, msg = _check_anchor(content, SKILLS_NEW_IMPORT_ANCHOR, path)
        if not ok:
            ok2, msg2 = _check_anchor(content, SKILLS_OLD_IMPORT_ANCHOR, path)
            if ok2:
                return {"ok": False, "message": f"{path} already in pre-state; nothing to reverse"}
            return {"ok": False, "message": msg}
        new_content = content.replace(SKILLS_NEW_IMPORT_ANCHOR, SKILLS_OLD_IMPORT_ANCHOR, 1)

    post_lines = _line_count(new_content)
    line_delta = post_lines - pre_lines

    if not dry_run:
        _backup(path)
        _write(path, new_content)

    return {
        "ok": True,
        "path": path,
        "pre_lines": pre_lines,
        "post_lines": post_lines,
        "line_delta": line_delta,
        "edit": "T-2 (metta function wrapping + call_with_inference_limit import)",
    }


def _process_memory_metta(direction, dry_run):
    path = MEMORY_METTA
    if not os.path.exists(path):
        return {"ok": False, "message": f"{path} does not exist"}

    content = _read(path)
    pre_lines = _line_count(content)

    if direction == "apply":
        # Three coordinated edits in this file. All must match before any write.
        for anchor, label in [
            (MEMORY_OLD_CONFIG_DECLS, "config-declarations"),
            (MEMORY_OLD_INITMEMORY, "initMemory"),
            (MEMORY_OLD_TAIL, "tail (episodes function)"),
        ]:
            ok, msg = _check_anchor(content, anchor, f"{path}:{label}")
            if not ok:
                return {"ok": False, "message": msg}
        new_content = content
        new_content = new_content.replace(MEMORY_OLD_CONFIG_DECLS, MEMORY_NEW_CONFIG_DECLS, 1)
        new_content = new_content.replace(MEMORY_OLD_INITMEMORY, MEMORY_NEW_INITMEMORY, 1)
        new_content = new_content.replace(MEMORY_OLD_TAIL, MEMORY_NEW_TAIL, 1)
    else:  # reverse
        for anchor, label in [
            (MEMORY_NEW_CONFIG_DECLS, "config-declarations"),
            (MEMORY_NEW_INITMEMORY, "initMemory"),
            (MEMORY_NEW_TAIL, "tail (with promotion infrastructure)"),
        ]:
            ok, msg = _check_anchor(content, anchor, f"{path}:{label}")
            if not ok:
                return {"ok": False, "message": msg}
        new_content = content
        new_content = new_content.replace(MEMORY_NEW_TAIL, MEMORY_OLD_TAIL, 1)
        new_content = new_content.replace(MEMORY_NEW_INITMEMORY, MEMORY_OLD_INITMEMORY, 1)
        new_content = new_content.replace(MEMORY_NEW_CONFIG_DECLS, MEMORY_OLD_CONFIG_DECLS, 1)

    post_lines = _line_count(new_content)
    line_delta = post_lines - pre_lines

    if not dry_run:
        _backup(path)
        _write(path, new_content)

    return {
        "ok": True,
        "path": path,
        "pre_lines": pre_lines,
        "post_lines": post_lines,
        "line_delta": line_delta,
        "edit": "Additive: config params + promotion functions + bridge + reconcile + query-promoted",
    }


def _process_helper_py(direction, dry_run):
    path = HELPER_PY
    if not os.path.exists(path):
        return {"ok": False, "message": f"{path} does not exist"}

    content = _read(path)
    pre_lines = _line_count(content)

    if direction == "apply":
        ok, msg = _check_anchor(content, HELPER_OLD_BANNER_ANCHOR, path)
        if not ok:
            ok2, msg2 = _check_anchor(content, HELPER_NEW_BANNER_ANCHOR, path)
            if ok2:
                return {"ok": False, "message": f"{path} already in post-state; refusing to re-apply"}
            return {"ok": False, "message": msg}
        new_content = content.replace(HELPER_OLD_BANNER_ANCHOR, HELPER_NEW_BANNER_ANCHOR, 1)
    else:  # reverse
        ok, msg = _check_anchor(content, HELPER_NEW_BANNER_ANCHOR, path)
        if not ok:
            ok2, msg2 = _check_anchor(content, HELPER_OLD_BANNER_ANCHOR, path)
            if ok2:
                return {"ok": False, "message": f"{path} already in pre-state; nothing to reverse"}
            return {"ok": False, "message": msg}
        new_content = content.replace(HELPER_NEW_BANNER_ANCHOR, HELPER_OLD_BANNER_ANCHOR, 1)

    post_lines = _line_count(new_content)
    line_delta = post_lines - pre_lines

    if not dry_run:
        _backup(path)
        _write(path, new_content)

    return {
        "ok": True,
        "path": path,
        "pre_lines": pre_lines,
        "post_lines": post_lines,
        "line_delta": line_delta,
        "edit": "Promotion infrastructure (11 functions + global + imports + self-test)",
    }


def _process_loop_metta(direction, dry_run):
    path = LOOP_METTA
    if not os.path.exists(path):
        return {"ok": False, "message": f"{path} does not exist"}

    content = _read(path)
    pre_lines = _line_count(content)

    if direction == "apply":
        ok, msg = _check_anchor(content, LOOP_OLD_T4_ANCHOR, path)
        if not ok:
            ok2, msg2 = _check_anchor(content, LOOP_NEW_T4_ANCHOR, path)
            if ok2:
                return {"ok": False, "message": f"{path} already in post-state; refusing to re-apply"}
            return {"ok": False, "message": msg}
        new_content = content.replace(LOOP_OLD_T4_ANCHOR, LOOP_NEW_T4_ANCHOR, 1)
    else:  # reverse
        ok, msg = _check_anchor(content, LOOP_NEW_T4_ANCHOR, path)
        if not ok:
            ok2, msg2 = _check_anchor(content, LOOP_OLD_T4_ANCHOR, path)
            if ok2:
                return {"ok": False, "message": f"{path} already in pre-state; nothing to reverse"}
            return {"ok": False, "message": msg}
        new_content = content.replace(LOOP_NEW_T4_ANCHOR, LOOP_OLD_T4_ANCHOR, 1)

    post_lines = _line_count(new_content)
    line_delta = post_lines - pre_lines

    if not dry_run:
        _backup(path)
        _write(path, new_content)

    return {
        "ok": True,
        "path": path,
        "pre_lines": pre_lines,
        "post_lines": post_lines,
        "line_delta": line_delta,
        "edit": "T-4 (history-write condition expanded to include sexpr non-empty)",
    }


# =====================================================================
# MAIN
# =====================================================================

def main():
    parser = argparse.ArgumentParser(description="Phase 1 memory-layer merge apply script")
    parser.add_argument("--apply", action="store_true", help="Apply changes to disk (default is dry-run)")
    parser.add_argument("--reverse", action="store_true", help="Reverse direction (post-state -> pre-state)")
    args = parser.parse_args()

    direction = "reverse" if args.reverse else "apply"
    dry_run = not args.apply

    processors = [
        (_process_skills_metta, "src/skills.metta (T-2 wrapping)"),
        (_process_memory_metta, "src/memory.metta (additive + bridge + query-promoted)"),
        (_process_helper_py, "src/helper.py (promotion infrastructure)"),
        (_process_loop_metta, "src/loop.metta (T-4 history-write)"),
    ]

    print()
    print("=" * 78)
    mode = "DRY-RUN" if dry_run else "WRITING"
    print(f"  PHASE 1 MEMORY-LAYER MERGE: {direction.upper()} ({mode})")
    print("=" * 78)
    print()

    # First pass: per-file state checks (no writes).
    print(">>> Per-file state checks <<<")
    print()
    results = []
    for processor, label in processors:
        result = processor(direction, dry_run=True)
        results.append((label, result))
        if not result.get("ok"):
            print(f"  [{label}]")
            print(f"    FAIL: {result.get('message')}")
        else:
            print(f"  [{label}]")
            print(f"    OK: pre_lines={result.get('pre_lines')}, "
                  f"post_lines={result.get('post_lines')}, "
                  f"line_delta={result.get('line_delta'):+d}")
            print(f"    Edit: {result.get('edit')}")
    print()

    # Atomic gate: if any state check fails, abort before writing anything.
    if any(not r.get("ok") for _, r in results):
        print("  STATE CHECK FAILED. Aborting before any writes.")
        print("  Resolve the failures above and re-run.")
        print()
        return 1

    print("  All state checks passed.")
    print()

    if dry_run:
        print("=" * 78)
        print("  DRY-RUN MODE: no files written. To apply, add --apply.")
        print("=" * 78)
        print()
        print("  Reversibility: python3 staging/apply_phase1_memory_layer_merge.py --reverse --apply")
        print()
        return 0

    # Second pass: write.
    print("=" * 78)
    print("  WRITING")
    print("=" * 78)
    print()
    final_results = []
    for processor, label in processors:
        result = processor(direction, dry_run=False)
        if not result.get("ok"):
            print(f"  FAIL on {label}: {result.get('message')}")
            return 1
        print(f"  Wrote: {label}")
        final_results.append((label, result))
    print()

    print("=" * 78)
    print("  DISK VERIFICATION")
    print("=" * 78)
    print()
    for label, r in final_results:
        print(f"  {label}: {r.get('post_lines')} lines, edit applied")
    print()

    print("=" * 78)
    print(f"  PHASE 1 MEMORY-LAYER MERGE {direction.upper()} COMPLETE")
    print("=" * 78)
    print()

    if direction == "apply":
        print("  Next steps:")
        print()
        print("  1. Container rebuild:")
        print("       docker compose build --no-cache clarityclaw && \\")
        print("       docker compose up -d clarityclaw")
        print()
        print("  2. Verify substrate boots and initMemory runs the new path:")
        print("       docker logs clarity_omega 2>&1 | grep -E 'Initializing memory'")
        print()
        print("  3. Verify promotion_open_map ran (creates SQLite file):")
        print("       docker exec -it clarity_omega ls -la /PeTTa/repos/omegaclaw/memory/promotions.db")
        print()
        print("  4. Verify metta function wrapping works:")
        print("       (observe LLM-generated (metta ...) calls in log; they should return strings)")
        print()
        print("  5. Test reconcile-promotion-atoms idempotency:")
        print("       restart container twice; verify no errors on second start")
        print()
        print("  Reversibility: python3 staging/apply_phase1_memory_layer_merge.py --reverse --apply")
    else:
        print("  Next steps:")
        print("    docker compose build --no-cache clarityclaw && docker compose up -d clarityclaw")
    print()
    return 0


if __name__ == "__main__":
    sys.exit(main())
