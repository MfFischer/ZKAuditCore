from __future__ import annotations

from collections import defaultdict

from zk_auditcore.ir.models import CircuitIR


class ConstraintGraph:
    def __init__(self, ir: CircuitIR) -> None:
        self.ir = ir
        self.signal_to_constraints: dict[str, list[str]] = defaultdict(list)
        self.constraint_edges: dict[str, list[str]] = defaultdict(list)
        self._build()

    def _build(self) -> None:
        for constraint in self.ir.constraints:
            for sig in constraint.signal_refs:
                self.signal_to_constraints[sig].append(constraint.id)

        for constraint in self.ir.constraints:
            linked: set[str] = set()
            for sig in constraint.signal_refs:
                linked.update(self.signal_to_constraints.get(sig, []))
            linked.discard(constraint.id)
            self.constraint_edges[constraint.id] = sorted(linked)

    def neighborhood(self, constraint_id: str) -> list[str]:
        return self.constraint_edges.get(constraint_id, [])
