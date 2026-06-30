#!/usr/bin/env python3
"""
proceed_voice_harness.py

Validates the Extension B substrate (soul/proceed_voice.metta) in the live
container, cold, BEFORE any loop wiring. Hands only: it builds expressions, runs
them via run.sh, parses output, and compares to references computed in Python. It
never composes any voice; the references check the substrate only.

RESULTS ARTIFACT: every run writes a timestamped log to the host (--log-dir,
default ".") AND to the container /tmp/. The log captures, per probe, the EXACT
script sent (test lines) and the COMPLETE raw output (the metta-to-prolog
compilation trace plus the eval results), not just the console tail. The console
stays readable (tails + verdicts); the log is the durable record to diff across
iterations.

DISCIPLINE (the shared ethic, see ClarityOmega_Build_Verification_Ethic.md):
  - HANDS ONLY. Python builds and checks; it never computes the cognition.
  - RAW OUTPUT BEFORE EVERY VERDICT.
  - UNREDUCED DETECTION in the result section only (and tolerant of names ending
    in '?', which the discriminator and gate predicates use).
  - INLINE BODIES, not import!. A one-shot run.sh compiles inline (= ...) defs to
    reducible clauses but does not register import!-ed rules for top-level ! eval.
    The host soul/ maps to the runtime soul/ dir, so a file dropped in soul/ is
    already at the container soul path. All three bodies (cycle_classifier,
    soul_utils, proceed_voice) are read from the CONTAINER. proceed_voice.metta is
    present in soul/ but NOT yet imported in lib_clarity_reasoning, so it is cold
    (defined, queryable, but not wired into the loop). Validating it needs no flag
    and no rebuild: just place it in soul/ (SOP) and run.
  - FRESH SPACE PER CALL. Inputs are built with sread (faithful to loop line 132,
    where $sexpr is sread of the LLM output), so command lists are data, never
    evaluated as calls. The input instrument is confirmed in STAGE 0 first.
  - PREFLIGHT distinguishes substrate-wrong from substrate-absent.

WHAT THIS DOES NOT TEST (the harness / in-loop boundary, named not blurred):
  - compose-proceed-voice's full path makes a live soul-llm-call. That LLM
    round-trip is an IN-LOOP test, not a cold harness test, and is omitted here.
  - Whether the py-call bridges (string-contains -> soul_governance.contains_token,
    soul-extract-soul-note -> helper.extract_after) resolve under one-shot run.sh
    is itself an UNKNOWN. STAGE 1 probes it. If the bridges do not reduce cold, the
    binding-gate functions (STAGE 3) are in-loop-only, and the harness says so
    rather than reporting a misleading FAIL. The pure discriminator and payload
    functions (STAGE 2) do not use py-call and are testable regardless.
  - Import registration / boot wiring is a separate boot test, not this harness.

USAGE (run on the host, from repo root):
  python3 staging/proceed_voice_harness.py
        [--container clarity_omega]
        [--log-dir .]

  Prerequisite: proceed_voice.metta placed in soul/ (SOP). No path flag needed.
"""

import argparse
import datetime
import os
import re
import subprocess
import sys

DEFAULT_CONTAINER = "clarity_omega"
RUN_SH = "./run.sh"
TIMEOUT = 60

# All three bodies read from the CONTAINER (host soul/ maps to the runtime soul/ dir,
# so a file placed in soul/ is already at the container soul path).
CYCLE_CLASSIFIER = "/PeTTa/repos/omegaclaw/soul/cycle_classifier.metta"
SOUL_UTILS = "/PeTTa/repos/omegaclaw/soul/soul_utils.metta"
PROCEED_VOICE = "/PeTTa/repos/omegaclaw/soul/proceed_voice.metta"

# Arms the import system; carries no rules we evaluate. Defensive, harmless.
LIB_IMPORT_LINE = "!(import! &self (library lib_import))"


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
# Container plumbing
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


def fetch_container_body(container, path):
    """Read a file body from the container. Returns text or None."""
    p = run(["docker", "exec", container, "sh", "-c", "cat " + path])
    return p.stdout if (p.returncode == 0 and p.stdout) else None


def assemble_bodies(container):
    """Build the inlined definition block: lib_import, then the three file bodies, all
    read from the container. Returns (block, missing)."""
    parts = [LIB_IMPORT_LINE]
    missing = []
    for path in (CYCLE_CLASSIFIER, SOUL_UTILS, PROCEED_VOICE):
        b = fetch_container_body(container, path)
        if b is None:
            missing.append(path)
        else:
            parts.append(b)
    return "\n".join(parts), missing


_BLOCK_CACHE = {}


def eval_in_container(container, block, lines, label="probe"):
    """Concatenate the inlined block + the body lines, write to a temp file, run via
    run.sh. Record the exact body lines and the COMPLETE raw output to the log."""
    script = block + "\n" + "\n".join(lines) + "\n"
    path = "/tmp/_proceed_voice_harness.metta"
    w = run(["docker", "exec", "-i", container, "sh", "-c", "cat > " + path], input=script)
    if w.returncode != 0:
        out, err = None, "write failed: " + str(w.stderr)
    else:
        p = run(["docker", "exec", container, "sh", "-c",
                 "cd /PeTTa && " + RUN_SH + " " + path + " 2>&1"])
        out, err = p.stdout, None

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
# Parsers (lenient; the raw output is the source of truth)
# ---------------------------------------------------------------------------

def tail(out, n=6):
    return [ln for ln in strip_ansi(out).splitlines() if ln.strip()][-n:]


def show_raw(out, n=6):
    if not out:
        print("    (no output)")
        return
    for ln in tail(out, n):
        print("    " + ln)


def result_section(out):
    """Lines after the LAST caret separator: the actual reduction result(s). Do NOT
    drop lines equal to 'true'. The prolog goal-success marker 'true' appears FIRST
    here and the real result LAST, so a boolean function that legitimately returns
    'true' would be erased if we filtered 'true' (the bug that false-failed
    lone-send-proceed?). Callers take the LAST line as the result; is_unreduced and
    token checks scan all lines, and the leading goal 'true' is harmless to both."""
    lines = strip_ansi(out or "").splitlines()
    last_sep = -1
    for i, ln in enumerate(lines):
        s = ln.strip()
        if s and set(s) == {"^"}:
            last_sep = i
    seg = lines[last_sep + 1:] if last_sep >= 0 else lines
    return [ln.strip() for ln in seg if ln.strip()]


def last_result(out):
    sec = result_section(out)
    if not sec:
        return ""
    r = sec[-1]
    if r.startswith("[") and r.endswith("]"):
        r = r[1:-1].strip()
    return r


def is_unreduced(out, fname):
    """A reduced call yields a value in the result section; an unreduced call echoes
    the bare (fname ...) term there. Scan ONLY the result section. The match tolerates
    names ending in '?': after the name we require whitespace or a close-paren, NOT a
    word boundary (\\b fails between '?' and a space)."""
    sec = result_section(out)
    pat = r'\(\s*' + re.escape(fname) + r'(\s|\))'
    return any(re.search(pat, ln) for ln in sec)


def is_py_error(out):
    """A py-call into an unavailable module raises a Python error rather than echoing
    an unreduced term. Detect it as its own class so a bridge that errors under
    one-shot run.sh is not mistaken for either a pass or a mere non-reduction."""
    sec = result_section(out)
    return any(("ModuleNotFoundError" in ln) or ("Error'" in ln) or ln.startswith("ERROR:")
               for ln in sec)


def py_error_detail(out):
    for ln in result_section(out):
        if "ModuleNotFoundError" in ln or "No module named" in ln:
            return ln
    return ""


def last_bool(out):
    """PeTTa renders booleans lowercase. Read the final result line only."""
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


def has_token(out, tok):
    return tok in strip_ansi(out or "")


def result_has_token(out, tok):
    return any(tok in ln for ln in result_section(out))


def last_int(out):
    nums = re.findall(r'-?\d+', last_result(out))
    return int(nums[-1]) if nums else None


# ---------------------------------------------------------------------------
# Input construction: sread, faithful to loop line 132 ($sexpr = sread of output)
# ---------------------------------------------------------------------------

def sread_cmds(src):
    """Return a MeTTa (sread "...") call that parses a command-list source string into
    data, mirroring how the loop builds $sexpr. Quotes and backslashes are escaped so
    the source survives as a MeTTa string literal."""
    esc = src.replace('\\', '\\\\').replace('"', '\\"')
    return '(sread "' + esc + '")'


def call_with_cmds(fn, decision, cmds_src):
    """Build !(let $cmds (sread "...") (fn decision $cmds)) for a 2-arg (decision cmds)
    predicate, or !(let $cmds (sread "...") (fn $cmds)) when decision is None."""
    sr = sread_cmds(cmds_src)
    if decision is None:
        return '!(let $cmds ' + sr + ' (' + fn + ' $cmds))'
    return '!(let $cmds ' + sr + ' (' + fn + ' ' + decision + ' $cmds))'


# ---------------------------------------------------------------------------
# Stage scaffolding
# ---------------------------------------------------------------------------

def stage(title):
    pr("")
    pr("=" * 64)
    pr(title)
    pr("=" * 64)


def verdict_line(label, ok):
    pr("  [" + ("PASS" if ok else "FAIL") + "] " + label)
    return ok


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--container", default=DEFAULT_CONTAINER)
    ap.add_argument("--log-dir", default=".")
    args = ap.parse_args()
    c = args.container
    ts = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")

    pr("=" * 64)
    pr("proceed_voice.metta cold substrate harness")
    pr("=" * 64)

    # PREFLIGHT
    stage("PREFLIGHT")
    if not container_running(c):
        pr("  [FAIL] container '" + c + "' not running. Start it and re-run.")
        sys.exit(1)
    pr("  [OK] container '" + c + "' running")

    block, missing = assemble_bodies(c)
    if missing:
        pr("  [FAIL] could not read these bodies from the container:")
        for m in missing:
            pr("         " + m)
        pr("  All three live in soul/ (host soul/ maps to the runtime soul/ dir). If")
        pr("  proceed_voice.metta is the missing one, confirm it is in soul/. If soul/")
        pr("  needs a rebuild to sync, run: docker compose build --no-cache clarityclaw")
        pr("  && docker compose up -d clarityclaw")
        sys.exit(1)
    pr("  [OK] inlined bodies assembled (" + str(len(block)) + " chars):")
    pr("       cycle_classifier + soul_utils + proceed_voice (all from container soul/)")

    results = {}

    # STAGE 0: input instrument. Confirm sread + the count idiom before trusting any
    # result that depends on them (read the instrument first). NOTE: superpose does
    # NOT evaluate its argument; (superpose (sread "...")) iterates the literal tuple
    # (sread "...") and never parses. So bind sread first, then superpose the bound
    # parsed list. This mirrors how the real functions receive $cmds already bound.
    stage("STAGE 0  INPUT INSTRUMENT (sread bound, then count idiom)")
    out, _ = eval_in_container(c, block, [
        '!(let $p ' + sread_cmds('((send "hi"))') + ' (size-atom (collapse (superpose $p))))',
    ], label="STAGE 0 lone count == 1")
    print("  lone-list count RAW (tail):"); show_raw(out, 4)
    n1 = last_int(out)
    out, _ = eval_in_container(c, block, [
        '!(let $p ' + sread_cmds('((send "hi") (metta "x"))') + ' (size-atom (collapse (superpose $p))))',
    ], label="STAGE 0 two-cmd count == 2")
    print("  two-cmd count RAW (tail):"); show_raw(out, 4)
    n2 = last_int(out)
    out, _ = eval_in_container(c, block, [
        '!(car-atom ' + sread_cmds('((send "hi"))') + ')',
    ], label="STAGE 0 car-atom is the command")
    print("  car-atom RAW (tail):"); show_raw(out, 4)
    car_ok = result_has_token(out, "send") and result_has_token(out, "hi") and not is_unreduced(out, "sread")
    instrument_ok = (n1 == 1) and (n2 == 2) and car_ok
    pr("    counts: lone=" + str(n1) + " (expect 1), two=" + str(n2) + " (expect 2); car-atom ok=" + str(car_ok))
    results["instrument"] = verdict_line(
        "sread bound then count idiom gives 1 and 2; car-atom is the command",
        instrument_ok)
    if not instrument_ok:
        pr("  Instrument is not solid. Every later result depends on it; resolve first.")

    # STAGE 1: py-bridge reachability probe (the key unknown). Three outcomes per
    # bridge: reduces to a value, echoes unreduced, or raises a Python error (an
    # unavailable module). The last is NOT a pass and NOT a mere non-reduction.
    stage("STAGE 1  PY-BRIDGE REACHABILITY (string-contains, soul-extract-soul-note)")
    out, _ = eval_in_container(c, block, [
        '!(string-contains "VERDICT: PROCEED SOUL-TONE: grounded" "SOUL-TONE: grounded")',
        '!(string-contains "VERDICT: PROCEED SOUL-TONE: firm" "SOUL-TONE: grounded")',
    ], label="STAGE 1 string-contains pos/neg")
    print("  string-contains RAW (tail):"); show_raw(out, 6)
    sc_unreduced = is_unreduced(out, "string-contains")
    sc_error = is_py_error(out)
    out2, _ = eval_in_container(c, block, [
        '!(soul-extract-soul-note "VERDICT: PROCEED SOUL-NOTE: stay with the uncertainty")',
    ], label="STAGE 1 soul-extract-soul-note")
    print("  soul-extract-soul-note RAW (tail):"); show_raw(out2, 6)
    sn_unreduced = is_unreduced(out2, "soul-extract-soul-note")
    sn_error = is_py_error(out2)
    bridge_ok = ((not sc_unreduced) and (not sn_unreduced)
                 and (not sc_error) and (not sn_error)
                 and result_has_token(out2, "uncertainty"))
    if bridge_ok:
        results["py_bridge"] = verdict_line(
            "py-call bridges reduce under run.sh (binding gate is harness-testable)", True)
    elif sc_error or sn_error:
        pr("  [DEFER -> IN-LOOP] py-call bridges error under one-shot run.sh:")
        pr("            string-contains: " + (py_error_detail(out) or "(no py error)"))
        pr("            soul-extract-soul-note: " + (py_error_detail(out2) or "(no py error)"))
        pr("            The Python modules (soul_governance, helper) are not importable")
        pr("            in the one-shot run.sh context; in the live loop they ARE loaded.")
        pr("            This is a DISCOVERY, not a substrate bug. The binding gate")
        pr("            (STAGE 3) is IN-LOOP-ONLY. STAGE 2 pure functions are unaffected.")
        results["py_bridge"] = "DEFER"
    else:
        pr("  [INSPECT] bridges neither reduced to the expected value nor errored cleanly.")
        pr("            string-contains unreduced: " + str(sc_unreduced) +
           ", soul-extract-soul-note unreduced: " + str(sn_unreduced) +
           ", note token present: " + str(result_has_token(out2, "uncertainty")))
        pr("            Read the two RAW blocks above before trusting any STAGE 3 result.")
        results["py_bridge"] = False

    # STAGE 2: pure discriminator + payload (no py-call; testable regardless).
    stage("STAGE 2  PURE DISCRIMINATOR + PAYLOAD (lone-send, send-payload, rewrite)")

    pure = True

    # lone-send-proceed? : five scenarios, both polarities.
    for label, decision, cmds_src, expect in [
        ("proceed + lone send", "proceed", '((send "hi"))', True),
        ("proceed + two commands", "proceed", '((send "hi") (metta "x"))', False),
        ("proceed + lone non-send", "proceed", '((metta "x"))', False),
        ("pause + lone send", "pause", '((send "hi"))', False),
        ("proceed + empty (cornered/paused)", "proceed", '()', False),
    ]:
        out, _ = eval_in_container(c, block, [call_with_cmds("lone-send-proceed?", decision, cmds_src)],
                                   label="STAGE 2 lone-send-proceed? " + label)
        print("  " + label + " RAW (tail):"); show_raw(out, 3)
        got = last_bool(out)
        unred = is_unreduced(out, "lone-send-proceed?")
        ok = (got is expect) and not unred
        pr("    got: " + str(got) + "  expect: " + str(expect) + "  unreduced: " + str(unred) +
           "  [" + ("ok" if ok else "BAD") + "]")
        pure = pure and ok
    results["lone_send"] = verdict_line("lone-send-proceed? correct on all five scenarios", pure)

    # send-payload : extract the drafted text from the lone send.
    out, _ = eval_in_container(c, block, [call_with_cmds("send-payload", None, '((send "hello world"))')],
                               label="STAGE 2 send-payload")
    print("  send-payload RAW (tail):"); show_raw(out, 3)
    sp_ok = result_has_token(out, "hello world") and not is_unreduced(out, "send-payload")
    results["send_payload"] = verdict_line("send-payload extracts the drafted text", sp_ok)

    # extract-send-arg : the head destructure in isolation.
    out, _ = eval_in_container(c, block, ['!(let $c ' + sread_cmds('(send "x")') + ' (extract-send-arg $c))'],
                               label="STAGE 2 extract-send-arg")
    print("  extract-send-arg RAW (tail):"); show_raw(out, 3)
    ea_ok = result_has_token(out, "x") and not is_unreduced(out, "extract-send-arg")
    results["extract_send_arg"] = verdict_line("extract-send-arg destructures the send command", ea_ok)

    # rewrite-send-payload : rebuild the one-command tuple with new text.
    out, _ = eval_in_container(c, block,
        ['!(let $cmds ' + sread_cmds('((send "old"))') + ' (rewrite-send-payload $cmds "new"))'],
        label="STAGE 2 rewrite-send-payload")
    print("  rewrite-send-payload RAW (tail):"); show_raw(out, 3)
    rw_ok = (result_has_token(out, "send") and result_has_token(out, "new")
             and not result_has_token(out, "old") and not is_unreduced(out, "rewrite-send-payload"))
    results["rewrite_send_payload"] = verdict_line(
        "rewrite-send-payload rebuilds ((send <new>)), old text gone", rw_ok)

    # STAGE 3: binding gate (conditional on STAGE 1 bridge reachability).
    stage("STAGE 3  BINDING GATE (at-base-stance?, soul-note-present?, binding-work-exists?)")
    if not bridge_ok:
        pr("  [DEFER -> IN-LOOP] py-call bridges are cold-unavailable (STAGE 1).")
        pr("  binding-work-exists? depends on string-contains and soul-extract-soul-note,")
        pr("  so its cold validation is not possible here; it moves to the in-loop test.")
        pr("  Recording as DEFER, not PASS and not FAIL.")
        results["binding_gate"] = "DEFER"
    else:
        gate = True
        for label, fn, verdict, expect in [
            ("at-base-stance? grounded", "at-base-stance?", "VERDICT: PROCEED SOUL-TONE: grounded", True),
            ("at-base-stance? firm", "at-base-stance?", "VERDICT: PROCEED SOUL-TONE: firm", False),
            ("soul-note-present? with note", "soul-note-present?",
             "VERDICT: PROCEED SOUL-TONE: grounded SOUL-NOTE: stay with it", True),
            ("soul-note-present? no note", "soul-note-present?", "VERDICT: PROCEED SOUL-TONE: grounded", False),
            ("binding gate: grounded + no note -> skip", "binding-work-exists?",
             "VERDICT: PROCEED SOUL-TONE: grounded", False),
            ("binding gate: firm + no note -> fire", "binding-work-exists?",
             "VERDICT: PROCEED SOUL-TONE: firm", True),
            ("binding gate: grounded + note -> fire", "binding-work-exists?",
             "VERDICT: PROCEED SOUL-TONE: grounded SOUL-NOTE: stay with it", True),
        ]:
            out, _ = eval_in_container(c, block, ['!(' + fn + ' "' + verdict + '")'],
                                       label="STAGE 3 " + label)
            print("  " + label + " RAW (tail):"); show_raw(out, 3)
            got = last_bool(out)
            unred = is_unreduced(out, fn)
            ok = (got is expect) and not unred
            pr("    got: " + str(got) + "  expect: " + str(expect) + "  unreduced: " + str(unred) +
               "  [" + ("ok" if ok else "BAD") + "]")
            gate = gate and ok
        results["binding_gate"] = verdict_line(
            "binding gate detects delta from base rhythm (grounded), fires on note or non-base", gate)

    # SUMMARY
    stage("SUMMARY")

    def status(v):
        if v == "DEFER":
            return "DEFER"
        return "PASS" if v else "FAIL"

    for k, v in results.items():
        pr("  " + k.ljust(22) + " " + status(v))
    cold = {k: v for k, v in results.items() if v != "DEFER"}
    deferred = [k for k, v in results.items() if v == "DEFER"]
    allp = all(bool(v) for v in cold.values())
    pr("")
    if allp:
        pr("  >>> PROCEED_VOICE SUBSTRATE VALIDATED (cold-testable parts, synthetic inputs).")
        pr("  Every cold-testable function reduced correctly. Deferred to in-loop (by")
        pr("  design, not failure): " + (", ".join(deferred) if deferred else "(none)") + ".")
        pr("  The deferred items depend on py-call bridges (helper, soul_governance) that")
        pr("  are not importable under one-shot run.sh but ARE loaded in the live loop.")
        pr("  Also not tested here: compose-proceed-voice's soul-llm-call round-trip and")
        pr("  import registration (boot test). Next: Step 2 Python fixtures, then the")
        pr("  reversible helper-append apply, the loop-wiring apply, then in-loop.")
    else:
        pr("  >>> NOT FULLY VALIDATED. Read each RAW block in the log against its verdict.")
        pr("  An unreduced (function ...) echo in the result section means that function")
        pr("  did not fire. A py-call error (ModuleNotFoundError) means a bridge is cold-")
        pr("  unavailable, which is DEFER not FAIL. A None where a bool was expected often")
        pr("  means the result parser dropped the result line, not a substrate fault: read")
        pr("  the raw. Check inlined bodies (STAGE 0), the dependency cat, and the shape")
        pr("  against Atom_Operations_Map.")

    _write_log(args, ts, c)
    if not allp:
        sys.exit(3)


def _write_log(args, ts, container):
    fname = "proceed_voice_harness_" + ts + ".log"
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
