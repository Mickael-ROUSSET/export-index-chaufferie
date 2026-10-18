#!/usr/bin/env python3
"""Rassemble les index d'abonnés contenus dans des fichiers NN_Nom.txt."""
import argparse
import configparser
import re
import sys
from datetime import datetime
from pathlib import Path
from openpyxl import Workbook
from openpyxl.styles import Font, PatternFill

MOIS = {'janvier': 1, 'février': 2, 'fevrier': 2, 'mars': 3, 'avril': 4,
        'mai': 5, 'juin': 6, 'juillet': 7, 'août': 8, 'aout': 8,
        'septembre': 9, 'octobre': 10, 'novembre': 11, 'décembre': 12, 'decembre': 12}
DATE = re.compile(r'(?:lundi|mardi|mercredi|jeudi|vendredi|samedi|dimanche)?\s*(\d{1,2})\s+([a-zA-Zéûèêôîùà]+)\s+(\d{4})\s+(\d{2}):(\d{2}):(\d{2})', re.I)
VALEUR = re.compile(r'^[+-]?[\d\s\u00a0]+(?:[,.]\d+)?$')

def extraire(ligne):
    # La date occupe le début de ligne ; le séparateur peut être une
    # tabulation, plusieurs espaces, un point-virgule ou une virgule.
    ligne = ligne.strip().lstrip("\ufeff")
    match = DATE.match(ligne)
    if not match:
        raise ValueError("date française non reconnue : " + repr(ligne[:100]))
    j, mois, an, h, mi, s = match.groups()
    mois_num = MOIS.get(mois.lower())
    if mois_num is None:
        raise ValueError("mois non reconnu : " + mois)
    date = datetime(int(an), mois_num, int(j), int(h), int(mi), int(s))
    reste = ligne[match.end():]
    # Séparateurs permis : tabulation, espaces, point-virgule.
    # Une virgule peut aussi séparer les champs, mais reste utilisée
    # comme séparateur décimal dans la valeur.
    reste = reste.lstrip(" \t;")
    if reste.startswith(","):
        reste = reste[1:].lstrip()
    brut = reste.strip().replace("\u00a0", "").replace("\u202f", "").replace(" ", "")
    if not re.fullmatch(r"[+-]?\d+(?:[,.]\d+)?", brut):
        raise ValueError("index non numérique ou séparateur non reconnu : " + repr(reste[:100]))
    return date, float(brut.replace(",", "."))

def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('repertoire', nargs='?', help='Répertoire des fichiers TXT')
    p.add_argument('-o', '--sortie', help='Chemin du classeur Excel')
    args = p.parse_args()
    config = configparser.ConfigParser()
    config.read(Path(__file__).resolve().parent / 'config.ini', encoding='utf-8')
    repertoire = args.repertoire or config.get('export', 'repertoire', fallback='').strip()
    if not repertoire:
        p.error('Précisez un répertoire ou configurez config.ini')
    dossier = Path(repertoire)
    if not dossier.is_dir():
        p.error('Répertoire introuvable : ' + str(dossier))
    sortie_config = config.get('export', 'sortie', fallback='').strip()
    sortie = Path(args.sortie or sortie_config) if (args.sortie or sortie_config) else dossier / 'Index_abonnes.xlsx'
    wb = Workbook()
    ws = wb.active
    ws.title = 'Index abonnés'
    ws.append(['N°', 'Abonné', 'Date du relevé', 'Index', 'Fichier source'])
    erreurs = []
    for fichier in sorted(dossier.glob('*.txt'), key=lambda f: f.name.lower()):
        nom = re.fullmatch(r'((?:\d+|[Ee]\d+))[_\-](.+)', fichier.stem)
        # Le préfixe numérique est facultatif : accepter aussi Nom.txt.
        numero = nom.group(1) if nom else ''
        abonne = nom.group(2).replace('_', ' ') if nom else fichier.stem.replace('_', ' ')
        try:
            donnees = fichier.read_bytes()
            if donnees.startswith((b'\xff\xfe', b'\xfe\xff')):
                contenu = donnees.decode('utf-16')
            elif donnees.startswith(b'\xef\xbb\xbf'):
                contenu = donnees.decode('utf-8-sig')
            else:
                try:
                    contenu = donnees.decode('utf-8')
                except UnicodeDecodeError:
                    contenu = donnees.decode('cp1252')
            lignes = [l for l in contenu.splitlines() if l.strip()]
            if not lignes:
                raise ValueError('fichier vide')
            # Ignorer les en-têtes Trend et les lignes parasites.
            # Retenir le dernier relevé valide, sans confondre avec l'identifiant du point.
            releves = []
            for ligne_texte in lignes:
                if DATE.match(ligne_texte.strip().lstrip("\ufeff")):
                    releves.append(extraire(ligne_texte))
            if not releves:
                raise ValueError("aucune ligne de relevé datée reconnue")
            date, index = releves[-1]
            ws.append([numero, abonne, date, index, fichier.name])
        except (ValueError, OSError) as exc:
            erreurs.append((fichier.name, str(exc)))
    for ligne in ws.iter_rows(min_row=2):
        ligne[2].number_format = 'DD/MM/YYYY HH:MM:SS'
        ligne[3].number_format = '#,##0.0000'
    ws.freeze_panes = 'A2'
    ws.auto_filter.ref = ws.dimensions
    for cellule in ws[1]:
        cellule.fill = PatternFill('solid', fgColor='17365D')
        cellule.font = Font(color='FFFFFF', bold=True)
    for col, largeur in {'A': 10, 'B': 30, 'C': 24, 'D': 22, 'E': 35}.items():
        ws.column_dimensions[col].width = largeur
    if erreurs:
        we = wb.create_sheet('Erreurs')
        we.append(['Fichier', 'Erreur'])
        for erreur in erreurs:
            we.append(erreur)
        we.column_dimensions['A'].width = 40
        we.column_dimensions['B'].width = 65
        for c in we[1]:
            c.font = Font(bold=True, color='FFFFFF')
            c.fill = PatternFill('solid', fgColor='9C3030')
    sortie.parent.mkdir(parents=True, exist_ok=True)
    wb.save(sortie)
    print(f'{ws.max_row - 1} abonnés exportés ; {len(erreurs)} fichier(s) en erreur.')
    print('Excel :', sortie)
    for fichier, erreur in erreurs:
        print(f'ATTENTION {fichier} : {erreur}', file=sys.stderr)

if __name__ == '__main__':
    main()
