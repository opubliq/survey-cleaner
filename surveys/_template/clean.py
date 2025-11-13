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

# ============================================================================
# VARIABLE METADATA (pour enrichir codebook.json)
# ============================================================================
# Ce dictionnaire permet d'ajouter les labels des questions et choix de réponse
# au codebook.json final. Ces labels seront utilisés par les LLMs dans les marts
# pour interpréter sémantiquement les données.
#
# WORKFLOW:
# 1. Consultez raw/codebook.md pour la question et les choix de réponse
# 2. Nettoyez la variable dans clean_data() ci-dessous
# 3. Ajoutez l'entrée correspondante ici avec question_label et value_labels
#
# NOTE: C'est OPTIONNEL - si vous n'ajoutez pas les labels, codebook.json sera
#       quand même généré avec les stats de base.
#
# EXEMPLE:
# VARIABLE_METADATA = {
#     'op_satisfaction_gov': {
#         'question_label': "Dans quelle mesure êtes-vous satisfait du gouvernement actuel?",
#         'value_labels': {
#             0.0: "Très insatisfait",
#             0.25: "Plutôt insatisfait",
#             0.5: "Neutre",
#             0.75: "Plutôt satisfait",
#             1.0: "Très satisfait"
#         }
#     },
#     'ses_province': {
#         'question_label': "Dans quelle province habitez-vous?",
#         'value_labels': {
#             'quebec': "Québec",
#             'ontario': "Ontario",
#             'british_columbia': "Colombie-Britannique"
#         }
#     }
# }
VARIABLE_METADATA = {
    # Ajoutez vos variables ici au fur et à mesure du cleaning
}

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
    """Créer le codebook standardisé dynamiquement (local mode only)

    Génère automatiquement:
    - Type de variable (numeric vs character)
    - Value counts pour variables catégorielles
    - Statistiques descriptives pour variables numériques
    - Counts de valeurs manquantes
    - Labels de questions et choix de réponse (depuis VARIABLE_METADATA)
    """
    codebook = {
        "survey": "[NOM_SONDAGE]",  # TODO: Remplacer par nom réel
        "variables": {}
    }

    for col in df_clean.columns:
        # Détection automatique du type
        dtype = df_clean[col].dtype
        is_numeric = pd.api.types.is_numeric_dtype(dtype)
        is_string = pd.api.types.is_string_dtype(dtype) or dtype == 'object'

        # Base metadata
        var_info = {
            "label": col,
            "type": "numeric" if is_numeric else "character",
            "original_variable": f"[RAW_{col}]",  # TODO: Mapper variable originale
            "missing": int(df_clean[col].isna().sum()),
            "stats": {
                "n": int(len(df_clean)),
                "n_valid": int(df_clean[col].notna().sum())
            }
        }

        # Enrichir avec metadata si présentes (question_label et value_labels)
        if col in VARIABLE_METADATA:
            meta = VARIABLE_METADATA[col]
            if 'question_label' in meta:
                var_info['question_label'] = meta['question_label']

        # Pour variables catégorielles: ajouter value_counts
        if is_string or (is_numeric and df_clean[col].nunique() <= 20):
            value_counts = df_clean[col].value_counts(dropna=True)
            total_valid = df_clean[col].notna().sum()

            var_info["values"] = {}
            for value, count in value_counts.items():
                value_str = str(value)
                value_entry = {
                    "count": int(count),
                    "percent": round(float(count) / total_valid * 100, 2) if total_valid > 0 else 0
                }

                # Enrichir avec value_label si disponible dans VARIABLE_METADATA
                if col in VARIABLE_METADATA and 'value_labels' in VARIABLE_METADATA[col]:
                    # Convertir la clé pour lookup (numeric ou string)
                    lookup_key = float(value_str) if is_numeric else value
                    if lookup_key in VARIABLE_METADATA[col]['value_labels']:
                        value_entry['label'] = VARIABLE_METADATA[col]['value_labels'][lookup_key]

                var_info["values"][value_str] = value_entry

        # Pour variables numériques continues: ajouter stats descriptives
        if is_numeric and df_clean[col].nunique() > 20:
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