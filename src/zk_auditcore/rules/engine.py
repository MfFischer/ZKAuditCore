from __future__ import annotations

from dataclasses import dataclass
from typing import Protocol

from zk_auditcore.ir.models import CircuitIR, Finding


class Rule(Protocol):
    rule_id: str

    def run(self, ir: CircuitIR) -> list[Finding]:
        ...


@dataclass(frozen=True)
class RuleEngine:
    rules: list[Rule]

    def execute(self, ir: CircuitIR) -> list[Finding]:
        findings: list[Finding] = []
        for rule in sorted(self.rules, key=lambda r: r.rule_id):
            findings.extend(rule.run(ir))
        return sorted(
            findings,
            key=lambda f: (
                f.rule_id,
                f.constraint_ref or "",
                f.signal_ref or "",
                f.title,
            ),
        )
