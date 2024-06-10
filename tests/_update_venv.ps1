#!/usr/bin/env pwsh

<#
Author: NewtCode Anna Burova
Created: 2024-06
Updated: 2026-11

Run:
& 'D:\VS_Code\dev-newtutils\tests\_update_venv.ps1'

Install the project in editable mode with test dependencies in each virtual environment.
#>

# ===================================================================== ======= =================== ====================

# Directory containing virtual environments
$WorkspaceDirectory = "D:\VS_Code"

$Environments = @(
    ".venv315"
    ".venv314"
    ".venv313"
    ".venv312"
    ".venv311"
)

# --------------------------------------------------------------------- ------- ------------------- --------------------

# Directory containing this script and one level above the tests/ directory.
$ProjectDirectory = Split-Path -Path $PSScriptRoot -Parent
# D:\VS_Code\dev-newtutils

Set-Location -LiteralPath $ProjectDirectory

Write-Host ""

# --------------------------------------------------------------------- ------- ------------------- --------------------

if (Get-Command deactivate -ErrorAction SilentlyContinue) {

    Write-Host "Deactivating virtual environment..."

    deactivate

    Write-Host ""
}

# --------------------------------------------------------------------- ------- ------------------- --------------------

foreach ($Environment in $Environments) {

    $PythonPath = Join-Path `
        -Path $WorkspaceDirectory `
        -ChildPath "$Environment\Scripts\python.exe"

    Write-Host "`nInstalling project and test dependencies in $Environment..."

    & $PythonPath -m pip install -e ".[test]"

    if ($LASTEXITCODE -ne 0) {
        throw "Failed to install project in $Environment. Exit code: $LASTEXITCODE"
    }
}

# --------------------------------------------------------------------- ------- ------------------- --------------------

Set-Location -LiteralPath $WorkspaceDirectory

Write-Host ""

# ===================================================================== ======= =================== ====================
