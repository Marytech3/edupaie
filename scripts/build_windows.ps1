$ErrorActionPreference = "Stop"
$projectRoot = (Resolve-Path (Join-Path $PSScriptRoot "..")).Path
$python = Join-Path $projectRoot ".venv\Scripts\python.exe"

if (-not (Test-Path -LiteralPath $python)) {
    throw "Environnement absent. Créez-le avec py -3 -m venv .venv, puis installez les dépendances avec .\.venv\Scripts\python.exe -m pip install -r requirements-build.txt"
}
if (-not (Test-Path -LiteralPath (Join-Path $projectRoot "data\edupaie_demo.db"))) {
    throw "Base de démonstration absente : data\edupaie_demo.db"
}

Push-Location $projectRoot
try {
    & $python -m PyInstaller --noconfirm --clean --onedir --windowed `
        --name EduPaie `
        --runtime-hook "scripts\qt_dll_runtime_hook.py" `
        --add-data "database\schema.sql;database" `
        --add-data "data\edupaie_demo.db;data" `
        main.py
    if ($LASTEXITCODE -ne 0) {
        throw "PyInstaller a échoué avec le code $LASTEXITCODE"
    }
    $bundleRoot = Join-Path $projectRoot "dist\EduPaie"
    $qtRuntime = Join-Path $bundleRoot "_internal\PySide6"
    foreach ($dllName in @(
        "Qt6Core.dll", "Qt6Gui.dll", "Qt6Widgets.dll",
        "MSVCP140.dll", "MSVCP140_1.dll", "MSVCP140_2.dll",
        "VCRUNTIME140.dll", "VCRUNTIME140_1.dll"
    )) {
        $sourceDll = Join-Path $qtRuntime $dllName
        if (Test-Path -LiteralPath $sourceDll) {
            Copy-Item -LiteralPath $sourceDll -Destination $bundleRoot -Force
        }
    }
    Write-Host "Application prête : $projectRoot\dist\EduPaie\EduPaie.exe"
}
finally {
    Pop-Location
}
