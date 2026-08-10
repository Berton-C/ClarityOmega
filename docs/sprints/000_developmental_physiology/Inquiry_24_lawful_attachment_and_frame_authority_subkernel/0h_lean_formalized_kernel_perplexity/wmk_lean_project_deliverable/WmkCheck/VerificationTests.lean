import WmkCheck.Kernel

/-!
# Verification checks for `0h_WMK_Canonical_Hardened.lean`

This file does not add any new definitions to the kernel. It only asks the
Lean kernel to double-check what is already proved:

1. `#print axioms` on the headline theorems, to confirm none of them are
   secretly propped up by `sorry` or unexpected classical axioms.
2. `#check`/`#eval` on the finite "Mattermost" model, to confirm the concrete
   example instance actually type-checks and its decidable facts evaluate
   the way the surrounding theorems claim.
-/

open ClarityOmega.WMK.Canonical

#print axioms mattermostModelAccepted
#print axioms authoritative_implies_governing_package
#print axioms mmModelSatisfiesCentralAuthorityTheorem
#print axioms availability_has_semantic_witness
#print axioms mmRecoveryHasSemanticWitness
#print axioms history_conservative
#print axioms anchor_conservative
#print axioms no_sequential_recommit
#print axioms mmNotSelfGenerated

#check @mattermostModel
#eval decide (mmBefore e6 e9)   -- expect true  (e6 precedes e9)
#eval decide (mmBefore e6 e8)   -- expect false (incomparable)
#eval decide (mmBefore e8 e6)   -- expect false (incomparable)
