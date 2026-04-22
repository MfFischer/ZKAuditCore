from __future__ import annotations

from pathlib import Path

from zk_auditcore.pipeline.run import analyze, verify


def test_analyze_generates_artifacts(tmp_path: Path) -> None:
    fixture = Path("fixtures/circuits/vulnerable_sample.json")
    out_dir = tmp_path / "artifacts"
    bundle = analyze(input_path=fixture, out_dir=out_dir)

    assert len(bundle.findings.findings) >= 2
    assert (out_dir / "findings.json").exists()
    assert (out_dir / "coverage.json").exists()
    assert (out_dir / "report.html").exists()
    assert (out_dir / "attestation.json").exists()
    assert verify(out_dir) is True


def test_multiple_vulnerable_fixtures(tmp_path: Path) -> None:
    fixtures = [
        Path("fixtures/circuits/vulnerable_sample.json"),
        Path("fixtures/circuits/vulnerable_tornado_like.json"),
        Path("fixtures/circuits/vulnerable_ctf_like.json"),
    ]
    for idx, fixture in enumerate(fixtures):
        out = tmp_path / f"run_{idx}"
        bundle = analyze(input_path=fixture, out_dir=out)
        assert len(bundle.findings.findings) >= 1
