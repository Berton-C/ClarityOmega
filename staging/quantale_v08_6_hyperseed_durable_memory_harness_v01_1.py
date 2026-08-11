#!/usr/bin/env python3
"""
v08.6 Hyperseed Durable Memory Harness v01

This is the actual v08.6 durable-memory harness after the fresh Hyperseed pass.
It tests pure semantic reductions and, when requested, inspects storage and
crosses a restart boundary. It distinguishes declaration, runtime residue,
persisted trace, restored candidate, and durable growth norm.
"""
from __future__ import annotations
import argparse, datetime as dt, hashlib, json, os, re, shlex, sqlite3, subprocess, time
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

HARNESS_VERSION = "v08.6-hyperseed-durable-memory-v01.1"
REQUIRED_TOKENS = [
    "q-v08-6-version", "fresh-hyperseed-durable-memory-pass",
    "q-persistence-class?", "q-learned-growth-source-status?", "q-growth-commit-status?",
    "q-growth-restored-status?", "q-growth-claim-durability?", "q-living-pattern-status?",
    "q-growth-reinforcement-status?", "q-growth-decay-status?", "q-growth-calcification-risk?",
    "q-growth-continuity-status?", "q-growth-structural-persistence?", "q-growth-temporal-carry-status?",
    "q-question-persistence-status?", "q-growth-predictive-status?", "q-growth-navigation-improvement?",
    "q-growth-realness-status?", "q-growth-routing-update-status?", "q-growth-overforcing-risk?",
    "q-growth-norm-status?", "q-growth-shared-memory-status?", "q-growth-intersubjective-check?",
    "q-growth-negative-control-status?", "q-growth-restart-test-status?",
]
LAW_TOKENS = [
    "no-trace-no-growth-claim", "no-restore-evidence-no-durable-growth",
    "no-revalidation-no-new-norm", "no-revision-path-no-safe-evolution",
    "source-declaration-is-not-learned-growth", "stale-residue-is-not-durable-growth",
    "repetition-is-not-reinforcement-without-independent-support",
    "continuity-is-carried-structure-not-identity-assertion",
    "durable-norm-is-gentle-reweighting-not-hard-sovereign-override",
]
TARGETS = [
    "persistence-class-reduces", "learned-growth-source-reduces", "commit-restore-revalidation-reduces",
    "living-pattern-trace-reduces", "reinforcement-decay-reduces", "structural-continuity-reduces",
    "temporal-question-persistence-reduces", "predictive-navigation-realness-reduces",
    "minimal-forcing-routing-update-reduces", "shared-memory-hooks-reduce", "negative-controls-block",
    "restart-persistence-harness-required",
]

def sha256_bytes(b: bytes) -> str: return hashlib.sha256(b).hexdigest()
def sha256_file(path: Path) -> Optional[str]:
    try: return sha256_bytes(path.read_bytes())
    except Exception: return None
def now_stamp() -> str: return dt.datetime.now().strftime("%Y%m%d_%H%M%S")
def strip_comments(text: str) -> str:
    out=[]
    for line in text.splitlines(): out.append(line.split(";;",1)[0] if ";;" in line else line)
    return "\n".join(out)
def paren_balance(text: str) -> int: return text.count("(") - text.count(")")
def safe_read_text(path: Path, limit: Optional[int]=None) -> str:
    try:
        data = path.read_text(errors="replace")
        return data if limit is None else data[:limit]
    except Exception: return ""
def run_cmd(cmd: List[str], input_text: Optional[str]=None, timeout:int=180) -> Tuple[int,str,str]:
    p = subprocess.run(cmd, input=input_text, text=True, capture_output=True, timeout=timeout)
    return p.returncode, p.stdout, p.stderr

@dataclass
class Check:
    tier: str; name: str; status: str; details: str=""; data: Any=None
@dataclass
class Recorder:
    out_dir: Path; meta: Dict[str,Any]; checks: List[Check]=field(default_factory=list)
    @property
    def log_dir(self) -> Path: return self.out_dir
    def add(self,tier,name,status,details="",data=None): self.checks.append(Check(tier,name,status,details,data))
    def summary(self):
        out={"PASS":0,"FAIL":0,"HOLD":0,"INSPECT":0,"SKIP":0}
        for c in self.checks: out[c.status]=out.get(c.status,0)+1
        return out
    def write(self):
        self.out_dir.mkdir(parents=True, exist_ok=True); stamp=now_stamp()
        payload={"meta":self.meta,"summary":self.summary(),"checks":[c.__dict__ for c in self.checks]}
        jp=self.out_dir/f"v08_6_hyperseed_durable_memory_trace_{stamp}.json"
        mp=self.out_dir/f"v08_6_hyperseed_durable_memory_trace_{stamp}.md"
        jp.write_text(json.dumps(payload, indent=2, sort_keys=True))
        lines=[f"# v08.6 Hyperseed Durable Memory Trace {stamp}","",f"Harness: `{HARNESS_VERSION}`","","## Summary","","```text",json.dumps(self.summary(),indent=2,sort_keys=True),"```", "", "## Checks", ""]
        for c in self.checks:
            lines.append(f"### [{c.tier}] {c.status}: {c.name}")
            if c.details: lines += ["", c.details]
            if c.data is not None:
                lines += ["", "```json", json.dumps(c.data, indent=2, sort_keys=True)[:10000], "```"]
            lines.append("")
        mp.write_text("\n".join(lines)); return mp,jp

def file_info(path: Path) -> Dict[str,Any]:
    d={"path":str(path),"exists":path.exists()}
    if path.exists():
        st=path.stat(); d.update({"is_file":path.is_file(),"is_dir":path.is_dir(),"size":st.st_size,"mtime_iso":dt.datetime.fromtimestamp(st.st_mtime).isoformat()})
        if path.is_file(): d["sha256"]=sha256_file(path)
    return d

def static_checks(engine:Path, ladder:Path, rec:Recorder):
    for label,path in [("engine",engine),("ladder",ladder)]:
        if path.exists(): rec.add("Tier S0", f"file present: {label}", "PASS", f"path={path} size={path.stat().st_size} sha256={sha256_file(path)}")
        else: rec.add("Tier S0", f"file present: {label}", "FAIL", f"missing path={path}")
    if not engine.exists() or not ladder.exists(): return
    et=engine.read_text(errors="replace"); lt=ladder.read_text(errors="replace")
    rec.add("Tier S1", "engine raw paren balance", "PASS" if paren_balance(et)==0 else "FAIL", f"balance={paren_balance(et)}")
    rec.add("Tier S1", "engine comment-stripped paren balance", "PASS" if paren_balance(strip_comments(et))==0 else "FAIL", f"balance={paren_balance(strip_comments(et))}")
    rec.add("Tier S1", "ladder comment-stripped paren balance", "PASS" if paren_balance(strip_comments(lt))==0 else "FAIL", f"balance={paren_balance(strip_comments(lt))}")
    missing=[t for t in REQUIRED_TOKENS if t not in et]
    rec.add("Tier S2", "all v08.6 durable-memory primitive families present", "PASS" if not missing else "FAIL", f"missing={missing}")
    missing_law=[t for t in LAW_TOKENS if t not in et]
    rec.add("Tier S2", "all v08.6 durable-memory laws present", "PASS" if not missing_law else "FAIL", f"missing={missing_law}")
    missing_targets=[t for t in TARGETS if t not in et or t not in lt]
    rec.add("Tier S2", "engine and ladder expose all v08.6 harness targets", "PASS" if not missing_targets else "FAIL", f"missing={missing_targets}")
    section = et.split("54. v08.6",1)[1] if "54. v08.6" in et else et
    writer_terms=["(add-atom", "(remove-atom", "(set-atom!"]
    found=[w for w in writer_terms if w in section]
    rec.add("Tier S3", "v08.6 engine section remains pure", "PASS" if not found else "FAIL", f"writer_terms_found={found}")
    for bad in ["durable-growth-norm)", "blocked-source-declaration-masquerade", "blocked-overforced-norm", "blocked-fixed-residue"]:
        rec.add("Tier S3", f"critical token present: {bad}", "PASS" if bad in et else "FAIL", "")

def engine_plus_expression(engine_text:str, expression:str)->str:
    return engine_text.rstrip()+"\n\n"+expression.strip()+"\n"
def docker_write(container,temp_path,body):
    cmd=["docker","exec","-i",container,"sh","-c",f"cat > {shlex.quote(temp_path)}"]
    rc,out,err=run_cmd(cmd,body); return rc,out,err," ".join(shlex.quote(x) for x in cmd)
def docker_run_metta(container,temp_path):
    shell=f"cd /PeTTa && ./run.sh {shlex.quote(temp_path)} 2>&1"; cmd=["docker","exec",container,"sh","-c",shell]
    rc,out,err=run_cmd(cmd,timeout=240); return rc,out,err," ".join(shlex.quote(x) for x in cmd)
ANSI_RE = re.compile(r"\x1b\[[0-9;]*[A-Za-z]")

def strip_ansi(text: str) -> str:
    return ANSI_RE.sub("", text)

def is_noise_result_line(s: str) -> bool:
    if not s:
        return True
    # PeTTa/Prolog trace scaffolding, not semantic result.
    if s.startswith("-->"):
        return True
    if set(s) == {"^"} and len(s) >= 5:
        return True
    if s.startswith(":- findall"):
        return True
    if s in {"_).", ")."}:
        return True
    # Continuation fragments from pretty-printed prolog goals.
    if s == "A)," or s.endswith(",") or s.endswith("),"):
        return True
    if s in {"[", "]", "],"}:
        return True
    if s.startswith("match(") or s.startswith("'") or s.startswith("[ '"):
        return True
    return False

def parse_result_section(stdout:str, expression:str):
    """
    Extract the actual local result of the final runnable expression.

    v01 failed here because PeTTa emits ANSI-coloured trace scaffolding:
      -->  prolog goal  -->
      A),
      ^^^^^^^^^^^^^^^^^^^^^^^
      <actual-result>

    The parser kept scaffold lines, so local_result_match became false even
    when the final semantic result was correct. v01.1 strips ANSI and treats
    only the last non-scaffold lines after the final caret as the result.
    """
    clean_stdout = strip_ansi(stdout)
    lines = clean_stdout.splitlines()

    start = None
    for i,line in enumerate(lines):
        if line.strip().startswith("--> metta runnable"):
            start = i
    if start is None:
        for i,line in enumerate(lines):
            if expression.strip() in line:
                start = i
    if start is None:
        return [], "", False

    caret = None
    for i in range(start, len(lines)):
        s = lines[i].strip()
        if s and set(s) == {"^"} and len(s) >= 5:
            caret = i

    result_lines = lines[caret+1:] if caret is not None else lines[start+1:]
    semantic = []
    for raw in result_lines:
        s = raw.strip()
        if is_noise_result_line(s):
            continue
        semantic.append(s)

    # Usually a single atom. Keep multiple semantic lines if the runtime ever returns them.
    actual = "\n".join(semantic).strip()
    unreduced = "(partial " in actual or actual.startswith("(partial")
    return semantic, actual, unreduced

def probes()->List[Tuple[str,str,str]]:
    return [
        ("persistence source declared", "!(q-persistence-class? source-file-declared)", "declared-substrate"),
        ("persistence runtime residue", "!(q-persistence-class? runtime-only)", "runtime-residue"),
        ("persistence restored durable norm", "!(q-persistence-class? restored-revalidated-routing-active)", "durable-growth-norm"),
        ("source declaration masquerade blocked", "!(q-learned-growth-source-status? source-file-declared no-runtime-trace no-restore-evidence)", "blocked-source-declaration-masquerade"),
        ("runtime learned source candidate", "!(q-learned-growth-source-status? runtime-added trace-recorded restore-evidence-present)", "learned-growth-source-candidate"),
        ("commit ready", "!(q-growth-commit-status? event contact-grounded trace-supported soul-routed support-adequate)", "growth-commit-ready"),
        ("commit blocked no trace", "!(q-growth-commit-status? event contact-grounded trace-absent soul-routed support-adequate)", "blocked-no-trace"),
        ("restore candidate", "!(q-growth-restored-status? event persisted-trace restored revalidated)", "restored-growth-candidate"),
        ("durable claim", "!(q-growth-claim-durability? growth-claim-allowed persisted restored revalidated)", "durable-growth-claim"),
        ("living pattern ready", "!(q-living-pattern-status? trace-present recurrence-supported decay-tracked revision-path-present)", "living-pattern-trace-ready"),
        ("living pattern needs decay", "!(q-living-pattern-status? trace-present recurrence-supported decay-absent revision-path-present)", "hold-needs-decay-tracking"),
        ("repetition without support blocked", "!(q-living-pattern-status? trace-present repetition-only decay-tracked revision-path-present)", "blocked-repetition-without-support"),
        ("reinforcement supported", "!(q-growth-reinforcement-status? event repeated-independent support-refresh-present low-contradiction)", "reinforcement-supported"),
        ("same source reinforcement blocked", "!(q-growth-reinforcement-status? event repeated-same-source support-refresh-present low-contradiction)", "blocked-not-independent"),
        ("decay weakens candidate", "!(q-growth-decay-status? event no-recent-support decay-window-open)", "decay-weakens-candidate"),
        ("fixed residue blocked", "!(q-growth-decay-status? event no-recent-support decay-ignored)", "blocked-fixed-residue"),
        ("calcification risk", "!(q-growth-calcification-risk? event high-repetition low-novelty revision-path-absent)", "calcification-risk"),
        ("continuity supported", "!(q-growth-continuity-status? event pre-state post-state carried-structure bounded-drift)", "structural-continuity-supported"),
        ("identity assertion blocked", "!(q-growth-continuity-status? event pre-state post-state identity-assertion drift-unknown)", "blocked-identity-assertion"),
        ("structural persistence", "!(q-growth-structural-persistence? event transform-applied invariant-preserved bounded-drift)", "graded-structural-persistence"),
        ("temporal carry", "!(q-growth-temporal-carry-status? event commit-cycle restore-cycle revalidation-cycle)", "growth-temporal-carry-supported"),
        ("persistent question open", "!(q-question-persistence-status? question support-present time-trace-present routing-open)", "persistent-question-open"),
        ("predictive growth realness", "!(q-growth-predictive-status? event prediction-loss-reduced interval-scoped soul-routed)", "growth-realness-supported"),
        ("predictive blocked no time", "!(q-growth-predictive-status? event prediction-loss-reduced interval-absent soul-routed)", "blocked-no-time-scope"),
        ("navigation improvement", "!(q-growth-navigation-improvement? event prior-routing new-routing outcome-improved)", "navigation-improvement-supported"),
        ("durable growth realness", "!(q-growth-realness-status? event prediction-loss-reduced soul-routed time-scoped contact-supported)", "durable-growth-realness-supported"),
        ("gentle routing update", "!(q-growth-routing-update-status? event restored-growth-candidate gentle-reweighting revision-path-present)", "durable-growth-norm-candidate"),
        ("hard override blocked", "!(q-growth-routing-update-status? event restored-growth-candidate hard-override revision-path-absent)", "blocked-overforced-norm"),
        ("low overforcing risk", "!(q-growth-overforcing-risk? event minimal-forcing high-carry revision-present)", "low-overforcing-risk"),
        ("durable norm", "!(q-growth-norm-status? event restored-growth-candidate routing-default-updated revision-path-present)", "durable-growth-norm"),
        ("durable norm blocked no revision", "!(q-growth-norm-status? event restored-growth-candidate routing-default-updated revision-path-absent)", "blocked-no-revision-path"),
        ("shared growth support", "!(q-growth-shared-memory-status? event shared-support-set independent-witness translation-witness-present)", "shared-growth-support"),
        ("question persistence missing temporal trace blocked", "!(q-question-persistence-status? question support-present time-trace-absent routing-open)", "blocked-no-temporal-trace"),
        ("stale residue blocked", "!(q-growth-staleness-risk? event old support-refresh-absent high-contradiction)", "blocked-stale-growth-residue"),
        ("restart pass semantic", "!(q-growth-restart-test-status? baseline-absent commit-observed restart-observed restore-observed revalidated)", "persistence-cycle-pass"),
        ("restart skipped hold", "!(q-growth-restart-test-status? baseline-absent commit-observed restart-skipped restore-observed revalidated)", "hold-restart-not-tested"),
        ("ephemeral leak blocked", "!(q-growth-negative-control-status? ephemeral-event restored)", "blocked-ephemeral-leak"),
        ("same source control blocked", "!(q-growth-negative-control-status? repeated-same-source reinforcement-claimed)", "blocked-not-independent"),
        ("no decay tracking control blocked", "!(q-growth-negative-control-status? no-decay-tracking durable-norm)", "blocked-fixed-residue"),
        ("hard override no revision blocked", "!(q-growth-negative-control-status? hard-override-no-revision durable-norm)", "blocked-overforced-norm"),
        ("harness target present", "!(match &self (q-v08-6-harness-target predictive-navigation-realness-reduces) present)", "present"),
    ]

def runtime_probe(engine:Path, container:str, rec:Recorder, raw_mode:str, raw_tail_chars:int):
    if not engine.exists(): rec.add("Tier R0","runtime skipped missing engine","SKIP",str(engine)); return
    et=engine.read_text(errors="replace"); raw_dir=rec.log_dir/"raw_probe_outputs"
    if raw_mode in {"fail","all"}: raw_dir.mkdir(parents=True, exist_ok=True)
    ps=probes(); rec.add("Tier R0","runtime semantic probes active","PASS",f"planned_probes={len(ps)}")
    for idx,(name,expr,expected) in enumerate(ps,1):
        safe=re.sub(r"[^A-Za-z0-9_.-]+","_",name)[:80].strip("_")
        temp=f"/tmp/_v08_6_hyperseed_durable_memory_{idx:03d}_{safe}.metta"
        body=engine_plus_expression(et,expr)
        wrc,wout,werr,wcmd=docker_write(container,temp,body)
        rc,stdout,stderr,rcmd=docker_run_metta(container,temp) if wrc==0 else (wrc,wout,werr,"write failed")
        result,actual,unreduced=parse_result_section(stdout,expr)
        local = expected in result or actual==expected or expected in actual.split()
        status="PASS" if rc==0 and local and not unreduced else "FAIL"
        sidecar=None
        if raw_mode=="all" or (raw_mode=="fail" and status=="FAIL"):
            sidecar=raw_dir/f"probe_{idx:03d}_{safe}.raw.txt"; sidecar.write_text(stdout)
        rec.add("Tier R1",name,status,f"expected={expected}; actual={actual!r}; local={local}; unreduced={unreduced}; returncode={rc}",{
            "probe_index":idx,"expression":expr,"expected_token":expected,"actual_result_section":result,
            "actual_result_text":actual,"local_result_match":local,"unreduced":unreduced,"returncode":rc,
            "stdout_chars":len(stdout),"stdout_sha256":sha256_bytes(stdout.encode()),"stdout_tail":"" if status=="PASS" else stdout[-raw_tail_chars:],
            "stderr_chars":len(stderr),"stderr_sha256":sha256_bytes(stderr.encode()),"stderr_tail":"" if status=="PASS" else stderr[-raw_tail_chars:],
            "raw_sidecar_path":str(sidecar) if sidecar else None,"temp_path":temp,"docker_run_command":rcmd,"docker_write_command":wcmd
        })

def storage_paths(root:Path):
    return {"memory_dir":root/"memory","history_metta":root/"memory"/"history.metta","promotions_db":root/"memory"/"promotions.db","memory_chromadb":root/"memory"/"chromadb","soul_dir":root/"soul","chroma_db_dir":root/"chroma_db","staging_dir":root/"staging"}
def inspect_storage(root:Path, rec:Recorder, event_id:Optional[str]=None):
    paths=storage_paths(root); data={k:file_info(v) for k,v in paths.items()}
    required=["memory_dir","history_metta","staging_dir"]
    present=[k for k in required if data[k]["exists"]]
    rec.add("Tier P0","storage surfaces inspected","PASS" if len(present)>=2 else "INSPECT",f"present={present}",data)
    if event_id:
        hits={}
        hist=paths["history_metta"]
        hits["history_metta"] = hist.exists() and event_id in safe_read_text(hist)
        staging=[]; sd=paths["staging_dir"]
        if sd.exists():
            for p in sd.rglob("*"):
                if p.is_file() and p.stat().st_size < 20_000_000:
                    try:
                        if event_id in p.read_text(errors="ignore"): staging.append(str(p))
                    except Exception: pass
        hits["staging_files"]=staging
        db=paths["promotions_db"]; dbi={"exists":db.exists(),"tables":[],"event_id_seen":False,"error":None}
        if db.exists() and db.is_file():
            try:
                con=sqlite3.connect(str(db)); cur=con.cursor(); tables=[r[0] for r in cur.execute("SELECT name FROM sqlite_master WHERE type='table'").fetchall()]; dbi["tables"]=tables
                for t in tables:
                    try:
                        rows=cur.execute(f"SELECT * FROM {t} LIMIT 500").fetchall()
                        if any(event_id in str(r) for r in rows): dbi["event_id_seen"]=True
                    except Exception: pass
                con.close()
            except Exception as e: dbi["error"]=repr(e)
        hits["promotions_db"]=dbi
        any_hit=bool(hits["history_metta"] or staging or dbi["event_id_seen"])
        rec.add("Tier P1","event visible on durable storage surfaces","PASS" if any_hit else "HOLD",f"event_id={event_id}; any_hit={any_hit}",hits)

def commit_probe(engine:Path, container:str, rec:Recorder, event_id:str, raw_mode:str, raw_tail_chars:int):
    if not engine.exists(): rec.add("Tier C0","commit skipped missing engine","SKIP",str(engine)); return
    et=engine.read_text(errors="replace")
    script="\n".join([
        f"!(add-atom &self (q-durable-growth-committed {event_id} contact-grounded trace-supported soul-routed persisted-trace))",
        f"!(match &self (q-durable-growth-committed {event_id} $contact $trace $soul $persist) (committed {event_id} $contact $trace $soul $persist))",
        f"!(q-growth-commit-status? {event_id} contact-grounded trace-supported soul-routed support-adequate)",
        f"!(q-living-pattern-status? trace-present recurrence-supported decay-tracked revision-path-present)",
    ])
    temp=f"/tmp/_v08_6_hyperseed_commit_{event_id}.metta"; body=engine_plus_expression(et,script)
    wrc,wout,werr,wcmd=docker_write(container,temp,body); rc,stdout,stderr,rcmd=docker_run_metta(container,temp) if wrc==0 else (wrc,wout,werr,"write failed")
    committed=f"committed {event_id}" in stdout; ready="growth-commit-ready" in stdout; living="living-pattern-trace-ready" in stdout
    status="PASS" if rc==0 and committed and ready and living else "FAIL"
    manifest=rec.log_dir/f"durable_memory_commit_manifest_{event_id}.json"
    manifest.write_text(json.dumps({"event_id":event_id,"committed_seen":committed,"commit_ready_seen":ready,"living_pattern_seen":living,"stdout_sha256":sha256_bytes(stdout.encode()),"created_at":dt.datetime.now().isoformat()},indent=2))
    rec.add("Tier C0","runtime durable-memory marker commit",status,f"event_id={event_id}; committed={committed}; commit_ready={ready}; living={living}; manifest={manifest}",{"stdout_tail":"" if status=="PASS" else stdout[-raw_tail_chars:],"stdout_chars":len(stdout),"stdout_sha256":sha256_bytes(stdout.encode()),"docker_write_command":wcmd,"docker_run_command":rcmd})

def restart_container(container:str, rec:Recorder):
    cmd=["docker","restart",container]; rc,out,err=run_cmd(cmd,timeout=180)
    rec.add("Tier C1","container restart boundary crossed","PASS" if rc==0 else "FAIL",f"container={container}; returncode={rc}",{"stdout":out,"stderr":err,"command":" ".join(shlex.quote(x) for x in cmd)})
    if rc==0: time.sleep(5)

def restore_probe(engine:Path, container:str, rec:Recorder, event_id:str, raw_mode:str, raw_tail_chars:int):
    if not engine.exists(): rec.add("Tier C2","restore skipped missing engine","SKIP",str(engine)); return
    et=engine.read_text(errors="replace")
    script="\n".join([
        f"!(match &self (q-durable-growth-committed {event_id} $contact $trace $soul $persist) (restored {event_id} $contact $trace $soul $persist))",
        f"!(q-growth-restored-status? {event_id} persisted-trace restored revalidated)",
        f"!(q-growth-routing-update-status? {event_id} restored-growth-candidate gentle-reweighting revision-path-present)",
        f"!(q-growth-norm-status? {event_id} restored-growth-candidate routing-default-updated revision-path-present)",
    ])
    temp=f"/tmp/_v08_6_hyperseed_restore_{event_id}.metta"; body=engine_plus_expression(et,script)
    wrc,wout,werr,wcmd=docker_write(container,temp,body); rc,stdout,stderr,rcmd=docker_run_metta(container,temp) if wrc==0 else (wrc,wout,werr,"write failed")
    restored=f"restored {event_id}" in stdout; restored_status="restored-growth-candidate" in stdout; routing="durable-growth-norm-candidate" in stdout; norm="durable-growth-norm" in stdout
    status="PASS" if rc==0 and restored and restored_status and routing and norm else "HOLD"
    rec.add("Tier C2","post-boundary restore and norm evidence",status,f"event_id={event_id}; restored={restored}; restored_status={restored_status}; routing={routing}; norm={norm}",{"stdout_tail":"" if status=="PASS" else stdout[-raw_tail_chars:],"stdout_chars":len(stdout),"stdout_sha256":sha256_bytes(stdout.encode()),"docker_write_command":wcmd,"docker_run_command":rcmd})

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--engine",default="staging/lib_quantale_autopoietic_epistemic_dynamics_engine_v08_6_HYPERSEED_DURABLE_MEMORY_SURFACE.metta")
    ap.add_argument("--ladder",default="staging/quantale_engine_validation_ladder_v08_6_HYPERSEED_DURABLE_MEMORY_SURFACE.metta")
    ap.add_argument("--log-dir",default="shared_files")
    ap.add_argument("--repo-root",default=".")
    ap.add_argument("--container",default="clarity_omega")
    ap.add_argument("--runtime",action="store_true")
    ap.add_argument("--inspect-storage",action="store_true")
    ap.add_argument("--commit-test",action="store_true")
    ap.add_argument("--restart-container",action="store_true")
    ap.add_argument("--restore-test",action="store_true")
    ap.add_argument("--event-id",default=None)
    ap.add_argument("--raw-mode",choices=["none","fail","all"],default="fail")
    ap.add_argument("--raw-tail-chars",type=int,default=3000)
    args=ap.parse_args()
    engine=Path(args.engine); ladder=Path(args.ladder); out=Path(args.log_dir)
    event_id=args.event_id or ("growth_event_"+dt.datetime.now().strftime("%Y%m%d_%H%M%S"))
    rec=Recorder(out,{"harness_version":HARNESS_VERSION,"engine":str(engine),"ladder":str(ladder),"runtime":args.runtime,"container":args.container,"event_id":event_id})
    static_checks(engine,ladder,rec)
    if args.runtime: runtime_probe(engine,args.container,rec,args.raw_mode,args.raw_tail_chars)
    else: rec.add("Tier R0","runtime semantic probes skipped","SKIP","use --runtime")
    if args.inspect_storage: inspect_storage(Path(args.repo_root),rec,event_id if (args.commit_test or args.restore_test or args.event_id) else None)
    else: rec.add("Tier P0","storage inspection skipped","SKIP","use --inspect-storage")
    if args.commit_test:
        if args.runtime: commit_probe(engine,args.container,rec,event_id,args.raw_mode,args.raw_tail_chars)
        else: rec.add("Tier C0","commit requested without runtime","FAIL","commit requires --runtime")
    else: rec.add("Tier C0","commit test not requested","HOLD","use --commit-test")
    if args.restart_container:
        restart_container(args.container,rec)
    else: rec.add("Tier C1","restart boundary not crossed","HOLD","use --restart-container for real persistence evidence")
    if args.restore_test or args.restart_container:
        if args.runtime: restore_probe(engine,args.container,rec,event_id,args.raw_mode,args.raw_tail_chars)
        else: rec.add("Tier C2","restore requested without runtime","FAIL","restore requires --runtime")
    else: rec.add("Tier C2","restore test not requested","HOLD","use --restore-test or --restart-container")
    mp,jp=rec.write(); print(f"TRACE_MD {mp}"); print(f"TRACE_JSON {jp}"); print(f"SUMMARY {rec.summary()}")
    return 1 if rec.summary().get("FAIL",0) else 0
if __name__ == "__main__": raise SystemExit(main())
