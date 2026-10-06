from src.services.paiement_service import PaiementService
from src.ui.paiement_dialog import PaiementDialog

from PySide6.QtCore import Qt
from PySide6.QtCore import QUrl
from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QLineEdit,
    QComboBox,
    QLabel,
    QPushButton,
    QStackedWidget,
    QTableWidget,
    QTableWidgetItem,
    QMessageBox,
    QHeaderView,
)
from PySide6.QtGui import QColor, QDesktopServices

from src.data1.eleve_repository import EleveRepository
from src.data1.referentiel_repository import ReferentielRepository
from src.ui.eleve_dialog import EleveDialog
from src.ui.eleve_profile_view import EleveProfileView


class ElevesView(QWidget):
    def __init__(self, db):
        super().__init__()
        self.setObjectName("page")
        self.db = db
        self.eleve_repo = EleveRepository(db)
        self.referentiel_repo = ReferentielRepository(db)

        conteneur = QVBoxLayout(self)
        conteneur.setContentsMargins(0, 0, 0, 0)
        self.pages_eleves = QStackedWidget()
        conteneur.addWidget(self.pages_eleves)

        self.liste_page = QWidget()
        self.liste_page.setObjectName("page")
        self.pages_eleves.addWidget(self.liste_page)
        self.profil_page = EleveProfileView(db)
        self.pages_eleves.addWidget(self.profil_page)

        layout = QVBoxLayout(self.liste_page)
        layout.setContentsMargins(28, 24, 28, 18)
        layout.setSpacing(12)

        titre = QLabel("Élèves")
        titre.setObjectName("pageTitle")
        sous_titre = QLabel("Recherchez, filtrez, puis double-cliquez pour ouvrir une fiche")
        sous_titre.setObjectName("pageSubtitle")
        layout.addWidget(titre)
        layout.addWidget(sous_titre)

        barre_recherche = QHBoxLayout()
        barre_recherche.setSpacing(8)
        self.recherche_input = QLineEdit()
        self.recherche_input.setPlaceholderText("Rechercher un élève, une classe...")

        self.filtre_classe = QComboBox()
        self.filtre_classe.addItem("Toutes les classes", None)
        self.filtre_statut = QComboBox()
        self.filtre_statut.addItems([
            "Tous les statuts", "Soldé", "Partiellement payé", "Non payé"
        ])

        barre_recherche.addWidget(self.recherche_input, 1)
        barre_recherche.addWidget(self.filtre_classe)
        barre_recherche.addWidget(self.filtre_statut)
        layout.addLayout(barre_recherche)

        self.btn_ajouter = QPushButton("Ajouter un élève")
        self.btn_ajouter.setObjectName("primaryButton")
        self.btn_modifier = QPushButton("Modifier")
        self.btn_supprimer = QPushButton("Supprimer")
        self.btn_paiement = QPushButton("Encaisser un paiement")
        self.btn_historique = QPushButton("Historique des paiements")

        actions = QHBoxLayout()
        self.nombre_eleves_label = QLabel("0 élève")
        self.nombre_eleves_label.setObjectName("mutedText")
        actions.addWidget(self.nombre_eleves_label)
        actions.addStretch()
        actions.addWidget(self.btn_modifier)
        actions.addWidget(self.btn_supprimer)
        actions.addWidget(self.btn_paiement)
        actions.addWidget(self.btn_historique)
        actions.addWidget(self.btn_ajouter)

        self.table = QTableWidget()
        self.table.setObjectName("dataTable")
        self.table.setColumnCount(7)
        self.table.setHorizontalHeaderLabels([
            "Élève", "Classe", "Année", "Dû", "Payé", "Solde", "Statut",
        ])
        self.table.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
        self.table.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
        self.table.setAlternatingRowColors(True)
        self.table.setShowGrid(False)
        self.table.verticalHeader().setVisible(False)
        self.table.horizontalHeader().setSectionResizeMode(0, QHeaderView.ResizeMode.Stretch)
        for colonne in range(1, 7):
            self.table.horizontalHeader().setSectionResizeMode(
                colonne, QHeaderView.ResizeMode.ResizeToContents
            )

        layout.addWidget(self.table)
        layout.addLayout(actions)

        self.charger_classes()
        self.charger_eleves()

        self.recherche_input.textChanged.connect(self.charger_eleves)
        self.filtre_classe.currentIndexChanged.connect(self.charger_eleves)
        self.filtre_statut.currentIndexChanged.connect(self.charger_eleves)
        self.btn_ajouter.clicked.connect(self.ajouter_eleve)
        self.btn_modifier.clicked.connect(self.modifier_eleve)
        self.btn_supprimer.clicked.connect(self.supprimer_eleve)
        self.btn_paiement.clicked.connect(self.enregistrer_paiement)
        self.btn_historique.clicked.connect(self.ouvrir_historique_selectionne)
        self.table.cellDoubleClicked.connect(self.ouvrir_fiche_eleve)
        self.profil_page.retour_demande.connect(self.retourner_a_la_liste)
        self.profil_page.paiement_demande.connect(self.enregistrer_paiement)
        self.profil_page.modification_demandee.connect(self.modifier_eleve)

    def ouvrir_fiche_eleve(self, ligne, _colonne):
        eleve_id = self.table.item(ligne, 0).data(Qt.ItemDataRole.UserRole)
        self.ouvrir_profil(eleve_id)

    def ouvrir_historique_selectionne(self):
        eleve_id = self.obtenir_eleve_selectionne()
        if eleve_id is not None:
            self.ouvrir_profil(eleve_id)

    def ouvrir_profil(self, eleve_id):
        self.profil_page.charger(eleve_id)
        self.pages_eleves.setCurrentWidget(self.profil_page)

    def retourner_a_la_liste(self):
        self.charger_eleves()
        self.pages_eleves.setCurrentWidget(self.liste_page)

    def charger_classes(self):
        self.filtre_classe.clear()
        self.filtre_classe.addItem("Toutes les classes", None)
        for classe in self.referentiel_repo.lister_classes():
            self.filtre_classe.addItem(classe["nom"], classe["id"])

    def charger_eleves(self):
        recherche = self.recherche_input.text().strip()
        classe_id = self.filtre_classe.currentData()
        statut_filtre = self.filtre_statut.currentText()
        eleves = []
        for eleve in self.eleve_repo.lister(recherche, classe_id):
            total_du = float(eleve["total_du"])
            total_paye = float(eleve["total_paye"])
            solde = float(eleve["solde_restant"])

            if total_paye == 0:
                statut = "Non payé"
            elif solde <= 0:
                statut = "Soldé"
            else:
                statut = "Partiellement payé"

            if statut_filtre != "Tous les statuts" and statut != statut_filtre:
                continue
            eleves.append((eleve, total_du, total_paye, solde, statut))

        self.table.setRowCount(len(eleves))
        self.nombre_eleves_label.setText(
            f"{len(eleves)} élève" + ("s" if len(eleves) != 1 else "")
        )

        for ligne, (eleve, total_du, total_paye, solde, statut) in enumerate(eleves):
            valeurs = [
                f"{eleve['nom']} {eleve['prenom']}",
                eleve["classe"],
                eleve["annee_scolaire"],
                f"{total_du:,.0f} FCFA",
                f"{total_paye:,.0f} FCFA",
                f"{solde:,.0f} FCFA",
                statut,
            ]

            for colonne, valeur in enumerate(valeurs):
                item = QTableWidgetItem(valeur)
                item.setData(Qt.ItemDataRole.UserRole, eleve["id"])

                if colonne == 6:
                    couleurs = {
                        "Soldé": ("#ddf3e5", "#176437"),
                        "Partiellement payé": ("#fff1c2", "#805300"),
                        "Non payé": ("#fce0e2", "#a1232c"),
                    }
                    fond, texte = couleurs[statut]
                    item.setBackground(QColor(fond))
                    item.setForeground(QColor(texte))
                    item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
                    police = item.font()
                    police.setBold(True)
                    item.setFont(police)

                self.table.setItem(ligne, colonne, item)

        self.table.setSortingEnabled(False)

    def ajouter_eleve(self):
        dialogue = EleveDialog(
            self.referentiel_repo.lister_classes(),
            self.referentiel_repo.lister_annees(),
            parent=self,
        )

        if dialogue.exec():
            donnees = dialogue.donnees()
            self.eleve_repo.ajouter(**donnees)
            self.charger_eleves()
            QMessageBox.information(self, "Succès", "Élève ajouté avec succès.")

    def obtenir_eleve_selectionne(self):
        ligne = self.table.currentRow()

        if ligne < 0:
            QMessageBox.warning(
                self,
                "Sélection requise",
                "Sélectionnez d’abord un élève dans la liste.",
            )
            return None

        return self.table.item(ligne, 0).data(Qt.ItemDataRole.UserRole)

    def modifier_eleve(self, eleve_id=None):
        if eleve_id is None:
            eleve_id = self.obtenir_eleve_selectionne()
        if eleve_id is None:
            return

        eleve = self.eleve_repo.obtenir_par_id(eleve_id)
        dialogue = EleveDialog(
            self.referentiel_repo.lister_classes(),
            self.referentiel_repo.lister_annees(),
            eleve=eleve,
            parent=self,
        )

        if dialogue.exec():
            self.eleve_repo.modifier(eleve_id, **dialogue.donnees())
            self.charger_eleves()
            if self.profil_page.eleve_id == eleve_id:
                self.profil_page.charger(eleve_id)
            QMessageBox.information(self, "Succès", "Élève modifié avec succès.")

    def supprimer_eleve(self):
        eleve_id = self.obtenir_eleve_selectionne()
        if eleve_id is None:
            return

        reponse = QMessageBox.question(
            self,
            "Confirmer la suppression",
            "Voulez-vous vraiment supprimer cet élève et ses paiements ?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
        )

        if reponse == QMessageBox.StandardButton.Yes:
            self.eleve_repo.supprimer(eleve_id)
            self.charger_eleves()

    def enregistrer_paiement(self, eleve_id=None):
        if eleve_id is None:
            eleve_id = self.obtenir_eleve_selectionne()

        if eleve_id is None:
            return

        eleve = self.eleve_repo.obtenir_par_id(eleve_id)
        solde = self.eleve_repo.calculer_solde(eleve_id)

        if solde <= 0:
            QMessageBox.information(
                self,
                "Élève soldé",
                "Cet élève a déjà réglé la totalité de ses frais.",
            )
            return

        dialogue = PaiementDialog(eleve, solde, self)

        if dialogue.exec():
            try:
                resultat = PaiementService(self.db).enregistrer_paiement(
                    eleve_id,
                    **dialogue.donnees(),
                )

                self.charger_eleves()
                if self.profil_page.eleve_id == eleve_id:
                    self.profil_page.charger(eleve_id)

                if resultat["chemin_pdf"]:
                    message = QMessageBox(self)
                    message.setWindowTitle("Paiement enregistré")
                    message.setText(
                        "Paiement enregistré avec succès.\n"
                        f"Reçu : {resultat['numero_recu']}\n"
                        f"PDF : {resultat['chemin_pdf']}"
                    )
                    ouvrir = message.addButton(
                        "Ouvrir le reçu PDF", QMessageBox.ButtonRole.AcceptRole
                    )
                    message.addButton("Fermer", QMessageBox.ButtonRole.RejectRole)
                    message.exec()
                    if message.clickedButton() is ouvrir:
                        QDesktopServices.openUrl(
                            QUrl.fromLocalFile(str(resultat["chemin_pdf"]))
                        )
                else:
                    QMessageBox.warning(
                        self,
                        "Paiement enregistré - PDF indisponible",
                        "Le paiement est bien enregistré, mais le PDF n'a pas pu être créé.\n"
                        f"Détail : {resultat['erreur_pdf']}",
                    )

            except ValueError as erreur:
                QMessageBox.warning(self, "Paiement refusé", str(erreur))

            except Exception as erreur:
                QMessageBox.critical(
                    self,
                    "Erreur",
                    f"Une erreur est survenue : {erreur}",
                )
