# Coverage and Evidence Methodology

This document defines how ZKAuditCore computes and reports coverage and how findings are tied to verifiable evidence.

## Coverage Model

Coverage is computed over circuit constraints with explicit exclusions.

- **Total constraints**: all parsed constraints in the IR
- **Excluded constraints**: constraints marked as pass-through/trivial
- **Verified constraints**: non-excluded constraints that were checked by configured rule/solver stages
- **Unverified constraints**: non-excluded constraints not checked, with reason tags

Reported percentage:

- `verified_percent = verified_constraints / (total_constraints - excluded_constraints)`

## Exclusion Rules

Current MVP excludes pass-through constraints that do not materially contribute to security properties. Exclusions are recorded explicitly so coverage claims remain auditable.

## Finding Traceability

Each finding includes evidence references when available:

- `rule_id`
- `constraint_ref` or `signal_ref`
- `solver_status`
- `proof_trace`

This allows deterministic linkage from output artifacts back to analysis inputs.

## Reproducibility Inputs

Attestation manifests capture:

- Input hash
- IR hash
- Rule set version
- Solver identity and timeout settings
- Execution environment fingerprint

These fields support replay checks and attestation verification.
