# Build a single-file executable for Windows.
# PyInstaller is not a cross-compiler: build on Windows for Windows.
# Usage (PowerShell, from the repository root, venv active):  .\scripts\build.ps1
$ErrorActionPreference = "Stop"
Set-Location (Join-Path $PSScriptRoot "..")

python -m pip install -r requirements-dev.txt
python -m PyInstaller `
  --noconfirm --clean `
  --onefile `
  --name ForkableToDoNotes `
  --collect-data todonotes `
  packaging/launch.py

Write-Host "✅ Built: dist\ForkableToDoNotes.exe"
