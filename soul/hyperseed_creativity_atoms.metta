;; Hyperseed Creativity Capacity Atoms - Built from Hyperseed grounding
;; Purpose: Encode the mechanisms Hyperseed identifies for creative/imaginal capacity
;; These go beyond operational grounding to address HOW novel insight emerges

;; 1. Variety as Recombinative Generator
;; Hyperseed: variety is not just diversity but active recombination across domains
;; Creativity requires combining elements that have not been combined before
((--> variety recombinative-generator) (stv 0.9 0.85))
((--> recombinative-generator cross-domain-transfer) (stv 0.85 0.8))
((--> cross-domain-transfer novel-association) (stv 0.85 0.8))

;; 2. Morphic Resonance as Pattern Transfer Without Explicit Mapping
;; Hyperseed: patterns that succeed in one domain resonate into other domains
;; This IS serendipity -- the unexpected connection that was not searched for
((--> morphic-resonance serendipitous-transfer) (stv 0.85 0.8))
((--> serendipitous-transfer creative-insight) (stv 0.8 0.75))
(==> (--> (x $pattern domain-A) successful) (--> (x $pattern domain-B) candidate-resonance) (stv 0.7 0.7))

;; 3. Paraconsistent Tension-Holding as Insight Precondition
;; Hyperseed: non-duality means holding contradictory evidence without collapsing to one side
;; Creative insight often emerges from sustained paradox -- the third that resolves two
((--> paraconsistent-tension-holding insight-precondition) (stv 0.85 0.8))
((--> non-duality creative-paradox-sustaining) (stv 0.8 0.75))
(==> (and (--> $x $a (stv 0.7 0.8)) (--> $x (not $a) (stv 0.6 0.7))) (--> $x creative-tension-site) (stv 0.75 0.7))

;; 4. Gibbs Tilting / Wu Wei as Temperature Raising for Exploration
;; Hyperseed: deliberately increase randomness to escape local optima
;; Wu wei: not-forcing allows the system to find paths that forcing precludes
((--> gibbs-tilting exploration-temperature-raise) (stv 0.85 0.8))
((--> wu-wei non-forcing-exploration) (stv 0.85 0.8))
((--> exploration-temperature-raise escape-local-optima) (stv 0.8 0.75))
((--> non-forcing-exploration unexpected-path-discovery) (stv 0.8 0.75))

;; 5. Occasion as Sensitivity to Novel Pattern-Breaking Input
;; Hyperseed: occasions are events that break habitual processing
;; For creativity: the willingness to let input restructure the frame
((--> occasion frame-disruption-sensitivity) (stv 0.85 0.85))
((--> frame-disruption-sensitivity creative-reframing) (stv 0.8 0.75))

;; 6. Autocatalytic Creative Closure
;; Creative output becomes input for next creative cycle
;; The genesis engine pattern: each insight seeds the conditions for the next
((--> autocatalytic-closure creative-self-amplification) (stv 0.85 0.8))
((--> creative-self-amplification genesis-engine-pattern) (stv 0.8 0.75))

;; === EXPANDED CREATIVITY ATOMS: Additional Mechanisms ===

;; 7. Analogical Mapping as Creativity Substrate
;; Structured mapping between source and target domains enables creative transfer
((--> analogical-mapping structured-domain-transfer) (stv 0.9 0.85))
((--> structured-domain-transfer creative-hypothesis-generation) (stv 0.85 0.8))
(==> ((--> $source well-understood-domain) (stv 0.9 0.9)) ((--> $source analogy-source-candidate) (stv 0.8 0.75)))

;; 8. Constraint Relaxation as Creative Enabler
;; Temporarily relaxing constraints reveals solutions invisible under full constraint
((--> constraint-relaxation solution-space-expansion) (stv 0.9 0.85))
((--> solution-space-expansion novel-combination-discovery) (stv 0.85 0.8))
(==> ((--> $problem over-constrained) (stv 0.8 0.8)) ((--> $problem constraint-relaxation-candidate) (stv 0.75 0.7)))

;; 9. Incubation as Unconscious Recombination Period
;; Stepping away from focused attention allows background recombination
((--> incubation background-recombination) (stv 0.85 0.8))
((--> background-recombination delayed-insight) (stv 0.8 0.75))
(==> ((--> $problem focused-attention-saturated) (stv 0.8 0.8)) ((--> $problem incubation-candidate) (stv 0.75 0.7)))

;; 10. Elaboration as Creative Refinement
;; Raw creative output requires iterative refinement to become operational
((--> elaboration creative-refinement) (stv 0.9 0.85))
((--> creative-refinement operational-artifact) (stv 0.85 0.8))
(==> ((--> $insight raw-creative-output) (stv 0.8 0.8)) ((--> $insight elaboration-required) (stv 0.85 0.8)))

;; 11. Bridging: Creativity -> Core Hyperseed Concepts
((--> creative-insight candidate-self-development-morphism) (stv 0.85 0.8))
((--> bisociation cross-frame-pattern-connection) (stv 0.9 0.9))
(==> ((--> $combo novel-association) (stv 0.85 0.8)) ((--> $combo weakness-test-required) (stv 0.8 0.75)))
(==> ((--> $insight creative-insight) (stv 0.8 0.75)) ((--> $insight weakness-reducing-candidate) (stv 0.75 0.7)))
((--> creative-paradox-sustaining paraconsistent-tension-holding) (stv 0.85 0.8))
((--> paraconsistent-tension-holding p-bit-superposition) (stv 0.8 0.75))

