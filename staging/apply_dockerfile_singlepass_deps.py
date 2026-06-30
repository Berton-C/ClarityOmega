#!/usr/bin/env python3
"""
Dockerfile fix: collapse the two pip install passes into ONE so torch and
transformers co-resolve to a compatible set (fixes the float8/FP8 out-of-sync
break that --no-cache surfaced). Keeps CPU-only torch via --extra-index-url
(verified: resolves torch-*+cpu, no CUDA). No version pins; arm64 stays open.

Dry-run (default):  python3 staging/apply_dockerfile_singlepass_deps.py
Apply:              python3 staging/apply_dockerfile_singlepass_deps.py --apply
Reverse:            python3 staging/apply_dockerfile_singlepass_deps.py --reverse --apply
Backup: Dockerfile.bak.singlepass_deps
"""
import argparse, sys
from pathlib import Path

DOCKERFILE = Path("Dockerfile")
BAK = Path("Dockerfile.bak.singlepass_deps")

OLD = (
    "RUN python3 -m pip install --no-cache-dir --break-system-packages \\\n"
    "    --index-url https://download.pytorch.org/whl/cpu \\\n"
    "    torch \\\n"
    " && python3 -m pip install --no-cache-dir --break-system-packages \\\n"
    "    chromadb \\\n"
    "    janus-swi \\\n"
    "    openai \\\n"
    "    uagents \\\n"
    "    sentence-transformers"
)

NEW = (
    "# Single resolver pass so torch + transformers co-resolve compatibly.\n"
    "# --extra-index-url keeps the CPU-only torch wheel (no CUDA); PyPI stays primary\n"
    "# for the rest. No version pins (arm64 wheels remain selectable on native builds).\n"
    "RUN python3 -m pip install --no-cache-dir --break-system-packages \\\n"
    "    --extra-index-url https://download.pytorch.org/whl/cpu \\\n"
    "    torch \\\n"
    "    transformers \\\n"
    "    sentence-transformers \\\n"
    "    chromadb \\\n"
    "    janus-swi \\\n"
    "    openai \\\n"
    "    uagents"
)

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--apply", action="store_true")
    ap.add_argument("--reverse", action="store_true")
    a = ap.parse_args()
    if not DOCKERFILE.exists():
        print(f"MISSING {DOCKERFILE}"); return 1
    txt = DOCKERFILE.read_text()
    src, dst = (NEW, OLD) if a.reverse else (OLD, NEW)
    n = txt.count(src)
    print(f"{'REVERSE' if a.reverse else 'APPLY'}: anchor found {n}x (need exactly 1)")
    if n != 1:
        print("HALT: anchor not unique/found. No change."); return 1
    out = txt.replace(src, dst, 1)
    print(f"line delta: {out.count(chr(10)) - txt.count(chr(10)):+d}")
    if not a.apply:
        print("\n--- would change ---\n" + dst); print("\nDRY-RUN. Re-run with --apply."); return 0
    if not a.reverse:
        BAK.write_text(txt); print(f"backup: {BAK}")
    DOCKERFILE.write_text(out); print(f"wrote: {DOCKERFILE}")
    return 0

sys.exit(main())
