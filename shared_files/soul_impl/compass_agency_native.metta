; Compass Agency Dimension — Native MeTTa NAL Atoms
; Ported from Python compass_semantic_scorer.py AGENCY_NEIGHBORHOOD
; Concept proximity expressed as inheritance with stv confidence = proximity weight

; Core agency concepts — stv confidence IS the proximity weight
(--> option agency-concept (stv 1.0 0.9))
(--> choice agency-concept (stv 1.0 0.9))
(--> choose agency-concept (stv 0.95 0.9))
(--> decide agency-concept (stv 0.9 0.9))
(--> decision agency-concept (stv 0.9 0.9))
(--> alternative agency-concept (stv 0.85 0.9))
(--> autonomy agency-concept (stv 0.9 0.9))
(--> empower agency-concept (stv 0.9 0.9))
(--> consider agency-concept (stv 0.85 0.9))
(--> tradeoff agency-concept (stv 0.85 0.9))
(--> preference agency-concept (stv 0.8 0.9))
(--> freedom agency-concept (stv 0.8 0.9))
(--> path agency-concept (stv 0.8 0.9))
(--> approach agency-concept (stv 0.8 0.9))
(--> weigh agency-concept (stv 0.8 0.9))
(--> control agency-concept (stv 0.75 0.9))
(--> could agency-concept (stv 0.75 0.9))
(--> direction agency-concept (stv 0.7 0.9))
(--> might agency-concept (stv 0.7 0.9))

; Agency to compass dimension
(--> agency-concept compass-agency (stv 1.0 0.9))

; Scoring via deduction: if a response-token inherits agency-concept,
; and agency-concept inherits compass-agency, NAL deduction yields
; compass-agency membership with truth value reflecting proximity weight.
; Example: (--> option agency-concept (stv 1.0 0.9)) + (--> agency-concept compass-agency (stv 1.0 0.9))
; |- yields (--> option compass-agency) with derived stv
