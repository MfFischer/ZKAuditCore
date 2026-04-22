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
    coverage_pct = bundle.coverage.verified_percent
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
  <head>
    <meta charset="utf-8">
    <title>ZKAuditCore Report</title>
    <style>
      body {{ font-family: Arial, sans-serif; margin: 32px; color: #111827; }}
      .hero {{
        background: #eef2ff;
        border: 1px solid #c7d2fe;
        border-radius: 10px;
        padding: 16px;
        margin-bottom: 20px;
      }}
      .hero h2 {{ margin: 0; font-size: 26px; }}
      .sub {{ color: #374151; margin-top: 8px; }}
      table {{ border-collapse: collapse; width: 100%; }}
      th, td {{ border: 1px solid #d1d5db; padding: 8px; text-align: left; }}
      th {{ background: #f9fafb; }}
      pre {{ background: #f9fafb; border: 1px solid #e5e7eb; padding: 12px; border-radius: 8px; }}
    </style>
  </head>
  <body>
    <h1>ZKAuditCore MVP Report</h1>
    <div class="hero">
      <h2>We analyzed {coverage_pct}% of your constraints.</h2>
      <div class="sub">
        Deterministic analysis with evidence-linked findings and reproducible artifacts.
      </div>
    </div>
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
