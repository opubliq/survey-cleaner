#!/usr/bin/env python3
"""
Script de nettoyage pour [NOM_SONDAGE]

Usage:
    python clean.py

Output:
    - processed/data_cleaned.csv: Données nettoyées
    - processed/codebook.json: Codebook standardisé
"""

import pandas as pd
import numpy as np
import json
from pathlib import Path

# Paths
BASE_DIR = Path(__file__).parent
RAW_DIR = BASE_DIR / "raw"
PROCESSED_DIR = BASE_DIR / "processed"
PROCESSED_DIR.mkdir(exist_ok=True)

def load_data():
    """Charger les données brutes"""
    # TODO: Adapter selon le format (CSV, SAV, XLSX)
    data_file = list(RAW_DIR.glob("data.*"))[0]

    if data_file.suffix == ".csv":
        df = pd.read_csv(data_file)
    elif data_file.suffix == ".sav":
        df = pd.read_spss(data_file)
    elif data_file.suffix in [".xlsx", ".xls"]:
        df = pd.read_excel(data_file)
    else:
        raise ValueError(f"Format non supporté: {data_file.suffix}")

    return df

def clean_data(df):
    """Nettoyer et standardiser les données"""
    df_clean = df.copy()

    # TODO: Implémenter le nettoyage
    # 1. Renommer les variables selon les conventions
    # 2. Recoder les valeurs manquantes
    # 3. Standardiser les échelles
    # 4. Créer les variables dérivées si nécessaire

    return df_clean

def create_codebook(df_clean):
    """Créer le codebook standardisé"""
    codebook = {
        "variables": {}
    }

    for col in df_clean.columns:
        codebook["variables"][col] = {
            "label": col,  # TODO: Ajouter les vrais labels
            "type": str(df_clean[col].dtype),
            "values": {},  # TODO: Ajouter les valeurs et labels si applicable
            "missing": df_clean[col].isna().sum(),
            "stats": {
                "n": len(df_clean),
                "n_valid": df_clean[col].notna().sum()
            }
        }

    return codebook

def main():
    """Pipeline principal"""
    print("Chargement des données...")
    df = load_data()
    print(f"  {len(df)} observations, {len(df.columns)} variables")

    print("\nNettoyage des données...")
    df_clean = clean_data(df)

    print("\nCréation du codebook...")
    codebook = create_codebook(df_clean)

    print("\nSauvegarde...")
    df_clean.to_csv(PROCESSED_DIR / "data_cleaned.csv", index=False)
    with open(PROCESSED_DIR / "codebook.json", "w", encoding="utf-8") as f:
        json.dump(codebook, f, indent=2, ensure_ascii=False)

    print("\n✓ Traitement terminé")
    print(f"  - {PROCESSED_DIR / 'data_cleaned.csv'}")
    print(f"  - {PROCESSED_DIR / 'codebook.json'}")

if __name__ == "__main__":
    main()