# Trame de soutenance EduPaie (12 minutes)

## Déroulé proposé

| Durée | Partie | À montrer / expliquer |
| --- | --- | --- |
| 0:00-1:00 | Besoin | Difficulté de suivre les paiements et soldes de chaque élève sur papier ou dans plusieurs fichiers. |
| 1:00-2:00 | Objectifs et périmètre | Fiches élèves, encaissements partiels, statut, historique, reçus PDF et tableau de bord. |
| 2:00-3:30 | Architecture | Montrer `src/ui`, `src/services`, `src/data1`, puis expliquer SQLite et le stockage local. |
| 3:30-5:00 | Modèle de données | Présenter les tables `eleves`, `paiements`, `recus`, `classes` et `annees_scolaires`; expliquer les clés étrangères et le solde calculé. |
| 5:00-9:30 | Démonstration | Avec les données fictives : filtrer la liste, ouvrir la fiche d'un élève, voir son historique, enregistrer un paiement partiel, ouvrir le reçu, puis montrer le tableau de bord actualisé. |
| 9:30-10:30 | Sécurité et distribution | Montrer les sauvegardes, l'emplacement des données locales et le paquet autonome Windows. Distinguer l'exécutable de la base de données. |
| 10:30-12:00 | Limites et conclusion | Usage mono-poste, absence de comptes utilisateurs et de synchronisation; résumer la valeur et les améliorations futures. |

Ce déroulé laisse environ deux minutes pour les questions. Pour tenir en 10 minutes, réduire le contexte et la démonstration; pour 15 minutes, détailler la validation des paiements, la transaction SQLite et les limites.

## Démonstration pas à pas

1. Lancer EduPaie avec `data/edupaie_demo.db` déjà copiée dans le profil de test.
2. Montrer les statuts des trois groupes d'élèves dans la liste.
3. Rechercher un élève partiellement payé et ouvrir sa fiche par double-clic.
4. Parcourir l'historique et ouvrir un reçu existant.
5. Enregistrer sur un élève fictif un paiement inférieur au solde restant; expliquer qu'un versement partiel conserve un solde.
6. Ouvrir le PDF et le tableau de bord pour relier l'action aux données.

## Questions probables et réponses courtes

**Pourquoi SQLite ?** La cible est un poste local et une petite structure. SQLite évite l'installation et l'administration d'un serveur. Le choix devrait être réévalué si plusieurs postes doivent écrire simultanément dans les mêmes données.

**Pourquoi séparer UI, services et dépôts ?** La séparation isole les règles financières de l'affichage et des requêtes; elle rend les responsabilités plus faciles à comprendre et à faire évoluer.

**Comment le solde est-il calculé ?** À la lecture : frais dus moins somme des paiements de l'élève. Le solde n'est pas dupliqué dans une colonne persistante.

**Comment un paiement est-il associé à un reçu ?** Une transaction crée un enregistrement de reçu et un enregistrement de paiement liés par une clé étrangère unique; le PDF est produit à partir des données figées du reçu.

**Quelles validations sont faites ?** Un paiement doit être positif, utiliser un mode autorisé et ne pas dépasser le solde restant. La base définit aussi des contraintes de montant et de relations.

**Que se passe-t-il si le PDF échoue ?** L'opération financière reste enregistrée; l'interface peut signaler que le fichier n'a pas été créé. Il faut résoudre le problème de stockage avant de remettre le reçu.

**Les données sont-elles synchronisées entre deux ordinateurs ?** Non. Chaque profil Windows dispose de sa propre base locale. Le transfert passe par une sauvegarde/restauration; OneDrive ne doit pas synchroniser une base ouverte.

**Quelles sont les principales évolutions ?** Authentification et rôles, journal d'audit, frais par classe, import/export tabulaire et sauvegardes automatiques testées.

## Conseils de préparation

- Faire la démonstration à partir d'une copie de la base de test, jamais de données réelles.
- Vérifier avant l'oral que les reçus PDF d'exemple s'ouvrent et que le dossier du paquet autonome est complet.
- Garder `database/schema.sql`, le diagramme MCD et les captures accessibles pour les questions.
- Ne pas annoncer la synchronisation multi-poste, la sécurité par compte ou l'automatisation des sauvegardes comme des fonctions existantes.
