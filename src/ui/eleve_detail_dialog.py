import json

from PySide6.QtCore import QUrl
from PySide6.QtGui import QDesktopServices
from PySide6.QtWidgets import (
    QDialog, QVBoxLayout, QLabel, QTableWidget, QTableWidgetItem,
    QHBoxLayout, QPushButton, QMessageBox,
)

from src.data1.eleve_repository import EleveRepository
from src.data1.paiement_repository import PaiementRepository
from src.services.recu_service import RecuService


class EleveDetailDialog(QDialog):
    def __init__(self, db, eleve_id, parent=None):
        super().__init__(parent)
        self.db = db
        self.eleve_id = eleve_id
        self.paiements = PaiementRepository(db)
        self.setWindowTitle("Fiche élève et historique des paiements")
        self.resize(760, 430)

        layout = QVBoxLayout(self)
        eleve = EleveRepository(db).obtenir_par_id(eleve_id)
        solde = EleveRepository(db).calculer_solde(eleve_id)
        layout.addWidget(QLabel(
            f"{eleve['prenom']} {eleve['nom']} - {eleve['classe']} - "
            f"{eleve['annee_scolaire']} - Solde : {float(solde):,.0f} FCFA"
        ))
        self.etat_label = QLabel("Paiements, du plus ancien au plus récent")
        layout.addWidget(self.etat_label)

        self.table = QTableWidget(0, 4)
        self.table.setHorizontalHeaderLabels([
            "Date", "Montant", "Mode de paiement", "N° du reçu"
        ])
        self.table.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
        self.table.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
        layout.addWidget(self.table)

        boutons = QHBoxLayout()
        self.btn_reimprimer = QPushButton("Réimprimer le reçu sélectionné")
        fermer = QPushButton("Fermer")
        boutons.addWidget(self.btn_reimprimer)
        boutons.addStretch()
        boutons.addWidget(fermer)
        layout.addLayout(boutons)
        self.btn_reimprimer.clicked.connect(self.reimprimer_recu)
        fermer.clicked.connect(self.accept)
        self.charger_historique()

    def charger_historique(self):
        self.lignes = self.paiements.lister_par_eleve(self.eleve_id)
        if not self.lignes:
            self.etat_label.setText("Aucun paiement n’a encore été enregistré pour cet élève.")
        self.table.setRowCount(len(self.lignes))
        for rang, paiement in enumerate(self.lignes):
            valeurs = [
                paiement["date_paiement"],
                f"{float(paiement['montant']):,.0f} FCFA",
                paiement["mode_paiement"],
                paiement["numero_recu"],
            ]
            for colonne, valeur in enumerate(valeurs):
                self.table.setItem(rang, colonne, QTableWidgetItem(str(valeur)))
        self.table.resizeColumnsToContents()
        self.btn_reimprimer.setEnabled(bool(self.lignes))

    def reimprimer_recu(self):
        rang = self.table.currentRow()
        if rang < 0:
            QMessageBox.information(self, "Sélection requise", "Sélectionnez un paiement dans l’historique.")
            return
        paiement = self.lignes[rang]
        try:
            contenu = json.loads(paiement["contenu_json"])
            chemin = RecuService().generer_pdf(contenu)
            QDesktopServices.openUrl(QUrl.fromLocalFile(str(chemin)))
        except Exception as erreur:
            QMessageBox.critical(self, "Erreur PDF", f"Le reçu n'a pas pu être réimprimé : {erreur}")
