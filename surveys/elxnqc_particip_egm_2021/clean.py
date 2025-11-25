#!/usr/bin/env python3
"""
Script de nettoyage pour elxnqc_particip_egm_2021

DUAL-MODE SCRIPT:
  - AWS Mode: Exposé via clean_data(df) pour pipeline_sondages lambda
  - Local Mode: Exécution standalone via python clean.py

AWS Integration:
    La fonction clean_data(df) est appelée par lambda_raffineur_nettoyage
    qui charge les données depuis S3 et gère l'export vers Parquet.

Local Usage:
    python surveys/elxnqc_particip_egm_2021/clean.py

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

    # caseid → id_respondent: Unique respondent identifier
    df_clean['id_respondent'] = df['caseid'].copy()

    # regio → ses_region_administrative: Administrative region of Quebec
    df_clean['ses_region_administrative'] = df['regio'].map({
        1.0: 'bas_saint_laurent',
        2.0: 'saguenay_lac_saint_jean',
        3.0: 'capitale_nationale',
        4.0: 'mauricie',
        5.0: 'estrie',
        6.0: 'montreal',
        7.0: 'outaouais',
        8.0: 'abitibi_temiscamingue',
        9.0: 'cote_nord',
        10.0: 'nord_du_quebec',
        11.0: 'gaspesie_iles_de_la_madeleine',
        12.0: 'chaudiere_appalaches',
        13.0: 'laval',
        14.0: 'lanaudiere',
        15.0: 'laurentides',
        16.0: 'monteregie',
        17.0: 'centre_du_quebec'
    })

    # age → ses_age_category: Age category (categorical)
    # Note: Original variable is already categorized, not continuous
    # Mapping based on standard Quebec survey age categories
    df_clean['ses_age_category'] = df['age'].map({
        1.0: '18_24',    # 18-24 ans
        2.0: '25_34',    # 25-34 ans
        3.0: '35_44',    # 35-44 ans
        4.0: '45_54',    # 45-54 ans
        5.0: '55_64',    # 55-64 ans
        6.0: '65_plus'   # 65 ans et plus
    })

    # q1 → behav_vote_turnout_municipal_2021: Voting turnout in Nov 7, 2021 municipal election
    df_clean['behav_vote_turnout_municipal_2021'] = df['q1'].map({
        1.0: 'voted',
        2.0: 'did_not_vote',
        3.0: 'not_eligible'
    })

    # q2 → behav_vote_method: How did you vote? (Base: voters only)
    df_clean['behav_vote_method'] = df['q2'].map({
        1.0: 'in_person',
        2.0: 'by_mail'
    })

    # q3a → op_covid_measures_easy_to_understand: COVID safety instructions were easy to understand (Base: voted in person)
    # Ordinal scale normalized to [0,1]: 1=Strongly agree → 1.0, 4=Strongly disagree → 0.0
    df_clean['op_covid_measures_easy_to_understand'] = df['q3a'].map({
        1.0: 1.0,    # Tout à fait d'accord
        2.0: 0.67,   # Plutôt d'accord
        3.0: 0.33,   # Plutôt en désaccord
        4.0: 0.0     # Tout à fait en désaccord
    })

    # q3b → op_covid_measures_reassuring: COVID safety measures were reassuring (Base: voted in person)
    # Ordinal scale normalized to [0,1]: 1=Strongly agree → 1.0, 4=Strongly disagree → 0.0
    df_clean['op_covid_measures_reassuring'] = df['q3b'].map({
        1.0: 1.0,    # Tout à fait d'accord
        2.0: 0.67,   # Plutôt d'accord
        3.0: 0.33,   # Plutôt en désaccord
        4.0: 0.0     # Tout à fait en désaccord
    })

    # q4 → op_voting_ease: Was it easy or difficult to vote? (Base: voters only)
    # Ordinal scale normalized to [0,1]: 1=Very easy → 1.0, 4=Very difficult → 0.0
    df_clean['op_voting_ease'] = df['q4'].map({
        1.0: 1.0,    # Très facile
        2.0: 0.67,   # Plutôt facile
        3.0: 0.33,   # Plutôt difficile
        4.0: 0.0     # Très difficile
    })

    # q5a-q5i → Reasons for not voting (Base: non-voters only)
    # Binary: 1=Yes this reason played a role, 0=No

    # q5a → op_reason_not_vote_no_interest: No interest in municipal politics
    df_clean['op_reason_not_vote_no_interest'] = df['q5a'].map({
        1.0: 1.0,  # Oui
        2.0: 0.0   # Non
    })

    # q5b → op_reason_not_vote_lack_info: Lacked information about issues/candidates
    df_clean['op_reason_not_vote_lack_info'] = df['q5b'].map({
        1.0: 1.0,
        2.0: 0.0
    })

    # q5c → op_reason_not_vote_disliked_candidates: Disliked all candidates/parties
    df_clean['op_reason_not_vote_disliked_candidates'] = df['q5c'].map({
        1.0: 1.0,
        2.0: 0.0
    })

    # q5d → op_reason_not_vote_not_concerned: Not concerned by campaign issues
    df_clean['op_reason_not_vote_not_concerned'] = df['q5d'].map({
        1.0: 1.0,
        2.0: 0.0
    })

    # q5e → op_reason_not_vote_no_impact: Vote would not make a difference
    df_clean['op_reason_not_vote_no_impact'] = df['q5e'].map({
        1.0: 1.0,
        2.0: 0.0
    })

    # q5f → op_reason_not_vote_lost_trust: Lost trust in politicians/politics
    df_clean['op_reason_not_vote_lost_trust'] = df['q5f'].map({
        1.0: 1.0,
        2.0: 0.0
    })

    # q5g → op_reason_not_vote_too_busy: Too busy
    df_clean['op_reason_not_vote_too_busy'] = df['q5g'].map({
        1.0: 1.0,
        2.0: 0.0
    })

    # q5h → op_reason_not_vote_away: Away from home/city
    df_clean['op_reason_not_vote_away'] = df['q5h'].map({
        1.0: 1.0,
        2.0: 0.0
    })

    # q5i → op_reason_not_vote_covid_concern: Concerned about COVID situation
    df_clean['op_reason_not_vote_covid_concern'] = df['q5i'].map({
        1.0: 1.0,
        2.0: 0.0
    })

    # ============================================================================
    # DEMOGRAPHIC VARIABLES
    # ============================================================================

    # sexe → ses_gender: Gender
    df_clean['ses_gender'] = df['sexe'].map({
        1.0: 'male',
        2.0: 'female',
        3.0: 'other',
        9.0: np.nan  # Prefer not to answer
    })

    # langm → ses_language_home: Language spoken most often at home
    df_clean['ses_language_home'] = df['langm'].map({
        1.0: 'french',
        2.0: 'english',
        3.0: 'other'
    })

    # orig → ses_born_canada: Born in Canada
    df_clean['ses_born_canada'] = df['orig'].map({
        1.0: 1.0,  # Yes, born in Canada
        2.0: 0.0,  # No, born elsewhere
        9.0: np.nan
    })

    # scol → ses_education: Highest level of education completed
    df_clean['ses_education'] = df['scol'].map({
        1.0: 'elementary',
        2.0: 'high_school',
        3.0: 'college_cegep',
        4.0: 'bachelor',
        5.0: 'graduate',  # Masters/PhD
        9.0: np.nan
    })

    # occup → ses_occupation: Main occupation in last 12 months
    df_clean['ses_occupation'] = df['occup'].map({
        1.0: 'employed',
        2.0: 'self_employed',
        3.0: 'retired',
        4.0: 'student',
        5.0: 'homemaker',
        6.0: 'unemployed',
        9.0: np.nan
    })

    # reven → ses_income_household: Household annual income before tax
    df_clean['ses_income_household'] = df['reven'].map({
        1.0: 'under_20k',
        2.0: '20k_to_40k',
        3.0: '40k_to_60k',
        4.0: '60k_to_80k',
        5.0: '80k_to_100k',
        6.0: '100k_to_120k',
        7.0: '120k_to_150k',
        8.0: 'over_150k',
        98.0: np.nan,  # Prefer not to answer
        99.0: np.nan   # Don't know
    })

    # menag → ses_household_type: Household composition type
    df_clean['ses_household_type'] = df['menag'].map({
        1.0: 'single_no_children',
        2.0: 'couple_no_children',
        3.0: 'couple_with_children',
        4.0: 'single_parent',
        5.0: 'multigenerational',
        6.0: 'other',
        9.0: np.nan
    })

    # ============================================================================
    # WEIGHTS
    # ============================================================================

    # pond17 → weight_standard: Standard weight (not accounting for turnout)
    df_clean['weight_standard'] = df['pond17'].copy()

    # pondalt → weight_turnout_adjusted: Alternative weight (adjusted for turnout by municipality size)
    df_clean['weight_turnout_adjusted'] = df['pondalt'].copy()

    # ============================================================================
    # BINARY VARIABLES (YES/NO)
    # ============================================================================

    # q5j → op_reason_not_vote_other: Other reason for not voting (Base: non-voters)
    df_clean['op_reason_not_vote_other'] = df['q5j'].map({
        1.0: 1.0,  # Yes
        2.0: 0.0   # No
    })

    # q13 → behav_contacted_by_campaign: Contacted by party/candidate during campaign
    df_clean['behav_contacted_by_campaign'] = df['q13'].map({
        1.0: 1.0,  # Yes
        2.0: 0.0   # No
    })

    # q23 → ses_homeowner: Home ownership
    df_clean['ses_homeowner'] = df['q23'].map({
        1.0: 1.0,  # Yes, homeowner
        2.0: 0.0   # No, renter/other
    })

    # q24 → behav_considered_running: Ever considered running for municipal office
    df_clean['behav_considered_running'] = df['q24'].map({
        1.0: 1.0,  # Yes
        2.0: 0.0   # No
    })

    # ============================================================================
    # ORDINAL OPINION/BEHAVIOR VARIABLES
    # ============================================================================

    # Knowledge of candidates
    # q6a → op_knowledge_candidates_names: Knew names of mayoral candidates
    df_clean['op_knowledge_candidates_names'] = df['q6a'].map({
        1.0: 1.0,    # Yes, all or most
        2.0: 0.5,    # Yes, some
        3.0: 0.0     # No
    })

    # q6b → op_knowledge_candidates_platforms: Knew platforms/projects of candidates
    df_clean['op_knowledge_candidates_platforms'] = df['q6b'].map({
        1.0: 1.0,    # Yes, well
        2.0: 0.5,    # Yes, somewhat
        3.0: 0.0     # No
    })

    # q7 → op_closeness_to_party: Felt close to a municipal party/team
    df_clean['op_closeness_to_party'] = df['q7'].map({
        1.0: 1.0,    # Yes, very close
        2.0: 0.67,   # Yes, somewhat close
        3.0: 0.33,   # Not very close
        4.0: 0.0,    # Not close at all
        9.0: np.nan  # Don't know
    })

    # q8/q8x → op_campaign_finance_rules_adequate: Campaign finance rules are adequate (skip - mostly don't know)
    # Skipping q8/q8x due to 48% don't know

    # q9 → op_satisfaction_democracy_municipal: Satisfaction with how democracy works in municipality
    df_clean['op_satisfaction_democracy_municipal'] = df['q9'].map({
        1.0: 1.0,    # Very satisfied
        2.0: 0.67,   # Somewhat satisfied
        3.0: 0.33,   # Not very satisfied
        4.0: 0.0     # Not satisfied at all
    })

    # Political efficacy/trust (q10a-e) - 4-point agree/disagree scale
    # q10a → op_council_too_complicated: Council functioning is too complicated to understand
    df_clean['op_council_too_complicated'] = df['q10a'].map({
        1.0: 1.0,    # Strongly agree
        2.0: 0.67,   # Somewhat agree
        3.0: 0.33,   # Somewhat disagree
        4.0: 0.0     # Strongly disagree
    })

    # q10b → op_council_not_concerned_citizens: Municipal officials don't care about ordinary people
    df_clean['op_council_not_concerned_citizens'] = df['q10b'].map({
        1.0: 1.0,
        2.0: 0.67,
        3.0: 0.33,
        4.0: 0.0
    })

    # q10c → op_trust_council: Can trust municipal council most of the time
    df_clean['op_trust_council'] = df['q10c'].map({
        1.0: 1.0,
        2.0: 0.67,
        3.0: 0.33,
        4.0: 0.0
    })

    # q10d → op_citizens_can_influence: Citizens can influence council decisions
    df_clean['op_citizens_can_influence'] = df['q10d'].map({
        1.0: 1.0,
        2.0: 0.67,
        3.0: 0.33,
        4.0: 0.0
    })

    # q10e → op_elected_reflect_diversity: Elected officials reflect municipality's diversity
    df_clean['op_elected_reflect_diversity'] = df['q10e'].map({
        1.0: 1.0,
        2.0: 0.67,
        3.0: 0.33,
        4.0: 0.0
    })

    # q11 → op_council_decisions_impact: Impact of council decisions on respondent
    df_clean['op_council_decisions_impact'] = df['q11'].map({
        1.0: 1.0,    # A lot
        2.0: 0.67,   # Somewhat
        3.0: 0.33,   # Not much
        4.0: 0.0     # Not at all
    })

    # Skipping q12_m1-m8 (information sources - multi-response with high missing)

    # q14 → op_interest_municipal_politics: Interest in municipal politics
    df_clean['op_interest_municipal_politics'] = df['q14'].map({
        1.0: 1.0,    # Very interested
        2.0: 0.67,   # Somewhat interested
        3.0: 0.33,   # Not very interested
        4.0: 0.0     # Not interested at all
    })

    # q15 → behav_vote_frequency_history: Historical voting frequency (all elections)
    df_clean['behav_vote_frequency_history'] = df['q15'].map({
        1.0: 1.0,    # Always
        2.0: 0.67,   # Often
        3.0: 0.33,   # Sometimes
        4.0: 0.0     # Rarely/never
    })

    # q16 → op_voting_duty_vs_choice: Voting as duty vs choice
    df_clean['op_voting_duty_vs_choice'] = df['q16'].map({
        1.0: 'duty',
        2.0: 'choice',
        9.0: np.nan
    })

    # Perceptions of voting (q17a-c) - 4-point agree/disagree
    # q17a → op_vote_makes_difference: My vote can make a difference
    df_clean['op_vote_makes_difference'] = df['q17a'].map({
        1.0: 1.0,
        2.0: 0.67,
        3.0: 0.33,
        4.0: 0.0
    })

    # q17b → op_voting_makes_proud: Voting makes me proud
    df_clean['op_voting_makes_proud'] = df['q17b'].map({
        1.0: 1.0,
        2.0: 0.67,
        3.0: 0.33,
        4.0: 0.0
    })

    # q17c → op_voting_important_to_others: Voting is important to family/friends
    df_clean['op_voting_important_to_others'] = df['q17c'].map({
        1.0: 1.0,
        2.0: 0.67,
        3.0: 0.33,
        4.0: 0.0
    })

    # q18 → op_frequency_discuss_politics: How often discuss municipal politics
    df_clean['op_frequency_discuss_politics'] = df['q18'].map({
        1.0: 1.0,    # Very often
        2.0: 0.67,   # Often
        3.0: 0.33,   # Rarely
        4.0: 0.0     # Never
    })

    # q19 → behav_volunteering_past_year: Volunteered in past 12 months
    df_clean['behav_volunteering_past_year'] = df['q19'].map({
        1.0: 'regularly',
        2.0: 'occasionally',
        3.0: 'never',
        9.0: np.nan
    })

    # q20 → behav_civic_participation: Civic participation in past 12 months
    df_clean['behav_civic_participation'] = df['q20'].map({
        1.0: 1.0,  # Yes
        2.0: 0.0,  # No
        9.0: np.nan
    })

    # q21 → op_sense_of_belonging: Sense of belonging to municipality
    df_clean['op_sense_of_belonging'] = df['q21'].map({
        1.0: 1.0,    # Very strong
        2.0: 0.67,   # Somewhat strong
        3.0: 0.33,   # Somewhat weak
        4.0: 0.0     # Very weak
    })

    # q22 → ses_years_in_municipality: How long lived in municipality
    df_clean['ses_years_in_municipality'] = df['q22'].map({
        1.0: 'under_5_years',
        2.0: '5_to_10_years',
        3.0: '11_to_20_years',
        4.0: 'over_20_years'
    })

    # Barriers to running for office (q25a-e) - 4-point agree/disagree
    # q25a → op_barrier_running_salary: Salary not high enough
    df_clean['op_barrier_running_salary'] = df['q25a'].map({
        1.0: 1.0,
        2.0: 0.67,
        3.0: 0.33,
        4.0: 0.0
    })

    # q25b → op_barrier_running_workload: Workload too important
    df_clean['op_barrier_running_workload'] = df['q25b'].map({
        1.0: 1.0,
        2.0: 0.67,
        3.0: 0.33,
        4.0: 0.0
    })

    # q25c → op_barrier_running_recognition: Little recognition for the function
    df_clean['op_barrier_running_recognition'] = df['q25c'].map({
        1.0: 1.0,
        2.0: 0.67,
        3.0: 0.33,
        4.0: 0.0
    })

    # q25d → op_barrier_running_incumbency: Too difficult to win against incumbents
    df_clean['op_barrier_running_incumbency'] = df['q25d'].map({
        1.0: 1.0,
        2.0: 0.67,
        3.0: 0.33,
        4.0: 0.0
    })

    # q25e → op_barrier_running_harassment: Risk of harassment/intimidation too high
    df_clean['op_barrier_running_harassment'] = df['q25e'].map({
        1.0: 1.0,
        2.0: 0.67,
        3.0: 0.33,
        4.0: 0.0
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
    df = pd.read_csv(data_file)

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
        "survey": "elxnqc_particip_egm_2021",
        "variables": {}
    }

    for col in df_clean.columns:
        # Détection automatique du type
        dtype = df_clean[col].dtype
        is_numeric = pd.api.types.is_numeric_dtype(dtype)
        is_string = pd.api.types.is_string_dtype(dtype) or dtype == 'object'

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
