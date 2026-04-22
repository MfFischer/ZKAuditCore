$ErrorActionPreference = "Stop"

Write-Host "ZKAuditCore demo run starting..." -ForegroundColor Cyan

$outDir = "artifacts_demo_" + (Get-Date -Format "yyyyMMdd_HHmmss")
$input = "fixtures/circuits/vulnerable_sample.json"

python -m zk_auditcore.cli.main analyze $input --out-dir $outDir
python -m zk_auditcore.cli.main verify --out-dir $outDir

$required = @(
    "$outDir/findings.json",
    "$outDir/coverage.json",
    "$outDir/report.html",
    "$outDir/attestation.json",
    "$outDir/attestation_status.json"
)

foreach ($file in $required) {
    if (-not (Test-Path $file)) {
        throw "Missing required artifact: $file"
    }
}

Write-Host "Demo complete. Artifacts available in $outDir" -ForegroundColor Green
