#!/usr/bin/env python3
"""
soul_namespace_discovery_diagnostic.py

Discovery harness for the namespace-check candidates. Modeled on
capability_registry_diagnostic.py and soul_mutation_gate_diagnostic.py: drives
the clarity_omega container via run.sh, evaluates the discovery harness, parses
the trailing result block, and reports what each primitive returned plus whether
the registry-match candidate discriminates.

This is a DISCOVERY run, not strict pass/fail: TEST 1-4 reveal which native
char/symbol primitives exist (deciding Candidate 1); TEST 5-11 prove whether the
registry-match candidate (Candidate 2, proven-idiom only) discriminates soul vs
non-soul targets. The proof log captures everything so the choice is factual.

USAGE (host with docker):
  python3 soul_namespace_discovery_diagnostic.py
  Optional: --container, --harness, --keep-temp

Writes /tmp/soul_lock_emptiness_log_<ts>.log in the container
(maps to host shared_files/) with the loaded input, raw atomspace output, and
the per-test interpretation.
"""
import argparse
import datetime
import re
import subprocess
import sys

DEFAULT_CONTAINER = "clarity_omega"
DEFAULT_HARNESS = "/PeTTa/repos/omegaclaw/soul/soul_lock_emptiness_harness.metta"


def run(cmd):
    p = subprocess.run(cmd, capture_output=True, text=True)
    return p.returncode, p.stdout, p.stderr


def container_running(container):
    rc, out, _ = run(["docker", "ps", "--filter", f"name={container}",
                      "--format", "{{.Names}}"])
    return rc == 0 and container in out


def container_file_exists(container, path):
    rc, _, _ = run(["docker", "exec", container, "test", "-f", path])
    return rc == 0


def build_combined(container, harness_path):
    rc, harn, err = run(["docker", "exec", container, "cat", harness_path])
    if rc != 0:
        return None, f"could not read harness: {err}"
    combined = (
        ";; ===== LIBRARY BOOTSTRAP =====\n"
        "!(import! &self (library lib_import))\n"
        ";; ===== DISCOVERY HARNESS =====\n"
        + harn + "\n"
    )
    return combined, None


def evaluate(container, combined_text, keep_temp):
    ts = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    temp_path = f"/tmp/soul_lock_emptiness_combined_{ts}.metta"
    p = subprocess.run(
        ["docker", "exec", "-i", container, "sh", "-c", f"cat > {temp_path}"],
        input=combined_text, text=True, capture_output=True)
    if p.returncode != 0:
        return None, ts, None, f"failed to write temp: {p.stderr}"
    rc, out, err = run(["docker", "exec", container, "sh", "-c",
                        f"cd /PeTTa && ./run.sh {temp_path} 2>&1"])
    if not keep_temp:
        run(["docker", "exec", container, "rm", "-f", temp_path])
    return out, ts, rc, None


def strip_ansi(text):
    return re.sub(r'\x1b\[[0-9;]*m', '', text)


def parse_results(output):
    """
    Extract inline-tagged results. Each tested expression was wrapped as
    (RESULT-N <value>), so the evaluated value prints as (RESULT-N <value>) in
    the trailing block. We find every RESULT-N occurrence and take its value.

    Because the evaluator may render the tagged result either as a bare
    '(RESULT-5 1)' value line OR echo it in a goal, we scan ALL lines for the
    pattern 'RESULT-N' followed by its value, and keep the LAST occurrence for
    each N (the reduced value prints after the echoes). Position-independent and
    immune to println/add-atom acks (those carry no RESULT- tag).
    """
    output = strip_ansi(output)
    text = output

    results = {}
    # Match (RESULT-<n> <value>) allowing multiline value up to the matching
    # close paren at the same depth. Simpler robust approach: find each
    # 'RESULT-<n>' token, then capture the balanced parenthetical value after it.
    for m in re.finditer(r'RESULT-(\d+)', text):
        n = m.group(1)
        # Walk from just after the tag to capture the value token(s) until the
        # paren that closes the RESULT wrapper. The wrapper opened with '(' just
        # before 'RESULT-N'. Find that open paren, then balance.
        tag_start = m.start()
        # find the '(' immediately preceding the tag (allowing whitespace)
        i = tag_start - 1
        while i >= 0 and text[i] in " \t":
            i -= 1
        if i < 0 or text[i] != "(":
            continue
        open_idx = i
        # balance from open_idx
        depth = 0
        j = open_idx
        in_str = False
        esc = False
        end_idx = None
        while j < len(text):
            c = text[j]
            if in_str:
                if esc:
                    esc = False
                elif c == "\\":
                    esc = True
                elif c == '"':
                    in_str = False
            else:
                if c == '"':
                    in_str = True
                elif c == "(":
                    depth += 1
                elif c == ")":
                    depth -= 1
                    if depth == 0:
                        end_idx = j
                        break
            j += 1
        if end_idx is None:
            continue
        inner = text[open_idx + 1:end_idx]  # 'RESULT-N <value>'
        val = inner[len("RESULT-" + n):].strip()
        # keep the LAST occurrence (reduced value prints after echoes)
        results[n] = " ".join(val.split())
    return results


# Lock-emptiness interpretation.
INTERP = [
    ("1", "exists_num", None, "A string_length reduces to a number?"),
    ("2", "exists_num", None, "A string-length (hyphen) reduces?"),
    ("3", "exists_num", None, "A length reduces?"),
    ("4", "exists_num", None, "A size-atom on a string reduces?"),
    ("5", "true",  None, "B structural lock clear: == unlocked -> True"),
    ("6", "false", None, "B pending? when clear -> False"),
    ("7", "true",  None, "B pending? when held -> True"),
    ("8", "value", None, "B get-state after held -> (locked soul-note)?"),
    ("9", "false", None, "B pending? after reclear -> False"),
    ("10", "true",  None, "C == empty string when clear -> True"),
    ("11", "false", None, "C == empty string when held -> False (may be unreliable)"),
]


def interpret(results):
    rows = []
    for n, kind, exp, human in INTERP:
        v = results.get(n)
        if v is None:
            rows.append((f"RESULT-{n}", "NO-RESULT", human, "tag not found (run may have halted before here)"))
            continue
        if kind == "exists_num":
            # reduces to a number if v is an int string; absent if echoed unreduced
            isnum = v.lstrip("-").isdigit()
            rows.append((f"RESULT-{n}", "REDUCES" if isnum else "ABSENT", human,
                         (f"-> {v}" if isnum else f"unreduced: {v}")))
        elif kind == "true":
            rows.append((f"RESULT-{n}", "PASS" if v.lower()=="true" else "FAIL", human, f"got {v!r}"))
        elif kind == "false":
            ok = v.lower()=="false" or v.startswith("(")
            rows.append((f"RESULT-{n}", "PASS" if ok else "FAIL", human, f"got {v!r}"))
        elif kind == "value":
            rows.append((f"RESULT-{n}", "VALUE", human, f"returned: {v}"))
    return rows


def candidate_verdict(rows):
    by = {r[0]: r[1] for r in rows}
    a_works = any(by.get(f"RESULT-{t}")=="REDUCES" for t in ("1","2","3","4"))
    b_works = all(by.get(f"RESULT-{t}")=="PASS" for t in ("5","6","7","9"))
    c_works = by.get("RESULT-10")=="PASS" and by.get("RESULT-11")=="PASS"
    lines = []
    a_which = [t for t in ("1","2","3","4") if by.get(f"RESULT-{t}")=="REDUCES"]
    lines.append(f"DIRECTION A (string-length primitive): " +
                 (f"REDUCES via RESULT-{','.join(a_which)}" if a_works else "NONE reduce, no native string-length"))
    lines.append("DIRECTION B (structural atom-lock): " +
                 ("WORKS, == against unlocked/locked discriminates, NO string ops" if b_works
                  else "did not fully pass, inspect"))
    lines.append("DIRECTION C (== empty string): " +
                 ("both reduce correctly" if c_works else "unreliable or absent, inspect"))
    if b_works:
        lines.append(">>> USE DIRECTION B: lock holds an atom (unlocked / (locked x)); "
                     "pending = NOT (== state unlocked). No string layer, consistent with proven idioms. "
                     "This replaces the string_length form that halted the full-gate run.")
    elif a_works:
        lines.append(">>> Direction A: a string-length primitive exists; use it in place of string_length.")
    elif c_works:
        lines.append(">>> Direction C: == empty-string reduces; usable if non-empty case is also reliable here.")
    else:
        lines.append(">>> No clean lock-emptiness test found; inspect raw output.")
    return lines


def write_log(container, ts, combined, raw, rc, rows, cand_lines):
    log_path = f"/tmp/soul_lock_emptiness_log_{ts}.log"
    L = ["=" * 70, "SOUL LOCK EMPTINESS TEST: PROOF LOG", "=" * 70,
         f"timestamp: {ts}", f"container: {container}", f"run.sh return: {rc}", ""]
    L.append("INTERPRETATION TABLE")
    L.append("-" * 70)
    for tid, verdict, human, note in rows:
        L.append(f"{tid:8s} {verdict:10s} {human}")
        if note:
            L.append(f"         {note}")
    L.append("")
    L.append("CANDIDATE VERDICT")
    L.append("-" * 70)
    L.extend(cand_lines)
    L.append("")
    L.append("=" * 70)
    L.append("RAW run.sh OUTPUT (atomspace behavior)")
    L.append("=" * 70)
    L.append(strip_ansi(raw))
    L.append("")
    L.append("=" * 70)
    L.append("COMBINED INPUT EVALUATED")
    L.append("=" * 70)
    L.append(combined)
    subprocess.run(["docker", "exec", "-i", container, "sh", "-c", f"cat > {log_path}"],
                   input="\n".join(L) + "\n", text=True, capture_output=True)
    return log_path


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--container", default=DEFAULT_CONTAINER)
    ap.add_argument("--harness", default=DEFAULT_HARNESS)
    ap.add_argument("--keep-temp", action="store_true")
    args = ap.parse_args()

    print("=" * 70)
    print("Lock Emptiness Harness")
    print("=" * 70)
    print("\nPREFLIGHT")
    if not container_running(args.container):
        print(f"  [FAIL] container '{args.container}' not running")
        sys.exit(1)
    print(f"  [OK] container running")
    if not container_file_exists(args.container, args.harness):
        print(f"  [FAIL] harness not found at {args.harness}")
        sys.exit(1)
    print(f"  [OK] harness: {args.harness}")

    combined, err = build_combined(args.container, args.harness)
    if err:
        print(f"  [FAIL] {err}")
        sys.exit(1)

    print("\nEVALUATING (via run.sh)")
    out, ts, rc, err = evaluate(args.container, combined, args.keep_temp)
    if err:
        print(f"  [FAIL] {err}")
        sys.exit(1)
    print(f"  run.sh return: {rc}")

    results = parse_results(out)
    if not results:
        print("\n  [WARN] no RESULT- tags parsed. Raw (first 3000 chars):")
        print(strip_ansi(out)[:3000])
        log_path = write_log(args.container, ts, combined, out, rc, [], [])
        print(f"\n  log: {log_path}")
        sys.exit(3)

    rows = interpret(results)
    cand_lines = candidate_verdict(rows)
    log_path = write_log(args.container, ts, combined, out, rc, rows, cand_lines)

    print("\n" + "=" * 70)
    print("INTERPRETATION")
    print("=" * 70)
    for tid, verdict, human, note in rows:
        print(f"  {tid:8s} {verdict:10s} {human}")
        if note:
            print(f"           {note}")

    print("\n" + "=" * 70)
    print("CANDIDATE VERDICT")
    print("=" * 70)
    for ln in cand_lines:
        print(f"  {ln}")

    print(f"\n  proof log: {log_path}")
    print(f"  (host: shared_files/{log_path.split('/')[-1]})")


if __name__ == "__main__":
    main()
