#!/usr/bin/env python3
"""
Namespace collision census (Repair 1 root-cause frame, 2026-06-10).
For every function name the mutation gate, verdict module, and wiring
glue DEFINE or CALL, find every definition site across the load-chain
surface. Duplicates are the root-cause class (proven: soul_utils:139
legacy stub (soul-is-metta-cmd? -> False) colliding with the gate).

Run from repo root:  python3 staging/namespace_census.py
Read-only. Output: collision table + clean table.
"""
import re
from pathlib import Path

# The load-chain surface (approximates what boot actually loads;
# excludes archives, OLD, shared_files, volumes, memory).
SCAN_DIRS = ["soul", "src", "lib_clarity_reasoning", "skills"]
SCAN_ROOT_GLOBS = ["*.metta"]
EXCLUDE_SUBSTR = [".bak", "staging/OLD", "shared_files", "volumes/",
                  "omega_archive", "omegaclaw_src_may", "memory/",
                  "hyperon-experimental"]

# Every name the governance stack defines or stands on.
NAMES = [
    # committed gate
    "soul-is-metta-cmd?", "soul-any-metta?", "soul-extract-metta-arg",
    "soul-target-head", "soul-ns-construct", "soul-head-is-member?",
    "soul-metta-targets-soul-namespace?", "soul-mutation-pending?",
    # verdict module section 1
    "path-scope-score", "output-cmd-head", "output-cmd-path",
    "output-cmd-is-write", "output-cmd-is-append", "output-cmd-skill",
    "output-cmd-operation", "output-cmd-scope", "output-cmd-target-class",
    "output-cmd-grounding", "rank-from-dims", "output-cmd-rank",
    "batch-rank", "compute-output-verdict",
    # wiring glue
    "metta-arg-mutates?", "batch-targets-soul?", "derive-gate-state",
    "output-decision",
    # kernel governance seeds
    "resolve-operation-risk", "soul-cmd-skill", "soul-file-class-of",
    "soul-use-llm-eval?", "filter-empty-entries",
    # loop-block consumers and neighbors
    "soul-proceed?", "soul-pause?", "soul-note-record", "apply-corner-gate",
    # primitives worth a paranoia check
    "any", "collapse", "car-atom", "cdr-atom", "quote",
]


def files():
    out = []
    for d in SCAN_DIRS:
        p = Path(d)
        if p.is_dir():
            out += sorted(p.rglob("*.metta"))
    for g in SCAN_ROOT_GLOBS:
        out += sorted(Path(".").glob(g))
    seen, final = set(), []
    for f in out:
        s = str(f)
        if any(x in s for x in EXCLUDE_SUBSTR) or s in seen:
            continue
        seen.add(s)
        final.append(f)
    return final


def main():
    sites = {n: [] for n in NAMES}
    flist = files()
    print(f"Scanning {len(flist)} load-chain files...")
    for f in flist:
        try:
            text = f.read_text(errors="replace")
        except Exception:
            continue
        for i, line in enumerate(text.splitlines(), 1):
            stripped = line.strip()
            if stripped.startswith(";"):
                continue
            for n in NAMES:
                # definition site: (= (NAME ...   (escape ? and special chars)
                pat = r"\(=\s*\(" + re.escape(n) + r"[\s)]"
                if re.search(pat, line):
                    sites[n].append(f"{f}:{i}: {stripped[:100]}")
    collisions = {n: s for n, s in sites.items() if len(s) > 1}
    singles = {n: s for n, s in sites.items() if len(s) == 1}
    missing = [n for n, s in sites.items() if len(s) == 0]

    print("\n========== COLLISIONS (multiple definition sites) ==========")
    if not collisions:
        print("  none")
    for n, s in sorted(collisions.items()):
        print(f"\n  {n}  ({len(s)} sites):")
        for line in s:
            print(f"    {line}")

    print("\n========== SINGLE-SITE (clean) ==========")
    for n, s in sorted(singles.items()):
        print(f"  {n}: {s[0].split(':')[0]}:{s[0].split(':')[1]}")

    print("\n========== NOT DEFINED IN SCAN SURFACE ==========")
    print("  (builtins or container-side libs; expected for primitives)")
    for n in sorted(missing):
        print(f"  {n}")

    print("\nNOTE: multi-clause pattern dispatch within ONE file "
          "(e.g. soul-cmd-skill's 12 kernel clauses) appears as a "
          "collision with all sites in the same file; that is by design "
          "and fine. CROSS-FILE collisions are the bug class.")


if __name__ == "__main__":
    main()
