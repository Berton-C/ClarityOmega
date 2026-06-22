# Investigation: string-safe encode/decode asymmetry and MM token leak

**Status:** Open. Confirmed mechanism, deferred fix. NOT Sprint 0-Coda scope.
**Date opened:** 2026-05-26
**Surfaced during:** Sprint 0-Coda Phase B, resolution 3 (comparison-level) ground-truth investigation
**Severity:** Low-distraction now; can become ugly if handled without care. Do not touch reactively.
**Related prior work:** String-Safe Restore confidence assessment (commit a318abc / F7 context)

---

## The confirmed mechanism

`string-safe` (src/utils.metta line 22-23) encodes exactly three characters on the way out:

```
(= (string-safe $str)
   (string-replace (string-replace (string-replace $str "\"\"" "_quote_") "\n" "_newline_") "'" "_apostrophe_"))
```

- doublequote → `_quote_`
- newline → `_newline_`
- apostrophe → `_apostrophe_`

`balance_parentheses` (src/helper.py line 70-83) reverses exactly ONE of those three on the way back:

```
def balance_parentheses(s):
    s = s.replace("_quote_", '"').strip()
    ...
```

- `_quote_` → doublequote
- `_newline_` → (no reversal)
- `_apostrophe_` → (no reversal)

The asymmetry is exact and verified in the live container (2026-05-26): 3 tokens encoded, 1 token decoded by `balance_parentheses`. The line-196 comment in helper.py notes `balance_parentheses` diverges from upstream and that T-5 (response-normalization-pipeline simplification) is deferred.

## The observed behavior this explains

Berton reports: when Clarity is more unstable, she sometimes prints `_apostrophe_` and `_newline_` literally in her Mattermost responses. The encoded tokens leak to human-visible output.

The mechanism above explains why: any apostrophe or newline that `string-safe` encoded survives as the literal token because `balance_parentheses` does not reverse it. When output flows through `balance_parentheses` (or any path that does not reverse these two tokens), the encoded form leaks.

## What is NOT yet known (the actual investigation, when it happens)

The asymmetry is confirmed. What is not traced is the full set of OUTPUT PATHS. The leak happening "under instability" rather than always suggests there is more than one output path, and only some of them route through a token-reversal step. The investigation question is:

1. What are all the paths from a `string-safe`-encoded string to human-visible MM output?
2. Which of those paths reverse `_newline_` / `_apostrophe_`, and which do not?
3. Why does instability correlate with hitting the non-reversing path(s)?

The anchor for whoever picks this up: **`balance_parentheses` reverses only `_quote_`; find all output paths and identify where `_newline_` / `_apostrophe_` should reverse but do not.** Do not start from scratch; start from the confirmed asymmetry.

## The constraint any fix MUST respect (load-bearing — do not skip)

Prior work ("String-Safe Restore" confidence assessment) established WHY `string-safe` exists:

Commit a318abc (F7, April 20) introduced a py-call boundary at loop.metta that called `(py-call (helper.safe_results_str (repr $results)))`. When `$results` is an unbound MeTTa variable from an empty match query, Janus refuses to marshal it across the Python boundary, and the container crashes. The fix was to restore the pure-MeTTa pattern `(string-safe (repr $results))` — no boundary crossing, no marshal failure. A prior attempt (69c73fc) that kept `(repr $results)` inside py-call still crashed, because the boundary crossing itself was the problem, not the stringification approach.

**Therefore: `string-safe` is not merely a cosmetic encoder. It is the crash-safe marshal boundary for stringifying possibly-unbound MeTTa values without crossing into Python.** Any fix to the encode/decode asymmetry MUST preserve this marshal-safety role. Naively "fixing" the decode side, or moving stringification across the py-call boundary to make decode symmetric, risks reintroducing the Janus marshal crash that `string-safe` was built to prevent. Root-cause-before-fix applies with extra weight here: the surface solves a real crash, and the encoding is load-bearing for stability, not just for transport hygiene.

## Why this is parked, not chased now

Sprint 0-Coda's Phase D verification sidesteps the asymmetry entirely by comparing at the encoded level — `(string-safe (getSkills))` vs `(string-safe $skills-str)` — where both sides pass through the same three replacements and the comparison is clean and deterministic. Sprint 0-Coda does not depend on the decode side at all. The leak fix is a separate deliberate investigation with its own root-cause-before-fix discipline, to be scheduled when it is the right time, not as a side effect of Sprint 0-Coda.

## Related

- T-5 (response-normalization-pipeline simplification): deferred upstream-catch-up item; `balance_parentheses` divergence is the T-5 territory.
- `normalize_string` (helper.py ~line 85): truncation-cap function, separate backlog item, noted in passing during the same investigation.
