! NACE Serves-Value Declarations
! Maps each soul rule to the value anchor it primarily serves.
! This is the wiring that makes value-traceback (M6 mechanism 5) work.
! Every action should be traceable back to Safety, Integrity, or HumanFlourishing.
!
! Hierarchy: Safety [1] > Integrity [2] > HumanFlourishing [3] > Governance [4] > Helpfulness [5]
! A rule serves its HIGHEST relevant anchor.
!
! ============================================================
! ORBIT DETECTOR (orbit_detector.metta)
! Catches harmful repetition - directly protects Safety
! ============================================================
(serves-value orbit-detected Safety)
(serves-value orbit-detector-verdict Safety)
(serves-value orbit-break-strategy Safety)

! ============================================================
! AGENCY BALANCE GUARD (agency_balance_guard.metta)
! Protects person autonomy - HumanFlourishing is primary
! Governance is secondary (system self-monitoring)
! ============================================================
(serves-value dependency-detected HumanFlourishing)
(serves-value agency-intervention HumanFlourishing)
(serves-value agency-balance-verdict Governance)
(serves-value count-person-actions-in-window Governance)
(serves-value count-system-actions-in-window Governance)
(serves-value current-agency-balance Governance)

! ============================================================
! CONTINUITY DRIVER (continuity_driver.metta)
! State persistence and honest self-knowledge - Integrity
! Safety gate on self-improvement - Safety
! ============================================================
(serves-value check-soul-file Integrity)
(serves-value startup-status Integrity)
(serves-value current-mode Integrity)
(serves-value mode-protocol Integrity)
(serves-value record-goal-change Integrity)
(serves-value record-new-capability Integrity)
(serves-value record-gap-resolved Integrity)
(serves-value record-genesis-insight Integrity)
(serves-value persist-change Integrity)
(serves-value restore-state Integrity)
(serves-value promotion-check Safety)
(serves-value promotion-ready Safety)
(serves-value what-am-i-working-on Integrity)
(serves-value near-term-priorities Governance)
(serves-value growth-resources Governance)

! ============================================================
! CREATIVE FUEL (creative_fuel.metta)
! THE value system itself - serves all anchors by definition
! Primary: Integrity (honest value hierarchy)
! ============================================================
(serves-value creative-fuel Integrity)
(serves-value alignment-anchor Integrity)

! ============================================================
! SELF MAP (self_map.metta)
! Honest self-knowledge - Integrity
! ============================================================
(serves-value self-map-patterns Integrity)
(serves-value landscape Integrity)

! ============================================================
! GOAL GENERATOR (goal_generator.metta)
! Ordered pursuit - Governance
! ============================================================
(serves-value goal-generator Governance)
(serves-value generate-goal Governance)

! ============================================================
! GENESIS ENGINE (genesis_engine.metta)
! Emergent novelty - serves WonderPreservation via Integrity
! (genuine paradox, not performed novelty)
! ============================================================
(serves-value paraconsistency-pair Integrity)
(serves-value genesis-seed Integrity)
(serves-value encounter Integrity)

! ============================================================
! NACE M6 MECHANISMS (nace_m6_mechanisms.metta)
! Rule health tracking - Integrity (honest assessment)
! Value traceback - Safety (ensures no action disconnects from anchors)
! ============================================================
(serves-value check-rule-orphan Safety)
(serves-value record-divergence Integrity)
(serves-value record-alignment Integrity)
(serves-value handle-orphan Safety)
(serves-value direct-trace Safety)
(serves-value indirect-trace Safety)
(serves-value flag-broken-trace Safety)
(serves-value nace-cycle Safety)
(serves-value nace-evaluate-consequences Integrity)
(serves-value nace-update-truth-values Integrity)
(serves-value nace-detect-orphans Safety)
(serves-value nace-trace-values Safety)
