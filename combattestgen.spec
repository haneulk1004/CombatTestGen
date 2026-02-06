# -*- mode: python ; coding: utf-8 -*-
from PyInstaller.utils.hooks import collect_data_files
import sys

block_cipher = None

# Collect customtkinter data files (themes, etc.)
datas = collect_data_files('customtkinter')

# Add templates directory
datas.append(('src/templates', 'src/templates'))

a = Analysis(
    ['src/cli/main.py'],
    pathex=[],
    binaries=[],
    datas=datas,
    hiddenimports=['src.gui.main_window', 'PIL._tkinter_finder'],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)
pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

# Single file executable
exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name='CombatTestGen',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=True, # Keep console for CLI usage. GUI will launch as separate window but console remains.
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon=None # Add icon later if needed
)
