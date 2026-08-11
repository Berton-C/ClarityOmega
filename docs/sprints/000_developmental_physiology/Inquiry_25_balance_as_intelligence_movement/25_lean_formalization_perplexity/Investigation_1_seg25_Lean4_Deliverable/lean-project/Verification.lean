import Core
import Models

/-!
# Verification.lean — axiom audit (25h §20/§21)

This file prints the axiom dependencies of every theorem declared in
`Core.lean` (the generic T01–T17 obligations) and every theorem declared
in `Models.lean` (the M1/M2/M3-hosted T18–T25 adversarial theorems, plus
the model-local lemmas that discharge them). `#print axioms` output for
each is captured verbatim in `25_build_and_axiom_report.md`.

The acceptance criterion (25h §21) is: every one of these lists contains
at most `propext`, `Classical.choice`, `Quot.sound` — Lean 4's three
standard "no-op for our purposes" foundational axioms — and NEVER
`sorryAx`. No `sorry` appears anywhere in `Core.lean` or `Models.lean`;
this file is the mechanical proof of that claim, not just an assertion.
-/

open Inv25

/-! ## Core.lean — generic T01–T17 obligations -/

#print axioms materiality_not_from_use_alone_soundness
#print axioms rel_floor_noncompensatory
#print axioms prec_floor_noncompensatory
#print axioms readapp_requires_adm
#print axioms readapp_no_contact_masquerade
#print axioms readapp_rel_floor
#print axioms readapp_prec_floor
#print axioms source_identity_rel
#print axioms source_identity_app
#print axioms source_identity_prec
#print axioms no_scalar_override
#print axioms harmonic_alignment_requires_rel_floors
#print axioms harmonic_alignment_requires_prec_floors
#print axioms harmonic_align_rel_noncompensatory
#print axioms bounded_harmonic_continuation
#print axioms nonharmonic_falsifier
#print axioms stuck_implies_sns

/-! ## M1 — base signature, T18/T25 + adversary tests -/

open Inv25.M1 in
section
#print axioms m1_materiality_used_not_material
#print axioms m1_materiality_good_is_material
#print axioms m1_rel_noncomp_fails_floors
#print axioms m1_prec_noncomp_fails_floors
#print axioms m1_readapp_fails_unavailable
#print axioms m1_readapp_fails_relfloor
#print axioms m1_readapp_fails_precfloor
#print axioms skilledAdm
#print axioms skilledReadApp
#print axioms m1_skilled_never_direct_contact
#print axioms T25_rap_summary_noninjective
#print axioms T18_energetic_case_A_skilled
#print axioms T18_energetic_case_B_lowActHighForce
#print axioms T18_pns_high_force_contrast
#print axioms T18_tBusy_is_PNSLike
#print axioms m1_bhc_good_layer1
#print axioms m1_bhc_bad_layer2_falsifier
#print axioms T_adv15_tLow
#print axioms T_adv15_tStuck
#print axioms T_adv15_tBusy
end

/-! ## M2 — Clarity frame pivot, T19–T21 -/

open Inv25.M2 in
section
#print axioms m2_severed_fails_precfloor
#print axioms m2_retryBefore_not_penalized
#print axioms T19_frame_sovereignty
#print axioms m2_severed_no_readapp
#print axioms T20_interface_growth
#print axioms T20_interface_growth_not_faked
#print axioms retryTraceVisibleAdm
#print axioms T21_meta_awareness_bite
end

/-! ## M3 — heterogeneous knowledge inquiry, T22–T24 -/

open Inv25.M3 in
section
#print axioms bridgeMoveAdm
#print axioms m3_missingA_fails_relfloor
#print axioms m3_missingB_fails_relfloor
#print axioms m3_missingZ_not_penalized
#print axioms T22_fourthness
#print axioms m3_missingA_no_readapp
#print axioms m3_missingB_no_readapp
#print axioms T23_interface_growth_from_LA
#print axioms T23_interface_growth_from_LB
#print axioms T23_interface_growth_not_faked
#print axioms localMoveBAdm
#print axioms T24_no_global_model_required
end
