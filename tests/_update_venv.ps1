$projectPath = "D:\VS_Code\dev-newtutils"
$venvRoot = "D:\VS_Code"

Set-Location $projectPath

$venvironments = @(
    "venv310"
    "venv311"
    "venv312"
    "venv313"
    "venv314"
)

foreach ($venv in $venvironments) {
    Write-Host ""
    Write-Host ""

    $venvPath = Join-Path $venvRoot ".$venv"
    $python = Join-Path $venvPath "Scripts\python.exe"

    if (-not (Test-Path -LiteralPath $python -PathType Leaf)) {
        Write-Warning "Skipping ${venv}: Python not found"
        continue
    }

    Write-Host "Installing package and test dependencies in $venv"

    & $python -m pip install -e ".[test]"

    if ($LASTEXITCODE -ne 0) {
        Write-Warning "Installation failed in $venv"
        continue
    }
}
