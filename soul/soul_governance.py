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
