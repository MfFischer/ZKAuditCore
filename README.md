# ZKAuditCore MVP

Commercial-grade MVP foundation for deterministic ZK circuit auditing.

## Status

This repository contains a Phase-1 CLI + CI implementation focused on:

- Circom-oriented IR ingestion and constraint graphing
- Deterministic static rule execution
- Z3-backed solver outcomes and traces
- Coverage metrics and reproducibility manifests
- Signed attestation hooks and report exports

## Quick Start

1. Create a Python 3.11+ environment.
2. Install:
   - `pip install -e .[dev]`
3. Run:
   - `zk-auditcore analyze fixtures/circuits/vulnerable_sample.json --out-dir artifacts`
