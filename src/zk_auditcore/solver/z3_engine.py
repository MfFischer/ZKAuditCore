from __future__ import annotations

from z3 import Int, Solver, sat, unknown  # type: ignore[import-untyped]

from zk_auditcore.ir.models import CircuitIR, SolverResult, SolverStatus


def run_solver(ir: CircuitIR, timeout_ms: int = 2000, max_constraints: int = 5000) -> SolverResult:
    if len(ir.constraints) > max_constraints:
        checked = [c.id for c in ir.constraints[:max_constraints]]
        unchecked = [c.id for c in ir.constraints[max_constraints:]]
        return SolverResult(
            status=SolverStatus.unknown,
            checked_constraints=checked,
            unchecked_constraints=unchecked,
            reason=f"constraint_limit_exceeded:{max_constraints}",
        )

    solver = Solver()
    solver.set(timeout=timeout_ms)
    symbols = {sig.id: Int(sig.id) for sig in ir.signals}

    for constraint in ir.constraints:
        # MVP-safe encoding: keep deterministic relation placeholder.
        if len(constraint.signal_refs) >= 2:
            left, right = constraint.signal_refs[:2]
            if left in symbols and right in symbols:
                solver.add(symbols[left] == symbols[right])

    result = solver.check()
    if result == sat:
        model = solver.model()
        out_model = {d.name(): str(model[d]) for d in model.decls()}
        return SolverResult(
            status=SolverStatus.sat,
            checked_constraints=[c.id for c in ir.constraints],
            unchecked_constraints=[],
            model=out_model,
        )
    if result == unknown:
        return SolverResult(
            status=SolverStatus.unknown,
            checked_constraints=[c.id for c in ir.constraints],
            unchecked_constraints=[],
            reason=solver.reason_unknown(),
        )
    return SolverResult(
        status=SolverStatus.unsat,
        checked_constraints=[c.id for c in ir.constraints],
        unchecked_constraints=[],
    )
