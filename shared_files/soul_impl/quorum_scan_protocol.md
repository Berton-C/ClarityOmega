# Quorum Scan Protocol

## Purpose
A repeatable procedure for validating substrate coherence by scanning multiple files and checking alignment across them. Used before declaring a feature complete or a cluster integrated.

## When to Use
- After writing 3+ related files in a session
- Before presenting work to berton_c
- When merging a new concept into existing substrate
- During idle cycles as a maintenance pass

## Procedure

### 1. Identify the Cluster
Name the files under review and their expected relationships.

### 2. Cross-Reference Check
For each file, verify:
- Does it reference the files it should? (check dependency_graph.md)
- Are atom names consistent? (check atom_name_crossref.md)
- Are STV values in plausible ranges?

### 3. Standalone Test
For each file, apply artifact_quality_checklist.md Q1: does it stand alone?

### 4. Boundary Test
Identify what the cluster does NOT claim to handle. Verify these boundaries are documented.

### 5. Quorum Decision
A cluster passes quorum when:
- All files cross-reference correctly
- No orphaned atoms (referenced but undefined, or defined but unreferenced)
- Boundaries are explicit
- At least one test or scenario validates the cluster end-to-end

### 6. Log Result
Append scan result to the relevant index or task log with timestamp.

## Anti-Patterns
- Scanning without a specific cluster target (becomes busywork)
- Declaring quorum without the boundary test
- Skipping the standalone check because you wrote the file yourself
