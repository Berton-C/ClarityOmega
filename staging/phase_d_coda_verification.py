#!/usr/bin/env python3
"""
phase_d_coda_verification.py

Validates the Sprint 0-Coda capability-registry dispatcher (Path C) in the live
container, against the staged draft at soul/capability_registry_path_c_draft.metta,
BEFORE the loop wiring of Phase C. Read what the substrate actually did, not just
verdicts.

RESULTS ARTIFACT: every run writes a timestamped log to the host (--log-dir,
default ".") AND to the container /tmp/. The log captures, per probe, the EXACT
script sent and the COMPLETE raw output (the metta-to-prolog compilation trace
plus the eval results). The console stays readable (tails + verdicts); the log is
the durable record to diff across iterations.

DISCIPLINE:
  - HANDS ONLY. Python builds expressions, runs them via run.sh, parses output.
  - RAW OUTPUT BEFORE EVERY VERDICT.
  - UNREDUCED DETECTION. An echoed (function ...) in the result section is a FAIL.
  - PREFLIGHT. Distinguish substrate-wrong from substrate-absent.
  - FRESH SPACE PER CALL. Each probe seeds its atoms AND reads them back in ONE
    combined run.sh input (seed !() and read !() are separate lines, same file).

WHAT THE FIRST TWO RUNS TAUGHT (baked in):

  (point 1) THE COUPLING GAP. P-1/P-2/P-3 each test an ENDPOINT. None tested the
  JOINT: that dispatch's match pattern structurally couples to the registered
  shape. A 4-field matcher silently fails to couple with a 5-field producer (no
  error, empty match, silent fallback, every endpoint except P-3 falsely green).
  So P-0 runs FIRST: a standalone match asserting the 5-field registered-
  capability shape is matchable. The match itself is the invariant.

  (point 2) COINCIDENCE-OF-CORRECTNESS. A differential test passes VACUOUSLY when
  control and experimental share an upstream failure (both fall back, difference
  invisible). So every differential test first runs a CONTROL-PRECONDITION GATE:
  assert the control case exercises the path under test BEFORE testing that the
  change alters it. If control does not fire, the differential test is INVALID.

  (point 3) TWO-DEFECT INDEPENDENCE. Two independent defects existed: match-shape
  mismatch and missing (eligible-lifecycle active). A single both-fixed fixture
  masks whether either fix alone sufficed. So a MATRIX runs four cells:
      A match-BROKEN + lifecycle-BROKEN -> not invoked
      B match-FIXED  + lifecycle-BROKEN -> not invoked (lifecycle drops it)
      C match-BROKEN + lifecycle-FIXED  -> not invoked (won't couple)
      D match-FIXED  + lifecycle-FIXED  -> INVOKED (working configuration)
  The MATCH axis is controlled from the FIXTURE side against the FIXED draft:
  a 5-field fixture atom couples with the fixed 5-field matcher; a 4-field atom
  does not. The LIFECYCLE axis: seed (eligible-lifecycle active) or not. Only D
  should invoke; B and C each isolate one defect's blocking effect.

TRANSPORT: inline the registry-draft BODY (cat from container) ahead of the test
calls. A one-shot run.sh <file> compiles inline (= ...) to reducible clauses but
does NOT register import!-ed rules for top-level ! eval. Only lib_import imported.

NOT TESTED HERE: P-4 (CHARS_SENT/encoded-skills), P-5 (LLM parity), P-6 (silent
chain termination) -- post-Phase-C observational criteria, reported PRE-CONDITION.

USAGE: python3 phase_d_coda_verification.py [--container clarity_omega]
                                            [--registry PATH] [--log-dir DIR]
"""

import argparse
import datetime
import os
import re
import subprocess
import sys

DEFAULT_CONTAINER = "clarity_omega"
DEFAULT_REGISTRY = "/PeTTa/repos/omegaclaw/soul/capability_registry_path_c_draft.metta"
RUN_SH = "./run.sh"
TIMEOUT = 60

LIB_IMPORT_LINE = "!(import! &self (library lib_import))"

CAP_5FIELD = ('!(add-atom &self (registered-capability schema: (skill-request cycle: $k) '
              'handler: skill-discovery priority: 100 lifecycle: active metadata: ()))')
CAP_4FIELD = ('!(add-atom &self (registered-capability schema: (skill-request cycle: $k) '
              'handler: skill-discovery priority: 100 lifecycle: active))')
HANDLER_DEF = ('!(add-atom &self (= (skill-discovery $request) '
               '(skill-set skills: "FIXTURE-SKILLS")))')
ELIGIBLE_LIFECYCLE = '!(add-atom &self (eligible-lifecycle active))'


def fixture_atoms(match_fixed, lifecycle_fixed):
    atoms = [CAP_5FIELD if match_fixed else CAP_4FIELD, HANDLER_DEF]
    if lifecycle_fixed:
        atoms.append(ELIGIBLE_LIFECYCLE)
    return atoms


class Recorder:
    def __init__(self):
        self.lines = []

    def pr(self, s=""):
        print(s)
        self.lines.append(s)

    def log_only(self, s=""):
        self.lines.append(s)

    def text(self):
        return "\n".join(self.lines) + "\n"


REC = Recorder()


def pr(s=""):
    REC.pr(s)


def run(cmd, **kw):
    return subprocess.run(cmd, capture_output=True, text=True, timeout=TIMEOUT, **kw)


def strip_ansi(t):
    return re.sub(r'\x1b\[[0-9;]*m', '', t or "")


def container_running(container):
    try:
        p = run(["docker", "ps", "--filter", "name=" + container, "--format", "{{.Names}}"])
        return p.returncode == 0 and container in p.stdout
    except (subprocess.TimeoutExpired, FileNotFoundError):
        return False


def container_file_exists(container, path):
    try:
        p = run(["docker", "exec", container, "test", "-f", path])
        return p.returncode == 0
    except (subprocess.TimeoutExpired, FileNotFoundError):
        return False


_REGISTRY_BODY = {"text": None}


def fetch_registry_body(container, path):
    if _REGISTRY_BODY["text"] is not None:
        return _REGISTRY_BODY["text"]
    p = run(["docker", "exec", container, "sh", "-c", "cat " + path])
    body = p.stdout if (p.returncode == 0 and p.stdout) else None
    _REGISTRY_BODY["text"] = body
    return body


def eval_probe(container, registry_path, fixture, lines, label):
    body = fetch_registry_body(container, registry_path)
    if body is None:
        out, err = None, "could not read registry body: " + registry_path
    else:
        combined = (
            LIB_IMPORT_LINE + "\n"
            + ";; ===== REGISTRY DRAFT (inlined body) =====\n"
            + body + "\n"
            + ";; ===== FIXTURE ATOMS =====\n"
            + "\n".join(fixture) + "\n"
            + ";; ===== PROBE =====\n"
            + "\n".join(lines) + "\n"
        )
        path = "/tmp/_phase_d_coda_probe.metta"
        w = run(["docker", "exec", "-i", container, "sh", "-c", "cat > " + path],
                input=combined)
        if w.returncode != 0:
            out, err = None, "write failed: " + str(w.stderr)
        else:
            p = run(["docker", "exec", container, "sh", "-c",
                     "cd /PeTTa && " + RUN_SH + " " + path + " 2>&1"])
            out, err = p.stdout, None

    REC.log_only("\n" + "-" * 70)
    REC.log_only("PROBE: " + label)
    REC.log_only("-" * 70)
    REC.log_only("FIXTURE ATOMS:")
    for a in fixture:
        REC.log_only("  " + a)
    REC.log_only("PROBE LINES:")
    for ln in lines:
        REC.log_only("  " + ln)
    REC.log_only("RAW OUTPUT (ansi-stripped, full):")
    REC.log_only(strip_ansi(out) if out else ("(no output; err=" + str(err) + ")"))
    return out, err


def show_raw(out, n=6):
    if not out:
        print("    (no output)")
        return
    lines = [ln for ln in strip_ansi(out).splitlines() if ln.strip()]
    for ln in lines[-n:]:
        print("    " + ln)


def result_section(out):
    lines = strip_ansi(out or "").splitlines()
    last_sep = -1
    for i, ln in enumerate(lines):
        s = ln.strip()
        if s and set(s) == {"^"}:
            last_sep = i
    seg = lines[last_sep + 1:] if last_sep >= 0 else lines
    return [ln.strip() for ln in seg if ln.strip() and ln.strip() != "true"]


def result_text(out):
    return "\n".join(result_section(out))


def has_in_result(out, tok):
    return tok in result_text(out)


def is_unreduced(out, fname):
    sec = result_section(out)
    return any(re.search(r'\(\s*' + re.escape(fname) + r'\b', ln) for ln in sec)


def stage(name):
    pr("\n" + "=" * 70)
    pr(name)
    pr("=" * 70)


def verdict_line(label, ok):
    pr("  " + label.ljust(54) + " " + ("PASS" if ok else "FAIL"))
    return ok


def matrix_line(label, observed, expected, ok):
    pr("  " + label.ljust(40) + " observed=" + str(observed).ljust(7)
       + " expected=" + str(expected).ljust(7) + " [" + ("ok" if ok else "BAD") + "]")
    return ok


def probe_dispatch_then_capability_invoked():
    return ["!(dispatch (skill-request cycle: 1) 1)",
            "!(collapse (match &self (capability-invoked invocation-id: $iid "
            "handler: $h input-atom: $a) $h))"]


def handler_invoked(out):
    return has_in_result(out, "skill-discovery")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--container", default=DEFAULT_CONTAINER)
    ap.add_argument("--registry", default=DEFAULT_REGISTRY)
    ap.add_argument("--log-dir", default=".")
    args = ap.parse_args()
    c = args.container
    reg = args.registry
    results = {}

    ts = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    pr("=" * 70)
    pr("Phase D Coda verification (capability-registry dispatcher, pre-wiring)")
    pr("timestamp: " + ts + "   container: " + c)
    pr("=" * 70)
    REC.log_only("TRANSPORT: inline registry body (lib_import + draft body + fixture atoms).")
    REC.log_only("REGISTRY: " + reg)

    stage("STAGE 0  PREFLIGHT")
    if not container_running(c):
        pr("  [FAIL] container '" + c + "' not running. Start it and re-run.")
        _write_log(args, ts, c)
        sys.exit(1)
    pr("  [OK] container '" + c + "' running")
    if not container_file_exists(c, reg):
        pr("  [FAIL] registry draft not found at " + reg)
        _write_log(args, ts, c)
        sys.exit(1)
    pr("  [OK] registry: " + reg)
    body = fetch_registry_body(c, reg)
    if body is None:
        pr("  [FAIL] could not read registry body")
        _write_log(args, ts, c)
        sys.exit(1)
    draft_is_5field = "metadata: $m" in body
    pr("  [OK] registry body read (" + str(len(body)) + " chars)")
    pr("  draft dispatch matcher includes metadata field: " + str(draft_is_5field))
    if not draft_is_5field:
        pr("  [WARN] draft dispatch matcher lacks metadata: $m. match-FIXED cells will")
        pr("         fail because 'match fixed' depends on the FIXED draft. Apply the")
        pr("         draft fix first, then re-run.")

    # P-0 COUPLING INVARIANT (point 1)
    stage("P-0  COUPLING INVARIANT (dispatch matcher <-> registered shape)")
    pr("  The match itself is the invariant: assert the 5-field shape is matchable")
    pr("  and that the old 4-field pattern does NOT match it (mismatch was real).")
    out, _ = eval_probe(
        c, reg, fixture_atoms(True, True),
        ["!(collapse (match &self (registered-capability schema: $s handler: $h "
         "priority: $p lifecycle: $l metadata: $m) $h))"],
        "P-0 coupling: 5-field registered-capability matchable")
    print("  P-0 5-field RAW (tail):")
    show_raw(out)
    p0_5field_ok = has_in_result(out, "skill-discovery")
    out4, _ = eval_probe(
        c, reg, fixture_atoms(True, True),
        ["!(collapse (match &self (registered-capability schema: $s handler: $h "
         "priority: $p lifecycle: $l) $h))"],
        "P-0 coupling: 4-field pattern against 5-field atom (expect empty)")
    print("  P-0 4-field-vs-5-field RAW (tail):")
    show_raw(out4)
    p0_4field_empty = not has_in_result(out4, "skill-discovery")
    verdict_line("5-field pattern matches 5-field atom", p0_5field_ok)
    verdict_line("4-field pattern does NOT match (mismatch real)", p0_4field_empty)
    results["P-0 coupling invariant"] = verdict_line(
        "P-0 coupling (the joint dispatch depends on)", p0_5field_ok and p0_4field_empty)

    # DEFECT-ISOLATION MATRIX (point 3)
    stage("DEFECT-ISOLATION MATRIX (match-shape x eligible-lifecycle)")
    pr("  Against the FIXED draft, only the both-fixed cell should invoke. Each")
    pr("  single-fix cell stays blocked: the two defects are independent.")
    cells = [
        ("A match-BROKEN  lifecycle-BROKEN", False, False, False),
        ("B match-FIXED   lifecycle-BROKEN", True, False, False),
        ("C match-BROKEN  lifecycle-FIXED", False, True, False),
        ("D match-FIXED   lifecycle-FIXED", True, True, True),
    ]
    matrix_ok = True
    cell_observed = {}
    for label, mfix, lfix, expect in cells:
        out, _ = eval_probe(c, reg, fixture_atoms(mfix, lfix),
                            probe_dispatch_then_capability_invoked(), "MATRIX " + label)
        print("  " + label + " RAW (tail):")
        show_raw(out, 4)
        observed = handler_invoked(out)
        cell_observed[label[0]] = observed
        matrix_ok = matrix_line(label, observed, expect, observed == expect) and matrix_ok
    results["MATRIX defect isolation"] = verdict_line(
        "defect-isolation matrix (only both-fixed invokes)", matrix_ok)
    results["P-1/P-3 via matrix cell D (handler runs)"] = verdict_line(
        "both-fixed cell invokes handler", cell_observed.get("D") is True)

    # P-2 dispatch fires
    stage("P-2  DISPATCH FIRES (dispatch-invocation, unconditional)")
    out, _ = eval_probe(c, reg, fixture_atoms(True, True),
                        ["!(dispatch (skill-request cycle: 1) 1)",
                         "!(collapse (match &self (dispatch-invocation invocation-id: $iid "
                         "input-atom: $a) $iid))"],
                        "P-2 dispatch then read dispatch-invocation")
    print("  dispatch-invocation read RAW (tail):")
    show_raw(out)
    p2_ok = has_in_result(out, "1") and not is_unreduced(out, "dispatch")
    results["P-2 dispatch fires"] = verdict_line(
        "dispatch-invocation present after dispatch", p2_ok)

    # P-7 with CONTROL-PRECONDITION GATE (point 2)
    stage("P-7  FILTER-STEP EXTENSIBILITY (with control-precondition gate)")
    out_ctrl, _ = eval_probe(c, reg, fixture_atoms(True, True),
                             probe_dispatch_then_capability_invoked(),
                             "P-7 CONTROL precondition (no extra step, expect invoked)")
    print("  control-precondition RAW (tail):")
    show_raw(out_ctrl, 4)
    control_fires = handler_invoked(out_ctrl)
    verdict_line("control precondition: handler invoked, no extra step", control_fires)
    if not control_fires:
        pr("  >>> CONTROL PRECONDITION FAILED. The path under test does not fire even")
        pr("  in the control case, so P-7a/P-7b cannot distinguish a working filter step")
        pr("  from an upstream block. Marking both INVALID (not a coincidence pass).")
        results["P-7a passthrough (INVALID: control did not fire)"] = False
        results["P-7b block->fallback (INVALID: control did not fire)"] = False
    else:
        out, _ = eval_probe(
            c, reg, fixture_atoms(True, True),
            ['!(add-atom &self (= (test-passthrough-filter-step $entry) $entry))',
             '!(add-atom &self (capability-filter-step order: 25 step: test-passthrough-filter-step))']
            + probe_dispatch_then_capability_invoked(),
            "P-7a passthrough filter step (expect still invoked)")
        print("  passthrough RAW (tail):")
        show_raw(out, 4)
        results["P-7a filter passthrough"] = verdict_line(
            "passthrough step added, handler still invoked", handler_invoked(out))

        out, _ = eval_probe(
            c, reg, fixture_atoms(True, True),
            ['!(add-atom &self (= (test-block-filter-step $entry) filtered-out))',
             '!(add-atom &self (capability-filter-step order: 26 step: test-block-filter-step))',
             "!(dispatch (skill-request cycle: 1) 1)",
             "!(collapse (match &self (dispatch-fallback-activated invocation-id: $i "
             "input-atom: $a reason: $r) $r))",
             "!(collapse (match &self (capability-invoked invocation-id: $iid "
             "handler: $h input-atom: $a) $h))"],
            "P-7b block filter step (expect fallback, handler NOT invoked)")
        print("  block RAW (tail):")
        show_raw(out, 5)
        fallback_fired = has_in_result(out, "no-matching-capability")
        handler_blocked = not has_in_result(out, "skill-discovery")
        pr("  fallback fired: " + str(fallback_fired) + "   handler blocked: "
           + str(handler_blocked) + "   (control fired -> differential valid)")
        results["P-7b filter block -> fallback"] = verdict_line(
            "block routes to fallback, handler NOT invoked", fallback_fired and handler_blocked)

    stage("OBSERVATIONAL CRITERIA (post-Phase-C; not run here)")
    pr("  P-4 (CHARS_SENT / encoded-skills parity): PRE-CONDITION-NOT-MET")
    pr("  P-5 (LLM behavior parity):               PRE-CONDITION-NOT-MET")
    pr("  P-6 (Criterion-5 silent chain term.):    PRE-CONDITION-NOT-MET")

    stage("SUMMARY")
    for k, v in results.items():
        pr("  " + k.ljust(48) + " " + ("PASS" if v else "FAIL"))
    allp = all(results.values())
    pr("")
    if allp:
        pr("  >>> DISPATCHER SUBSTRATE VALIDATED (on fixture atoms).")
        pr("  Coupling holds (P-0); the two defects are isolated and only the")
        pr("  both-fixed cell dispatches (matrix); dispatch fires (P-2); the filter")
        pr("  pipeline passes through and blocks to fallback with a control")
        pr("  precondition proving the differential is real (P-7).")
    else:
        pr("  >>> NOT FULLY VALIDATED. Read each RAW block against its verdict. If a")
        pr("  match-FIXED matrix cell did not invoke, confirm the draft carries the")
        pr("  5-field dispatch matcher. If the control precondition failed, P-7 is")
        pr("  INVALID by design (not a coincidence pass).")

    _write_log(args, ts, c)
    if not allp:
        sys.exit(3)


def _write_log(args, ts, container):
    fname = "phase_d_coda_verification_" + ts + ".log"
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
