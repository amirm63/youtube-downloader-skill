$ErrorActionPreference = "Stop"

$repoRoot = (Resolve-Path (Join-Path $PSScriptRoot "..")).Path
$skillDir = Join-Path $repoRoot ".claude\skills\youtube-downloader"
$skillEntry = Join-Path $skillDir "SKILL.md"
$distDir = Join-Path $repoRoot "dist"
$zipPath = Join-Path $distDir "youtube-downloader-skill.zip"

if (-not (Test-Path -LiteralPath $skillEntry)) {
    Write-Error "SKILL.md not found at expected path: $skillEntry"
}

if (-not (Test-Path -LiteralPath $distDir)) {
    New-Item -ItemType Directory -Path $distDir | Out-Null
}

if (Test-Path -LiteralPath $zipPath) {
    Remove-Item -LiteralPath $zipPath -Force
}

Compress-Archive -Path (Join-Path $skillDir "*") -DestinationPath $zipPath
Write-Host "Created skill zip: $zipPath"
