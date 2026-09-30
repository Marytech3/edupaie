PRAGMA foreign_keys = ON;

CREATE TABLE IF NOT EXISTS classes (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nom TEXT NOT NULL UNIQUE
);

CREATE TABLE IF NOT EXISTS annees_scolaires (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    libelle TEXT NOT NULL UNIQUE
);

CREATE TABLE IF NOT EXISTS eleves (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nom TEXT NOT NULL,
    prenom TEXT NOT NULL,
    classe_id INTEGER NOT NULL,
    annee_scolaire_id INTEGER NOT NULL,
    total_du REAL NOT NULL CHECK (total_du >= 0),
    cree_le TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,

    FOREIGN KEY (classe_id) REFERENCES classes(id),
    FOREIGN KEY (annee_scolaire_id) REFERENCES annees_scolaires(id)
);

CREATE TABLE IF NOT EXISTS recus (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    numero TEXT NOT NULL UNIQUE,
    date_emission TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
    contenu_json TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS paiements (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    eleve_id INTEGER NOT NULL,
    montant REAL NOT NULL CHECK (montant > 0),
    date_paiement TEXT NOT NULL,
    mode_paiement TEXT NOT NULL
        CHECK (mode_paiement IN ('Espèces', 'Chèque', 'Virement', 'Mobile Money')),
    recu_id INTEGER NOT NULL UNIQUE,

    FOREIGN KEY (eleve_id) REFERENCES eleves(id) ON DELETE CASCADE,
    FOREIGN KEY (recu_id) REFERENCES recus(id)
);

CREATE TABLE IF NOT EXISTS parametres (
    cle TEXT PRIMARY KEY,
    valeur TEXT NOT NULL
);