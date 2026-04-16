from __future__ import annotations

from pathlib import Path

import typer

from zk_auditcore.pipeline.run import analyze, replay, verify

app = typer.Typer(help="ZKAuditCore deterministic ZK auditing CLI.")


@app.command("analyze")
def analyze_cmd(
    input_file: Path = typer.Argument(..., exists=True),
    out_dir: Path = typer.Option(Path("artifacts"), "--out-dir"),
    solver_timeout_ms: int = typer.Option(2000, "--solver-timeout-ms"),
) -> None:
    bundle = analyze(input_path=input_file, out_dir=out_dir, solver_timeout_ms=solver_timeout_ms)
    typer.echo(f"Findings: {len(bundle.findings.findings)}")
    typer.echo(f"Coverage verified: {bundle.coverage.verified_percent}%")


@app.command("report")
def report_cmd(
    input_file: Path = typer.Argument(..., exists=True),
    out_dir: Path = typer.Option(Path("artifacts"), "--out-dir"),
) -> None:
    analyze(input_path=input_file, out_dir=out_dir)
    typer.echo(f"Report generated in {out_dir}")


@app.command("attest")
def attest_cmd(
    input_file: Path = typer.Argument(..., exists=True),
    out_dir: Path = typer.Option(Path("artifacts"), "--out-dir"),
) -> None:
    analyze(input_path=input_file, out_dir=out_dir)
    typer.echo(f"Attestation generated in {out_dir / 'attestation.json'}")


@app.command("verify")
def verify_cmd(out_dir: Path = typer.Option(Path("artifacts"), "--out-dir")) -> None:
    ok = verify(out_dir=out_dir)
    if ok:
        typer.echo("Attestation manifest verified.")
        raise typer.Exit(code=0)
    typer.echo("Attestation manifest invalid.")
    raise typer.Exit(code=1)


@app.command("replay")
def replay_cmd(
    input_file: Path = typer.Argument(..., exists=True),
    out_dir: Path = typer.Option(Path("artifacts_replay"), "--out-dir"),
) -> None:
    replay(input_path=input_file, out_dir=out_dir)
    typer.echo(f"Replay completed in {out_dir}")


if __name__ == "__main__":
    app()
