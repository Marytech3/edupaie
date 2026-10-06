from PySide6.QtCore import QDate
from PySide6.QtWidgets import (
    QDialog,
    QFormLayout,
    QLabel,
    QDoubleSpinBox,
    QDateEdit,
    QComboBox,
    QDialogButtonBox,
    QMessageBox,
)


class PaiementDialog(QDialog):
    def __init__(self, eleve, solde_restant, parent=None):
        super().__init__(parent)

        self.eleve = eleve
        self.solde_restant = float(solde_restant)

        self.setWindowTitle("Enregistrer un paiement")
        self.setMinimumWidth(420)

        layout = QFormLayout(self)

        layout.addRow(
            "Élève :",
            QLabel(f"{eleve['prenom']} {eleve['nom']} — {eleve['classe']}"),
        )
        layout.addRow("Total dû :", QLabel(f"{float(eleve['total_du']):,.0f} FCFA"))
        layout.addRow("Solde restant :", QLabel(f"{self.solde_restant:,.0f} FCFA"))

        self.montant_input = QDoubleSpinBox()
        self.montant_input.setRange(0, self.solde_restant)
        self.montant_input.setDecimals(0)
        self.montant_input.setSuffix(" FCFA")

        self.date_input = QDateEdit(QDate.currentDate())
        self.date_input.setCalendarPopup(True)

        self.mode_input = QComboBox()
        self.mode_input.addItems([
            "Espèces",
            "Chèque",
            "Virement",
            "Mobile Money",
        ])

        layout.addRow("Montant * :", self.montant_input)
        layout.addRow("Date * :", self.date_input)
        layout.addRow("Mode de paiement * :", self.mode_input)

        boutons = QDialogButtonBox(
            QDialogButtonBox.StandardButton.Save
            | QDialogButtonBox.StandardButton.Cancel
        )
        boutons.accepted.connect(self.valider)
        boutons.rejected.connect(self.reject)

        layout.addRow(boutons)

    def valider(self):
        montant = self.montant_input.value()

        if montant <= 0:
            QMessageBox.warning(
                self,
                "Montant invalide",
                "Le montant doit être supérieur à zéro.",
            )
            return

        if montant > self.solde_restant:
            QMessageBox.warning(
                self,
                "Montant refusé",
                "Le montant ne peut pas dépasser le solde restant.",
            )
            return

        self.accept()

    def donnees(self):
        return {
            "montant": self.montant_input.value(),
            "date_paiement": self.date_input.date().toString("yyyy-MM-dd"),
            "mode_paiement": self.mode_input.currentText(),
        }