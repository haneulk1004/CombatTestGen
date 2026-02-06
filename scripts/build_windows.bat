@echo off
echo Building CombatTestGen...

rem Change to project root (parent of script dir)
pushd %~dp0\..

rem Activate venv if exists
if exist "venv\Scripts\activate.bat" (
    call venv\Scripts\activate.bat
)

rem Run PyInstaller
pyinstaller --clean --noconfirm combattestgen.spec

echo Build complete. Check dist/ folder.
popd
pause
