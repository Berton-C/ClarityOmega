#!/usr/bin/env python3
from pathlib import Path
import subprocess, re, hashlib, sys

ROOT = Path.cwd()
SHARED = ROOT / 'shared_files'
OUT = Path('/tmp/cg-v3-investigation/second-failure/t57')
CONTAINER = 'clarity_omega'
POP = ROOT / 'soul/recent_action_populator.metta'
MAN = ROOT / 'lib_clarity_reasoning/lib_clarity_reasoning.metta'
SHARED.mkdir(exist_ok=True)
OUT.mkdir(parents=True, exist_ok=True)

CASES = {
    'A-ZERO': [],
    'B-RETAINED': [
        '(recent-action 100 responsive-send keep-a)',
        '(recent-action 101 exploration-query keep-b)',
        '(recent-action 102 pin-only keep-c)',
    ],
    'C-MIXED': [
        '(recent-action 88 responsive-send prune-a)',
        '(recent-action 89 exploration-query prune-b)',
        '(recent-action 100 responsive-send keep-a)',
        '(recent-action 101 exploration-query keep-b)',
        '(recent-action 102 pin-only keep-c)',
    ],
}
PRUNE_BEFORE = 92

def run(cmd):
    return subprocess.run(cmd, capture_output=True, text=True)

def probe(case, atoms, mode):
    adds = '\n'.join(f'!(add-atom &self {a})' for a in atoms)
    traversal = '''(let $old (superpose $to-remove)
      (if (== $old ())
          ()
          (remove-atom &self $old)))'''
    tested = traversal if mode == 'original' else f'(collapse {traversal})'
    return f'''!(import! &self (library lib_import))
!(import! &self /PeTTa/repos/omegaclaw/lib_omegaclaw.metta)
{adds}

(= (t57-snapshot)
   (collapse
     (match &self
       (recent-action $old-id $old-type $old-desc)
       (if (< $old-id {PRUNE_BEFORE})
           (recent-action $old-id $old-type $old-desc)
           ()))))

(= (t57-test)
   (let $to-remove (t57-snapshot)
     {tested}))

!(let $s (t57-snapshot)
   (println! (T57-SNAPSHOT {case} {mode} count (size-atom $s) values $s)))

!(let $v (collapse (t57-test))
   (println! (T57-TRAVERSAL {case} {mode} count (size-atom $v) values $v)))

!(let $r (collapse
           (match &self
             (recent-action $id $type $desc)
             (recent-action $id $type $desc)))
   (println! (T57-REMAINING {case} {mode} count (size-atom $r) values $r)))

!(println! (T57-END {case} {mode}))
'''

def extract(raw):
    return [x.strip() for x in raw.splitlines() if x.strip().startswith('(T57-')]

audit = []
ok = True
for p in (POP, MAN):
    exists = p.is_file()
    audit.append(f"{'PASS' if exists else 'FAIL'} exists: {p}")
    if exists:
        audit.append(f'  sha256: {hashlib.sha256(p.read_bytes()).hexdigest()}')
    ok &= exists

if POP.is_file():
    t = POP.read_text(errors='replace')
    checks = {
        'intentional empty sentinel present': '(if (< $old-id $prune-before)' in t and '())' in t,
        'snapshot uses collapse': '$to-remove' in t and '(collapse' in t,
        'snapshot re-expanded with superpose': '(superpose $to-remove)' in t,
        'TRACE-172 follows pruning region': 'TRACE-172-EXIT' in t,
    }
    for k, v in checks.items():
        audit.append(f"{'PASS' if v else 'FAIL'} {k}")
        ok &= v

if MAN.is_file():
    v = './soul/recent_action_populator' in MAN.read_text(errors='replace')
    audit.append(f"{'PASS' if v else 'FAIL'} manifest imports populator")
    ok &= v

if not ok:
    text = '=== T57 SOURCE AUDIT ===\n' + '\n'.join(audit) + '\nT57 ABORT: source audit failed.\n'
    (OUT / 't57-evidence.log').write_text(text)
    print(text)
    sys.exit(2)

ps = run(['docker', 'ps', '--filter', f'name=^{CONTAINER}$', '--format', '{{.Names}}'])
if CONTAINER not in ps.stdout.splitlines():
    print(f'T57 ABORT: container not running: {CONTAINER}')
    sys.exit(2)

rows = []
witnesses = []
for case, atoms in CASES.items():
    for mode in ('original', 'collapsed'):
        name = f"t57_{case.lower().replace('-', '_')}_{mode}.metta"
        host = SHARED / name
        host.write_text(probe(case, atoms, mode))
        p = run(['docker', 'exec', CONTAINER, 'sh', '-lc', f'cd /PeTTa && /PeTTa/run.sh /tmp/{name}'])
        raw = (p.stdout or '') + (p.stderr or '')
        (OUT / f'{name}.raw.log').write_text(raw)
        ws = extract(raw)
        witnesses += [f'--- {case}/{mode} ---'] + ws
        joined = '\n'.join(ws)
        def count(tag):
            m = re.search(rf'\({tag}\s+{case}\s+{mode}\s+count\s+(\d+)', joined)
            return int(m.group(1)) if m else None
        rows.append((case, mode, p.returncode, count('T57-SNAPSHOT'), count('T57-TRAVERSAL'), count('T57-REMAINING')))

report = [
    '=== T57 HYPOTHESIS ===',
    'The intentional () non-prune branch is safe only if the exact production',
    'pruning traversal remains single-valued. T57 compares the exact traversal',
    'with the same traversal wrapped in collapse. No production file is edited.',
    '',
    '=== SOURCE AUDIT ===',
    *audit,
    '',
    '=== CARDINALITY DIFFERENTIAL ===',
    f"{'CASE':14} {'MODE':10} {'RC':>3} {'SNAP':>5} {'TRAV':>5} {'REMAIN':>6}",
    '-' * 52,
]
for r in rows:
    report.append(f"{r[0]:14} {r[1]:10} {r[2]:>3} {str(r[3]):>5} {str(r[4]):>5} {str(r[5]):>6}")

report += ['', '=== DECISIVE WITNESSES ===', *witnesses, '', '=== VERDICT ===']
complete = all(r[2] == 0 and None not in r[3:] for r in rows)
d = {(r[0], r[1]): r for r in rows}
if not complete:
    report += ['INCOMPLETE: missing decisive witness. Do not infer a fix.']
else:
    orig_mult = d[('B-RETAINED', 'original')][4] > 1 or d[('C-MIXED', 'original')][4] > 1
    coll_one = d[('B-RETAINED', 'collapsed')][4] == 1 and d[('C-MIXED', 'collapsed')][4] == 1
    if orig_mult and coll_one:
        report += [
            'SUPPORTED: the exact production traversal leaks snapshot cardinality;',
            'changing only the traversal boundary to collapse restores one continuation.',
            '',
            'Interpretation: the () branch may remain intentional as a filter sentinel.',
            'The defect is not its existence by itself; the defect is retaining each',
            'per-match result and re-expanding it without reconverging to one result.',
        ]
    elif not orig_mult:
        report += [
            'NOT SUPPORTED: the exact traversal stayed single-valued in controlled fixtures.',
            'Do not patch production from source inspection alone.',
        ]
    else:
        report += [
            'MIXED: original multiplied, but collapse did not consistently restore one result.',
            'The defect is broader than a single missing collapse boundary.',
        ]

report += [
    '',
    '=== DEFERRED SECONDARY ISSUE REGISTER ===',
    'RA-SECONDARY-01: duplicate recent-action atoms sharing a cycle ID may make',
    'recent_action_retriever choose arbitrarily through car-atom. Verify and repair',
    'after the primary loop multiplier is resolved.',
    '',
    f"Primary log: {OUT / 't57-evidence.log'}",
    '=== T57 COMPLETE ===',
]

text = '\n'.join(report) + '\n'
(OUT / 't57-evidence.log').write_text(text)
print(text)
sys.exit(0 if complete else 1)
