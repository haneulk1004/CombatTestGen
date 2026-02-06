#!/bin/bash
echo "Building CombatTestGen..."

# Activate venv if exists
if [ -f "../venv/bin/activate" ]; then
    source ../venv/bin/activate
fi

# Run PyInstaller
pyinstaller --clean --noconfirm ../combattestgen.spec

echo "Build complete. Check dist/ folder."
