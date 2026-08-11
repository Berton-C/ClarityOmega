#!/usr/bin/env python3
"""
T53 — exact recursive-tail differential harness

Purpose
-------
Test one variable only: whether the exact recursive-tail call shape used by
production advances $k from 1 -> 2 -> 3 -> 4 under the local ClarityOmega
container environment.

This harness does NOT edit src/loop.metta, invoke the live agent loop, call the
LLM, or call any corner-gate/v3 recorder function. It writes one bounded MeTTa
probe into shared_files/ (container /tmp/), invokes it through /PeTTa/run.sh,
and validates explicit self-generated witnesses.

Differential arms
-----------------
A. Arithmetic control: (+ 1 $k) with $k=1 must reduce to 2.
B. Plain bounded recursion: the recursive argument must progress 1,2,3,4.
C. Production-tail-shaped bounded recursion: same tail ordering as production:
       sleep -> cut -> gc -> recursive call with (+ 1 $k)
   It must also progress 1,2,3,4.

A PASS means arithmetic reduction and the production tail call shape work in
isolation. It does NOT prove the full production loop is correct; it cleanly
rules this exact tail shape in or out before investigating AtomSpace branching
inside the full loop body.

Run from the ClarityOmega repository root:
    python3 staging/t53_exact_recursive_tail_differential.py
"""

from __future__ import annotations

import argparse
import hashlib
import re
import subprocess
import sys
from pathlib import Path

DEFAULT_CONTAINER = "clarity_omega"
DEFAULT_LOOP = Path("src/loop.metta")
DEFAULT_SHARED = Path("shared_files")
PROBE_NAME = "t53_exact_recursive_tail_differential.metta"
OUT_DIR = Path("/tmp/cg-v3-investigation/second-failure/t53")
TIMEOUT = 120

ANSI_RE = re.compile(r"\x1b\[[0-9;]*m")

EXPECTED_TAIL = "(omegaclaw (+ 1 $k))"
EXPECTED_ORDER = [
    "(sleep (sleepInterval))",
    "(cut)",
    "(gc)",
    EXPECTED_TAIL,
]

PROBE = r'''!(import! &self (library lib_import))

;; T53 is deliberately self-contained. It tests the exact recursive-tail
;; expression and operator ordering without entering the unbounded agent loop.

(= (t53-arithmetic-control $k)
   (+ 1 $k))

;; Arm B: simple bounded recursion, no cut/gc.
(= (t53-plain-tail $k $remaining)
   (progn
     (println! (T53-PLAIN-ENTRY $k $remaining))
     (if (== $remaining 0)
         (progn
           (println! (T53-PLAIN-DONE $k))
           $k)
         (t53-plain-tail (+ 1 $k) (- $remaining 1)))))

;; Arm C: bounded surrogate with the same tail ordering as production:
;; sleep -> cut -> gc -> recursive call with (+ 1 $k).
(= (t53-production-shaped-tail $k $remaining)
   (progn
     (println! (T53-PROD-ENTRY $k $remaining))
     (if (== $remaining 0)
         (progn
           (println! (T53-PROD-DONE $k))
           $k)
         (progn
           (sleep 0)
           (cut)
           (gc)
           (t53-production-shaped-tail (+ 1 $k) (- $remaining 1))))))

!(println! (T53-ARITHMETIC 1 (t53-arithmetic-control 1)))
!(println! (T53-PLAIN-RESULT (t53-plain-tail 1 3)))
!(println! (T53-PROD-RESULT (t53-production-shaped-tail 1 3)))
!(println! (T53-COMPLETE))
'''


def run(cmd: list[str], *, timeout: int = TIMEOUT) -> subprocess.CompletedProcess[str]:
    return subprocess.run(cmd, capture_output=True, text=True, timeout=timeout)


def clean(text: str) -> str:
    return ANSI_RE.sub("", text or "")


def exact_order_present(text: str) -> bool:
    pos = -1
    for needle in EXPECTED_ORDER:
        pos = text.find(needle, pos + 1)
        if pos < 0:
            return False
    return True


def source_audit(loop_path: Path) -> tuple[bool, str]:
    rows: list[str] = []
    if not loop_path.is_file():
        return False, f"FAIL: production loop not found: {loop_path}\n"

    text = loop_path.read_text(errors="replace")
    digest = hashlib.sha256(text.encode()).hexdigest()
    checks = [
        ("recursive head exists", "(= (omegaclaw $k)" in text),
        ("visible iteration consumes $k", "(println! (---------iteration $k))" in text),
        ("recent-action consumes $k", "(populate-recent-action $sexpr $msgnew $k)" in text),
        ("v3 recorder consumes $k", "(do-record-coupling-cycle! $metta_cmds $msgnew $k" in text),
        ("exact recursive tail exists", EXPECTED_TAIL in text),
        ("tail operator ordering exact", exact_order_present(text)),
    ]

    rows.append("=== T53 SOURCE AUDIT ===")
    rows.append(f"path:   {loop_path}")
    rows.append(f"sha256: {digest}")
    rows.append("")
    ok = True
    for label, passed in checks:
        rows.append(f"{'PASS' if passed else 'FAIL'}: {label}")
        ok = ok and passed

    rows.append("")
    rows.append("Production tail under test:")
    for item in EXPECTED_ORDER:
        rows.append(f"  {item}")
    return ok, "\n".join(rows) + "\n"


def container_running(name: str) -> bool:
    p = run(["docker", "ps", "--filter", f"name=^{name}$", "--format", "{{.Names}}"])
    return p.returncode == 0 and name in p.stdout.splitlines()


def parse_values(output: str, marker: str) -> list[int]:
    return [int(x) for x in re.findall(rf"\({re.escape(marker)}\s+([0-9]+)\s+[0-9]+\)", output)]


def parse_done(output: str, marker: str) -> list[int]:
    return [int(x) for x in re.findall(rf"\({re.escape(marker)}\s+([0-9]+)\)", output)]


def analyze(output: str) -> tuple[bool, str]:
    arithmetic = re.findall(r"\(T53-ARITHMETIC\s+1\s+([0-9]+)\)", output)
    plain_entries = parse_values(output, "T53-PLAIN-ENTRY")
    prod_entries = parse_values(output, "T53-PROD-ENTRY")
    plain_done = parse_done(output, "T53-PLAIN-DONE")
    prod_done = parse_done(output, "T53-PROD-DONE")
    plain_result = re.findall(r"\(T53-PLAIN-RESULT\s+([0-9]+)\)", output)
    prod_result = re.findall(r"\(T53-PROD-RESULT\s+([0-9]+)\)", output)
    complete_count = len(re.findall(r"\(T53-COMPLETE\)", output))

    expected = [1, 2, 3, 4]
    checks = [
        ("arithmetic (+ 1 1) reduced to 2", arithmetic == ["2"]),
        ("plain recursion entries are exactly 1,2,3,4", plain_entries == expected),
        ("plain recursion terminates at 4", plain_done == [4] and plain_result == ["4"]),
        ("production-shaped entries are exactly 1,2,3,4", prod_entries == expected),
        ("production-shaped recursion terminates at 4", prod_done == [4] and prod_result == ["4"]),
        ("probe completed exactly once", complete_count == 1),
    ]

    rows = ["=== T53 DECISIVE ANALYSIS ===", ""]
    rows.append(f"arithmetic witness:          {arithmetic or 'NOT OBSERVED'}")
    rows.append(f"plain recursion entries:     {plain_entries or 'NOT OBSERVED'}")
    rows.append(f"plain terminal/result:       {plain_done or 'NOT OBSERVED'} / {plain_result or 'NOT OBSERVED'}")
    rows.append(f"production-shaped entries:   {prod_entries or 'NOT OBSERVED'}")
    rows.append(f"production terminal/result:  {prod_done or 'NOT OBSERVED'} / {prod_result or 'NOT OBSERVED'}")
    rows.append(f"completion witnesses:        {complete_count}")
    rows.append("")

    passed = True
    for label, result in checks:
        rows.append(f"{'PASS' if result else 'FAIL'}: {label}")
        passed = passed and result

    rows.append("")
    if passed:
        rows.append("T53 VERDICT: PASS")
        rows.append(
            "The exact production recursive-tail arithmetic and operator ordering "
            "advance $k correctly in a bounded isolated evaluation. The frozen-$k "
            "production failure is therefore not caused by (+ 1 $k), cut, gc, or "
            "their tail ordering alone. The next localization must compare the full "
            "loop body's result multiplicity/backtracking before this proven-good tail."
        )
    else:
        rows.append("T53 VERDICT: FAIL")
        rows.append(
            "The probe did not capture every required witness. Do not infer a cause "
            "from partial output; inspect raw.log and focused-output.txt."
        )

    return passed, "\n".join(rows) + "\n"


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--container", default=DEFAULT_CONTAINER)
    ap.add_argument("--loop", type=Path, default=DEFAULT_LOOP)
    ap.add_argument("--shared", type=Path, default=DEFAULT_SHARED)
    args = ap.parse_args()

    OUT_DIR.mkdir(parents=True, exist_ok=True)
    args.shared.mkdir(parents=True, exist_ok=True)

    audit_ok, audit = source_audit(args.loop)
    (OUT_DIR / "source-audit.txt").write_text(audit)

    print("=== T53 HYPOTHESIS ===")
    print("The exact production recursive tail — sleep, cut, gc, then")
    print("recursive invocation with (+ 1 $k) — either advances 1->2->3->4")
    print("in isolation or it does not. Every value is emitted by this probe itself.")
    print()
    print(audit, end="")

    if not audit_ok:
        print("T53 ABORT: source audit failed. Nothing executed.")
        return 2

    if not container_running(args.container):
        print(f"T53 ABORT: container is not running: {args.container}")
        return 2

    probe_host = args.shared / PROBE_NAME
    probe_host.write_text(PROBE)
    probe_container = f"/tmp/{PROBE_NAME}"

    p = run([
        "docker", "exec", args.container, "sh", "-lc",
        f"cd /PeTTa && /PeTTa/run.sh {probe_container}",
    ])
    raw = clean((p.stdout or "") + (p.stderr or ""))
    (OUT_DIR / "raw.log").write_text(raw)

    focused_lines = [line for line in raw.splitlines() if "(T53-" in line]
    focused = "\n".join(focused_lines) + ("\n" if focused_lines else "")
    (OUT_DIR / "focused-output.txt").write_text(focused)

    passed, analysis = analyze(raw)
    (OUT_DIR / "analysis.txt").write_text(analysis)

    print()
    print(f"t53 rc={p.returncode}")
    print()
    print("=== T53 DECISIVE OUTPUT ===")
    print(focused if focused else "NO T53 WITNESSES CAPTURED")
    print(analysis, end="")
    print()
    print("=== T53 ARTIFACTS ===")
    print(probe_host)
    print(OUT_DIR / "source-audit.txt")
    print(OUT_DIR / "raw.log")
    print(OUT_DIR / "focused-output.txt")
    print(OUT_DIR / "analysis.txt")
    print()
    print("=== T53 COMPLETE ===")

    return 0 if (p.returncode == 0 and passed) else 1


if __name__ == "__main__":
    sys.exit(main())
