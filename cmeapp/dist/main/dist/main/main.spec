

# -*- mode: python ; coding: utf-8 -*-

import kivy
from kivy_deps import sdl2, glew
import reportlab

block_cipher = None


a = Analysis(['main.py'],
             pathex=[],
             binaries=[],
             datas=[],
             hiddenimports=["kivy","reportlab.lib.pagesizes","reportlab.pdfgen","reportlab.lib.units","reportlab.lib.utils","reportlab.lib.colors","reportlab.graphics.shapes","smtplib"],
             hookspath=[],
             hooksconfig={},
             runtime_hooks=[],
             excludes=[],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher,
             noarchive=False)
pyz = PYZ(a.pure, a.zipped_data,
             cipher=block_cipher)

a.datas +=[('Code\app.kv', 
'C:\\Users\\alber\\Desktop\\ALBERT\\FCF\\APP\\VERSIONS\\vers11\\cmeapp\app.kv', 
'DATA')]


exe = EXE(pyz,
          a.scripts, 
          [],
          exclude_binaries=True,
          name='cmeapp',
          debug=False,
          bootloader_ignore_signals=False,
          strip=False,
          upx=True,
          console=False,
          disable_windowed_traceback=False,
          target_arch=None,
          codesign_identity=None,
          entitlements_file=None )
coll = COLLECT(exe, Tree('C:\\Users\\alber\\Desktop\\ALBERT\\FCF\\APP\\VERSIONS\\vers11\\cmeapp\\'),
               a.binaries,
               a.zipfiles,
               a.datas, 
	       *[Tree(p) for p in 
               (sdl2.dep_bins + glew.dep_bins)],
               strip=False,
               upx=True,
               upx_exclude=[],
               name='main')
