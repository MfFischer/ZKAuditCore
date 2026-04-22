# Contributing

Thanks for contributing to ZKAuditCore.

## Ground Rules

- Keep changes deterministic and reproducible.
- Prefer explicit, typed schemas over implicit structures.
- Preserve traceability from findings to rule/solver evidence.
- Avoid introducing non-essential dependencies.

## Local Setup

1. Install Python `3.11+`.
2. Install dependencies:
   - `pip install -e .[dev]`
3. Run quality gates before opening a PR:
   - `ruff check src tests`
   - `mypy src`
   - `pytest -q`

## Pull Request Expectations

- Include a short problem statement and rationale.
- Add or update tests for behavior changes.
- Document user-visible changes in `README.md` or `docs/`.
- Keep commits focused and easy to review.

## Commit Conventions

- Use imperative, descriptive commit titles.
- Explain "why" in the commit body for non-trivial changes.

## Scope Discipline

Phase-1 scope is intentionally narrow. Please avoid adding:

- Multi-framework adapters
- Protocol-level analysis
- Automated fix generation
- Non-deterministic analysis paths
