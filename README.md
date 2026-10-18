# Export des index abonnés — Chaufferie

Outil Windows/Python regroupant les fichiers `NN_Nom.txt` en un classeur Excel.

## Installation
1. Installer Python 3.10+ avec le lanceur `py`.
2. Télécharger le dépôt (Code > Download ZIP), puis le décompresser.
3. Exécuter `Installer.cmd`.
4. Adapter le chemin `repertoire` dans `config.ini`.
5. Exécuter `Exporter.cmd`.

## Exemple
`09_Ecole.txt` contenant `vendredi 16 octobre 2026 00:00:00<TAB>1234510,0000` produit une ligne avec numéro 09, abonné Ecole, date 16/10/2026, index 1234510,0000.

## Options
`Exporter.cmd "C:\Autre\Primaire"` surcharge le répertoire ; `-o "C:\Exports\index.xlsx"` choisit le fichier de sortie.

Le script lit la dernière ligne non vide de chaque TXT (non récursif), accepte UTF-8 et CP1252 et écrit les anomalies dans un onglet Erreurs. Vérifier les données avant facturation : aucun calcul de consommation ni contrôle métier.

Documentation détaillée dans `docs/`.
