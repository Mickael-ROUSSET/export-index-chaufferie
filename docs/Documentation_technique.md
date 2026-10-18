# Documentation technique

Python 3.10+ et `openpyxl`. Dépendances dans `requirements.txt`.

Entrée CLI prioritaire sur `config.ini`. Sortie via `-o`, puis `config.ini`, sinon `Index_abonnes.xlsx` dans le dossier d'entrée.

Parcours non récursif des `*.txt`. Noms `NN_Nom.txt` ou `NN-Nom.txt`. Encodage UTF-8-SIG, repli CP1252. Extraction par expressions régulières, conversion en date Python et nombre Excel.

Erreurs de lecture/format dans l'onglet Erreurs. Tests : `python -m unittest discover -s tests`.
