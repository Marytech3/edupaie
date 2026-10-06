# MCD - EduPaie

Le schéma relationnel exécutable est `schema.sql`. Ce MCD décrit ses principales entités et clés.

```mermaid
erDiagram
    CLASSES ||--o{ ELEVES : regroupe
    ANNEES_SCOLAIRES ||--o{ ELEVES : concerne
    ELEVES ||--o{ PAIEMENTS : recoit
    RECUS ||--o| PAIEMENTS : justifie

    CLASSES {
        integer id PK
        text nom UK
    }
    ANNEES_SCOLAIRES {
        integer id PK
        text libelle UK
    }
    ELEVES {
        integer id PK
        text nom
        text prenom
        integer classe_id FK
        integer annee_scolaire_id FK
        real total_du
        text cree_le
    }
    PAIEMENTS {
        integer id PK
        integer eleve_id FK
        real montant
        text date_paiement
        text mode_paiement
        integer recu_id FK_UK
    }
    RECUS {
        integer id PK
        text numero UK
        text date_emission
        text contenu_json
    }
    PARAMETRES {
        text cle PK
        text valeur
    }
```

`UK` signifie clé unique, `PK` clé primaire et `FK` clé étrangère. Chaque élève appartient à une classe et à une année. Un élève peut avoir plusieurs paiements; chaque paiement référence un reçu unique. Le reçu archive les détails utilisés lors de l'encaissement. `PARAMETRES` est une table clé-valeur sans relation directe avec les autres tables. Le solde est calculé à partir des frais dus et de la somme des paiements.
