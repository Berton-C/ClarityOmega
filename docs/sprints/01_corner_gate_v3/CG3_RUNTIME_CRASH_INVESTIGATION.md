# Corner-Gate v3 Runtime Crash Investigation

**Date:** 2026-07-12
**Status:** ROOT CAUSE PROVEN; MINIMAL CORRECTION PROVEN; PRODUCTION REPOSITORY NOT YET MODIFIED
**Incident:** Payload A.4 / Step B.2 applied and rebuilt successfully, but the ClarityOmega container exited with code 2 at the end of iteration 1 and entered its restart policy.

## 1. Investigation commitment

This investigation followed the established procedural commitment:

* Small, reversible tests.
* One variable changed at a time.
* Each test began with a stated hypothesis.
* Findings were recorded before proceeding.
* No production fix was applied until the causal mechanism and correction were independently proven.
* The production container remained down during investigation.

## 2. Original runtime failure

The application completed model execution during iteration 1. It failed when the retired Corner-Gate shim attempted to append the new coupling-legibility line:

```text
ERROR: /PeTTa/src/main.pl:23: user:main
'gate-aware-results'/2:
Unknown procedure: 'coupling-legibility-line'/1
```

The container exited with code 2.

Initial interpretation:

* `gate-aware-results` had loaded.
* `coupling-legibility-line` had not become callable.
* The missing predicate could have resulted from file identity, import path, import ordering, image skew, namespace resolution, or an earlier payload compilation failure.

## 3. Environmental facts established

The following possibilities were tested and eliminated:

1. **Wrong target path:** disproven.
   The active files were located under `soul/corner_gap/`.

2. **Definition/call spelling mismatch:** disproven.
   `coupling-legibility-line` was defined and the gate called the exact same symbol.

3. **Wrong import order:** disproven.
   Production ordering was:

   ```text
   v08.7.2 engine
   → coupling_legibility
   → coupling_legibility_writers
   → corner_gate
   ```

4. **Duplicate active files:** disproven.
   Only one active copy of each relevant payload existed.

5. **Installer copy corruption:** disproven.
   Payload source and installed destination were byte-identical.

6. **Stale rebuilt image:** disproven.
   The image’s active `lib_clarity_reasoning.metta` and `src/helper.py` were byte-identical to the host files.

7. **Missing Python helper payload:** disproven.
   The v3 formatter and target/signature helpers were present in the rebuilt image.

8. **Working-directory mismatch:** tested and eliminated.

9. **Missing OmegaClaw bootstrap:** corrected in the probe; the payload still failed to register.

## 4. Compilation boundary

An inline production-runtime probe established that the pure payload began compiling successfully.

Compilation completed through:

```text
coupling-legibility-schema-version
coupling-lower-band
coupling-upper-band
coupling-contains
coupling-max-num
coupling-min-num
coupling-mid-ord
coupling-dedupe
```

The transpiler then failed before emitting `coupling-known-heads`:

```text
length/2:
Domain error: `not_less_than_zero' expected, found `-10'
```

This bounded the first failing form to:

```metta
(= (coupling-known-heads)
   (write-file append-file shell remember read-file query episodes metta
    send pin search tavily-search technical-analysis))
```

No hidden or non-ASCII characters existed in this source interval.

## 5. Proven root cause

The expression above was intended as a literal list of command-head symbols.

Because `write-file` was already a callable function, the transpiler interpreted the expression as a call:

```text
write-file(argument-1, argument-2, ... argument-12)
```

rather than as list data.

The known `write-file` arity was 2, while the expression supplied 12 apparent arguments:

```text
2 - 12 = -10
```

This exactly explains the transpiler’s negative-length error.

The pure payload import aborted before later definitions—including `coupling-legibility-line`—were registered. The surrounding import process continued. At the end of iteration 1, `gate-aware-results` called the absent predicate and terminated the process.

## 6. Differential proof

Test T17 changed only the first list element:

```text
write-file
→ cg3-inert-list-head
```

The same expression then compiled successfully as list data.

This proved that the callable head symbol, rather than expression length, hidden characters, or later payload logic, caused the transpiler failure.

## 7. Consumer contract

`coupling-known-heads` has only two production consumers:

```metta
(surface-for-head-total $h)
(command-class-of-total $h)
```

Both consume it exclusively as a membership set through `coupling-contains`.

No active consumer:

* renders the full list;
* depends on its ordering;
* depends on its length;
* compares the full structure;
* or requires `write-file` to occupy expression-head position.

## 8. Proven minimal correction

The tested correction is:

```metta
(= (coupling-known-heads)
   (let $tagged
        (coupling-known-heads-data
          write-file append-file shell remember read-file query episodes metta
          send pin search tavily-search technical-analysis)
     (cdr-atom $tagged)))
```

Mechanism:

1. `coupling-known-heads-data` is an inert tag.
2. The transpiler therefore treats the expression as data.
3. `cdr-atom` removes the tag.
4. Callers receive exactly the intended thirteen-symbol list beginning with `write-file`.

## 9. Semantic proof

Test T19 produced:

```text
(write-file append-file shell remember read-file query episodes metta
 send pin search tavily-search technical-analysis)
```

Membership behavior:

```text
write-file          → true
technical-analysis  → true
unknown-head        → false
```

No domain error occurred.

## 10. Complete-payload proof

Test T20 applied only the proven correction to a temporary copy of the full pure payload.

Results:

```text
schema                    → v3-18-field
write-file surface        → runtime-output
write-file command class  → action-class
unknown surface           → no-contact
unknown command class     → neutral
```

`coupling-legibility-line` compiled and returned:

```text
COUPLING-STATE: contact 0/none |
chain window-filling |
accord window-filling |
band window-filling |
support 0.00 |
residual window-filling |
trajectory window-filling |
next window-filling
```

No domain error, unresolved procedure, syntax error, or parse error occurred.

The proven corrected candidate hash was:

```text
0665131e1491bced69a8ab3e5870637a6a9757b45375fee3095d17ade540cc81
```

## 11. Production-import closure proof

Test T21b used:

* the real production image;
* the real `lib_omegaclaw` bootstrap;
* the real `lib_clarity_reasoning` manifest;
* the real writers payload;
* the real `corner_gate`;
* a temporary complete soul tree differing in exactly one file;
* the corrected pure payload.

The real import chain succeeded:

```text
lib_omegaclaw
→ lib_clarity_reasoning
→ coupling_legibility
→ coupling_legibility_writers
→ corner_gate
```

`gate-aware-results` compiled and returned:

```text
(RESULTS:
  ((COUPLING-STATE-LINE COUPLING-STATE: ...)
   probe-result))
```

This proved that:

* `coupling-legibility-line` was callable;
* `gate-aware-results` successfully invoked it;
* the synthetic result was preserved;
* the coupling line was appended;
* the exact production import seam was functional.

## 12. Validation gap exposed

The original validation harness primarily inlined or directly combined payload contents.

That proved payload semantics under harness loading but did not prove:

```text
real production manifest
→ real transpiler import
→ complete payload compilation
→ gate dependency closure
```

A permanent production-import closure gate must be added to the validator.

It must require:

* `coupling-legibility-schema-version = v3-18-field`;
* exact known-head membership behavior;
* `write-file → runtime-output`;
* `write-file → action-class`;
* unknown head → `no-contact`;
* unknown head → `neutral`;
* ground `COUPLING-STATE` rendering;
* `gate-aware-results` preserving a synthetic result;
* no domain error;
* no unresolved procedure.

## 13. Durable constraints

1. Do not place a known callable symbol in head position when a parenthesized expression is intended as data.
2. Do not treat process exit code 0 as proof that a MeTTa expression reduced; unknown expressions may remain inert.
3. Validate real production import closure, not only concatenated or inline payload behavior.
4. Payload identity must be updated after the correction.
5. The installer, validator, and identity manifest must agree on the corrected pure-payload hash.
6. The failed installed state must be reversed and baseline restoration verified before the corrected artifact set is applied.

## 14. Next procedural phase

1. Commit this investigation record and focused evidence only.
2. Reverse the failed v3 installation using the exact installer that performed it.
3. Verify pre-v3 hashes and reversed topology.
4. Produce Payload A.5 / Step B.3 with the proven correction.
5. Add the permanent production-import closure regression.
6. Refresh all affected hashes.
7. Run installer dry-run.
8. Run static and disposable production-import validation.
9. Commit the corrected reviewed artifact set.
10. Apply, rebuild, and perform a bounded live smoke test before restoring normal operation.
