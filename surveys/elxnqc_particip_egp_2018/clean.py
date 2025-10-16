#!/usr/bin/env python3
"""
Script de nettoyage pour elxnqc_particip_egp_2018

DUAL-MODE SCRIPT:
  - AWS Mode: Exposé via clean_data(df) pour pipeline_sondages lambda
  - Local Mode: Exécution standalone via python clean.py

AWS Integration:
    La fonction clean_data(df) est appelée par lambda_raffineur_nettoyage
    qui charge les données depuis S3 et gère l'export vers Parquet.

Local Usage:
    python surveys/elxnqc_particip_egp_2018/clean.py

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

    # VOT1 - Participation électorale provinciale 2018
    # 1 = Voted, 2 = Did not vote
    df_clean['behav_vote_turnout_provincial_2018'] = df['VOT1'].map({
        1: 1.0,  # Voted
        2: 0.0   # Did not vote
    })

    # REGIO - Région administrative du Québec (17 régions)
    df_clean['ses_region_administrative'] = df['REGIO'].map({
        1: 'bas_saint_laurent',
        2: 'saguenay_lac_saint_jean',
        3: 'capitale_nationale',
        4: 'mauricie_bois_franc',
        5: 'estrie',
        6: 'montreal',
        7: 'outaouais',
        8: 'abitibi_temiscamingue',
        9: 'cote_nord',
        10: 'nord_du_quebec',
        11: 'gaspesie_iles_madeleine',
        12: 'chaudiere_appalaches',
        13: 'laval',
        14: 'lanaudiere',
        15: 'laurentides',
        16: 'monteregie',
        17: 'centre_du_quebec'
    })

    # REGIX - Regroupement régional (3 catégories)
    df_clean['ses_region_grouped'] = df['REGIX'].map({
        1: 'montreal',
        2: 'quebec',
        3: 'elsewhere'
    })

    # ZONE - Type de zone (urbain/intermédiaire/rural)
    df_clean['ses_zone_type'] = df['ZONE'].map({
        1: 'urban',           # Grands centres urbains
        2: 'intermediate',    # Zones intermédiaires
        3: 'rural'            # Zones rurales et éloignées
    })

    # Q2 - Catégories d'âge (6 groupes)
    df_clean['ses_age_category'] = df['Q2'].map({
        1: '18_24',      # 18 à 24 ans
        2: '25_34',      # 25 à 34 ans
        3: '35_44',      # 35 à 44 ans
        4: '45_54',      # 45 à 54 ans
        5: '55_64',      # 55 à 64 ans
        6: '65_plus'     # 65 ans et plus
    })

    # Q4 - Nuance de participation électorale (4 niveaux)
    df_clean['behav_vote_intention_type'] = df['Q4'].map({
        1: 'did_not_vote_no_intention',           # Je n'ai pas voté
        2: 'thought_about_voting_but_did_not',    # J'ai pensé à voter mais n'y suis pas allé
        3: 'usually_vote_but_not_this_time',      # D'habitude je vote mais pas cette fois
        4: 'voted'                                # J'ai voté
    })

    # Q5 - Moment de la décision de vote (timing)
    df_clean['behav_vote_decision_timing'] = df['Q5'].map({
        1: 'more_than_month_before',     # Plus d'un mois avant
        2: 'few_weeks_before',           # Quelques semaines avant
        3: 'few_days_before',            # Quelques jours avant
        4: 'election_day',               # Le jour du vote
        9: np.nan                        # Ne sais pas
    })

    # Q6A-Q6P - Série de facteurs qui ont joué un rôle (16 items binaires)
    # Questions conditionnelles posées aux non-votants (75% missing)
    # 1.0 = Oui, a joué un rôle, 2.0 = Non
    q6_vars = ['Q6A', 'Q6B', 'Q6C', 'Q6D', 'Q6E', 'Q6F', 'Q6G', 'Q6H',
               'Q6I', 'Q6J', 'Q6K', 'Q6L', 'Q6M', 'Q6N', 'Q6O', 'Q6P']
    for i, var in enumerate(q6_vars, start=1):
        df_clean[f'op_nonvoting_reason_{chr(96+i)}'] = df[var].map({
            1.0: 1.0,  # Oui, a joué un rôle
            2.0: 0.0   # Non
        })

    # Q8A-Q8I - Série de facteurs qui ont joué un rôle (9 items binaires)
    # Questions conditionnelles posées aux votants (25% missing)
    # 1.0 = Oui, a joué un rôle, 2.0 = Non
    q8_vars = ['Q8A', 'Q8B', 'Q8C', 'Q8D', 'Q8E', 'Q8F', 'Q8G', 'Q8H', 'Q8I']
    for i, var in enumerate(q8_vars, start=1):
        df_clean[f'op_voting_reason_{chr(96+i)}'] = df[var].map({
            1.0: 1.0,  # Oui, a joué un rôle
            2.0: 0.0   # Non
        })

    # Q9A-Q9C - Participation à des élections passées (binaire: voted/did not vote)
    # 1 = Oui (a voté), 2 = Non (n'a pas voté)
    # 8 = N'avait pas le droit de vote, 9 = Ne sait pas

    # Q9A - Participation à une élection passée (type A)
    df_clean['behav_past_election_voted_a'] = df['Q9A'].map({
        1: 1.0,      # Oui, a voté
        2: 0.0,      # Non, n'a pas voté
        8: np.nan,   # N'avait pas droit de vote
        9: np.nan    # Ne sait pas
    })

    # Q9B - Participation à une élection passée (type B)
    df_clean['behav_past_election_voted_b'] = df['Q9B'].map({
        1: 1.0,      # Oui, a voté
        2: 0.0,      # Non, n'a pas voté
        8: np.nan,   # N'avait pas droit de vote
        9: np.nan    # Ne sait pas
    })

    # Q9C - Participation à une élection passée (type C)
    df_clean['behav_past_election_voted_c'] = df['Q9C'].map({
        1: 1.0,      # Oui, a voté
        2: 0.0,      # Non, n'a pas voté
        8: np.nan,   # N'avait pas droit de vote
        9: np.nan    # Ne sait pas
    })

    # Q10A - A voté seul(e) ou accompagné(e)? (Base: votants seulement)
    df_clean['behav_voted_alone_or_accompanied'] = df['Q10A'].map({
        1.0: 'alone',         # Seul(e)
        2.0: 'accompanied',   # Accompagné(e)
        9.0: np.nan           # Préfère ne pas répondre
    })

    # Q10BM1-M5 - Qui a accompagné au vote (multi-réponses, très high missing >75%)
    # SKIP ces variables car:
    # 1. Très peu remplies (>75% missing)
    # 2. Multi-réponses complexes avec valeurs hétérogènes
    # 3. Variables ouvertes associées (Q10BM*O) sont texte libre

    # Q10C - Variable conditionnelle (92.7% missing) - SKIP
    # Q10D - Variable conditionnelle (95.6% missing) - SKIP

    # Q11 - Importance (échelle ordinale 4 niveaux + don't know)
    # Contexte probable: importance du vote ou de la participation électorale
    # Normalisation: 1=Très important → 1.0, 4=Pas du tout important → 0.0
    df_clean['op_importance_voting'] = df['Q11'].map({
        1: 1.0,      # Très important
        2: 0.67,     # Assez important
        3: 0.33,     # Peu important
        4: 0.0,      # Pas du tout important
        5: np.nan    # Je ne sais pas
    })

    # Q12A-Q12B - Échelles d'intérêt (0-10)
    # 0 = Aucun intérêt, 10 = Beaucoup d'intérêt
    # Normalisation: diviser par 10 pour obtenir [0.0, 1.0]

    # Q12A - Niveau d'intérêt (sujet A)
    df_clean['op_interest_level_a'] = df['Q12A'] / 10.0

    # Q12B - Niveau d'intérêt (sujet B)
    df_clean['op_interest_level_b'] = df['Q12B'] / 10.0

    # Q13 - Question binaire (Oui/Non/Ne sais pas)
    # Distribution équilibrée (52% Oui, 40% Non)
    df_clean['behav_generic_binary_q13'] = df['Q13'].map({
        1: 1.0,      # Oui
        2: 0.0,      # Non
        9: np.nan    # Ne sais pas
    })

    return df_clean

# ============================================================================
# LOCAL MODE FUNCTIONS (not used by AWS lambda)
# ============================================================================

def load_data():
    """Charger les données brutes (local mode only)"""
    data_file = RAW_DIR / "data.csv"

    if not data_file.exists():
        raise FileNotFoundError(f"Data file not found: {data_file}")

    print(f"Loading: {data_file}")
    df = pd.read_csv(data_file, encoding='latin-1', sep=';')

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
        "survey": "elxnqc_particip_egp_2018",
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
            "original_variable": f"[RAW_{col}]",
            "missing": int(df_clean[col].isna().sum()),
            "stats": {
                "n": int(len(df_clean)),
                "n_valid": int(df_clean[col].notna().sum())
            }
        }

        # Pour variables catégorielles: ajouter value_counts
        if is_string or (is_numeric and df_clean[col].nunique() <= 20):
            value_counts = df_clean[col].value_counts(dropna=True)
            total_valid = df_clean[col].notna().sum()

            var_info["values"] = {}
            for value, count in value_counts.items():
                var_info["values"][str(value)] = {
                    "count": int(count),
                    "percent": round(float(count) / total_valid * 100, 2) if total_valid > 0 else 0
                }

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
