import sys
import shutil
import traceback
from PySide6.QtWidgets import QApplication, QMessageBox

from src.data1.database import Database
from src.data1.referentiel_repository import ReferentielRepository
from src.ui.main_window import MainWindow
from src.ui.theme import STYLE_SHEET
from src.utils.paths import (
    DATABASE_PATH, SCHEMA_PATH, SEED_DATABASE_PATH, RECEIPTS_DIR,
)


def initialiser_base_de_donnees():
    DATABASE_PATH.parent.mkdir(parents=True, exist_ok=True)
    if not DATABASE_PATH.exists() and SEED_DATABASE_PATH.exists():
        shutil.copy2(SEED_DATABASE_PATH, DATABASE_PATH)
    db = Database(DATABASE_PATH)

    with open(SCHEMA_PATH, "r", encoding="utf-8") as fichier:
        db.executescript(fichier.read())

    ReferentielRepository(db).initialiser()
    RECEIPTS_DIR.mkdir(exist_ok=True)
    return db



if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setApplicationName("EduPaie")
    app.setStyleSheet(STYLE_SHEET)
    db = None
    try:
        db = initialiser_base_de_donnees()
        window = MainWindow(db)
        window.show()
        code_retour = app.exec()
    except Exception as erreur:
        journal = DATABASE_PATH.parent / "startup_error.log"
        journal.parent.mkdir(parents=True, exist_ok=True)
        journal.write_text(traceback.format_exc(), encoding="utf-8")
        QMessageBox.critical(
            None,
            "EduPaie n'a pas pu démarrer",
            f"Une erreur empêche l'ouverture de l'application.\n\n{erreur}\n\n"
            f"Détails enregistrés dans :\n{journal}",
        )
        code_retour = 1
    finally:
        if db is not None:
            db.close()
    sys.exit(code_retour)
