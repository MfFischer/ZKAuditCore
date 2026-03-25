from __future__ import annotations

from enum import StrEnum
from hashlib import sha256

from pydantic import BaseModel, Field


class Severity(StrEnum):
    low = "low"
    medium = "medium"
    high = "high"
    critical = "critical"


class SolverStatus(StrEnum):
    sat = "SAT"
    unsat = "UNSAT"
    unknown = "UNKNOWN"


class Signal(BaseModel):
    id: str
    name: str
    is_public: bool = False
    component: str = "root"


class Constraint(BaseModel):
    id: str
    expression: str
    signal_refs: list[str] = Field(default_factory=list)
    is_passthrough: bool = False


class Component(BaseModel):
    id: str
    name: str
    parent_id: str | None = None


class CircuitIR(BaseModel):
    circuit_name: str
    signals: list[Signal]
    constraints: list[Constraint]
    components: list[Component]
    source_ref: str
    parser_version: str = "mvp-v1"

    def stable_hash(self) -> str:
        canonical = self.model_dump_json()
        return sha256(canonical.encode("utf-8")).hexdigest()


class Finding(BaseModel):
    rule_id: str
    severity: Severity
    title: str
    description: str
    constraint_ref: str | None = None
    signal_ref: str | None = None
    solver_status: SolverStatus | None = None
    proof_trace: list[str] = Field(default_factory=list)
    evidence: dict[str, str] = Field(default_factory=dict)


class SolverResult(BaseModel):
    status: SolverStatus
    checked_constraints: list[str]
    unchecked_constraints: list[str]
    reason: str | None = None
    model: dict[str, str] = Field(default_factory=dict)
