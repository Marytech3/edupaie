import json
from datetime import datetime

from src.data1.eleve_repository import EleveRepository
from src.data1.paiement_repository import PaiementRepository
from src.services.recu_service import RecuService


class PaiementService:
    MODES_AUTORISES = (
        "Espèces",
        "Chèque",
        "Virement",
        "Mobile Money",
    )

    def __init__(self, db):
        self.db = db
        self.eleve_repo = EleveRepository(db)
        self.paiement_repo = PaiementRepository(db)

    def generer_numero_recu(self):
        annee = datetime.now().year

        ligne = self.db.fetch_one(
            "SELECT COUNT(*) AS total FROM recus"
        )

        prochain_numero = ligne["total"] + 1
        return f"REC-{annee}-{prochain_numero:05d}"

    def enregistrer_paiement(self, eleve_id, montant, date_paiement, mode_paiement):
        montant = float(montant)

        if montant <= 0:
            raise ValueError("Le montant doit être supérieur à zéro.")

        if mode_paiement not in self.MODES_AUTORISES:
            raise ValueError("Le mode de paiement est invalide.")

        eleve = self.eleve_repo.obtenir_par_id(eleve_id)
        if eleve is None:
            raise ValueError("Élève introuvable.")

        solde_avant = float(self.eleve_repo.calculer_solde(eleve_id))

        if montant > solde_avant:
            raise ValueError(
                f"Le montant dépasse le solde restant de {solde_avant:,.0f} FCFA."
            )

        numero_recu = self.generer_numero_recu()
        solde_apres = solde_avant - montant

        contenu_recu = {
            "numero": numero_recu,
            "nom_eleve": eleve["nom"],
            "prenom_eleve": eleve["prenom"],
            "classe": eleve["classe"],
            "annee_scolaire": eleve["annee_scolaire"],
            "montant": montant,
            "date_paiement": date_paiement,
            "mode_paiement": mode_paiement,
            "solde_restant": solde_apres,
        }

        try:
            self.db.connection.execute("BEGIN")

            cursor_recu = self.db.connection.execute(
                """
                INSERT INTO recus(numero, contenu_json)
                VALUES (?, ?)
                """,
                (numero_recu, json.dumps(contenu_recu, ensure_ascii=False)),
            )

            recu_id = cursor_recu.lastrowid

            cursor_paiement = self.db.connection.execute(
                """
                INSERT INTO paiements
                    (eleve_id, montant, date_paiement, mode_paiement, recu_id)
                VALUES (?, ?, ?, ?, ?)
                """,
                (eleve_id, montant, date_paiement, mode_paiement, recu_id),
            )

            self.db.connection.commit()

        except Exception:
            self.db.connection.rollback()
            raise

        resultat = {
            "paiement_id": cursor_paiement.lastrowid,
            "recu_id": recu_id,
            "numero_recu": numero_recu,
            "contenu_recu": contenu_recu,
        }
        try:
            resultat["chemin_pdf"] = RecuService().generer_pdf(contenu_recu)
            resultat["erreur_pdf"] = None
        except Exception as erreur_pdf:
            # Le paiement et son reçu en base restent enregistrés même si
            # l'export PDF échoue; l'interface peut alors expliquer la suite.
            resultat["chemin_pdf"] = None
            resultat["erreur_pdf"] = str(erreur_pdf)
        return resultat
