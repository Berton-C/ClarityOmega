# classify_command_risk -- implementation sketch
# For soul_precision_proposal -- ClarityClaw draft 2026-04-27
# Would live in helper.py or new module

OP_RISK_MAP = {
    'read-only': {'ls','cat','head','tail','wc','find','grep','echo','pwd','whoami'},
    'create-modify': {'touch','mkdir','cp','mv','sed','tee'},
    'destroy': {'rm','rmdir','kill','pkill'},
    'network': {'curl','wget','ssh','scp','ping','nc'},
    'execute': {'python','python3','bash','sh','node','chmod'},
}

SCOPE_PREFIXES = [
    ('own-soul-dir', '/PeTTa/repos/omegaclaw/soul/'),
    ('own-repo', '/PeTTa/repos/omegaclaw/'),
    ('shared-workspace', '/PeTTa/repos/'),
    ('system', '/'),
]

def classify_op(token):
    for level, cmds in OP_RISK_MAP.items():
        if token in cmds:
            return level
    return 'unknown-assume-high'

def classify_scope(tokens):
    paths = [t for t in tokens if t.startswith('/')]
    if not paths:
        return 'own-repo'
    for p in paths:
        for level, prefix in SCOPE_PREFIXES:
            if p.startswith(prefix):
                return level
    return 'system'

def composite(op, scope, actor):
    if op in ('destroy','network','execute') and scope == 'system':
        return 'critical'
    if op == 'read-only' and scope in ('own-soul-dir','own-repo'):
        return 'minimal'
    if actor == 'developer-established':
        return 'moderate'
    return 'high'
