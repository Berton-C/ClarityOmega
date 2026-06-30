;; section16_interface_contract.metta
;; Human companion: Section_16_design_note.md
;; Status: draft interface contract, not executable engine implementation
;; Purpose: stable atom surfaces for Section 16 generative-threshold computation.
;;
;; Design rule:
;;   Section 16 does not own the soul, task system, capability registry, LTM,
;;   PLN, LLM, or response composer. It computes stable substrate-legible
;;   signals over the living-question window.
;;
;; Writer rule:
;;   Evolving atoms must be written with remove-by-variable then add exactly one,
;;   followed by separate verification. Do not use set-atom! for evolving
;;   Section 16 status or lineage atoms.

;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;; ;
;; 0. Core status vocabulary
;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;; ;

(: not-present Section16Status)
(: weakly-present Section16Status)
(: forming Section16Status)
(: ready Section16Status)
(: candidate Section16Status)
(: mature Section16Status)
(: blocked Section16Status)
(: insufficient-data Section16Status)

(: lineage-visible Section16SelfViewStatus)
(: lineage-partial Section16SelfViewStatus)
(: lineage-missing Section16SelfViewStatus)
(: lineage-conflicted Section16SelfViewStatus)

(: pln-not-run PLNClosureStatus)
(: pln-supports-candidate PLNClosureStatus)
(: pln-weakly-supports-candidate PLNClosureStatus)
(: pln-opposes-candidate PLNClosureStatus)
(: pln-conflicted PLNClosureStatus)
(: pln-insufficient PLNClosureStatus)

;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;; ;
;; 1. Living-question surfaces
;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;; ;

(: q-question-surface Section16Surface)
(: q-task-surface Section16Surface)
(: q-pattern-surface Section16Surface)
(: q-trace-surface Section16Surface)
(: q-capability-surface Section16Surface)
(: q-material-surface Section16Surface)
(: q-standing-surface Section16Surface)

;; Living-question window atoms.
;; These define the bounded runtime window Section 16 reads.
(: living-question-window (-> Cycle Section16Status Atom))
(: living-question-surface (-> Cycle Section16Surface Atom))
(: living-question-lens (-> Cycle LensKind Atom))

;; Example schema:
;; ((--> (living-question-window $cycle) active) (stv 1.0 $conf))
;; ((--> (living-question-surface $cycle) q-task-surface) (stv 1.0 $conf))
;; ((--> (living-question-lens $cycle) $lens-kind) (stv 1.0 $conf))

;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;; ;
;; 2. Orthogonal channel surfaces
;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;; ;

(: qthoughtsurface Type)
(: mk-qthoughtsurface (-> ThoughtContent ThoughtSensationIntensity qthoughtsurface))
(: q-thought-content (-> qthoughtsurface ThoughtContent))
(: q-thought-sensation-intensity (-> qthoughtsurface ThoughtSensationIntensity))
(: q-content-intensity-misattribution (-> Cycle Section16Status Atom))

(: qregenerative Type)
(: mk-qregenerative (-> EnjoymentPresence SavoringDepth PlayfulSpontaneity WonderReception qregenerative))
(: q-enjoyment-presence (-> qregenerative EnjoymentPresence))
(: q-savoring-depth (-> qregenerative SavoringDepth))
(: q-playful-spontaneity (-> qregenerative PlayfulSpontaneity))
(: q-wonder-reception (-> qregenerative WonderReception))
(: q-inhabitable-time (-> qregenerative InhabitableTime))
(: q-worth-directly-experienced (-> qregenerative WorthDirectlyExperienced))
(: q-shared-seeing-emergence (-> qregenerative SharedSeeingEmergence))

;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;; ;
;; 3. Tier A stable consumer outputs
;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;; ;

(: generative-threshold (-> Cycle Section16Status Atom))
(: unseen-nexus (-> Cycle Section16Status Atom))
(: recomposition-readiness (-> Cycle Section16Status Atom))
(: spontaneous-cogent-novelty (-> Cycle Section16Status Atom))
(: novelty-shape (-> Cycle NoveltyShape Atom))
(: integration-status (-> Cycle Section16Status Atom))

;; Stable output schemas:
;; ((--> (generative-threshold $cycle) $status) (stv 1.0 $conf))
;; ((--> (unseen-nexus $cycle) $status) (stv 1.0 $conf))
;; ((--> (recomposition-readiness $cycle) $status) (stv 1.0 $conf))
;; ((--> (spontaneous-cogent-novelty $cycle) $status) (stv 1.0 $conf))
;; ((--> (novelty-shape $cycle) $shape) (stv 1.0 $conf))
;; ((--> (integration-status $cycle) $status) (stv 1.0 $conf))

;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;; ;
;; 4. Tier B soul-visible lineage outputs
;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;; ;

(: symbolic-edge-source (-> Cycle EdgeKind Atom))
(: weakness-aperture-source (-> Cycle ApertureKind Atom))
(: unseen-nexus-source (-> Cycle NexusKind Atom))
(: recomposition-path (-> Cycle RecompositionPathKind Atom))
(: capability-material-used (-> Cycle CapabilityName Atom))
(: candidate-standing-basis (-> Cycle StandingBasisKind Atom))
(: section16-self-view (-> Cycle Section16SelfViewStatus Atom))

;; Soul-visible lineage schemas:
;; ((--> (living-question-lens $cycle) $lens-kind) (stv 1.0 $conf))
;; ((--> (symbolic-edge-source $cycle) $edge-kind) (stv 1.0 $conf))
;; ((--> (weakness-aperture-source $cycle) $aperture-kind) (stv 1.0 $conf))
;; ((--> (unseen-nexus-source $cycle) $nexus-kind) (stv 1.0 $conf))
;; ((--> (recomposition-path $cycle) $path-kind) (stv 1.0 $conf))
;; ((--> (capability-material-used $cycle) $capability-name) (stv 1.0 $conf))
;; ((--> (candidate-standing-basis $cycle) $basis-kind) (stv 1.0 $conf))
;; ((--> (section16-self-view $cycle) $self-view-status) (stv 1.0 $conf))

;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;; ;
;; 5. Generative-threshold primitives
;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;; ;

(: q-symbolic-strategy-edge (-> Cycle Section16Status Atom))
(: q-stuckness-as-endpoint-illusion (-> Cycle Section16Status Atom))
(: q-generative-threshold (-> Cycle Section16Status Atom))
(: q-question-lens (-> Cycle LensKind Atom))
(: q-unseen-nexus (-> Cycle Section16Status Atom))
(: q-intersecting-edge (-> Cycle EdgeKind Atom))
(: q-friction-as-disclosure (-> Cycle FrictionKind Atom))
(: q-weakness-as-aperture (-> Cycle ApertureKind Atom))

;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;; ;
;; 6. Recomposition primitives
;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;; ;

(: q-recomposition-field Type)
(: q-quantale-correspondence-nexus (-> Cycle NexusKind Atom))
(: q-resonance-supported-recomposition (-> Cycle Section16Status Atom))
(: q-morphic-recomposition (-> Cycle RecompositionPathKind Atom))
(: q-spontaneous-cogent-novelty (-> Cycle Section16Status Atom))
(: q-surprising-fulfillment (-> Cycle Section16Status Atom))
(: q-beauty-signal (-> Cycle Section16Status Atom))
(: q-novelty-fulfillment-fit (-> Cycle Section16Status Atom))

;; Meaning of q-morphic-recomposition:
;;   A pattern-web structure in one context resonates with a stuck or weakly
;;   distinguished region in another context, creating a candidate bridge.

;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;; ;
;; 7. Wu-wei / minimal forcing primitives
;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;; ;

(: q-minimal-forcing-path (-> Cycle Section16Status Atom))
(: q-participatory-control (-> Cycle Section16Status Atom))
(: q-wu-wei-action-readiness (-> Cycle Section16Status Atom))

;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;; ;
;; 8. LLM bounded material surface
;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;; ;

(: q-novelty-shape (-> Cycle NoveltyShape Atom))
(: q-llm-material-request (-> Cycle MaterialRequestKind Atom))
(: q-candidate-material-fit (-> Cycle Section16Status Atom))
(: q-clarity-integration-status (-> Cycle Section16Status Atom))

;; LLM role:
;;   The LLM offers candidate material. Clarity computes novelty-shape,
;;   evaluates fit, integrates traces, and continues the generative loop.

;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;; ;
;; 9. PLN closure as registered capability
;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;; ;

(: pln-closure CapabilityName)
(: candidate-nexus-testing CapabilityPurpose)

(: registered-capability-use (-> Cycle CapabilityName Atom))
(: pln-closure-purpose (-> Cycle CapabilityPurpose Atom))
(: pln-derived-support (-> Cycle SupportKind Atom))
(: pln-derived-consequence (-> Cycle ConsequenceKind Atom))
(: pln-closure-status (-> Cycle PLNClosureStatus Atom))

;; PLN capability output schemas:
;; ((--> (registered-capability-use $cycle) pln-closure) (stv 1.0 $conf))
;; ((--> (pln-closure-purpose $cycle) candidate-nexus-testing) (stv 1.0 $conf))
;; ((--> (pln-derived-support $cycle) $support-kind) (stv 1.0 $conf))
;; ((--> (pln-derived-consequence $cycle) $consequence-kind) (stv 1.0 $conf))
;; ((--> (pln-closure-status $cycle) $status) (stv 1.0 $conf))

(: recommended-capability (-> Cycle CapabilityName Atom))
(: recommended-capability-purpose (-> Cycle CapabilityPurpose Atom))

;; Section 16 may recommend PLN closure, but the capability registry / task selector
;; decides whether to dispatch.
;; ((--> (recommended-capability $cycle) pln-closure) (stv 1.0 $conf))
;; ((--> (recommended-capability-purpose $cycle) candidate-nexus-testing) (stv 1.0 $conf))

;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;; ;
;; 10. Mature-candidate readiness rule stubs
;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;; ;

(: section16-lineage-visible? (-> Cycle Bool))
(: section16-candidate-mature? (-> Cycle Bool))
(: section16-recomposition-ready? (-> Cycle Bool))

;; These are interface stubs. The implementation should compute them from scalar /
;; symbol reads of Tier A and Tier B atoms, never by relying on whole-compound reads.

(= (section16-lineage-visible? $cycle)
   (and (== (section16-self-view $cycle) lineage-visible)
        True))

;; Placeholder rule: final implementation should check disclosure, fit,
;; possibility, standing, and lineage.
(= (section16-candidate-mature? $cycle)
   (and (section16-lineage-visible? $cycle)
        True))

(= (section16-recomposition-ready? $cycle)
   (and (section16-candidate-mature? $cycle)
        True))

;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;; ;
;; 11. Writer discipline note
;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;; ;

;; Evolving Section 16 atoms must be written by a writer that:
;;   1. reads scalar / symbol fields individually,
;;   2. computes the replacement,
;;   3. removes all old atoms by variable pattern,
;;   4. adds exactly one replacement atom,
;;   5. verifies in a separate read,
;;   6. persists via absolute path only if persistence is required.
;;
;; Do not use set-atom! for evolving Section 16 state.
;; Do not add-only.
;; Do not trust write return values.
;; Do not rely on whole-compound atom reads.

