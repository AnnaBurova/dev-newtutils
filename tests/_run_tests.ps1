#!/usr/bin/env pwsh

<#
Author: NewtCode Anna Burova
Created: 2024-06
Updated: 2026-11

Run:
& 'D:\VS_Code\dev-newtutils\tests\_run_tests.ps1'

Run selected test modules in configured virtual environments across four pytest modes.
#>

# ===================================================================== ======= =================== ====================

# Directory containing virtual environments
$WorkspaceDirectory = "D:\VS_Code"

$Environments = @(
    "venv315"
    "venv314"
    "venv313"
    "venv312"
    "venv311"
)

$Modules = @(
    "console_stringify_value"
    # "utility"
    # "files"
    # "sql"
    # "network"
)

# --------------------------------------------------------------------- ------- ------------------- --------------------

Set-Location -LiteralPath $PSScriptRoot
# D:\VS_Code\dev-newtutils\tests

# Ensure output directory exists
$OutputDirectory = Join-Path -Path $PSScriptRoot -ChildPath "output"
if (-not (Test-Path -LiteralPath $OutputDirectory -PathType Container)) {
    New-Item -ItemType Directory -Path $OutputDirectory | Out-Null
}

# UTF-8 encoding without BOM (for consistent LF output files)
$Utf8NoBom = [System.Text.UTF8Encoding]::new($false)

Write-Host ""

# --------------------------------------------------------------------- ------- ------------------- --------------------

if (Get-Command deactivate -ErrorAction SilentlyContinue) {

    Write-Host "Deactivating virtual environment..."

    deactivate

    Write-Host ""
}

# --------------------------------------------------------------------- ------- ------------------- --------------------

foreach ($Environment in $Environments) {

    $PytestPath = Join-Path `
        -Path $WorkspaceDirectory `
        -ChildPath ".$Environment\Scripts\pytest.exe"

    # Skip environment if pytest executable is not found
    if (-not (Test-Path -LiteralPath $PytestPath -PathType Leaf)) {
        Write-Host "`nSkipping $Environment : pytest not found"
        continue
    }

    # ----------------------------------------------------------------- ------- ------------------- --------------------

    foreach ($Module in $Modules) {

        $TestFile = "test_${Module}.py"

        foreach ($Mode in 1..4) {

            Write-Host "tests/${TestFile}: mode $Mode, environment $Environment"

            $ModeArgs = switch ($Mode) {
                1 { @() }
                2 { @("-vv") }
                3 { @("-s") }
                4 { @("-s", "-vv") }
            }

            # Run pytest and capture both stdout and stderr
            $RawLines = & $PytestPath $TestFile @ModeArgs 2>&1 | ForEach-Object { $_.ToString() }

            # Strip execution time from summary line
            $ProcessedLines = $RawLines | ForEach-Object {
                $_ -replace '(passed|ran) in [0-9.]+s( ={10,})$', '$1$2'
            }

            # Join with LF (`n) and write as UTF-8 without BOM (equivalent to dos2unix)
            $Content = ($ProcessedLines -join "`n") + "`n"
            $OutputFile = Join-Path -Path $OutputDirectory -ChildPath "${Environment}_test_${Module}_${Mode}.txt"
            [System.IO.File]::WriteAllText($OutputFile, $Content, $Utf8NoBom)
        }
    }
}

# --------------------------------------------------------------------- ------- ------------------- --------------------

Set-Location -LiteralPath $WorkspaceDirectory

Write-Host ""

# ===================================================================== ======= =================== ====================
