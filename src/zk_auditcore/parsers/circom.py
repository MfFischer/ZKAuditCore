from __future__ import annotations

import json
from pathlib import Path

from zk_auditcore.ir.models import CircuitIR, Component, Constraint, Signal


def parse_circom_json(input_path: Path) -> CircuitIR:
    """
    MVP parser adapter:
    Expects a deterministic JSON representation of a Circom circuit.
    """
    raw = json.loads(input_path.read_text(encoding="utf-8"))

    circuit_name = str(raw.get("circuit_name", input_path.stem))
    source_ref = str(raw.get("source_ref", str(input_path)))

    signals = [
        Signal(
            id=str(item["id"]),
            name=str(item["name"]),
            is_public=bool(item.get("is_public", False)),
            component=str(item.get("component", "root")),
        )
        for item in raw.get("signals", [])
    ]
    constraints = [
        Constraint(
            id=str(item["id"]),
            expression=str(item["expression"]),
            signal_refs=[str(x) for x in item.get("signal_refs", [])],
            is_passthrough=bool(item.get("is_passthrough", False)),
        )
        for item in raw.get("constraints", [])
    ]
    components = [
        Component(
            id=str(item["id"]),
            name=str(item["name"]),
            parent_id=str(item["parent_id"]) if item.get("parent_id") else None,
        )
        for item in raw.get("components", [{"id": "cmp_root", "name": "root"}])
    ]

    return CircuitIR(
        circuit_name=circuit_name,
        signals=signals,
        constraints=constraints,
        components=components,
        source_ref=source_ref,
    )
