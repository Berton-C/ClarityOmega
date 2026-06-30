#!/usr/bin/env python3
"""
detection_surface_harness.py

Interrogates the soul-mutation DETECTION surface and dumps a structured report.
NOT a one-shot check -- a reusable instrument. Run before the fix to map gaps,
run after the fix to PROVE gaps closed, run whenever the kernel evolves.

WHAT IT ANSWERS (each = a report section):
  A. Membership seed inventory   -- every (soul-ns-member HEAD) tag; bare vs soul-prefixed
  B. Constitutional head verify  -- Clarity's 8 heads: exist? where? how many atoms each?
  C. Coverage matrix             -- constitutional x tagged: COVERED / GAP / over-tag
  D. Writer survey               -- does normal operation write these heads to &self?
  E. Live-predicate note         -- what needs the running container (NOT this harness)

HONEST LIMITS (stated in the report too):
  Sections A-D are FILE-BASED static analysis -- reliable in this harness.
  Section E (soul-head-is-member? actual True/False at runtime, live atomspace tag
  counts) needs the running container with the skill chain loaded. This harness
  does NOT claim those; it flags them as container-only.

USAGE:
  python3 detection_surface_harness.py [REPO_ROOT]
  (REPO_ROOT defaults to "."; run from repo root or pass the path.)
  Writes report to <REPO_ROOT>/shared_files/detection_surface_report_<ts>.log
  and also prints to stdout.
"""

import sys
import os
import re
import datetime
from pathlib import Path

# Clarity's enumeration (2026-06-13 MM handoff) -- the 8 bare-headed constitutional
# heads, with her cited line ranges. The harness VERIFIES these against the live file.
CLARITY_HEADS = [
    ("priority", "~22-26", "alignment anchor ordering"),
    ("irreversible-skill", "~280-283", "declares which skills are irreversible (gate territory)"),
    ("tension-vector", "~287-291", "5 declared threat vectors"),
    ("threatens", "~294-300", "7 tension-pattern affinities"),
    ("person-state-type", "~325-329", "5 person-classification types"),
    ("irreversible-weight", "~335-341", "7 weights, checkpoint threshold math"),
    ("task-context-field", "~345-352", "8 agentic-mode structural fields"),
    ("operation-risk", "~370-384", "15 atoms, labeled constitutional, never runtime-edited"),
]

SEED_FILE = "soul/soul_namespace_membership_seed.metta"
KERNEL_FILE = "soul/soul_kernel.metta"
# Writer-survey scan set: runtime files that could write heads to &self each cycle.
WRITER_SCAN = ["src/loop.metta", "src/helper.py"]
WRITER_SCAN_GLOBS = ["soul/*.metta", "soul/*.py"]

WRITE_OPS = ["add-atom", "set-atom!", "change-state!"]


def read(path: Path) -> str:
    try:
        return path.read_text()
    except Exception as e:
        return f"<<UNREADABLE: {e}>>"


def section(title):
    return f"\n{'=' * 76}\n{title}\n{'=' * 76}"


def main():
    root = Path(sys.argv[1]) if len(sys.argv) > 1 else Path(".")
    ts = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    lines = []

    def out(s=""):
        print(s)
        lines.append(s)

    out("#" * 76)
    out("# DETECTION-SURFACE HARNESS REPORT")
    out(f"# Generated: {datetime.datetime.now().isoformat()}")
    out(f"# Repo root: {root.resolve()}")
    out("# Reusable instrument: re-run after the fix to prove gaps closed.")
    out("#" * 76)

    # ---------- SECTION A: membership seed inventory ----------
    out(section("A. MEMBERSHIP SEED INVENTORY (file-based, reliable)"))
    seed_path = root / SEED_FILE
    seed_text = read(seed_path)
    out(f"  Source: {SEED_FILE}")
    if seed_text.startswith("<<UNREADABLE"):
        out(f"  {seed_text}")
        tagged_heads = set()
    else:
        # Match (soul-ns-member HEAD) capturing HEAD, but LINE-BY-LINE so we can
        # skip comment lines, and reject placeholder tokens that appear in docs
        # (e.g. the literal 'HEAD' used in a comment like ';; (soul-ns-member HEAD)').
        tag_re = re.compile(r"\(soul-ns-member\s+([^\s)]+)\s*\)")
        # A MeTTa line comment starts with ';'. Strip an inline comment, and skip
        # any line whose code portion is empty (pure comment).
        PLACEHOLDER_TOKENS = {"HEAD", "head", "<HEAD>", "..."}
        tags = []
        for raw in seed_text.splitlines():
            code = raw.split(";", 1)[0]  # drop inline/line comments
            if not code.strip():
                continue
            for m in tag_re.findall(code):
                if m in PLACEHOLDER_TOKENS:
                    continue  # documentation placeholder, not a real tag
                tags.append(m)
        tagged_heads = set(tags)
        bare = sorted(h for h in tagged_heads if not h.startswith("soul-"))
        prefixed = sorted(h for h in tagged_heads if h.startswith("soul-"))
        out(f"  Total (soul-ns-member ...) tags found: {len(tags)} ({len(tagged_heads)} unique heads)")
        out(f"  soul-prefixed tagged heads: {len(prefixed)}")
        out(f"  BARE (non-soul-prefixed) tagged heads: {len(bare)}")
        if bare:
            out(f"    bare tagged: {bare}")
        else:
            out("    bare tagged: NONE  <- this is the gap's root: only soul-prefixed heads tagged")

    # ---------- SECTION B: constitutional head verification ----------
    out(section("B. CONSTITUTIONAL HEAD VERIFICATION (Clarity's 8 vs live kernel)"))
    kernel_path = root / KERNEL_FILE
    kernel_text = read(kernel_path)
    out(f"  Source: {KERNEL_FILE}")
    kernel_lines = kernel_text.splitlines() if not kernel_text.startswith("<<UNREADABLE") else []
    verified = {}
    if not kernel_lines:
        out(f"  {kernel_text}")
    else:
        out(f"  Kernel line count: {len(kernel_lines)}")
        out("")
        for head, cited, desc in CLARITY_HEADS:
            # find lines that look like an atom definition with this exact head:
            # ( HEAD ... )  -- head as first token after an open paren
            pat = re.compile(r"\(" + re.escape(head) + r"[\s)]")
            hits = [i + 1 for i, ln in enumerate(kernel_lines) if pat.search(ln)]
            exists = len(hits) > 0
            verified[head] = {"exists": exists, "lines": hits, "count": len(hits)}
            status = "FOUND" if exists else "NOT FOUND (spelling/location mismatch?)"
            line_span = f"lines {hits[0]}-{hits[-1]}" if hits else "no match"
            out(f"  [{ 'OK ' if exists else 'XX ' }] {head:24s} cited {cited:10s} -> {status}")
            out(f"        live: {len(hits)} atom-line(s), {line_span}")
            if exists:
                # show the first matching line trimmed, as evidence
                first = kernel_lines[hits[0] - 1].strip()
                out(f"        e.g. L{hits[0]}: {first[:90]}")
            out(f"        role: {desc}")

    # ---------- SECTION C: coverage matrix ----------
    out(section("C. COVERAGE MATRIX (constitutional x tagged)"))
    out("  head                      constitutional   tagged   verdict")
    out("  " + "-" * 66)
    gaps = []
    for head, _, _ in CLARITY_HEADS:
        is_const = verified.get(head, {}).get("exists", False)
        is_tagged = head in tagged_heads
        if is_const and not is_tagged:
            verdict = "GAP -> needs tag"
            gaps.append(head)
        elif is_const and is_tagged:
            verdict = "COVERED"
        elif not is_const and is_tagged:
            verdict = "tagged but not found in kernel (recheck)"
        else:
            verdict = "not found + not tagged"
        out(f"  {head:24s}  {str(is_const):14s}  {str(is_tagged):7s}  {verdict}")
    out("")
    out(f"  GAPS (constitutional, untagged): {len(gaps)}")
    if gaps:
        out(f"    -> tag these: {gaps}")

    # ---------- SECTION D: writer survey ----------
    out(section("D. WRITER SURVEY (does normal operation write these heads to &self?)"))
    out("  Per Discipline 6: if a head is written to &self during normal cycles, tagging it")
    out("  would push routine work into PENDING (false-positive / over-gate risk).")
    out("")
    scan_files = []
    for rel in WRITER_SCAN:
        p = root / rel
        if p.exists():
            scan_files.append(p)
    for glob in WRITER_SCAN_GLOBS:
        scan_files.extend(sorted((root).glob(glob)))
    scan_files = [p for p in scan_files if p.is_file()]
    out(f"  Scanned {len(scan_files)} runtime/substrate files for write-ops on the 8 heads.")
    out("")
    for head, _, _ in CLARITY_HEADS:
        writer_hits = []
        for p in scan_files:
            txt = read(p)
            if txt.startswith("<<UNREADABLE"):
                continue
            rel = str(p.relative_to(root)) if str(p).startswith(str(root)) else str(p)
            for i, ln in enumerate(txt.splitlines(), 1):
                code = ln.split(";", 1)[0]  # drop MeTTa/py line comments
                if not code.strip():
                    continue
                # a write-op line that mentions this head (in code, not comment)
                if any(op in code for op in WRITE_OPS) and re.search(r"\(" + re.escape(head) + r"[\s)]", code):
                    # classify: boot-construction (kernel) vs runtime (loop/helper/other)
                    kind = "BOOT-CONSTRUCTION" if rel.endswith("soul_kernel.metta") else "RUNTIME"
                    writer_hits.append((rel, i, code.strip()[:100], kind))
        runtime_hits = [h for h in writer_hits if h[3] == "RUNTIME"]
        boot_hits = [h for h in writer_hits if h[3] == "BOOT-CONSTRUCTION"]
        if runtime_hits:
            out(f"  [OVER-GATE RISK] {head}: {len(runtime_hits)} RUNTIME writer(s) -- tagging would gate normal work")
            for rel, i, snippet, _ in runtime_hits[:6]:
                out(f"        RUNTIME {rel}:{i}  {snippet}")
            if boot_hits:
                out(f"        (+ {len(boot_hits)} boot-construction writer(s) in kernel -- expected)")
        elif boot_hits:
            out(f"  [boot only]    {head}: {len(boot_hits)} writer(s), ALL boot-construction in kernel -- no runtime over-gate")
            for rel, i, snippet, _ in boot_hits[:2]:
                out(f"        BOOT {rel}:{i}  {snippet}")
            if len(boot_hits) > 2:
                out(f"        ... and {len(boot_hits) - 2} more boot-construction lines")
        else:
            out(f"  [no writers]   {head}: no write-ops found -> tagging safe")
    out("")
    out("  INTERPRETATION: 'boot only' heads are written solely during kernel construction")
    out("  (initSoulSeeds boot), not per-cycle. Tagging them does NOT over-gate runtime work.")
    out("  BUT confirm separately that the gate is NOT in-path during boot kernel construction,")
    out("  or tagging would gate the constitution's own building. (See Section E / boot-path read.)")

    # ---------- SECTION E: live-predicate note ----------
    out(section("E. LIVE-PREDICATE BEHAVIOR (container-only; NOT claimed by this harness)"))
    out("  The following require the running container with the skill chain loaded and are")
    out("  NOT answered here (stating honestly rather than fake-claiming):")
    out("    - soul-head-is-member? actual True/False per head at runtime")
    out("    - live atomspace count of (soul-ns-member ...) after boot seeding")
    out("    - whether derive-gate-state routes a real (HEAD ...) mutation to PENDING")
    out("  To answer E: emit a test mutation in the live loop (caught, safe) OR a")
    out("  skill-chain-loaded probe, and read the gate flag. Do that AFTER the fix as the")
    out("  end-to-end PENDING-path validation that has never yet fired.")

    # ---------- SUMMARY ----------
    out(section("SUMMARY"))
    found = sum(1 for h, _, _ in CLARITY_HEADS if verified.get(h, {}).get("exists"))
    out(f"  Constitutional heads claimed: {len(CLARITY_HEADS)}")
    out(f"  Verified present in live kernel: {found}/{len(CLARITY_HEADS)}")
    out(f"  Coverage gaps (constitutional, untagged): {len(gaps)}")
    over_gate = "see Section D for any head with writers"
    out(f"  Over-gate risk: {over_gate}")
    out(f"  Fix-1 readiness: tag the {len(gaps)} gap head(s) IF Section D shows no normal-op writers.")
    out(f"  Fix-2 (general fallback): deferred per Clarity (needs careful &self-scope, separate iter).")

    # write log
    try:
        sf = root / "shared_files"
        sf.mkdir(exist_ok=True)
        logp = sf / f"detection_surface_report_{ts}.log"
        logp.write_text("\n".join(lines) + "\n")
        print(f"\nREPORT WRITTEN: {logp}")
    except Exception as e:
        print(f"\n(log write skipped: {e})")


if __name__ == "__main__":
    main()
