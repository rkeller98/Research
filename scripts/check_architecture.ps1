[CmdletBinding()]
param([switch]$SelfTest)
$ErrorActionPreference = 'Stop'
$pythonCommand = Get-Command python -ErrorAction SilentlyContinue
if (-not $pythonCommand) { $pythonCommand = Get-Command python3 -ErrorAction SilentlyContinue }
if (-not $pythonCommand) { throw 'Architecture check requires Python 3 on PATH.' }
$checkArgs = @((Join-Path $PSScriptRoot 'check_architecture.py'))
if ($SelfTest) { $checkArgs += '--self-test' }
& $pythonCommand.Source @checkArgs
if ($LASTEXITCODE -ne 0) { throw 'Publications architecture check failed.' }
