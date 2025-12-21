# -*- mode: python ; coding: utf-8 -*-
from PyInstaller.utils.hooks import collect_all

datas = [('C:\\Users\\harry\\OneDrive\\Desktop\\Ai-Directory-Organizer-main\\version2\\config', 'config')]
binaries = []
hiddenimports = ['tkinter', 'tkinter.ttk', 'tkinter.filedialog', 'tkinter.messagebox', 'tkinter.scrolledtext', 'file_analyzer', 'ai_categorizer', 'directory_organizer', 'duplicate_detector', 'file_filter', 'file_statistics', 'undo_manager', 'config_manager', 'cloud_storage']
tmp_ret = collect_all('magic')
datas += tmp_ret[0]; binaries += tmp_ret[1]; hiddenimports += tmp_ret[2]
tmp_ret = collect_all('yaml')
datas += tmp_ret[0]; binaries += tmp_ret[1]; hiddenimports += tmp_ret[2]


a = Analysis(
    ['C:\\Users\\harry\\OneDrive\\Desktop\\Ai-Directory-Organizer-main\\version2\\src\\gui_main.py'],
    pathex=['C:\\Users\\harry\\OneDrive\\Desktop\\Ai-Directory-Organizer-main\\version2\\src'],
    binaries=binaries,
    datas=datas,
    hiddenimports=hiddenimports,
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
    optimize=0,
)
pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.datas,
    [],
    name='DirectoryManagementSystem',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)
