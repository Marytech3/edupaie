import json

from PySide6.QtCore import Qt, QUrl, Signal
from PySide6.QtGui import QDesktopServices
from PySide6.QtWidgets import (
    QFrame,
    QHBoxLayout,
    QLabel,
    QPushButton,
    QTableWidget,
    QTableWidgetItem,
    QVBoxLayout,
    QWidget,
    QHeaderView,
    QMessageBox,
)

from src.data1.eleve_repository import EleveRepository
from src.data1.paiement_repository import PaiementRepository
from src.services.recu_service import RecuService


def formater_montant(valeur):
    return f"{float(valeur):,.0f} FCFA".replace(",", " ")


class EleveProfileView(QWidget):
    retour_demande = Signal()
    paiement_demande = Signal(int)
    modification_demandee = Signal(int)

    def __init__(self, db, parent=None):
        super().__init__(parent)
        self.setObjectName("page")
        self.db = db
        self.eleves = EleveRepository(db)
        self.paiements_repo = PaiementRepository(db)
        self.eleve_id = None
        self.paiements = []

        layout = QVBoxLayout(self)
        layout.setContentsMargins(28, 22, 28, 18)
        layout.setSpacing(14)

        self.btn_retour = QPushButton("←  Retour à la liste")
        self.btn_retour.setObjectName("backButton")
        self.btn_retour.clicked.connect(self.retour_demande.emit)
        layout.addWidget(self.btn_retour, 0, Qt.AlignmentFlag.AlignLeft)

        entete = QHBoxLayout()
        identite = QVBoxLayout()
        identite.setSpacing(3)
        self.nom_label = QLabel()
        self.nom_label.setObjectName("pageTitle")
        self.details_label = QLabel()
        self.details_label.setObjectName("pageSubtitle")
        identite.addWidget(self.nom_label)
        identite.addWidget(self.details_label)
        entete.addLayout(identite)
        entete.addStretch()
        self.statut_label = QLabel()
        self.statut_label.setObjectName("statusBadge")
        entete.addWidget(self.statut_label, 0, Qt.AlignmentFlag.AlignTop)
        layout.addLayout(entete)

        cartes = QHBoxLayout()
        cartes.setSpacing(12)
        self.frais_value = self.creer_carte(cartes, "Frais annuels")
        self.frais_value.setObjectName("metricDue")
        self.paye_value = self.creer_carte(cartes, "Total réglé")
        self.paye_value.setObjectName("metricPaid")
        self.solde_value = self.creer_carte(cartes, "Solde restant")
        self.solde_value.setObjectName("metricBalance")
        layout.addLayout(cartes)

        actions = QHBoxLayout()
        actions.setSpacing(8)
        self.btn_paiement = QPushButton("Nouveau paiement")
        self.btn_paiement.setObjectName("primaryButton")
        self.btn_modifier = QPushButton("Modifier la fiche")
        self.btn_dernier_recu = QPushButton("Ouvrir le dernier reçu")
        self.btn_paiement.clicked.connect(
            lambda: self.paiement_demande.emit(self.eleve_id)
        )
        self.btn_modifier.clicked.connect(
            lambda: self.modification_demandee.emit(self.eleve_id)
        )
        self.btn_dernier_recu.clicked.connect(self.ouvrir_dernier_recu)
        actions.addWidget(self.btn_paiement)
        actions.addWidget(self.btn_modifier)
        actions.addWidget(self.btn_dernier_recu)
        actions.addStretch()
        layout.addLayout(actions)

        titre_historique = QLabel("Historique des paiements")
        titre_historique.setObjectName("sectionTitle")
        layout.addWidget(titre_historique)
        self.historique_etat = QLabel()
        self.historique_etat.setObjectName("pageSubtitle")
        layout.addWidget(self.historique_etat)

        self.table = QTableWidget(0, 4)
        self.table.setObjectName("dataTable")
        self.table.setHorizontalHeaderLabels([
            "Date", "Montant", "Mode de paiement", "N° du reçu",
        ])
        self.table.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
        self.table.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
        self.table.setAlternatingRowColors(True)
        self.table.setShowGrid(False)
        self.table.verticalHeader().setVisible(False)
        self.table.horizontalHeader().setSectionResizeMode(
            QHeaderView.ResizeMode.Stretch
        )
        self.table.cellDoubleClicked.connect(self.ouvrir_recu_selectionne)
        layout.addWidget(self.table, 1)

    @staticmethod
    def creer_carte(parent_layout, titre):
        carte = QFrame()
        carte.setObjectName("metricCard")
        contenu = QVBoxLayout(carte)
        contenu.setContentsMargins(18, 13, 18, 13)
        contenu.setSpacing(4)
        etiquette = QLabel(titre.upper())
        etiquette.setObjectName("metricLabel")
        valeur = QLabel("0 FCFA")
        valeur.setObjectName("metricValue")
        contenu.addWidget(etiquette)
        contenu.addWidget(valeur)
        parent_layout.addWidget(carte, 1)
        return valeur

    def charger(self, eleve_id):
        self.eleve_id = eleve_id
        eleve = self.eleves.obtenir_par_id(eleve_id)
        solde = max(0.0, float(self.eleves.calculer_solde(eleve_id)))
        total_du = float(eleve["total_du"])
        total_paye = max(0.0, total_du - solde)

        if total_paye <= 0:
            statut = "Non payé"
        elif solde <= 0:
            statut = "Soldé"
        else:
            statut = "Partiellement payé"

        self.nom_label.setText(f"{eleve['nom']} {eleve['prenom']}")
        self.details_label.setText(
            f"{eleve['classe']}  ·  Année {eleve['annee_scolaire']}"
        )
        self.statut_label.setText(statut)
        couleurs = {
            "Soldé": ("#ddf3e5", "#176437"),
            "Partiellement payé": ("#fff1c2", "#805300"),
            "Non payé": ("#fce0e2", "#a1232c"),
        }
        fond, texte = couleurs[statut]
        self.statut_label.setStyleSheet(
            f"background-color:{fond};color:{texte};border-radius:12px;"
            "padding:6px 14px;font-weight:600;"
        )

        self.frais_value.setText(formater_montant(total_du))
        self.paye_value.setText(formater_montant(total_paye))
        self.solde_value.setText(formater_montant(solde))

        self.paiements = self.paiements_repo.lister_par_eleve(eleve_id)
        self.historique_etat.setText(
            "" if self.paiements else "Aucun paiement n’a encore été enregistré pour cet élève."
        )
        self.table.setRowCount(len(self.paiements))
        for ligne, paiement in enumerate(self.paiements):
            valeurs = (
                paiement["date_paiement"],
                formater_montant(paiement["montant"]),
                paiement["mode_paiement"],
                paiement["numero_recu"],
            )
            for colonne, valeur in enumerate(valeurs):
                item = QTableWidgetItem(str(valeur))
                item.setData(Qt.ItemDataRole.UserRole, paiement["id"])
                self.table.setItem(ligne, colonne, item)
        self.btn_dernier_recu.setEnabled(bool(self.paiements))

    def ouvrir_dernier_recu(self):
        if self.paiements:
            self.ouvrir_recu(self.paiements[-1])

    def ouvrir_recu_selectionne(self, ligne, _colonne):
        if 0 <= ligne < len(self.paiements):
            self.ouvrir_recu(self.paiements[ligne])

    def ouvrir_recu(self, paiement):
        try:
            contenu = json.loads(paiement["contenu_json"])
            chemin = RecuService().generer_pdf(contenu)
            QDesktopServices.openUrl(QUrl.fromLocalFile(str(chemin)))
        except Exception as erreur:
            QMessageBox.critical(
                self,
                "Erreur lors de l’ouverture du reçu",
                f"Le reçu n’a pas pu être ouvert : {erreur}",
            )
