from __future__ import annotations

import json
import os
from pathlib import Path
from typing import cast

from zk_auditcore.attestation.manifest import (
    create_manifest,
    try_sigstore_sign,
    verify_manifest_content,
    write_manifest,
)
from zk_auditcore.coverage.calculator import compute_coverage
from zk_auditcore.ir.models import Finding
from zk_auditcore.parsers.circom import parse_circom_json
from zk_auditcore.reporting.exporters import export_html, export_json
from zk_auditcore.reporting.schema import AnalysisBundle, FindingsDocument
from zk_auditcore.rules.core import default_rules
from zk_auditcore.rules.engine import Rule, RuleEngine
from zk_auditcore.solver.z3_engine import run_solver


def analyze(input_path: Path, out_dir: Path, solver_timeout_ms: int = 2000) -> AnalysisBundle:
    ir = parse_circom_json(input_path)
    engine = RuleEngine(rules=cast(list[Rule], default_rules()))
    findings: list[Finding] = engine.execute(ir)
    solver_result = run_solver(ir, timeout_ms=solver_timeout_ms)

    for finding in findings:
        finding.solver_status = solver_result.status
        if finding.constraint_ref:
            finding.proof_trace = [f"constraint:{finding.constraint_ref}"]

    coverage = compute_coverage(ir, solver_result)
    bundle = AnalysisBundle(
        findings=FindingsDocument(findings=findings),
        coverage=coverage,
        evidence_index={f.rule_id: f.proof_trace for f in findings},
    )
    export_json(bundle, out_dir)
    export_html(bundle, out_dir)

    manifest = create_manifest(
        input_path=input_path,
        ir_hash=ir.stable_hash(),
        solver_timeout_ms=solver_timeout_ms,
        ruleset_version="mvp-v1",
    )
    manifest_path = out_dir / "attestation.json"
    write_manifest(manifest, manifest_path)
    sign_result = try_sigstore_sign(manifest_path)
    (out_dir / "attestation_status.json").write_text(
        json.dumps(sign_result.model_dump(mode="json"), indent=2, sort_keys=True),
        encoding="utf-8",
    )
    require_sigstore = os.getenv("REQUIRE_SIGSTORE", "0") == "1"
    if require_sigstore and not sign_result.signature_created:
        raise RuntimeError("Sigstore signing is required but unavailable or failed.")
    return bundle


def verify(out_dir: Path) -> bool:
    return verify_manifest_content(out_dir / "attestation.json")


def replay(input_path: Path, out_dir: Path) -> AnalysisBundle:
    return analyze(input_path=input_path, out_dir=out_dir, solver_timeout_ms=2000)
