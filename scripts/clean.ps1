[CmdletBinding()]
param(
    [Parameter(Position = 0)]
    [ValidatePattern('^[A-Za-z0-9_-]+$')]
    [string]$Paper
)

$ErrorActionPreference = 'Stop'
$repoRoot = (Resolve-Path (Join-Path $PSScriptRoot '..')).Path
$buildRoot = Join-Path $repoRoot 'build'
$target = if ($Paper) { Join-Path $buildRoot $Paper } else { $buildRoot }

if (-not (Test-Path -LiteralPath $target)) {
    Write-Host "Nothing to clean: $target"
    exit 0
}

$separators = [char[]]@([IO.Path]::DirectorySeparatorChar, [IO.Path]::AltDirectorySeparatorChar)
$resolvedBuild = [IO.Path]::GetFullPath($buildRoot).TrimEnd($separators)
$resolvedTarget = [IO.Path]::GetFullPath($target).TrimEnd($separators)
$comparison = if ([IO.Path]::DirectorySeparatorChar -eq '\') { [StringComparison]::OrdinalIgnoreCase } else { [StringComparison]::Ordinal }
$buildPrefix = $resolvedBuild + [IO.Path]::DirectorySeparatorChar
if (-not $resolvedTarget.Equals($resolvedBuild, $comparison) -and -not $resolvedTarget.StartsWith($buildPrefix, $comparison)) {
    throw "Refusing to remove a path outside the build directory: $resolvedTarget"
}

Remove-Item -LiteralPath $resolvedTarget -Recurse -Force
Write-Host "Removed $resolvedTarget"
