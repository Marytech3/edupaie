from pathlib import Path
import os
import sys


ROOT_DIR = Path(__file__).resolve().parents[2]
try:
    _NUITKA_COMPILED = __compiled__
except NameError:
    _NUITKA_COMPILED = None

if getattr(sys, "frozen", False):
    RESOURCE_DIR = Path(sys._MEIPASS)
    APP_DATA_DIR = Path(os.environ.get("LOCALAPPDATA", Path.home())) / "EduPaie"
elif _NUITKA_COMPILED is not None:
    # In standalone mode the bundled schema and seed database sit beside the
    # executable. ``containing_dir`` on imported modules can refer to the
    # parent deployment directory, so derive this from the launched binary.
    RESOURCE_DIR = Path(sys.argv[0]).resolve().parent
    APP_DATA_DIR = Path(os.environ.get("LOCALAPPDATA", Path.home())) / "EduPaie"
else:
    RESOURCE_DIR = ROOT_DIR
    # Source runs and packaged runs share the same user data. This keeps the
    # database and receipt files in place when launching from the project.
    APP_DATA_DIR = Path(os.environ.get("LOCALAPPDATA", Path.home())) / "EduPaie"

SCHEMA_PATH = RESOURCE_DIR / "database" / "schema.sql"
SEED_DATABASE_PATH = RESOURCE_DIR / "data" / "edupaie_demo.db"
DATABASE_PATH = APP_DATA_DIR / "data" / "edupaie.db"
RECEIPTS_DIR = APP_DATA_DIR / "receipts"
