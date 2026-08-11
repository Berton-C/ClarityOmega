#!/usr/bin/env python3
"""
T59 — Writer evaluation-contract differential

Grounded by:
  * T58: recent-action pruning returns one result per snapshot member.
  * Atom Operations Map:
      - match returns one result per matching atom;
      - add-atom is non-idempotent;
      - remove-atom removes all matching atoms;
      - write return values are not trustworthy;
      - post-state must be verified separately;
      - collapse materializes nondeterministic streams.

Question
--------
What exact evaluation-shape difference makes recent-action behave as a generator
while the state-delta and coupling-status clearers behave as side-effect procedures?

T59 compares four shapes, each in fresh MeTTa processes:

  RA-CURRENT
      Exact current recent-action snapshot + uncollapsed superpose/remove traversal.

  RA-DRAIN-ONLY
      Same recent-action sentinel snapshot, but the drain is collapse-wrapped and
      explicitly returns one () — matching the proven writer clearer idiom.

  SD-CLEARER
      Exact structural shape of do-clear-state-delta!.

  CP-CLEARER
      Exact structural shape of do-clear-coupling-status!.

For each shape, T59 measures:
  1. function return cardinality;
  2. continuation-marker cardinality when bound in an enclosing let*;
  3. post-write AtomSpace state via a separate match read;
  4. behavior at ZERO / ONE / MANY cardinality.

No production file is edited.

Run from repo root:
    python3 staging/t59_writer_evaluation_contract_differential.py
"""

from __future__ import annotations

import argparse
import hashlib
import re
import subprocess
import sys
from pathlib import Path

CONTAINER = "clarity_omega"
ROOT = Path.cwd()
SHARED = ROOT / "shared_files"
OUT = Path("/tmp/cg-v3-investigation/second-failure/t59")
TIMEOUT = 180

SHARED.mkdir(parents=True, exist_ok=True)
OUT.mkdir(parents=True, exist_ok=True)

SOURCES = {
    "recent_action": ROOT / "soul/recent_action_populator.metta",
    "state_delta": ROOT / "soul/state_delta_writer_writers.metta",
    "coupling": ROOT / "soul/coupling_integrity_detector_writers.metta",
}

CASES = {
    "ZERO": [],
    "ONE": [1],
    "MANY": [1, 2, 3],
}

SHAPES = ("RA-CURRENT", "RA-DRAIN-ONLY", "SD-CLEARER", "CP-CLEARER")

ANSI_RE = re.compile(r"\x1b\[[0-9;]*m")


def run(cmd: list[str]) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        cmd, capture_output=True, text=True, timeout=TIMEOUT
    )


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def source_audit() -> tuple[bool, list[str]]:
    rows = ["=== T59 SOURCE AUDIT ==="]
    ok = True

    for label, path in SOURCES.items():
        exists = path.is_file()
        rows.append(f"{'PASS' if exists else 'FAIL'} {label}: {path}")
        if exists:
            rows.append(f"      sha256: {sha256(path)}")
        ok &= exists

    if SOURCES["recent_action"].is_file():
        text = SOURCES["recent_action"].read_text(errors="replace")
        checks = {
            "RA collapsed snapshot": "$to-remove    (collapse (match &self" in text,
            "RA intentional () sentinel": "(if (< $old-id $prune-before)" in text,
            "RA uncollapsed drain": "$_prune       (let $old (superpose $to-remove)" in text,
        }
        for label, passed in checks.items():
            rows.append(f"{'PASS' if passed else 'FAIL'} {label}")
            ok &= passed

    if SOURCES["state_delta"].is_file():
        text = SOURCES["state_delta"].read_text(errors="replace")
        checks = {
            "SD guards empty list before superpose": "(if (== $existing ())" in text,
            "SD collapse-wraps drain": "(collapse (let $old (superpose $existing)" in text,
            "SD forces singleton return": "             ()))))" in text,
        }
        for label, passed in checks.items():
            rows.append(f"{'PASS' if passed else 'FAIL'} {label}")
            ok &= passed

    if SOURCES["coupling"].is_file():
        text = SOURCES["coupling"].read_text(errors="replace")
        checks = {
            "CP guards empty list before superpose": "(if (== $existing ())" in text,
            "CP collapse-wraps drain": "(collapse (let $old (superpose $existing)" in text,
            "CP source explicitly documents N-result multiplication":
                "multiply the add that follows" in text,
        }
        for label, passed in checks.items():
            rows.append(f"{'PASS' if passed else 'FAIL'} {label}")
            ok &= passed

    return ok, rows


def atoms_for(shape: str, ids: list[int]) -> list[str]:
    if shape.startswith("RA-"):
        # All IDs are retained relative to prune-before 0, intentionally producing ()
        return [
            f"(t59-ra {100+i} kind desc-{i})"
            for i in ids
        ]
    if shape == "SD-CLEARER":
        return [f"(t59-sd {i} verdict-{i})" for i in ids]
    return [f"(t59-cp {i} verdict-{i})" for i in ids]


def function_definition(shape: str) -> list[str]:
    if shape == "RA-CURRENT":
        return [
            "(= (t59-fn)",
            "   (let $to-remove",
            "        (collapse",
            "          (match &self",
            "            (t59-ra $old-id $t $d)",
            "            (if (< $old-id 0)",
            "                (t59-ra $old-id $t $d)",
            "                ())))",
            "     (let $old (superpose $to-remove)",
            "       (if (== $old ())",
            "           ()",
            "           (remove-atom &self $old)))))",
        ]

    if shape == "RA-DRAIN-ONLY":
        return [
            "(= (t59-fn)",
            "   (let $to-remove",
            "        (collapse",
            "          (match &self",
            "            (t59-ra $old-id $t $d)",
            "            (if (< $old-id 0)",
            "                (t59-ra $old-id $t $d)",
            "                ())))",
            "     (if (== $to-remove ())",
            "         ()",
            "         (let $_drained",
            "              (collapse",
            "                (let $old (superpose $to-remove)",
            "                  (if (== $old ())",
            "                      ()",
            "                      (remove-atom &self $old))))",
            "           ()))))",
        ]

    if shape == "SD-CLEARER":
        return [
            "(= (t59-fn)",
            "   (let $existing",
            "        (collapse",
            "          (match &self",
            "            (t59-sd $c $v)",
            "            (t59-sd $c $v)))",
            "     (if (== $existing ())",
            "         ()",
            "         (let $_drained",
            "              (collapse",
            "                (let $old (superpose $existing)",
            "                  (remove-atom &self $old)))",
            "           ()))))",
        ]

    return [
        "(= (t59-fn)",
        "   (let $existing",
        "        (collapse",
        "          (match &self",
        "            (t59-cp $c $v)",
        "            (t59-cp $c $v)))",
        "     (if (== $existing ())",
        "         ()",
        "         (let $_drained",
        "              (collapse",
        "                (let $old (superpose $existing)",
        "                  (remove-atom &self $old)))",
        "           ()))))",
    ]


def read_pattern(shape: str) -> tuple[str, str]:
    if shape.startswith("RA-"):
        return "(t59-ra $id $t $d)", "$id"
    if shape == "SD-CLEARER":
        return "(t59-sd $id $v)", "$id"
    return "(t59-cp $id $v)", "$id"


def probe_text(shape: str, case: str, ids: list[int]) -> str:
    atoms = atoms_for(shape, ids)
    pattern, scalar = read_pattern(shape)

    lines = [
        "!(import! &self (library lib_import))",
        "!(import! &self /PeTTa/repos/omegaclaw/lib_omegaclaw.metta)",
        "",
        f"!(println! (T59-BEGIN {shape} {case}))",
    ]
    lines.extend(f"!(add-atom &self {atom})" for atom in atoms)
    lines.append("")
    lines.extend(function_definition(shape))
    lines.extend([
        "",
        "!(let $returns (collapse (t59-fn))",
        f"   (println! (T59-RETURN {shape} {case}",
        "                           count (size-atom $returns)",
        "                           values $returns)))",
        "",
        # Fresh state is needed for continuation measurement because first call may remove.
        # Re-seed only SD/CP; RA retained atoms are not removed by the current or drain-only shapes.
    ])

    if shape in ("SD-CLEARER", "CP-CLEARER"):
        lines.extend(f"!(add-atom &self {atom})" for atom in atoms)

    lines.extend([
        "",
        "!(let* (($_call (t59-fn))",
        f"         ($_after (println! (T59-CONTINUATION {shape} {case}))))",
        "   ())",
        "",
        f"!(let $remaining (collapse (match &self {pattern} {scalar}))",
        f"   (println! (T59-POSTSTATE {shape} {case}",
        "                              count (size-atom $remaining)",
        "                              values $remaining)))",
        "",
        f"!(println! (T59-END {shape} {case}))",
        "",
    ])
    return "\n".join(lines)


def parse_count(witnesses: list[str], marker: str, shape: str, case: str):
    pattern = re.compile(
        rf"^\(T59-{marker}\s+{re.escape(shape)}\s+{re.escape(case)}"
        rf"\s+count\s+(\d+)\b"
    )
    for line in witnesses:
        match = pattern.search(line)
        if match:
            return int(match.group(1))
    return None


def execute(shape: str, case: str, ids: list[int], container: str) -> dict:
    stem = f"t59_{shape.lower().replace('-', '_')}_{case.lower()}"
    probe = SHARED / f"{stem}.metta"
    probe.write_text(probe_text(shape, case, ids))

    process = run([
        "docker", "exec", container, "sh", "-lc",
        f"cd /PeTTa && /PeTTa/run.sh /tmp/{probe.name}",
    ])

    raw = ANSI_RE.sub("", (process.stdout or "") + (process.stderr or ""))
    raw_path = OUT / f"{stem}.raw.log"
    raw_path.write_text(raw)

    witnesses = [
        line.strip()
        for line in raw.splitlines()
        if line.strip().startswith("(T59-")
    ]

    return_count = parse_count(witnesses, "RETURN", shape, case)
    post_count = parse_count(witnesses, "POSTSTATE", shape, case)
    continuation_count = sum(
        1 for line in witnesses
        if line.startswith(f"(T59-CONTINUATION {shape} {case})")
    )

    required = [
        f"(T59-BEGIN {shape} {case}",
        f"(T59-RETURN {shape} {case}",
        f"(T59-POSTSTATE {shape} {case}",
        f"(T59-END {shape} {case}",
    ]
    missing = [
        marker for marker in required
        if not any(line.startswith(marker) for line in witnesses)
    ]

    valid = (
        process.returncode == 0
        and not missing
        and return_count is not None
        and post_count is not None
    )

    return {
        "shape": shape,
        "case": case,
        "rc": process.returncode,
        "returns": return_count,
        "continuations": continuation_count,
        "post": post_count,
        "valid": valid,
        "missing": missing,
        "witnesses": witnesses,
        "raw": raw_path,
        "raw_tail": "\n".join(raw.splitlines()[-100:]) if not valid else "",
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--container", default=CONTAINER)
    args = parser.parse_args()
    container = args.container

    audit_ok, audit_rows = source_audit()
    log_path = OUT / "t59-evidence.log"

    header = [
        "=== T59 HYPOTHESIS ===",
        "The recent-action multiplier is caused by an evaluation-contract mismatch:",
        "its snapshot produces one member per matched atom (including () sentinels),",
        "and its uncollapsed drain returns that cardinality into loop.metta.",
        "The corrected writer idiom collapse-wraps the drain and forces one return.",
        "",
        "Atom Operations Map constraints:",
        "  - match cardinality is real and must be counted;",
        "  - write returns are not trusted;",
        "  - post-state is match-verified separately;",
        "  - remove-atom behavior is assessed by stored state, not return token.",
        "",
    ] + audit_rows + [""]

    if not audit_ok:
        text = "\n".join(header + ["T59 ABORT: source audit failed."])
        log_path.write_text(text + "\n")
        print(text)
        return 2

    ps = run([
        "docker", "ps",
        "--filter", f"name=^{container}$",
        "--format", "{{.Names}}",
    ])
    if container not in ps.stdout.splitlines():
        text = "\n".join(header + [f"T59 ABORT: container not running: {container}"])
        log_path.write_text(text + "\n")
        print(text)
        return 2

    results = []
    for shape in SHAPES:
        for case, ids in CASES.items():
            print(f"T59 running {shape}/{case}")
            results.append(execute(shape, case, ids, container))

    report = header + [
        "=== T59 CONTRACT TABLE ===",
        "",
        f"{'SHAPE':14} {'CASE':6} {'RC':>3} {'RETURNS':>7} "
        f"{'CONT':>5} {'POST':>5} {'VALID':>6}",
        "-" * 59,
    ]

    for result in results:
        report.append(
            f"{result['shape']:14} {result['case']:6} {result['rc']:>3} "
            f"{str(result['returns']):>7} "
            f"{result['continuations']:>5} "
            f"{str(result['post']):>5} "
            f"{('YES' if result['valid'] else 'NO'):>6}"
        )

    report += ["", "=== DECISIVE WITNESSES ==="]
    for result in results:
        report.append(f"\n--- {result['shape']} / {result['case']} ---")
        report.extend(result["witnesses"] or ["NO T59 WITNESSES"])
        if not result["valid"]:
            report.append(f"MISSING: {result['missing']}")
            report.append(f"RAW LOG: {result['raw']}")
            report.append("RAW TAIL:")
            report.append(result["raw_tail"] or "<empty>")

    report += ["", "=== T59 VERDICT ==="]

    invalid = [r for r in results if not r["valid"]]
    if invalid:
        report += [
            "INVALID — at least one comparison surface lacked mandatory witnesses.",
            "No production change is authorized.",
        ]
        exit_code = 1
    else:
        by_key = {(r["shape"], r["case"]): r for r in results}

        ra_current_many = by_key[("RA-CURRENT", "MANY")]
        ra_drain_many = by_key[("RA-DRAIN-ONLY", "MANY")]
        sd_many = by_key[("SD-CLEARER", "MANY")]
        cp_many = by_key[("CP-CLEARER", "MANY")]

        generator_confirmed = (
            ra_current_many["returns"] == 3
            and ra_current_many["continuations"] == 3
            and ra_current_many["post"] == 3
        )
        reconverged = (
            ra_drain_many["returns"] == 1
            and ra_drain_many["continuations"] == 1
            and ra_drain_many["post"] == 3
        )
        peers_single = (
            sd_many["returns"] == 1
            and sd_many["continuations"] == 1
            and sd_many["post"] == 0
            and cp_many["returns"] == 1
            and cp_many["continuations"] == 1
            and cp_many["post"] == 0
        )

        if generator_confirmed and reconverged and peers_single:
            report += [
                "SUPPORTED.",
                "",
                "The exact contract difference is now grounded:",
                "  1. RA-CURRENT exposes one return and one enclosing continuation",
                "     per snapshot member.",
                "  2. RA-DRAIN-ONLY preserves the intentional sentinel snapshot and",
                "     stored-state behavior, but collapse-wraps the drain and returns",
                "     exactly one continuation.",
                "  3. Both established peer clearers use that same singleton contract.",
                "",
                "This authorizes a minimal production repair limited to the",
                "recent-action pruning drain/reconvergence boundary.",
                "It does not authorize changing the intentional () filter branch.",
            ]
        else:
            report += [
                "NOT FULLY SUPPORTED.",
                "",
                "At least one expected contract relation did not hold.",
                "Inspect the table and witnesses before designing a fix.",
            ]
        exit_code = 0

    report += [
        "",
        "=== DEFERRED ISSUE REGISTER ===",
        "RA-SECONDARY-01 remains open:",
        "duplicate recent-action atoms sharing one cycle ID may make",
        "recent_action_retriever select arbitrarily through car-atom.",
        "Address only after the primary multiplier repair is live-confirmed.",
        "",
        f"Primary evidence log: {log_path}",
        "=== T59 COMPLETE ===",
    ]

    text = "\n".join(report) + "\n"
    log_path.write_text(text)
    print("\n" + text, end="")
    return exit_code


if __name__ == "__main__":
    raise SystemExit(main())
