from __future__ import annotations

from pydantic import BaseModel, Field

from zk_auditcore.coverage.calculator import CoverageReport
from zk_auditcore.ir.models import Finding


class FindingsDocument(BaseModel):
    version: str = "1.0.0"
    findings: list[Finding] = Field(default_factory=list)


class AnalysisBundle(BaseModel):
    findings: FindingsDocument
    coverage: CoverageReport
    evidence_index: dict[str, list[str]] = Field(default_factory=dict)
