# Guide d'installation - Windows sans Python

## Pour la personne qui reçoit EduPaie

1. Copiez `EduPaie_Test_Sans_Python_2026-10-06.zip` depuis la clé USB vers **Téléchargements**.
2. Faites un clic droit sur le ZIP, choisissez **Extraire tout**, puis cliquez sur **Extraire**. N'exécutez pas le programme depuis l'aperçu du ZIP.
3. Ouvrez le dossier `EduPaie_Test_Portable` qui vient d'être extrait.
4. Double-cliquez sur `EduPaie.exe`. Ne déplacez pas ce fichier seul : les DLL Qt, le dossier `PySide6`, `database\schema.sql` et `data\edupaie_demo.db` sont requis à côté.
5. Au premier lancement, EduPaie crée sa base active dans `%LOCALAPPDATA%\EduPaie\data\edupaie.db` et ses reçus dans `%LOCALAPPDATA%\EduPaie\receipts\`.

Si Windows demande une confirmation, vérifiez que le ZIP provient bien de la personne responsable du projet et que le nom du dossier est `EduPaie_Test_Portable`. Ne lancez pas l'application depuis un dossier OneDrive dont le statut affiche encore **Synchronisation en attente**; utilisez le dossier extrait dans Téléchargements ou sur le Bureau.

## Créer un raccourci

Dans le dossier extrait, faites un clic droit sur `EduPaie.exe`, choisissez **Afficher plus d'options → Envoyer vers → Bureau (créer un raccourci)**. Le raccourci doit viser l'exécutable qui reste dans le dossier complet extrait.

## Données de test et données réelles

Cette archive contient la base de démonstration. Sur le second PC, EduPaie initialise une base de travail distincte dans le profil Windows de cet ordinateur. Les élèves/paiements réels du premier ordinateur ne sont pas inclus dans cette archive d'essai. Pour transférer des données réelles, utilisez l'archive créée par **Paramètres → Créer une sauvegarde**, puis restaurez-la sur le second poste une fois que la fonction est disponible dans la version distribuée.

## Important

La version de test a été empaquetée avec Nuitka (mode standalone), un équivalent autorisé de PyInstaller. Elle n'exige pas Python sur le PC de destination. Copiez/extrayez tout le paquet, pas le seul `EduPaie.exe`. La fonction de sauvegarde/restauration en cours de correction dans les sources n'est pas intégrée à cette ancienne archive de test.
