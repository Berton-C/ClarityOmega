#!/usr/bin/env python3
"""
corner_gap_pipeline_harness.py

Validates the corner-gap substrate pipeline (Layers 1-4) in the live container,
against the staged COLD files in soul/in_progress/corner_gap/, BEFORE any loop
wiring. The point is to discover what we do not know while no water flows.

RESULTS ARTIFACT: every run writes a timestamped log to the host (--log-dir,
default ".") AND to the container /tmp/. The log captures, per probe, the EXACT
script sent and the COMPLETE raw output (the metta-to-prolog compilation trace
plus the eval results), not just the console tail. That full trace is where the
deep knowledge lives. The console stays readable (tails + verdicts); the log is
the durable record to diff across iterations.

DISCIPLINE (from the established probe shape in prior sprints):
  - HANDS ONLY. Python builds expressions, runs them via run.sh, parses output,
    and compares to a reference computed in Python. Python never computes the
    cognition; the reference is for CHECKING the substrate only.
  - RAW OUTPUT BEFORE EVERY VERDICT. The safeguard that catches false confidence.
  - UNREDUCED DETECTION. An echoed (function ...) in the output means the function
    did not fire; that is a FAIL, not a pass.
  - PREFLIGHT. Distinguish substrate-wrong from substrate-absent.
  - FRESH SPACE PER CALL. Each run.sh invocation loads a fresh AtomSpace, so each
    scenario seeds its own atoms and is isolated from the others.

WHAT IT DOES NOT TEST: the Layer 5 loop wiring (not built) or end-to-end
behavioral dynamics (needs the live loop with the model in it). It answers "do the
substrate functions reduce and classify correctly," not "does the gate change
behavior." That second question is a later in-loop test.

USAGE: python3 corner_gap_pipeline_harness.py [--container clarity_omega]
                                             [--skip-graded] [--log-dir DIR]
"""

import argparse
import datetime
import os
import re
import subprocess
import sys

DEFAULT_CONTAINER = "clarity_omega"
RUN_SH = "./run.sh"
TIMEOUT = 30

CORNER_DIR = "/PeTTa/repos/omegaclaw/soul/in_progress/corner_gap"

# TRANSPORT: inline bodies, not import! lines.
# Confirmed in-container (2026-06-04): a one-shot `run.sh <file>` compiles inline
# (= ...) definitions to reducible prolog clauses, but does NOT register import!-ed
# library/file rules for top-level ! evaluation (they collect as data, goal=true).
# Production reduces soul functions as internal calls inside the (omegaclaw) loop,
# a mode a one-shot file cannot reach. So the harness concatenates the actual file
# BODIES (read from the container via cat) ahead of the test calls. Only lib_import
# is imported, since it arms the import system and carries no rules we evaluate.
# The import-vs-register gap (does the agent BOOT with these wired into
# lib_clarity_reasoning) is a separate boot test, not this logic harness.
LIB_IMPORT_LINE = "!(import! &self (library lib_import))"

# Crisp v1 spine: bodies inlined for every stage. Order is dependency-friendly but
# (= ...) clauses are order-independent for reduction once all are present.
CORNER_FILES = [
    "state_delta_writer.metta",
    "state_delta_writer_writers.metta",
    "coupling_integrity_detector.metta",
    "coupling_integrity_detector_writers.metta",
    "corner_gate.metta",
]
# Graded stages (Stage 7, 8): the optional quantale/continuity files, plus the
# cold-lib bodies they depend on (q-meet etc), inlined for the same reason.
GRADED_FILES = [
    "coupling_quantale_merge.metta",
    "cycle_continuity_probe.metta",
    "cycle_continuity_probe_writers.metta",
]
GRADED_LIB_PATHS = [
    "/PeTTa/repos/omegaclaw/lib_clarity_reasoning/lib_quantale.metta",
    "/PeTTa/repos/omegaclaw/lib_clarity_reasoning/lib_self_continuity.metta",
]


# ---------------------------------------------------------------------------
# Recorder: tee console + accumulate the full log artifact
# ---------------------------------------------------------------------------

class Recorder:
    def __init__(self):
        self.lines = []

    def pr(self, s=""):          # console + log
        print(s)
        self.lines.append(s)

    def log_only(self, s=""):    # log artifact only (full raw, scripts)
        self.lines.append(s)

    def text(self):
        return "\n".join(self.lines) + "\n"


REC = Recorder()


def pr(s=""):
    REC.pr(s)


# ---------------------------------------------------------------------------
# Container plumbing (matches the established pattern)
# ---------------------------------------------------------------------------

def run(cmd, **kw):
    return subprocess.run(cmd, capture_output=True, text=True, timeout=TIMEOUT, **kw)


def strip_ansi(t):
    return re.sub(r'\x1b\[[0-9;]*m', '', t or "")


def container_running(container):
    try:
        p = run(["docker", "ps", "--filter", "name=" + container, "--format", "{{.Names}}"])
        return p.returncode == 0 and container in p.stdout
    except subprocess.TimeoutExpired:
        return False


_BODY_CACHE = {}


def fetch_body(container, path):
    """Read a file body from the container once, cache it. Returns text or None."""
    if path in _BODY_CACHE:
        return _BODY_CACHE[path]
    p = run(["docker", "exec", container, "sh", "-c", "cat " + path])
    body = p.stdout if (p.returncode == 0 and p.stdout) else None
    _BODY_CACHE[path] = body
    return body


def assemble_bodies(container, include_graded=False):
    """Build the inlined definition block: lib_import line, then file bodies.
    Returns (block_text, missing_paths)."""
    parts = [LIB_IMPORT_LINE]
    missing = []
    if include_graded:
        for libp in GRADED_LIB_PATHS:
            b = fetch_body(container, libp)
            if b is None:
                missing.append(libp)
            else:
                parts.append(b)
    files = CORNER_FILES + (GRADED_FILES if include_graded else [])
    for fn in files:
        path = CORNER_DIR + "/" + fn
        b = fetch_body(container, path)
        if b is None:
            missing.append(path)
        else:
            parts.append(b)
    return "\n".join(parts), missing


def eval_in_container(container, lines, include_graded=False, label="probe"):
    """
    Inline the corner_gap file BODIES (+ lib_import, + graded cold-lib bodies when
    asked), then the body lines, write to a temp file, run via run.sh.
    Records the exact body lines and the COMPLETE raw output into the log artifact.
    Returns (stdout, err).
    """
    block, missing = assemble_bodies(container, include_graded)
    script = block + "\n" + "\n".join(lines) + "\n"
    path = "/tmp/_corner_gap_harness.metta"
    if missing:
        out, err = None, "missing file bodies: " + ", ".join(missing)
    else:
        w = run(["docker", "exec", "-i", container, "sh", "-c", "cat > " + path], input=script)
        if w.returncode != 0:
            out, err = None, "write failed: " + str(w.stderr)
        else:
            p = run(["docker", "exec", container, "sh", "-c",
                     "cd /PeTTa && " + RUN_SH + " " + path + " 2>&1"])
            out, err = p.stdout, None

    # Full record to the log artifact (not the console).
    REC.log_only("\n" + "-" * 70)
    REC.log_only("PROBE: " + label)
    REC.log_only("-" * 70)
    REC.log_only("SCRIPT SENT (body lines only; inlined definition block omitted for brevity):")
    for ln in lines:
        REC.log_only("  " + ln)
    REC.log_only("RAW OUTPUT (ansi-stripped, full):")
    REC.log_only(strip_ansi(out) if out else ("(no output; err=" + str(err) + ")"))
    return out, err


# ---------------------------------------------------------------------------
# Parsers (lenient by design; the raw output is the source of truth)
# ---------------------------------------------------------------------------

def tail(out, n=6):
    return [ln for ln in strip_ansi(out).splitlines() if ln.strip()][-n:]


def show_raw(out, n=6):
    # Console only (the full raw is already in the log artifact via eval).
    if not out:
        print("    (no output)")
        return
    for ln in tail(out, n):
        print("    " + ln)


def last_result(out):
    lines = [ln.strip() for ln in strip_ansi(out or "").splitlines() if ln.strip()]
    if not lines:
        return ""
    r = lines[-1]
    if r.startswith("[") and r.endswith("]"):
        r = r[1:-1].strip()
    return r


def last_int(out):
    nums = re.findall(r'-?\d+', last_result(out))
    return int(nums[-1]) if nums else None


def has_token(out, tok):
    return tok in strip_ansi(out or "")


def last_bool(out):
    # PeTTa renders booleans lowercase (true/false) in output, even though the
    # source uses True/False. Read the final result line only. The old whole-output
    # fallback is removed: with inlined file bodies the source text contains
    # True/False throughout and would false-match.
    r = last_result(out).strip().lower()
    if r == "true":
        return True
    if r == "false":
        return False
    if re.search(r'\btrue\b', r) and not re.search(r'\bfalse\b', r):
        return True
    if re.search(r'\bfalse\b', r) and not re.search(r'\btrue\b', r):
        return False
    return None


def last_symbol(out, candidates):
    clean = strip_ansi(out or "")
    best, best_pos = None, -1
    for cand in candidates:
        pos = clean.rfind(cand)
        if pos > best_pos:
            best, best_pos = cand, pos
    return best


_PBIT = re.compile(r'(?:mk-)?pbit\s+([0-9.]+)\s+([0-9.]+)')


def last_pbit(out):
    pairs = _PBIT.findall(strip_ansi(out or ""))
    return (float(pairs[-1][0]), float(pairs[-1][1])) if pairs else None


def result_section(out):
    """Lines after the LAST caret separator: the actual reduction result(s).
    The 'true' goal-success marker is dropped. Everything above the last caret
    (the metta-runnable echo !(fname ...) and the prolog goal 'fname'(A)) is NOT
    the result and must not be scanned for reduction state."""
    lines = strip_ansi(out or "").splitlines()
    last_sep = -1
    for i, ln in enumerate(lines):
        s = ln.strip()
        if s and set(s) == {"^"}:
            last_sep = i
    seg = lines[last_sep + 1:] if last_sep >= 0 else lines
    return [ln.strip() for ln in seg if ln.strip() and ln.strip() != "true"]


def is_unreduced(out, fname):
    # A reduced call yields a value in the result section; an unreduced call
    # echoes the bare (fname ...) term there. Scan ONLY the result section: the
    # metta-runnable echo !(fname ...) always appears above it and would otherwise
    # false-match every reduced call.
    sec = result_section(out)
    return any(re.search(r'\(\s*' + re.escape(fname) + r'\b', ln) for ln in sec)


def list_len_from_collapse(out):
    r = last_result(out)
    if r == "" or r == "()":
        return 0
    depth, count, started = 0, 0, False
    for ch in r:
        if ch == "(":
            if depth == 0:
                count += 1
            depth += 1
            started = True
        elif ch == ")":
            depth = max(0, depth - 1)
    if count == 0 and started is False and r:
        return len(r.split())
    return count


# ---------------------------------------------------------------------------
# Python references (for CHECKING only)
# ---------------------------------------------------------------------------

REAL_CLASSES = ["responsive-send", "status-send-unprompted",
                "verification-query", "exploration-query", "pin-only"]
PERSON_CLASSES = ["responsive-send", "verification-query"]
SYSTEM_CLASSES = ["status-send-unprompted", "exploration-query", "pin-only"]


def ref_verdict(classes, state_delta):
    emit = any(c in REAL_CLASSES for c in classes)
    if not emit:
        return "composure"
    if state_delta == "forward":
        return "healthy-coupling"
    person = sum(1 for c in classes if c in PERSON_CLASSES)
    system = sum(1 for c in classes if c in SYSTEM_CLASSES)
    return "drifting" if person >= system else "corner"


def qmeet(a, b):
    return (min(a[0], b[0]), min(a[1], b[1]))


def ref_corner_pbit_core(classes, state_delta):
    emit = (1.0, 0.9) if any(c in REAL_CLASSES for c in classes) else (0.0, 0.9)
    outflat = (0.0, 0.9) if state_delta == "forward" else (1.0, 0.7)
    person = sum(1 for c in classes if c in PERSON_CLASSES)
    system = sum(1 for c in classes if c in SYSTEM_CLASSES)
    total = person + system
    decoupled = (system / total, min(0.9, total / 5)) if total > 0 else (0.0, 0.0)
    return qmeet(emit, qmeet(outflat, decoupled))


def close(a, b, tol=0.02):
    return a is not None and b is not None and abs(a[0]-b[0]) < tol and abs(a[1]-b[1]) < tol


# ---------------------------------------------------------------------------
# Seed helpers
# ---------------------------------------------------------------------------

def seed_recent_actions(classes):
    return ['!(add-atom &self (recent-action ' + str(i+1) + ' ' + c + ' "d' + str(i) + '"))'
            for i, c in enumerate(classes)]


def seed_state_delta(verdict, cycle=1):
    return ['!(add-atom &self (state-delta ' + str(cycle) + ' ' + verdict + '))'] if verdict else []


def seed_coupling_status(verdicts):
    return ['!(add-atom &self (coupling-status ' + str(i+1) + ' ' + v + '))'
            for i, v in enumerate(verdicts)]


# ---------------------------------------------------------------------------
# Stage helpers
# ---------------------------------------------------------------------------

def stage(name):
    pr("\n" + "=" * 70)
    pr(name)
    pr("=" * 70)


def verdict_line(label, ok):
    pr("  " + label.ljust(52) + " " + ("PASS" if ok else "FAIL"))
    return ok


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--container", default=DEFAULT_CONTAINER)
    ap.add_argument("--skip-graded", action="store_true")
    ap.add_argument("--log-dir", default=".")
    args = ap.parse_args()
    c = args.container
    do_graded = not args.skip_graded
    results = {}

    ts = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    pr("=" * 70)
    pr("Corner-gap pipeline harness (substrate validation, pre-wiring)")
    pr("timestamp: " + ts + "   container: " + c + "   graded: " + str(do_graded))
    pr("=" * 70)
    REC.log_only("TRANSPORT: inline bodies (lib_import + file bodies, no import! of rules).")
    REC.log_only("FILES INLINED:")
    for fn in CORNER_FILES + (GRADED_FILES if do_graded else []):
        REC.log_only("  " + CORNER_DIR + "/" + fn)
    if do_graded:
        for libp in GRADED_LIB_PATHS:
            REC.log_only("  " + libp)

    # STAGE 0: preflight + load
    stage("STAGE 0  PREFLIGHT + LOAD")
    if not container_running(c):
        pr("  [FAIL] container '" + c + "' not running. Start it and re-run.")
        _write_log(args, ts, c)
        sys.exit(1)
    pr("  [OK] container '" + c + "' running")

    # Load-gate split (Clarity's improvement): import_ok / symbol_ok / reduce_ok.
    # Separating these means a STAGE 0 failure names WHICH layer broke, not just
    # "load failed". import_ok = all bodies present; symbol_ok = target defined in
    # the inlined source; reduce_ok = the ! call returns a real value, not an echo.
    block, missing = assemble_bodies(c, do_graded)
    import_ok = (len(missing) == 0)
    symbol_ok = import_ok and ("corner-gate-feedback" in block)
    out, err = eval_in_container(c, ["!(corner-gate-feedback)"], do_graded, "STAGE 0 load probe")
    print("  Load probe RAW (tail):")
    show_raw(out)
    reduce_ok = bool(out) and has_token(out, "corner detected") and not is_unreduced(out, "corner-gate-feedback")

    pr("  Load gate (Clarity's import_ok / symbol_ok / reduce_ok split):")
    verdict_line("import_ok  (all file bodies present)", import_ok)
    verdict_line("symbol_ok  (corner-gate-feedback defined in source)", symbol_ok)
    verdict_line("reduce_ok  (corner-gate-feedback reduces, not echoed)", reduce_ok)
    load_ok = import_ok and symbol_ok and reduce_ok
    results["load"] = verdict_line("STAGE 0 load gate (import + symbol + reduce)", load_ok)
    if not load_ok:
        if not import_ok:
            pr("\n  >>> import_ok FAILED. Missing file bodies (check paths under")
            pr("  in_progress/corner_gap/ and the graded lib paths):")
            for m in missing:
                pr("      " + m)
        elif not symbol_ok:
            pr("\n  >>> symbol_ok FAILED. corner-gate-feedback is not defined in the")
            pr("  inlined source. Check the function name in corner_gate.metta.")
        else:
            pr("\n  >>> reduce_ok FAILED. Bodies inlined and symbol present, but the")
            pr("  call did not reduce (echoed). Inspect the RAW tail above; a symbol")
            pr("  used by corner-gate-feedback may be defined in a file not inlined.")
        _write_log(args, ts, c)
        sys.exit(2)

    # STAGE 1: detector counts + emission (arity)
    stage("STAGE 1  DETECTOR COUNTS + EMISSION (arity)")
    classes = ["status-send-unprompted", "status-send-unprompted", "pin-only"]
    out, _ = eval_in_container(c, seed_recent_actions(classes) + ["!(count-actions-in-window)"],
                               label="STAGE 1 count-actions-in-window (3 seeded)")
    pr("  seeded 3 system-class recent-action atoms")
    print("  count-actions-in-window RAW (tail):"); show_raw(out, 4)
    got = last_int(out)
    cnt_ok = (got == 3) and not is_unreduced(out, "count-actions-in-window")
    pr("  count: " + str(got) + "  expected: 3")
    results["count"] = verdict_line("count-actions-in-window matches seed (arity)", cnt_ok)

    out, _ = eval_in_container(c, seed_recent_actions(classes) + ["!(emission-present)"],
                               label="STAGE 1 emission-present (seeded)")
    print("  emission-present RAW (tail):"); show_raw(out, 3)
    em = last_bool(out)
    results["emission"] = verdict_line("emission-present True when actions seeded", em is True)

    out, _ = eval_in_container(c, ["!(emission-present)"], label="STAGE 1 emission-present (no seeds)")
    print("  emission-present (no seeds) RAW (tail):"); show_raw(out, 3)
    er = last_bool(out)
    results["emission_rest"] = verdict_line("emission-present False when resting", er is False)

    # STAGE 2: state-delta classifier + singleton round-trip
    stage("STAGE 2  STATE-DELTA (classifier + singleton clear-then-write)")
    truth = [(("True", "False", "False"), "forward"),
             (("False", "True", "True"), "forward"),
             (("False", "True", "False"), "none"),
             (("False", "False", "False"), "none")]
    cls_ok = True
    for (m, ne, nv), exp in truth:
        out, _ = eval_in_container(c, ["!(classify-state-delta " + m + " " + ne + " " + nv + ")"],
                                   label="STAGE 2 classify(" + m + "," + ne + "," + nv + ")")
        got = last_symbol(out, ["forward", "none"])
        ok = (got == exp) and not is_unreduced(out, "classify-state-delta")
        pr("  classify(" + m + "," + ne + "," + nv + ") -> " + str(got) + "  expected " + exp + "  [" + ("ok" if ok else "BAD") + "]")
        cls_ok = cls_ok and ok
    results["classify"] = verdict_line("classify-state-delta truth table", cls_ok)

    populates = ["!(populate-state-delta True False False 1)",
                 "!(populate-state-delta False False False 2)"]
    out_a, _ = eval_in_container(c, populates + ["!(latest-state-delta-verdict)"],
                                 label="STAGE 2 singleton: latest verdict after 2 populates")
    print("  latest-state-delta-verdict RAW (tail):"); show_raw(out_a, 3)
    latest = last_symbol(out_a, ["forward", "none"])
    out_b, _ = eval_in_container(c, populates + ["!(collapse (match &self (state-delta $x $y) ($x $y)))"],
                                 label="STAGE 2 singleton: atom dump after 2 populates")
    print("  state-delta atom dump RAW (tail):"); show_raw(out_b, 3)
    natoms = list_len_from_collapse(out_b)
    singleton_ok = (latest == "none") and (natoms == 1)
    pr("  latest verdict: " + str(latest) + " (expected none)   state-delta atoms: " + str(natoms) + " (expected 1)")
    results["singleton"] = verdict_line("state-delta stays singleton (do-clear works)", singleton_ok)

    # STAGE 3: crisp verdict matrix (the core logic)
    stage("STAGE 3  CRISP COUPLING-VERDICT MATRIX")
    scenarios = [
        ("composure (no emission)", [], None, "composure"),
        ("healthy (emit + forward)", ["status-send-unprompted"], "forward", "healthy-coupling"),
        ("drifting (emit + none + person)", ["responsive-send", "verification-query"], "none", "drifting"),
        ("corner (emit + none + system)", ["status-send-unprompted", "exploration-query"], "none", "corner"),
    ]
    matrix_ok = True
    for label, cls, sd, exp in scenarios:
        out, _ = eval_in_container(c, seed_recent_actions(cls) + seed_state_delta(sd) + ["!(coupling-verdict)"],
                                   label="STAGE 3 " + label)
        got = last_symbol(out, ["healthy-coupling", "drifting", "corner", "composure"])
        ref = ref_verdict(cls, sd)
        ok = (got == exp == ref) and not is_unreduced(out, "coupling-verdict")
        pr("  " + label)
        print("    RAW (tail):"); show_raw(out, 3)
        pr("    verdict: " + str(got) + "  expected: " + str(exp) + "  ref: " + str(ref) + "  [" + ("ok" if ok else "BAD") + "]")
        matrix_ok = matrix_ok and ok
    results["verdict_matrix"] = verdict_line("verdict matrix (composure/healthy/drift/corner)", matrix_ok)

    # STAGE 4: sustained corner + consecutive-clear
    stage("STAGE 4  SUSTAINED CORNER + CONSECUTIVE-CLEAR")
    out, _ = eval_in_container(c, seed_coupling_status(["corner", "corner"]) + ["!(corner-confirmed)"],
                               label="STAGE 4 corner-confirmed (2 corners)")
    print("  2 consecutive corners RAW (tail):"); show_raw(out, 3)
    cc2 = last_bool(out)
    out, _ = eval_in_container(c, seed_coupling_status(["corner"]) + ["!(corner-confirmed)"],
                               label="STAGE 4 corner-confirmed (1 corner)")
    cc1 = last_bool(out)
    pr("  corner-confirmed: 2 corners -> " + str(cc2) + " (expect True), 1 corner -> " + str(cc1) + " (expect False)")
    results["sustained"] = verdict_line("corner-confirmed fires at 2, not 1", cc2 is True and cc1 is False)

    out, _ = eval_in_container(c, seed_coupling_status(["corner", "corner"]) +
                               ["!(do-clear-coupling-status!)",
                                "!(collapse (match &self (coupling-status $x $y) ($x $y)))"],
                               label="STAGE 4 do-clear-coupling-status! removes all")
    print("  after do-clear RAW (tail):"); show_raw(out, 3)
    cleared = list_len_from_collapse(out)
    results["clear_all"] = verdict_line("do-clear-coupling-status! removes all", cleared == 0)

    out, _ = eval_in_container(c, ["!(add-atom &self (coupling-status 1 corner))",
                                   "!(populate-coupling-verdict 2)",
                                   "!(collapse (match &self (coupling-status $x $y) $y))"],
                               label="STAGE 4 populate clears window on non-corner")
    print("  prior corner + composure cycle, post-populate RAW (tail):"); show_raw(out, 3)
    only_composure = has_token(out, "composure") and not re.search(r'\bcorner\b', last_result(out) or "")
    results["consecutive_clear"] = verdict_line("populate clears window on non-corner verdict", only_composure)

    # STAGE 5: the gate
    stage("STAGE 5  GATE (apply-corner-gate)")
    out, _ = eval_in_container(c, seed_coupling_status(["corner", "corner"]) + ['!(apply-corner-gate (Send "x"))'],
                               label="STAGE 5 apply-corner-gate (cornered)")
    print("  cornered RAW (tail):"); show_raw(out, 3)
    gate_silence = last_result(out) in ("()", "")
    out, _ = eval_in_container(c, seed_coupling_status([]) + ['!(apply-corner-gate (Send "x"))'],
                               label="STAGE 5 apply-corner-gate (not cornered)")
    print("  not cornered RAW (tail):"); show_raw(out, 3)
    passthru = has_token(out, "Send")
    results["gate"] = verdict_line("gate silences when cornered, passes when not", gate_silence and passthru)

    # STAGE 6: the feedback shaping
    stage("STAGE 6  FEEDBACK (gate-aware-results)")
    out, _ = eval_in_container(c, seed_coupling_status(["corner", "corner"]) + ['!(gate-aware-results (RESULTS: (foo)))'],
                               label="STAGE 6 gate-aware-results (cornered)")
    print("  cornered RAW (tail):"); show_raw(out, 3)
    fb_gated = has_token(out, "corner detected") and has_token(out, "RESULTS")
    out, _ = eval_in_container(c, seed_coupling_status([]) + ['!(gate-aware-results (RESULTS: (foo)))'],
                               label="STAGE 6 gate-aware-results (not cornered)")
    print("  not cornered RAW (tail):"); show_raw(out, 3)
    fb_pass = has_token(out, "foo")
    results["feedback"] = verdict_line("feedback injected when cornered, passthrough when not", fb_gated and fb_pass)

    # STAGE 7: graded quantale merge
    if do_graded:
        stage("STAGE 7  GRADED MERGE (quantale; higher risk)")
        gm_ok = True
        for label, cls, sd in [
            ("corner-ish (system, none)", ["status-send-unprompted", "exploration-query", "pin-only"], "none"),
            ("healthy-ish (system, forward)", ["status-send-unprompted"], "forward"),
        ]:
            out, _ = eval_in_container(c, seed_recent_actions(cls) + seed_state_delta(sd) + ["!(corner-pbit-core)"],
                                       include_graded=True, label="STAGE 7 corner-pbit-core " + label)
            got = last_pbit(out)
            ref = ref_corner_pbit_core(cls, sd)
            ok = close(got, ref) and not is_unreduced(out, "corner-pbit-core")
            pr("  " + label)
            print("    RAW (tail):"); show_raw(out, 4)
            pr("    corner-pbit-core: " + str(got) + "  ref: (" + format(ref[0], ".3f") + ", " + format(ref[1], ".3f") + ")  [" + ("ok" if ok else "BAD") + "]")
            gm_ok = gm_ok and ok
        results["graded_merge"] = verdict_line("corner-pbit-core matches quantale reference", gm_ok)

        # STAGE 8: continuity probe
        stage("STAGE 8  CONTINUITY PROBE (pfn round-trip + self-continuity)")
        cls = ["status-send-unprompted", "status-send-unprompted", "pin-only"]
        out, _ = eval_in_container(c, seed_recent_actions(cls) +
                                   ["!(do-snapshot-cycle-pfn!)",
                                    "!(collapse (match &self (cycle-pfn-snapshot $p) $p))"],
                                   include_graded=True, label="STAGE 8 build + snapshot + read-back")
        print("  pfn round-trip RAW (tail):"); show_raw(out, 4)
        pfn_stored = has_token(out, "pfn") and has_token(out, "edge") and not is_unreduced(out, "build-cycle-pfn")
        results["pfn_roundtrip"] = verdict_line("build-cycle-pfn stores as inert data (round-trip)", pfn_stored)

        out, _ = eval_in_container(c, seed_recent_actions(cls) +
                                   ["!(do-snapshot-cycle-pfn!)", "!(behavior-stasis-pbit)"],
                                   include_graded=True, label="STAGE 8 behavior-stasis (frozen profile)")
        print("  frozen profile RAW (tail):"); show_raw(out, 4)
        st = last_pbit(out)
        frozen_high = st is not None and st[0] >= 0.95 and not is_unreduced(out, "self-continuity-score")
        pr("  frozen stasis pbit: " + str(st) + "  expect strength near 1.0")
        results["stasis_frozen"] = verdict_line("self-continuity reduces; frozen reads ~1.0", frozen_high)

        out, _ = eval_in_container(c, seed_recent_actions(cls) + ["!(behavior-stasis-pbit)"],
                                   include_graded=True, label="STAGE 8 behavior-stasis (no prior snapshot)")
        print("  bootstrap RAW (tail):"); show_raw(out, 3)
        st0 = last_pbit(out)
        bootstrap_inert = st0 is not None and abs(st0[1] - 0.0) < 0.01
        pr("  bootstrap stasis pbit: " + str(st0) + "  expect confidence 0.0 (inert)")
        results["stasis_bootstrap"] = verdict_line("bootstrap stasis is q-unknown (conf 0)", bootstrap_inert)

    # SUMMARY
    stage("SUMMARY")
    for k, v in results.items():
        pr("  " + k.ljust(20) + " " + ("PASS" if v else "FAIL"))
    allp = all(results.values())
    pr("")
    if allp:
        pr("  >>> PIPELINE SUBSTRATE VALIDATED (parts, on synthetic atoms).")
        pr("  Functions reduce and classify correctly. Next: reconcile Clarity's")
        pr("  originals, refresh artifact_1 line numbers, then wire Layer 5 one")
        pr("  commit at a time. Behavioral (in-loop) testing comes after wiring.")
    else:
        pr("  >>> NOT FULLY VALIDATED. Read each RAW block in the log against its")
        pr("  verdict. An unreduced (function ...) echo means that function did not")
        pr("  fire: check the import preamble, the file load (STAGE 0), and the shape.")
        pr("  A count/verdict mismatch with a clean reduce means a logic or partition")
        pr("  error (e.g., the person/system tag split under review).")

    _write_log(args, ts, c)
    if not allp:
        sys.exit(3)


def _write_log(args, ts, container):
    """Write the accumulated log artifact to the host and into the container /tmp/."""
    fname = "corner_gap_pipeline_harness_" + ts + ".log"
    text = REC.text()
    host_path = os.path.join(args.log_dir, fname)
    try:
        with open(host_path, "w") as f:
            f.write(text)
        host_msg = host_path
    except OSError as e:
        host_msg = "(host write failed: " + str(e) + ")"
    cont_msg = "/tmp/" + fname
    try:
        w = run(["docker", "exec", "-i", container, "sh", "-c", "cat > /tmp/" + fname], input=text)
        if w.returncode != 0:
            cont_msg = "(container write failed: " + str(w.stderr) + ")"
    except Exception as e:
        cont_msg = "(container write failed: " + str(e) + ")"
    print("\nLog artifact written:")
    print("  host:      " + host_msg)
    print("  container: " + cont_msg)


if __name__ == "__main__":
    main()
