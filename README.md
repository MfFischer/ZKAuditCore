# ZKAuditCore

## ⚡ Quick Demo (for reviewers)

Run a full deterministic audit on a sample circuit:

```bash
git clone https://github.com/MfFischer/ZKAuditCore
cd ZKAuditCore
pip install -e .[dev]

zk-auditcore analyze fixtures/circuits/vulnerable_sample.json --out-dir artifacts_demo
zk-auditcore verify --out-dir artifacts_demo
```

Expected output:

- Coverage report: "We analyzed X% of your constraints"
- Evidence-linked findings (rule + constraint + solver result)
- Signed attestation manifest

Artifacts generated:

- `report.html`
- `coverage.json`
- `findings.json`
- `attestation.json`

👉 That's it. No extra text. No fluff.

## 🧠 Why this works

It signals immediately:

- ✅ "This runs"
- ✅ "This is deterministic"
- ✅ "This produces audit artifacts"

Most grant repos don't have this, so it stands out instantly.

## 📸 Do you need a screenshot?

### ❌ Not required
### ✅ But highly recommended

## 🎯 When to include a screenshot

Add one screenshot only if:

- your `report.html` looks clean
- coverage % is visible
- findings are structured

## 📍 Where to place it

```md
### Sample Report Output

![ZKAuditCore Report Screenshot](docs/report_example.png)
```

Deterministic, coverage-aware, exploit-oriented analysis for zero-knowledge circuits.

ZKAuditCore is a CLI-first security analysis pipeline that generates reproducible, evidence-linked audit artifacts for ZK systems. It is designed to support human auditors with verifiable outputs rather than probabilistic heuristics.

## Why ZKAuditCore

- Deterministic execution and stable output ordering
- Evidence-backed findings with rule and solver traceability
- Constraint-level coverage metrics with explicit exclusions
- Reproducibility manifest and Sigstore signing support
- CI-friendly workflow for repeatable security review

## MVP Scope (Phase 1)

- Circom-oriented ingestion to typed analysis IR
- Constraint dependency graph construction
- Static rule engine with extensible rule contracts
- Z3 integration with `SAT` / `UNSAT` / `UNKNOWN` semantics
- Coverage calculator with reason-tagged unverified sets
- JSON + HTML report exports with evidence references
- Attestation manifest + signature status output

## Repository Layout

- `src/zk_auditcore/cli` - CLI commands (`analyze`, `report`, `attest`, `verify`, `replay`)
- `src/zk_auditcore/parsers` - parser adapters and ingestion entry points
- `src/zk_auditcore/ir` - typed IR models and dependency graphing
- `src/zk_auditcore/rules` - rule engine and built-in checks
- `src/zk_auditcore/solver` - SMT execution adapters
- `src/zk_auditcore/coverage` - defensible coverage metrics
- `src/zk_auditcore/attestation` - reproducibility and signing hooks
- `src/zk_auditcore/reporting` - schema and exporters
- `src/zk_auditcore/pipeline` - end-to-end orchestration
- `fixtures/circuits` - sample vulnerable inputs
- `tests` - integration validation suite

## Quick Start

1. Use Python `3.11+`.
2. Install dependencies:
   - `pip install -e .[dev]`
3. Run analysis:
   - `zk-auditcore analyze fixtures/circuits/vulnerable_sample.json --out-dir artifacts`
4. Verify attestation manifest:
   - `zk-auditcore verify --out-dir artifacts`

## Output Artifacts

An analysis run emits:

- `findings.json`
- `coverage.json`
- `report.html`
- `attestation.json`
- `attestation_status.json`

## Engineering Principles

- LLM outputs (when used for narrative reporting) must remain schema-bound and evidence-grounded.
- Cryptographic reasoning is delegated to deterministic engines and typed rule logic.
- Coverage claims must remain explainable and reproducible.
- Human sign-off remains mandatory for audit conclusions.

## Development

- Lint: `ruff check src tests`
- Type check: `mypy src`
- Test: `pytest -q`

See `CONTRIBUTING.md` for contribution workflow and `SECURITY.md` for vulnerability reporting.
