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
            f"""
            <tr class="finding-row">
                <td class="font-mono text-sm text-slate-500">{f.rule_id}</td>
                <td>
                    <span class="badge severity-{f.severity.value}">
                        {f.severity.value.upper()}
                    </span>
                </td>
                <td>
                    <div class="finding-title">{f.title}</div>
                    <div class="finding-desc">{f.description}</div>
                </td>
                <td><code class="ref-code">{f.constraint_ref or f.signal_ref or '-'}</code></td>
                <td>
                    <span
                        class="solver-status status-{(
                            f.solver_status.value.lower() if f.solver_status else 'none'
                        )}"
                    >
                        {f.solver_status.value if f.solver_status else '-'}
                    </span>
                </td>
            </tr>
            """
            for f in findings
        ]
    )
    report_id = "MVP-DEMO"
    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>ZKAuditCore | Security Analysis Report</title>
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link
        href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&family=JetBrains+Mono:wght@400;500&display=swap"
        rel="stylesheet"
    >
    <style>
        :root {{
            --primary: #4f46e5;
            --primary-light: #818cf8;
            --bg: #ffffff;
            --text-main: #1e293b;
            --text-muted: #64748b;
            --border: #e2e8f0;
            --card-bg: #f8fafc;
            
            --critical: #ef4444;
            --high: #f97316;
            --medium: #f59e0b;
            --low: #3b82f6;
            --info: #0ea5e9;
            
            --sat: #10b981;
            --unsat: #ef4444;
            --unknown: #94a3b8;
        }}

        * {{ box-sizing: border-box; }}
        body {{ 
            font-family: 'Inter', -apple-system, sans-serif; 
            margin: 0; 
            padding: 0;
            color: var(--text-main);
            background-color: #f1f5f9;
            line-height: 1.5;
        }}

        .container {{
            max-width: 1100px;
            margin: 40px auto;
            padding: 0 20px;
        }}

        header {{
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 32px;
        }}

        .logo {{
            font-size: 24px;
            font-weight: 800;
            letter-spacing: -0.025em;
            color: var(--primary);
            display: flex;
            align-items: center;
            gap: 8px;
        }}

        .logo::before {{
            content: "";
            width: 32px;
            height: 32px;
            background: linear-gradient(135deg, var(--primary), var(--primary-light));
            border-radius: 8px;
            display: inline-block;
        }}

        .hero {{
            background: linear-gradient(135deg, #1e293b 0%, #334155 100%);
            color: white;
            padding: 48px;
            border-radius: 24px;
            margin-bottom: 32px;
            box-shadow: 0 20px 25px -5px rgba(0, 0, 0, 0.1), 0 10px 10px -5px rgba(0, 0, 0, 0.04);
            position: relative;
            overflow: hidden;
        }}

        .hero::after {{
            content: "";
            position: absolute;
            top: -50%;
            right: -10%;
            width: 400px;
            height: 400px;
            background: radial-gradient(circle, rgba(79, 70, 229, 0.2) 0%, transparent 70%);
            border-radius: 50%;
        }}

        .hero h1 {{ 
            margin: 0; 
            font-size: 36px; 
            font-weight: 800;
            letter-spacing: -0.025em;
        }}

        .coverage-metric {{
            display: flex;
            align-items: baseline;
            gap: 12px;
            margin-top: 16px;
        }}

        .coverage-value {{
            font-size: 56px;
            font-weight: 800;
            color: var(--primary-light);
        }}

        .coverage-label {{
            font-size: 18px;
            color: #94a3b8;
            font-weight: 500;
        }}

        .section-card {{
            background: white;
            border-radius: 20px;
            padding: 32px;
            box-shadow: 0 1px 3px rgba(0,0,0,0.1);
            margin-bottom: 32px;
            border: 1px solid var(--border);
        }}

        h2 {{ 
            font-size: 20px; 
            font-weight: 700; 
            margin-top: 0; 
            margin-bottom: 24px;
            display: flex;
            align-items: center;
            gap: 10px;
        }}

        table {{ 
            border-collapse: separate; 
            border-spacing: 0;
            width: 100%; 
        }}

        th {{ 
            background: #f8fafc; 
            padding: 12px 16px;
            text-align: left;
            font-size: 12px;
            font-weight: 600;
            text-transform: uppercase;
            letter-spacing: 0.05em;
            color: var(--text-muted);
            border-bottom: 1px solid var(--border);
        }}

        td {{ 
            padding: 16px; 
            border-bottom: 1px solid var(--border);
            vertical-align: top;
        }}

        .finding-row:hover {{ background-color: #f8fafc; }}

        .badge {{
            display: inline-flex;
            align-items: center;
            padding: 4px 10px;
            border-radius: 6px;
            font-size: 11px;
            font-weight: 700;
            text-transform: uppercase;
        }}

        .severity-critical {{
            background: #fef2f2; color: var(--critical); border: 1px solid #fee2e2;
        }}
        .severity-high {{
            background: #fff7ed; color: var(--high); border: 1px solid #ffedd5;
        }}
        .severity-medium {{
            background: #fffbeb; color: var(--medium); border: 1px solid #fef3c7;
        }}
        .severity-low {{
            background: #eff6ff; color: var(--low); border: 1px solid #dbeafe;
        }}

        .finding-title {{ font-weight: 600; font-size: 15px; margin-bottom: 4px; }}
        .finding-desc {{ font-size: 14px; color: var(--text-muted); }}

        .ref-code {{
            font-family: 'JetBrains Mono', monospace;
            background: #f1f5f9;
            padding: 2px 6px;
            border-radius: 4px;
            font-size: 12px;
            color: var(--primary);
        }}

        .solver-status {{
            font-weight: 600;
            font-size: 12px;
        }}
        .status-sat {{ color: var(--sat); }}
        .status-unsat {{ color: var(--unsat); }}
        .status-unknown {{ color: var(--unknown); }}

        pre {{ 
            background: #1e293b; 
            color: #e2e8f0;
            padding: 20px; 
            border-radius: 12px; 
            font-family: 'JetBrains Mono', monospace;
            font-size: 13px;
            overflow-x: auto;
            border: 1px solid #334155;
        }}

        .footer {{
            text-align: center;
            color: var(--text-muted);
            font-size: 13px;
            margin-top: 64px;
            padding-bottom: 40px;
        }}
    </style>
</head>
<body>
    <div class="container">
        <header>
            <div class="logo">ZKAuditCore</div>
            <div style="font-size: 14px; font-weight: 500; color: var(--text-muted);">
                Report ID: {report_id}
            </div>
        </header>

        <div class="hero">
            <h1>Security Analysis Summary</h1>
            <div class="coverage-metric">
                <span class="coverage-value">{coverage_pct}%</span>
                <span class="coverage-label">Constraint Coverage</span>
            </div>
            <p style="margin-top: 24px; color: #cbd5e1; max-width: 600px; font-size: 15px;">
                Deterministic formal verification of ZK circuit constraints.
                This report provides a verifiable attestation of the
                security properties analyzed.
            </p>
        </div>

        <div class="section-card">
            <h2>Findings</h2>
            <table>
                <thead>
                    <tr>
                        <th>Rule ID</th>
                        <th>Severity</th>
                        <th>Title & Description</th>
                        <th>Reference</th>
                        <th>Status</th>
                    </tr>
                </thead>
                <tbody>
                    {rows}
                </tbody>
            </table>
        </div>

        <div class="section-card">
            <h2>Raw Coverage Data</h2>
            <pre>{json.dumps(bundle.coverage.model_dump(), indent=2, sort_keys=True)}</pre>
        </div>

        <div class="footer">
            Generated by ZKAuditCore &bull; Formal Verification for Zero-Knowledge Systems
        </div>
    </div>
</body>
</html>
"""
    (out_dir / "report.html").write_text(html, encoding="utf-8")
