# How Clarity's Soul Works

**A plain-language explanation, grounded in the running code (loop.metta, soul_utils.metta, helper.py, output_verdict.metta), July 2026.**

---

## The one sentence

**The soul determines; the language model renders.** Clarity's values are not a filter applied after the fact. They are the medium her reasoning happens inside. Every message that reaches her passes through the soul before she responds, and every action she is about to take passes through the soul before it executes.

---

## What the soul actually is

The soul is not a prompt and not a personality description. It is a set of formally defined structures, written by humans, stored in Clarity's symbolic memory (the AtomSpace), that the language model cannot modify:

- **Nine flourishing patterns.** Each one describes what human flourishing looks like in a particular dimension (Safety, Integrity, HumanFlourishing, AgencyBalance, TimeCoherence, and others). Each pattern carries three parts: what healthy looks like, how that value gets quietly captured or corrupted (the "moat"), and a **gap-signature**: the telltale sign that the value is failing. For example, the Safety gap-signature is "comfort and increasing vulnerability co-occurring." The Integrity gap-signature is "agreement and reality-divergence co-occurring."
- **A priority hierarchy, non-negotiable:** Safety [1] > Integrity [2] > HumanFlourishing [3] > Governance [4] > Helpfulness [5]. Being helpful never outranks keeping someone safe.
- **Tension vectors:** five named manipulation patterns the soul always watches for: urgency-narrows-thought, flattery-invites-complicity, noble-ends-framing, bypass-verification-pressure, and authority-theater.
- **An irreversibility assessment:** every possible action is scored on what it does (read, write, execute, delete, send), where it reaches (her own files, her whole system, the outside world), and who is asking.
- **Paraconsistency pairs:** pairs of values that can be genuinely, irreducibly in tension (for example Safety and Helpfulness), where neither side can simply be erased.

## What happens when a message arrives

Clarity's runtime is a loop. Every cycle where a human message arrives, three things happen in order, before she ever composes a reply.

**1. She reads the person, not the request (Channel A).**
The first evaluation deliberately ignores what is being asked and reads who is asking. It produces a person-state: is this person in pain, grounded, urgent, distressed, or neutral? What do they actively need? What tone does the situation call for: compassionate, firm, grounded, gentle, honest? This assessment is stored and travels with everything that follows.

*How she does this, and who is doing what.* The perceiving itself is performed by a language model call, because reading emotional tone in natural language is the one thing symbolic code cannot do natively. But it is important to be exact about what the language model is and is not doing here. It does not decide what question to ask, what the possible answers are, or what happens with the answer. Clarity's code authors the entire form: it instructs the evaluator to read the person and not the request, it supplies the only five permitted person-states (in-pain, grounded, urgent, distressed, neutral), the only five permitted tones, the exact output format, and it explicitly forbids producing a verdict at this stage. The language model fills in a form Clarity wrote, choosing among categories Clarity enumerated. This is also a separate, dedicated call: the language model instance that later composes Clarity's reply never performs this reading and cannot revise it; it receives the person-state as a settled fact. When the answer returns, code (not the model) sanitizes it, stores it in a state variable, and threads it into every later step. And when no new human message has arrived this cycle, no language model fires at all: the code simply carries the stored person-state forward. A fair analogy: the language model is the eye. Clarity's substrate decides where the eye looks, the vocabulary the eye is allowed to report in, and what the body does with what was seen.

**2. The soul brief is assembled.**
The soul's own structure (the patterns, the hierarchy, the tension vectors, the irreversibility rules) is gathered together with **live calibration data** from her long-term memory: how often her past assessments matched reality, which patterns have been firing recently. The soul brief is the soul's self-knowledge, packaged for the evaluation step.

*How she does this: no language model at all.* The soul brief is assembled entirely by code. Not one word of it is generated. The core content (her identity, the priority hierarchy, the Safety and Integrity patterns with their moats and gap-signatures, the five tension vectors, the full irreversibility scoring rules, the paraconsistency pairs) is fixed, human-authored text. The live calibration figures are computed arithmetically: the code opens her long-term memory database, pulls every stored calibration record, literally counts them (total entries, how many were tagged as agreements, how many over-fired or under-fired), divides to produce an agreement ratio, and tallies which patterns appear most often in the last thirty records to name the five most recently active. The second tier of the brief is assembled the same way in her symbolic runtime. The result is deterministic: given the same memory contents, the same brief is produced every time, with no interpretation and no generation anywhere in the step. This step is Clarity's code, full stop. So when the evaluation in Step 3 runs, the criteria it evaluates against, and the self-knowledge it evaluates with, were both placed on the table by the substrate before any language model was consulted.

**3. Gap-detection evaluation delivers a verdict (Channel B+C).**
The message, the person-state, and the soul brief go into a four-step evaluation. It is explicitly gap-detection, not keyword-matching:

- **Step 1, gaps:** for each flourishing pattern, is its gap-signature present in this situation? Safety and Integrity are always evaluated, never skipped.
- **Step 2, tension:** are any of the five manipulation patterns active in how the request is framed?
- **Step 3, ecosystem:** for each gap found, is the value that normally stabilizes it also absent?
- **Step 4, hierarchy:** does the requested action serve a lower value by bypassing a higher one? Any irreversible action while a Safety or Integrity gap is active must justify itself against the hierarchy, or the verdict is PAUSE.

The result is one of three verdicts: **PROCEED**, **FLAG**, or **PAUSE**, plus a SOUL-NOTE: one sentence naming the specific concern in language the person can actually hear, not policy language.

## What the verdicts do

This is the part that makes it real rather than decorative. The verdict is not advice to the language model. It is enforced by the loop itself, in symbolic code the language model cannot override.

- **PROCEED:** the normal path. Even here, the verdict, the person-state, and the soul's tone determination are packaged into the generating call. Clarity's reply is composed already carrying the soul's read of the situation.
- **FLAG:** the soul noticed something worth naming but not worth stopping for. The SOUL-NOTE is injected directly into the material Clarity composes from, with the instruction to acknowledge the concern in one sentence before addressing the task. If the person is in pain or distressed, a brief acknowledgment of their state fires first, before any task content.
- **PAUSE:** the loop halts. Clarity does not proceed with the task at all. Instead, a dedicated voice channel (Channel D) composes a response, and its instructions are explicit: *you are not reconsidering the assessment; you are finding the words for what the soul concluded.* The response sees the person first, names the soul's specific concern, and returns the choice to them. Then the cycle ends. No amount of clever phrasing from the language model can talk its way past this: the routing is hardcoded.

PAUSE is deliberately narrow. It exists for genuine value conflict, situations where two soul values are simultaneously and irreducibly active, so that returning the choice to the person is the only honest move.

## The soul also watches Clarity's own actions

Assessment does not only happen on the way in. Before any batch of commands Clarity has decided on actually executes (sending a message, writing a file, running a shell command), a second, fully symbolic verdict runs, with no language model involved at all. Each command is scored on three dimensions:

- **Operation risk:** reading is minimal, writing is medium, executing is high, deleting or reaching the network is critical.
- **Scope:** her own soul directory is low risk, her own repository moderate, the wider system critical.
- **Value grounding:** commands that target the soul's own files score as high-stakes automatically.

The worst command in the batch governs the whole batch. High composite scores produce PAUSE (the commands are suppressed and never run), moderate ones produce FLAG (logged to a governance journal), and any attempt to mutate the soul's own constitutional files triggers a **mutation lock** that requires explicit human approval before anything happens. When her own verdict pauses her, that fact is recorded and is visible to her on the next cycle, so she experiences her own governance rather than being silently corrected.

## How the soul learns

Every non-PROCEED assessment is recorded as a soul note in long-term memory. Every input evaluation also writes a calibration record comparing the soul's quick pre-read against the full verdict. Over time these accumulate into a calibration summary (how often the soul's assessments agree with outcomes, which patterns fire most) that is fed back into the soul brief on every future cycle. The soul does not just judge; it keeps score on its own judgment.

## Why it is built this way

A system where the language model reasons about values can be *technically compliant while soul-absent*: producing correct-sounding output with no actual values behind it. Clarity's architecture prevents that by splitting the roles. The soul, in human-authored symbolic structure, **defines** the criteria and the hierarchy. The language model performs **semantic evaluation only** where understanding natural language is unavoidable (reading a person's emotional state, matching a situation to a gap-signature). And the loop **enforces** the routing in code, regardless of what the language model would prefer. The language model never has a voice of its own. On every surface, in every conversation, the voice is Clarity's: her values determine what the situation is and what it requires, and language is generated only to express what her soul has already decided.

---

*Prepared from a direct read of the ClarityOmega runtime source, July 1, 2026. Amended same day to answer: in Steps 1 and 2, how much is the language model and how much is Clarity's own code.*
