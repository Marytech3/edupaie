"""Capture les écrans EduPaie à partir de la base de démonstration locale."""

import os
from pathlib import Path
import sys

os.environ.setdefault("QT_QPA_PLATFORM", "offscreen")
ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from PySide6.QtCore import Qt
from PySide6.QtGui import QFontDatabase
from PySide6.QtWidgets import QApplication

from src.data1.database import Database
from src.ui.main_window import MainWindow
from src.ui.theme import STYLE_SHEET


SORTIE = ROOT / "docs" / "assets"


def main():
    SORTIE.mkdir(parents=True, exist_ok=True)
    app = QApplication([])
    for fichier_police in ("segoeui.ttf", "segoeuib.ttf"):
        QFontDatabase.addApplicationFont(str(Path("C:/Windows/Fonts") / fichier_police))
    app.setApplicationName("EduPaie")
    app.setStyleSheet(STYLE_SHEET)

    db = Database(ROOT / "data" / "edupaie_demo.db")
    window = MainWindow(db)
    window.resize(1440, 900)
    window.show()
    app.processEvents()

    window.grab().save(str(SORTIE / "tableau_de_bord.png"))
    window.btn_eleves.click()
    app.processEvents()
    window.grab().save(str(SORTIE / "liste_eleves.png"))

    if window.eleves_page.table.rowCount():
        ligne_fiche = next(
            (ligne for ligne in range(window.eleves_page.table.rowCount())
             if "Partiellement" in window.eleves_page.table.item(ligne, 6).text()),
            0,
        )
        eleve_id = window.eleves_page.table.item(ligne_fiche, 0).data(Qt.ItemDataRole.UserRole)
        window.eleves_page.ouvrir_profil(eleve_id)
        app.processEvents()
        window.grab().save(str(SORTIE / "fiche_eleve.png"))

    window.btn_parametres.click()
    app.processEvents()
    window.grab().save(str(SORTIE / "parametres.png"))

    window.close()
    db.close()
    app.quit()


if __name__ == "__main__":
    main()
