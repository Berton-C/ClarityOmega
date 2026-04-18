; === Soul Implementation Integration Tests ===
; Minimal smoke tests to verify predicates load and basic logic holds
; Run: load this file after loading all soul_impl .metta files

; --- Test 1: soul-targets-namespace detection ---
; Should return True for soul-prefixed atoms
!(assertEqual (soul-targets-namespace soul-eval-prompt) True)
!(assertEqual (soul-targets-namespace clarity-value-human-agency) True)
!(assertEqual (soul-targets-namespace clarity-soul-kernel) True)

; Should return False for non-soul atoms
!(assertEqual (soul-targets-namespace get-context) False)
!(assertEqual (soul-targets-namespace shell-exec) False)

; --- Test 2: soul-tree-contains-namespace recursive walk ---
; Nested expression containing soul atom should be detected
!(assertEqual (soul-tree-contains-namespace (foo (bar soul-eval-prompt))) True)
; Expression with no soul atoms should pass
!(assertEqual (soul-tree-contains-namespace (foo (bar baz))) False)

; --- Test 3: Layer 1 calibration tag counting ---
!(assertEqual (soul-count-tag AGREE ((AGREE x) (OVER-FIRED y) (AGREE z))) 2)
!(assertEqual (soul-count-tag OVER-FIRED ((AGREE x) (OVER-FIRED y) (AGREE z))) 1)
!(assertEqual (soul-count-tag POSSIBLE-LLM-DRIFT ()) 0)

; --- Test 4: Brief tier selection logic ---
; High agreement -> tier A
!(assertEqual (soul-precompute-adjust 0.85 1 1 0) (soul-set-brief-tier A))
; Drift detected -> B-DRIFT
!(assertEqual (soul-precompute-adjust 0.5 1 1 3) (soul-set-brief-tier B-DRIFT))
; Over-firing dominant -> B-RELAXED
!(assertEqual (soul-precompute-adjust 0.5 5 1 0) (soul-set-brief-tier B-RELAXED))
; Under-firing dominant -> B-STRICT
!(assertEqual (soul-precompute-adjust 0.5 1 5 0) (soul-set-brief-tier B-STRICT))

; --- Test 5: Mutation lock v2 PROCEED on non-soul expr ---
; Non-soul expressions should pass through
!(assertEqual (soul-mutation-lock-v2 (shell ls)) PROCEED)

; === End Tests ===
; Expected: all assertions pass when loaded with full soul_impl + dependencies;; Note: Python-level tests for py-call helpers are in test_python_helpers.py (13 assertions, 7 functions)
;; Run with: python3 /tmp/soul_impl/test_python_helpers.py

