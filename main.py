import sys
from PySide6.QtWidgets import QApplication

from src.data1.database import Database
from src.ui.main_window import MainWindow
from src.utils.paths import DATABASE_PATH, SCHEMA_PATH, RECEIPTS_DIR


def initialiser_base_de_donnees():
    db = Database(DATABASE_PATH)

    with open(SCHEMA_PATH, "r", encoding="utf-8") as fichier:
        db.executescript(fichier.read())

    RECEIPTS_DIR.mkdir(exist_ok=True)
    return db


if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setApplicationName("EduPaie")

    db = initialiser_base_de_donnees()

    window = MainWindow(db)
    window.show()

    code_retour = app.exec()
    db.close()
    sys.exit(code_retour)