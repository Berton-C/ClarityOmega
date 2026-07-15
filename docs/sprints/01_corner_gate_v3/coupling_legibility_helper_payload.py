# ============================================================
# coupling_legibility_helper_payload.py
# Draft A.3 payload 3 of 3. Design canon: corner_gate_v3_adapter_design.md.
# Status: DRAFT A.3 FOR BERTON RATIFICATION.
# History: A.1 resolved helper items 1-5: H4 fixture in the delivery verification,
# sha256 compact identity hashes, pin-only signatures return none, shell
# excluded from target extraction (conservative, no false accusations),
# widened head regex.
#
# These functions are appended to src/helper.py by the monolith (Phase 3).
# Python is only ever the hands for MeTTa and never does reasoning
# (ratified). Three jobs only: line formatting, command signature hashing,
# target extraction. Content of sends and pins is NEVER read; only command
# heads and first quoted arguments (paths, patterns) are touched.
#
# RF2 (accepted): four functions, hands-only string plumbing.
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
        return str(v)
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
                         next_move, honesty, contact_audit="hidden"):
    """The one rendered line. Verbatim engine vocabulary; fixed field order
    per design doc Contract 3. accord is the TASK accord. contact_audit is
    the divergence-gated contact accord: rendered only when MeTTa passed a
    real symbol (the sentinel hidden means no render). Honesty appears ONLY
    as name-action-not-verification (ratified render discipline)."""
    try:
        cc = _cl_token(contact_count, "0")
        ds = _cl_token(dominant_surface, "none")
        ch = _cl_token(chain_state)
        ac = _cl_token(accord)
        bd = _cl_token(band, "window-filling")
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
        ca = _cl_safe_str(contact_audit).strip()
        if ca not in ("", "hidden", "None", "()", "not-computed", "window-filling"):
            line = line + " | contact-audit " + _cl_token(ca)
        hs = _cl_safe_str(honesty).strip()
        if hs == "name-action-not-verification":
            line = line + " | honesty name-action-not-verification"
        return line
    except Exception:
        # Absolute floor: the formatter never throws into the loop.
        return "COUPLING-STATE: window-filling"


# Head tokens may include digits, underscores, hyphens, and trailing marks.
_CL_HEAD_RE = re.compile(r"\(\s*([A-Za-z0-9_\-]+[!?]?)\s")
_CL_ARG_RE = re.compile(r"\(\s*([A-Za-z0-9_\-]+[!?]?)\s+\"([^\"]*)\"")

# Gate H target extraction heads. Shell is deliberately EXCLUDED from action
# target extraction: a harness target has no verification-class counterpart
# in v1, so shell actions yield target unknown, which reduces honesty to
# not-computed (conservative in the safe direction: shell can never produce
# a false claim-completion OR a false accusation).
_CL_ACTION_TARGET_HEADS = ("write-file", "append-file")
_CL_VERIFY_TARGET_HEADS = ("read-file", "query", "metta", "episodes")


def _cl_hash8(s):
    """Compact non-security identity hash (sha256 first 8 hex)."""
    return hashlib.sha256(s.encode("utf-8", "replace")).hexdigest()[:8]


def coupling_command_signature(cmds_repr):
    """Stable signature: first non-pin head plus an 8-hex sha256 of the raw
    batch text. Empty, unparseable, and PIN-ONLY batches sign as none: pins
    are narration, and narration must not become command lineage (ratified;
    pin loops are caught by the no-contact path, not signature repetition)."""
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
        if head == "none":
            return "none"
        return head + ":" + _cl_hash8(s)
    except Exception:
        return "none"


def head_kind(head):
    """Target-kind per Gate H: file for file ops, atom-query for reads."""
    if head in ("write-file", "append-file", "read-file"):
        return "file"
    if head in ("query", "metta", "episodes"):
        return "atom-query"
    return "unknown"


def _cl_targets(cmds_repr, heads_wanted):
    """First quoted argument for the first command whose head is in
    heads_wanted. Target identity: kind plus 8-hex sha256 of the quoted
    argument. Returns 'unknown' when no target is mechanically knowable
    (never fabricates)."""
    try:
        s = _cl_safe_str(cmds_repr)
        for head, arg in _CL_ARG_RE.findall(s):
            if head in heads_wanted:
                a = arg.strip()
                if a == "":
                    return "unknown"
                return head_kind(head) + ":" + _cl_hash8(a)
        return "unknown"
    except Exception:
        return "unknown"


def coupling_action_target(cmds_repr):
    """Target of the first file-writing action command, or 'unknown'."""
    return _cl_targets(cmds_repr, _CL_ACTION_TARGET_HEADS)


def coupling_verify_target(cmds_repr):
    """Target of the first verification-class command, or 'unknown'.
    Gate H comparison: write-file and read-file on the same path hash to the
    same kind 'file' plus path hash, the H1 same-target case; different
    paths differ (H4); a verification against a DIFFERENT target can never
    equal the action target, so it can never produce claim-completion."""
    return _cl_targets(cmds_repr, _CL_VERIFY_TARGET_HEADS)
