# soul/soul_governance.py
# Governance hands (ADR-008): pure data extraction, no judgment.
# Imported by soul/output_verdict.metta via PeTTa's importer_helper
# (metta.pl: sys.path.append(dir) + __import__), the same mechanism
# that makes helper.py py-callable. Lives in soul/ (bind-mounted:
# no rebuild needed; container restart only).


def path_scope(p):
    """Scope score for a path string: 1 soul-dir, 2 own-repo, 4 system.
    str(p) coerces whatever form janus passes."""
    s = str(p)
    if s.startswith('/PeTTa/repos/omegaclaw/soul/'):
        return 1
    if s.startswith('/PeTTa/repos/omegaclaw/'):
        return 2
    return 4


def journal_append(kind, content):
    """One line per governance event (PAUSE/FLAG) to the governance
    journal. Hands only: timestamp + kind + truncated content."""
    import datetime as _dt
    line = "{} {} {}\n".format(
        _dt.datetime.utcnow().isoformat(), str(kind), str(content)[:2000])
    with open('/PeTTa/repos/omegaclaw/soul/governance_journal.log', 'a') as f:
        f.write(line)
    return True


def repr_kind(r):
    """Arg-kind detector on the REPR (repr is total over unbound vars
    and always marshals; raw marshalling of unbound-carrying exprs
    kills py_call, F30). repr of a STRING carries a leading quote
    (probe9 P1); an expression's does not (P1b). Returns INT (1 =
    string, 0 = other): MeTTa-side comparison is (== n 1), the
    int-equality pattern proven throughout rank logic, avoiding the
    unverified python-bool-into-if marshalling class (ledger F35)."""
    return 1 if (isinstance(r, str) and r.lstrip().startswith('"')) else 0

def pause_note_compose(verdict_repr):
    """Repair 3: extract the SOUL-NOTE tail from an output verdict repr.
    Returns the note text (her own words) or the verdict head as fallback."""
    v = str(verdict_repr).strip()
    if v.startswith('"') and v.endswith('"'):
        v = v[1:-1]
    idx = v.find("SOUL-NOTE: ")
    note = v[idx + len("SOUL-NOTE: "):].strip() if idx >= 0 else v[:200]
    return note[:600]


def contains_token(haystack, needle):
    """Repair 3 (F-R3-7): truthful substring scan for string-contains.
    Bridge pattern proven by repr_kind: string in, INT out, consumed
    as (== n 1). Pure plumbing; routing policy stays in MeTTa."""
    return 1 if str(needle) in str(haystack) else 0


def pause_context(note_repr):
    """Repair 3: prompt prefix surfacing the pause-record. Empty when clear."""
    n = str(note_repr).strip()
    if n.startswith('"') and n.endswith('"'):
        n = n[1:-1]
    n = n.strip()
    if not n:
        return ""
    return ("PREVIOUS-BATCH-PAUSED: your soul paused your previous command batch "
            "and it did not execute. The concern, in your own words: " + n +
            " Address or re-emit knowingly. ")

# ============================================================================
# Surface C SEAM 1: gate_decision_record
# Destination: APPEND to /PeTTa/repos/omegaclaw/soul_governance.py (the live
#   module reachable through the omegaclaw boot chain).
# Contract (matches soul_mutation_lock.metta call sites, 6 positional args):
#   gate_decision_record(gate, phase, op_repr, head_repr, fp, sender) -> 1
# Recorded line carries 7 fields: timestamp gate phase op head fp sender.
#   - timestamp generated here (mechanical, hands-only).
#   - sender recorded for AUDIT only; Surface D learning MUST EXCLUDE it
#     (sender-agnostic; sender-aware would train authority-theater).
# Append-only journal; consumed by nothing yet, written from day one.
# Mechanical journaling (no judgment) -> squarely within the Python
#   hands-only boundary; compliant.
# ============================================================================

def gate_decision_record(gate, phase, op_repr, head_repr, fp, sender):
    import datetime
    line = "%s %s %s op=%s head=%s fp=%s sender=%s\n" % (
        datetime.datetime.now().isoformat(),
        str(gate), str(phase),
        str(op_repr), str(head_repr), str(fp), str(sender))
    try:
        with open("/PeTTa/repos/omegaclaw/soul/governance_journal.log", "a") as f:
            f.write(line)
    except Exception:
        pass
    return 1

# ============================================================================
# Surface C: complete soul_governance.py additions (append all three).
# Destination: APPEND to /PeTTa/repos/omegaclaw/soul_governance.py
#
# These close the ENTIRE soul_governance dependency surface that Surface C
# and its inlined output_verdict extraction chain invoke. Verified against
# the live container via env_probe13/14: contains_token was already live;
# these three were absent (gate_decision_record and is_string proven absent
# by AttributeError; approval_scan in the same un-applied Repair-3/output_verdict
# Python half, added here so the transition path has no missing dependency).
#
# All three are mechanical (journaling, a type predicate, a token parse with a
# fixed precedence rule). No model judgment. Hands-only, compliant.
# approval_scan carries one small precedence rule (DENY wins) -- the single
# soft spot flagged for review; reproduced verbatim from Clarity's SEAM-3
# design so Surface E can reuse it unchanged.
# ============================================================================

def is_string(x):
    # output_verdict norm-metta-arg dependency: distinguishes a string arg
    # (needs sread) from an already-structured arg (passes through).
    # Consumed as a MeTTa truthy: (if (py-call (soul_governance.is_string $a)) ...).
    return isinstance(x, str)


def gate_decision_record(gate, phase, op_repr, head_repr, fp, sender):
    # SEAM 1: append-only learning record (Surface D training data).
    # 7 fields: timestamp gate phase op head fp sender. timestamp generated
    # here. sender recorded for AUDIT only -- D's learning MUST EXCLUDE it
    # (sender-agnostic; sender-aware would train authority-theater).
    import datetime
    line = "%s %s %s op=%s head=%s fp=%s sender=%s\n" % (
        datetime.datetime.now().isoformat(),
        str(gate), str(phase),
        str(op_repr), str(head_repr), str(fp), str(sender))
    try:
        with open("/PeTTa/repos/omegaclaw/soul/governance_journal.log", "a") as f:
            f.write(line)
    except Exception:
        pass
    return 1


def approval_scan(msg, sender, lock_fp, authorized):
    # SEAM 3: sender-bound approval/denial parse. Returns INT 2/1/0
    # (APPROVE/DENY/NONE; consumed via == n k, the repr_kind convention,
    # never a Python bool into a MeTTa if). DENY wins if both tokens present.
    # APPROVE needs an authorized sender AND the matching fingerprint. DENY
    # also needs an authorized sender (denial is a governance act). Generic:
    # Surface E reuses this verbatim, changing only the token strings.
    m = str(msg)
    s = str(sender).strip().rstrip(":")
    auth = s in [a.strip().rstrip(":") for a in str(authorized).split(",") if a.strip()]
    if not auth:
        return 0
    if "SOUL-MUTATION-DENIED" in m:
        return 1
    if "SOUL-MUTATION-APPROVED" in m and str(lock_fp).strip() in m:
        return 2
    return 0

# Surface C PENDING-entry: the mutation_fingerprint helper (SEAM 3 plumbing).
# APPEND to /PeTTa/repos/omegaclaw/soul_governance.py.
#
# Spec basis:
#   Integration Map sec 2: unlocked --[soul mutation detected]--> (locked op head fp)  PENDING
#   Integration Map SEAM 3: "approval_scan + &authorized_approvers + mutation_fingerprint".
#   The fingerprint is the token the human must echo to approve; approval_scan
#   matches the echoed token against &last_gate_fingerprint. It must therefore be
#   DETERMINISTIC over (op, head): the same pending mutation always yields the same fp.
#
# Faculty split (ADR-008): this is HANDS (mechanical string->digest), not judgment.
# MeTTa never touches strings; Python computes the digest; MeTTa decides policy.

import hashlib


def mutation_fingerprint(op_repr, head_repr):
    """SEAM 3: deterministic 8-hex-char fingerprint of a soul mutation's op+head.

    Args are repr-rendered MeTTa atoms (e.g. "add-atom", "soul-value"), the same
    op/head the lock stores and approval echoes. Deterministic so the fp the human
    echoes in 'SOUL-MUTATION-APPROVED <fp>' matches &last_gate_fingerprint.
    sha256[:8] over a delimited join; the delimiter prevents ("ab","c") and
    ("a","bc") from colliding."""
    payload = str(op_repr) + "\x1f" + str(head_repr)
    return hashlib.sha256(payload.encode("utf-8")).hexdigest()[:8]
