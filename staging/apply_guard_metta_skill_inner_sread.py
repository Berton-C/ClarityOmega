#!/usr/bin/env python3
"""
apply_guard_metta_skill_inner_sread.py

Crash fix: guard the metta skill's inner sread (src/skills.metta lines 56-58).

Proven crash chain (probes 2026-07-01):
  Genesis directive + the getSkills |- NAL examples lead Clarity to emit
  (metta "...") commands whose argument is escaped-quote-prefixed content
  (e.g. \"(|- ... copied from the examples). The outer batch parse is guarded
  and survives; the metta skill re-parses its string argument at
  skills.metta:57 with an UNGUARDED sread. The quote-prefixed form throws an
  uncaught syntax error (main.pl:23), exit code 2, container dies. Isolated
  probe reproduced the exact live signature on the quote-prefixed form (Form
  B) while the clean balanced form (Form A) parses fine; one throw killed the
  whole probe process, demonstrating the kill behavior.

The fix wraps the inner sread in catch and cases on (Error $a $b):
  - parse failure returns (METTA_ARGUMENT_PARSE_ERROR <detail>) through the
    normal COMMAND_RETURN feedback path (she sees it next cycle, like every
    handled error) instead of killing the container
  - parseable arguments take the $else branch, which is the current body
    UNCHANGED, so normal behavior is byte-identical

Pattern grounds (Atom_Operations_Map has no catch/case coverage; validity
rests on): catch-around-sread in a let bind, probe-proven executing this
session; case on (Error $a $b), the HandleError production pattern in
loop.metta, fired thousands of times.

Upstream status: Patrick's current mettaclaw skills.metta has the SAME
unguarded sread (verified against attached upstream copy). Unfixed upstream,
so fixed here per fork policy. Worth reporting upstream.

Conventions: dry-run default, --apply, --reverse, exact-substring match
(abort unless found exactly once, both directions), base64 byte-exact blocks,
code-aware paren counting (";" metta comments, string literals excluded),
all-or-none single edit. py_compile does not apply to .metta; the structural
check is the paren count. No em dashes.

Usage (run from repo root):
  python3 staging/apply_guard_metta_skill_inner_sread.py
  python3 staging/apply_guard_metta_skill_inner_sread.py --apply
  python3 staging/apply_guard_metta_skill_inner_sread.py --reverse --apply
"""

import argparse
import base64
import os
import sys

TARGET = "src/skills.metta"

_B = {
    'OLD': 'KD0gKG1ldHRhICRzdHIpCiAgIChsZXQgJGNvZGUgKHNyZWFkICRzdHIpCiAgICAgICAgKHJlcHIgKHByb2duIChjYWxsX3dpdGhfaW5mZXJlbmNlX2xpbWl0IChQcmVkaWNhdGUgKHF1b3RlIChldmFsICRjb2RlICR4KSkpIDEwMDAwMDAwMCkgJHgpKSkp',
    'NEW': 'OzsgR3VhcmRlZCBtZXR0YSBza2lsbDogdGhlIGlubmVyIHNyZWFkIHJlLXBhcnNlcyB0aGUgTExNLXN1cHBsaWVkIGFyZ3VtZW50Cjs7IHN0cmluZy4gVW5ndWFyZGVkLCBhIG1hbGZvcm1lZCBhcmd1bWVudCAoZS5nLiBlc2NhcGVkLXF1b3RlLXByZWZpeGVkIHwtCjs7IGNvbnRlbnQgY29waWVkIGZyb20gdGhlIE5BTCBleGFtcGxlcyBkdXJpbmcgR2VuZXNpcyBlbmNvdW50ZXJzKSB0aHJvd3MgYW4KOzsgdW5jYXVnaHQgc3ludGF4IGVycm9yIGF0IG1haW4ucGw6MjMgYW5kIGtpbGxzIHRoZSBjb250YWluZXIgKGV4aXQgMikuCjs7IFByb3ZlbiBieSBpc29sYXRlZCBwcm9iZSAyMDI2LTA3LTAxOiBxdW90ZS1wcmVmaXhlZCBmb3JtIHJlcHJvZHVjZXMgdGhlCjs7IGV4YWN0IGNyYXNoIHNpZ25hdHVyZTsgY2F0Y2ggY29udmVydHMgaXQgdG8gYW4gKEVycm9yIC4uLikgdGVybS4KOzsgUGF0dGVybiBncm91bmRzOiBjYXRjaC1hcm91bmQtc3JlYWQgaW4gYSBsZXQgYmluZCAocHJvYmUtcHJvdmVuIGV4ZWN1dGluZyksCjs7IGNhc2Ugb24gKEVycm9yICRhICRiKSAoSGFuZGxlRXJyb3IgcHJvZHVjdGlvbiBwcmVjZWRlbnQsIGxvb3AubWV0dGEpLgo7OyBVcHN0cmVhbSBzdGF0dXM6IFBhdHJpY2sncyBjdXJyZW50IG1ldHRhY2xhdyBoYXMgdGhlIHNhbWUgdW5ndWFyZGVkIHNyZWFkOwo7OyBmaXhlZCBoZXJlIHBlciBmb3JrIHBvbGljeSAodW5maXhlZCB1cHN0cmVhbSAtPiBmaXggdG8gcGVyZm9ybSBhcyBpbnRlbmRlZCkuCjs7IEEgcGFyc2UgZmFpbHVyZSBub3cgcmV0dXJucyBNRVRUQV9BUkdVTUVOVF9QQVJTRV9FUlJPUiB0aHJvdWdoIHRoZSBub3JtYWwKOzsgQ09NTUFORF9SRVRVUk4gZmVlZGJhY2sgcGF0aCBpbnN0ZWFkIG9mIGNyYXNoaW5nIHRoZSBwcm9jZXNzLgooPSAobWV0dGEgJHN0cikKICAgKGxldCAkY29kZSAoY2F0Y2ggKHNyZWFkICRzdHIpKQogICAgICAgIChjYXNlICRjb2RlCiAgICAgICAgICAoKChFcnJvciAkYSAkYikgKHJlcHIgKE1FVFRBX0FSR1VNRU5UX1BBUlNFX0VSUk9SICRhKSkpCiAgICAgICAgICAgKCRlbHNlIChyZXByIChwcm9nbiAoY2FsbF93aXRoX2luZmVyZW5jZV9saW1pdCAoUHJlZGljYXRlIChxdW90ZSAoZXZhbCAkY29kZSAkeCkpKSAxMDAwMDAwMDApICR4KSkpKSkpKQ==',
}

def _d(k):
    return base64.b64decode(_B[k]).decode("utf-8")


def code_aware_paren_count(text):
    """Count parens excluding string literals and ; line comments (metta)."""
    opens = closes = 0
    in_str = False
    esc = False
    in_comment = False
    for ch in text:
        if in_comment:
            if ch == "\n":
                in_comment = False
            continue
        if in_str:
            if esc:
                esc = False
            elif ch == "\\":
                esc = True
            elif ch == '"':
                in_str = False
            continue
        if ch == '"':
            in_str = True
        elif ch == ";":
            in_comment = True
        elif ch == "(":
            opens += 1
        elif ch == ")":
            closes += 1
    return opens, closes


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--apply", action="store_true")
    ap.add_argument("--reverse", action="store_true")
    args = ap.parse_args()

    old, new = _d("OLD"), _d("NEW")
    a, b = (new, old) if args.reverse else (old, new)

    if not os.path.exists(TARGET):
        print("ABORT: %s not found. Run from repo root." % TARGET)
        sys.exit(1)
    before = open(TARGET, "r", encoding="utf-8").read()

    n = before.count(a)
    if n != 1:
        print("ABORT: target found %d times (need exactly 1). Direction=%s"
              % (n, "REVERSE" if args.reverse else "FORWARD"))
        sys.exit(1)
    after = before.replace(a, b, 1)

    ob, cb = code_aware_paren_count(before)
    no, nc = code_aware_paren_count(after)

    print("=" * 70)
    print("GUARD metta skill inner sread (crash fix, skills.metta)")
    print("=" * 70)
    print("file      : %s" % TARGET)
    print("direction : %s" % ("REVERSE" if args.reverse else "FORWARD"))
    print("mode      : %s" % ("APPLY (writing)" if args.apply else "DRY-RUN (no write)"))
    print("code-aware parens: opens %d->%d closes %d->%d  delta before=%d after=%d  %s"
          % (ob, no, cb, nc, ob - cb, no - nc,
             "OK (balanced both)" if (ob - cb) == (no - nc) == 0 else "NOTE inspect"))
    print()
    print("--- removing ---")
    print(a)
    print("--- inserting ---")
    print(b)
    print()

    if args.apply:
        with open(TARGET, "w", encoding="utf-8") as f:
            f.write(after)
        print(">>> WRITTEN. Next: rebuild --no-cache, restart, let Genesis run.")
    else:
        print(">>> DRY-RUN only. Re-run with --apply to write.")


if __name__ == "__main__":
    main()
