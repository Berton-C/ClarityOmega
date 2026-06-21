# The Shared Ethic: Cold-Harness-then-Reversible-Apply

**What this is.** A generic, project-wide guide to how ClarityOmega extends its runtime
safely. It is not tied to any one capability. It captures the single discipline that the
project's verify and apply scripts all embody, so that a fresh thread (a context-less
Claude, or a new contributor) can read this, then read the canonical template scripts,
and be back on scope and method before writing a line of code.

**How to use it when context is lost.** Read this document first. Then read the four
canonical templates named in Section 9 against this frame. The templates are the ground
truth for mechanics; this document is the ground truth for intent. If what you are about
to write does not match the ethic in Section 1 and would not pass the checklist in
Section 10, stop and rebuild it to the templates before proposing it.

---

## 1. The one shared ethic

Prove every substrate function reduces correctly while no water is flowing, on synthetic
inputs, with the raw reduction trace as the source of truth, before any wiring. Then land
the wiring as a coordinated all-or-none edit that builds its own reverse at the same
moment it builds the forward, because the runtime invariably goes south and a clean
rollback has to exist before it is needed.

Two halves, both non-negotiable:

1. **Verify cold, then wire.** A capability is not "built" because the MeTTa looks right.
   It is built when a hands-only harness has shown each function reducing and classifying
   correctly in the live container, on seeded inputs, with the full trace logged. Reading
   is necessary but not sufficient; the harness is the proof.
2. **Apply reversibly, never trust the write.** Every edit to a live file lands through a
   one-shot script that is dry-run by default, simulates forward and reverse, checks
   parens and line deltas and pre-state, backs up, writes, then re-reads from disk to
   confirm. The reverse path is first-class and dry-run-tested alongside the forward.

Getting things done by skipping either half serves no one. It wastes time, tokens, and
attention, and it ships non-functional code that has to be found and unwound in the
runtime later. Get it right, build it right, no waste.

---

## 2. The two instruments

There are exactly two kinds of script, and they answer different questions.

- **The harness** (verify / diagnostic). Answers "do these substrate functions reduce and
  classify correctly?" It runs cold against staged files before any wiring. It never
  computes the cognition; it checks it.
- **The apply script.** Answers "can this wiring land and be rolled back cleanly?" It is
  the only thing that writes to live files (loop.metta, helper.py, lib_clarity_reasoning,
  artifact_1), and it writes nothing until every check is green.

A capability moves from drafted to live by passing through a harness, then through one or
more apply scripts, then through an in-loop behavioral test (Section 6).

---

## 3. Harness discipline

Every harness obeys these. They are generic; the specific probes change, the shape does not.

1. **Hands only.** Python builds the expressions, runs them through the container's
   evaluator, parses output, and compares to a reference computed independently in Python.
   Python never computes the cognition. The reference exists only to check the substrate,
   never as a production path. This keeps the MeTTa-first boundary inside the test rig.
2. **Raw output before every verdict.** Print the actual reduction tail before PASS or
   FAIL. This is the safeguard against false confidence. A verdict with no visible raw is
   not trustworthy.
3. **Unreduced detection, in the result section only.** An echoed `(function ...)` term in
   the result means the function did not fire: that is a FAIL, not a pass. Scan only the
   lines after the last result separator, because the source echo and the prolog goal
   appear above and would false-match every reduced call. (See Section 5.)
4. **Inline the bodies; do not rely on `import!`.** A one-shot evaluator compiles inline
   `(= ...)` definitions to reducible clauses but does not register `import!`-ed library
   rules for top-level evaluation. So the harness reads the actual file bodies and
   concatenates them ahead of the test calls. Whether the production import path registers
   the file is a separate boot question, not this harness.
5. **Fresh space per call.** Each evaluator invocation reloads a clean AtomSpace. Each
   scenario seeds its own atoms, and any write-then-read lives in one combined invocation.
   State both polarities of every check before running it.
6. **Preflight.** Distinguish substrate-wrong from substrate-absent: container running,
   files present, evaluator found. Fail early with the reason.
7. **The results artifact.** Every run writes a timestamped log to both the host and the
   container, capturing per probe the exact script sent and the complete raw trace, not
   just the console tail. The console stays readable; the log is the durable, diff-able
   record where the load-bearing knowledge lives.
8. **Lenient parsers, raw is truth.** Extractors are forgiving (booleans render lowercase;
   the goal-success marker is dropped) and never override the raw. The summary names what
   each failure means and where to look.

---

## 4. Apply discipline

Every apply script obeys these.

1. **Dry-run by default.** `--apply` writes, `--reverse --apply` rolls back. Nothing writes
   until every check passes. The reverse is simulated and dry-run-checked next to the
   forward, before anything is committed to disk.
2. **All-or-none coordinated edits.** When a change spans files (for example loop.metta
   plus the lib import plus the artifact_1 phase entry), they land as one change or none.
   The maintenance contract (keep the wiring diagram current in the same commit) is folded
   into the same script, not deferred.
3. **Anchor exactly once.** Each edit keys on an exact existing line or substring that must
   appear precisely once. If it is not found exactly once, abort. This is what prevents a
   wrong-location edit.
4. **Code-aware paren count.** Count parens excluding string literals and line comments,
   before and after. The delta must be zero. A balanced expression changes nothing.
5. **Simulate, state-check, assert line delta, back up, write, re-verify from disk.** Check
   the pre-state (forward: anchors present and new absent; reverse: new present) to block
   double-apply. Assert the exact line delta. Back up to `path.bak.<tag>` before
   overwriting. After writing, re-read from disk and re-check parens and state, because the
   write is not trusted until the disk confirms it. Print a diff preview first, and the
   exact rebuild command on success.

---

## 5. The non-obvious techniques that carry the weight

These are the parts that are easy to miss and expensive to get wrong.

- **The result-section scan.** The evaluator echoes the source `!(fname ...)` line and a
  prolog goal above the actual reduction result. Unreduced-detection must read only below
  the last result separator, or every reduced call false-matches its own echo and the
  harness reports false PASS. This single technique is what separates a real reduction from
  an echo that looks like output. Note: function names can end in `?`; the echo-match
  pattern must allow a non-word character after the name (a space or close-paren), or it
  silently fails to detect unreduced predicates.
- **The transport gap.** Inline bodies, not imports, for the reasons in 3.4. The corollary
  is that the repo is copied into the image at build, not live-mounted, so a freshly
  drafted file is not in the running container until a rebuild. Cold validation therefore
  reads the new file from the host and reads its already-built dependencies from the
  container.
- **Fresh space per call.** Atoms written in one evaluator call are invisible in the next.
  Probes that write and read must be one combined invocation.
- **Read the instrument first.** You cannot trust any test if you cannot trust the read or
  the input construction that the test relies on. Confirm the input-building mechanism (for
  example, that parsing a command-list string yields the expected data shape and count)
  before trusting any result that depends on it.
- **Empty strings and booleans across the bridge.** A Python empty string returned through
  the bridge does not equal MeTTa's `""`; test presence with string-length greater than
  zero. Booleans render lowercase in output. A nested ordinary-function call inside a bind
  does not reduce; sequence it through a `let`. (These are runtime physics; consult the
  Atom Operations Map before composing.)

---

## 6. The harness / in-loop boundary

A cold harness proves that functions reduce and classify on synthetic inputs. It does not
prove behavior. Name the boundary; never let it blur.

What a cold harness cannot answer, and where each belongs instead:

- **Does a Python bridge resolve under the one-shot evaluator?** This is itself a discovery
  probe inside the harness. If a function depends on a `py-call` bridge, probe the bridge
  in isolation first; if it does not reduce cold, the functions that depend on it are
  in-loop-only, and the harness says so rather than reporting a misleading FAIL.
- **LLM round-trips.** Any function that calls the model cannot be exercised cold. Its full
  path is an in-loop test.
- **Model-in-loop behavior.** Whether a gate changes what the agent does is a live-loop
  question with the model in it, scheduled explicitly after wiring.
- **Import registration / boot.** Whether the agent boots with the file wired into the
  reasoning library is a separate boot test, distinct from the logic harness.

---

## 7. The standard build sequence for a new capability

One change per commit, each independently verifiable and independently rollbackable. No
piling changes together.

1. **Cold substrate harness.** Validate the new MeTTa file's functions in-container,
   inline bodies, raw-before-verdict, both polarities, logged. Discover the py-bridge
   reachability question here.
2. **Python fixtures (if the capability adds helpers).** Exercise each new Python function
   against fixtures as a standalone test before it touches the live helper file. Read the
   contracts of any existing helpers you depend on; do not assume them.
3. **Reversible apply for the helper append.** Anchor once, back up, syntax-check, reverse.
4. **Reversible apply for the loop / library wiring.** Insert the hook, rewire the
   consumer, add the import, update the wiring diagram, all-or-none, paren and line-delta
   and state checked, disk-verified, reversible.
5. **In-loop behavioral test.** After rebuild, the model-in-loop test the harness
   deliberately deferred: the live round-trip and the both-polarity behavioral fixtures.

---

## 8. Environment facts the scripts assume

- Running container is `clarity_omega`; compose service is `clarityclaw`. The evaluator is
  `/PeTTa/run.sh <file>`, run from `/PeTTa`.
- The repo is copied into the image at build, not live-mounted. Any change inside the repo
  needs `docker compose build --no-cache clarityclaw` before it is in the running
  container. Cold validation avoids the rebuild by reading the new file from the host.
- Verify and apply scripts live in `staging/` and are executed from the repo root. Paths
  are relative to the repo root.
- The container `/tmp/` maps to the host `shared_files/`, which is how log artifacts and
  combined temp files reach the host.
- Backups are written next to the file as `path.bak.<tag>`. On a failed disk verification,
  the script prints the exact restore commands.
- No em-dashes anywhere in output. Pasteable commands are chunked into the largest sensible
  single paste with `&&`, never chaining heredocs with `&&`.

---

## 9. The canonical templates

Read these against this frame. Each exemplifies part of the ethic.

- **verify_nace_substrate.py** -- the minimal harness: preflight, inline import plus file,
  raw before verdict, a Python reference for the arithmetic, unreduced-detection guidance
  in the summary. The clearest small example of hands-only checking.
- **corner_gap_pipeline_harness.py** -- the full harness: the Recorder dual log artifact,
  inline file bodies fetched from the container, the result-section and unreduced detector,
  staged probes from primitives up, seeded scenarios with references, the explicit "what
  this does not test" boundary. The template for any substrate harness.
- **capability_registry_diagnostic.py** -- the combined-input diagnostic: build one MeTTa
  input from registry plus harness, evaluate via run.sh, parse by test markers, assess with
  conservative PASS / FAIL / INSPECT, and a standing "the gap" note that survives pass or
  fail. The template for interface diagnostics.
- **apply_task_state_step2_wiring.py** -- the apply template: dry-run default, all-or-none
  across three files, code-aware paren count, anchor-exactly-once, simulate forward and
  reverse, state checks, line-delta assertion, backups, post-write disk verification, diff
  preview, the artifact_1 maintenance contract folded in, the rebuild command on success.

---

## 10. Re-alignment checklist

Before writing any verify or apply script, confirm each. A NO halts until fixed.

Harness:
- [ ] Hands only; the reference is computed in Python and used only for checking.
- [ ] Raw output prints before every verdict.
- [ ] Unreduced detection scans the result section only and handles `?`-ending names.
- [ ] Bodies are inlined; dependency bodies read from the container, the new file from the host.
- [ ] Each scenario seeds its own atoms; write-and-read in one invocation; both polarities stated.
- [ ] Preflight distinguishes substrate-wrong from substrate-absent.
- [ ] A timestamped log is written to host and container with the full raw trace per probe.
- [ ] The py-bridge / LLM / in-loop boundary is named, and bridge reachability is probed, not assumed.

Apply:
- [ ] Dry-run by default; reverse simulated and dry-run-checked beside the forward.
- [ ] Coordinated edits are all-or-none; the wiring diagram update is in the same script.
- [ ] Every anchor is verified to appear exactly once.
- [ ] Code-aware paren count, delta zero, before and after.
- [ ] Pre-state checked; line delta asserted; backup taken; disk re-verified after write.
- [ ] Diff preview printed; rebuild command printed on success.

If both lists are green, the script matches the ethic. If not, it does not, no matter how
correct the content looks.
