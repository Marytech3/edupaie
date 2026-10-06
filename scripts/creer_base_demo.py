"""Crée une base de démonstration distincte des données de travail."""

import json
import sqlite3
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DESTINATION = ROOT / "data" / "edupaie_demo.db"
SCHEMA = ROOT / "database" / "schema.sql"


def main():
    if DESTINATION.exists():
        raise SystemExit(f"La base existe déjà et n'a pas été remplacée : {DESTINATION}")
    DESTINATION.parent.mkdir(parents=True, exist_ok=True)
    connexion = sqlite3.connect(DESTINATION)
    connexion.execute("PRAGMA foreign_keys = ON")
    connexion.executescript(SCHEMA.read_text(encoding="utf-8"))

    classes = ["6e A", "6e B", "5e A", "5e B", "4e A", "3e A"]
    for classe in classes:
        connexion.execute("INSERT OR IGNORE INTO classes(nom) VALUES (?)", (classe,))
    connexion.execute(
        "INSERT OR IGNORE INTO annees_scolaires(libelle) VALUES ('2026-2027')"
    )
    classe_ids = {
        nom: identifiant
        for identifiant, nom in connexion.execute("SELECT id, nom FROM classes")
    }
    annee_id = connexion.execute(
        "SELECT id FROM annees_scolaires WHERE libelle = '2026-2027'"
    ).fetchone()[0]

    prenoms = [
        "Afi", "Koffi", "Ama", "Yao", "Mawuli", "Akou", "Kodjo", "Esi",
        "Komlan", "Abla", "Sena", "Kossi", "Dela", "Adjovi", "Togbe",
    ]
    noms = [
        "Mensah", "Agbeko", "Amouzou", "Tchalla", "Amegan", "Dossou",
        "Kouassi", "Assogba", "Lawson", "Akpene", "Aklassou", "Kpatcha",
        "Gaba", "Amegah", "Bawa",
    ]
    modes = ["Espèces", "Chèque", "Virement", "Mobile Money"]
    for index, (prenom, nom) in enumerate(zip(prenoms, noms), start=1):
        classe = classes[(index - 1) % len(classes)]
        eleve_id = connexion.execute(
            """INSERT INTO eleves(nom, prenom, classe_id, annee_scolaire_id, total_du)
               VALUES (?, ?, ?, ?, 100000)""",
            (nom, prenom, classe_ids[classe], annee_id),
        ).lastrowid

        # 1-5 : non payés; 6-10 : partiels; 11-15 : soldés.
        montants = []
        if 6 <= index <= 10:
            montants = [20000, 15000] if index % 2 == 0 else [40000]
        elif index >= 11:
            montants = [60000, 40000] if index % 2 == 0 else [100000]

        for rang, montant in enumerate(montants, start=1):
            verse = sum(montants[:rang])
            contenu = {
                "numero": f"DEMO-{index:02d}-{rang:02d}",
                "nom_eleve": nom,
                "prenom_eleve": prenom,
                "classe": classe,
                "annee_scolaire": "2026-2027",
                "montant": montant,
                "date_paiement": f"2026-09-{min(index + rang, 28):02d}",
                "mode_paiement": modes[(index + rang) % len(modes)],
                "solde_restant": 100000 - verse,
            }
            recu_id = connexion.execute(
                "INSERT INTO recus(numero, contenu_json) VALUES (?, ?)",
                (contenu["numero"], json.dumps(contenu, ensure_ascii=False)),
            ).lastrowid
            connexion.execute(
                """INSERT INTO paiements
                   (eleve_id, montant, date_paiement, mode_paiement, recu_id)
                   VALUES (?, ?, ?, ?, ?)""",
                (eleve_id, montant, contenu["date_paiement"],
                 contenu["mode_paiement"], recu_id),
            )

    connexion.commit()
    connexion.close()
    print(f"Base de démonstration créée : {DESTINATION}")


if __name__ == "__main__":
    main()
