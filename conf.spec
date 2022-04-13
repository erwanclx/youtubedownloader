# -*- mode: python ; coding: utf-8 -*-

import sys
import os

from kivy_deps import sdl2, glew

from kivymd import hooks_path as kivymd_hooks_path

path = os.path.abspath(".")

a = Analysis(
    ["main.py"],
    pathex=[path],
    hookspath=[kivymd_hooks_path],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=None,
    noarchive=False,
    hiddenimports=[
        "libs.baseclass.bottom_app_bar",
        "libs.baseclass.bottom_sheet",
        "libs.baseclass.cards",
        "libs.baseclass.chips",
        "libs.baseclass.data_tables",
        "libs.baseclass.dialog_change_theme",
        "libs.baseclass.dialogs",
        "libs.baseclass.drop_item",
        "libs.baseclass.expansionpanel",
        "libs.baseclass.filemanager",
        "libs.baseclass.grid",
        "libs.baseclass.home",
        "libs.baseclass.list_items",
        "libs.baseclass.md_icons",
        "libs.baseclass.menu",
        "libs.baseclass.navigation_drawer",
        "libs.baseclass.pickers",
        "libs.baseclass.refresh_layout",
        "libs.baseclass.snackbar",
        "libs.baseclass.stack_buttons",
        "libs.baseclass.tabs",
        "libs.baseclass.taptargetview",
        "libs.baseclass.textfields",
        "libs.baseclass.toggle_button",
        "libs.baseclass.toolbar",
        "libs.baseclass.user_animation_card",
        "kivymd.stiffscroll",
    ],	
)
pyz = PYZ(a.pure, a.zipped_data, cipher=None)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    *[Tree(p) for p in (sdl2.dep_bins + glew.dep_bins)],
    debug=False,
    strip=False,
    upx=True,
    name="Youtube Downloader",
    icon="icon.ico",
    console=False,
)