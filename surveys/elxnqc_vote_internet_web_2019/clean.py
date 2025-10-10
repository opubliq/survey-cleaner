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
    #
    # RÈGLES CRITIQUES:
    #   1. Ne JAMAIS copier puis replace: df_clean['x'] = df['y'].copy() + .replace()
    #   2. TOUJOURS utiliser .map() pour catégorielles (unmapped → NaN automatique)
    #   3. Pour normalisation: créer vecteur NaN, puis remplir valeurs valides seulement
    #   4. Ne jamais modifier df directement
    #   5. Valeurs catégorielles: simples et concises (pas de répétition du nom de variable)
    #      - ses_province: "quebec", "ontario" (PAS "province_quebec", "province_ontario")
    #      - behav_vote_choice: "liberal", "conservative", "ndp" (abréviations anglaises OK)
    #
    # EXEMPLES SÉCURISÉS:
    #
    # # Categorical (USE .map(), NOT .copy() + .replace()):
    # df_clean['ses_gender'] = df['Q1_gender'].map({
    #     1.0: 'male',
    #     2.0: 'female',
    #     3.0: 'other'
    # })
    # # Unmapped values automatically become NaN
    #
    # # Province (simple values, no prefix):
    # df_clean['ses_province'] = df['Q2_province'].map({
    #     1.0: 'quebec',
    #     2.0: 'ontario',
    #     3.0: 'alberta',
    #     4.0: 'british_columbia'
    # })
    #
    # # Political parties (use short English abbreviations):
    # df_clean['behav_vote_choice'] = df['Q10_vote'].map({
    #     1.0: 'liberal',      # Liberal Party
    #     2.0: 'conservative', # Conservative Party
    #     3.0: 'ndp',          # New Democratic Party
    #     4.0: 'bloc',         # Bloc Québécois
    #     5.0: 'green',        # Green Party
    #     6.0: 'ppc',          # People's Party of Canada
    #     7.0: 'other',
    #     9.0: np.nan          # Don't know
    # })
    #
    # # Ordinal scale (map directly to normalized values):
    # df_clean['op_satisfaction'] = df['Q5_satisfaction'].map({
    #     1.0: 1.0,    # Very satisfied
    #     2.0: 0.75,
    #     3.0: 0.5,
    #     4.0: 0.25,
    #     5.0: 0.0,    # Very dissatisfied
    #     9.0: np.nan  # Don't know
    # })
    #
    # # Numeric normalization (0-100 → 0-1, safe pattern):
    # df_clean['op_party_rating'] = np.nan
    # mask = (df['Q10_rating'] >= 0) & (df['Q10_rating'] <= 100)
    # df_clean.loc[mask, 'op_party_rating'] = df.loc[mask, 'Q10_rating'] / 100.0
    # # Only valid range [0-100] is normalized, everything else stays NaN
    #
    # # Text/open-ended:
    # df_clean['op_comment'] = df['Q20_comment'].astype(str)
    # df_clean.loc[df['Q20_comment'].isna(), 'op_comment'] = np.nan
    # ============================================================================

    # TODO: Ajouter le code de nettoyage pour chaque variable ci-dessous

    # CLE → id_respondent: Unique respondent identifier
    df_clean['id_respondent'] = df['CLE'].astype(str)

    # DATE → tech_date_response: Date of survey response (ISO 8601 format YYYY-MM-DD)
    df_clean['tech_date_response'] = df['DATE'].apply(lambda x:
        f"20{str(int(x))[0:2]}-{str(int(x))[2:4]}-{str(int(x))[4:6]}"
    )

    # LANG → tech_language_survey: Survey questionnaire language
    df_clean['tech_language_survey'] = df['LANG'].map({
        1.0: 'french',
        2.0: 'english'
    })

    # B1 → op_internet_voting: Opinion on Internet voting (Likert scale 1-4)
    df_clean['op_internet_voting'] = df['B1'].map({
        1.0: 1.0,    # Tout à fait d'accord
        2.0: 0.667,  # Plutôt d'accord
        3.0: 0.333,  # Plutôt en désaccord
        4.0: 0.0,    # Tout à fait en désaccord
        9.0: np.nan  # NSP/Refus
    })

    # B4 → behav_internet_voting_intent: Likelihood of using Internet voting if offered (Likert scale 1-4)
    df_clean['behav_internet_voting_intent'] = df['B4'].map({
        1.0: 1.0,    # Certainement l'utiliserais
        2.0: 0.667,  # Probablement l'utiliserais
        3.0: 0.333,  # Probablement ne l'utiliserais pas
        4.0: 0.0,    # Certainement ne l'utiliserais pas
        8.0: 0.0,    # Je ne vote jamais aux élections (fonctionnellement = ne l'utiliserait pas)
        9.0: np.nan  # NSP/Refus
    })

    # B11 → op_internet_voting_confidence: Confidence in election results if Internet voting is added (Likert scale 1-4)
    df_clean['op_internet_voting_confidence'] = df['B11'].map({
        1.0: 1.0,    # Très confiant
        2.0: 0.667,  # Plutôt confiant
        3.0: 0.333,  # Plutôt pas confiant
        4.0: 0.0,    # Pas du tout confiant
        9.0: np.nan   # NSP/Refus
    })

    # C1 → op_coercion_concern: Concern about being coerced to vote for unwanted candidate (Likert scale 1-4)
    df_clean['op_coercion_concern'] = df['C1'].map({
        1.0: 1.0,    # Très inquiet(e)
        2.0: 0.667,  # Plutôt inquiet(e)
        3.0: 0.333,  # Plutôt pas inquiet(e)
        4.0: 0.0,    # Pas du tout inquiet(e)
        9.0: np.nan  # NSP/Refus
    })

    # C3 → op_privacy_concern: Concern about someone revealing how they voted (Likert scale 1-4)
    df_clean['op_privacy_concern'] = df['C3'].map({
        1.0: 1.0,    # Très inquiet(e)
        2.0: 0.667,  # Plutôt inquiet(e)
        3.0: 0.333,  # Plutôt pas inquiet(e)
        4.0: 0.0,    # Pas du tout inquiet(e)
        9.0: np.nan  # NSP/Refus
    })

    # C5 → op_fraud_concern: Concern about election results being modified by malicious act (Likert scale 1-4)
    df_clean['op_fraud_concern'] = df['C5'].map({
        1.0: 1.0,    # Très inquiet(e)
        2.0: 0.667,  # Plutôt inquiet(e)
        3.0: 0.333,  # Plutôt pas inquiet(e)
        4.0: 0.0,    # Pas du tout inquiet(e)
        9.0: np.nan  # NSP/Refus
    })

    # D1 → op_turnout_increase: Perceived effect of Internet voting on electoral turnout (Likert scale 1-4)
    df_clean['op_turnout_increase'] = df['D1'].map({
        1.0: 1.0,    # Beaucoup
        2.0: 0.667,  # Assez
        3.0: 0.333,  # Peu
        4.0: 0.0,    # Pas du tout
        9.0: np.nan  # NSP/Refus
    })

    # D3 → op_voting_ease: Perceived effect of Internet voting on ease of exercising right to vote (Likert scale 1-4)
    df_clean['op_voting_ease'] = df['D3'].map({
        1.0: 1.0,    # Beaucoup
        2.0: 0.667,  # Assez
        3.0: 0.333,  # Peu
        4.0: 0.0,    # Pas du tout
        9.0: np.nan  # NSP/Refus
    })

    # D6 → op_accuracy_improvement: Perceived effect of Internet voting on election accuracy (Likert scale 1-4)
    df_clean['op_accuracy_improvement'] = df['D6'].map({
        1.0: 1.0,    # Beaucoup
        2.0: 0.667,  # Assez
        3.0: 0.333,  # Peu
        4.0: 0.0,    # Pas du tout
        9.0: np.nan  # NSP/Refus
    })

    # AGE → ses_age_group: Age group of respondent
    df_clean['ses_age_group'] = df['AGE'].map({
        1.0: '18-24',
        2.0: '25-34',
        3.0: '35-44',
        4.0: '45-54',
        5.0: '55-64',
        6.0: '65+',
        9.0: np.nan,   # NSP
        10.0: np.nan,  # Refus
        99.0: np.nan   # Refus
    })

    # SEXE → ses_gender: Gender of respondent
    df_clean['ses_gender'] = df['SEXE'].map({
        1.0: 'male',
        2.0: 'female',
        3.0: 'non_binary',
        9.0: np.nan  # NSP/Refus
    })

    # REG → ses_region: Administrative region of Quebec (alphabetical order)
    df_clean['ses_region'] = df['REG'].map({
        1.0: 'abitibi_temiscamingue',
        2.0: 'bas_saint_laurent',
        3.0: 'capitale_nationale',
        4.0: 'centre_du_quebec',
        5.0: 'chaudiere_appalaches',
        6.0: 'cote_nord',
        7.0: 'estrie',
        8.0: 'gaspesie_iles_de_la_madeleine',
        9.0: 'lanaudiere',
        10.0: 'laurentides',
        11.0: 'laval',
        12.0: 'mauricie',
        13.0: 'monteregie',
        14.0: 'montreal',
        15.0: 'nord_du_quebec',
        16.0: 'outaouais',
        17.0: 'saguenay_lac_saint_jean',
        99.0: np.nan  # NSP/Refus
    })

    return df_clean

# ============================================================================
# LOCAL MODE FUNCTIONS (not used by AWS lambda)
# ============================================================================

def load_data():
    """Charger les données brutes (local mode only)"""
    # Charger le fichier Excel avec la feuille "Data"
    data_file = RAW_DIR / "VPI 2019_Consultation en ligne_Base de données.xlsx"

    if not data_file.exists():
        raise FileNotFoundError(f"Fichier non trouvé: {data_file}")

    df = pd.read_excel(data_file, sheet_name='Data')

    return df

def create_codebook(df_clean):
    """Créer le codebook standardisé dynamiquement (local mode only)

    Génère automatiquement:
    - Type de variable (numeric vs character)
    - Value counts pour variables catégorielles
    - Statistiques descriptives pour variables numériques
    - Counts de valeurs manquantes
    """
    codebook = {
        "survey": "elxnqc_vote_internet_web_2019",
        "variables": {}
    }

    for col in df_clean.columns:
        # Détection automatique du type
        dtype = df_clean[col].dtype
        is_numeric = pd.api.types.is_numeric_dtype(dtype)
        is_string = pd.api.types.is_string_dtype(dtype) or dtype == 'object'

        # Détection de variables spéciales (identifiants, dates, open-ended)
        is_identifier = col.startswith('id_') or col.endswith('_id')
        is_date = 'date' in col.lower() or col.startswith('tech_date')
        is_open_text = col.startswith('op_') and is_string and df_clean[col].nunique() > 100

        # Variables à exclure des value_counts
        skip_value_counts = is_identifier or is_date or is_open_text

        # Base metadata
        var_info = {
            "label": col,  # TODO: Enrichir avec vrais labels depuis codebook
            "type": "numeric" if is_numeric else "character",
            "original_variable": f"[RAW_{col}]",  # TODO: Mapper variable originale
            "missing": int(df_clean[col].isna().sum()),
            "stats": {
                "n": int(len(df_clean)),
                "n_valid": int(df_clean[col].notna().sum())
            }
        }

        # Pour variables catégorielles: ajouter value_counts (sauf identifiants/dates/open-text)
        if not skip_value_counts and (is_string or (is_numeric and df_clean[col].nunique() <= 20)):
            value_counts = df_clean[col].value_counts(dropna=True)
            total_valid = df_clean[col].notna().sum()

            var_info["values"] = {}
            for value, count in value_counts.items():
                var_info["values"][str(value)] = {
                    "count": int(count),
                    "percent": round(float(count) / total_valid * 100, 2) if total_valid > 0 else 0
                }

        # Pour variables numériques continues: ajouter stats descriptives (sauf identifiants/dates)
        if is_numeric and df_clean[col].nunique() > 20 and not skip_value_counts:
            series = df_clean[col].dropna()
            if len(series) > 0:
                var_info["stats"].update({
                    "mean": round(float(series.mean()), 3),
                    "sd": round(float(series.std()), 3),
                    "min": round(float(series.min()), 3),
                    "max": round(float(series.max()), 3),
                    "median": round(float(series.median()), 3)
                })

        codebook["variables"][col] = var_info

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