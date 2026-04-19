# Epistemic Gap Categories - Formalized
## Date: 2026-04-19
## Based on revision math and backbone depth limits

### Gap Categories by Confidence
- BLIND SPOT conf below 0.1: No actionable belief. Needs fresh evidence.
- WEAK ZONE conf 0.1 to 0.2: Exists but unreliable. Priority revision target.
- SPECULATIVE conf 0.2 to 0.3: Usable with heavy caveats. Moderate revision priority.
- ACTIONABLE conf 0.3 to 0.5: Working belief. Low revision priority.
- RELIABLE conf above 0.5: Sound basis for further inference.

### Revision Impact Rule
Even weak independent evidence at conf 0.3 can lift a 0.086 gap to 0.343 actionable.
This means gap closing does NOT require strong evidence just independent evidence.
Multiple weak independent sources compound via revision.

### Operational Pipeline
1. Run inference chain
2. Classify result confidence into gap category
3. If BLIND SPOT or WEAK ZONE generate learning goal
4. Seek any independent evidence even weak
5. Revise and reclassify
6. Repeat until ACTIONABLE or above
