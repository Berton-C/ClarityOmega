#!/usr/bin/env python3
from __future__ import annotations
import argparse, hashlib, re, subprocess
from pathlib import Path

DEFAULT_CONTAINER='clarity_omega'
DEFAULT_REPO=Path.cwd()
DEFAULT_SHARED=Path('shared_files')
DEFAULT_OUT=Path('/tmp/cg-v3-investigation/second-failure/t58')
TIMEOUT=180
ANSI_RE=re.compile(r'\x1b\[[0-9;]*m')
ERROR_RE=re.compile(r'Unknown procedure|Domain error|not_less_than_zero|METTA_ARGUMENT_PARSE_ERROR|ERROR:|Traceback|Exception')
PRUNE_BEFORE=92

CASES=[
 ('ZERO',[], 'No existing atoms.'),
 ('RETAINED',[
  '(t58-action 100 responsive-send keep-a)',
  '(t58-action 101 exploration-query keep-b)',
  '(t58-action 102 pin-only keep-c)'],
  'Three atoms intentionally map to ().'),
 ('MIXED',[
  '(t58-action 88 responsive-send prune-a)',
  '(t58-action 89 exploration-query prune-b)',
  '(t58-action 100 responsive-send keep-a)',
  '(t58-action 101 exploration-query keep-b)',
  '(t58-action 102 pin-only keep-c)'],
  'Two prunable plus three retained atoms.')]

MODES=[
 ('ORIGINAL','(let $old (superpose $to-remove) (if (== $old ()) () (remove-atom &self $old)))','Exact production-shaped traversal.'),
 ('COLLAPSED','(collapse (let $old (superpose $to-remove) (if (== $old ()) () (remove-atom &self $old))))','Only difference: one outer collapse.')]

def sha256(p): return hashlib.sha256(p.read_bytes()).hexdigest()
def clean(s): return ANSI_RE.sub('',s or '')
def run(cmd,timeout=TIMEOUT): return subprocess.run(cmd,capture_output=True,text=True,timeout=timeout)

def source_audit(repo):
    pop=repo/'soul/recent_action_populator.metta'
    man=repo/'lib_clarity_reasoning/lib_clarity_reasoning.metta'
    rows=['=== T58 SOURCE AND CLOSURE AUDIT ===',f'repo: {repo}']
    ok=True
    for p in (pop,man):
        ex=p.is_file(); rows.append(f"{'PASS' if ex else 'FAIL'} file: {p.relative_to(repo)}")
        if ex: rows.append(f'      sha256: {sha256(p)}')
        ok &= ex
    if pop.is_file():
        t=pop.read_text(errors='replace')
        checks={
          'intentional retained branch returns ()':'(if (< $old-id $prune-before)' in t and '())' in t,
          'snapshot uses collapse':'$to-remove' in t and '(collapse' in t,
          'snapshot re-expanded by superpose':'(superpose $to-remove)' in t,
          'pruning uses remove-atom':'(remove-atom &self $old)' in t,
          'TRACE-172 follows pruning':'TRACE-172-EXIT' in t}
        for label,passed in checks.items():
            rows.append(f"{'PASS' if passed else 'FAIL'} populator: {label}"); ok &= passed
    if man.is_file():
        passed='./soul/recent_action_populator' in man.read_text(errors='replace')
        rows.append(f"{'PASS' if passed else 'FAIL'} manifest: imports recent_action_populator"); ok &= passed
    rows += ['', 'Execution scaffold:', '  identical to T54: docker exec -> cd /PeTTa -> /PeTTa/run.sh /tmp/<probe>', '  identical local production closure import.', '']
    return ok,'\n'.join(rows)

def probe_text(case,atoms,mode,traversal):
    lines=[
      '!(import! &self (library lib_import))',
      '!(import! &self /PeTTa/repos/omegaclaw/lib_omegaclaw.metta)',
      '',f'!(println! (T58-BEGIN {case} {mode}))','']
    lines += [f'!(add-atom &self {a})' for a in atoms]
    lines += [
      '',
      '(= (t58-snapshot)',
      '   (collapse',
      '     (match &self',
      '       (t58-action $old-id $old-type $old-desc)',
      f'       (if (< $old-id {PRUNE_BEFORE})',
      '           (t58-action $old-id $old-type $old-desc)',
      '           ()))))',
      '',
      '(= (t58-traversal)',
      '   (let $to-remove (t58-snapshot)',
      f'     {traversal}))',
      '',
      f'!(let $snapshot (t58-snapshot) (println! (T58-SNAPSHOT {case} {mode} count (size-atom $snapshot) values $snapshot)))',
      f'!(let $outputs (collapse (t58-traversal)) (println! (T58-TRAVERSAL {case} {mode} count (size-atom $outputs) values $outputs)))',
      f'!(let $remaining (collapse (match &self (t58-action $id $type $desc) (t58-action $id $type $desc))) (println! (T58-REMAINING {case} {mode} count (size-atom $remaining) values $remaining)))',
      f'!(println! (T58-END {case} {mode}))','']
    return '\n'.join(lines)

def execute_case(container,shared,out,case,atoms,mode,traversal):
    safe=f'{case.lower()}_{mode.lower()}'
    hp=shared/f't58_{safe}.metta'; hp.write_text(probe_text(case,atoms,mode,traversal))
    p=run(['docker','exec',container,'sh','-lc',f'cd /PeTTa && /PeTTa/run.sh /tmp/{hp.name}'])
    raw=clean((p.stdout or '')+(p.stderr or '')); rp=out/f'{safe}.raw.log'; rp.write_text(raw)
    ws=[ln.strip() for ln in raw.splitlines() if ln.strip().startswith('(T58-')]
    joined='\n'.join(ws)
    def cnt(marker):
        m=re.search(rf'\(T58-{marker}\s+{re.escape(case)}\s+{re.escape(mode)}\s+count\s+([0-9]+)\b',joined)
        return int(m.group(1)) if m else None
    snap,trav,remain=cnt('SNAPSHOT'),cnt('TRAVERSAL'),cnt('REMAINING')
    required=[f'(T58-{m} {case} {mode}' for m in ('BEGIN','SNAPSHOT','TRAVERSAL','REMAINING','END')]
    missing=[m for m in required if not any(w.startswith(m) for w in ws)]
    errors=[ln.strip() for ln in raw.splitlines() if ERROR_RE.search(ln)]
    valid=p.returncode==0 and not missing and None not in (snap,trav,remain)
    return dict(case=case,mode=mode,rc=p.returncode,snapshot=snap,traversal=trav,remaining=remain,valid=valid,missing=missing,witnesses=ws,errors=errors[-30:] if not valid else [],probe=str(hp),raw=str(rp),raw_tail='\n'.join(raw.splitlines()[-120:]) if not valid else '')

def analyze(results):
    rows=['=== T58 CARDINALITY DIFFERENTIAL ===','',f"{'CASE':10} {'MODE':10} {'RC':>3} {'SNAP':>6} {'TRAV':>6} {'REMAIN':>7} {'VALID':>6}",'-'*64]
    for r in results:
        rows.append(f"{r['case']:10} {r['mode']:10} {r['rc']:>3} {str(r['snapshot']):>6} {str(r['traversal']):>6} {str(r['remaining']):>7} {('YES' if r['valid'] else 'NO'):>6}")
    rows += ['', '=== DECISIVE RUNTIME WITNESSES ===']
    for r in results:
        rows.append(f"\n--- {r['case']} / {r['mode']} ---")
        rows += r['witnesses'] or ['NO T58 RUNTIME WITNESSES']
        if not r['valid']:
            rows += [f"MISSING: {r['missing']}"]
            if r['errors']: rows += ['RUNTIME ERRORS:']+r['errors']
            rows += [f"RAW LOG: {r['raw']}",'RAW TAIL:',r['raw_tail'] or '<empty>']
    rows += ['', '=== T58 VERDICT ===']
    invalid=[r for r in results if not r['valid']]
    if invalid:
        rows += ['INVALID — at least one case missed mandatory runtime markers.','No pruning conclusion is authorized.','Invalid cases: '+', '.join(f"{r['case']}/{r['mode']}" for r in invalid)]
        return '\n'.join(rows)+'\n'
    d={(r['case'],r['mode']):r for r in results}
    baseline=d[('ZERO','ORIGINAL')]['traversal']==1 and d[('ZERO','COLLAPSED')]['traversal']==1
    orig=d[('RETAINED','ORIGINAL')]['traversal']>1 or d[('MIXED','ORIGINAL')]['traversal']>1
    coll=d[('RETAINED','COLLAPSED')]['traversal']==1 and d[('MIXED','COLLAPSED')]['traversal']==1
    if baseline and orig and coll:
        rows += ['SUPPORTED.','The production-shaped traversal leaks snapshot cardinality.','One outer collapse restores exactly one continuation.','The () branch may remain intentional; the demonstrated defect is unreconverged superpose output.','Repair constraint: preserve two-pass snapshot-before-mutation semantics.']
    elif not orig:
        rows += ['NOT SUPPORTED.','The production-shaped traversal remained single-valued.','Do not patch recent_action_populator from source inspection alone.']
    elif not coll:
        rows += ['MIXED.','Original multiplied, but outer collapse did not reliably restore one result.']
    else:
        rows += ['ANOMALOUS BASELINE.','ZERO fixture was not single-valued. Inspect witnesses before changing production.']
    return '\n'.join(rows)+'\n'

def main():
    ap=argparse.ArgumentParser(); ap.add_argument('--container',default=DEFAULT_CONTAINER); ap.add_argument('--repo',type=Path,default=DEFAULT_REPO); ap.add_argument('--shared',type=Path,default=DEFAULT_SHARED); ap.add_argument('--out',type=Path,default=DEFAULT_OUT); args=ap.parse_args()
    repo=args.repo.resolve(); shared=(repo/args.shared).resolve() if not args.shared.is_absolute() else args.shared.resolve(); out=args.out; out.mkdir(parents=True,exist_ok=True); shared.mkdir(parents=True,exist_ok=True)
    log=out/'t58-evidence.log'; ok,audit=source_audit(repo)
    header=['=== T58 HYPOTHESIS ===','The current pruning traversal returns one continuation per snapshot member.','Adding only one outer collapse restores exactly one continuation while','preserving the intentional () branch and snapshot-before-mutation design.','','Single variable: traversal result cardinality.','Runner: proven T54 execution scaffold.','Production files edited: none.','',audit]
    if not ok:
        text='\n'.join(header)+'\nT58 ABORT: source audit failed. Nothing executed.\n'; log.write_text(text); print(text,end=''); return 2
    ps=run(['docker','ps','--filter',f'name=^{args.container}$','--format','{{.Names}}'])
    if args.container not in ps.stdout.splitlines():
        text='\n'.join(header)+f'\nT58 ABORT: container not running: {args.container}\n'; log.write_text(text); print(text,end=''); return 2
    results=[]
    for case,atoms,cp in CASES:
        for mode,traversal,mp in MODES:
            print(f'T58 running {case}/{mode}: {cp} {mp}')
            results.append(execute_case(args.container,shared,out,case,atoms,mode,traversal))
    report='\n'.join(header)+'\n'+analyze(results)
    report += '\n=== DEFERRED ISSUE REGISTER ===\nRA-SECONDARY-01 remains open: duplicate cycle IDs may make the retriever\nchoose arbitrarily through car-atom. Address after the primary multiplier.\n'
    report += f'\n=== T58 ARTIFACTS ===\nONE PRIMARY LOG: {log}\nGenerated probes:\n'
    for r in results: report += f"  {r['probe']}\n"
    report += 'Raw logs retained only for forensic fallback:\n'
    for r in results: report += f"  {r['raw']}\n"
    report += '\n=== T58 COMPLETE ===\n'; log.write_text(report); print('\n'+report,end='')
    return 0 if all(r['valid'] for r in results) else 1

if __name__=='__main__':
    raise SystemExit(main())
