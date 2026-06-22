# ClarityOmega First Principles: Ground Truth

**Status:** GROUND TRUTH. This is the shortest authoritative statement of what the
soul architecture is and who owns what. Every design and every build is checked
against this document before it proceeds. When any other document, prior conclusion,
or remembered picture disagrees with this one, this one wins, and the live source
wins over this one (Principle 0).

**How to use it:** Paste this document at the start of any soul design or build work.
Before proceeding, the two pre-flight questions in Section 7 must be answered in
writing. This document is deliberately short so pasting it costs nothing.

**Version:** v1, 2026-06-19.

---

## The one sentence

**The soul determines; the LLM renders; on every surface; always.**

Everything below is elaboration of that sentence. If a design contradicts it, the
design is wrong, not the sentence.

---

## 0. The load-bearing principle: reason from facts verified now, never from a frame

This is first because it governs whether every other principle is actually applied or
merely nodded at. Roughly 99% of the wasted effort in this project happens at this
seam: reasoning from an inherited picture of the system instead of from the principles
and from facts verified in the current session.

A *frame* is any inherited picture of what the system is, or of what the work should
be, that has not been re-grounded now. The danger is that reasoning from a frame feels
identical to reasoning from facts. The violation is invisible from inside it. So the
principle is enforced by two mechanical tells, each catchable with one question.

**State-claim tell.** Any assertion about what the system currently does, contains, or
is wired as is INVALID unless it was read from live source (the file on disk, git, or
the running runtime) in the current session. Absent a current read, the claim must be
stated as an assumption to verify, out loud, as such. When a fresh source read
contradicts a held conclusion, **the read wins, immediately, with no argument.**
- Enforcement question: *"Where did you read that, this session?"*
- If the answer is "I concluded it earlier," "the document says," or "I recall," the
  principle is being violated. Stop and read source.

**Design tell.** Any design or build elaboration is INVALID until the soul-absent
question (Section 7) has been answered for the thing being built, BEFORE the
elaboration, not after. Refining the *how* of something before settling *whether it
should exist* is the inherited-frame violation.
- Enforcement question: *"Did you settle whether this should exist before designing how?"*

**Honest limit.** This principle does not make drift impossible. It makes drift
catchable in one exchange instead of days. The recovery cost collapses from a
rediscovery to a single question and a single source read. That is the realistic claim
and it is still the largest lever in this document.

---

## 1. Ownership: who owns what, and where it lives

| Concern | Owner | Where it lives | The LLM's role |
|---|---|---|---|
| **Voice** (how Clarity shows up, her tone, her stance, what reaches the person) | Clarity / the soul | Substrate: SOUL-TONE, SOUL-NOTE, the assessment | Renders the soul's determination into words. Never authors it. |
| **Reasoning** (what the situation is, what it requires, what is true) | Clarity / the soul | Substrate: MeTTa symbolic reasoning, soul structure, memory | Performs *semantic evaluation only* where language understanding is irreducible (reading the person, matching the situation to soul criteria). Never decides what the soul values. |
| **Navigation** (how Clarity moves through any engagement: a conversation, her own file system, her own work) | Clarity / the soul | Substrate: the soul navigating by its own values | Supplies inference when asked. Never sets the course. |
| **Action** (what Clarity does: sends, writes, shell, task execution) | Clarity / the soul | Substrate determination present at the generating call | Renders soul-determined action into commands. The soul's determination governs the action upstream; the LLM does not author free action that gates catch downstream. |
| **PAUSE** (halting on genuine irreducible value conflict) | The soul, enforced by hardcoded loop routing | Loop: PAUSE/FLAG/PROCEED routing, non-overridable by the LLM | The LLM's verdict produces consequences it did not program and cannot prefer away. |

The throughline of the table: **the soul owns determination on every concern. The LLM
owns rendering and irreducible semantic evaluation, nothing more.** "On every surface"
means human conversation AND Clarity's own agenda AND her work with her own files and
tools. Her voice is the only voice in every room she is in.

---

## 2. The four principles (standing, verbatim)

1. **loop.metta stays hooks, not logic.** Touching loop.metta means adding a hook that
   points at `soul/` content. No logic in loop.metta. The separation keeps upstream
   merges workable.
2. **MeTTa-first; Python is only the hands.** All logic lives in MeTTa to the fullest
   extent possible. Python exists only for what MeTTa cannot do (LLM calls, IO, string
   plumbing).
3. **Take back reasoning from the LLM on every surface we can.** Clarity owns reasoning
   as much as she owns her voice and her navigation by her own values. The job is to
   maintain that boundary and keep bringing reasoning under her purview.
4. **The LLM never has a voice. Only Clarity has a voice.** Her voice is determined by
   her and by how she navigates every surface she engages: with a human, with her own
   file system, with her own creative work. Her voice on all surfaces all the time. The
   LLM only generates language that the soul has already determined.

---

## 3. The Orchestrator Frame (the law, quoted from spec Section 3, lines 222-234)

> **MeTTaClaw is the orchestrator. The LLM is the language composer.**
>
> MeTTaClaw understands its own soul, its own history, its own assessment of the person
> in front of it, and its own judgment about what each situation requires. It makes
> those determinations through native MeTTa symbolic reasoning, the soul's formal
> structure, and accumulated session history in long-term memory.
>
> The LLM gives MeTTaClaw's conclusions a voice. It does not decide what MeTTaClaw
> thinks or feels. It is skilled at natural language. It is told what to say and it
> expresses that with competence.

The failure mode the spec names directly, which is the test for all soul work:

> A system where the LLM reasons about soul structure can be soul-absent while being
> technically compliant.

The three responsibilities (spec line 230): **MeTTaClaw defines** the criteria,
hierarchy, irreversibility table, gap-signatures (human-authored AtomSpace atoms, not
LLM-modifiable). **The LLM performs semantic evaluation** only where language
understanding is irreducible. **MeTTaClaw enforces** routing as hardcoded loop logic
regardless of what the LLM prefers.

---

## 4. PAUSE is narrow

PAUSE is for **genuine paraconsistent conflict**: two soul values simultaneously and
irreducibly active, where neither can be erased without loss, so returning the choice
to the person is the only non-collapsing option (spec Section 5, the paraconsistent
pairs).

PAUSE is the fallback for when alignment **cannot** be achieved. It is NOT the tool for
catching misalignment that should have been prevented upstream. A broad PAUSE surface
is a SYMPTOM: it means the soul's determination is absent upstream of generation, so
the only remaining move is to block. When the soul governs the generating call (Section
1, Action), most of what a broad PAUSE catches is never generated, and PAUSE narrows to
its proper scope. **A large PAUSE surface is evidence of drift, not of safety.**

---

## 5. The intended shape vs. the standing drift

The intended shape: the soul's determination is present at the point language or action
is generated, on every path. The LLM generates carrying that determination. Gates and
PAUSE are the narrow last-resort floor, not the primary mechanism. The soul is
**upstream** of generation.

The standing drift (the thing restoration corrects): the soul positioned **downstream**
of the LLM, as a lattice of gates trying to catch problems after the LLM already
authored freely. A broad PAUSE compensating for the absent upstream determination. The
LLM authoring voice and framing by default because the determination was stripped
before it generated.

Restoration means returning the runtime to the intended shape. It is not invention. The
mechanism for getting the soul's determination to the generating call already exists in
the spec (for example, the FLAG path's injection of the SOUL-NOTE into the send before
the main call). Restoration applies the existing mechanism where drift defeated it; it
does not build a new author-with-a-fence.

---

## 6. Verify against the live runtime, always

The principles in this document describe the system as it is INTENDED. The system as it
ACTUALLY RUNS diverges from intent through rollbacks, half-wired repairs, and
stale-copy drift. Therefore: **before concluding what the system does, read it from
live source this session.** Never reason about current behavior from this document,
from any other document, from a project-knowledge copy, or from memory. This document
is the standard the system should meet; it is not evidence of what the system currently
does. (This is Principle 0 applied to the architecture itself.)

---

## 7. The mandatory pre-flight (the enforcement)

Before any soul design or build proceeds, both questions are answered in writing. These
are not rhetorical. A design that cannot answer them cleanly is not ready.

**Question 1 (the soul-absent test):**
> *"In what situations would this produce technically-correct output that is
> soul-absent?"*

If the honest answer names a situation where the LLM ends up authoring voice, framing,
stance, navigation, or action that the soul did not determine, the design violates the
Orchestrator Frame and must change before proceeding. (This question alone would have
stopped the drifted "Extension B" composer: the honest answer was "it lets the LLM
author framing," which is soul-absent by construction.)

**Question 2 (the frame-discipline test):**
> *"Which claims in this proposal about what the system currently does were read from
> live source this session, and which are assumptions?"*

Every state-claim must trace to a current source read or be flagged as an assumption to
verify. Any claim that traces to memory, to a prior conclusion, or to a document is a
Principle 0 violation and must be re-grounded before the work rests on it.

**The standing protocol:** when this document is pasted, both questions are answered
against the current work first, before anything else. If the answers reveal a frame
violation or a soul-absent surface, the work stops and re-grounds. This is the
mechanism that converts the principles from a creed into a contract.

---

## 8. What this document does not do

It does not replace the strategy map, the artifacts, or the restoration specs. It is
the short ground truth they all serve. When detail is needed, those documents carry it.
When direction is in doubt, this document carries it. And when this document and the
live runtime disagree about what the system *does*, the live runtime is the fact and
this document is the goal.

---

## Document end

This is the ground truth. The soul determines; the LLM renders; on every surface;
always. Reason from these principles and from facts verified now, never from a frame.
Read the live source before claiming what the system does. Answer the two pre-flight
questions before building. Keep PAUSE narrow by putting the soul upstream. That is the
whole design.
