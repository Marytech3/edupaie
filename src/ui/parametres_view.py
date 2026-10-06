from datetime import datetime
from pathlib import Path
from pathlib import PurePosixPath
import sqlite3
import zipfile

from PySide6.QtCore import Signal
from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QFileDialog,
    QMessageBox, QFrame,
)

from src.utils.paths import RECEIPTS_DIR


class ParametresView(QWidget):
    donnees_restaurees = Signal()

    def __init__(self, db):
        super().__init__()
        self.db = db
        self.setObjectName("page")
        layout = QVBoxLayout(self)
        layout.setContentsMargins(28, 24, 28, 18)
        layout.setSpacing(14)

        titre = QLabel("Paramètres")
        titre.setObjectName("pageTitle")
        sous_titre = QLabel("Sauvegarder les données de l’application")
        sous_titre.setObjectName("pageSubtitle")
        layout.addWidget(titre)
        layout.addWidget(sous_titre)

        carte = QFrame()
        carte.setObjectName("backupCard")
        contenu = QVBoxLayout(carte)
        contenu.setContentsMargins(20, 18, 20, 18)
        contenu.setSpacing(10)

        entete = QLabel("Copie de sauvegarde")
        entete.setObjectName("sectionTitle")
        description = QLabel(
            "Enregistre les élèves, les paiements et les reçus PDF dans une archive ZIP. "
            "Choisis un emplacement facile à retrouver, par exemple une clé USB."
        )
        description.setWordWrap(True)
        description.setObjectName("mutedText")
        contenu.addWidget(entete)
        contenu.addWidget(description)

        actions = QHBoxLayout()
        actions.addStretch()
        self.btn_sauvegarder = QPushButton("Créer une sauvegarde")
        self.btn_sauvegarder.setObjectName("primaryButton")
        self.btn_sauvegarder.clicked.connect(self.creer_sauvegarde)
        actions.addWidget(self.btn_sauvegarder)
        self.btn_restaurer = QPushButton("Restaurer une sauvegarde")
        self.btn_restaurer.clicked.connect(self.restaurer_sauvegarde)
        actions.addWidget(self.btn_restaurer)
        contenu.addLayout(actions)
        layout.addWidget(carte)
        layout.addStretch()

    def creer_sauvegarde(self):
        nom = f"EduPaie_sauvegarde_{datetime.now():%Y-%m-%d_%H-%M}.zip"
        chemin, _ = QFileDialog.getSaveFileName(
            self, "Enregistrer la sauvegarde", str(Path.home() / "Documents" / nom),
            "Archive ZIP (*.zip)",
        )
        if not chemin:
            return
        destination = Path(chemin)
        if destination.suffix.lower() != ".zip":
            destination = destination.with_suffix(".zip")

        try:
            donnees_db = self.db.connection.serialize()
            with zipfile.ZipFile(destination, "w", zipfile.ZIP_DEFLATED) as archive:
                archive.writestr("data/edupaie.db", donnees_db)
                if RECEIPTS_DIR.exists():
                    for recu in RECEIPTS_DIR.rglob("*.pdf"):
                        chemin_relatif = PurePosixPath("receipts") / recu.relative_to(RECEIPTS_DIR).as_posix()
                        archive.write(recu, str(chemin_relatif))
            QMessageBox.information(
                self, "Sauvegarde terminée",
                f"La sauvegarde des données et des reçus a été créée ici :\n{destination}",
            )
        except (OSError, sqlite3.Error, zipfile.BadZipFile) as erreur:
            QMessageBox.critical(
                self, "Échec de la sauvegarde",
                f"La sauvegarde n’a pas pu être créée.\n\n{erreur}",
            )

    def restaurer_sauvegarde(self):
        chemin, _ = QFileDialog.getOpenFileName(
            self, "Choisir une sauvegarde EduPaie", str(Path.home() / "Documents"),
            "Archive ZIP (*.zip)",
        )
        if not chemin:
            return

        try:
            with zipfile.ZipFile(chemin, "r") as archive:
                donnees_db = archive.read("data/edupaie.db")
                recus = []
                for entree in archive.infolist():
                    nom = entree.filename.replace("\\", "/")
                    relatif = PurePosixPath(nom)
                    if (entree.is_dir() or relatif.is_absolute() or ".." in relatif.parts
                            or not relatif.parts or relatif.parts[0] != "receipts"
                            or relatif.suffix.lower() != ".pdf"):
                        continue
                    recus.append((relatif, archive.read(entree)))

            base_sauvegardee = sqlite3.connect(":memory:")
            base_actuelle = sqlite3.connect(":memory:")
            try:
                base_sauvegardee.deserialize(donnees_db)
                resultat = base_sauvegardee.execute("PRAGMA integrity_check").fetchone()
                tables = {
                    ligne[0] for ligne in base_sauvegardee.execute(
                        "SELECT name FROM sqlite_master WHERE type='table'"
                    )
                }
                if resultat is None or resultat[0] != "ok" or not {
                    "eleves", "paiements", "recus", "classes", "annees_scolaires"
                }.issubset(tables):
                    raise ValueError("Cette archive ne contient pas une base EduPaie valide.")
            except Exception:
                base_sauvegardee.close()
                base_actuelle.close()
                raise

            confirmation = QMessageBox.question(
                self,
                "Confirmer la restauration",
                "Cette opération remplacera la liste des élèves et les paiements actuels "
                "par ceux de la sauvegarde. Continuer ?",
                QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
                QMessageBox.StandardButton.No,
            )
            if confirmation != QMessageBox.StandardButton.Yes:
                base_sauvegardee.close()
                base_actuelle.close()
                return

            anciens_recus = {}
            try:
                self.db.connection.backup(base_actuelle)
                for relatif, contenu in recus:
                    destination = RECEIPTS_DIR.joinpath(*relatif.parts[1:])
                    anciens_recus[destination] = destination.read_bytes() if destination.exists() else None

                base_sauvegardee.backup(self.db.connection)
                for relatif, contenu in recus:
                    destination = RECEIPTS_DIR.joinpath(*relatif.parts[1:])
                    destination.parent.mkdir(parents=True, exist_ok=True)
                    destination.write_bytes(contenu)
            except Exception:
                base_actuelle.backup(self.db.connection)
                for destination, contenu in anciens_recus.items():
                    if contenu is None:
                        destination.unlink(missing_ok=True)
                    else:
                        destination.write_bytes(contenu)
                raise
            finally:
                base_sauvegardee.close()
                base_actuelle.close()

            self.donnees_restaurees.emit()
            QMessageBox.information(
                self, "Restauration terminée",
                "Les élèves, les paiements et les reçus de la sauvegarde ont été restaurés.",
            )
        except (OSError, sqlite3.Error, zipfile.BadZipFile, KeyError, ValueError) as erreur:
            QMessageBox.critical(
                self, "Échec de la restauration",
                f"La sauvegarde n’a pas pu être restaurée.\n\n{erreur}",
            )
