param(
    [switch]$InstallPythonPackagesOnly
)

$ErrorActionPreference = "Stop"

Write-Host "[1/2] Installiere bzw. aktualisiere Python-Pakete..."
python -m pip install --upgrade pip
python -m pip install --upgrade yt-dlp

if ($InstallPythonPackagesOnly) {
    Write-Host "Nur Python-Pakete wurden aktualisiert."
    exit 0
}

Write-Host "[2/2] Prufe ffmpeg..."
if (Get-Command ffmpeg -ErrorAction SilentlyContinue) {
    Write-Host "ffmpeg ist bereits im PATH vorhanden."
    exit 0
}

if (Get-Command winget -ErrorAction SilentlyContinue) {
    Write-Host "Installiere ffmpeg via winget (Gyan.FFmpeg)..."
    winget install --id Gyan.FFmpeg --exact --accept-package-agreements --accept-source-agreements
    Write-Host "ffmpeg wurde installiert. Bitte Terminal neu starten, damit PATH aktualisiert wird."
    exit 0
}

Write-Warning "winget nicht gefunden. Bitte ffmpeg manuell installieren: https://ffmpeg.org/download.html"
exit 1
