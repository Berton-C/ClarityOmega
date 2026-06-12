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
