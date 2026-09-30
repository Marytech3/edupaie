class ReferentielRepository:
    def __init__(self, db):
        self.db = db

    def initialiser(self):
        classes = ["6e A", "6e B", "5e A", "5e B", "4e A", "3e A"]
        annees = ["2025-2026", "2026-2027"]

        for nom in classes:
            self.db.execute(
                "INSERT OR IGNORE INTO classes(nom) VALUES (?)",
                (nom,),
            )

        for libelle in annees:
            self.db.execute(
                "INSERT OR IGNORE INTO annees_scolaires(libelle) VALUES (?)",
                (libelle,),
            )

    def lister_classes(self):
        return self.db.fetch_all("SELECT * FROM classes ORDER BY nom")

    def lister_annees(self):
        return self.db.fetch_all(
            "SELECT * FROM annees_scolaires ORDER BY libelle DESC"
        )