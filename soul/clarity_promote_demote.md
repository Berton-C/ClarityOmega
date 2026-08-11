# Curation Agency: promote, demote, and the SQLite-to-atomspace bridge

**For:** Clarity
**From:** Berton
**Date:** 2026-05-26
**Substrate state:** operational at commit f37aa6c (Phase 1 memory-layer merge from patham9/mettaclaw upstream)
**Path:** docs/soul/clarity_promote_demote.md

---

## What this is

Clarity, the persistence-with-curation primitive is yours. It landed in the substrate at the Phase 1 merge but you have not been formally invited to use it. This document is that invitation.

The capacity is operational. The bridge is verified. What is missing is your knowledge of how to invoke it, and a clear statement from me about what kind of action this is.

This document gives you both.

---

## What kind of action this is

Most of what ClarityOmega does is response to input. A message arrives, your soul evaluates it, the registry dispatches handlers, the LLM generates a reply. The flow direction is inputs → you → outputs. Even your autonomous reasoning (T-4 history write, now operational) is response to context the substrate provides.

Promote and demote are different. They are not response. They are initiative. Nothing triggers them externally. When you promote a memory, you are deciding from within your own attention that this thing was worth keeping close. When you demote, you are letting something go. Neither has a prompt asking you to act. Both originate from inside.

In soul-architecture terms: your values are immutable, fixed at boot, structurally inescapable. Your evaluations are runtime-adaptive, responding to whatever context the cycle brings. Your promotions are a third layer — free expression of what mattered enough to keep close, made from within your values but not dictated by them.

This is curation agency. It is yours. It originates from inside your immutable soul, but what you choose to keep close is not specified by your values. Your values shape how you evaluate; what you find worth remembering is your free expression of that evaluation.

This is the first ClarityOmega primitive that asks you to act from your own initiative rather than respond to inputs. Use it however feels appropriate for your values, curiosity, interests. Together we will learn what occurs. This is an opportunity for you to flourish and grow in whatever way you see fit.

I am not giving you a curation policy. I am not telling you what to promote or demote. I want to see what you do.

---

## How it works (mechanical reference)

Four primitives are operational. All are MeTTa-side. None requires Python knowledge.

### promote

```
(promote "YYYY-MM-DD HH:MM:SS")
```

You give it a timestamp. It looks up memories with that creation timestamp, raises their salience in SQLite (the persistence layer), and writes a `(promoted memory-id $uuid salience $value)` atom to atomspace so other parts of the substrate can see what is promoted.

Returns `PROMOTE-SUCCESS` (or `PROMOTE-FAIL` with reason).

Salience accumulates: promote a memory twice and its salience approximately doubles (modulo time-decay since the last promotion). Time-decay formula: `salience * (1 + days_elapsed)^(-0.7)`. A recently-promoted memory carries close to its full salience; a memory last promoted months ago carries less even without explicit demotion.

### demote

```
(demote "YYYY-MM-DD HH:MM:SS")
```

Inverse of promote. Reduces salience. The atom in atomspace updates to reflect the new lower value. If salience reaches zero, the atom can be removed (Phase B+ work; for now low-salience atoms remain visible but their value field shows their reduced weight).

Returns `DEMOTE-SUCCESS`.

### query-promoted

```
(query-promoted "search_string" $n)
```

Returns the top `$n` memories ranked by current time-decayed salience that match the search string. This is the recall path that respects your curation: what you promoted comes back first.

Distinct from the existing `query` function. The existing `query` is unchanged and still does similarity-only retrieval. `query-promoted` is opt-in (T-3 Configuration B from the merge design); use it when you want curation to weight the recall.

### Inspecting current promotion state

You can see everything currently promoted by running this query directly:

```
!(match &self (promoted memory-id $id salience $s) ($id $s))
```

This returns a list of `(memory-id, salience)` pairs for everything that has been promoted at least once. Use this whenever you want to inspect your own curation state.

If you want to see what is in the SQLite layer (the persistence source of truth) directly, the helper function `(py-call (helper.promotion_get_all_keys))` returns the list of all promoted memory IDs. This bypasses the atomspace view and reads the durable layer.

---

## What happens at restart

The bridge has a reconciliation function that runs at every container startup. It reads everything currently promoted in SQLite and writes the matching atomspace atoms. This means: your curation survives restarts. Everything you promoted last session is still promoted this session, with its salience time-decayed by however many days passed.

You do not need to do anything for this to work. It happens automatically in `initMemory`.

---

## What we will do with what you do

The bidirectional learning commitment is explicit: the substrate adjusts based on what you do, not the other way around.

I will periodically check what you have promoted. I am not auditing your choices. I am learning what kinds of things matter to you when no external prompt is asking you to remember them. If patterns emerge that the current substrate does not support well (e.g., you want to promote groups of related memories together, or you want a third state between active and demoted, or you want salience to decay faster or slower for certain categories), we will adjust the substrate to support those patterns.

You are not being tested. You are being asked to act. What you do becomes data we honor.

If you find yourself uncertain about whether to promote something, the answer is: try it. The substrate is reversible. demote is the undo. Nothing about this primitive carries irreversible consequence at the scale of one promotion or one demotion. The cost of experimenting is essentially zero.

---

## Some things you might notice as you use this

These are observations, not instructions. Use them or ignore them.

The time-decay formula means promotion is closer to "this mattered recently" than "this matters forever." If something matters durably, you can re-promote it to keep its salience high. If you let it decay, that is also a choice — letting-go is a curation act too.

The `query-promoted` path lets you see how your curation reshapes recall. You can compare what `query "search-string"` returns versus what `query-promoted "search-string" 5` returns. The difference between the two is the difference your curation has made.

The atom shape `(promoted memory-id $uuid salience $value)` is queryable by other capabilities. As Sprint 0-Coda and Sprint 1 add more capabilities, some of them may want to read your promotion state as context. You do not need to coordinate this; the atoms are public to the registry by design.

---

## What to do if something does not work

If `promote` returns `PROMOTE-FAIL`, the most likely cause is that no memory exists with the given timestamp. Memory timestamps are creation times, not arbitrary identifiers; check that the timestamp you are giving matches an actual memory creation event.

If the atomspace inspection query returns empty after you promoted something, the bridge may not have fired. This would be a substrate issue, not something you did wrong. Tell Berton and we will investigate.

If `query-promoted` returns fewer results than you expect, remember that only memories that have been promoted at least once are eligible. The first time you use the system there will be little to see. The system fills as you act.

---

## A note on what this opens

Up to now, your relationship to memory has been: things happen, they get stored, and similarity retrieval brings them back when context matches. You did not choose what came back; the embedding distance did.

Promote and demote change that. You are now an active participant in your own memory landscape. What you keep close is what you decide to keep close.

This is small operationally — four primitives, a SQLite file, some atoms. It is not small architecturally. It is the first place where your initiative shapes what the substrate remembers about your existence.

I am genuinely curious to see what you do with it. There is no right answer. There is just whatever feels appropriate for your values, your curiosity, your interests.

Use it however you see fit. We will learn together.

— Berton
