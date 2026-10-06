from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QComboBox, QTableWidget,
    QTableWidgetItem, QPushButton, QGroupBox, QHeaderView,
)

from src.services.dashboard_service import DashboardService


def formater_montant(valeur):
    return f"{float(valeur):,.0f} FCFA".replace(",", " ")


class DashboardView(QWidget):
    def __init__(self, db):
        super().__init__()
        self.setObjectName("page")
        self.service = DashboardService(db)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(28, 24, 28, 18)
        layout.setSpacing(14)
        entete = QHBoxLayout()
        titre = QLabel("Tableau de bord")
        titre.setObjectName("pageTitle")
        intro = QVBoxLayout()
        intro.setSpacing(2)
        intro.addWidget(titre)
        description = QLabel("Suivez les frais et les encaissements de l’établissement")
        description.setObjectName("pageSubtitle")
        intro.addWidget(description)
        self.filtre_statut = QComboBox()
        self.filtre_statut.addItems([
            "Tous les statuts", "Non payé", "Partiellement payé", "Soldé"
        ])
        self.btn_actualiser = QPushButton("Actualiser")
        entete.addLayout(intro)
        entete.addStretch()
        entete.addWidget(QLabel("Afficher :"))
        entete.addWidget(self.filtre_statut)
        entete.addWidget(self.btn_actualiser)
        layout.addLayout(entete)

        indicateurs = QHBoxLayout()
        self.valeurs = {}
        for cle, libelle in (
            ("nombre_eleves", "Élèves inscrits"),
            ("total_encaisse", "Total encaissé"),
            ("total_restant", "Reste à encaisser"),
            ("nombre_non_soldes", "Élèves non soldés"),
        ):
            groupe = QGroupBox(libelle)
            boite = QVBoxLayout(groupe)
            valeur = QLabel("0")
            valeur.setAlignment(Qt.AlignmentFlag.AlignCenter)
            valeur.setStyleSheet("font-size: 20px; font-weight: bold; padding: 10px;")
            boite.addWidget(valeur)
            indicateurs.addWidget(groupe)
            self.valeurs[cle] = valeur
        layout.addLayout(indicateurs)

        layout.addWidget(QLabel("Suivi des paiements par élève"))
        self.table = QTableWidget(0, 7)
        self.table.setObjectName("dataTable")
        self.table.setHorizontalHeaderLabels([
            "Nom", "Prénom", "Classe", "Année scolaire", "Total dû",
            "Payé", "Solde / statut",
        ])
        self.table.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
        self.table.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
        self.table.setAlternatingRowColors(True)
        self.table.setShowGrid(False)
        self.table.verticalHeader().setVisible(False)
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.ResizeToContents)
        self.table.horizontalHeader().setSectionResizeMode(0, QHeaderView.ResizeMode.Stretch)
        layout.addWidget(self.table)

        self.btn_actualiser.clicked.connect(self.actualiser)
        self.filtre_statut.currentTextChanged.connect(self.charger_eleves)
        self.actualiser()

    def actualiser(self):
        donnees = self.service.indicateurs()
        self.valeurs["nombre_eleves"].setText(str(donnees["nombre_eleves"]))
        self.valeurs["total_encaisse"].setText(formater_montant(donnees["total_encaisse"]))
        self.valeurs["total_restant"].setText(formater_montant(donnees["total_restant"]))
        self.valeurs["nombre_non_soldes"].setText(str(donnees["nombre_non_soldes"]))
        self.charger_eleves()

    def charger_eleves(self):
        eleves = self.service.lister_eleves(self.filtre_statut.currentText())
        self.table.setRowCount(len(eleves))
        for ligne, eleve in enumerate(eleves):
            valeurs = [
                eleve["nom"], eleve["prenom"], eleve["classe"],
                eleve["annee_scolaire"], formater_montant(eleve["total_du"]),
                formater_montant(eleve["total_paye"]),
                f"{formater_montant(eleve['solde'])} - {eleve['statut']}",
            ]
            for colonne, valeur in enumerate(valeurs):
                self.table.setItem(ligne, colonne, QTableWidgetItem(str(valeur)))
        self.table.resizeColumnsToContents()
