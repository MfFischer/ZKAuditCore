# ZKAuditCore v0.1.0-mvp Release Notes

## Highlights

- Deterministic CLI workflow for ZK audit artifact generation
- Typed findings and coverage schema with evidence traceability
- Z3-based solver outcomes with explicit `SAT/UNSAT/UNKNOWN` semantics
- Reproducibility manifest and Sigstore signing integration

## Included Commands

- `zk-auditcore analyze`
- `zk-auditcore report`
- `zk-auditcore attest`
- `zk-auditcore verify`
- `zk-auditcore replay`

## Known MVP Limits

- Circom-focused ingestion only
- Reduced initial core rule set
- No protocol-level or multi-framework analysis

## Recommended Next Iteration

- Extend core rules toward full Phase-1 target
- Improve richer R1CS-to-Z3 expression encoding
- Add deterministic replay snapshot tests
