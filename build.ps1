$ErrorActionPreference = "Stop"

if (!(Get-Command "7z.exe" -ErrorAction SilentlyContinue)) {Throw "Unable to locate 7z.exe."}

if(!(Test-Path -Path ".\pytess.py" )) {Throw "You are in the wrong directory..."}
if(!(Test-Path -Path ".\icon.ico" )) {Throw "Unable to locate icon.ico..."}
if(!(Test-Path -Path ".\readme.txt" )) {Throw "Unable to locate readme.txt..."}
if(!(Test-Path -Path ".\bin" )) {Throw "You do not have the required bin directory..."}

if((Test-Path -Path ".\pytess" )) {Remove-Item ".\pytess" -Recurse -Force}
if((Test-Path -Path ".\build" )) {Remove-Item ".\build" -Recurse -Force}
if((Test-Path -Path ".\dist" )) {Remove-Item ".\dist" -Recurse -Force}
if((Test-Path -Path ".\__pycache__" )) {Remove-Item ".\__pycache__" -Recurse -Force}
if((Test-Path -Path ".\pytess.zip" )) {Remove-Item ".\pytess.zip"  -Force}

pyinstaller.exe --clean --console --onefile ".\pytess.spec"
if ( ! $lastExitCode -eq 0 ) { Throw "Error running pyinstaller.exe" }

Rename-Item -Path ".\dist" -NewName ".\pytess"
Copy-Item ".\readme.txt" -Destination ".\pytess\readme.txt"
7z.exe a ".\pytess.zip" ".\pytess"
if ( ! $lastExitCode -eq 0 ) { Throw "Error running 7z.exe" }
