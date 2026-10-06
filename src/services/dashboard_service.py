class DashboardService:
    """Fournit les indicateurs et la liste des élèves pour le tableau de bord."""

    def __init__(self, db):
        self.db = db

    def indicateurs(self):
        ligne = self.db.fetch_one(
            """
            SELECT
                COUNT(DISTINCT e.id) AS nombre_eleves,
                COALESCE((SELECT SUM(montant) FROM paiements), 0) AS total_encaisse,
                COALESCE(SUM(e.total_du - COALESCE(p.total_paye, 0)), 0)
                    AS total_restant,
                COALESCE(SUM(CASE
                    WHEN COALESCE(p.total_paye, 0) < e.total_du THEN 1 ELSE 0
                END), 0) AS nombre_non_soldes
            FROM eleves e
            LEFT JOIN (
                SELECT eleve_id, SUM(montant) AS total_paye
                FROM paiements GROUP BY eleve_id
            ) p ON p.eleve_id = e.id
            """
        )
        return dict(ligne)

    def lister_eleves(self, statut="Tous les statuts"):
        requete = """
            SELECT e.id, e.nom, e.prenom, c.nom AS classe,
                   a.libelle AS annee_scolaire, e.total_du,
                   COALESCE(p.total_paye, 0) AS total_paye,
                   e.total_du - COALESCE(p.total_paye, 0) AS solde,
                   CASE
                     WHEN COALESCE(p.total_paye, 0) = 0 THEN 'Non payé'
                     WHEN e.total_du - COALESCE(p.total_paye, 0) <= 0 THEN 'Soldé'
                     ELSE 'Partiellement payé'
                   END AS statut
            FROM eleves e
            JOIN classes c ON c.id = e.classe_id
            JOIN annees_scolaires a ON a.id = e.annee_scolaire_id
            LEFT JOIN (
                SELECT eleve_id, SUM(montant) AS total_paye
                FROM paiements GROUP BY eleve_id
            ) p ON p.eleve_id = e.id
        """
        params = ()
        if statut != "Tous les statuts":
            requete += " WHERE CASE WHEN COALESCE(p.total_paye, 0) = 0 THEN 'Non payé' WHEN e.total_du - COALESCE(p.total_paye, 0) <= 0 THEN 'Soldé' ELSE 'Partiellement payé' END = ?"
            params = (statut,)
        requete += " ORDER BY CASE statut WHEN 'Non payé' THEN 1 WHEN 'Partiellement payé' THEN 2 ELSE 3 END, e.nom, e.prenom"
        return self.db.fetch_all(requete, params)
