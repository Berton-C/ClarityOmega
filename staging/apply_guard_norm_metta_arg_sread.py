#!/usr/bin/env python3
"""
apply_guard_norm_metta_arg_sread.py

Crash fix 2 of 2: guard the output-verdict gate's inner sread
(soul/output_verdict.metta, norm-metta-arg).

Proven crash chain (probes 2026-07-02):
  After the metta-skill guard landed (src/skills.metta), the container still
  crashed at 3-4 iterations. Her batch contained a bang-prefixed metta
  argument: (metta "!(match &self $x $x)"). The per-cycle output-intercept
  gate walk (derive-gate-state -> batch-targets-soul? -> norm-metta-arg)
  re-parses every metta command argument with an UNGUARDED sread BEFORE the
  guarded metta skill ever runs. Isolated reproduction on the exact batch
  shape died at that sread with the exact live signature (main.pl:23 syntax
  error, exit 2, pre-SOUL-GATE-FLAG timing match).

The fix wraps that sread in catch and cases on (Error $a $b):
  - parse failure returns the EXPRESSION-shaped sentinel
    (UNPARSEABLE-METTA-ARG $e), which downstream car-atom consumers
    (metta-arg-mutates?, F25 hazard) handle goal-safely and classify
    non-mutating
  - parseable arguments return the parsed form unchanged ($else branch)
  - no-bypass argument: an unparseable arg cannot execute as a mutation,
    because the guarded metta skill returns METTA_ARGUMENT_PARSE_ERROR
    instead of evaluating it; gate inspects safely, skill executes safely
  - covers both consumers: batch-targets-soul? (output_verdict.metta) and
    soul-batch-op/soul-batch-head (soul_mutation_lock.metta)

Pattern grounds: identical catch/case idiom as the skills.metta guard
(probe-proven executing; HandleError production precedent in loop.metta).

Deployment note: soul/ is bind-mounted. NO REBUILD NEEDED. Apply + restart.

Conventions: dry-run default, --apply, --reverse, exact-substring match
(abort unless found exactly once, both directions), base64 byte-exact blocks,
code-aware paren counting (";" metta comments, string literals excluded),
all-or-none single edit. No em dashes.

Usage (run from repo root):
  python3 staging/apply_guard_norm_metta_arg_sread.py
  python3 staging/apply_guard_norm_metta_arg_sread.py --apply
  python3 staging/apply_guard_norm_metta_arg_sread.py --reverse --apply
"""

import argparse
import base64
import os
import sys

TARGET = "soul/output_verdict.metta"

_B = {
    'OLD': 'KD0gKG5vcm0tbWV0dGEtYXJnICRhKQogICAoaWYgKD09IChweS1jYWxsIChzb3VsX2dvdmVybmFuY2UucmVwcl9raW5kIChyZXByICRhKSkpIDEpIChzcmVhZCAkYSkgJGEpKQ==',
    'NEW': 'OzsgQ1JBU0ggR1VBUkQgKDIwMjYtMDctMDIpOiB0aGlzIHNyZWFkIHdhcyB0aGUgc2Vjb25kIHVuZ3VhcmRlZCBwYXJzZSBvZiBhbgo7OyBMTE0tc3VwcGxpZWQgc3RyaW5nIChmaXJzdDogdGhlIG1ldHRhIHNraWxsLCBndWFyZGVkIGluIHNyYy9za2lsbHMubWV0dGEpLgo7OyBBIG1hbGZvcm1lZCBtZXR0YSBhcmd1bWVudCAocHJvYmUtcHJvdmVuOiBiYW5nLXByZWZpeGVkICIhKG1hdGNoIC4uLikiKQo7OyB0aHJldyBhbiB1bmNhdWdodCBzeW50YXggZXJyb3IgaGVyZSBkdXJpbmcgdGhlIHBlci1jeWNsZSBnYXRlIHdhbGsKOzsgKGJhdGNoLXRhcmdldHMtc291bD8gLT4gbm9ybS1tZXR0YS1hcmcpLCBraWxsaW5nIHRoZSBjb250YWluZXIgYXQKOzsgbWFpbi5wbDoyMyBleGl0IDIgQkVGT1JFIHRoZSBvdXRwdXQgdmVyZGljdCBwcmludGVkLiBSZXByb2R1Y2VkIGluIGFuCjs7IGlzb2xhdGVkIHByb2JlIG9uIHRoZSBleGFjdCBsaXZlIGJhdGNoIHNoYXBlLgo7OyBUaGUgY2F0Y2ggY29udmVydHMgdGhlIHRocm93IHRvIGFuIChFcnJvciAuLi4pIHRlcm07IHRoZSBFcnJvciBicmFuY2gKOzsgcmV0dXJucyBhbiBFWFBSRVNTSU9OLXNoYXBlZCBzZW50aW5lbCAobm90IGEgYmFyZSBhdG9tKSBzbyBkb3duc3RyZWFtCjs7IGNhci1hdG9tIGNvbnN1bWVycyAobWV0dGEtYXJnLW11dGF0ZXM/LCBGMjUgaGF6YXJkKSBzdGF5IGdvYWwtc2FmZSBhbmQKOzsgY2xhc3NpZnkgaXQgbm9uLW11dGF0aW5nLiBTYWZldHkgdnMgdGhlICJuYWl2ZWx5IHNraXBwZWQgd2F2ZXMgbXV0YXRpb25zCjs7IHRocm91Z2giIHdhcm5pbmcgYWJvdmU6IGFuIHVucGFyc2VhYmxlIGFyZyBjYW5ub3QgZXhlY3V0ZSBhcyBhIG11dGF0aW9uLAo7OyBiZWNhdXNlIHRoZSBndWFyZGVkIG1ldHRhIHNraWxsIHJldHVybnMgTUVUVEFfQVJHVU1FTlRfUEFSU0VfRVJST1IKOzsgaW5zdGVhZCBvZiBldmFsdWF0aW5nIGl0LiBHYXRlIGluc3BlY3RzIHNhZmVseTsgc2tpbGwgZXhlY3V0ZXMgc2FmZWx5LgooPSAobm9ybS1tZXR0YS1hcmcgJGEpCiAgIChpZiAoPT0gKHB5LWNhbGwgKHNvdWxfZ292ZXJuYW5jZS5yZXByX2tpbmQgKHJlcHIgJGEpKSkgMSkKICAgICAgIChsZXQgJHAgKGNhdGNoIChzcmVhZCAkYSkpCiAgICAgICAgICAgIChjYXNlICRwCiAgICAgICAgICAgICAgKCgoRXJyb3IgJGUgJGQpIChVTlBBUlNFQUJMRS1NRVRUQS1BUkcgJGUpKQogICAgICAgICAgICAgICAoJGVsc2UgJHApKSkpCiAgICAgICAkYSkp',
}

def _d(k):
    return base64.b64decode(_B[k]).decode("utf-8")


def code_aware_paren_count(text):
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
    print("GUARD norm-metta-arg sread (crash fix 2, output_verdict.metta)")
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
        print(">>> WRITTEN. soul/ is bind-mounted: NO rebuild. Restart the container.")
    else:
        print(">>> DRY-RUN only. Re-run with --apply to write.")


if __name__ == "__main__":
    main()
