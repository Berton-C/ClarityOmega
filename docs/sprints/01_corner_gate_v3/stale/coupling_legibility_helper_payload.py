# ============================================================
# coupling_legibility_helper_payload.py
# Draft A payload 3 of 3. Design canon: corner_gate_v3_adapter_design.md v0.6.
# Status: DRAFT FOR BERTON LAYER-1 REVIEW.
#
# These functions are appended to src/helper.py by the monolith (Phase 3).
# Python is only ever the hands for MeTTa and never does reasoning
# (ratified). Three jobs only: line formatting, command signature hashing,
# target extraction. Content of sends and pins is NEVER read; only command
# heads and first arguments (paths, patterns) are touched, which is string
# plumbing, not reasoning.
#
# REVIEW-FLAG RF2: design doc named one helper payload (coupling_line_format).
# This payload carries four functions because signature hashing and target
# extraction are string plumbing MeTTa cannot do. For markup.
#
# Totality contract (ratified formatter cases): every function always
# returns a string, never throws, and never turns missing data into
# semantic content.
# ============================================================

import hashlib
import re


def _cl_safe_str(v):
    """Defensive string coercion. None and empty become the empty string."""
    try:
        if v is None:
            return ""
        s = str(v)
        return s
    except Exception:
        return ""


def _cl_token(v, fallback="not-computed"):
    """One rendered token: non-empty, no $ leakage, bounded length."""
    s = _cl_safe_str(v).strip()
    if s == "" or s == "()" or s == "None":
        return fallback
    if "$" in s:
        # A $ means an unbound variable leaked; never render it as content.
        return fallback
    if len(s) > 48:
        s = s[:48]
    return s


def coupling_line_format(contact_count, dominant_surface, chain_state,
                         accord, band, support, residual, trajectory,
                         next_move, honesty):
    """The one rendered line. Verbatim engine vocabulary; fixed field order
    per design doc Contract 3. Honesty appears ONLY as
    name-action-not-verification (ratified render discipline: claim-completion
    and not-computed are never rendered)."""
    try:
        cc = _cl_token(contact_count, "0")
        ds = _cl_token(dominant_surface, "none")
        ch = _cl_token(chain_state)
        ac = _cl_token(accord)
        bd = _cl_token(band, "window-filling")
        # support is the one numeric field; render to 2 decimals, else token.
        try:
            sp = "%.2f" % float(_cl_safe_str(support))
        except Exception:
            sp = _cl_token(support)
        rs = _cl_token(residual)
        tj = _cl_token(trajectory)
        nm = _cl_token(next_move)
        line = ("COUPLING-STATE: contact " + cc + "/" + ds
                + " | chain " + ch
                + " | accord " + ac
                + " | band " + bd
                + " | support " + sp
                + " | residual " + rs
                + " | trajectory " + tj
                + " | next " + nm)
        hs = _cl_safe_str(honesty).strip()
        if hs == "name-action-not-verification":
            line = line + " | honesty name-action-not-verification"
        return line
    except Exception:
        # Absolute floor: the formatter never throws into the loop.
        return "COUPLING-STATE: window-filling"


_CL_HEAD_RE = re.compile(r"\(\s*([a-zA-Z\-]+)\s")
_CL_ARG_RE = re.compile(r"\(\s*([a-zA-Z\-]+)\s+\"([^\"]*)\"")

# Command heads by class, mirroring the pure-file table (RF3).
_CL_ACTION_HEADS = ("write-file", "append-file", "shell")
_CL_VERIFY_HEADS = ("read-file", "query", "metta", "episodes")


def coupling_command_signature(cmds_repr):
    """Stable signature: first non-pin head plus an 8-hex hash of the raw
    batch text. Empty or unparseable batches sign as none."""
    try:
        s = _cl_safe_str(cmds_repr)
        if s.strip() == "" or s.strip() == "()":
            return "none"
        heads = _CL_HEAD_RE.findall(s)
        head = "none"
        for h in heads:
            if h != "pin":
                head = h
                break
        digest = hashlib.md5(s.encode("utf-8", "replace")).hexdigest()[:8]
        return head + ":" + digest
    except Exception:
        return "none"


def _cl_targets(cmds_repr, heads_wanted):
    """First quoted argument for the first command whose head is in
    heads_wanted. Gate H target identity: kind is the head, id is an 8-hex
    hash of the quoted argument. Returns 'unknown' when no target is
    mechanically knowable (never fabricates)."""
    try:
        s = _cl_safe_str(cmds_repr)
        for head, arg in _CL_ARG_RE.findall(s):
            if head in heads_wanted:
                a = arg.strip()
                if a == "":
                    return "unknown"
                digest = hashlib.md5(a.encode("utf-8", "replace")).hexdigest()[:8]
                return head_kind(head) + ":" + digest
        return "unknown"
    except Exception:
        return "unknown"


def head_kind(head):
    """Target-kind per Gate H examples: file for file ops, file-query for
    reads, atom-query for metta/query, harness for shell."""
    if head in ("write-file", "append-file"):
        return "file"
    if head == "read-file":
        return "file"
    if head in ("query", "metta", "episodes"):
        return "atom-query"
    if head == "shell":
        return "harness"
    return "unknown"


def coupling_action_target(cmds_repr):
    """Target of the first action-class command, or 'unknown'.
    NOTE: shell targets hash the full command string; a shell action is
    therefore same-target-verifiable only by an identical shell read, which
    is conservative in the safe direction (Gate H: unknown or different
    target can never produce claim-completion)."""
    return _cl_targets(cmds_repr, _CL_ACTION_HEADS)


def coupling_verify_target(cmds_repr):
    """Target of the first verification-class command, or 'unknown'.
    Gate H comparison note: write-file and read-file on the same path hash
    identically (kind 'file', id hash of the path string), which is exactly
    the H1 same-target case; different paths differ (H4)."""
    return _cl_targets(cmds_repr, _CL_VERIFY_HEADS)
