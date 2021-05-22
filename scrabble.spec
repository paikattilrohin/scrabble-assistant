# -*- mode: python ; coding: utf-8 -*-


block_cipher = None


a = Analysis(['scrabble.py'],
             pathex=['/Users/hobonobleXD/Desktop/Code_Base/Scrabble'],
             binaries=[],
             datas=[('scrabble_words.json', '.'), ('COMIC.TTF', '.'), ('happy_birthday_dumbass.mp3', '.'), ('happy_birthday_video.mp4', '.')],
             hiddenimports=[],
             hookspath=[],
             runtime_hooks=[],
             excludes=[],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher,
             noarchive=False)
pyz = PYZ(a.pure, a.zipped_data,
             cipher=block_cipher)
exe = EXE(pyz,
          a.scripts,
          a.binaries,
          a.zipfiles,
          a.datas,
          [],
          name='scrabble',
          debug=False,
          bootloader_ignore_signals=False,
          strip=False,
          upx=True,
          upx_exclude=[],
          runtime_tmpdir=None,
          console=True )
