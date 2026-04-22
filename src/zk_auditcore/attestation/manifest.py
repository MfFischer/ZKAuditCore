from __future__ import annotations

import hashlib
import json
import platform
import subprocess
from datetime import UTC, datetime
from pathlib import Path

from pydantic import BaseModel


class RunManifest(BaseModel):
    generated_at: str
    input_sha256: str
    ir_sha256: str
    solver: str
    solver_timeout_ms: int
    ruleset_version: str
    environment: dict[str, str]


class AttestationResult(BaseModel):
    signature_created: bool
    message: str


def sha256_file(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def create_manifest(
    input_path: Path, ir_hash: str, solver_timeout_ms: int, ruleset_version: str
) -> RunManifest:
    return RunManifest(
        generated_at=datetime.now(UTC).isoformat(),
        input_sha256=sha256_file(input_path),
        ir_sha256=ir_hash,
        solver="z3",
        solver_timeout_ms=solver_timeout_ms,
        ruleset_version=ruleset_version,
        environment={
            "python_version": platform.python_version(),
            "platform": platform.platform(),
        },
    )


def write_manifest(manifest: RunManifest, out_path: Path) -> None:
    payload = json.dumps(manifest.model_dump(mode="json"), indent=2, sort_keys=True)
    out_path.write_text(payload, encoding="utf-8")


def try_sigstore_sign(manifest_path: Path) -> AttestationResult:
    try:
        subprocess.run(
            [
                "sigstore",
                "sign",
                "--bundle",
                str(manifest_path) + ".sigstore.json",
                str(manifest_path),
            ],
            check=True,
            capture_output=True,
            text=True,
            timeout=20,
        )
        return AttestationResult(signature_created=True, message="sigstore_signed")
    except Exception:
        return AttestationResult(
            signature_created=False,
            message="sigstore_not_available_or_failed",
        )


def verify_manifest_content(manifest_path: Path) -> bool:
    payload = json.loads(manifest_path.read_text(encoding="utf-8"))
    return all(k in payload for k in ["input_sha256", "ir_sha256", "solver", "environment"])
