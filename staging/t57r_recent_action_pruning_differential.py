#!/usr/bin/env python3
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path.cwd()
SHARED = ROOT / "shared_files"
OUT = Path("/tmp/cg-v3-investigation/second-failure/t57r")
CONTAINER = "clarity_omega"
SHARED.mkdir(parents=True, exist_ok=True)
OUT.mkdir(parents=True, exist_ok=True)

CASES = {
    "ZERO": [],
    "RETAINED": [
        "(t57-action 100 responsive-send keep-a)",
        "(t57-action 101 exploration-query keep-b)",
        "(t57-action 102 pin-only keep-c)",
    ],
    "MIXED": [
        "(t57-action 88 responsive-send prune-a)",
        "(t57-action 89 exploration-query prune-b)",
        "(t57-action 100 responsive-send keep-a)",
        "(t57-action 101 exploration-query keep-b)",
        "(t57-action 102 pin-only keep-c)",
    ],
}
PRUNE_BEFORE = 92

def run(cmd):
    return subprocess.run(cmd, text=True, capture_output=True)

def build_probe(case, atoms, mode):
    adds = "\n".join(f"!(add-atom &self {a})" for a in atoms)
    original = "(let $old (superpose $to-remove) (if (== $old ()) () (remove-atom &self $old)))"
    tested = original if mode == "ORIGINAL" else f"(collapse {original})"
    return "\n".join([
        f"!(println! (T57R-BEGIN {case} {mode}))",
        adds,
        "(= (t57r-snapshot)",
        "   (collapse",
        "     (match &self",
        "       (t57-action $old-id $old-type $old-desc)",
        f"       (if (< $old-id {PRUNE_BEFORE})",
        "           (t57-action $old-id $old-type $old-desc)",
        "           ()))))",
        "(= (t57r-traversal)",
        "   (let $to-remove (t57r-snapshot)",
        f"     {tested}))",
        f"!(let $snapshot (t57r-snapshot) (println! (T57R-SNAPSHOT {case} {mode} count (size-atom $snapshot) values $snapshot)))",
        f"!(let $outputs (collapse (t57r-traversal)) (println! (T57R-TRAVERSAL {case} {mode} count (size-atom $outputs) values $outputs)))",
        f"!(let $remaining (collapse (match &self (t57-action $id $type $desc) (t57-action $id $type $desc))) (println! (T57R-REMAINING {case} {mode} count (size-atom $remaining) values $remaining)))",
        f"!(println! (T57R-END {case} {mode}))",
        "",
    ])

ps = run(["docker","ps","--filter",f"name=^{CONTAINER}$","--format","{{.Names}}"])
if CONTAINER not in ps.stdout.splitlines():
    print(f"T57-R ABORT: container not running: {CONTAINER}")
    sys.exit(2)

results = []
witnesses = []
failures = []

for case, atoms in CASES.items():
    for mode in ("ORIGINAL", "COLLAPSED"):
        name = f"t57r_{case.lower()}_{mode.lower()}.metta"
        probe = SHARED / name
        probe.write_text(build_probe(case, atoms, mode))
        p = run(["docker","exec",CONTAINER,"sh","-lc",f"cd /PeTTa && /PeTTa/run.sh /tmp/{name}"])
        raw = (p.stdout or "") + (p.stderr or "")
        raw_path = OUT / f"{name}.raw.log"
        raw_path.write_text(raw)
        ws = [ln.strip() for ln in raw.splitlines() if ln.strip().startswith("(T57R-")]
        witnesses.append(f"--- {case}/{mode} ---")
        witnesses.extend(ws or ["NO T57R RUNTIME MARKERS"])

        def count(tag):
            pat = re.compile(rf"^\(T57R-{tag}\s+{case}\s+{mode}\s+count\s+(\d+)\b")
            for ln in ws:
                m = pat.search(ln)
                if m:
                    return int(m.group(1))
            return None

        snap = count("SNAPSHOT")
        trav = count("TRAVERSAL")
        remain = count("REMAINING")
        required = [f"(T57R-{m} {case} {mode}" for m in ("BEGIN","SNAPSHOT","TRAVERSAL","REMAINING","END")]
        missing = [m for m in required if not any(ln.startswith(m) for ln in ws)]
        valid = p.returncode == 0 and not missing and None not in (snap, trav, remain)
        if not valid:
            failures.append(
                f"{case}/{mode}: rc={p.returncode} missing={missing} snap={snap} trav={trav} remain={remain}\n"
                f"RAW={raw_path}\nTAIL:\n" + "\n".join(raw.splitlines()[-120:])
            )
        results.append((case, mode, p.returncode, snap, trav, remain, valid))

report = [
    "=== T57-R HYPOTHESIS ===",
    "The intentional () non-prune branch is safe only if the exact production-shaped",
    "pruning traversal returns exactly one continuation. The only differential is",
    "an outer collapse around that traversal. No production file is edited.",
    "",
    "=== CARDINALITY TABLE ===",
    f"{'CASE':10} {'MODE':10} {'RC':>3} {'SNAP':>6} {'TRAV':>6} {'REMAIN':>7} {'VALID':>6}",
    "-" * 62,
]
for r in results:
    report.append(
        f"{r[0]:10} {r[1]:10} {r[2]:>3} {str(r[3]):>6} {str(r[4]):>6} "
        f"{str(r[5]):>7} {('YES' if r[6] else 'NO'):>6}"
    )

report += ["", "=== DECISIVE RUNTIME WITNESSES ==="] + witnesses

if failures:
    report += [
        "",
        "=== VERDICT ===",
        "INVALID: mandatory runtime witnesses missing. No pruning conclusion.",
        "",
        "=== FAILURE DIAGNOSTICS ===",
    ] + failures
    rc = 1
else:
    d = {(r[0], r[1]): r for r in results}
    original_multiplies = d[("RETAINED","ORIGINAL")][4] > 1 or d[("MIXED","ORIGINAL")][4] > 1
    collapsed_single = d[("RETAINED","COLLAPSED")][4] == 1 and d[("MIXED","COLLAPSED")][4] == 1
    report += ["", "=== VERDICT ==="]
    if original_multiplies and collapsed_single:
        report += [
            "SUPPORTED: the exact traversal leaks snapshot cardinality;",
            "changing only the traversal boundary to collapse restores one continuation.",
            "The () branch may remain intentional; the defect is unreconverged superpose output.",
        ]
    elif not original_multiplies:
        report += ["NOT SUPPORTED: exact traversal stayed single-valued. Do not patch production."]
    else:
        report += ["MIXED: original multiplied, but collapse did not consistently restore one result."]
    rc = 0

report += [
    "",
    "=== DEFERRED ISSUE REGISTER ===",
    "RA-SECONDARY-01 remains open: duplicate cycle IDs may make the retriever",
    "choose arbitrarily through car-atom. Address after the primary multiplier.",
    "",
    f"Primary evidence log: {OUT / 't57r-evidence.log'}",
    "=== T57-R COMPLETE ===",
]

text = "\n".join(report) + "\n"
(OUT / "t57r-evidence.log").write_text(text)
print(text, end="")
sys.exit(rc)
