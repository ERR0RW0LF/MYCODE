echo off

REM q: how do i start a program from a batch file
REM a: start /wait program.exe
REM q: how do i start a program from a batch file without waiting for it to finish
REM a: start program.exe

REM starting installer for Vscode insiders
start /wait C:\Users\%username%\Downloads\VSCodeUserSetup-x64-1.86.0-insider.exe

REM q: how can i run a powershell command from a batch file
REM a: powershell.exe -command "command"

REM installing git using powershell
powershell.exe -command "winget install --id Git.Git -e --source winget --force"

REM installing python using powershell
powershell.exe -command "Set-ExecutionPolicy Bypass -Scope Process -Force; [System.Net.ServicePointManager]::SecurityProtocol = [System.Net.ServicePointManager]::SecurityProtocol -bor 3072; iex ((New-Object System.Net.WebClient).DownloadString('https://community.chocolatey.org/install.ps1'))"
powershell.exe -command "choco install python -y"

