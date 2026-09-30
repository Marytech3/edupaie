from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QLineEdit,
    QComboBox,
    QPushButton,
    QTableWidget,
    QTableWidgetItem,
    QMessageBox,
)

from src.data1.eleve_repository import EleveRepository
from src.data1.referentiel_repository import ReferentielRepository
from src.ui.eleve_dialog import EleveDialog


class ElevesView(QWidget):
    def __init__(self, db):
        super().__init__()
        self.db = db
        self.eleve_repo = EleveRepository(db)
        self.referentiel_repo = ReferentielRepository(db)

        layout = QVBoxLayout(self)

        barre = QHBoxLayout()
        self.recherche_input = QLineEdit()
        self.recherche_input.setPlaceholderText("Rechercher par nom ou prénom...")

        self.filtre_classe = QComboBox()
        self.filtre_classe.addItem("Toutes les classes", None)

        self.btn_ajouter = QPushButton("Ajouter un élève")
        self.btn_modifier = QPushButton("Modifier")
        self.btn_supprimer = QPushButton("Supprimer")

        barre.addWidget(self.recherche_input)
        barre.addWidget(self.filtre_classe)
        barre.addWidget(self.btn_ajouter)
        barre.addWidget(self.btn_modifier)
        barre.addWidget(self.btn_supprimer)

        self.table = QTableWidget()
        self.table.setColumnCount(8)
        self.table.setHorizontalHeaderLabels([
            "Nom", "Prénom", "Classe", "Année",
            "Total dû", "Total payé", "Solde", "Statut",
        ])
        self.table.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
        self.table.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)

        layout.addLayout(barre)
        layout.addWidget(self.table)

        self.charger_classes()
        self.charger_eleves()

        self.recherche_input.textChanged.connect(self.charger_eleves)
        self.filtre_classe.currentIndexChanged.connect(self.charger_eleves)
        self.btn_ajouter.clicked.connect(self.ajouter_eleve)
        self.btn_modifier.clicked.connect(self.modifier_eleve)
        self.btn_supprimer.clicked.connect(self.supprimer_eleve)

    def charger_classes(self):
        for classe in self.referentiel_repo.lister_classes():
            self.filtre_classe.addItem(classe["nom"], classe["id"])

    def charger_eleves(self):
        recherche = self.recherche_input.text().strip()
        classe_id = self.filtre_classe.currentData()
        eleves = self.eleve_repo.lister(recherche, classe_id)

        self.table.setRowCount(len(eleves))

        for ligne, eleve in enumerate(eleves):
            total_du = float(eleve["total_du"])
            total_paye = float(eleve["total_paye"])
            solde = float(eleve["solde_restant"])

            if total_paye == 0:
                statut = "Non payé"
            elif solde <= 0:
                statut = "Soldé"
            else:
                statut = "Partiellement payé"

            valeurs = [
                eleve["nom"],
                eleve["prenom"],
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

                if colonne == 7:
                    if statut == "Soldé":
                        item.setBackground(Qt.GlobalColor.green)
                    elif statut == "Non payé":
                        item.setBackground(Qt.GlobalColor.red)
                    else:
                        item.setBackground(Qt.GlobalColor.yellow)

                self.table.setItem(ligne, colonne, item)

        self.table.resizeColumnsToContents()

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

    def modifier_eleve(self):
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