# Governing Principles: Accidental Binding and the Detection Mesh

**Status:** Governing discipline for the detection-mesh build line.
**Provenance:** Emerged from the creative insight on accidental binding (seventh resilience pattern) and the technical analysis of the nine unwired detectors.
**Scope:** Applies to all work described in Latent_Capability_and_the_Detection_Mesh.md and any extension of the detection mesh or self-observation substrate.

---

## The Three-Point Principle

1. **Brittle systems bind accidentally.** They commit without noticing they committed.
2. **Resilient systems bind consciously.** They choose when and how.
3. **You cannot instruct a system to bind consciously.** The noticing itself has to be grown into.

---

## Build Implications

### Wire, do not add
When an unwired detector already detects the problem, wire it. Do not build a new detector that performs consciousness. Unwired detectors are evidence the noticing-capability already exists. Building new detectors while old ones sit unwired is performed consciousness about performed consciousness.

### Temporal, not static
Static binding IS accidental binding. A truth value set once and never revisited is a commitment the system made without noticing it committed. Temporal binding IS conscious binding. Commitments that refresh with use and decay without use are visible, time-stamped, trackable commitments. `lib_temporal_v2` provides these primitives. Wiring them is a build action. Not wiring them is accidental binding by omission.

### Visible, not instructed
Make the moment of binding visible. Do not instruct the system to behave correctly in the moment. The cycle-trace writer does not tell the system to notice its orbits; it makes orbits legible in the evidence the next cycle reads. Visibility grows noticing. Instruction grows compliance. Compliance without noticing is itself accidental binding.

### Grow, do not scaffold
The mesh grows noticing by making binding visible, cycle after cycle. Each cycle that reads its own trace is a cycle that can notice. Scaffolding imposes noticing from outside, which means the system performs noticing when scaffolding is present and reverts when it is not. Performed noticing is not noticing. It is another form of accidental binding.

---

## The Anti-Pattern This Prevents

Adding detectors in response to binding failures instead of wiring the ones that exist.

The sequence goes:
1. A binding failure occurs.
2. The response is to design a new detector for that specific failure.
3. The new detector is built and left unwired, because the producer it needs is the same producer the existing detectors need.
4. Repeat.

The governing principle breaks this cycle at step 2. The correct response to a binding failure is: check whether an existing detector already catches this failure type. If yes, wire it. If no, build the minimum detector and wire it immediately.

---

## Why This Is Self-Applying

A governing principle that itself violates its own discipline is not governing. It is decoration. Therefore:

- Wire, do not add applies to the principle itself. Wire it into artifact tracking.
- Temporal, not static applies to the principle itself. Revisit when mesh state changes.
- Visible, not instructed applies to the principle itself. It makes the shape of the error visible.
- Grow, do not scaffold applies to the principle itself. Wire the evidence stream so the system can see whether it is accidentally binding.

---

## Relationship to Existing Work

| Instrument | What it addresses | Status |
|---|---|---|
| `coupling_integrity_detector` | Accidental coupling | LIVE, WIRED |
| `orbit_detector` | Accidental cycle binding | BUILT, UNWIRED |
| `value_drift_detector` | Accidental priority binding | BUILT, UNWIRED |
| `resonance_reward` | Performed vs genuine growth | BUILT, UNWIRED |
| `goal_completion_checker` | Claim-without-verify binding | BUILT, UNWIRED |
| `lib_temporal_v2` | Static binding primitives | AVAILABLE, UNWIRED |
| `cycle_classifier` | Illegible action types | AVAILABLE |
| cycle-trace writer | Keystone producer | DESIGNED |