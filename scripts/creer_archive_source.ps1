$ErrorActionPreference = "Stop"
$racine = (Resolve-Path (Join-Path $PSScriptRoot "..")).Path
$destination = Join-Path $racine "EduPaie_source_complet.zip"

if (Test-Path -LiteralPath $destination) {
    $archiveExistante = (Resolve-Path -LiteralPath $destination).Path
    if (-not $archiveExistante.StartsWith($racine, [System.StringComparison]::OrdinalIgnoreCase)) {
        throw "Le chemin de l'archive sort du dossier du projet."
    }
    Remove-Item -LiteralPath $archiveExistante -Force
}

Add-Type -AssemblyName System.IO.Compression.FileSystem
$archive = [System.IO.Compression.ZipFile]::Open(
    $destination,
    [System.IO.Compression.ZipArchiveMode]::Create
)

try {
    $fichiers = @(
        "README.md", "MANUEL_UTILISATEUR.md", "main.py", "requirements.txt",
        "requirements-build.txt", "pysidedeploy.spec", ".gitignore",
        "Lancer EduPaie.vbs"
    )
    foreach ($nom in $fichiers) {
        $chemin = Join-Path $racine $nom
        if (Test-Path -LiteralPath $chemin -PathType Leaf) {
            $nomArchive = "EduPaie_source_complet/" + $nom.Replace("\", "/")
            [System.IO.Compression.ZipFileExtensions]::CreateEntryFromFile(
                $archive, $chemin, $nomArchive,
                [System.IO.Compression.CompressionLevel]::Optimal
            ) | Out-Null
        }
    }

    $dossiers = @("src", "database", "scripts", "docs", "output\pdf")
    foreach ($nomDossier in $dossiers) {
        $dossier = Join-Path $racine $nomDossier
        if (-not (Test-Path -LiteralPath $dossier -PathType Container)) { continue }
        Get-ChildItem -LiteralPath $dossier -Recurse -File |
            Where-Object { $_.Extension -ne ".pyc" -and $_.FullName -notmatch "\\__pycache__\\" } |
            ForEach-Object {
                $relatif = $_.FullName.Substring($racine.Length + 1).Replace("\", "/")
                $nomArchive = "EduPaie_source_complet/" + $relatif
                [System.IO.Compression.ZipFileExtensions]::CreateEntryFromFile(
                    $archive, $_.FullName, $nomArchive,
                    [System.IO.Compression.CompressionLevel]::Optimal
                ) | Out-Null
            }
    }

    $baseDemo = Join-Path $racine "data\edupaie_demo.db"
    [System.IO.Compression.ZipFileExtensions]::CreateEntryFromFile(
        $archive, $baseDemo, "EduPaie_source_complet/data/edupaie_demo.db",
        [System.IO.Compression.CompressionLevel]::Optimal
    ) | Out-Null
}
finally {
    $archive.Dispose()
}

Get-Item -LiteralPath $destination | Select-Object FullName, Length, LastWriteTime
