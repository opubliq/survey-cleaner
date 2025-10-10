#!/usr/bin/env python3
"""
Script pour compter le nombre de variables dans tous les datasets de SharedFolder_data_produit/
"""

import os
import sys
import pandas as pd
import pyreadstat
import chardet
from pathlib import Path

def identify_dataset_file(folder_path):
    """
    Identifie le fichier dataset dans un dossier (exclut les codebooks)
    Retourne (filepath, type) ou (None, None) si non trouvé
    """
    files = list(folder_path.iterdir())

    # Priorité: .csv, .dta, .sav
    # Exclure les fichiers contenant 'codebook', 'dictionary', 'guide' dans le nom
    exclude_keywords = ['codebook', 'dictionary', 'guide', 'readme']

    data_files = {
        'csv': [],
        'dta': [],
        'sav': [],
        'xlsx': []
    }

    for file in files:
        if file.is_file():
            ext = file.suffix.lower()[1:]  # Enlever le point
            filename_lower = file.name.lower()

            # Vérifier si c'est un codebook
            is_codebook = any(keyword in filename_lower for keyword in exclude_keywords)

            if ext in data_files and not is_codebook:
                data_files[ext].append(file)

    # Ordre de priorité: csv > dta > sav > xlsx
    for ext in ['csv', 'dta', 'sav', 'xlsx']:
        if data_files[ext]:
            # Prendre le plus gros fichier si plusieurs
            largest = max(data_files[ext], key=lambda f: f.stat().st_size)
            return largest, ext

    return None, None

def detect_encoding(filepath):
    """
    Détecte l'encodage d'un fichier en utilisant chardet
    """
    with open(filepath, 'rb') as f:
        raw_data = f.read(100000)  # Lire les premiers 100KB
        result = chardet.detect(raw_data)
        return result['encoding']

def count_variables(filepath, filetype):
    """
    Compte le nombre de variables (colonnes) dans un dataset
    Retourne (n_vars, n_rows) ou (None, None) en cas d'erreur
    """
    try:
        if filetype == 'csv':
            # Détecter l'encodage automatiquement
            detected_encoding = detect_encoding(filepath)
            print(f"   Encodage détecté: {detected_encoding}")

            # Essayer d'abord avec l'encodage détecté, puis avec des fallbacks
            encodings = [detected_encoding, 'utf-8', 'latin-1', 'cp1252', 'iso-8859-1', 'windows-1252']
            # Retirer les doublons tout en préservant l'ordre
            encodings = list(dict.fromkeys([e for e in encodings if e]))

            # Essayer différents séparateurs
            separators = [',', ';', '\t', '|']

            df = None
            last_error = None
            best_result = None

            for encoding in encodings:
                for sep in separators:
                    try:
                        df = pd.read_csv(filepath, nrows=1, encoding=encoding, sep=sep,
                                       low_memory=False, on_bad_lines='warn')
                        n_vars = len(df.columns)

                        # Garder le meilleur résultat (le plus de colonnes)
                        if best_result is None or n_vars > best_result['n_vars']:
                            # Pour le nombre de lignes, on lit tout avec le même encodage et séparateur
                            df_full = pd.read_csv(filepath, encoding=encoding, sep=sep,
                                                 low_memory=False, on_bad_lines='warn')
                            n_rows = len(df_full)
                            best_result = {
                                'n_vars': n_vars,
                                'n_rows': n_rows,
                                'encoding': encoding,
                                'sep': sep
                            }
                    except (UnicodeDecodeError, UnicodeError) as e:
                        last_error = e
                        continue
                    except Exception as e:
                        last_error = e
                        continue

            # Si on a trouvé au moins un résultat
            if best_result and best_result['n_vars'] > 1:
                print(f"   Encodage utilisé: {best_result['encoding']}, Séparateur: {repr(best_result['sep'])}")
                return best_result['n_vars'], best_result['n_rows']

            # Si tous les encodages ont échoué
            if last_error:
                raise last_error

        elif filetype == 'dta':
            df, meta = pyreadstat.read_dta(filepath, row_limit=1)
            n_vars = len(df.columns)
            # Relire pour avoir le nombre de lignes
            df_full, _ = pyreadstat.read_dta(filepath)
            n_rows = len(df_full)
            return n_vars, n_rows

        elif filetype == 'sav':
            df, meta = pyreadstat.read_sav(filepath, row_limit=1)
            n_vars = len(df.columns)
            # Relire pour avoir le nombre de lignes
            df_full, _ = pyreadstat.read_sav(filepath)
            n_rows = len(df_full)
            return n_vars, n_rows

        elif filetype == 'xlsx':
            df = pd.read_excel(filepath, nrows=1)
            n_vars = len(df.columns)
            df_full = pd.read_excel(filepath)
            n_rows = len(df_full)
            return n_vars, n_rows

    except Exception as e:
        print(f"❌ Erreur lors de la lecture de {filepath.name}: {e}", file=sys.stderr)
        return None, None

    return None, None

def check_if_cleaned(folder_name):
    """
    Vérifie si le dataset a été nettoyé (existe dans surveys/)
    Retourne True si le dossier existe avec un clean.py
    """
    survey_path = Path("surveys") / folder_name
    if survey_path.exists() and survey_path.is_dir():
        # Vérifier si clean.py existe
        clean_py = survey_path / "clean.py"
        if clean_py.exists():
            return "✅ Done"
        else:
            return "🔧 In Progress"
    return "❌ Not Started"

def main():
    base_path = Path("SharedFolder_data_produit")

    if not base_path.exists():
        print(f"❌ Le dossier {base_path} n'existe pas")
        sys.exit(1)

    results = []

    # Parcourir tous les sous-dossiers
    folders = sorted([f for f in base_path.iterdir() if f.is_dir() and not f.name.startswith('_')])

    print(f"🔍 Analyse de {len(folders)} dossiers...\n")

    for folder in folders:
        dataset_file, filetype = identify_dataset_file(folder)

        # Vérifier si le dataset a été nettoyé
        cleaned_status = check_if_cleaned(folder.name)

        if dataset_file is None:
            print(f"⚠️  {folder.name}: Aucun dataset trouvé")
            results.append({
                'folder': folder.name,
                'dataset_file': 'N/A',
                'file_type': 'N/A',
                'n_variables': 'N/A',
                'n_rows': 'N/A',
                'status': 'NOT_FOUND',
                'cleaned': cleaned_status
            })
            continue

        print(f"📊 {folder.name} {cleaned_status}")
        print(f"   Fichier: {dataset_file.name} ({filetype})")

        n_vars, n_rows = count_variables(dataset_file, filetype)

        if n_vars is not None:
            print(f"   Variables: {n_vars}")
            print(f"   Observations: {n_rows}")
            status = 'OK'
        else:
            print(f"   ❌ Erreur lors de la lecture")
            status = 'ERROR'

        print()

        results.append({
            'folder': folder.name,
            'dataset_file': dataset_file.name,
            'file_type': filetype,
            'n_variables': n_vars if n_vars is not None else 'ERROR',
            'n_rows': n_rows if n_rows is not None else 'ERROR',
            'status': status,
            'cleaned': cleaned_status
        })

    # Créer un DataFrame avec les résultats
    df_results = pd.DataFrame(results)

    # Sauvegarder en CSV
    output_file = "dataset_tracker.csv"
    df_results.to_csv(output_file, index=False)
    print(f"✅ Résultats sauvegardés dans {output_file}")

    # Afficher un résumé
    print("\n" + "="*80)
    print("RÉSUMÉ")
    print("="*80)
    print(f"Total datasets analysés: {len(results)}")
    print(f"Succès: {len([r for r in results if r['status'] == 'OK'])}")
    print(f"Erreurs: {len([r for r in results if r['status'] == 'ERROR'])}")
    print(f"Non trouvés: {len([r for r in results if r['status'] == 'NOT_FOUND'])}")

    if any(r['status'] == 'OK' for r in results):
        total_vars = sum(r['n_variables'] for r in results if isinstance(r['n_variables'], int))
        print(f"\nTotal de variables (tous datasets): {total_vars}")

    # Statistiques de nettoyage
    print("\n" + "="*80)
    print("STATUT DE NETTOYAGE")
    print("="*80)
    done = len([r for r in results if r['cleaned'] == '✅ Done'])
    in_progress = len([r for r in results if r['cleaned'] == '🔧 In Progress'])
    not_started = len([r for r in results if r['cleaned'] == '❌ Not Started'])

    print(f"✅ Done: {done}/{len(results)}")
    print(f"🔧 In Progress: {in_progress}/{len(results)}")
    print(f"❌ Not Started: {not_started}/{len(results)}")

    if len(results) > 0:
        progress_pct = (done / len(results)) * 100
        print(f"\nProgression globale: {progress_pct:.1f}%")

if __name__ == "__main__":
    main()
