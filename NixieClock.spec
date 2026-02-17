# -*- mode: python ; coding: utf-8 -*-
# PyInstaller spec dla Nixie Clock Control
# Generuje macOS .app bundle

block_cipher = None

a = Analysis(
    ['main_unified.py'],
    pathex=[],
    binaries=[],
    datas=[],
    hiddenimports=[
        'serial',
        'serial.tools',
        'serial.tools.list_ports',
        'PyQt6',
        'PyQt6.QtWidgets',
        'PyQt6.QtCore',
        'PyQt6.QtGui',
        # Moduły aplikacji
        'config',
        'styles',
        'widgets',
        'config_vintage',
        'styles_vintage',
        'widgets_vintage',
        'serial_handler',
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

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name='NixieClock',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=False,  # Bez okna terminala
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)

coll = COLLECT(
    exe,
    a.binaries,
    a.zipfiles,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name='NixieClock',
)

app = BUNDLE(
    coll,
    name='Zegar Nixie Z5700M.app',
    icon='NixieClock.icns',
    bundle_identifier='pl.nixie.clock',
    info_plist={
        'CFBundleName': 'Zegar Nixie Z5700M',
        'CFBundleDisplayName': 'Zegar Nixie Z5700M',
        'CFBundleVersion': '1.0.0',
        'CFBundleShortVersionString': '1.0',
        'NSHighResolutionCapable': True,
        'NSRequiresAquaSystemAppearance': False,  # Dark mode support
        'LSMinimumSystemVersion': '11.0',
        'NSHumanReadableCopyright': '© 2025 Nixie Clock',
        # Uprawnienia do portów szeregowych USB
        'com.apple.security.device.usb': True,
        'NSBluetoothAlwaysUsageDescription': 'Aplikacja używa portu szeregowego do komunikacji z zegarem.',
    },
)
