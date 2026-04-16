from __future__ import annotations

import json
from pathlib import Path

from zk_auditcore.reporting.schema import AnalysisBundle


def export_json(bundle: AnalysisBundle, out_dir: Path) -> None:
    out_dir.mkdir(parents=True, exist_ok=True)
    findings_payload = json.dumps(bundle.findings.model_dump(mode="json"), indent=2, sort_keys=True)
    (out_dir / "findings.json").write_text(
        findings_payload, encoding="utf-8"
    )
    coverage_payload = json.dumps(bundle.coverage.model_dump(mode="json"), indent=2, sort_keys=True)
    (out_dir / "coverage.json").write_text(
        coverage_payload, encoding="utf-8"
    )


def export_html(bundle: AnalysisBundle, out_dir: Path) -> None:
    out_dir.mkdir(parents=True, exist_ok=True)
    findings = bundle.findings.findings
    rows = "".join(
        [
            "<tr>"
            f"<td>{f.rule_id}</td><td>{f.severity.value}</td>"
            f"<td>{f.title}</td><td>{f.constraint_ref or f.signal_ref or '-'}</td>"
            "</tr>"
            for f in findings
        ]
    )
    html = f"""<!DOCTYPE html>
<html>
  <head><meta charset="utf-8"><title>ZKAuditCore Report</title></head>
  <body>
    <h1>ZKAuditCore MVP Report</h1>
    <h2>Coverage</h2>
    <pre>{json.dumps(bundle.coverage.model_dump(), indent=2, sort_keys=True)}</pre>
    <h2>Findings</h2>
    <table border="1" cellpadding="6" cellspacing="0">
      <tr><th>Rule</th><th>Severity</th><th>Title</th><th>Reference</th></tr>
      {rows}
    </table>
  </body>
</html>
"""
    (out_dir / "report.html").write_text(html, encoding="utf-8")
