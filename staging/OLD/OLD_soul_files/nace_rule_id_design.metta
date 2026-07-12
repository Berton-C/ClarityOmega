! NACE Rule-ID + Network-Tag Design (Draft)
! Status: awaiting human review before implementation
! 
! PROBLEM: Rules are anonymous (=) definitions. No stable handle for NACE to attach
! truth values, track consequences, or attribute to networks.
!
! DESIGN DECISIONS:
!
! 1. RULE-ID SCHEME
!    Shape: (rule-meta <rule-name> <network-tag>)
!    - rule-name: explicit symbol, not inferred from function head
!    - network-tag: SN | FPN | DMN
!    - Added ALONGSIDE rules, not replacing them
!
!    Example:
!    (= (orbit-detected $action-type $count)
!       (if (>= $count (orbit-threshold)) True False))
!    (rule-meta orbit-detector-default SN)
!
!    The rule-name should reference the module + disambiguator, not be auto-generated.
!    Two rules with same head shape get different names.
!
! 2. TRUTH VALUES ON RULES
!    Shape: (rule-stv <rule-name> (stv $strength $confidence))
!    - Separate from rule-meta to allow independent revision
!    - NACE updates these based on consequence-evidence
!
!    Example:
!    (rule-stv orbit-detector-default (stv 0.9 0.5))
!
! 3. CONSEQUENCE-EVIDENCE CHANNEL
!    Shape: (consequence-evidence $producing-network $producing-rule $consuming-network $evaluated-consequence)
!    - producing-network: SN | FPN | DMN (who generated the output)
!    - producing-rule: matches rule-name from rule-meta
!    - consuming-network: who acted on it
!    - evaluated-consequence: judged against Layer 1+2 values
!
!    Example:
!    (consequence-evidence SN orbit-detector-default FPN action-appropriate)
!
! 4. LIFECYCLE
!    - Rule fires -> record (consequence-evidence ...) atom in &self
!    - NACE reads consequence-evidence stream
!    - Updates (rule-stv ...) via revision
!    - Flags rules where consequence diverges from intent
!
! OPEN QUESTIONS FOR HUMAN:
! - Is (rule-meta name network) the right shape, or should network be a separate atom?
! - Should rule-stv start at (stv 0.5 0.5) for all new rules, or vary by network?
! - Should consequence-evidence atoms expire after N cycles, or persist forever?
! - What evaluates consequence against Layer 1+2 values? A dedicated atom? Human review?
