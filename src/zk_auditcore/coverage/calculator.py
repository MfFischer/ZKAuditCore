from __future__ import annotations

from pydantic import BaseModel

from zk_auditcore.ir.models import CircuitIR, SolverResult


class CoverageReport(BaseModel):
    total_constraints: int
    excluded_constraints: list[str]
    verified_constraints: int
    unverified_constraints: int
    verified_percent: float
    unverified_reasons: dict[str, int]


def compute_coverage(ir: CircuitIR, solver_result: SolverResult) -> CoverageReport:
    excluded = [c.id for c in ir.constraints if c.is_passthrough]
    total_non_excluded = len(ir.constraints) - len(excluded)
    checked = [c for c in solver_result.checked_constraints if c not in excluded]
    verified = len(checked)
    unverified = max(total_non_excluded - verified, 0)

    reason = solver_result.reason or "not_checked"
    reasons: dict[str, int] = {}
    if unverified > 0:
        reasons[reason] = unverified

    pct = (verified / total_non_excluded * 100.0) if total_non_excluded else 100.0
    return CoverageReport(
        total_constraints=len(ir.constraints),
        excluded_constraints=excluded,
        verified_constraints=verified,
        unverified_constraints=unverified,
        verified_percent=round(pct, 2),
        unverified_reasons=reasons,
    )
