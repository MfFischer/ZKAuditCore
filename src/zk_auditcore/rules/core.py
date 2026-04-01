from __future__ import annotations

from dataclasses import dataclass

from zk_auditcore.ir.models import CircuitIR, Finding, Severity


@dataclass(frozen=True)
class UnconstrainedSignalRule:
    rule_id: str = "R001_UNCONSTRAINED_SIGNAL"

    def run(self, ir: CircuitIR) -> list[Finding]:
        referenced = {sig for c in ir.constraints for sig in c.signal_refs}
        findings: list[Finding] = []
        for signal in ir.signals:
            if signal.id not in referenced:
                findings.append(
                    Finding(
                        rule_id=self.rule_id,
                        severity=Severity.high,
                        title="Signal not constrained",
                        description=f"Signal {signal.name} is never constrained.",
                        signal_ref=signal.id,
                        evidence={"signal_name": signal.name},
                    )
                )
        return findings


@dataclass(frozen=True)
class EqualityMisuseRule:
    rule_id: str = "R002_EQUALITY_MISUSE"

    def run(self, ir: CircuitIR) -> list[Finding]:
        findings: list[Finding] = []
        for constraint in ir.constraints:
            if "==" in constraint.expression and "===" not in constraint.expression:
                findings.append(
                    Finding(
                        rule_id=self.rule_id,
                        severity=Severity.medium,
                        title="Potential equality misuse",
                        description="Found '==' where strict '===' is expected in Circom contexts.",
                        constraint_ref=constraint.id,
                        evidence={"expression": constraint.expression},
                    )
                )
        return findings


@dataclass(frozen=True)
class MissingRangeCheckRule:
    rule_id: str = "R003_MISSING_RANGE_CHECK"

    def run(self, ir: CircuitIR) -> list[Finding]:
        findings: list[Finding] = []
        for constraint in ir.constraints:
            expr = constraint.expression.lower()
            has_bound = ("<" in expr or ">" in expr) and "range" in expr
            if "input" in expr and not has_bound:
                findings.append(
                    Finding(
                        rule_id=self.rule_id,
                        severity=Severity.medium,
                        title="Input missing explicit range check",
                        description="Input-like signal usage without obvious range guard.",
                        constraint_ref=constraint.id,
                        evidence={"expression": constraint.expression},
                    )
                )
        return findings


@dataclass(frozen=True)
class NullifierPatternRule:
    rule_id: str = "R004_NULLIFIER_ANTIPATTERN"

    def run(self, ir: CircuitIR) -> list[Finding]:
        findings: list[Finding] = []
        for constraint in ir.constraints:
            expr = constraint.expression.lower()
            if "nullifier" in expr and "used[" not in expr:
                findings.append(
                    Finding(
                        rule_id=self.rule_id,
                        severity=Severity.high,
                        title="Nullifier handling anti-pattern",
                        description="Nullifier appears without a one-time-use tracking pattern.",
                        constraint_ref=constraint.id,
                        evidence={"expression": constraint.expression},
                    )
                )
        return findings


def default_rules() -> list[object]:
    return [
        UnconstrainedSignalRule(),
        EqualityMisuseRule(),
        MissingRangeCheckRule(),
        NullifierPatternRule(),
    ]
