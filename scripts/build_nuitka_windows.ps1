$ErrorActionPreference = "Stop"
$projectRoot = (Resolve-Path (Join-Path $PSScriptRoot "..")).Path
$python = Join-Path $projectRoot ".venv\Scripts\python.exe"
$deploy = Join-Path $projectRoot ".venv\Scripts\pyside6-deploy.exe"
$env:NUITKA_CACHE_DIR = Join-Path $projectRoot "build\nuitka-cache"
New-Item -ItemType Directory -Force -Path $env:NUITKA_CACHE_DIR | Out-Null

if (-not (Test-Path -LiteralPath $python) -or -not (Test-Path -LiteralPath $deploy)) {
    throw "Installez les dépendances avec .\.venv\Scripts\python.exe -m pip install -r requirements.txt"
}

Push-Location $projectRoot
try {
    & $deploy --force --verbose --keep-deployment-files --name EduPaie --config-file pysidedeploy.spec main.py
    if ($LASTEXITCODE -ne 0) {
        throw "pyside6-deploy a échoué avec le code $LASTEXITCODE"
    }
    $ancienNom = Join-Path $projectRoot "deployment\EduPaie.dist\main.exe"
    $nouveauNom = Join-Path $projectRoot "deployment\EduPaie.dist\EduPaie.exe"
    if ((Test-Path -LiteralPath $ancienNom) -and -not (Test-Path -LiteralPath $nouveauNom)) {
        Move-Item -LiteralPath $ancienNom -Destination $nouveauNom
    }
    if (-not (Test-Path -LiteralPath $nouveauNom)) {
        throw "Nuitka n'a pas produit deployment\EduPaie.dist\EduPaie.exe"
    }
    Write-Host "Construction Nuitka terminée. Consultez le dossier deployment."
}
finally {
    Pop-Location
}
