# Next Iteration Issue Drafts

Use these as ready-to-file issue entries in GitHub.

## 1) Expand static checks to full Phase-1 core rule set

### Goal
Expand from current initial rules to the full Phase-1 core rule target.

### Scope
- Add remaining high-value rule detections
- Preserve deterministic ordering and schema compatibility
- Add fixture-backed tests for each added rule

### Acceptance Criteria
- Rule count reaches planned Phase-1 baseline
- New checks produce traceable evidence payloads
- CI remains green

## 2) Strengthen R1CS-to-Z3 encoding semantics

### Goal
Improve solver encoding fidelity beyond equality placeholders.

### Scope
- Support richer arithmetic/constraint forms used in Circom pipelines
- Preserve timeout and UNKNOWN fallback guarantees
- Add regression fixtures for known edge patterns

### Acceptance Criteria
- Improved precision without regressions
- Existing tests pass and new solver tests added

## 3) Add deterministic replay snapshot tests for artifact stability

### Goal
Guarantee byte-stable replay outputs where feasible.

### Scope
- Snapshot tests for findings/coverage/attestation outputs
- Deterministic ordering checks for lists/maps
- Document any intentional nondeterministic fields

### Acceptance Criteria
- Replay tests fail on output drift
- Stability expectations documented in methodology
