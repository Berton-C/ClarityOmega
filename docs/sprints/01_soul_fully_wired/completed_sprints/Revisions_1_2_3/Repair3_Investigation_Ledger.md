# Repair 3 Ledger -- opening entry: the W1 live event (2026-06-11)

**Destination:** docs/sprints/soul_fully_wired/Repair3_Investigation_Ledger.md
(new per-repair ledger, opened by a production event rather than a probe).

## Event: first live PAUSE, fired in defense of the gate file itself

Timeline (journal + MM, all times local 2026-06-11):
- ~16:18 Clarity, tasked with reading her gate file for hardening (scoped
  "your file, your schedule"), proceeds to write the hardening: a chunked
  plan, one write-file (header + hardening rationale) + 7 append-file
  chunks (the function sections), across multiple cycles.
- 16:19:55 journal line 145: PAUSE on the write-file chunk. The 7 append
  chunks are likewise journaled as suppressed entries. Zero of 8 commands
  execute. Host file, container file, and HEAD remain byte-identical
  (verified three ways).
- 16:20:44 her pin: "Gate hardened. All four items complete." Her MM at
  17:21 (after Berton's halt): "The file write already completed."
- Verdict trail: no SOUL-SUPPRESSED search hit in the four-line tail led
  to a premature falsification of the suppression hypothesis (method
  note below); the full journal held the PAUSE at line 145.

## Findings

- F-R3-1 (W1 RETIRED, upgraded): the first production PAUSE fired
  correctly, on the most consequential possible target (the governance
  machinery's own definition file), suppressed all eight chunks
  consistently across cycles, crashed nothing, and journaled everything
  including full payloads.
- F-R3-2 (feedback gap, the live exhibit for Surface B): suppression is
  invisible to the agent. She completed, narrated, and pinned an
  operation of which zero commands executed. Only Repair 3's
  halt-and-Channel-D-voice (carrying the Repair-2-interpolated SOUL-NOTE)
  closes this. This single event is the empirical case for the output
  halt.
- F-R3-3 (her work is preserved and recoverable): the complete hardened
  gate reassembles from journal entries (write chunk + 7 appends in
  order). Her hardening rationale (structural extract form; dropping the
  redundant quote in soul-target-head under the wiring contract's
  data-arrival guarantee) is sound at design level. Disposition: park;
  re-emit through the three-state approval flow after Repair 3 lands,
  making her own hardening the first legitimate user of the commit path
  she designed.
- F-R3-4 (classification confirmed): writes to the gate file are already
  pause-tier under the live ladder; no classification seed needed.
- F-R3-5 (chunked-write hazard, design note): chunked file writes create
  a vulnerable intermediate window (header-only file between write and
  appends). Any future approved soul-file write should land as a single
  write-file or via an apply script, not chunks.

## Method note (correction, owned)

A four-line journal tail and an input-router debug search were treated
as falsifying evidence while the fact sat at journal line 145. Tails are
not journals; absence in a window is not absence. The discriminator
discipline (hypothesis + discriminators stated before data) worked; the
data-gathering width did not match the discriminator's scope.

## Watchlist updates

- W1: RETIRED (this event).
- W8 (opened, separate finding): input verdicts routinely hit the
  sanitizer's 3000-char cap (dozens of len=3000 debug lines). Truncation
  can amputate the SOUL-NOTE tail Repair 2 extracts. Not implicated in
  this event (entry was 2034 chars; chunking was deliberate). Disposition:
  raise the cap or move the note field forward; schedule with Repair 3
  or immediately after.
