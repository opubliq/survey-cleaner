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

    # Variable: cps19_consent -> tech_consent
    # Survey consent indicator (all respondents consented, value = 1)
    df_clean['tech_consent'] = df['cps19_consent'].copy()

    # Variable: cps19_citizenship -> ses_citizenship
    # Citizenship status (categorical)
    # 4 = Canadian citizen, 5 = Permanent resident, 6 = Other (screened out)
    df_clean['ses_citizenship'] = df['cps19_citizenship'].copy()
    df_clean['ses_citizenship'] = df_clean['ses_citizenship'].replace({
        4.0: 'canadian_citizen',
        5.0: 'permanent_resident',
        6.0: 'other'
    })

    # Variable: cps19_yob -> tech_yob_quota
    # Technical quota variable (not actual year of birth, values 1-82)
    df_clean['tech_yob_quota'] = df['cps19_yob'].copy()

    # Variable: cps19_yob_2001_age -> tech_age_screening
    # Age screening for people born in 2001 (1=17, 2=18)
    # Most values are missing (only filled for people born in 2001)
    df_clean['tech_age_screening'] = df['cps19_yob_2001_age'].copy()

    # Variable: cps19_gender -> ses_gender
    # Gender (categorical)
    # 1 = man, 2 = woman, 3 = other
    df_clean['ses_gender'] = df['cps19_gender'].copy()
    df_clean['ses_gender'] = df_clean['ses_gender'].replace({
        1.0: 'male',
        2.0: 'female',
        3.0: 'other'
    })

    # Variable: cps19_province -> ses_province
    # Province or territory of residence
    df_clean['ses_province'] = df['cps19_province'].copy()
    df_clean['ses_province'] = df_clean['ses_province'].replace({
        14.0: 'province_alberta',
        15.0: 'province_british_columbia',
        16.0: 'province_manitoba',
        17.0: 'province_new_brunswick',
        18.0: 'province_newfoundland_and_labrador',
        19.0: 'territory_northwest_territories',
        20.0: 'province_nova_scotia',
        21.0: 'territory_nunavut',
        22.0: 'province_ontario',
        23.0: 'province_prince_edward_island',
        24.0: 'province_quebec',
        25.0: 'province_saskatchewan',
        26.0: 'territory_yukon'
    })

    # Variable: cps19_education -> ses_education
    # Highest level of education completed
    df_clean['ses_education'] = df['cps19_education'].copy()
    df_clean['ses_education'] = df_clean['ses_education'].replace({
        1.0: 'no_schooling',
        2.0: 'some_elementary',
        3.0: 'completed_elementary',
        4.0: 'some_secondary',
        5.0: 'completed_secondary',
        6.0: 'some_technical_college',
        7.0: 'completed_technical_college',
        8.0: 'some_university',
        9.0: 'bachelor_degree',
        10.0: 'master_degree',
        11.0: 'professional_or_doctorate',
        12.0: np.nan  # Don't know/Prefer not to answer -> missing
    })

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

    # tech_consent
    codebook["variables"]["tech_consent"] = {
        "label": "Survey consent indicator",
        "type": "numeric",
        "original_variable": "cps19_consent",
        "note": "All respondents in dataset consented (value = 1)",
        "missing": int(df_clean["tech_consent"].isna().sum()),
        "stats": {
            "n": int(len(df_clean)),
            "n_valid": int(df_clean["tech_consent"].notna().sum())
        }
    }

    # ses_citizenship
    val_counts = df_clean["ses_citizenship"].value_counts()
    codebook["variables"]["ses_citizenship"] = {
        "label": "Citizenship status",
        "type": "character",
        "original_variable": "cps19_citizenship",
        "values": {
            val: {"count": int(val_counts.get(val, 0)),
                  "percent": round(100 * val_counts.get(val, 0) / len(df_clean), 2)}
            for val in ['canadian_citizen', 'permanent_resident', 'other']
        },
        "missing": int(df_clean["ses_citizenship"].isna().sum()),
        "stats": {
            "n": int(len(df_clean)),
            "n_valid": int(df_clean["ses_citizenship"].notna().sum())
        }
    }

    # tech_yob_quota
    codebook["variables"]["tech_yob_quota"] = {
        "label": "Year of birth quota variable (technical, not actual YOB)",
        "type": "numeric",
        "original_variable": "cps19_yob",
        "note": "Quota variable with values 1-82, not actual year of birth",
        "missing": int(df_clean["tech_yob_quota"].isna().sum()),
        "stats": {
            "n": int(len(df_clean)),
            "n_valid": int(df_clean["tech_yob_quota"].notna().sum())
        }
    }

    # tech_age_screening
    codebook["variables"]["tech_age_screening"] = {
        "label": "Age screening question for respondents born in 2001",
        "type": "numeric",
        "original_variable": "cps19_yob_2001_age",
        "note": "1=17 years old (screened out), 2=18 years old. Mostly missing (only for people born in 2001)",
        "missing": int(df_clean["tech_age_screening"].isna().sum()),
        "stats": {
            "n": int(len(df_clean)),
            "n_valid": int(df_clean["tech_age_screening"].notna().sum())
        }
    }

    # ses_gender
    val_counts_gender = df_clean["ses_gender"].value_counts()
    codebook["variables"]["ses_gender"] = {
        "label": "Gender",
        "type": "character",
        "original_variable": "cps19_gender",
        "values": {
            val: {"count": int(val_counts_gender.get(val, 0)),
                  "percent": round(100 * val_counts_gender.get(val, 0) / len(df_clean), 2)}
            for val in ['male', 'female', 'other']
        },
        "missing": int(df_clean["ses_gender"].isna().sum()),
        "stats": {
            "n": int(len(df_clean)),
            "n_valid": int(df_clean["ses_gender"].notna().sum())
        }
    }

    # ses_province
    val_counts_province = df_clean["ses_province"].value_counts()
    codebook["variables"]["ses_province"] = {
        "label": "Province or territory of residence",
        "type": "character",
        "original_variable": "cps19_province",
        "values": {
            val: {"count": int(val_counts_province.get(val, 0)),
                  "percent": round(100 * val_counts_province.get(val, 0) / len(df_clean), 2)}
            for val in val_counts_province.index
        },
        "missing": int(df_clean["ses_province"].isna().sum()),
        "stats": {
            "n": int(len(df_clean)),
            "n_valid": int(df_clean["ses_province"].notna().sum())
        }
    }

    # ses_education
    val_counts_education = df_clean["ses_education"].value_counts()
    codebook["variables"]["ses_education"] = {
        "label": "Highest level of education completed",
        "type": "character",
        "original_variable": "cps19_education",
        "note": "Original value 12 (Don't know/Prefer not to answer) recoded to missing",
        "values": {
            val: {"count": int(val_counts_education.get(val, 0)),
                  "percent": round(100 * val_counts_education.get(val, 0) / len(df_clean), 2)}
            for val in val_counts_education.index
        },
        "missing": int(df_clean["ses_education"].isna().sum()),
        "stats": {
            "n": int(len(df_clean)),
            "n_valid": int(df_clean["ses_education"].notna().sum())
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