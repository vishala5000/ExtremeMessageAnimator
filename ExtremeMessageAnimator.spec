# -*- mode: python ; coding: utf-8 -*-

from PyInstaller.utils.hooks import collect_dynamic_libs


block_cipher = None


pygame_binaries = collect_dynamic_libs(
    "pygame"
)


a = Analysis(
    ["app.py"],
    pathex=[],
    binaries=pygame_binaries,
    datas=[],
    hiddenimports=[
        "pygame",
        "pygame.base",
        "pygame.constants",
        "pygame.display",
        "pygame.draw",
        "pygame.font",
        "pygame.image",
        "pygame.key",
        "pygame.mixer",
        "pygame.mouse",
        "pygame.surface",
        "pygame.time",
        "pygame.transform",
        "pygame.event",
    ],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)


pyz = PYZ(
    a.pure,
    a.zipped_data,
    cipher=block_cipher
)


exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.datas,
    [],
    name="ExtremeMessageAnimator",
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=False,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)
