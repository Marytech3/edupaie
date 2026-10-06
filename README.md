# EduPaie

EduPaie est une application de bureau pour suivre les élèves, les frais scolaires, les paiements et les reçus d'un établissement. L'interface est réalisée avec PySide6 et les données sont conservées dans une base SQLite locale.

## Fonctionnalités

- Ajouter, modifier, rechercher et filtrer les élèves par classe et statut de paiement.
- Enregistrer un paiement en FCFA avec date et mode de paiement.
- Refuser les montants nuls ou supérieurs au solde restant.
- Générer un reçu PDF et consulter l'historique d'un élève.
- Voir les encaissements et soldes dans le tableau de bord.
- Créer une archive de sauvegarde contenant la base SQLite et les reçus PDF, puis restaurer cette archive.

## Installation et lancement depuis les sources (Windows)

Prérequis : Windows 10 ou 11 et Python 3.11 ou supérieur. Depuis PowerShell, dans le dossier du projet :

```powershell
py -3 -m venv .venv
.\.venv\Scripts\python.exe -m pip install --upgrade pip
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
.\.venv\Scripts\python.exe main.py
```

Pour construire l'exécutable, ajoutez les dépendances de build :

```powershell
.\.venv\Scripts\python.exe -m pip install -r requirements-build.txt
```

Le fichier `Lancer EduPaie.vbs` lance aussi l'application sans laisser de fenêtre de terminal ouverte, si l'environnement `.venv` a été installé.

## Jeu de données de démonstration

`data/edupaie_demo.db` est une base de démonstration distincte des données de travail. Elle contient 15 élèves : cinq non payés, cinq partiellement payés et cinq soldés, avec des dates et modes de paiement variés. Elle est copiée dans le profil utilisateur au premier démarrage. Le script `scripts/creer_base_demo.py` documente sa création; il s'arrête si le fichier existe déjà pour éviter de l'écraser.

## Construire l'application Windows

La méthode PyInstaller produit un dossier autonome (Python n'a pas besoin d'être installé sur le PC de destination) :

```powershell
.\scripts\build_windows.ps1
```

Le résultat est `dist/EduPaie/`. Distribuez **tout ce dossier**, par exemple en le compressant en ZIP. Ne copiez pas le fichier `.exe` seul. Un script Nuitka alternatif est conservé dans `scripts/build_nuitka_windows.ps1`; PyInstaller est la méthode de build documentée et recommandée.

Un paquet autonome de test est disponible : [EduPaie_Test_Sans_Python_2026-10-06.zip](deployment/EduPaie_Test_Sans_Python_2026-10-06.zip). Il est construit avec Nuitka standalone et comprend son guide d'installation ci-dessous.

L'archive de test actuellement fournie dans `deployment/` est antérieure aux dernières modifications des fonctions de sauvegarde/restauration. Pour ces fonctions, lancez les sources avec `Lancer EduPaie.vbs` ou reconstruisez le dossier PyInstaller après installation de `requirements-build.txt`.

Guide détaillé : [Installation sur un PC Windows](docs/GUIDE_INSTALLATION_WINDOWS.md).

## Où sont stockées les données ?

La base de travail et les reçus ne sont pas stockés dans le dossier de l'exécutable :

- Base : `%LOCALAPPDATA%\EduPaie\data\edupaie.db`
- Reçus PDF : `%LOCALAPPDATA%\EduPaie\receipts\`

Pour transférer EduPaie sur un autre PC, copiez le dossier autonome complet. Les données de test se recréent depuis la base de démonstration. Pour transférer des données réelles, utilisez la fonction de sauvegarde/restauration depuis Paramètres.

## Architecture et données

- `src/ui/` : fenêtre principale, vues, formulaires et thème.
- `src/services/` : règles de paiement, indicateurs et génération des reçus.
- `src/data1/` : accès à SQLite et dépôts de données.
- `database/schema.sql` : définition des tables et contraintes.
- `data/edupaie_demo.db` : jeu de démonstration.

Le modèle des données est expliqué dans [docs/architecture.md](docs/architecture.md) et [database/MCD.md](database/MCD.md). La documentation courte à remettre est [Documentation_technique.pdf](output/pdf/Documentation_technique.pdf); le manuel d'une page est [Manuel_utilisateur.pdf](output/pdf/Manuel_utilisateur.pdf).

## Documentation du projet

- [Manuel utilisateur](MANUEL_UTILISATEUR.md)
- [Guide de soutenance de 10 à 15 minutes](docs/soutenance.md)
- [Archive du code source](EduPaie_source_complet.zip) (générée pour la remise; elle exclut les données de travail `data/edupaie.db`)

## Limites connues

- L'application est mono-poste et ne synchronise pas les données entre plusieurs ordinateurs.
- Il n'y a pas de comptes utilisateurs ni de journal d'audit.
- Les montants sont saisis par élève; les frais par classe ne sont pas calculés automatiquement.
- Les sauvegardes sont manuelles; conservez une copie séparée, par exemple sur une clé USB.
- Les élèves inclus dans la base de démonstration sont fictifs.

## Dépôt

Le dépôt configuré localement est `Marytech3/edupaie`. L'archive source contient l'état de travail décrit dans ce README; les modifications locales ne sont pas publiées sur le dépôt distant par ce paquet de remise.
