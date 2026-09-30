from PySide6.QtWidgets import (
    QDialog,
    QFormLayout,
    QLineEdit,
    QComboBox,
    QDoubleSpinBox,
    QDialogButtonBox,
    QMessageBox,
)


class EleveDialog(QDialog):
    def __init__(self, classes, annees, eleve=None, parent=None):
        super().__init__(parent)
        self.eleve = eleve
        self.setWindowTitle("Modifier un élève" if eleve else "Ajouter un élève")

        self.nom_input = QLineEdit()
        self.prenom_input = QLineEdit()

        self.classe_combo = QComboBox()
        for classe in classes:
            self.classe_combo.addItem(classe["nom"], classe["id"])

        self.annee_combo = QComboBox()
        for annee in annees:
            self.annee_combo.addItem(annee["libelle"], annee["id"])

        self.total_du_input = QDoubleSpinBox()
        self.total_du_input.setRange(0, 100_000_000)
        self.total_du_input.setDecimals(0)
        self.total_du_input.setSuffix(" FCFA")

        formulaire = QFormLayout(self)
        formulaire.addRow("Nom * :", self.nom_input)
        formulaire.addRow("Prénom * :", self.prenom_input)
        formulaire.addRow("Classe * :", self.classe_combo)
        formulaire.addRow("Année scolaire * :", self.annee_combo)
        formulaire.addRow("Total des frais dus * :", self.total_du_input)

        boutons = QDialogButtonBox(
            QDialogButtonBox.StandardButton.Save
            | QDialogButtonBox.StandardButton.Cancel
        )
        boutons.accepted.connect(self.valider)
        boutons.rejected.connect(self.reject)
        formulaire.addRow(boutons)

        if eleve:
            self.remplir_formulaire()

    def remplir_formulaire(self):
        self.nom_input.setText(self.eleve["nom"])
        self.prenom_input.setText(self.eleve["prenom"])
        self.total_du_input.setValue(float(self.eleve["total_du"]))

        index_classe = self.classe_combo.findData(self.eleve["classe_id"])
        self.classe_combo.setCurrentIndex(index_classe)

        index_annee = self.annee_combo.findData(self.eleve["annee_scolaire_id"])
        self.annee_combo.setCurrentIndex(index_annee)

    def valider(self):
        if not self.nom_input.text().strip():
            QMessageBox.warning(self, "Champ obligatoire", "Le nom est obligatoire.")
            return

        if not self.prenom_input.text().strip():
            QMessageBox.warning(self, "Champ obligatoire", "Le prénom est obligatoire.")
            return

        if self.total_du_input.value() <= 0:
            QMessageBox.warning(
                self,
                "Montant invalide",
                "Le total des frais doit être supérieur à zéro.",
            )
            return

        self.accept()

    def donnees(self):
        return {
            "nom": self.nom_input.text().strip().upper(),
            "prenom": self.prenom_input.text().strip().title(),
            "classe_id": self.classe_combo.currentData(),
            "annee_scolaire_id": self.annee_combo.currentData(),
            "total_du": self.total_du_input.value(),
        }