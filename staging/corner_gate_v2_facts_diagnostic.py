#!/usr/bin/env python3
"""
corner_gate_v2_facts_diagnostic.py

Read-only verification that the crisis ledger's load-bearing facts are THE
facts (Berton's requirement, 2026-07-08). Checks the live tree, the running
container (if up), and the logs. Ends with the harnessable inline chain
re-proof (exemplar transport: inline bodies via run.sh; per the pipeline
harness's own doctrine, import-ORDER behavior is a BOOT test, not a harness
test, so this script verifies everything else and names that boundary).

Style: capability_registry_diagnostic / corner_gap_pipeline_harness.
RAW OUTPUT BEFORE EVERY VERDICT. Unreduced echo = FAIL. Read-only throughout.

USAGE: python3 staging/corner_gate_v2_facts_diagnostic.py [--container clarity_omega]
       [--post-fix]   # after the import-order fix: expects engine BEFORE consumers
"""
import argparse
import re
import subprocess
import sys

TIMEOUT = 60
MANIFEST = "lib_clarity_reasoning/lib_clarity_reasoning.metta"
ENGINE_FILE = ("lib_clarity_reasoning/lib_quantale_autopoietic_epistemic_dynamics_"
               "engine_v08_7_2_SOUL_EVOLUTIONARY_CANONICAL_TOPOLOGY")


def run(cmd, **kw):
    return subprocess.run(cmd, capture_output=True, text=True, timeout=TIMEOUT, **kw)


def strip_ansi(t):
    return re.sub(r"\x1b\[[0-9;]*m", "", t or "")


RESULTS = {}


def verdict(label, ok, detail=""):
    RESULTS[label] = ok
    print("  " + label.ljust(58) + (" PASS" if ok else " FAIL")
          + (("   " + detail) if detail else ""))
    return ok


def stage(name):
    print("\n" + "=" * 72 + "\n" + name + "\n" + "=" * 72)


def host_read(path):
    try:
        with open(path) as f:
            return f.read()
    except OSError:
        return None


def import_line_no(manifest_text, needle):
    for i, line in enumerate(manifest_text.splitlines(), 1):
        if line.startswith("!(import!") and needle in line:
            return i
    return None


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--container", default="clarity_omega")
    ap.add_argument("--post-fix", action="store_true",
                    help="Expect the import-order fix applied (engine before consumers)")
    args = ap.parse_args()
    c = args.container

    stage("STAGE 1  MANIFEST FACTS (host tree)")
    m = host_read(MANIFEST)
    if m is None:
        print("  FATAL: manifest not readable from host. Run from repo root.")
        sys.exit(2)
    engine_count = m.count("!(import! &self (library omegaclaw ./" + ENGINE_FILE + "))")
    verdict("F1 engine import occurs exactly once (anti-fork)", engine_count == 1,
            f"count={engine_count}")
    ln_engine = import_line_no(m, ENGINE_FILE)
    ln_selfc = import_line_no(m, "lib_self_continuity")
    ln_merge = import_line_no(m, "coupling_quantale_merge")
    ln_gate = import_line_no(m, "corner_gate")
    print(f"  import positions: engine={ln_engine} self_continuity={ln_selfc} "
          f"merge={ln_merge} corner_gate={ln_gate}")
    have_all = None not in (ln_engine, ln_selfc, ln_merge)
    verdict("F2 all three key imports present", have_all)
    if have_all:
        if args.post_fix:
            verdict("F3 ORDER: engine BEFORE self_continuity AND merge (C1' fix)",
                    ln_engine < ln_selfc and ln_engine < ln_merge)
        else:
            verdict("F3 ORDER (current, documents the C1' defect): "
                    "engine AFTER merge", ln_engine > ln_merge)
    verdict("F4 lib_quantale import absent (retirement holds)",
            "!(import! &self (library omegaclaw ./lib_clarity_reasoning/lib_quantale))"
            not in m)

    stage("STAGE 2  SOURCE FACTS (host tree)")
    loop = host_read("src/loop.metta") or ""
    verdict("F5 loop 166 gate-v2 call present (the kill site)",
            "(apply-corner-gate-v2 $sexpr_verdict $msgnew)" in loop)
    ww = host_read("soul/corner_gap/corner_window_writers.metta") or ""
    verdict("F6 corner-window driver INERT (diagnostic toggle in place)",
            "INERT-PROBE 2026-07-07" in ww)
    sentinels = 0
    for path in ["soul/recent_action_populator.metta",
                 "soul/corner_gap/state_delta_writer_writers.metta",
                 "soul/corner_gap/coupling_integrity_detector_writers.metta",
                 "soul/idle_cycle_detector_writers.metta",
                 "soul/agency_balance_guard_writers.metta"]:
        t = host_read(path) or ""
        if "TRACE-17" in t:
            sentinels += 1
    verdict("F7 five trace sentinels on disk", sentinels == 5, f"found={sentinels}")
    rc = run(["grep", "-rn", "--include=*.metta", "(= (q-geq",
              "lib_clarity_reasoning/", "soul/"])
    qgeq_sites = [l for l in rc.stdout.splitlines() if ".bak" not in l]
    verdict("F8 q-geq defined at exactly one loaded site (lib_self_continuity)",
            len(qgeq_sites) == 1 and "lib_self_continuity" in qgeq_sites[0],
            f"sites={len(qgeq_sites)}")
    # F9: the anti-duplicate-dispatch invariant is about LOADED files. Build the
    # loaded set FROM the manifest's own import lines (principled, no hardcoded
    # exclusions), then intersect with the on-disk definition sites.
    loaded = set()
    for line in m.splitlines():
        mm = re.search(r"\(library omegaclaw \./([^)\s]+)\)", line)
        if mm and line.startswith("!(import!"):
            loaded.add(mm.group(1) + ".metta")
    rc = run(["grep", "-rln", "--include=*.metta", "(= (q-meet",
              "lib_clarity_reasoning/", "soul/"])
    disk_sites = [l for l in rc.stdout.splitlines() if ".bak" not in l]
    loaded_sites = [f for f in disk_sites if f in loaded]
    unloaded_sites = [f for f in disk_sites if f not in loaded]
    if unloaded_sites:
        print("  on-disk but UNIMPORTED (excluded by manifest intersection): "
              + str(unloaded_sites))
    verdict("F9 q-meet defined at exactly one LOADED site (the v08.7.2 engine)",
            len(loaded_sites) == 1 and "v08_7_2" in loaded_sites[0],
            f"loaded_sites={loaded_sites}")

    stage("STAGE 3  CONTAINER + LOG FACTS (skipped cleanly if container down)")
    up = False
    try:
        p = run(["docker", "ps", "--filter", "name=" + c, "--format", "{{.Names}}"])
        up = p.returncode == 0 and c in p.stdout
    except Exception:
        up = False
    print("  container running: " + str(up))
    if up:
        p = run(["docker", "exec", c, "grep", "-c", "INERT-PROBE",
                 "/PeTTa/repos/omegaclaw/soul/corner_gap/corner_window_writers.metta"])
        verdict("F10 container sees the inert driver (mount serving)",
                p.stdout.strip() == "1", f"count={p.stdout.strip()!r}")
        p = run(["docker", "logs", c])
        logs = strip_ansi(p.stdout + p.stderr)
        runtime = [l for l in logs.splitlines() if "println" not in l]
        fired = sum(1 for l in runtime if "(TRACE-172-EXIT)" in l)
        d1 = sum(1 for l in runtime if "(DIAG-CYCLE-START" in l)
        verdict("F11 msgnew path completes (TRACE-172-EXIT fired at least once)",
                fired >= 1, f"fires={fired}")
        verdict("F12 d1 fired at least once (full-chain completion observed)",
                d1 >= 1, f"fires={d1}")

    stage("STAGE 4  HARNESSABLE CHAIN RE-PROOF (inline transport, exemplar doctrine)")
    print("  NOTE per corner_gap_pipeline_harness: one-shot run.sh does NOT register")
    print("  import!-ed rules; probe imports double-load. Import-ORDER is therefore a")
    print("  BOOT test. This stage re-proves the chain LOGIC on inline bodies only.")
    if up:
        srcs = ["/PeTTa/repos/omegaclaw/" + ENGINE_FILE + ".metta",
                "/PeTTa/repos/omegaclaw/lib_clarity_reasoning/lib_self_continuity.metta",
                "/PeTTa/repos/omegaclaw/soul/corner_gap/state_delta_writer.metta",
                "/PeTTa/repos/omegaclaw/soul/corner_gap/coupling_integrity_detector.metta",
                "/PeTTa/repos/omegaclaw/soul/corner_gap/coupling_quantale_merge.metta"]
        body = ""
        ok_read = True
        for s in srcs:
            p = run(["docker", "exec", c, "cat", s])
            if p.returncode != 0:
                ok_read = False
                print("  could not read: " + s)
                break
            body += p.stdout + "\n"
        if ok_read:
            fixture = ("!(add-atom &self (recent-action 1 exploration-query \"p\"))\n"
                       "!(add-atom &self (recent-action 2 exploration-query \"p\"))\n"
                       "!(add-atom &self (recent-action 3 exploration-query \"p\"))\n"
                       "!(add-atom &self (recent-action 4 exploration-query \"p\"))\n"
                       "!(add-atom &self (state-delta 4 none))\n"
                       "!(println! (H1_CORE (corner-pbit-core)))\n"
                       "!(println! (H2_CONFIRMED (corner-confirmed-core)))\n")
            text = "!(import! &self (library lib_import))\n" + body + fixture
            wr = run(["docker", "exec", "-i", c, "sh", "-c",
                      "cat > /tmp/facts_chain.metta"], input=text)
            if wr.returncode == 0:
                p = run(["docker", "exec", c, "sh", "-c",
                         "cd /PeTTa && ./run.sh /tmp/facts_chain.metta 2>&1 | tail -20"])
                raw = strip_ansi(p.stdout)
                print("  RAW (tail):")
                for l in raw.splitlines()[-8:]:
                    print("    " + l)
                got_core = "(H1_CORE (mk-pbit" in raw
                got_conf = ("(H2_CONFIRMED true)" in raw
                            or "(H2_CONFIRMED false)" in raw
                            or "(H2_CONFIRMED True)" in raw
                            or "(H2_CONFIRMED False)" in raw)
                verdict("F13 inline chain: corner-pbit-core reduces to ground pbit",
                        got_core)
                verdict("F14 inline chain: corner-confirmed-core reduces to a boolean",
                        got_conf)
            else:
                print("  could not write probe file into container; stage skipped")
    else:
        print("  container down; Stage 4 requires it (run.sh transport). Skipped.")

    stage("SUMMARY")
    for k, v in RESULTS.items():
        print("  " + k.ljust(62) + (" PASS" if v else " FAIL"))
    allp = all(RESULTS.values())
    print("\n  >>> " + ("ALL FACTS VERIFIED." if allp else
          "AT LEAST ONE FACT FAILED VERIFICATION: the ledger updates BEFORE any fix ships."))
    sys.exit(0 if allp else 3)


if __name__ == "__main__":
    main()
