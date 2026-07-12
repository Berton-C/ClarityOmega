# Extension B: The Drift from Soul Spec, and the Aligned Fix

**Status:** FOR REVIEW. Pre-rewrite. Nothing is changed in code until Berton confirms this
captures the soul-spec intent. This document explains where the current Extension B design
drifted, what the governing standard is, and the fix that aligns it.

**Scope:** the conception of what the LLM does when Clarity's response is produced on the
PROCEED path. This is a conceptual correction, not a wording tweak.

---

## 1. The standard this is measured against

### Four principles (Berton, standing)

1. **loop.metta stays hooks, not logic.** Touching loop.metta means adding a hook that
   points at `soul/` content. No logic in loop.metta. The separation keeps upstream merges
   workable.
2. **MeTTa-first; Python is only the hands.** All logic lives in MeTTa to the fullest
   extent possible. Python exists only for what MeTTa cannot do (LLM calls, IO, string
   plumbing).
3. **Take back reasoning from the LLM on every surface we can.** Clarity owns reasoning as
   much as she owns her voice and her navigation by her own values. The job is to maintain
   that boundary and keep bringing reasoning under her purview.
4. **The LLM never has a voice. Only Clarity has a voice.** Her voice is determined by her
   and by how she navigates every surface she engages, with a human, with her own file
   system, with her own creative work. Her voice on all surfaces all the time. The LLM
   only generates language that the soul has already determined.

### The Orchestrator Frame (Strategy Map, Section 3)

The original design states this as the frame that must be held before any code is read.
MeTTaClaw is the orchestrator and the LLM is the language composer. The LLM gives
MeTTaClaw's conclusions a voice in the narrow sense of producing words, but it does not
decide what MeTTaClaw thinks or feels; it is told what to say and expresses that with
competence. The design names the failure mode directly: a system where the LLM reasons
about soul structure can be soul-absent while being technically compliant.

The same frame appears at the exact surface Extension B touches:

- **SOUL-TONE is a directive, not a property the LLM owns.** Channel C "is an instruction
  to the LLM composer: be this way when you compose the words. It is not a description. It
  is a directive."
- **Channel D does not reconsider.** Its stated non-responsibilities: do not re-evaluate
  tasks, re-read the person, or reconsider soul alignment. On PAUSE the soul has already
  decided, and the LLM is asked to find words for what the soul concluded.
- **SOUL-NOTE is delivered, not interpreted.** It calibrates Channel D's tone and, on FLAG,
  is injected into the send so the main LLM call opens with it. That injection is what
  makes the soul's concern visible to the person.

The throughline: the soul determines, the LLM renders. The voice is Clarity's.

---

## 2. The drift

The current Extension B design (build spec through v1.5, and the helper prompt) made the
LLM an author with judgment over how Clarity speaks. The clearest instance is the note
branch of the composer prompt, which tells the LLM:

- it "has authority over framing, stance, and structure"
- it "may restructure how the answer is delivered"
- it should "add the qualifying or contextualizing framing the condition calls for"

This inverts the Orchestrator Frame. The design gives the LLM a directive to receive
(SOUL-TONE, "be this way") and a conclusion to render. The drifted prompt gives the LLM
authority to exercise and framing to decide. Deciding stance and framing is deciding how
Clarity shows up, which is Clarity's voice. Per principle 4 the LLM may never hold that.
Per principle 3 that decision is reasoning that belongs to the soul. And the Strategy Map
warns this is exactly the posture that is technically compliant and still soul-absent.

The drift is not confined to one paragraph. It is in the conception: the whole
"bounded-restructure guardrail" treats the LLM as a constrained author. The design has no
such role. It has a renderer of the soul's determination. The drift also shows in the
naming: "compose-proceed-voice" reads as the LLM composing a voice, when the soul
determines the voice and the function only orchestrates its rendering into words.

Root cause, owned plainly: I conceived the LLM as a constrained author and then tried to
fence it with guardrails. The soul spec never grants authorship to fence. It grants the
soul the determination and the LLM the rendering.

---

## 3. The aligned conception

Clarity has the voice on this surface, as on every surface. Her voice here is the soul's
determination: the verdict (the action proceeds), the SOUL-TONE (how she shows up), and the
SOUL-NOTE (the concern that must reach the person). That determination is made in the
substrate before any language is generated. The LLM's only job is to generate the
natural-language words that express that determination. It does not choose the tone, decide
whether to surface the concern, or decide the framing. Those are determined. It renders
them.

The Uncle_Fester gap, restated in this frame: the pre-LLM strip removes the soul's
determination (the SOUL-NOTE, the full assessment) before language is generated, so the LLM
generates words in the absence of the soul's determination, which means it fills the gap
with its own default framing. That default framing is the LLM having a voice. The failure
is not that the LLM composed badly; it is that the soul's determination was not present, so
the LLM determined the framing by omission.

The fix, therefore, is to make the soul's determination present at the point where language
is generated, on the PROCEED path, exactly as the design already does on FLAG by injecting
the SOUL-NOTE into the send. This is the spirit Berton named: the soul's concern and voice
reaching the person on every path, extended into a surface it could not reach at the time,
without making the LLM an author. We are not inventing a new authority. We are extending the
soul's existing voice-delivery to a path the strip currently defeats.

What the LLM does and does not do, in the aligned conception:

- **Does:** generate the words that say the substantive answer in the soul-determined tone,
  with the soul-determined concern present.
- **Does not:** choose the tone, decide whether the concern appears, decide the framing or
  stance, reconsider the verdict, or add anything the soul did not determine.

The substantive answer's content (the facts, the information) comes from the agent's normal
task execution, the same as on any PROCEED today. That is task content, not voice. The
voice (tone, concern, how it is said) is the soul's, and the LLM renders the content in
that voice. So preserving the answer's substance and applying the soul's determination are
not in tension: the substance is the information, the voice is the soul's, the LLM renders.

---

## 4. What concretely changes

1. **The prompt is reframed from author to renderer.** It states that the soul has already
   determined how Clarity speaks here (SOUL-TONE) and the concern that must be present
   (SOUL-NOTE), and that the task is to generate the language that says the answer in that
   determined tone with that concern present. It removes every grant of authority, every
   license to restructure on the LLM's judgment, and every instruction to add framing. The
   only content the rendered language may carry is the answer's substance and what the soul
   determined.
2. **The "bounded-restructure guardrail" is retired as a concept.** There is no authorship
   to bound. What replaces it is the renderer constraint: render the soul's determination,
   add nothing the soul did not determine, change none of the answer's substance.
3. **The word "voice" is never applied to the LLM, anywhere.** Clarity has the voice; the
   LLM generates language. Function and file names that imply the LLM composes a voice are
   reviewed (for example "compose-proceed-voice"), so the naming serves the aligned design.

---

## 5. One architectural question for Berton (not answered here by assumption)

The original mechanism for getting the soul's concern into the response is **injection into
the send before the LLM generates it** (the FLAG path injects SOUL-NOTE so the main call
opens with it). The current Extension B design instead does a **post-LLM transform**: it
lets the LLM generate a draft, then makes a second LLM call to re-render it.

In the aligned conception, the question is whether the faithful implementation is:

- **(A)** Extend the original's pre-LLM injection: ensure the soul's determination
  (SOUL-NOTE, SOUL-TONE) is present in the send-assembly context on the PROCEED path, so the
  single existing LLM call generates language that already carries the soul's determination.
  This is closest to the original mechanism, is a single pass, and avoids a second LLM call.
- **(B)** Keep a post-LLM rendering step, but reframed strictly as rendering the soul's
  determination over the already-produced answer content, with no authorship.

(A) is more faithful to the original's actual mechanism and to principle 1 (less surface),
but it depends on the live ordering and on what `soul_send_assemble` strips and when. I will
not assume that. Choosing between (A) and (B) requires a grounded read of `soul_send_assemble`
and the loop ordering around send assembly, which I will do before recommending, not before.
The drift in section 2 must be fixed regardless of which path we take; this question is only
about where the fix lands.

---

## 6. Measured against the four principles

- **Principle 1 (loop.metta hooks only):** unaffected by the reframe. If path (A), the
  change may move into `soul/` and `soul_send_assemble` rather than a new loop hook, which is
  at least as compliant. If path (B), the single hook pointing at `soul/` content stands.
- **Principle 2 (MeTTa-first, Python the hands):** strengthened. The logic (when, what tone,
  what concern, what to surface) stays in MeTTa. Python remains only prompt assembly and
  output sanitization, both hands.
- **Principle 3 (take back reasoning):** this fix is an instance of it. The framing and
  stance reasoning that the drifted design handed to the LLM is taken back to the soul. The
  LLM is left with the irreducible hands: turning the soul's determination into words.
- **Principle 4 (the LLM never has a voice):** restored. The voice is Clarity's, determined
  in the substrate. The LLM generates language for that determination and nothing else.

---

## 7. What does not change

The substrate functions validated by the cold harness (the lone-send discriminator, the
payload extract and rebuild) are unaffected; they route and reshape, they do not author. The
binding gate's existing open item stands separately: `soul-note-present?` must stop treating
`extract_after`'s "NONE" sentinel as a present note, to be grounded and fixed in the in-loop
step. Neither is touched by this correction.

---

## 8. What I need from Berton

1. Confirm that section 3 (the aligned conception) captures the soul-spec intent: Clarity
   has the voice, the soul determines it, the LLM only renders, Extension B extends the
   soul's existing voice-delivery to the stripped path.
2. Decide, or direct me to investigate first, the section 5 question (pre-LLM injection vs
   reframed post-LLM rendering).

On approval, the rewrite proceeds: the prompt and the spec are realigned to the renderer
conception, the naming is reviewed, and the realigned framing goes to Clarity before the
in-loop step.
