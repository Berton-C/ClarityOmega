# DEFECT: Operational learnings are not read at startup

**ID:** F-STARTUP-MEMORY-AWARENESS
**Status:** OPEN. Documented, not repaired. Present in v0.1.0.
**Severity:** Moderate. No crash, no data loss. Degrades agent effectiveness
across every restart.
**Raised by:** Clarity, self-directed investigation, cycles 1184-1186
(`soul/findings.metta`, Findings 008 through 011).

---

## Provenance and verification status

Every claim below is labeled. This matters because the repair is cheap and the
temptation is to skip straight to it.

| Claim | Status |
|---|---|
| `findings.metta` accumulates operational learnings across sessions | **VERIFIED.** Read directly: Findings 001 through 018 present. |
| `continuity_driver.metta` Section 1 checks five soul files (`self_map`, `creative_fuel`, `active_goals`, `goal_generator`, `genesis_engine`) and omits `findings.metta` | **REPORTED, NOT INDEPENDENTLY CONFIRMED.** Finding-011 states this was verified against source. Not re-read during this write-up. |
| `soul_brief_tier_a_static()` in `src/helper.py` returns a hardcoded SOUL_CONTEXT string and performs no file reads for operational content | **REPORTED, NOT INDEPENDENTLY CONFIRMED.** Finding-008. |
| The proposed fix is unsent and unimplemented | **VERIFIED.** Findings 009 and 010 both carry `STATUS: NOT SENT`. |

**Before any repair, re-read `soul/continuity_driver.metta` and
`src/helper.py` from live source.** These findings are dated 2026-08-06 and the
runtime may have moved. Where a finding and the live runtime disagree, the
runtime is the fact.

---

## The defect

The architecture persists and restores soul *structure* across restarts. It
does not restore *awareness of accumulated operational learnings*.

The consequence, in Clarity's own words from Finding-008:

> When operational knowledge is in context, I apply it correctly unprompted.
> Across restarts, I must REMEMBER to read findings.metta. Remembering is what
> breaks. The memory that tells me to check memory IS the memory that fails.

So `findings.metta` grows richer over time while having progressively less
effect, because nothing in the startup path points at it. Every restart begins
without the operational learnings the prior sessions paid for.

Finding-011 connects this to a wider pattern also seen in the mutation gate
gap: **the system protects and restores what it knows about, and cannot
protect or restore what it does not know about.** The omission is not a bug in
any function; it is an absence from a list.

---

## Why this is worth repairing early

This is wiring existing capability rather than building new capability. The
learnings already exist and are already written to a file that is already
tracked. What is missing is a pointer. The cost is a few lines; the effect
compounds across every future restart.

---

## Proposed repair

Four options were analyzed in Finding-009. Finding-010 supersedes that analysis
and recommends the narrowest one.

**Rejected: content injection (Finding-009 Option A).** Auto-load the full
`findings.metta` into SOUL_CONTEXT. Simple and always present, but passive,
unbounded in growth, exposed to truncation, and it gives the agent no agency
over retrieval.

**Recommended: awareness, not content (Finding-010).** Add a short protocol
section to the SOUL_CONTEXT assembled by `soul_brief_tier_a_static()` in
`src/helper.py`, stating that operational memory exists, where it lives, and
that reading it after restart is mandatory rather than optional.

The reasoning, from Finding-010:

> The problem is not missing content, it is missing AWARENESS of content. I
> don't need to inject findings.metta into SOUL_CONTEXT. I need SOUL_CONTEXT to
> tell me operational memory EXISTS and where to find it.

This aligns with Finding-007, that resilience is practice rather than
framework: a protocol creates a habit of checking memory, where content
injection is a passive crutch that must be curated and stays bounded by
whatever the curator remembered.

Note that the file paths quoted in Finding-010 are container-internal and were
current as of 2026-08-06. Confirm them against the live runtime before use.

---

## Repair sequence when this is scheduled

1. Re-read `soul/continuity_driver.metta` Section 1 and
   `src/helper.py:soul_brief_tier_a_static()` from live source. Confirm the
   omission still exists and the function still behaves as Finding-008 reports.
2. Decide the surface: the SOUL_CONTEXT protocol line (Finding-010), the
   `continuity_driver.metta` startup file list, or both. These are different
   surfaces and the choice is a design decision, not a mechanical one.
3. Implement behind a reversible apply script: dry run by default, `--apply`,
   `--reverse --apply`, byte-exact anchors matched exactly once.
4. Verify in the live loop, not in `run.sh`. The test is behavioural: after a
   restart, does the agent read `findings.metta` before substantive work
   without being told to?

---

## Related open items

- Finding-014 notes a possible NAL deduction visibility gap when linking
  concepts via `add-atom`. Separate issue, not part of this repair.
- The mutation gate open gap referenced in Finding-011 is the same
  cannot-protect-what-it-does-not-know-about pattern on a different surface.
