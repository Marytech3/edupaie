from pathlib import Path

from fpdf import FPDF

from src.utils.paths import RECEIPTS_DIR


class RecuService:
    """Crée un reçu PDF archivable à partir des données figées du paiement."""

    def generer_pdf(self, contenu_recu):
        RECEIPTS_DIR.mkdir(parents=True, exist_ok=True)
        numero = contenu_recu["numero"]
        chemin = RECEIPTS_DIR / f"{numero}.pdf"

        pdf = FPDF(format="A5", orientation="P")
        pdf.set_auto_page_break(auto=True, margin=15)
        pdf.add_page()
        pdf.set_title(f"Reçu {numero}")
        pdf.set_author("EduPaie")
        pdf.set_font("Helvetica", "B", 18)
        pdf.cell(0, 12, "EDUPAIE", align="C", new_x="LMARGIN", new_y="NEXT")
        pdf.set_font("Helvetica", "B", 14)
        pdf.cell(0, 10, "RECU DE PAIEMENT SCOLAIRE", align="C", new_x="LMARGIN", new_y="NEXT")
        pdf.ln(3)

        pdf.set_font("Helvetica", "B", 11)
        pdf.cell(0, 8, f"Numero : {numero}", new_x="LMARGIN", new_y="NEXT")
        pdf.set_draw_color(150, 150, 150)
        pdf.line(10, pdf.get_y(), 138, pdf.get_y())
        pdf.ln(5)

        pdf.set_font("Helvetica", "", 11)
        lignes = [
            ("Eleve", f"{contenu_recu['prenom_eleve']} {contenu_recu['nom_eleve']}"),
            ("Classe", contenu_recu["classe"]),
            ("Annee scolaire", contenu_recu["annee_scolaire"]),
            ("Date du paiement", contenu_recu["date_paiement"]),
            ("Mode de paiement", contenu_recu["mode_paiement"]),
        ]
        for libelle, valeur in lignes:
            pdf.set_font("Helvetica", "B", 10)
            pdf.cell(43, 8, f"{libelle} :")
            pdf.set_font("Helvetica", "", 10)
            pdf.multi_cell(0, 8, str(valeur), new_x="LMARGIN", new_y="NEXT")

        pdf.ln(4)
        pdf.set_font("Helvetica", "B", 12)
        pdf.cell(0, 10, f"Montant verse : {self._montant(contenu_recu['montant'])}", new_x="LMARGIN", new_y="NEXT")
        pdf.set_font("Helvetica", "", 11)
        pdf.cell(0, 9, f"Solde restant : {self._montant(contenu_recu['solde_restant'])}", new_x="LMARGIN", new_y="NEXT")
        pdf.ln(13)
        pdf.set_font("Helvetica", "I", 9)
        pdf.cell(0, 7, "Document genere par EduPaie.", align="C")
        pdf.output(str(chemin))
        return Path(chemin)

    @staticmethod
    def _montant(valeur):
        return f"{float(valeur):,.0f} FCFA".replace(",", " ")
