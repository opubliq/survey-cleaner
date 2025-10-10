#!/usr/bin/env python3
"""
Script d'exploration de variables pour elxnqc_vote_internet_web_2019
Permet d'explorer n'importe quelle variable avec son codebook

Usage:
    python _explore_var.py VARIABLE_NAME
    python _explore_var.py  # Mode interactif
"""

import pandas as pd
import numpy as np
import sys
from pathlib import Path

# Paths
SURVEY_DIR = Path(__file__).parent
RAW_DIR = SURVEY_DIR / "raw"
DATA_FILE = RAW_DIR / "VPI 2019_Consultation en ligne_Base de données.xlsx"

def load_data():
    """Charger les données et le codebook"""
    print(f"📂 Chargement: {DATA_FILE.name}")

    # Charger données
    df = pd.read_excel(DATA_FILE, sheet_name='Data')

    # Charger codebook (feuille 'Doc')
    df_codebook = pd.read_excel(DATA_FILE, sheet_name='Doc', header=None)

    return df, df_codebook

def find_in_codebook(var_name, df_codebook):
    """Chercher la variable dans le codebook"""
    # La structure est: [variable, label, modalites]
    matches = df_codebook[df_codebook[0] == var_name]

    if len(matches) > 0:
        row = matches.iloc[0]
        return {
            'variable': row[0],
            'label': row[1] if pd.notna(row[1]) else 'N/A',
            'modalites_ref': row[2] if pd.notna(row[2]) else 'N/A'
        }
    return None

def explore_variable(df, var_name, codebook_info):
    """Explorer une variable avec stats adaptées au type"""

    if var_name not in df.columns:
        print(f"\n❌ Variable '{var_name}' non trouvée!")
        print(f"\nVariables disponibles ({len(df.columns)}):")
        for col in sorted(df.columns):
            print(f"  - {col}")
        return

    print("\n" + "="*80)
    print(f"VARIABLE: {var_name}")
    print("="*80)

    # Codebook
    if codebook_info:
        print(f"\n📖 CODEBOOK:")
        print(f"   Label: {codebook_info['label']}")
        print(f"   Modalités: {codebook_info['modalites_ref']}")
    else:
        print(f"\n⚠️  Pas de description dans le codebook")

    # Stats de base
    series = df[var_name]
    dtype = series.dtype
    n_total = len(series)
    n_missing = series.isna().sum()
    n_valid = n_total - n_missing
    n_unique = series.nunique()

    print(f"\n📊 STATISTIQUES:")
    print(f"   Type: {dtype}")
    print(f"   Total obs: {n_total:,}")
    print(f"   Valeurs valides: {n_valid:,} ({n_valid/n_total*100:.1f}%)")
    print(f"   Valeurs manquantes: {n_missing:,} ({n_missing/n_total*100:.1f}%)")
    print(f"   Valeurs uniques: {n_unique:,}")

    # Exploration selon le type
    is_numeric = pd.api.types.is_numeric_dtype(dtype)
    is_string = pd.api.types.is_string_dtype(dtype) or dtype == 'object'

    if is_string or (is_numeric and n_unique <= 30):
        # CATÉGORIELLE ou NUMÉRIQUE DISCRÈTE
        print(f"\n🔢 VALUE COUNTS (top 30):")
        value_counts = series.value_counts(dropna=False).head(30)
        for value, count in value_counts.items():
            pct = count / n_total * 100
            bar = "█" * int(pct / 2)  # Bar chart ASCII
            value_str = str(value) if pd.notna(value) else "[MISSING]"
            print(f"   {value_str:20s} : {count:>6,} ({pct:5.1f}%) {bar}")

    elif is_numeric and n_unique > 30:
        # NUMÉRIQUE CONTINUE
        series_clean = series.dropna()

        if len(series_clean) > 0:
            print(f"\n📈 STATISTIQUES DESCRIPTIVES:")
            print(f"   Min: {series_clean.min():,.2f}")
            print(f"   Q1 (25%): {series_clean.quantile(0.25):,.2f}")
            print(f"   Médiane: {series_clean.median():,.2f}")
            print(f"   Q3 (75%): {series_clean.quantile(0.75):,.2f}")
            print(f"   Max: {series_clean.max():,.2f}")
            print(f"   Moyenne: {series_clean.mean():,.2f}")
            print(f"   Écart-type: {series_clean.std():,.2f}")

            # Histogramme ASCII simple
            print(f"\n📊 DISTRIBUTION (10 bins):")
            hist, bins = np.histogram(series_clean, bins=10)
            max_count = hist.max()
            for i, (count, left, right) in enumerate(zip(hist, bins[:-1], bins[1:])):
                bar = "█" * int(count / max_count * 40)
                print(f"   [{left:>10.1f} - {right:>10.1f}] : {count:>5,} {bar}")

    else:
        # AUTRE TYPE
        print(f"\n🔍 PREMIÈRES VALEURS (10):")
        print(series.head(10))

    print("\n" + "="*80)

def main():
    # Récupérer le nom de la variable
    if len(sys.argv) > 1:
        var_name = sys.argv[1]
    else:
        var_name = input("Nom de la variable à explorer: ").strip()

    if not var_name:
        print("❌ Aucune variable spécifiée!")
        sys.exit(1)

    # Charger données
    df, df_codebook = load_data()

    # Chercher dans codebook
    codebook_info = find_in_codebook(var_name, df_codebook)

    # Explorer
    explore_variable(df, var_name, codebook_info)

if __name__ == "__main__":
    main()
