from pathlib import Path


ROOT_DIR = Path(__file__).resolve().parents[2]
DATABASE_PATH = ROOT_DIR / "data" / "edupaie.db"
SCHEMA_PATH = ROOT_DIR / "database" / "schema.sql"
RECEIPTS_DIR = ROOT_DIR / "receipts"