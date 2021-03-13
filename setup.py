# -*- coding: utf-8 -*-
from setuptools import setup
import sys

if sys.platform == "win32":
    # 윈도우용
    import py2exe
    platform_options = {
        "windows": [{
            "script": "main.py",
            "icon_resources": [(1, "img/icon.ico")],
            "dest_base": "dodo"
        }],
        "zipfile": None,
        "setup_requires": ["py2exe"],
        "options": {
            "py2exe": {
                "includes": ["PyQt5.QtCore",
                             "PyQt5.QtWidgets",
                             "requests",
                             "bs4",
                             "m3u8",
                             "shutil"],
                "dll_excludes": ["w9xpopen.exe",
                                 "msvcr71.dll",
                                 "MSVCP90.dll"],
                "compressed": True
            }
        }
    }
elif sys.platform == "darwin":
    # 맥용
    platform_options = {
        "setup_requires": ["py2app"],
        "app": ["main.py"],
        "options": {
            "py2app": {
                "argv_emulation": True,
                "includes": ["PyQt5.QtCore",
                             "PyQt5.QtWidgets",
                             "requests",
                             "bs4",
                             "m3u8",
                             "shutil"],
                "iconfile": "img/icon.ico"
            }
        }
    }

else:
    # 스크립트
    platform_options = {
        "scripts": ["main.py"]
    }

setup(name="LearnUs Downloader", description="LearnUs 강의 영상 다운로더", version="1.0.0", **platform_options)
