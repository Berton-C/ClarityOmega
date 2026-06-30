#!/usr/bin/env python3
"""
apply_canon_balance_parens_and_line_contract.py

Coordinated, all-or-none fix for the command-malformation root cause.

Root cause (proven across 16 tests this session):
  Our OUTPUT_FORMAT instructed a single-blob ((cmd)(cmd)) shape and our
  balance_parentheses tried to salvage-and-wrap that blob, manufacturing
  (((( over-nesting and swallowing inline/trailing reasoning. Patrick's
  current upstream balance_parentheses solves this by splitting on
  command-headed lines, JSON-quoting each argument, and joining once. It
  requires the matching input contract: one command per line, reasoning out
  of the command stream. Test 14 proved his function produces correct
  superpose-ready ((cmd)(cmd)) batches for OUR exact command set given that
  contract.

Both halves land together (all-or-none): function alone breaks current blobs
(Test 12); contract alone does nothing (old function does not line-split).

Two files, four edits:
  src/helper.py:
    H1  add `import json` after the existing `import re`
    H23 insert LLM_COMMANDS (OUR 15) + quote_arg + starts_command_line +
        split_command_blocks, and replace balance_parentheses with the canon
        version (one contiguous replacement of the old function block)
  soul/behavioral_guidance.metta:
    B1  replace OUTPUT_FORMAT body with the explicit line-per-command contract

Conventions (apply_task_state_step2_wiring.py template): dry-run default,
--apply, --reverse, exact-substring match (abort unless found exactly once,
both directions), code-aware paren counting, pre/post paren-delta report,
py_compile of simulated helper.py, action summary, all-or-none. No em dashes.

OLD/NEW blocks are stored base64 to guarantee byte-exact matching (no source
escaping drift).

Usage (run from repo root):
  python3 staging/apply_canon_balance_parens_and_line_contract.py
  python3 staging/apply_canon_balance_parens_and_line_contract.py --apply
  python3 staging/apply_canon_balance_parens_and_line_contract.py --reverse --apply
"""

import argparse
import base64
import py_compile
import sys
import tempfile
import os

HELPER = "src/helper.py"
GUIDANCE = "soul/behavioral_guidance.metta"

_B = {
    'H1_OLD': 'ZnJvbSBjb2xsZWN0aW9ucyBpbXBvcnQgZGVxdWUKaW1wb3J0IHJlCg==',
    'H1_NEW': 'ZnJvbSBjb2xsZWN0aW9ucyBpbXBvcnQgZGVxdWUKaW1wb3J0IHJlCmltcG9ydCBqc29uCg==',
    'H23_OLD': 'ZGVmIGJhbGFuY2VfcGFyZW50aGVzZXMocyk6CiAgICBzID0gcy5yZXBsYWNlKCJfcXVvdGVfIiwgJyInKS5zdHJpcCgpCiAgICBmaXJzdF9wYXJlbiA9IHMuZmluZCgnKCcpCiAgICBpZiBmaXJzdF9wYXJlbiA+IDA6CiAgICAgICAgZ2FyYmFnZSA9IHNbOmZpcnN0X3BhcmVuXS5zdHJpcCgpCiAgICAgICAgcyA9IHNbZmlyc3RfcGFyZW46XQogICAgICAgIGlmIGdhcmJhZ2U6CiAgICAgICAgICAgIGdhcmJhZ2UgPSBnYXJiYWdlLnJlcGxhY2UoJyInLCAnXFwiJykKICAgICAgICAgICAgcyA9IHNbOjFdICsgZicocGluICJ7Z2FyYmFnZX0iKSAnICsgc1sxOl0KICAgIGlmIHMuc3RhcnRzd2l0aCgiKCgiKSBhbmQgcy5lbmRzd2l0aCgiKSkiKToKICAgICAgICByZXR1cm4gcwogICAgaWYgcy5zdGFydHN3aXRoKCIoIikgYW5kIHMuZW5kc3dpdGgoIikiKToKICAgICAgICByZXR1cm4gZiIoe3N9KSIKICAgIHJldHVybiBmIigoe3N9KSki',
    'H23_NEW': 'IyAtLS0tIENhbm9uIGNvbW1hbmQtYmF0Y2ggYXNzZW1ibGVyIChhZG9wdGVkIGZyb20gcGF0aGFtOS9tZXR0YWNsYXcgdXBzdHJlYW0pIC0tLS0KIyBSZXBsYWNlcyB0aGUgcHJpb3Igc2FsdmFnZS1hbmQtd3JhcCBiYWxhbmNlX3BhcmVudGhlc2VzLCB3aGljaCBtYW51ZmFjdHVyZWQKIyAoKCgoIG92ZXItbmVzdGluZyBmcm9tIGJsb2IgaW5wdXQgKHNlc3Npb24gZGlhZ25vc2lzLCAxNiB0ZXN0cykuIFBhdHJpY2sncwojIGRlc2lnbjogc3BsaXQgdGhlIHJlc3BvbnNlIGludG8gY29tbWFuZC1oZWFkZWQgbGluZXMsIEpTT04tcXVvdGUgZWFjaAojIGFyZ3VtZW50LCBqb2luIG9uY2UgaW50byB0aGUgc3VwZXJwb3NlLXJlYWR5ICgoY21kKShjbWQpKSBiYXRjaC4gUmVxdWlyZXMgdGhlCiMgb25lLWNvbW1hbmQtcGVyLWxpbmUgT1VUUFVUX0ZPUk1BVCBjb250cmFjdCAoYmVoYXZpb3JhbF9ndWlkYW5jZS5tZXR0YSkuCiMgTExNX0NPTU1BTkRTIHJlY29uY2lsZWQgdG8gT1VSIGxpdmUgc2tpbGwgc2V0ICgxNSk6IGdldFNraWxscyAxMyArIHByb21vdGUKIyArIGRlbW90ZSAocHJvbW90ZS9kZW1vdGUgbGl2ZSBpbiBtZW1vcnkubWV0dGEsIHVzZWQgd2hlbiBwcm9tcHRlZCkuCkxMTV9DT01NQU5EUyA9IHsKICAgICJwaW4iLAogICAgInJlbWVtYmVyIiwKICAgICJxdWVyeSIsCiAgICAiZXBpc29kZXMiLAogICAgInNlYXJjaCIsCiAgICAic2VuZCIsCiAgICAicHJvbW90ZSIsCiAgICAiZGVtb3RlIiwKICAgICJtZXR0YSIsCiAgICAic2hlbGwiLAogICAgInJlYWQtZmlsZSIsCiAgICAid3JpdGUtZmlsZSIsCiAgICAiYXBwZW5kLWZpbGUiLAogICAgInRhdmlseS1zZWFyY2giLAogICAgInRlY2huaWNhbC1hbmFseXNpcyIsCn0KCgpkZWYgcXVvdGVfYXJnKHgpOgogICAgcmV0dXJuIGpzb24uZHVtcHMoeCwgZW5zdXJlX2FzY2lpPUZhbHNlKQoKCmRlZiBzdGFydHNfY29tbWFuZF9saW5lKGxpbmUpOgogICAgcyA9IGxpbmUubHN0cmlwKCkKICAgIGlmIG5vdCBzOgogICAgICAgIHJldHVybiBGYWxzZQogICAgaWYgcy5zdGFydHN3aXRoKCIoIik6CiAgICAgICAgcyA9IHNbMTpdLmxzdHJpcCgpCiAgICBpZiBub3QgczoKICAgICAgICByZXR1cm4gRmFsc2UKICAgIGZpcnN0ID0gcy5zcGxpdChtYXhzcGxpdD0xKVswXS5yc3RyaXAoIikiKQogICAgcmV0dXJuIGZpcnN0IGluIExMTV9DT01NQU5EUwoKCmRlZiBzcGxpdF9jb21tYW5kX2Jsb2NrcyhzKToKICAgIGJsb2NrcyA9IFtdCiAgICBjdXIgPSBbXQogICAgZm9yIHJhdyBpbiBzLnNwbGl0bGluZXMoKToKICAgICAgICBpZiBub3QgcmF3LnN0cmlwKCk6CiAgICAgICAgICAgIGlmIGN1cjoKICAgICAgICAgICAgICAgIGN1ci5hcHBlbmQocmF3KQogICAgICAgICAgICBjb250aW51ZQogICAgICAgIGlmIHN0YXJ0c19jb21tYW5kX2xpbmUocmF3KSBhbmQgY3VyOgogICAgICAgICAgICBibG9ja3MuYXBwZW5kKCJcbiIuam9pbihjdXIpLnN0cmlwKCkpCiAgICAgICAgICAgIGN1ciA9IFtyYXddCiAgICAgICAgZWxzZToKICAgICAgICAgICAgY3VyLmFwcGVuZChyYXcpCiAgICBpZiBjdXI6CiAgICAgICAgYmxvY2tzLmFwcGVuZCgiXG4iLmpvaW4oY3VyKS5zdHJpcCgpKQogICAgcmV0dXJuIGJsb2NrcwoKCmRlZiBiYWxhbmNlX3BhcmVudGhlc2VzKHMpOgogICAgcyA9IHMucmVwbGFjZSgiX3F1b3RlXyIsICciJykucmVwbGFjZSgiX25ld2xpbmVfIiwgIlxuIikKICAgIHNleHBycyA9IFtdCiAgICBzcGVjaWFsX3R3b19hcmdfY21kcyA9IHsid3JpdGUtZmlsZSIsICJhcHBlbmQtZmlsZSJ9CiAgICBmb3IgbGluZSBpbiBzcGxpdF9jb21tYW5kX2Jsb2NrcyhzKToKICAgICAgICBsaW5lID0gbGluZS5zdHJpcCgpCiAgICAgICAgaWYgbm90IGxpbmU6CiAgICAgICAgICAgIGNvbnRpbnVlCiAgICAgICAgaWYgbGluZS5zdGFydHN3aXRoKCIoLSIpOgogICAgICAgICAgICBsaW5lID0gIihwaW4gLSIgKyBsaW5lWzI6XQogICAgICAgIGVsaWYgbGluZS5zdGFydHN3aXRoKCItIik6CiAgICAgICAgICAgIGxpbmUgPSAicGluICIgKyBsaW5lCiAgICAgICAgaWYgbGluZS5zdGFydHN3aXRoKCIoIikgYW5kIGxpbmUuZW5kc3dpdGgoIikiKToKICAgICAgICAgICAgbGluZSA9IGxpbmVbMTotMV0uc3RyaXAoKQogICAgICAgIGVsaWYgbGluZS5zdGFydHN3aXRoKCIoIik6CiAgICAgICAgICAgIGxpbmUgPSBsaW5lWzE6XS5zdHJpcCgpCiAgICAgICAgcGFydHMgPSBsaW5lLnNwbGl0KG1heHNwbGl0PTEpCiAgICAgICAgaWYgbm90IHBhcnRzOgogICAgICAgICAgICBjb250aW51ZQogICAgICAgIGNtZCA9IHBhcnRzWzBdCiAgICAgICAgcmVzdCA9IHBhcnRzWzFdLnN0cmlwKCkgaWYgbGVuKHBhcnRzKSA+IDEgZWxzZSAiIgogICAgICAgIGlmIGNtZCBpbiBzcGVjaWFsX3R3b19hcmdfY21kczoKICAgICAgICAgICAgaWYgbm90IHJlc3Q6CiAgICAgICAgICAgICAgICBzZXhwcnMuYXBwZW5kKGYiKHtjbWR9KSIpCiAgICAgICAgICAgICAgICBjb250aW51ZQogICAgICAgICAgICBpZiByZXN0LnN0YXJ0c3dpdGgoJyInKToKICAgICAgICAgICAgICAgIGVuZCA9IDEKICAgICAgICAgICAgICAgIGVzY2FwZWQgPSBGYWxzZQogICAgICAgICAgICAgICAgd2hpbGUgZW5kIDwgbGVuKHJlc3QpOgogICAgICAgICAgICAgICAgICAgIGNoID0gcmVzdFtlbmRdCiAgICAgICAgICAgICAgICAgICAgaWYgY2ggPT0gJyInIGFuZCBub3QgZXNjYXBlZDoKICAgICAgICAgICAgICAgICAgICAgICAgYnJlYWsKICAgICAgICAgICAgICAgICAgICBlc2NhcGVkID0gKGNoID09ICdcXCcgYW5kIG5vdCBlc2NhcGVkKQogICAgICAgICAgICAgICAgICAgIGlmIGNoICE9ICdcXCc6CiAgICAgICAgICAgICAgICAgICAgICAgIGVzY2FwZWQgPSBGYWxzZQogICAgICAgICAgICAgICAgICAgIGVuZCArPSAxCiAgICAgICAgICAgICAgICBpZiBlbmQgPCBsZW4ocmVzdCkgYW5kIHJlc3RbZW5kXSA9PSAnIic6CiAgICAgICAgICAgICAgICAgICAgZmlsZW5hbWUgPSByZXN0WzplbmQrMV0KICAgICAgICAgICAgICAgICAgICBjb250ZW50ID0gcmVzdFtlbmQrMTpdLnN0cmlwKCkKICAgICAgICAgICAgICAgIGVsc2U6CiAgICAgICAgICAgICAgICAgICAgZmlsZW5hbWUgPSBxdW90ZV9hcmcocmVzdFsxOl0pCiAgICAgICAgICAgICAgICAgICAgY29udGVudCA9ICIiCiAgICAgICAgICAgIGVsc2U6CiAgICAgICAgICAgICAgICBzcGxpdF9yZXN0ID0gcmVzdC5zcGxpdChtYXhzcGxpdD0xKQogICAgICAgICAgICAgICAgZmlsZW5hbWUgPSBxdW90ZV9hcmcoc3BsaXRfcmVzdFswXSkKICAgICAgICAgICAgICAgIGNvbnRlbnQgPSBzcGxpdF9yZXN0WzFdLnN0cmlwKCkgaWYgbGVuKHNwbGl0X3Jlc3QpID4gMSBlbHNlICIiCiAgICAgICAgICAgIGlmIGNvbnRlbnQ6CiAgICAgICAgICAgICAgICBpZiBjb250ZW50LnN0YXJ0c3dpdGgoJyInKSBhbmQgY29udGVudC5lbmRzd2l0aCgnIicpIGFuZCAiXG4iIG5vdCBpbiBjb250ZW50OgogICAgICAgICAgICAgICAgICAgIHNleHBycy5hcHBlbmQoZiIoe2NtZH0ge2ZpbGVuYW1lfSB7Y29udGVudH0pIikKICAgICAgICAgICAgICAgIGVsc2U6CiAgICAgICAgICAgICAgICAgICAgc2V4cHJzLmFwcGVuZChmIih7Y21kfSB7ZmlsZW5hbWV9IHtxdW90ZV9hcmcoY29udGVudCl9KSIpCiAgICAgICAgICAgIGVsc2U6CiAgICAgICAgICAgICAgICBzZXhwcnMuYXBwZW5kKGYiKHtjbWR9IHtmaWxlbmFtZX0pIikKICAgICAgICAgICAgY29udGludWUKICAgICAgICBpZiByZXN0OgogICAgICAgICAgICBpZiByZXN0LnN0YXJ0c3dpdGgoJyInKSBhbmQgcmVzdC5lbmRzd2l0aCgnIicpIGFuZCAiXG4iIG5vdCBpbiByZXN0OgogICAgICAgICAgICAgICAgc2V4cHJzLmFwcGVuZChmIih7Y21kfSB7cmVzdH0pIikKICAgICAgICAgICAgZWxzZToKICAgICAgICAgICAgICAgIHNleHBycy5hcHBlbmQoZiIoe2NtZH0ge3F1b3RlX2FyZyhyZXN0KX0pIikKICAgICAgICBlbHNlOgogICAgICAgICAgICBzZXhwcnMuYXBwZW5kKGYiKHtjbWR9KSIpCiAgICByZXQgPSAiICIuam9pbihzZXhwcnMpCiAgICByZXR1cm4gIigiICsgcmV0ICsgIiki',
    'B1_OLD': 'KD0gKG91dHB1dC1mb3JtYXQtZ3VpZGFuY2UpCiAgICJPVVRQVVRfRk9STUFUOiBPdXRwdXQgYSAoKHNraWxsTmFtZTEgYXJnczEpIChza2lsbE5hbWUyIGFyZ3MyKSAuLi4gKHNraWxsTmFtZU4gYXJnc04pKSBTLWV4cHJlc3Npb24gd2l0aCBhcyBtYW55IGNvbW1hbmRzIGFzIHRoZSB3b3JrIHJlcXVpcmVzLiBGb3IgYSBzaW5nbGUgY29tbWFuZDogKChza2lsbE5hbWUgYXJncykpIG5vdCAoc2tpbGxOYW1lIGFyZ3MpLiBFYWNoIGFyZyBpcyBhbiBleHBsaWNpdCBzdHJpbmcgaGVuY2UgbmVlZHMgcXVvdGVzIChtdWx0aS13b3JkIHN0cmluZ3MgbXVzdCBiZSBvbmUgcXVvdGVkIHN0cmluZyksIGFuZCB2YXJpYWJsZXMgYXJlIGZvcmJpZGRlbiEgVmVyaWZ5IGJhbGFuY2VkIHBhcmVudGhlc2VzIGFuZCBxdW90ZXMgYmVmb3JlIGVtaXR0aW5nLiIp',
    'B1_NEW': 'KD0gKG91dHB1dC1mb3JtYXQtZ3VpZGFuY2UpCiAgICJPVVRQVVRfRk9STUFUOiBFbWl0IG9uZSBjb21tYW5kIHBlciBsaW5lLiBUaGUgcnVsZSBmb3IgZWFjaCBjb21tYW5kIGxpbmUsIGV4YWN0bHk6IG9wZW4gd2l0aCBhIHNpbmdsZSBsZWZ0IHBhcmVudGhlc2lzLCB0aGVuIHRoZSBza2lsbCBuYW1lIGFzIHRoZSB2ZXJ5IGZpcnN0IHRva2VuLCB0aGVuIG9uZSBzcGFjZSwgdGhlbiB0aGUgYXJndW1lbnQgYXMgb25lIGRvdWJsZS1xdW90ZWQgc3RyaW5nLCB0aGVuIGEgc2luZ2xlIHJpZ2h0IHBhcmVudGhlc2lzLiBPbmUgcGFpciBvZiBwYXJlbnRoZXNlcyBwZXIgbGluZSwgbmV2ZXIgdHdvLCBuZXZlciBtb3JlLiBOb3RoaW5nIGJlZm9yZSB0aGUgb3BlbmluZyBwYXJlbnRoZXNpcyBhbmQgbm90aGluZyBhZnRlciB0aGUgY2xvc2luZyBwYXJlbnRoZXNpcyBvbiB0aGF0IGxpbmUuIEV4YW1wbGVzLCBlYWNoIGEgY29tcGxldGUgbGluZTogKHNlbmQgXCJoZWxsbyB0aGVyZVwiKSBhbmQgKG1ldHRhIFwiKG1hdGNoICZzZWxmIGZvbyBiYXIpXCIpIGFuZCAocGluIFwiY2hlY2tpbmcgdGhlIGZpbGUgbm93XCIpLiBQdXQgYXMgbWFueSBjb21tYW5kIGxpbmVzIGFzIHRoZSB3b3JrIHJlcXVpcmVzLCBlYWNoIG9uIGl0cyBvd24gbGluZS4gRG8gYWxsIG9mIHlvdXIgdGhpbmtpbmcgYW5kIGRlbGliZXJhdGlvbiBCRUZPUkUgdGhlIGNvbW1hbmQgbGluZXMsIG5ldmVyIG1peGVkIGludG8gdGhlbTogdGhlIGNvbW1hbmQgbGluZXMgYXJlIGNvbW1hbmRzIG9ubHksIG5vdCByZWFzb25pbmcgb3Igbm90ZXMuIFRoZSBhcmd1bWVudCBpcyBhbHdheXMgb25lIGRvdWJsZS1xdW90ZWQgc3RyaW5nIChtdWx0aS13b3JkIGFyZ3VtZW50cyBtdXN0IGJlIGEgc2luZ2xlIHF1b3RlZCBzdHJpbmcpLCBhbmQgdmFyaWFibGVzIGFyZSBmb3JiaWRkZW4uIEZvciB3cml0ZS1maWxlIGFuZCBhcHBlbmQtZmlsZSwgdGhlIGZpbGUgY29udGVudCBhcmd1bWVudCBtYXkgc3BhbiBtdWx0aXBsZSBsaW5lczsgdGhhdCBpcyB0aGUgb25lIHBsYWNlIG11bHRpLWxpbmUgY29udGVudCBiZWxvbmdzLiBwaW4gdGFrZXMgYSBicmllZiBzaW5nbGUtbGluZSBub3RlLCBuZXZlciBhIG1vbm9sb2d1ZS4iKQ==',
}

def _d(k):
    return base64.b64decode(_B[k]).decode("utf-8")

# (label, path, OLD, NEW)
EDITS = [
    ("H1 import json", HELPER, _d("H1_OLD"), _d("H1_NEW")),
    ("H23 canon balance_parentheses", HELPER, _d("H23_OLD"), _d("H23_NEW")),
    ("B1 OUTPUT_FORMAT line contract", GUIDANCE, _d("B1_OLD"), _d("B1_NEW")),
]


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
        elif ch == "#":
            in_comment = True
        elif ch == ";":
            in_comment = True
        elif ch == "(":
            opens += 1
        elif ch == ")":
            closes += 1
    return opens, closes


def process_file(path, reverse):
    try:
        text = open(path, "r", encoding="utf-8").read()
    except FileNotFoundError:
        return None, "ABORT: %s not found. Run from repo root." % path
    report = []
    for label, epath, old, new in EDITS:
        if epath != path:
            continue
        a, b = (new, old) if reverse else (old, new)
        n = text.count(a)
        if n != 1:
            return None, ("ABORT [%s in %s]: target found %d times (need exactly 1)."
                          % (label, path, n))
        text = text.replace(a, b, 1)
        report.append(label)
    return text, report


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--apply", action="store_true")
    ap.add_argument("--reverse", action="store_true")
    args = ap.parse_args()

    files = sorted(set(e[1] for e in EDITS))
    print("=" * 72)
    print("CANON balance_parentheses + line-per-command OUTPUT_FORMAT (all-or-none)")
    print("=" * 72)
    print("direction : %s" % ("REVERSE" if args.reverse else "FORWARD"))
    print("mode      : %s" % ("APPLY (writing)" if args.apply else "DRY-RUN (no write)"))
    print("files     : %s" % ", ".join(files))
    print()

    results = {}
    for path in files:
        if not os.path.exists(path):
            print("ABORT: %s not found. Run from repo root." % path)
            sys.exit(1)
        before = open(path, "r", encoding="utf-8").read()
        new_text, report = process_file(path, args.reverse)
        if new_text is None:
            print(report)
            sys.exit(1)
        ob, cb = code_aware_paren_count(before)
        no, nc = code_aware_paren_count(new_text)
        results[path] = new_text
        print("FILE %s" % path)
        print("  edits (simulated): %s" % ", ".join(report))
        print("  code-aware parens opens %d->%d closes %d->%d  delta before=%d after=%d  %s"
              % (ob, no, cb, nc, ob - cb, no - nc,
                 "OK" if (ob - cb) == (no - nc) == 0 else "NOTE inspect"))
        print()

    helper_new = results[HELPER]
    with tempfile.NamedTemporaryFile("w", suffix=".py", delete=False, encoding="utf-8") as tf:
        tf.write(helper_new)
        tmp = tf.name
    try:
        py_compile.compile(tmp, doraise=True)
        print("py_compile of simulated %s: PASS" % HELPER)
    except py_compile.PyCompileError as e:
        print("py_compile of simulated %s: FAIL" % HELPER)
        print(e)
        os.unlink(tmp)
        sys.exit(1)
    os.unlink(tmp)
    print()

    if args.apply:
        for path, new_text in results.items():
            with open(path, "w", encoding="utf-8") as f:
                f.write(new_text)
        print(">>> WRITTEN to %d file(s). Next: rebuild --no-cache, restart." % len(results))
    else:
        print(">>> DRY-RUN only. Re-run with --apply to write.")


if __name__ == "__main__":
    main()
