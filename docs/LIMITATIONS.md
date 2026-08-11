# ClarityOmega: Limitations, Safety Notes, and Experimental Areas

**Applies to:** ClarityOmega v0.1.0
**Status:** Read this before running the agent.

ClarityOmega is a working research prototype, not a production system. This
document states plainly what is unfinished, what is experimental, and what can
go wrong. Where this document and the live runtime disagree, the live runtime
is the fact.

---

## 1. Safety: what this agent can actually do

ClarityOmega is an autonomous agent that runs continuously and acts without
per-action human approval. Within its container it can:

- **execute operating system shell commands**
- **read, write, and modify files**
- **perform web searches and fetch remote content**
- **send messages autonomously** to its configured Mattermost channel
- **call an external LLM provider** with the content of its working context

The value substrate governs *what the agent determines to do*. It is not an
operating-system sandbox and does not constrain what the container itself is
permitted to reach.

**Run it in an isolated environment.** The reference deployment is Docker
Compose on a single machine. Do not run ClarityOmega with host filesystem
mounts you care about, on a machine holding credentials for other systems, or
with network access to infrastructure you would not hand to an autonomous
process.

### Credentials and network exposure

- Provider API keys are supplied through `.env` and are visible to the agent
  process. Use keys scoped to this project, with spend limits set.
- The bundled PostgreSQL service falls back to the password
  `mmuser_password` when `POSTGRES_PASSWORD` is unset. This is safe only for a
  strictly local deployment with no published ports. Set a real password
  before running anywhere reachable from another machine.
- Conversation content, including anything in the agent's working context, is
  transmitted to whichever LLM provider you configure.

---

## 2. Known defects present in v0.1.0

These are documented rather than fixed. Each is reproducible.

**Command-malformation retry loop.** When the agent emits malformed MeTTa, the
error surfaced back to it is a generic constant (`SINGLE_COMMAND_FORMAT_ERROR`
/ `MULTI_COMMAND_FAILURE`) with the underlying detail discarded. Lacking any
actionable signal, the agent rationally retries. Loops of 290 to 900+ cycles
have been observed. This is a feedback-channel defect, not a reasoning defect.
Mitigation in place: the `wrap_if_bare_command` safety net handles the
bare-single-command case.

**Container crash from malformed model output is not fully excluded.** A
`(catch (sread $response))` guard provides partial protection. A dedicated
parse-path crash guard is specified but not confirmed present. A safety-relevant
agent loop should be unable to crash its host by emitting a bad string; that
property is not yet guaranteed. Treat container restarts as expected.

**Operational learnings are not read at startup.** The agent accumulates
operational learnings in `soul/findings.metta` across sessions. The startup
protocol restores soul *structure* but does not point the agent at that file,
so each restart begins without learnings that earlier sessions paid for. The
agent's own account of it: "The memory that tells me to check memory IS the
memory that fails." A narrow repair is specified in
[`DEFECT-F-STARTUP-MEMORY-AWARENESS.md`](DEFECT-F-STARTUP-MEMORY-AWARENESS.md)
and is not applied in v0.1.0. This wires existing capability rather than
building new capability, and is a priority for the next release.

**String encode/decode asymmetry.** `string-safe` encodes three tokens
(double quote, newline, apostrophe); the live `balance_parentheses` reverses
only the double quote. Newlines and apostrophes can therefore surface in
Mattermost as literal `_newline_` / `_apostrophe_` tokens. Keep emitted strings
ASCII-safe. This is deliberately not patched in v0.1.0: `string-safe` is also
the crash-safe marshalling boundary, and changing it risks reintroducing a
marshalling crash. It is a separate, root-cause-first workstream.

**NAL derivations do not persist.** `|-nal` computes correct derivations and
stores nothing; only an explicit `add-atom` commits a result. The `|-nal`
operator reduces **only inside the live loop process**, never in standalone
`run.sh` invocations.

---

## 3. Verification and testing limits

**There is no meaningful automated behavioural test suite.** Soul evaluation,
NAL reduction, and quantale composition reduce only inside the running loop
process with its full AtomSpace loaded. They cannot be exercised in CI, and a
standalone `run.sh` invocation starts an empty AtomSpace and is **not**
equivalent to the live runtime.

Continuous integration therefore checks hygiene only: MeTTa parenthesis
balance, Python syntax, absence of committed secrets, and `.env.example`
staying in sync with `docker-compose.yml`. **A green CI run says nothing about
whether the agent behaves correctly.**

Real verification in this project is live-loop probing, differential comparison,
and reading container logs as ground truth.

---

## 4. Experimental and incomplete areas

Present in the repository, not part of what v0.1.0 claims to deliver:

- **Tier 6 lib activation.** `substrate_kb`, `lib_self_continuity`, and the
  `nace_*` substrate are imported and reducible but have no per-cycle caller.
  They are loaded and uncalled: capability that exists as data, not behaviour.
- **The quantale autopoietic epistemic engine.** Extensive design and
  validation work under `docs/sprints/03_quantale_autopoietic_epistemic_engine/`.
  Research artifacts, including superseded versions under `stale/`.
- **NACE capability-efficacy learning.** Substrate built and verified; wiring
  (import lines, writer, loop hook, dispatch gate) not landed.
- **The disposition layer.** Continuity measurement and pfn snapshots are
  specified and gated on an unresolved design question.
- **`staging/`.** Working scratch: apply scripts, diagnostics, probes, and
  logs from development. Retained for provenance. Not part of the supported
  surface and not required to run the system.

---

## 5. Operational notes

- **Docker layer caching is a persistent trap.** Any change inside the cloned
  repo requires `docker compose build --no-cache`.
- **The live container is ground truth.** `docker run --rm <image>` reads the
  baked image copy, not what the live container executes. Use
  `docker exec <container>` to reach the running runtime.
- **Runtime state accumulates** under `volumes/` and in ChromaDB. A fresh
  clone starts from seed state, not from any prior agent's history.
