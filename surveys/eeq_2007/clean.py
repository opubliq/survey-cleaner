#!/usr/bin/env python3
"""
Script de nettoyage pour eeq_2007 (Quebec Election Study 2007)

DUAL-MODE SCRIPT:
  - AWS Mode: Exposé via clean_data(df) pour pipeline_sondages lambda
  - Local Mode: Exécution standalone via python clean.py

AWS Integration:
    La fonction clean_data(df) est appelée par lambda_raffineur_nettoyage
    qui charge les données depuis S3 et gère l'export vers Parquet.

Local Usage:
    python surveys/eeq_2007/clean.py

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

    # ============================================================================
    # IDENTIFIANTS ET PONDÉRATIONS
    # ============================================================================

    # quest → id_respondent: Unique respondent identifier
    df_clean['id_respondent'] = df['quest'].copy()

    # pond → weight_main: Survey weight
    df_clean['weight_main'] = df['pond'].copy()

    # ============================================================================
    # VARIABLES SOCIO-DÉMOGRAPHIQUES (ses_)
    # ============================================================================

    # q76 → ses_gender: Gender (1=male, 2=female)
    df_clean['ses_gender'] = df['q76'].map({
        1.0: 'male',
        2.0: 'female'
    })

    # q75 → ses_age: Age calculated from birth year
    # Survey done in 2007, so age = 2007 - birth_year
    current_year = 2007
    df_clean['ses_age'] = current_year - df['q75']
    # Set invalid ages (< 18 or > 100) to NaN
    df_clean.loc[(df_clean['ses_age'] < 18) | (df_clean['ses_age'] > 100), 'ses_age'] = np.nan

    # ses_age_category: Age in categories
    df_clean['ses_age_category'] = pd.cut(
        df_clean['ses_age'],
        bins=[0, 25, 35, 45, 55, 65, 150],
        labels=['18_24', '25_34', '35_44', '45_54', '55_64', '65_plus']
    ).astype(str)
    df_clean.loc[df_clean['ses_age_category'] == 'nan', 'ses_age_category'] = np.nan

    # langu → ses_language: Language spoken
    # Based on distribution: 1=French (1883), 2=English (164), 3=Other...
    df_clean['ses_language'] = df['langu'].map({
        1.0: 'french',
        2.0: 'english',
        3.0: 'other',
        4.0: 'other',
        5.0: 'other',
        6.0: 'other',
        7.0: 'other',
        9.0: np.nan  # Don't know / Refused
    })

    # ethn1 → ses_ethnicity: Ethnicity/Origin
    # 1 is dominant (1971), likely Canadian/Québécois
    # Keeping as numeric for now - would need codebook for exact mapping
    df_clean['ses_ethnicity'] = df['ethn1'].map({
        1.0: 'canadian_quebecois',
        2.0: 'other_european',
        3.0: 'other_european',
        4.0: 'other_european',
        5.0: 'other_european',
        6.0: 'other_european',
        7.0: 'other_european',
        8.0: 'other',
        9.0: 'other',
        10.0: 'other',
        11.0: 'other',
        12.0: 'other',
        13.0: 'other',
        96.0: np.nan,  # Other
        98.0: np.nan   # Refused
    })

    # q77 → ses_education: Education level (COHÉRENCE AVEC EGM 2021)
    # Simplified to 5 categories to match reference survey
    df_clean['ses_education'] = df['q77'].map({
        2.0: 'elementary',
        3.0: 'elementary',
        4.0: 'high_school',      # Combined: some + completed
        5.0: 'high_school',
        6.0: 'college_cegep',    # Combined: some college + cegep
        7.0: 'college_cegep',
        8.0: 'bachelor',         # Combined: some university + bachelor
        9.0: 'bachelor',
        10.0: 'graduate',
        11.0: 'graduate',
        98.0: np.nan,
        99.0: np.nan
    })

    # q78 → ses_income_household: Household income (COHÉRENCE AVEC EGM 2021)
    # Regrouping into 8 categories to match reference survey
    # Note: EEQ q78 value 9 maps to 100k-150k range (cannot split further without data)
    df_clean['ses_income_household'] = df['q78'].map({
        1.0: 'under_20k',       # Combined: under_10k
        2.0: 'under_20k',       # Combined: 10k_to_20k
        3.0: '20k_to_40k',      # Combined: 20k_to_30k
        4.0: '20k_to_40k',      # Combined: 30k_to_40k
        5.0: '40k_to_60k',      # Combined: 40k_to_50k
        6.0: '40k_to_60k',      # Combined: 50k_to_60k
        7.0: '60k_to_80k',
        8.0: '80k_to_100k',
        9.0: '100k_to_120k',    # Mapping to lower bound for consistency
        10.0: 'over_150k',
        98.0: np.nan,
        99.0: np.nan
    })

    # q79 → ses_occupation: Main occupation (COHÉRENCE AVEC EGM 2021)
    # Mapping professional -> employed to match reference survey
    df_clean['ses_occupation'] = df['q79'].map({
        1.0: 'employed',        # professional → employed
        2.0: 'employed',
        3.0: 'self_employed',
        4.0: 'student',
        5.0: 'retired',
        6.0: 'homemaker',
        7.0: 'unemployed',
        8.0: np.nan,           # Other mapped to NaN for consistency
        9.0: np.nan,
        10.0: np.nan,
        11.0: np.nan,
        96.0: np.nan,
        99.0: np.nan
    })

    # nomx → ses_region: Electoral district/region code
    # 21 unique values - likely electoral districts
    # Keeping as numeric identifier for now
    df_clean['ses_region'] = df['nomx'].copy()

    # q80 → ses_born_canada: Born in Canada (COHÉRENCE AVEC EGM 2021)
    # 1.0 = born in Canada, 0.0 = not born (standard convention)
    # Based on distribution: 1=191, 2=1931 → 2 is "born in Canada"
    df_clean['ses_born_canada'] = df['q80'].map({
        1.0: 0.0,  # Not born in Canada
        2.0: 1.0,  # Born in Canada (matches EGM: 1.0 = yes)
        4.0: np.nan,
        5.0: np.nan,
        6.0: np.nan,
        8.0: np.nan,
        9.0: np.nan,
        10.0: np.nan,
        12.0: np.nan,
        15.0: np.nan,
        96.0: np.nan,
        99.0: np.nan
    })

    # q81 → ses_marital_status: Marital status
    # 5 categories: 1=188, 2=101, 3=142, 4=556, 5=1155
    df_clean['ses_marital_status'] = df['q81'].map({
        1.0: 'single',
        2.0: 'married',
        3.0: 'common_law',
        4.0: 'divorced_separated',
        5.0: 'widowed',
        98.0: np.nan,
        99.0: np.nan
    })

    # q66 → ses_union_member: Union membership
    # Binary: 1=1229, 2=598 (typical yes/no pattern)
    df_clean['ses_union_member'] = df['q66'].map({
        1.0: 1.0,  # Yes, union member
        2.0: 0.0,  # No
        8.0: np.nan,
        9.0: np.nan
    })

    # q67 → ses_household_size: Number of people in household
    # 4 categories: 1=209, 2=461, 3=673, 4=635
    df_clean['ses_household_size'] = df['q67'].map({
        1.0: '1_person',
        2.0: '2_persons',
        3.0: '3_4_persons',
        4.0: '5_plus_persons',
        8.0: np.nan,
        9.0: np.nan
    })

    # q68 → ses_homeowner: Home ownership (COHÉRENCE AVEC EGM 2021)
    # Binary: homeowner (1.0) vs non-homeowner (0.0) to match reference survey
    df_clean['ses_homeowner'] = df['q68'].map({
        1.0: 1.0,  # Own/homeowner
        2.0: 0.0,  # Rent
        3.0: 0.0,  # Other (not homeowner)
        4.0: 0.0,  # Other (not homeowner)
        8.0: np.nan,
        9.0: np.nan
    })

    # q69 → ses_children_home: Children living at home
    # 4 categories: 1=1005, 2=720, 3=276, 4=115
    df_clean['ses_children_home'] = df['q69'].map({
        1.0: 'no_children',
        2.0: 'children_under_18',
        3.0: 'children_18_plus',
        4.0: 'both',
        8.0: np.nan,
        9.0: np.nan
    })

    # q70 → ses_religion: Religious affiliation
    # Multiple categories: 1-5 (main religions), 96/97/98/99
    df_clean['ses_religion'] = df['q70'].map({
        1.0: 'catholic',
        2.0: 'protestant',
        3.0: 'other_christian',
        4.0: 'other_religion',
        5.0: 'no_religion',
        96.0: np.nan,
        97.0: np.nan,  # No religion / atheist
        98.0: np.nan,  # Don't know
        99.0: np.nan   # Refused
    })

    # q71 → ses_religiosity: Importance of religion
    # 3 categories: 1=349, 2=1064, 3=336 (likely: very/somewhat/not important)
    # Only 1770 responses (conditional on having religion?)
    df_clean['ses_religiosity'] = df['q71'].map({
        1.0: 1.0,    # Very important
        2.0: 0.5,    # Somewhat important
        3.0: 0.0,    # Not important
        8.0: np.nan,
        9.0: np.nan
    })

    # q74 → ses_region_administrative: Administrative region of Quebec
    # Multiple categories (1-7, 96/98/99)
    # This appears to be Quebec administrative regions
    df_clean['ses_region_administrative'] = df['q74'].map({
        1.0: 'montreal',
        2.0: 'quebec_city',
        3.0: 'outaouais',
        4.0: 'other_regions',
        5.0: 'eastern_quebec',
        6.0: 'monteregie',
        7.0: 'other',
        96.0: np.nan,
        98.0: np.nan,
        99.0: np.nan
    })

    # type → tech_sample_type: Type of sample (technical variable)
    df_clean['tech_sample_type'] = df['type'].map({
        1.0: 'type_1',
        2.0: 'type_2'
    })

    # q72 → ses_spouse_union_member: Spouse union membership (conditional)
    # Only 401 responses (conditional on being married/common-law)
    df_clean['ses_spouse_union_member'] = df['q72'].map({
        1.0: 1.0,  # Yes
        2.0: 0.0,  # No
        8.0: np.nan,
        9.0: np.nan
    })

    # q73 → ses_number_jobs: Number of jobs (conditional, very few responses)
    # Only 139 responses - skipping or keeping minimal
    # Skipping due to low response rate

    # ============================================================================
    # VARIABLES D'OPINION ET ATTITUDES (op_) - Échelles ordinales
    # ============================================================================
    # q2-q7 appear to be 4-point scales (1-4) with 8=DK, 9=Refused
    # Normalizing to [0, 1] where 1 = most positive/agreement

    # q2 → op_interest_politics: Interest in politics
    # Assuming 1=Very interested → 1.0, 4=Not interested → 0.0
    df_clean['op_interest_politics'] = df['q2'].map({
        1.0: 1.0,    # Very interested
        2.0: 0.67,   # Somewhat interested
        3.0: 0.33,   # Not very interested
        4.0: 0.0,    # Not interested at all
        8.0: np.nan, # Don't know
        9.0: np.nan  # Refused
    })

    # q3 → op_follow_campaign: How closely followed the campaign
    df_clean['op_follow_campaign'] = df['q3'].map({
        1.0: 1.0,    # Very closely
        2.0: 0.67,   # Fairly closely
        3.0: 0.33,   # Not very closely
        4.0: 0.0,    # Not at all
        8.0: np.nan,
        9.0: np.nan
    })

    # q4 → op_care_election_outcome: Care who wins election
    df_clean['op_care_election_outcome'] = df['q4'].map({
        1.0: 1.0,    # Great deal
        2.0: 0.67,   # Somewhat
        3.0: 0.33,   # Not much
        4.0: 0.0,    # Not at all
        8.0: np.nan,
        9.0: np.nan
    })

    # q5 → op_satisfaction_democracy: Satisfaction with democracy
    df_clean['op_satisfaction_democracy'] = df['q5'].map({
        1.0: 1.0,    # Very satisfied
        2.0: 0.67,   # Fairly satisfied
        3.0: 0.33,   # Not very satisfied
        4.0: 0.0,    # Not satisfied at all
        8.0: np.nan,
        9.0: np.nan
    })

    # q6 → op_trust_government: Trust in government
    df_clean['op_trust_government'] = df['q6'].map({
        1.0: 1.0,    # Always / Most of the time
        2.0: 0.67,   # Some of the time
        3.0: 0.33,   # Rarely
        4.0: 0.0,    # Never
        8.0: np.nan,
        9.0: np.nan
    })

    # q7 → op_political_efficacy: Feeling that politics too complicated
    # Note: This is reverse coded - higher = less efficacy
    df_clean['op_politics_too_complicated'] = df['q7'].map({
        1.0: 1.0,    # Strongly agree (politics IS complicated)
        2.0: 0.67,   # Agree
        3.0: 0.33,   # Disagree
        4.0: 0.0,    # Strongly disagree (politics NOT complicated)
        8.0: np.nan,
        9.0: np.nan
    })

    # ============================================================================
    # VARIABLES DE COMPORTEMENT ÉLECTORAL (behav_)
    # ============================================================================

    # q11 → behav_vote_turnout: Did you vote in the 2007 provincial election?
    # 1=1990 (yes), 2=172 (no) - clear voting participation
    df_clean['behav_vote_turnout_2007'] = df['q11'].map({
        1.0: 1.0,  # Yes, voted
        2.0: 0.0,  # No, did not vote
        8.0: np.nan,
        9.0: np.nan
    })

    # q16 → behav_vote_choice_provincial: Which party voted for (provincial 2007)
    # Based on 2007 Quebec election: PLQ, PQ, ADQ were main parties
    df_clean['behav_vote_choice_provincial'] = df['q16'].map({
        1.0: 'plq',   # Parti libéral du Québec (Jean Charest)
        2.0: 'pq',    # Parti Québécois (André Boisclair)
        3.0: 'adq',   # Action démocratique du Québec (Mario Dumont)
        4.0: 'qs',    # Québec solidaire
        5.0: 'pvq',   # Parti vert du Québec
        6.0: 'other',
        7.0: 'other',
        8.0: np.nan,  # Don't know
        9.0: np.nan,  # Refused
        96.0: np.nan,
        97.0: np.nan,
        98.0: np.nan,
        99.0: np.nan
    })

    # q17 → behav_vote_choice_federal: Which party would vote for (federal)
    df_clean['behav_vote_choice_federal'] = df['q17'].map({
        1.0: 'liberal',
        2.0: 'conservative',
        3.0: 'ndp',
        4.0: 'bloc',
        5.0: 'green',
        6.0: 'other',
        7.0: 'other',
        8.0: np.nan,
        9.0: np.nan,
        96.0: np.nan,
        97.0: np.nan,
        98.0: np.nan
    })

    # q8 → behav_vote_certainty: How certain about vote choice
    df_clean['behav_vote_certainty'] = df['q8'].map({
        1.0: 1.0,    # Absolutely certain
        2.0: 0.67,   # Fairly certain
        3.0: 0.33,   # Not very certain
        4.0: 0.0,    # Not certain at all
        8.0: np.nan,
        9.0: np.nan
    })

    # q9 → behav_vote_decision_timing: When decided how to vote
    df_clean['behav_vote_decision_timing'] = df['q9'].map({
        1.0: 1.0,    # Long before campaign
        2.0: 0.75,   # Early in campaign
        3.0: 0.5,    # During campaign
        4.0: 0.0,    # On election day
        8.0: np.nan,
        9.0: np.nan
    })

    # q10 → behav_vote_change_mind: Considered voting for another party
    df_clean['behav_vote_considered_other_party'] = df['q10'].map({
        1.0: 1.0,    # Yes, seriously considered
        2.0: 0.67,   # Yes, somewhat considered
        3.0: 0.33,   # Thought about it briefly
        4.0: 0.0,    # No, never
        8.0: np.nan,
        9.0: np.nan
    })

    # q10b → behav_interest_campaign: How interesting was the campaign
    df_clean['behav_campaign_interest'] = df['q10b'].map({
        1.0: 1.0,    # Very interesting
        2.0: 0.67,   # Fairly interesting
        3.0: 0.33,   # Not very interesting
        4.0: 0.0,    # Not interesting at all
        8.0: np.nan,
        9.0: np.nan
    })

    # q19 → behav_vote_frequency: Frequency of voting in elections
    df_clean['behav_vote_frequency'] = df['q19'].map({
        1.0: 1.0,    # Always vote
        2.0: 0.5,    # Sometimes vote
        3.0: 0.0,    # Rarely/never vote
        8.0: np.nan,
        9.0: np.nan
    })

    # q21 → behav_party_contact: Contacted by political party during campaign
    df_clean['behav_contacted_by_party'] = df['q21'].map({
        1.0: 1.0,    # Yes, multiple times
        2.0: 0.67,   # Yes, once or twice
        3.0: 0.33,   # Maybe/not sure
        4.0: 0.0,    # No
        8.0: np.nan,
        9.0: np.nan
    })

    # q22 → behav_campaign_participation: Tried to convince others
    df_clean['behav_tried_convince_others'] = df['q22'].map({
        1.0: 1.0,    # Yes, often
        2.0: 0.67,   # Yes, occasionally
        3.0: 0.33,   # Once or twice
        4.0: 0.0,    # No
        8.0: np.nan,
        9.0: np.nan
    })

    # q23 → behav_campaign_activities: Attended political meetings/rallies
    df_clean['behav_attended_political_events'] = df['q23'].map({
        1.0: 1.0,    # Yes, several
        2.0: 0.67,   # Yes, one or two
        3.0: 0.33,   # Thought about it
        4.0: 0.0,    # No
        8.0: np.nan,
        9.0: np.nan
    })

    # q24 → behav_political_donation: Made political donation
    df_clean['behav_political_donation'] = df['q24'].map({
        1.0: 1.0,    # Yes
        2.0: 0.0,    # No
        3.0: np.nan, # Maybe/uncertain
        8.0: np.nan,
        9.0: np.nan
    })

    # q25 → behav_sign_petition: Signed petition in past year
    df_clean['behav_signed_petition'] = df['q25'].map({
        1.0: 1.0,    # Yes
        2.0: 0.0,    # No
        3.0: np.nan, # Maybe
        8.0: np.nan,
        9.0: np.nan
    })

    # q26 → behav_boycott: Boycotted products for political reasons
    df_clean['behav_boycott_products'] = df['q26'].map({
        1.0: 1.0,  # Yes
        2.0: 0.0,  # No
        8.0: np.nan,
        9.0: np.nan
    })

    # q27 → behav_protest: Participated in demonstration/protest
    df_clean['behav_protest_participation'] = df['q27'].map({
        1.0: 1.0,    # Yes, several
        2.0: 0.67,   # Yes, one or two
        3.0: 0.33,   # Thought about it
        4.0: 0.0,    # No
        8.0: np.nan,
        9.0: np.nan
    })

    # q33 → behav_union_household: Anyone in household member of union
    df_clean['behav_union_household'] = df['q33'].map({
        1.0: 1.0,  # Yes
        2.0: 0.0,  # No
        8.0: np.nan,
        9.0: np.nan
    })

    # q12 → behav_party_identification: Which party feel closest to (provincial)
    df_clean['behav_party_identification_provincial'] = df['q12'].map({
        1.0: 'plq',
        2.0: 'pq',
        3.0: 'adq',
        4.0: 'qs',
        5.0: 'other',
        95.0: np.nan,  # None
        96.0: np.nan,
        97.0: np.nan,
        98.0: np.nan,
        99.0: np.nan
    })

    # q13 → behav_party_identification_federal: Which party feel closest to (federal)
    df_clean['behav_party_identification_federal'] = df['q13'].map({
        1.0: 'liberal',
        2.0: 'conservative',
        3.0: 'ndp',
        4.0: 'bloc',
        5.0: 'green',
        95.0: np.nan,
        96.0: np.nan,
        97.0: np.nan,
        98.0: np.nan,
        99.0: np.nan
    })

    # ============================================================================
    # THERMOMÈTRES (op_rating_*) - Échelles 0-100 normalisées à 0-1
    # ============================================================================
    # Codes spéciaux: 997/998/999 = don't know/refused/not applicable → NaN
    # Normalisation: valeur / 100.0 pour ramener à [0, 1]

    def normalize_thermometer(series):
        """Normalize 0-100 thermometer to 0-1, treating 997+ as NaN"""
        result = pd.Series(np.nan, index=series.index)
        valid_mask = (series >= 0) & (series <= 100)
        result.loc[valid_mask] = series.loc[valid_mask] / 100.0
        return result

    # q28-q32 → Thermomètres de leaders/partis (probablement Charest, Boisclair, Dumont, etc.)
    df_clean['op_rating_leader_1'] = normalize_thermometer(df['q28'])
    df_clean['op_rating_leader_2'] = normalize_thermometer(df['q29'])
    df_clean['op_rating_leader_3'] = normalize_thermometer(df['q30'])
    df_clean['op_rating_leader_4'] = normalize_thermometer(df['q31'])
    df_clean['op_rating_leader_5'] = normalize_thermometer(df['q32'])

    # q39-q43 → Thermomètres additionnels (partis ou leaders fédéraux probablement)
    df_clean['op_rating_entity_1'] = normalize_thermometer(df['q39'])
    df_clean['op_rating_entity_2'] = normalize_thermometer(df['q40'])
    df_clean['op_rating_entity_3'] = normalize_thermometer(df['q41'])
    df_clean['op_rating_entity_4'] = normalize_thermometer(df['q42'])
    df_clean['op_rating_entity_5'] = normalize_thermometer(df['q43'])

    # q64-q65 → Thermomètres (probablement institutions ou autres entités)
    df_clean['op_rating_institution_1'] = normalize_thermometer(df['q64'])
    df_clean['op_rating_institution_2'] = normalize_thermometer(df['q65'])

    # ============================================================================
    # OPINIONS ET ATTITUDES (op_) - Échelles ordinales normalisées
    # ============================================================================

    # q34 → op_sovereignty: Position on Quebec sovereignty
    # Binary question (1=Yes, 2=No) based on distribution
    df_clean['op_sovereignty'] = df['q34'].map({
        1.0: 1.0,  # Yes/Favor sovereignty
        2.0: 0.0,  # No/Against sovereignty
        8.0: np.nan,
        9.0: np.nan
    })

    # q35 → op_referendum_vote: How would vote in sovereignty referendum
    # Binary (1=Yes, 2=No)
    df_clean['op_referendum_vote'] = df['q35'].map({
        1.0: 1.0,  # Would vote Yes
        2.0: 0.0,  # Would vote No
        8.0: np.nan,
        9.0: np.nan
    })

    # q35a → op_referendum_certainty: Certainty about referendum vote
    df_clean['op_referendum_certainty'] = df['q35a'].map({
        1.0: 1.0,    # Very certain
        2.0: 0.67,   # Fairly certain
        3.0: 0.33,   # Not very certain
        4.0: 0.0,    # Not certain at all
        8.0: np.nan,
        9.0: np.nan
    })

    # q36-q38 → Positions on various issues (4-point scales)
    df_clean['op_issue_position_1'] = df['q36'].map({
        1.0: 1.0, 2.0: 0.67, 3.0: 0.33, 4.0: 0.0, 8.0: np.nan, 9.0: np.nan
    })

    df_clean['op_issue_position_2'] = df['q37'].map({
        1.0: 1.0, 2.0: 0.67, 3.0: 0.33, 4.0: 0.0, 8.0: np.nan, 9.0: np.nan
    })

    df_clean['op_issue_position_3'] = df['q38'].map({
        1.0: 1.0, 2.0: 0.67, 3.0: 0.33, 4.0: 0.0, 8.0: np.nan, 9.0: np.nan
    })

    # q47-q54 → Series of political attitudes (4-point agree/disagree scales)
    df_clean['op_attitude_1'] = df['q47'].map({
        1.0: 1.0, 2.0: 0.67, 3.0: 0.33, 4.0: 0.0, 8.0: np.nan, 9.0: np.nan
    })

    df_clean['op_attitude_2'] = df['q48'].map({
        1.0: 1.0, 2.0: 0.67, 3.0: 0.33, 4.0: 0.0, 8.0: np.nan, 9.0: np.nan
    })

    df_clean['op_voting_duty'] = df['q49'].map({
        1.0: 1.0,    # Strongly agree voting is duty
        2.0: 0.67,
        3.0: 0.33,
        8.0: np.nan,
        9.0: np.nan
    })

    df_clean['op_attitude_4'] = df['q50'].map({
        1.0: 1.0, 2.0: 0.67, 3.0: 0.33, 4.0: 0.0, 8.0: np.nan, 9.0: np.nan
    })

    df_clean['op_government_responsiveness'] = df['q51'].map({
        1.0: 1.0, 2.0: 0.67, 3.0: 0.33, 4.0: 0.0, 8.0: np.nan, 9.0: np.nan
    })

    df_clean['op_mps_lose_touch'] = df['q52'].map({
        1.0: 1.0, 2.0: 0.67, 3.0: 0.33, 4.0: 0.0, 8.0: np.nan, 9.0: np.nan
    })

    df_clean['op_attitude_7'] = df['q53'].map({
        1.0: 1.0, 2.0: 0.67, 3.0: 0.33, 4.0: 0.0, 8.0: np.nan, 9.0: np.nan
    })

    df_clean['op_attitude_8'] = df['q54'].map({
        1.0: 1.0, 2.0: 0.67, 3.0: 0.33, 4.0: 0.0, 8.0: np.nan, 9.0: np.nan
    })

    # q55-q62 → More political attitudes (multi-point scales with 97/98/99 codes)
    # Mapping higher values to higher agreement for consistency
    def map_opinion_scale(series):
        """Map opinion scales 1-6 to 0-1, treating 96+ as NaN"""
        return series.map({
            1.0: 1.0, 2.0: 0.8, 3.0: 0.6, 4.0: 0.4, 5.0: 0.2, 6.0: 0.0,
            96.0: np.nan, 97.0: np.nan, 98.0: np.nan, 99.0: np.nan
        })

    df_clean['op_government_intervention'] = map_opinion_scale(df['q55'])
    df_clean['op_left_right_position'] = map_opinion_scale(df['q56'])
    df_clean['op_redistribution'] = map_opinion_scale(df['q57'])
    df_clean['op_environment_economy'] = map_opinion_scale(df['q58'])
    df_clean['op_attitude_minorities'] = map_opinion_scale(df['q59'])
    df_clean['op_immigration_level'] = map_opinion_scale(df['q60'])
    df_clean['op_attitude_13'] = map_opinion_scale(df['q61a'])
    df_clean['op_attitude_14'] = map_opinion_scale(df['q61b'])
    df_clean['op_attitude_15'] = map_opinion_scale(df['q61c'])
    df_clean['op_attitude_16'] = map_opinion_scale(df['q61d'])
    df_clean['op_attitude_17'] = map_opinion_scale(df['q62'])

    # q44-q46 → Issue importance or priority rankings
    df_clean['op_issue_importance_1'] = df['q44'].map({
        1.0: 1.0, 2.0: 0.83, 3.0: 0.67, 4.0: 0.5, 5.0: 0.33, 6.0: 0.17, 7.0: 0.0,
        98.0: np.nan, 99.0: np.nan
    })

    df_clean['op_issue_importance_2'] = df['q45'].map({
        1.0: 1.0, 2.0: 0.83, 3.0: 0.67, 4.0: 0.5, 5.0: 0.33, 6.0: 0.17, 7.0: 0.0,
        98.0: np.nan, 99.0: np.nan
    })

    df_clean['op_issue_importance_3'] = df['q46'].map({
        1.0: 1.0, 2.0: 0.83, 3.0: 0.67, 4.0: 0.5, 5.0: 0.33, 6.0: 0.17, 7.0: 0.0,
        98.0: np.nan, 99.0: np.nan
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
        "survey": "eeq_2007",
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
