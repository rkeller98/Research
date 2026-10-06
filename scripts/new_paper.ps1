[CmdletBinding()]
param(
    [Parameter(Mandatory = $true, Position = 0)]
    [ValidatePattern('^[A-Za-z0-9_-]+$')]
    [string]$Name
)

$ErrorActionPreference = 'Stop'
& (Join-Path $PSScriptRoot 'check_architecture.ps1')
$repoRoot = (Resolve-Path (Join-Path $PSScriptRoot '..')).Path
$templateDir = Join-Path $repoRoot 'paper_template'
$papersDir = Join-Path $repoRoot 'papers'
$targetDir = Join-Path $papersDir $Name

if (-not (Test-Path -LiteralPath $templateDir -PathType Container)) {
    throw "Paper template not found: $templateDir"
}
if (Test-Path -LiteralPath $targetDir) {
    throw "Paper already exists: $targetDir"
}

New-Item -ItemType Directory -Path $papersDir -Force | Out-Null
Copy-Item -LiteralPath $templateDir -Destination $targetDir -Recurse
$newMain = Join-Path $targetDir 'main.tex'
$newMainText = [IO.File]::ReadAllText($newMain).Replace('\subimport{../shared/}', '\subimport{../../shared/}')
[IO.File]::WriteAllText($newMain, $newMainText, (New-Object Text.UTF8Encoding($false)))
Write-Host "Created paper using canonical shared infrastructure: $targetDir"
Write-Host "Read WRITING_GUIDE.md first; then edit metadata, sections, figures, and bibliography."
