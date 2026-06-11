#!/usr/bin/env python3
"""Repair 2: Channel D soul-note interpolation (CLEAN RESTORATION).

DESIGN (Soul Evaluation and Routing v9 lines 119-123, 133-141): Channel D
receives the actual SOUL-NOTE from the verdict and calibrates tone to it.
RUNTIME: helper.py soul_voice_prompt carries the literal placeholder
"SOUL-NOTE from verdict"; the note is never extracted (survey H2).
REPAIR: extract the note inside soul_voice_prompt and interpolate it.
VERIFY (function level; end-to-end requires Repair 3, ledger W6): the
composed prompt for a synthetic PAUSE verdict contains the note text and
not the placeholder. Built into this script post-write.

Usage: --dry-run (default) | --apply | --reverse --apply
"""
import argparse, re, sys
from pathlib import Path

TARGET = Path("src/helper.py")

INSERT_ANCHOR = '''    """Channel D: soul voice composition (200 tokens, fires on PAUSE)."""
'''
INSERT_NEW = '''    """Channel D: soul voice composition (200 tokens, fires on PAUSE)."""
    # Repair 2 (2026-06-11): interpolate the actual SOUL-NOTE so Channel D
    # calibrates to the specific concern, not a placeholder (v9 lines 119-123).
    v = str(verdict)
    idx = v.find("SOUL-NOTE: ")
    note = v[idx + len("SOUL-NOTE: "):].strip() if idx >= 0 else v
'''
OLD_LINE = '"What the soul specifically observed (calibrate your tone to this): SOUL-NOTE from verdict. "'
NEW_LINE = '"What the soul specifically observed (calibrate your tone to this): " + note + ". "'

def forward(c):
    if OLD_LINE not in c:
        raise RuntimeError("placeholder not found (already applied or drifted)")
    if "Repair 2 (2026-06-11)" in c:
        raise RuntimeError("Repair 2 already applied")
    # scope the docstring anchor to soul_voice_prompt (the docstring text is unique to it)
    if c.count(INSERT_ANCHOR) != 1:
        raise RuntimeError("docstring anchor not unique")
    c = c.replace(INSERT_ANCHOR, INSERT_NEW, 1)
    return c.replace(OLD_LINE, NEW_LINE, 1)

def reverse(c):
    if NEW_LINE not in c or INSERT_NEW not in c:
        raise RuntimeError("applied state not found")
    c = c.replace(INSERT_NEW, INSERT_ANCHOR, 1)
    return c.replace(NEW_LINE, OLD_LINE, 1)

def verify_function(c):
    m = re.search(r"def soul_voice_prompt\(.*?\n(?=def )", c, re.S)
    if not m:
        return False, "function not found"
    ns = {}
    exec(m.group(0), ns)
    out = ns["soul_voice_prompt"]("PERSON-STATE: distressed",
        "VERDICT: PAUSE SOUL-NOTE: bypassing a verification step")
    ok = ("bypassing a verification step" in out
          and "SOUL-NOTE from verdict" not in out)
    return ok, out[:160]

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--apply", action="store_true")
    ap.add_argument("--reverse", action="store_true")
    a = ap.parse_args()
    c = TARGET.read_text()
    try:
        sim = (reverse if a.reverse else forward)(c)
    except RuntimeError as e:
        print(f"STATE CHECK FAILED: {e}"); return 1
    import py_compile, tempfile, os
    with tempfile.NamedTemporaryFile("w", suffix=".py", delete=False) as f:
        f.write(sim); tmp = f.name
    try:
        py_compile.compile(tmp, doraise=True)
    finally:
        os.unlink(tmp)
    print(f"Simulated clean: {len(c.splitlines())} -> {len(sim.splitlines())} lines; py-compile OK")
    if not a.reverse:
        ok, sample = verify_function(sim)
        print(f"FUNCTION VERIFY (synthetic PAUSE): {'PASS' if ok else 'FAIL'}")
        print(f"  prompt head: {sample}")
        if not ok: return 1
    if not a.apply:
        print("DRY-RUN: no writes. Re-run with --apply."); return 0
    bak = Path(str(TARGET) + ".bak.repair2")
    if not a.reverse:
        bak.write_text(c); print(f"Backup: {bak}")
    TARGET.write_text(sim)
    print(f"Wrote: {TARGET}  ({'REVERSE' if a.reverse else 'FORWARD'})")
    print("Rebuild required (image-baked): docker compose build --no-cache clarityclaw && docker compose up -d")
    return 0

if __name__ == "__main__":
    sys.exit(main())
