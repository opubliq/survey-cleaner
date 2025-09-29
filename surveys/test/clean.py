#!/usr/bin/env python3
"""
Script de nettoyage pour [NOM_SONDAGE]

DUAL-MODE SCRIPT:
  - AWS Mode: Exposé via clean_data(df) pour pipeline_sondages lambda
  - Local Mode: Exécution standalone via python clean.py

AWS Integration:
    La fonction clean_data(df) est appelée par lambda_raffineur_nettoyage
    qui charge les données depuis S3 et gère l'export vers Parquet.

Local Usage:
    python clean.py

    Output:
        - processed/data_cleaned.csv: Données nettoyées
        - processed/codebook.json: Codebook standardisé
"""

import pandas as pd
import numpy as np
import json
from pathlib import Path

# Paths (used only in local mode)
BASE_DIR = Path(__file__).parent
RAW_DIR = BASE_DIR / "raw"
PROCESSED_DIR = BASE_DIR / "processed"

def clean_data(df):
    """Nettoyer et standardiser les données

    Cette fonction est le point d'entrée principal pour AWS lambda_raffineur_nettoyage.

    Args:
        df (pd.DataFrame): Données brutes chargées depuis Parquet

    Returns:
        pd.DataFrame: Données nettoyées

    Approche: Créer une nouvelle dataframe propre avec seulement les variables nettoyées.
    Les données raw (df) restent intactes.
    """
    # Initialize empty clean dataframe with same index
    df_clean = pd.DataFrame(index=df.index)

    # ============================================================================
    # VARIABLE PROCESSING
    # ============================================================================
    # Pour chaque variable, ajouter le code de nettoyage ici.
    # Pattern:
    #   1. Explorer la variable raw: df['raw_var']
    #   2. Nettoyer et créer nouvelle variable: df_clean['new_var'] = ...
    #   3. Ne jamais modifier df directement
    #
    # Exemple:
    # # Variable: age
    # df_clean['ses_age'] = df['Q1_age'].copy()
    # df_clean['ses_age'] = df_clean['ses_age'].replace({-99: np.nan, -98: np.nan})
    #
    # # Variable: satisfaction (Likert 1-5 -> 0-1)
    # df_clean['op_satisfaction'] = df['Q5_satisfaction'].copy()
    # df_clean['op_satisfaction'] = df_clean['op_satisfaction'].replace({-99: np.nan})
    # df_clean['op_satisfaction'] = (df_clean['op_satisfaction'] - 1) / 4
    # ============================================================================

    # TODO: Ajouter le code de nettoyage pour chaque variable ci-dessous

    # Variable: id -> id_respondent
    # Type: Identifier
    # Transformation: Rename with id_ prefix
    df_clean['id_respondent'] = df['id'].copy()

    # Variable: age -> ses_age (continuous) + ses_age_category (grouped)
    # Type: Numeric continuous
    # Transformation: Keep continuous + create categorical bins
    df_clean['ses_age'] = df['age'].copy()
    bins = [0, 25, 35, 45, 55, 100]
    labels = ['age_18_to_24', 'age_25_to_34', 'age_35_to_44', 'age_45_to_54', 'age_55_and_over']
    df_clean['ses_age_category'] = pd.cut(df['age'], bins=bins, labels=labels, right=False)

    # Variable: sexe -> ses_gender
    # Type: Categorical unordered
    # Transformation: Recode M/F to male/female
    df_clean['ses_gender'] = df['sexe'].copy()
    df_clean['ses_gender'] = df_clean['ses_gender'].replace({
        'M': 'male',
        'F': 'female'
    })

    # Variable: education -> ses_education
    # Type: Categorical unordered
    # Transformation: Recode to English descriptive names
    df_clean['ses_education'] = df['education'].copy()
    df_clean['ses_education'] = df_clean['ses_education'].replace({
        'Primaire': 'elementary_school',
        'Secondaire': 'high_school',
        'Collegial': 'college_cegep',
        'Universitaire': 'university'
    })

    # Variable: region -> ses_region
    # Type: Categorical unordered
    # Transformation: Standardize to lowercase with underscores
    df_clean['ses_region'] = df['region'].copy()
    df_clean['ses_region'] = df_clean['ses_region'].replace({
        'Quebec': 'quebec_city',
        'Montreal': 'montreal',
        'Laval': 'laval',
        'Gatineau': 'gatineau',
        'Sherbrooke': 'sherbrooke',
        'Trois-Rivieres': 'trois_rivieres',
        'Longueuil': 'longueuil'
    })

    # Variable: opinion_immigration -> op_immigration_opinion
    # Type: Likert scale (1-5)
    # Transformation: Normalize to 0-1 scale
    df_clean['op_immigration_opinion'] = df['opinion_immigration'].copy()
    df_clean['op_immigration_opinion'] = df_clean['op_immigration_opinion'].replace({99: np.nan})
    df_clean['op_immigration_opinion'] = (df_clean['op_immigration_opinion'] - 1) / 4

    return df_clean

# ============================================================================
# LOCAL MODE FUNCTIONS (not used by AWS lambda)
# ============================================================================

def load_data():
    """Charger les données brutes (local mode only)"""
    # TODO: Adapter selon le format (CSV, SAV, XLSX)
    data_file = list(RAW_DIR.glob("data.*"))[0]

    if data_file.suffix == ".csv":
        df = pd.read_csv(data_file)
    elif data_file.suffix == ".sav":
        import pyreadstat
        df, meta = pyreadstat.read_sav(data_file)
    elif data_file.suffix in [".xlsx", ".xls"]:
        df = pd.read_excel(data_file)
    else:
        raise ValueError(f"Format non supporté: {data_file.suffix}")

    return df

def create_codebook(df_clean):
    """Créer le codebook standardisé (local mode only)"""
    codebook = {
        "variables": {}
    }

    for col in df_clean.columns:
        codebook["variables"][col] = {
            "label": col,  # TODO: Ajouter les vrais labels
            "type": str(df_clean[col].dtype),
            "values": {},  # TODO: Ajouter les valeurs et labels si applicable
            "missing": int(df_clean[col].isna().sum()),
            "stats": {
                "n": int(len(df_clean)),
                "n_valid": int(df_clean[col].notna().sum())
            }
        }

    return codebook

def main():
    """Pipeline principal (local mode only)"""
    PROCESSED_DIR.mkdir(exist_ok=True)

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