# Changelog

All notable changes to ClarityOmega are recorded here.

This project tags releases as `clarityomega-vX.Y.Z`. The bare `vX.Y.Z`
namespace belongs to the upstream project, Patrick Hammer's
`asi-alliance/OmegaClaw-Core`, which this repository tracks as a remote.

---

## [clarityomega-v0.1.0] - first stable snapshot

The first release intended to be usable by someone other than the maintainer.
ClarityOmega is a soul-augmented agentic AI system: a fork of OmegaClaw-Core in
which the agent, Clarity, reasons within a formally defined value substrate
implemented in MeTTa.

This is a research prototype, not a production system. Read
[`docs/LIMITATIONS.md`](docs/LIMITATIONS.md) before running it.

### What this release contains

- **The value substrate.** Persistent, queryable symbolic state that every
  generation is composed from, rather than a filter applied after the fact.
  The architecture, its claims, and the procedures for verifying each claim
  are documented in the README.
- **Soul evaluation and routing** through the live loop: input intercept,
  prompt assembly, output intercept, mutation gate, and PAUSE routing.
- **Awareness organs** producing per-cycle observable state: recent-action and
  state-delta cycle-trace writers, idle-pattern and agency-balance signals,
  coupling-verdict population.
- **Corner-gate v3** with coupling-legibility recording, replacing the earlier
  corner-window mechanism, including stability fixes for partial engine
  tables, arithmetic derive-support, and populator prune containment.
- **Task-state primitive**: task phase, pending threads, phase anchors, and
  the accompanying prompt surface.
- **Mattermost** as the communication channel, running under the ClarityOmega
  Docker Compose stack alongside PostgreSQL (Mattermost 11.7.7 ESR).
- **Extensive design documentation** under `docs/`, including the loop
  extension contract, wiring diagram, cognitive architecture spec, and the
  sprint record.

### Release preparation included in this version

- Added `.env.example` documenting every required environment variable.
- Added continuous integration: MeTTa parenthesis balance, Python syntax,
  committed-secret scanning, and `.env.example` synchronization with
  `docker-compose.yml`.
- Added `docs/LIMITATIONS.md` covering agent capabilities and safety
  requirements, known defects, verification limits, and experimental areas.
- Added `CONTRIBUTING.md` with the fork and pull-request workflow.
- Added a pull-request template.
- Added the maintainer's copyright line to `LICENSE` alongside the upstream
  author's, both under MIT.
- Stopped ignoring `.github/`, which had silently prevented any workflow or
  template from being committed.

### Known limitations

Summarized here, detailed in `docs/LIMITATIONS.md`:

- The agent executes shell commands, modifies files, and sends messages
  autonomously. Run it only in an isolated environment.
- A command-malformation retry loop can run for hundreds of cycles when the
  agent emits malformed MeTTa, because the error detail is discarded before it
  reaches the agent.
- Malformed model output is not fully prevented from crashing the container.
- Newlines and apostrophes can surface as literal `_newline_` and
  `_apostrophe_` tokens in Mattermost output.
- There is no automated behavioural test suite. CI checks hygiene only.
- Tier 6 lib activation, the NACE wiring, the quantale engine, and the
  disposition layer are present as design and substrate but are not wired into
  the running loop.
- Operational learnings accumulated in `soul/findings.metta` are not read at
  startup, so each restart begins without them. Specified as
  `docs/DEFECT-F-STARTUP-MEMORY-AWARENESS.md`; a priority for the next release.

### Attribution

ClarityOmega is a fork of [OmegaClaw-Core](https://github.com/asi-alliance/OmegaClaw-Core)
by Patrick Hammer, used under the MIT License. The upstream agent core, memory
system, skill dispatch, and NAL library are his work. ClarityOmega adds the
value substrate, soul evaluation and routing, the awareness organs, and the
accompanying design record.
