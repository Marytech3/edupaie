class PaiementRepository:
    def __init__(self, db):
        self.db = db

    def creer(self, eleve_id, montant, date_paiement, mode_paiement, recu_id):
        cursor = self.db.execute(
            """
            INSERT INTO paiements
                (eleve_id, montant, date_paiement, mode_paiement, recu_id)
            VALUES (?, ?, ?, ?, ?)
            """,
            (eleve_id, montant, date_paiement, mode_paiement, recu_id),
        )
        return cursor.lastrowid

    def lister_par_eleve(self, eleve_id):
        return self.db.fetch_all(
            """
            SELECT
                p.id,
                p.montant,
                p.date_paiement,
                p.mode_paiement,
                r.numero AS numero_recu,
                r.contenu_json
            FROM paiements p
            JOIN recus r ON r.id = p.recu_id
            WHERE p.eleve_id = ?
            ORDER BY p.date_paiement ASC, p.id ASC
            """,
            (eleve_id,),
        )
