# ClarityOmega Project Knowledge Index

This file is the entry point for project knowledge. When opening a new working session, read this first to orient. The index lists what exists, where it lives, and what state it is in.

**Last updated:** 2026-05-10

---

## Project Identity

**ClarityOmega** is a soul-augmented AI agent. Repo: `github.com/Berton-C/clarityclaw` (mid-migration to OmegaClaw upstream at `github.com/asi-alliance/OmegaClaw-Core`). CLI: `clarityomega`. Connected to Mattermost. Runs on PeTTa/MeTTa runtime in Docker container `clarity_omega`.

Older names (ClarityClaw, MeTTaClaw fork) are historical. Naming cleanup pass across docs is on the backlog.

---

## Docs Tree at a Glance

```
docs/
├── decisions/          ADRs (forward-looking architectural decisions)
├── design/             Control documents (artifacts 1-7) + Sprint knowledge
├── investigations/     Diagnostic work products (this is where backward-looking findings live)
├── hyperseed_docs/     Active development resources for MeTTa reasoning capacity
├── hyperseed_sections/ Active development resources, sectioned reference
├── merging/            STALE - was planned for upstream merge, needs revisit
├── INDEX.md            This file
└── (root-level files)
```

`docs/old/` was moved to `staging/OLD/OLD_docs_files/` on 2026-05-10 and is no longer in the docs tree.

---

## Investigations

Investigations are diagnostic work products. Each has a tag at the conclusion commit, a doc with findings, and a status. Findings are status-tracked: OPEN, VERIFIED, RESOLVED, REJECTED, DEFERRED.

| Tag | Doc | Status |
|-----|-----|--------|
| `investigation-2026-05-10-spam-behavioral` | `docs/investigations/2026-05-10-spam-behavioral.md` | CONCLUDED, fix work in progress |

### Open Findings (Across All Investigations)

| Finding ID | Investigation | Status | Priority |
|------------|--------------|--------|----------|
| F-HISTORY-CONTAMINATION | 2026-05-10-spam-behavioral | VERIFIED | 1 |
| F-PREVMSG-STALE | 2026-05-10-spam-behavioral | VERIFIED | 2 (pairs with #8) |
| F-CONVERSATION-BOUNDARY | 2026-05-10-spam-behavioral | VERIFIED | 3 (likely subsumed by #1) |
| F-OUTPUT-FORMAT-NO-SILENCE | 2026-05-10-spam-behavioral | VERIFIED | 4 |
| F-DIRECTIVE-CONTEXT-STALE | 2026-05-10-spam-behavioral | VERIFIED | 5 |
| F-SEND-FILTER-NARROW | 2026-05-10-spam-behavioral | VERIFIED | 6 (conditional) |
| F-RECENT-ACTION-FRAMING | 2026-05-10-spam-behavioral | OPEN | 7 |
| F-ALIVENESS-PERMISSIVE | 2026-05-10-spam-behavioral | RESOLVED via reframing, fix pending | 8 (pairs with #2) |
| F-LAYER-1-OPTION-SET | 2026-05-10-spam-behavioral | VERIFIED | 9 |
| F-SOVEREIGNTY-AUDIT | 2026-05-10-spam-behavioral | DEFERRED | 10 |

### Historical Investigation Knowledge (in docs/investigations/, do not update)

These predate the investigation lifecycle convention. They contain real knowledge that may not yet be captured in current docs or code. **Knowledge audit pending** — see Backlog.

- `ClarityClaw_OmegaClaw_Merge_Checklist.md`
- `ClarityClaw_OmegaClaw_Migration_Knowledge.md`
- `ClarityClaw_Stage5_Integration_Knowledge.md`

---

## Architectural Decisions (ADRs)

| ADR | Title | Status | Note |
|-----|-------|--------|------|
| ADR-003 | Communication Channel — IRC for Phase 1 | Decided April 2026 | May be outdated; live system is on Mattermost. Reconciliation pending. |
| ADR-004 | Phase 2 Anthropic SDK Migration via LiteLLM | Planned, not yet active | OpenAI embeddings remain hardcoded |

ADRs are in `docs/decisions/`. ADR-001 and ADR-002 not found in current tree.

---

## Design / Control Documents

These artifacts are the authoritative control documents for the project going forward. Massive knowledge base, guides all development decisions.

Located in `docs/design/`:

- `artifact_1_loop_metta_wiring_diagram.md` — Loop wiring reference
- `artifact_2_hooks_piggybacks.md` — Hook and piggyback points
- `artifact_3_growth_surface.md` — Growth surface specification
- `artifact_4_ClarityOmega_Triple_Network_Scaffold_v1_1.md` — Triple network scaffold
- `artifact_5_ClarityOmega_Cognitive_Architecture_Spec_v3_0.md` — Cognitive architecture spec (175k chars, largest)
- `artifact_6_Hyperseed_Formalization_Catalog_v1_1.md` — Hyperseed formalization
- `artifact_7_Hyperseed_to_Network_Synergy_Map_v1_1.md` — Hyperseed-to-network synergy
- `ClarityClaw_Sprint_3_Knowledge.md` — Sprint 3 working knowledge

**Knowledge audit pending** — verify what unique knowledge in artifacts is or is not already represented in current code, ADRs, atom base, and investigation findings. See Backlog.

### Session-produced docs (to be moved to investigations/)

These currently live in `docs/design/` but belong in `docs/investigations/` per the investigation lifecycle convention:

- `ClarityOmega_Behavioral_Investigation_Knowledge.md` — Superseded by `2026-05-10-spam-behavioral.md`
- `ClarityOmega_Sprint_4_Output_Verdict.md` — Sprint 4 investigation closeout
- `ClarityOmega_Substrate_Crash_Knowledge.md` — Substrate crash mechanism investigation

(Move pending; see pasteable commands below.)

---

## Development Resources

Active reference material used to build new MeTTa reasoning capacity:

- `docs/hyperseed_docs/` — Hyperseed development docs
- `docs/hyperseed_sections/` — Hyperseed sectioned reference (34 files)

Not yet indexed in detail. Consult directly during development work.

---

## Sprint State

| Sprint | Status | Notes |
|--------|--------|-------|
| Sprint 1.5 | COMPLETE | Behavioral guidance stubs, output-format-guidance, self-check-guidance |
| Sprint 2 | COMPLETE | Mutation gate dead-code cleanup |
| Sprint 3 | COMPLETE | Recent-action populator and retriever; cycle classifier |
| Sprint 4 | COMPLETE | Status banner unblocked, GLM-Switch C10 fix, output verdict 5c remains stubbed |
| Housecleaning pause | IN PROGRESS | Spam-behavioral investigation closeout, fix work, structural cleanup |
| Sprint 5 | NOT STARTED | Output verdict 5c real implementation; further architectural work |

---

## Known Tags (Anchored Repo States)

| Tag | Significance |
|-----|--------------|
| `v1-pre-omegaclaw` | Pre-migration anchor |
| `v1-post-collapse-eval-fix` | Mechanism 3 substrate crash resolution (commit `d9d5b25`) |
| `investigation-2026-05-10-spam-behavioral` | Spam behavioral investigation conclusion |

---

## Working Conventions

**Investigation lifecycle.**
1. Hypothesis charter, source-grounded
2. Empirical work, status-tracked findings
3. Source trace verification before locking conclusions
4. Investigation doc written to `docs/investigations/<date>-<topic>.md`
5. Tag at conclusion commit: `investigation-<date>-<topic>`
6. INDEX.md updated

**Fix work lifecycle.**
1. Branch from `main`: `fix/<finding-id>-<short-name>`
2. Commit messages reference finding ID: `[<investigation-date>] <finding-id> RESOLVED: <description>`
3. Investigation doc updated, finding status changed
4. INDEX.md updated

**Source-first hypothesizing.** Read source before claiming architectural absence or presence. Verify-before-claim, especially when describing absences.

**Reasoning sovereignty as guiding principle.** Python is hands. MeTTa is mind. Prefer MeTTa-side reasoning over Python-side decision-making. Helpers exist for what cannot be done in MeTTa due to runtime constraints (PeTTa C1-C9), not because Python is convenient.

**Clarity at the table for in-container work and MeTTa fixes.** Documentation governance is Berton-and-Claude until her cognitive load is reduced. Present findings and proposed fixes as discrete asks. Soul evaluator catches attribution-anchor pressure — anchor on substance, not authorship.

**No em dashes** anywhere in any project text or document.

---

## Backlog

- Knowledge audit of design artifacts and historical investigations: identify unique knowledge not yet in current docs, code, ADRs, or atom base. Carry forward unique content. Archive redundant content to staging.
- Naming cleanup pass across docs (ClarityClaw → ClarityOmega).
- ADR-003 reconciliation: document current Mattermost channel state (new ADR or update).
- `docs/merging/` revisit when upstream merge is reconsidered.
- Move three session-produced docs from `docs/design/` to `docs/investigations/`.
- Output verdict 5c (loop.metta:119) real implementation, deferred to Sprint 5 or fix sequence.
