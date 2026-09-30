class EleveRepository:
    def __init__(self, db):
        self.db = db

    def lister(self, recherche="", classe_id=None):
        query = """
            SELECT
                e.id,
                e.nom,
                e.prenom,
                c.nom AS classe,
                a.libelle AS annee_scolaire,
                e.total_du,
                COALESCE(SUM(p.montant), 0) AS total_paye,
                e.total_du - COALESCE(SUM(p.montant), 0) AS solde_restant
            FROM eleves e
            JOIN classes c ON c.id = e.classe_id
            JOIN annees_scolaires a ON a.id = e.annee_scolaire_id
            LEFT JOIN paiements p ON p.eleve_id = e.id
            WHERE (e.nom LIKE ? OR e.prenom LIKE ?)
        """

        params = [f"%{recherche}%", f"%{recherche}%"]

        if classe_id:
            query += " AND e.classe_id = ?"
            params.append(classe_id)

        query += """
            GROUP BY e.id
            ORDER BY e.nom, e.prenom
        """

        return self.db.fetch_all(query, params)

    def obtenir_par_id(self, eleve_id):
        return self.db.fetch_one(
            """
            SELECT
                e.*,
                c.nom AS classe,
                a.libelle AS annee_scolaire
            FROM eleves e
            JOIN classes c ON c.id = e.classe_id
            JOIN annees_scolaires a ON a.id = e.annee_scolaire_id
            WHERE e.id = ?
            """,
            (eleve_id,),
        )

    def ajouter(self, nom, prenom, classe_id, annee_scolaire_id, total_du):
        cursor = self.db.execute(
            """
            INSERT INTO eleves
            (nom, prenom, classe_id, annee_scolaire_id, total_du)
            VALUES (?, ?, ?, ?, ?)
            """,
            (nom, prenom, classe_id, annee_scolaire_id, total_du),
        )
        return cursor.lastrowid

    def modifier(self, eleve_id, nom, prenom, classe_id, annee_scolaire_id, total_du):
        self.db.execute(
            """
            UPDATE eleves
            SET nom = ?, prenom = ?, classe_id = ?,
                annee_scolaire_id = ?, total_du = ?
            WHERE id = ?
            """,
            (nom, prenom, classe_id, annee_scolaire_id, total_du, eleve_id),
        )

    def supprimer(self, eleve_id):
        self.db.execute("DELETE FROM eleves WHERE id = ?", (eleve_id,))

    def calculer_solde(self, eleve_id):
        ligne = self.db.fetch_one(
            """
            SELECT
                e.total_du - COALESCE(SUM(p.montant), 0) AS solde
            FROM eleves e
            LEFT JOIN paiements p ON p.eleve_id = e.id
            WHERE e.id = ?
            GROUP BY e.id
            """,
            (eleve_id,),
        )
        return ligne["solde"] if ligne else 0