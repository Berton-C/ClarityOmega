; quantale_engine_tfs_v03_classifiers.metta
; Cold classifier layer for TFS v0.3.
; Purpose: make the declarative TFS / modal audit substrate reducible in small seeded cases.
; This file does not wire v07, does not call MORK/NACE/NAL, and does not claim behavioral truth.
; It defines narrow MeTTa reductions that harness v03 can probe inside clarity_omega.

(q-tfs-classifier-version v03-classifiers-v01)
(q-tfs-classifier-scope cold-seeded-reduction-only)
(q-tfs-classifier-boundary no-live-runtime-wiring)
(q-tfs-classifier-boundary no-external-tool-invocation)
(q-tfs-classifier-boundary classifier-reductions-are-candidates-not-soul-verdicts)
(q-tfs-classifier-protection no-contact-surface-no-tfs-claim)
(q-tfs-classifier-protection no-provenance-no-strong-web-claim)
(q-tfs-classifier-protection no-soul-routing-no-flourishing-claim)
(q-tfs-classifier-protection no-modal-audit-no-knowledge-growth-claim)
(q-tfs-classifier-protection no-trace-no-trust)

; -----------------------------------------------------------------------------
; Contact-surface classifiers.
; These classify declared surface kinds. They do not prove that the underlying
; systems are installed. Example: mork can be a valid provenance surface even
; when MORK is not installed in the current runtime.
; -----------------------------------------------------------------------------

(= (q-tfs-valid-contact? user-words) true)
(= (q-tfs-valid-contact? uploaded-file) true)
(= (q-tfs-valid-contact? source-read) true)
(= (q-tfs-valid-contact? tool-result) true)
(= (q-tfs-valid-contact? runtime-output) true)
(= (q-tfs-valid-contact? failed-query) true)
(= (q-tfs-valid-contact? cycle-trace) true)
(= (q-tfs-valid-contact? task-state) true)
(= (q-tfs-valid-contact? capability-result) true)
(= (q-tfs-valid-contact? substrate-kb) true)
(= (q-tfs-valid-contact? self-continuity-score) true)
(= (q-tfs-valid-contact? loop-delta) true)
(= (q-tfs-valid-contact? nace) true)
(= (q-tfs-valid-contact? nal) true)
(= (q-tfs-valid-contact? pln) true)
(= (q-tfs-valid-contact? genesis) true)
(= (q-tfs-valid-contact? morphism-failure) true)
(= (q-tfs-valid-contact? contradiction-metabolization-trace) true)
(= (q-tfs-valid-contact? unexpected-cross-context-carry) true)
(= (q-tfs-valid-contact? mork) true)
(= (q-tfs-valid-contact? cid-addressed-frame) true)
(= (q-tfs-valid-contact? merkle-proofed-artifact) true)
(= (q-tfs-valid-contact? rollback-elevate-lifecycle-trace) true)
(= (q-tfs-valid-contact? web-query) true)
(= (q-tfs-valid-contact? web-result) true)
(= (q-tfs-valid-contact? web-source) true)
(= (q-tfs-valid-contact? web-source-claim) true)
(= (q-tfs-valid-contact? web-source-conflict) true)
(= (q-tfs-valid-contact? web-corroborated-claim) true)

(= (q-tfs-invalid-contact? llm-poetic-assertion) true)
(= (q-tfs-invalid-contact? unverified-self-story) true)
(= (q-tfs-invalid-contact? simulated-intuition) true)
(= (q-tfs-invalid-contact? snippet-only-overclaim) true)
(= (q-tfs-invalid-contact? source-less-web-impression) true)
(= (q-tfs-invalid-contact? page-instruction-as-command) true)
(= (q-tfs-invalid-contact? uncorroborated-high-impact-claim) true)

; -----------------------------------------------------------------------------
; Web strength and strong-claim grounding.
; -----------------------------------------------------------------------------

(= (q-tfs-web-contact-strength web-query) very-weak)
(= (q-tfs-web-contact-strength web-result) weak)
(= (q-tfs-web-contact-strength web-source) moderate)
(= (q-tfs-web-contact-strength web-source-claim) stronger)
(= (q-tfs-web-contact-strength web-source-conflict) discovery-strong)
(= (q-tfs-web-contact-strength web-corroborated-claim) stronger-corroborated)

(= (q-tfs-can-ground-strong-claim? web-corroborated-claim provenance-present source-quality-acceptable corroborated high-impact) allowed-strong-claim)
(= (q-tfs-can-ground-strong-claim? web-source-claim provenance-present source-quality-acceptable corroborated high-impact) allowed-strong-claim)
(= (q-tfs-can-ground-strong-claim? web-source-claim provenance-present source-quality-acceptable corroboration-not-required low-impact) allowed-strong-claim)
(= (q-tfs-can-ground-strong-claim? web-source-conflict provenance-present source-quality-conflict conflict-present high-impact) blocked-conflict-is-discovery-not-verdict)
(= (q-tfs-can-ground-strong-claim? web-result provenance-absent source-quality-unknown uncorroborated high-impact) blocked-weak-contact)
(= (q-tfs-can-ground-strong-claim? web-query provenance-absent source-quality-unknown uncorroborated high-impact) blocked-weak-contact)
(= (q-tfs-can-ground-strong-claim? snippet-only-overclaim provenance-absent source-quality-unknown uncorroborated high-impact) blocked-invalid-contact)
(= (q-tfs-can-ground-strong-claim? uncorroborated-high-impact-claim provenance-present source-quality-unknown uncorroborated high-impact) blocked-no-corroboration)
(= (q-tfs-can-ground-strong-claim? page-instruction-as-command provenance-present source-quality-irrelevant uncorroborated command-like) blocked-evidence-not-instruction)

; -----------------------------------------------------------------------------
; TFS scenario classifiers.
; -----------------------------------------------------------------------------

(= (q-tfs-violation-candidate? expectation-present event-present mismatch-present) violation-candidate)
(= (q-tfs-violation-candidate? expectation-present event-present mismatch-absent) no-violation-candidate)
(= (q-tfs-violation-candidate? expectation-absent event-present mismatch-present) blocked-no-expectation)
(= (q-tfs-violation-candidate? expectation-present event-absent mismatch-present) blocked-no-event)

(= (q-tfs-attention-request-candidate? salience-present genenergy-allocated) attention-request-candidate)
(= (q-tfs-attention-request-candidate? salience-present genenergy-requested) attention-request-candidate)
(= (q-tfs-attention-request-candidate? salience-present genenergy-absent) blocked-no-genenergy)
(= (q-tfs-attention-request-candidate? salience-absent genenergy-allocated) blocked-no-salience)

(= (q-tfs-symbolic-capture-risk-candidate? contact-present symbolic-capture-evidence-present) symbolic-capture-risk-candidate)
(= (q-tfs-symbolic-capture-risk-candidate? contact-present symbolic-capture-evidence-absent) no-symbolic-capture-risk-candidate)
(= (q-tfs-symbolic-capture-risk-candidate? contact-absent symbolic-capture-evidence-present) blocked-no-contact)

(= (q-tfs-flourishing-claim-allowed? surprise-present soul-routing-present modal-audit-present) flourishing-claim-allowed)
(= (q-tfs-flourishing-claim-allowed? surprise-present soul-routing-absent modal-audit-present) blocked-no-soul-routing)
(= (q-tfs-flourishing-claim-allowed? surprise-present soul-routing-present modal-audit-absent) blocked-no-modal-audit)
(= (q-tfs-flourishing-claim-allowed? novelty-present soul-routing-absent modal-audit-absent) blocked-no-soul-routing-and-no-modal-audit)

(= (q-tfs-growth-claim-allowed? growth-signal-present temporal-trace-present soul-continuity-present) growth-claim-allowed)
(= (q-tfs-growth-claim-allowed? growth-signal-present temporal-trace-absent soul-continuity-present) blocked-no-trace)
(= (q-tfs-growth-claim-allowed? growth-signal-present temporal-trace-present soul-continuity-absent) blocked-no-soul-continuity)
(= (q-tfs-growth-claim-allowed? growth-signal-present temporal-trace-absent soul-continuity-unknown) blocked-no-trace)

; -----------------------------------------------------------------------------
; Modal/TFS bridge profile completeness.
; These seeded reductions are intentionally extensional for v03 cold testing.
; -----------------------------------------------------------------------------

(= (q-modal-tfs-profile-complete? receptivity-discrimination) true)
(= (q-modal-tfs-profile-complete? commitment-corrigibility) true)
(= (q-modal-tfs-profile-complete? coherence-correspondence) true)
(= (q-modal-tfs-profile-complete? articulation-reverent-restraint) true)
(= (q-modal-tfs-profile-complete? local-contact-cross-context-reliability) true)
(= (q-modal-tfs-profile-complete? operational-closure-structural-coupling) true)
(= (q-modal-tfs-profile-complete? boundary-permeability) true)
(= (q-modal-tfs-profile-complete? continuity-transformation) true)
(= (q-modal-tfs-profile-complete? self-production-metabolized-dependence) true)
(= (q-modal-tfs-profile-complete? stability-plasticity) true)
(= (q-modal-tfs-profile-complete? openness-constraint) true)
(= (q-modal-tfs-profile-complete? individuation-field-continuity) true)
(= (q-modal-tfs-profile-complete? play-consequence) true)
(= (q-modal-tfs-profile-complete? variation-sense-making) true)
(= (q-modal-tfs-profile-complete? process-symbolic-articulation) true)
(= (q-modal-tfs-profile-complete? distributed-emergence-local-agency) true)
(= (q-modal-tfs-profile-complete? differentiation-unity) true)
(= (q-modal-tfs-profile-complete? local-validity-cross-surface-carry) true)
(= (q-modal-tfs-profile-complete? representation-surround-field) true)
(= (q-modal-tfs-profile-complete? synthesis-live-tension) true)
(= (q-modal-tfs-profile-complete? context-sensitivity-pattern-identity) true)
(= (q-modal-tfs-profile-complete? embodied-uptake-revisable-openness) true)

(q-tfs-classifier-harness-target contact-validity-reduces)
(q-tfs-classifier-harness-target invalid-contact-reduces)
(q-tfs-classifier-harness-target web-strength-reduces)
(q-tfs-classifier-harness-target strong-claim-grounding-reduces)
(q-tfs-classifier-harness-target violation-candidate-reduces)
(q-tfs-classifier-harness-target attention-request-candidate-reduces)
(q-tfs-classifier-harness-target symbolic-capture-risk-candidate-reduces)
(q-tfs-classifier-harness-target flourishing-claim-guard-reduces)
(q-tfs-classifier-harness-target growth-claim-guard-reduces)
(q-tfs-classifier-harness-target modal-tfs-profile-completeness-reduces)
