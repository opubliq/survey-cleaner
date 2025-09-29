#!/usr/bin/env python3
"""
Script de nettoyage pour CES 2019 (Canadian Election Study 2019)

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
from datetime import datetime, timedelta

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

    # Variable: cps19_StartDate -> tech_survey_start_date
    # Technical metadata: Survey start timestamp
    # Keep as string representation (Stata timestamp format)
    df_clean['tech_survey_start_date'] = df['cps19_StartDate'].astype(str)
    df_clean.loc[df['cps19_StartDate'].isna(), 'tech_survey_start_date'] = np.nan

    # Variable: cps19_EndDate -> tech_survey_end_date
    # Technical metadata: Survey end timestamp
    # Keep as string representation (Stata timestamp format)
    df_clean['tech_survey_end_date'] = df['cps19_EndDate'].astype(str)
    df_clean.loc[df['cps19_EndDate'].isna(), 'tech_survey_end_date'] = np.nan

    # Variable: cps19_ResponseId -> id_respondent
    # Unique respondent identifier
    df_clean['id_respondent'] = df['cps19_ResponseId'].copy()

    return df_clean

# ============================================================================
# LOCAL MODE FUNCTIONS (not used by AWS lambda)
# ============================================================================

def load_data():
    """Charger les données brutes (local mode only)"""
    data_file = RAW_DIR / "ces_2019.sav"

    import pyreadstat
    # Handle encoding issues
    try:
        df, meta = pyreadstat.read_sav(data_file, encoding='utf-8')
    except:
        try:
            df, meta = pyreadstat.read_sav(data_file, encoding='latin1')
        except:
            df, meta = pyreadstat.read_sav(data_file, encoding='cp1252')

    return df

def create_codebook(df_clean, df_raw):
    """Créer le codebook standardisé (local mode only)"""
    codebook = {
        "survey": "Canadian Election Study 2019",
        "variables": {}
    }

    # tech_survey_start_date
    codebook["variables"]["tech_survey_start_date"] = {
        "label": "Campaign Period Survey start timestamp",
        "type": "character",
        "encoding": "stata_timestamp_string",
        "original_variable": "cps19_StartDate",
        "missing": int(df_clean["tech_survey_start_date"].isna().sum()),
        "stats": {
            "n": int(len(df_clean)),
            "n_valid": int(df_clean["tech_survey_start_date"].notna().sum())
        }
    }

    # tech_survey_end_date
    codebook["variables"]["tech_survey_end_date"] = {
        "label": "Campaign Period Survey end timestamp",
        "type": "character",
        "encoding": "stata_timestamp_string",
        "original_variable": "cps19_EndDate",
        "missing": int(df_clean["tech_survey_end_date"].isna().sum()),
        "stats": {
            "n": int(len(df_clean)),
            "n_valid": int(df_clean["tech_survey_end_date"].notna().sum())
        }
    }

    # id_respondent
    codebook["variables"]["id_respondent"] = {
        "label": "Unique respondent identifier",
        "type": "character",
        "original_variable": "cps19_ResponseId",
        "unique": True,
        "missing": int(df_clean["id_respondent"].isna().sum()),
        "stats": {
            "n": int(len(df_clean)),
            "n_valid": int(df_clean["id_respondent"].notna().sum()),
            "n_unique": int(df_clean["id_respondent"].nunique())
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
    codebook = create_codebook(df_clean, df)

    print("\nSauvegarde...")
    df_clean.to_csv(PROCESSED_DIR / "data_cleaned.csv", index=False)
    with open(PROCESSED_DIR / "codebook.json", "w", encoding="utf-8") as f:
        json.dump(codebook, f, indent=2, ensure_ascii=False)

    print("\n✓ Traitement terminé")
    print(f"  - {PROCESSED_DIR / 'data_cleaned.csv'}")
    print(f"  - {PROCESSED_DIR / 'codebook.json'}")
    print(f"\nVariables nettoyées: {len(df_clean.columns)}")

if __name__ == "__main__":
    main()