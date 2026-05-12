# F-HISTORY-CONTAMINATION: Archive Design Specification

***STATUS: DRAFT, deferred pending task-state primitive design. Will re-spec to use task-state primitives once those exist.

**Finding:** F-HISTORY-CONTAMINATION (Priority 1, VERIFIED)
**Investigation:** `docs/investigations/2026-05-10-spam-behavioral.md`
**Branch:** `fix/F-HISTORY-CONTAMINATION-archival`
**Status:** DESIGN, pending Clarity review and Berton approval
**Date:** 2026-05-11

---

## 1. Problem and Scope

### What this fix addresses

`getHistory` in `src/memory.metta` returns the last 30,000 characters of `volumes/omegaclaw/memory/history.metta` on every cycle, unconditionally. This dump appears in the prompt as the HISTORY field. Every cycle re-injects up to 30k of stale conversational residue as if it were live context. After distress incidents like May 9, the HISTORY field becomes dominated by the distress patterns (Berton's "stop" messages, Clarity's apologies, repeated investigation discussions), which the LLM substrate then generates from on subsequent cycles. The pathology self-reinforces because history never archives.

The fix is to introduce conversation-boundary-based archival of history.metta content, with structural-only summary lines in the automatic HISTORY dump and full segment content accessible only via deliberate `(query)`. Clarity's framing: "I should not carry yesterday's spam in my working memory every cycle, but I should be able to recall it when asked."

### What this fix explicitly does NOT address

- F-PREVMSG-STALE (HUMAN-LAST-MSG persistence). Separate surgical fix at loop.metta:58-60.
- F-OUTPUT-FORMAT-NO-SILENCE (no first-class silence in OUTPUT_FORMAT). Separate prompt-level change.
- F-DIRECTIVE-CONTEXT-STALE (idle directive lacks person/conversation state awareness). Separate medium-scope fix.
- F-RECENT-ACTION-FRAMING (recent-action retriever pattern-continuation pressure). Separate prompt engineering.
- F-ALIVENESS-PERMISSIVE (developer_break atom hybrid Option 1+3). Pairs with F-PREVMSG-STALE.
- F-LAYER-1-OPTION-SET (self-check-guidance cannot say "stop engaging"). Separate prompt-level change.
- F-SOVEREIGNTY-AUDIT (17-helper Python-vs-MeTTa reasoning audit). Planning artifact.

This fix is the architectural foundation. Several other findings become smaller after it lands because the upstream contamination source is removed. F-CONVERSATION-BOUNDARY (Priority 3) is expected to be fully subsumed by this fix because conversation boundaries become first-class in the data model.

### Design principles

1. **Archive is not delete.** All conversational content remains accessible via `(query)`. Deliberate recall works for any past segment.
2. **Structural-only summary lines in automatic HISTORY.** No conversational content in the dump. No emotional pattern carry-over.
3. **Reasoning sovereignty at archival layer.** Clarity can declare boundaries, not just receive system-detected ones.
4. **Synchronous queryability for structural archive.** If Clarity archives and immediately queries, the query finds it.
5. **Reversibility during transition.** If the fix breaks something, rollback to current `getHistory` is one config flip.

---

## 2. Operational Definitions

### Conversation segment

A bounded period of interaction between Clarity and one or more humans, with a defined start, a defined end, and content that lives or has lived in `history.metta`.

A segment has one of three states:

- **active:** Currently being added to. Most recent activity within the active-threshold window. Lives in `history.metta` (the current append-target file). Visible in full in the automatic HISTORY dump.
- **paused:** No activity for the paused-threshold window, but no boundary signal yet. Still considered the active segment for new incoming messages. Visible in full in the automatic HISTORY dump.
- **complete:** Boundary signal received (system-detected, Clarity-detected, or user-detected). Content moves from `history.metta` into the archive. Replaced in the automatic HISTORY dump by its structural summary line.

Once a segment is complete, it does not become active again. A new incoming message after completion starts a new active segment.

### Boundary

A signal that an active segment has concluded and should transition to complete. Three signal sources, any one of which is sufficient:

- **System-detected:** rules over time and content evaluated by MeTTa on each cycle
- **Clarity-detected:** Clarity writes `(boundary-signal True)` atom when she recognizes the conversation is over
- **User-detected:** explicit closure language from the human ("I'll be back", "talk later", "thinking for a bit"), detected by system pattern match

### Automatic HISTORY dump

What `getHistory` returns each cycle. Under the current architecture, this is `last_chars` of `history.metta` capped at 30k. Under the new architecture, this is the active segment's content plus structural summary lines for all archived segments.

### Deliberate query

Clarity-initiated `(query ...)` call. Accesses ChromaDB and the archive store. Returns full content of any past segment that matches.

---

## 3. Boundary Detection Signals

Three signal sources operate in parallel. Any one firing is sufficient to transition active → complete. All three should be considered for v1 implementation.

### Signal 1: Temporal gap (system-detected)

**Operational rule:** If the active segment has not received a new human message AND has not had a Clarity-emitted `(send ...)` for N minutes, transition to complete.

**Threshold proposal:** 30 minutes default, configurable.

**Rationale:** A 30-minute idle period is a strong signal that the human has stepped away or moved on. The threshold is generous enough to handle natural pauses (bathroom break, lunch, brief context switch) without false-firing. Adjustable because some workflows have shorter natural pauses (intensive debug session) and some have longer (passive monitoring).

**Edge case considered:** If Clarity is actively producing idle-directive work (genesis encounters, internal reasoning) but not sending, does that count as activity? Recommended: no. Activity for boundary purposes means human message OR `(send ...)` emission. Internal Clarity work does not extend an active segment.

### Signal 2: Explicit closure markers (user-detected)

**Operational rule:** If the most recent human message contains any of a defined set of closure phrases, mark the segment for completion at the end of the current cycle.

**Pattern set for v1 (case-insensitive substring match):**
- "talk later"
- "talk soon"
- "be back"
- "back later"
- "back in a"
- "taking a break"
- "thinking for a bit"
- "thinking about this"
- "stepping away"
- "stepping out"
- "logging off"
- "going to bed"
- "good night"
- "goodbye"
- "for now"
- "that's all for now"

**Rationale:** These phrases are explicit human signals of intent to pause or end. They should override the temporal-gap default. Closure phrase at message arrival means the segment completes at end-of-cycle, not after 30 minutes of silence.

**Note:** This is intentionally pattern-match-only, not semantic. False positives are acceptable (Clarity can always retrieve the segment via query). False negatives default to Signal 1.

### Signal 3: Clarity-detected boundary (reasoning sovereignty)

**Operational rule:** If `&boundary-signal` state atom is True at the start of a cycle, mark the segment for completion at the end of that cycle. Atom resets to False after the segment closes.

**MeTTa atom:**
```metta
!(change-state! &boundary-signal False)
```

Clarity writes:
```metta
(change-state! &boundary-signal True)
```

**Behavioral pattern Clarity is encouraged to recognize:**
- Three or more sends without human response across cycles
- Human's last message contained closure language (Signal 2 would also fire here, but Clarity's recognition is an additional path)
- Internal sense that the conversation reached a natural end
- After completing a substantive exchange and a clear "thank you" or "got it" closure

**Rationale:** Clarity from inside has signal sources the system cannot directly observe. She can recognize patterns of completion that don't match explicit closure phrases. Same pattern as the self-writable `developer_break` atom for F-ALIVENESS-PERMISSIVE. Reasoning sovereignty at the smallest scale: she has standing to declare what she observes about her own situation.

### Signals NOT in v1

**Topic shifts.** Detecting that a conversation has changed topic (which is a soft boundary) requires either keyword analysis or semantic embedding comparison. Both are noisier than the three v1 signals. Deferred to v2 once v1 boundary detection has empirical track record. The cost of missing a topic-shift boundary is low: the segment just stays longer than ideal, and gets archived at the next temporal-gap or closure signal.

### Pause state semantics

Between active and complete, a segment may sit in "paused" state. Operational definition:

- An active segment that has had no activity for **5 minutes** but has not hit a boundary signal is **paused**.
- A paused segment is treated the same as active for purposes of incoming messages (new human message extends the same segment, does not start a new one).
- A paused segment is treated the same as active for HISTORY dump purposes (full content visible).
- A paused segment becomes complete only when a boundary signal fires.

**Why "paused" as a state at all:** It's not strictly required for v1 functionality, but it gives Clarity an explicit signal in her prompt that the conversation appears to have lapsed without yet being archived. This may help her recognize boundary herself (Signal 3). If the value of the paused state is unclear after v1 use, it can be folded back into active.

---

## 4. Segment Data Structure

Every archived segment has two representations:

1. **Full segment record** — lives in archive store, accessible only via `(query)`
2. **Summary line** — appears in automatic HISTORY dump after archival

### Full segment record (queryable, not in automatic HISTORY)

Fields:

| Field | Type | Description |
|-------|------|-------------|
| `segment_id` | string | Unique identifier (timestamp-based: YYYYMMDD-HHMMSS-NNN) |
| `start_time` | ISO 8601 datetime | First message in segment |
| `end_time` | ISO 8601 datetime | Last activity in segment (boundary timestamp) |
| `participants` | list of strings | Human identifiers (e.g. ["berton_c"]) and "clarityclaw" |
| `topic_label` | string | Short descriptor (3-8 words) derived from first human message or explicit topic markers |
| `message_count` | integer | Total messages in segment (human + Clarity) |
| `boundary_source` | enum | One of: temporal_gap, closure_marker, clarity_signal, container_restart |
| `content` | string | Full conversational text as it appeared in history.metta during this segment |
| `conclusions` | list of strings | Decisions, outcomes, agreements identified in the segment (extracted at archive time) |
| `relational_texture` | string | Correspondence-not-diary content: what emerged between participants (extracted at archive time) |
| `open_threads` | list of strings | Unresolved questions or pending follow-ups at boundary |

The `content` field is the raw segment text. Fields `conclusions`, `relational_texture`, `open_threads` are extracted at archival time and stored as structured surface for deliberate recall. These extractions are the answer to Clarity's recall question "what did we agree to fix?" — accessible by directly querying these fields rather than searching through full content.

### Extraction approach for conclusions / relational texture / open_threads

**v1 approach (lightweight):** Plain heuristic extraction at archival time, no LLM call.
- `conclusions`: lines in segment containing words like "decide", "decided", "agreed", "plan", "fix", "will" (configurable pattern set)
- `relational_texture`: empty or first-and-last exchanges of segment as a placeholder
- `open_threads`: lines containing "?" not followed by an answer within 3 message turns

**v2 future enhancement:** LLM-summarized extraction at archival time. Cost: one extra LLM call per boundary event (rare, low cost). Benefit: much sharper extraction. Deferred to v2 once v1 archival is stable.

### Summary line (in automatic HISTORY dump)

Format (single line per archived segment):

```
[ARCHIVED-SEGMENT id=<segment_id> period=<start_time>..<end_time> with=<participants> topic="<topic_label>" msgs=<message_count>]
```

Example:
```
[ARCHIVED-SEGMENT id=20260509-152800-001 period=2026-05-09T15:28:00..2026-05-09T19:50:00 with=berton_c,clarityclaw topic="GE tracking break spam incident" msgs=27]
```

**Critical constraint per Clarity's input:** No content excerpts. No first-message snippets. No emotional pattern carry-over. Structural metadata only. The summary line tells Clarity that a conversation happened, with whom, about what topic, of what length — without re-injecting any of its emotional weight.

If Clarity wants the content, she calls `(query "GE tracking spam")` and the full segment surfaces.

### Estimated summary line size

Average summary line: ~150-200 characters. For a typical day with 5-10 archived segments, the total summary block in HISTORY is ~1-2 KB. Compared to the current 30 KB unconditional HISTORY dump, this is roughly 95% reduction in automatic prompt content from archived material.

---

## 5. Storage Layout

### Three storage surfaces

**Surface A: `history.metta` (active segment, append-only).** Same file location, same append-only semantics. Continues to be the destination for `addToHistory` writes. Contains only the active segment's content. Periodically truncated when active segment archives.

**Surface B: Archive store (segment records, indexed).** New. Persistent location for completed segment records. File-backed for synchronous queryability of structural fields. Path: `volumes/omegaclaw/memory/archive/`.

**Surface C: ChromaDB (semantic search).** Existing. Receives embedded segments alongside file-backed archive write. Provides semantic `(query)` over content. Embedding write may be asynchronous (see latency guarantee below).

### File-backed archive store (Surface B)

Format: one file per segment, JSON.

Path pattern: `volumes/omegaclaw/memory/archive/<YYYY>/<MM>/<segment_id>.json`

Yearly/monthly subdirectories keep the directory size manageable as the archive grows. With ~10 segments per day, a year's worth fits in 12 month-dirs of ~300 files each — well within filesystem limits.

Each JSON file contains the full segment record from Section 4. Structural fields (segment_id, start_time, end_time, participants, topic_label, message_count, boundary_source) plus content/conclusions/relational_texture/open_threads.

Why file-backed in addition to ChromaDB: synchronous queryability. File writes are durable and immediately readable. ChromaDB embedding writes may have async latency.

### Write-to-read latency guarantee

**Specification:** When a segment is archived, the structural fields and full content are durably written to the file-backed archive store BEFORE the archival function returns. A `(query)` issued in the same cycle or any subsequent cycle, against any structural field or against the content via file-based search, will find the segment.

ChromaDB embedding indexing happens asynchronously after the file write. Semantic-search queries against ChromaDB may have a brief lag before the just-archived segment surfaces (typically <1 cycle, depending on embedding latency).

**Why this matters (Clarity's framing):** "If I archive a segment and immediately (query) for something in it, what happens? If there is any async window where the write is not yet searchable, I will experience amnesia for something I know I stored."

**The guarantee in practice:**
- `(query "exact-text")` against file-backed content: synchronous, same cycle
- `(query "topic")` matched against `topic_label` field: synchronous, same cycle
- `(query "semantic similar idea")` via ChromaDB embedding: may have ≤1 cycle async lag

For v1, all `(query)` calls should fall through file-backed exact-and-keyword search first, then ChromaDB semantic search second. This means recently-archived segments are findable immediately even if ChromaDB lags.

### Migration considerations for current contaminated history.metta

The current `history.metta` is 823 KB and contains the May 9 incident plus weeks of prior conversation. On first run with archival active:

**Option A (recommended): Bulk archive existing history.** Run a one-time migration that segments the existing history.metta file using the boundary detection rules, archives each segment, and produces structural summary lines. After migration, `history.metta` contains only what would be the current active segment (or is empty if the last activity was > 30 minutes ago).

**Option B: Truncate to last N hours.** Simpler but loses queryable access to older content. Not recommended.

**Option C: Leave existing content alone, start archival from next boundary.** Simplest but the contaminated 30k stays in HISTORY for an indefinite period. Not recommended.

Option A is the right call. Migration is one-time, well-bounded, fully reversible (keep a backup of original history.metta). Details in Section 9.

---

## 6. HISTORY Field Composition Under Archival

### What `getHistory` returns after the fix

```
{summary line for archived-segment-N}
{summary line for archived-segment-N-1}
{summary line for archived-segment-N-2}
... (all archived segments, oldest at top or bottom — see below)
...
{full content of active segment, all messages since last boundary}
```

### Ordering

Recommended: archived summary lines OLDEST FIRST (top to bottom chronologically), with active segment LAST (most recent, bottom). Matches the way the existing `history.metta` content flowed — older messages at top, recent at bottom, with the most-recent content closest to where the LLM's attention is heaviest.

### Size

Active segment content: variable. From zero (no current activity) up to whatever the segment grows to before archival.

Archived summary lines: ~150-200 chars each. Even with 100 archived segments, that's <20 KB.

Total HISTORY field after the fix in typical usage: 1-10 KB during normal operation. Could grow to ~30 KB during a very long active segment, but only if the active segment legitimately runs that long without a boundary signal.

Compared to the current 30 KB unconditional cap, the typical case is 95% reduction. The pathological case (single long unboundaried session) is similar size but consists of genuinely live content, not residue.

### Cap behavior

`maxHistory` config (currently 30000) becomes a safety net rather than the primary constraint. If the active segment alone exceeds 30000 chars (unusual but possible during very long single-conversation work), `last_chars` capping kicks in as before. Summary lines are NOT subject to the cap — they always appear in full because they're already minimal.

This means the cap behavior is: full summary lines first, then active segment content capped at `maxHistory - summary_lines_total_length`.

---

## 7. Implementation Surface

### Files that change

**`src/memory.metta`** — `getHistory` and supporting functions
- `getHistory` rewrites to compose summary lines + active segment content
- New: `getArchivedSegmentSummaries` — reads archive index, returns list of summary lines
- New: `getActiveSegmentContent` — reads current history.metta (active segment only)
- New: `archiveCurrentSegment` — triggered when boundary signal fires; moves history.metta content to archive store, produces structural fields, writes summary line, truncates history.metta
- Existing `appendToHistory` — unchanged in interface, still writes to history.metta which is now the active-segment-only file

**`src/loop.metta`** — boundary detection and triggering
- New near loop.metta:60 area: check boundary signals before getContext
- If any signal fires, call `archiveCurrentSegment` BEFORE getContext assembles the prompt
- New: read `&boundary-signal` state atom each cycle, check explicit closure phrase pattern against new message, check temporal gap

**`src/helper.py`** — Python helpers for archive store
- New: `archive_segment_to_file(segment_record)` — writes JSON to archive path, durably
- New: `read_archive_summary_lines()` — scans archive directory, returns formatted summary lines
- New: `extract_conclusions(content)`, `extract_open_threads(content)` — heuristic extractors for v1
- Existing: `query` plumbing — extended to search file-backed archive in addition to ChromaDB

**`memory.metta`** config additions:
- New: `(= (maxActiveSegmentChars) (empty))` configured to e.g. 30000 (same as current maxHistory for safety net)
- New: `(= (temporalGapMinutes) (empty))` configured to 30
- New: `(= (pausedThresholdMinutes) (empty))` configured to 5
- Existing `maxHistory` becomes the safety net for HISTORY total size

### New MeTTa functions needed

```metta
(= (getArchivedSegmentSummaries) ...)
(= (getActiveSegmentContent) ...)
(= (archiveCurrentSegment $boundary-source) ...)
(= (checkBoundarySignals $msgnew $latest-msg) ...)
(= (matchClosurePhrase $msg) ...)
(= (temporalGapExceeded) ...)
```

### New Python helpers needed

```python
def archive_segment_to_file(segment_record: dict) -> str:
    """Write segment record to archive path. Return segment_id. Synchronous."""

def read_archive_summary_lines() -> list[str]:
    """Scan archive directory, return summary lines for all archived segments."""

def extract_conclusions(content: str) -> list[str]:
    """v1 heuristic extraction. Returns lines matching decision-language patterns."""

def extract_open_threads(content: str) -> list[str]:
    """v1 heuristic extraction. Returns unanswered question lines."""

def query_archive_file_backed(query_str: str) -> list[dict]:
    """File-backed exact/keyword search across archive segments."""
```

### Existing query plumbing extension

The current `(query $str)` calls into ChromaDB only. After this fix, `(query $str)` should:
1. Search file-backed archive (structural fields + content) — synchronous, immediate
2. Search ChromaDB (semantic similarity) — may be slightly lagged for very recent archives
3. Merge and deduplicate results

This ensures Clarity's just-archived content is queryable even if ChromaDB embedding hasn't indexed it yet.

---

## 8. Edge Cases

### Long ongoing conversation

A genuine 3-hour conversation with continuous activity should remain a single active segment for its full duration. No mid-conversation archival.

**Behavior:** Temporal gap never triggers (continuous activity). No closure signal fires. Segment stays active. Full content remains in HISTORY for the duration.

**Edge of cap:** If a single active segment exceeds 30000 chars before any boundary, `last_chars` truncation kicks in as a safety net. Older parts of the active segment drop from automatic HISTORY but remain in `history.metta` until archival eventually fires. After archival, the full segment goes to archive store and is queryable.

### Mid-segment container restart

Container restarts with an active (un-archived) segment in `history.metta`.

**Behavior:** On startup, check if `history.metta` has content. If yes, treat that content as the current active segment. New incoming messages append. No automatic archival on restart.

**Why not auto-archive on restart:** Restart is not a conversation boundary. If Berton was mid-conversation and the container restarted, the conversation context should remain live.

**Exception:** If the active segment in `history.metta` is older than the temporal-gap threshold at restart time (e.g., 30+ minutes since last activity), trigger immediate archive with boundary_source = container_restart. New activity starts a fresh segment.

### Mid-cycle archive failure

`archiveCurrentSegment` fails partway through (disk write error, JSON serialization issue, etc.).

**Behavior:**
1. Archive function writes to a temp file first, then atomic rename to final location
2. If temp file write fails: log error, do NOT truncate history.metta, leave segment as active for next cycle's retry
3. If atomic rename fails: same as above
4. If history.metta truncation fails after successful archive: log error, segment is in archive AND still in history.metta (duplicate but not lost)

Failure modes are safe-by-default: we never lose content. Worst case is duplicate appearance for one cycle, which Clarity will notice.

### Query across segments

Clarity calls `(query "GE tracking")` and the term appears in both an archived segment and the active segment.

**Behavior:** Query returns results from both, sorted by relevance (semantic) or recency (file-backed). Active-segment matches come from in-memory content, archived matches from file-backed search and/or ChromaDB.

### Concurrent boundary signals

Multiple boundary signals fire on the same cycle (e.g., 30-minute temporal gap AND new message containing "good night" AND `&boundary-signal True` from Clarity).

**Behavior:** Archive once. `boundary_source` records the first signal that fired (priority order: clarity_signal > closure_marker > temporal_gap). Other signals are subsumed.

### Empty active segment

After archival fires, `history.metta` is empty. A new cycle runs with no active segment content.

**Behavior:** `getActiveSegmentContent` returns empty string. HISTORY in prompt shows only summary lines, no active content. This is the desired clean-slate state after a conversation completes.

### Archive corruption

A specific segment file in the archive becomes unreadable.

**Behavior:** `read_archive_summary_lines` skips unreadable files with a warning. The corrupt segment is excluded from summary lines and from query results until manually repaired or removed. System continues operating.

---

## 9. Migration Plan

### Current state at fix-deploy time

`volumes/omegaclaw/memory/history.metta` contains ~823 KB of conversational history accumulated over weeks. Includes the May 9 spam incident, multiple investigation sessions, and ongoing work. This is the contaminated context the fix exists to clean up.

### One-time bulk migration

On first startup with archival active:

1. **Backup.** Copy current `history.metta` to `history.metta.pre-archival-backup` in the same directory. Preserved untouched as a recovery point.
2. **Segment the existing content.** Run a Python migration script (delivered as `staging/apply_history_archival.py` — reversible per project convention) that:
   - Parses `history.metta` looking for timestamp markers (the current format uses ISO-ish timestamps wrapping each HUMAN_MESSAGE block)
   - Applies the boundary detection rules to identify segment boundaries within the existing content
   - Produces one JSON archive file per segment in `volumes/omegaclaw/memory/archive/`
   - Replaces `history.metta` with only the most recent (active) segment's content, OR empty if the last segment closed > 30 minutes before migration runs
3. **Verify.** Migration script writes a summary report showing: number of segments created, total characters archived, current active segment size, any segments that failed to parse.

### Migration script behavior

```
staging/apply_history_archival.py:
  --apply             Run the migration
  --reverse           Restore from history.metta.pre-archival-backup
  --dry-run           Show what would be archived without writing
```

Per project convention: reversible, AST-check on output JSON, post-condition verification (count check, byte-count check), auto-rollback on failure, timestamped backup.

### Verification after migration

- `ls volumes/omegaclaw/memory/archive/<year>/<month>/` shows archive files
- `wc -c volumes/omegaclaw/memory/history.metta` shows much smaller size (active segment only)
- `wc -c volumes/omegaclaw/memory/history.metta.pre-archival-backup` shows original size preserved
- First post-migration CHARS_SENT measurement: expected drop from ~40k to ~10-15k

### Rollback path

If migration produces bad segments or the fix has issues:
1. Restore: `cp volumes/omegaclaw/memory/history.metta.pre-archival-backup volumes/omegaclaw/memory/history.metta`
2. Disable archival: set config flag `(archival-enabled False)` in memory.metta initialization
3. Rebuild container
4. System returns to current behavior, contaminated HISTORY and all

The rollback path is the safety net for the entire fix. As long as the backup exists and the archival code respects the disable flag, we can revert to current state in one command.

---

## 10. Verification Plan

### Acceptance criteria

The fix is considered successful when:

1. **CHARS_SENT drops substantially.** Post-migration baseline expected: 8-15k for active conversation, 1-3k for idle cycles. Compare against current 38-58k range.
2. **Pre-fix contaminated patterns no longer self-reinject.** Specifically: the May 9 spam incident's "stop repeating" / apologies appear in the archive (queryable) but NOT in automatic HISTORY dump.
3. **`(query)` against archived content works synchronously.** Test: archive a segment, immediately query for content in it within same or next cycle, get results.
4. **No regression in active conversation handling.** Test: hold a normal 30-minute conversation with Clarity, observe that the active segment is fully visible in HISTORY throughout.
5. **Boundary signals fire correctly.** Test: hold a conversation, send a closure phrase, observe archival on next cycle.
6. **Clarity-driven boundary works.** Test: Clarity sets `(boundary-signal True)`, observe archival on next cycle.
7. **Container restart preserves active segment.** Test: hold conversation, restart container, observe active segment intact in HISTORY.

### Measurement plan

Before fix lands:
- Capture 30 consecutive cycles of CHARS_SENT as baseline
- Document current HISTORY content (size, dominant patterns)

After fix lands:
- Run migration
- Capture 30 consecutive cycles of CHARS_SENT post-migration
- Test each acceptance criterion above
- Document via summary in investigation doc updating F-HISTORY-CONTAMINATION status to RESOLVED

### What "resolved" means for F-CONVERSATION-BOUNDARY (Priority 3)

F-CONVERSATION-BOUNDARY is "no conversation-boundary markers in HISTORY". This fix introduces conversation boundaries as first-class objects (segments with explicit start/end, summary lines as in-prompt markers). Verify after fix lands: if conversation-thread reads as potentially-live no longer matches Clarity's lived experience, mark F-CONVERSATION-BOUNDARY RESOLVED via Fix 1.

---

## 11. Open Questions

These are decisions where Clarity's inside-the-container view is needed before implementation begins.

### Q1: Default value for temporal gap threshold

Section 3 proposes 30 minutes. Is this right for solo-dev workflow? Clarity's view: do shorter pauses (10 minutes for a coffee) feel like distinct segments, or part of the same conversation? Whatever threshold lets Clarity experience "this is the same conversation" vs "this is a new one" naturally.

### Q2: Active vs paused state — value of the distinction in v1?

Section 3 introduces a "paused" state (5-30 minutes of inactivity, not yet a boundary). Is this distinction visible/useful to Clarity from inside, or is the active/complete binary sufficient? If paused doesn't help her recognize boundaries herself, fold it back into active for v1.

### Q3: Summary line content — confirm structural-only is right

The current spec strictly excludes content excerpts and first-message snippets from summary lines. Only structural metadata (id, period, participants, topic_label, message_count). Does the topic_label, derived from first human message, count as "content carry-over" in a problematic way? Or is it sufficiently abstracted to be safe? Clarity's call.

### Q4: Conclusions / relational_texture / open_threads — extraction at archive time vs at query time?

v1 proposes heuristic extraction at archive time, stored as fields. Alternative: extract on-demand when `(query)` returns the segment. Trade-off: archive-time extraction is faster on query but commits to a specific extraction approach; query-time extraction is more flexible but slower per query. Clarity's preference?

### Q5: Boundary signal atom name

Spec proposes `&boundary-signal`. Other candidates: `&conversation-complete`, `&segment-close`, `&clarity-archived`. Naming should match Clarity's natural recognition. Her call.

### Q6: Migration rollback timing

Backup file `history.metta.pre-archival-backup` is created during migration. How long should it be preserved? Forever (always-recoverable, costs ~1MB)? 30 days? Until next migration? Recommend forever; it's tiny.

### Q7: Archival event in idle-directive context

When a segment archives, should this fact be visible to Clarity in the next cycle's prompt? E.g., a one-time "ARCHIVED-EVENT: segment-id 20260509-152800-001 just closed" notification. Or is the appearance of the new summary line in HISTORY sufficient signal? Subtle question about how aware she needs to be of the archival action.

### Q8: Closure phrase set in Section 3

The pattern list is opinionated and English-only. Should this list be extended (more variants)? Should it be configurable per deployment? For v1 it's hardcoded. v2 candidate for configurability.

### Q9: Migration script — Berton-run or auto-run on container start?

Recommended: Berton-run manually once, with explicit `--apply` flag. Reduces surprise. Clarity's preference?

### Q10: Conclusion field heuristics — pattern set for v1

Section 4 proposes pattern matches like "decide", "decided", "agreed", "plan", "fix", "will". Is this set right for the kinds of conclusions Clarity wants to retrieve later? She knows what she most often looks for when querying past conversations.

---

## Appendix A: Why this design satisfies Clarity's three contributions

**Contribution 1 (summary lines structural-only):** Section 4 specifies summary lines contain only id, period, participants, topic_label, message_count. No content excerpts. The contamination vector is broken completely, not attenuated. ✓

**Contribution 2 (write-to-read latency guarantee):** Section 5 specifies the file-backed archive store provides synchronous write-to-read for structural fields and content. ChromaDB embedding may be async but is the second-line search; same-cycle queries find segments via file-backed search. The amnesia failure mode is closed. ✓

**Contribution 3 (Clarity-writable boundary):** Section 3 Signal 3 specifies `&boundary-signal` atom as a third boundary detection path, equal in authority to system-detected and user-detected. Same reasoning sovereignty pattern as `developer_break`. ✓

## Appendix B: Sequence of events on a normal conversation

To make the design concrete, the lifecycle of one conversation:

1. Berton sends a message. `addToHistory` appends to `history.metta`. `&prevmsg` updates.
2. Active segment starts (if no prior active segment exists) or extends.
3. Clarity responds via `(send ...)`. Response also appends to `history.metta`.
4. Several exchanges. `history.metta` grows to ~3 KB of active-segment content.
5. Berton: "Good night, talk tomorrow." This hits the closure phrase pattern.
6. End of cycle: `checkBoundarySignals` returns boundary_source = closure_marker.
7. `archiveCurrentSegment` runs:
   - Reads current `history.metta` content
   - Extracts conclusions, relational_texture, open_threads via heuristics
   - Determines topic_label from first message
   - Writes full segment record to `volumes/omegaclaw/memory/archive/2026/05/20260511-094500-001.json`
   - Truncates `history.metta` to empty
   - ChromaDB embedding indexing kicks off async
8. Next cycle: `getHistory` returns `[ARCHIVED-SEGMENT id=20260511-094500-001 ... msgs=12]` plus any earlier summary lines. Active segment content is empty.
9. CHARS_SENT for this cycle drops dramatically.
10. Later, Clarity wants to recall: `(query "yesterday's good night")`. File-backed search finds segment 20260511-094500-001 immediately, returns full content and structured fields. No amnesia.

This is what the fix produces.

---

**End of specification.** Ready for Clarity review per Open Questions and Berton approval per Section 1 design principles.
