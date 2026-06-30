#!/usr/bin/env python3
"""
probe_getskills_type.py

Proves the REAL cause of the string_length crash, using the actual src/skills.metta
getSkills (NOT a stub -- the stub is what masked this last time). Standalone via
run.sh; does not touch the loop.

Hypotheses under test, stated before running:
  H1  getSkills returns a MULTI-ELEMENT expression (list of skill strings),
      not a single flat string.
  H2  (string_length (getSkills)) FAILS / errors (reproduces the crash) because
      string_length wants a flat string, not a list.
  H3  flattening first with py-str fixes it: (string_length (py-str (getSkills)))
      yields an integer.
  H4  dispatch-skills returns getSkills' value, so the same flatten-then-measure
      works on (dispatch-skills 1); and py-str of it is non-empty (content path
      unaffected -- only the marker's length computation was wrong).

If H1-H4 hold, the marker fix is: measure (string_length (py-str $skills-str)),
not (string_length $skills-str). The content substitution ($skills-str into the
big py-str) was already correct because that py-str flattens.

USAGE (from repo root, after reverse has restored a clean tree):
  python3 staging/probe_getskills_type.py
"""

import datetime
import re
import subprocess

CONTAINER = "clarity_omega"
REPO = "/PeTTa/repos/omegaclaw"
DRAFT = REPO + "/soul/capability_registry_path_c_draft.metta"
SKILLS = REPO + "/src/skills.metta"
STAMP = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
LOG = "/tmp/probe_getskills_type_%s.log" % STAMP

RUNCHAIN_OLD = """(if (== $result decision-anchor)
                             (add-atom &self
                               (dispatch-chain-anchored
                                 invocation-id: $invocation-id
                                 anchor-handler: $handler))
                             (run-chain $tail $input-atom $invocation-id))"""
RUNCHAIN_NEW = """(progn
                           (add-atom &self
                             (dispatch-result
                               invocation-id: $invocation-id
                               result: $result
                               handler: $handler))
                           (if (== $result decision-anchor)
                             (add-atom &self
                               (dispatch-chain-anchored
                                 invocation-id: $invocation-id
                                 anchor-handler: $handler))
                             (run-chain $tail $input-atom $invocation-id)))"""

SKILL = """
(eligible-lifecycle active)
(registered-capability schema: (skill-request cycle: $k) handler: skill-discovery
   priority: 100 lifecycle: active metadata: ())
(= (skill-discovery $request)
   (let* (($capabilities (collapse (match &self
        (registered-capability schema: $s handler: $h priority: $p lifecycle: active metadata: $m)
        ($s $h $p $m))))
          ($formatted (format-skill-set $capabilities)))
         (skill-set skills: $formatted)))
(= (format-skill-set $capabilities) (getSkills))
(= (dispatch-skills $k)
   (let $_ (dispatch (skill-request cycle: $k) $k)
        (first-skill-or-default
          (collapse (match &self
            (dispatch-result invocation-id: $k result: (skill-set skills: $s) handler: $_h) $s)))))
(= (first-skill-or-default $strs)
   (if (== $strs ())
       (getSkills)
       (let $h (car-atom $strs)
            (if (== $h ()) (first-skill-or-default (cdr-atom $strs)) $h))))

;; ---- VALID tests: each candidate wrapped in a CALLED function so the inner
;; ---- (string_length ...) / (py-str ...) / (size-atom ...) compile as real
;; ---- calls, exactly as they do inside the loop's getContext let*. Isolated
;; ---- per bang so one failure does not suppress the others.
(= (p-size)  (let $x (size-atom (getSkills)) (PR-SIZE $x)))
(= (p-flat)  (let $x (string_length (py-str (getSkills))) (PR-FLAT $x)))
(= (p-dsize) (let $s (dispatch-skills 1) (let $x (size-atom $s) (PR-DSIZE $x))))
(= (p-dflat) (let $s (dispatch-skills 1) (let $x (string_length (py-str $s)) (PR-DFLAT $x))))
(= (p-dcontent) (let $s (dispatch-skills 1) (let $x (string_length (py-str $s)) (PR-DCONTENT $x))))
;; raw crash reproduction in a faithful (called-function) context, LAST.
(= (p-raw) (let $x (string_length (getSkills)) (PR-RAW $x)))
"""


def sh(cmd, stdin=None):
    p = subprocess.run(["docker", "exec", "-i", CONTAINER, "sh", "-c", cmd],
                       input=stdin, capture_output=True, text=True)
    return p.stdout + p.stderr


def section(out, marker):
    return out.rsplit(marker, 1)[-1] if marker in out else ""


def main():
    buf = []

    def say(s):
        print(s)
        buf.append(s)

    say("getSkills type probe %s" % STAMP)
    skills_src = sh("cat %s" % SKILLS)
    if "getSkills" not in skills_src:
        say("ERROR: could not read getSkills from %s. Output:\n%s" % (SKILLS, skills_src[:300]))
        return
    registry = sh("cat %s" % DRAFT)
    promoted = re.sub(r"\s+".join(re.escape(t) for t in RUNCHAIN_OLD.split()),
                      lambda m: RUNCHAIN_NEW, registry, count=1)

    probe = (skills_src + "\n" + promoted + "\n" + SKILL + """
!("===RESULTS===")
!(p-size)
!(p-flat)
!(p-dsize)
!(p-dflat)
!(p-dcontent)
!(p-raw)
""")
    path = "/tmp/_gsprobe_%s.metta" % STAMP
    sh("cat > %s" % path, stdin=probe)
    out = sh("cd /PeTTa && ./run.sh %s 2>&1" % path)
    buf.append("===== RAW =====\n" + out)
    res = out.rsplit("===RESULTS===", 1)[-1]

    def intval(label):
        m = re.search(r"\(" + label + r"\s+(\d+)\)", res)
        return int(m.group(1)) if m else None

    size = intval("PR-SIZE")
    flat = intval("PR-FLAT")
    dsize = intval("PR-DSIZE")
    dflat = intval("PR-DFLAT")
    dcontent = intval("PR-DCONTENT")
    raw_ok = re.search(r"\(PR-RAW\s+(\d+)\)", res) is not None  # True only if string_length(list) somehow succeeded

    say("PR-SIZE   size-atom (getSkills)                      = %s" % size)
    say("PR-FLAT   string_length (py-str (getSkills))          = %s" % flat)
    say("PR-DSIZE  size-atom on dispatch-skills result        = %s" % dsize)
    say("PR-DFLAT  string_length (py-str dispatch-skills)      = %s" % dflat)
    say("PR-DCONTENT (same as DFLAT; content present if > 0)   = %s" % dcontent)
    say("PR-RAW    string_length on raw list succeeded?         = %s (expected NO/crash)" % raw_ok)

    say("")
    candidates = []
    if dsize and dsize > 0:
        candidates.append("size-atom  -> marker = (size-atom $skills-str)        [DSIZE=%d]" % dsize)
    if dflat and dflat > 0:
        candidates.append("py-str+len -> marker = (string_length (py-str $skills-str)) [DFLAT=%d]" % dflat)
    if candidates:
        say("VALID FIX CANDIDATES (proven on the dispatch path, in a called-function context):")
        for c in candidates:
            say("  " + c)
        say("Recommend size-atom if present (simplest; no py-str dependency).")
    else:
        say("NO candidate returned a positive integer on the dispatch path. Read RAW; do not patch.")
    say("Raw-list string_length reproduced the crash: %s" % ("NO (it succeeded?! investigate)" if raw_ok else "YES (as expected)"))
    sh("cat > %s" % LOG, stdin="\n".join(buf))
    print("\nRaw trace in-container at %s" % LOG)


if __name__ == "__main__":
    main()
