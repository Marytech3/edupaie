"""Ajoute les répertoires des extensions Qt au chemin DLL Windows."""

import os
import sys


if sys.platform == "win32" and getattr(sys, "frozen", False):
    _base = getattr(sys, "_MEIPASS", os.path.dirname(sys.executable))
    _dll_directory_handles = []
    for _relative in ("PySide6", "shiboken6"):
        _directory = os.path.join(_base, _relative)
        if os.path.isdir(_directory):
            _dll_directory_handles.append(os.add_dll_directory(_directory))
