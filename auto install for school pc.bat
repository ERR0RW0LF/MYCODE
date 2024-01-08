@echo off

start "" "C:\Path\to\VSCodeInsiderInstaller.exe"

powershell -Command "Write-Host 'winget install --id Git.Git -e --source winget --force'"

cmd /c "python311 -m pip install package-name"
