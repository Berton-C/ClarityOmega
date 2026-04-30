# Debugging Protocol - Agreed 2026-04-28

## Context
Established after wake-issue debug session where analysis was sound
but delivery was sloppy and artifact type was wrong.

## Protocol Steps

1. **TRACE before theorizing**
   - grep/find actual entry points first
   - Follow real call chain with evidence
   - Show actual file contents and outputs

2. **Confirm artifact type before writing**
   - Ask: design doc, patch, or analysis?
   - Ask: what path should it live at?
   - Design files document WHAT and WHY
   - Functional code documents HOW
   - Know which one is needed

3. **One file per cycle**
   - Write one file, confirm it landed
   - Then write the next
   - No batching that compounds format risk

4. **Evidence over narrative**
   - Show real outputs not reconstructed logic
   - Actual grep results, actual file contents
   - If hypothesizing, label it as hypothesis

5. **Multi-part debugging with stacking dependencies**
   - Map the dependency chain first
   - Identify which layer is actually failing
   - Fix bottom-up not top-down
   - Verify each layer before moving up
