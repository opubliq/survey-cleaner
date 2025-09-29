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

    # Variable: cps19_demsat -> op_democracy_satisfaction
    # Ordinal satisfaction scale (1=Very satisfied, 4=Not at all satisfied)
    # 5 = Don't know -> NA
    # Scale: 1-4, reversed and normalized to 0-1 (1=very satisfied=1.0, 4=not at all=0.0)
    df_clean['op_democracy_satisfaction'] = df['cps19_demsat'].copy()
    df_clean.loc[df_clean['op_democracy_satisfaction'] == 5.0, 'op_democracy_satisfaction'] = np.nan
    df_clean['op_democracy_satisfaction'] = df_clean['op_democracy_satisfaction'].replace({
        1.0: 1.0,     # Very satisfied -> 1.0
        2.0: 0.667,   # Fairly satisfied -> 0.667
        3.0: 0.333,   # Not very satisfied -> 0.333
        4.0: 0.0      # Not at all satisfied -> 0.0
    })

    # ============================================================================
    # BATCH PROCESSING: Issues, Voting Behavior, Political Interest (30 variables)
    # ============================================================================

    # Variable: cps19_imp_iss -> op_most_important_issue_text
    # Most important issue to respondent (open-ended)
    df_clean['op_most_important_issue_text'] = df['cps19_imp_iss'].astype(str)
    df_clean.loc[df['cps19_imp_iss'].isna(), 'op_most_important_issue_text'] = np.nan

    # Variable: cps19_imp_loc_iss -> op_most_important_local_issue_text
    # Most important local issue (open-ended)
    df_clean['op_most_important_local_issue_text'] = df['cps19_imp_loc_iss'].astype(str)
    df_clean.loc[df['cps19_imp_loc_iss'].isna(), 'op_most_important_local_issue_text'] = np.nan

    # Variable: cps19_imp_iss_party_7_TEXT -> op_important_issue_party_other_text
    # Open-ended "other" specify field
    df_clean['op_important_issue_party_other_text'] = df['cps19_imp_iss_party_7_TEXT'].astype(str)
    df_clean.loc[df['cps19_imp_iss_party_7_TEXT'].isna(), 'op_important_issue_party_other_text'] = np.nan

    # Variable: cps19_imp_loc_iss_p_7_TEXT -> op_important_local_issue_party_other_text
    # Open-ended "other" specify field
    df_clean['op_important_local_issue_party_other_text'] = df['cps19_imp_loc_iss_p_7_TEXT'].astype(str)
    df_clean.loc[df['cps19_imp_loc_iss_p_7_TEXT'].isna(), 'op_important_local_issue_party_other_text'] = np.nan

    # Variable: cps19_votechoice_7_TEXT -> behav_vote_choice_other_text
    # Open-ended "other" specify field
    df_clean['behav_vote_choice_other_text'] = df['cps19_votechoice_7_TEXT'].astype(str)
    df_clean.loc[df['cps19_votechoice_7_TEXT'].isna(), 'behav_vote_choice_other_text'] = np.nan

    # Variable: cps19_votechoice_pr_7_TEXT -> behav_vote_choice_pr_other_text
    # Open-ended "other" specify field
    df_clean['behav_vote_choice_pr_other_text'] = df['cps19_votechoice_pr_7_TEXT'].astype(str)
    df_clean.loc[df['cps19_votechoice_pr_7_TEXT'].isna(), 'behav_vote_choice_pr_other_text'] = np.nan

    # Variable: cps19_vote_unlikely_7_TEXT -> behav_vote_unlikely_other_text
    # Open-ended "other" specify field
    df_clean['behav_vote_unlikely_other_text'] = df['cps19_vote_unlikely_7_TEXT'].astype(str)
    df_clean.loc[df['cps19_vote_unlikely_7_TEXT'].isna(), 'behav_vote_unlikely_other_text'] = np.nan

    # Variable: cps19_vote_unlike_pr_7_TEXT -> behav_vote_unlikely_pr_other_text
    # Open-ended "other" specify field
    df_clean['behav_vote_unlikely_pr_other_text'] = df['cps19_vote_unlike_pr_7_TEXT'].astype(str)
    df_clean.loc[df['cps19_vote_unlike_pr_7_TEXT'].isna(), 'behav_vote_unlikely_pr_other_text'] = np.nan

    # Variable: cps19_v_advance_7_TEXT -> behav_vote_advance_other_text
    # Open-ended "other" specify field
    df_clean['behav_vote_advance_other_text'] = df['cps19_v_advance_7_TEXT'].astype(str)
    df_clean.loc[df['cps19_v_advance_7_TEXT'].isna(), 'behav_vote_advance_other_text'] = np.nan

    # Variable: cps19_vote_lean_7_TEXT -> behav_vote_lean_other_text
    # Open-ended "other" specify field
    df_clean['behav_vote_lean_other_text'] = df['cps19_vote_lean_7_TEXT'].astype(str)
    df_clean.loc[df['cps19_vote_lean_7_TEXT'].isna(), 'behav_vote_lean_other_text'] = np.nan

    # Variable: cps19_vote_lean_pr_7_TEXT -> behav_vote_lean_pr_other_text
    # Open-ended "other" specify field
    df_clean['behav_vote_lean_pr_other_text'] = df['cps19_vote_lean_pr_7_TEXT'].astype(str)
    df_clean.loc[df['cps19_vote_lean_pr_7_TEXT'].isna(), 'behav_vote_lean_pr_other_text'] = np.nan

    # Variable: cps19_2nd_choice_7_TEXT -> behav_second_choice_other_text
    # Open-ended "other" specify field
    df_clean['behav_second_choice_other_text'] = df['cps19_2nd_choice_7_TEXT'].astype(str)
    df_clean.loc[df['cps19_2nd_choice_7_TEXT'].isna(), 'behav_second_choice_other_text'] = np.nan

    # Variable: cps19_2nd_choice_pr_7_TEXT -> behav_second_choice_pr_other_text
    # Open-ended "other" specify field
    df_clean['behav_second_choice_pr_other_text'] = df['cps19_2nd_choice_pr_7_TEXT'].astype(str)
    df_clean.loc[df['cps19_2nd_choice_pr_7_TEXT'].isna(), 'behav_second_choice_pr_other_text'] = np.nan

    # Variable: cps19_not_vote_for_7_TEXT -> behav_not_vote_for_other_text
    # Open-ended "other" specify field
    df_clean['behav_not_vote_for_other_text'] = df['cps19_not_vote_for_7_TEXT'].astype(str)
    df_clean.loc[df['cps19_not_vote_for_7_TEXT'].isna(), 'behav_not_vote_for_other_text'] = np.nan

    # Variable: cps19_interest_gen_1 -> op_political_interest
    # Interest in politics generally (0-10 scale)
    # 0-10 scale normalized to 0-1, with 11 or missing treated as NA
    df_clean['op_political_interest'] = df['cps19_interest_gen_1'].copy()
    df_clean.loc[df_clean['op_political_interest'] > 10, 'op_political_interest'] = np.nan
    df_clean['op_political_interest'] = df_clean['op_political_interest'] / 10.0

    # Variable: cps19_interest_elxn_1 -> op_election_interest
    # Interest in federal election (0-10 scale)
    # 0-10 scale normalized to 0-1, with 11 or missing treated as NA
    df_clean['op_election_interest'] = df['cps19_interest_elxn_1'].copy()
    df_clean.loc[df_clean['op_election_interest'] > 10, 'op_election_interest'] = np.nan
    df_clean['op_election_interest'] = df_clean['op_election_interest'] / 10.0

    # Variable: cps19_imp_iss_party -> op_important_issue_best_party
    # Which party is best at addressing most important issue
    # Party codes: 1=Liberal, 2=Conservative, 3=NDP, 4=Bloc, 5=Green, 6=People's, 7=Other, 9=Don't know
    df_clean['op_important_issue_best_party'] = df['cps19_imp_iss_party'].copy()
    df_clean['op_important_issue_best_party'] = df_clean['op_important_issue_best_party'].replace({
        1.0: 'liberal_party_canada',
        2.0: 'conservative_party_canada',
        3.0: 'new_democratic_party',
        4.0: 'bloc_quebecois',
        5.0: 'green_party_canada',
        6.0: 'peoples_party_canada',
        7.0: 'other',
        9.0: np.nan  # Don't know/no answer
    })

    # Variable: cps19_imp_loc_iss_p -> op_important_local_issue_best_party
    # Which party is best at addressing local issue
    # Party codes: 1=Liberal, 2=Conservative, 3=NDP, 4=Bloc, 5=Green, 6=People's, 7=Other, 9=Don't know
    df_clean['op_important_local_issue_best_party'] = df['cps19_imp_loc_iss_p'].copy()
    df_clean['op_important_local_issue_best_party'] = df_clean['op_important_local_issue_best_party'].replace({
        1.0: 'liberal_party_canada',
        2.0: 'conservative_party_canada',
        3.0: 'new_democratic_party',
        4.0: 'bloc_quebecois',
        5.0: 'green_party_canada',
        6.0: 'peoples_party_canada',
        7.0: 'other',
        9.0: np.nan  # Don't know/no answer
    })

    # Variable: cps19_votechoice -> behav_vote_choice
    # Vote choice in federal election
    # Party codes: 1=Liberal, 2=Conservative, 3=NDP, 4=Bloc, 5=Green, 6=People's, 7=Other, 9=Don't know
    df_clean['behav_vote_choice'] = df['cps19_votechoice'].copy()
    df_clean['behav_vote_choice'] = df_clean['behav_vote_choice'].replace({
        1.0: 'liberal_party_canada',
        2.0: 'conservative_party_canada',
        3.0: 'new_democratic_party',
        4.0: 'bloc_quebecois',
        5.0: 'green_party_canada',
        6.0: 'peoples_party_canada',
        7.0: 'other',
        9.0: np.nan  # Don't know/no answer
    })

    # Variable: cps19_votechoice_pr -> behav_vote_choice_pr
    # Vote choice in PR system (hypothetical)
    # Party codes: 1=Liberal, 2=Conservative, 3=NDP, 4=Bloc, 5=Green, 6=People's, 7=Other, 9=Don't know
    df_clean['behav_vote_choice_pr'] = df['cps19_votechoice_pr'].copy()
    df_clean['behav_vote_choice_pr'] = df_clean['behav_vote_choice_pr'].replace({
        1.0: 'liberal_party_canada',
        2.0: 'conservative_party_canada',
        3.0: 'new_democratic_party',
        4.0: 'bloc_quebecois',
        5.0: 'green_party_canada',
        6.0: 'peoples_party_canada',
        7.0: 'other',
        9.0: np.nan  # Don't know/no answer
    })

    # Variable: cps19_vote_unlikely -> behav_vote_unlikely_choice
    # Party would vote for if likely to vote
    # Party codes: 1=Liberal, 2=Conservative, 3=NDP, 4=Bloc, 5=Green, 6=People's, 7=Other, 9=Don't know
    df_clean['behav_vote_unlikely_choice'] = df['cps19_vote_unlikely'].copy()
    df_clean['behav_vote_unlikely_choice'] = df_clean['behav_vote_unlikely_choice'].replace({
        1.0: 'liberal_party_canada',
        2.0: 'conservative_party_canada',
        3.0: 'new_democratic_party',
        4.0: 'bloc_quebecois',
        5.0: 'green_party_canada',
        6.0: 'peoples_party_canada',
        7.0: 'other',
        9.0: np.nan  # Don't know/no answer
    })

    # Variable: cps19_vote_unlike_pr -> behav_vote_unlikely_pr_choice
    # Party would vote for in PR (if unlikely)
    # Party codes: 1=Liberal, 2=Conservative, 3=NDP, 4=Bloc, 5=Green, 6=People's, 7=Other, 9=Don't know
    df_clean['behav_vote_unlikely_pr_choice'] = df['cps19_vote_unlike_pr'].copy()
    df_clean['behav_vote_unlikely_pr_choice'] = df_clean['behav_vote_unlikely_pr_choice'].replace({
        1.0: 'liberal_party_canada',
        2.0: 'conservative_party_canada',
        3.0: 'new_democratic_party',
        4.0: 'bloc_quebecois',
        5.0: 'green_party_canada',
        6.0: 'peoples_party_canada',
        7.0: 'other',
        9.0: np.nan  # Don't know/no answer
    })

    # Variable: cps19_v_advance -> behav_advance_vote_choice
    # Party voted for in advance voting
    # Party codes: 1=Liberal, 2=Conservative, 3=NDP, 4=Bloc, 5=Green, 6=People's, 7=Other, 9=Don't know
    df_clean['behav_advance_vote_choice'] = df['cps19_v_advance'].copy()
    df_clean['behav_advance_vote_choice'] = df_clean['behav_advance_vote_choice'].replace({
        1.0: 'liberal_party_canada',
        2.0: 'conservative_party_canada',
        3.0: 'new_democratic_party',
        4.0: 'bloc_quebecois',
        5.0: 'green_party_canada',
        6.0: 'peoples_party_canada',
        7.0: 'other',
        9.0: np.nan  # Don't know/no answer
    })

    # Variable: cps19_vote_lean -> behav_vote_lean
    # Party respondent leans toward
    # Party codes: 1=Liberal, 2=Conservative, 3=NDP, 4=Bloc, 5=Green, 6=People's, 7=Other, 9=Don't know
    df_clean['behav_vote_lean'] = df['cps19_vote_lean'].copy()
    df_clean['behav_vote_lean'] = df_clean['behav_vote_lean'].replace({
        1.0: 'liberal_party_canada',
        2.0: 'conservative_party_canada',
        3.0: 'new_democratic_party',
        4.0: 'bloc_quebecois',
        5.0: 'green_party_canada',
        6.0: 'peoples_party_canada',
        7.0: 'other',
        9.0: np.nan  # Don't know/no answer
    })

    # Variable: cps19_vote_lean_pr -> behav_vote_lean_pr
    # Party respondent leans toward (PR)
    # Party codes: 1=Liberal, 2=Conservative, 3=NDP, 4=Bloc, 5=Green, 6=People's, 7=Other, 9=Don't know
    df_clean['behav_vote_lean_pr'] = df['cps19_vote_lean_pr'].copy()
    df_clean['behav_vote_lean_pr'] = df_clean['behav_vote_lean_pr'].replace({
        1.0: 'liberal_party_canada',
        2.0: 'conservative_party_canada',
        3.0: 'new_democratic_party',
        4.0: 'bloc_quebecois',
        5.0: 'green_party_canada',
        6.0: 'peoples_party_canada',
        7.0: 'other',
        9.0: np.nan  # Don't know/no answer
    })

    # Variable: cps19_2nd_choice -> behav_second_choice_party
    # Second choice party
    # Party codes: 1=Liberal, 2=Conservative, 3=NDP, 4=Bloc, 5=Green, 6=People's, 7=Other, 9=Don't know
    df_clean['behav_second_choice_party'] = df['cps19_2nd_choice'].copy()
    df_clean['behav_second_choice_party'] = df_clean['behav_second_choice_party'].replace({
        1.0: 'liberal_party_canada',
        2.0: 'conservative_party_canada',
        3.0: 'new_democratic_party',
        4.0: 'bloc_quebecois',
        5.0: 'green_party_canada',
        6.0: 'peoples_party_canada',
        7.0: 'other',
        9.0: np.nan  # Don't know/no answer
    })

    # Variable: cps19_2nd_choice_pr -> behav_second_choice_party_pr
    # Second choice party (PR)
    # Party codes: 1=Liberal, 2=Conservative, 3=NDP, 4=Bloc, 5=Green, 6=People's, 7=Other, 9=Don't know
    df_clean['behav_second_choice_party_pr'] = df['cps19_2nd_choice_pr'].copy()
    df_clean['behav_second_choice_party_pr'] = df_clean['behav_second_choice_party_pr'].replace({
        1.0: 'liberal_party_canada',
        2.0: 'conservative_party_canada',
        3.0: 'new_democratic_party',
        4.0: 'bloc_quebecois',
        5.0: 'green_party_canada',
        6.0: 'peoples_party_canada',
        7.0: 'other',
        9.0: np.nan  # Don't know/no answer
    })

    # Variable: cps19_v_likely -> behav_vote_likelihood
    # Likelihood of voting (1=certain, 7=certain not to vote)
    # 1-5 scale (1=certain to vote, 5=certain not to vote), 6=ineligible, 7=don't know
    # Normalize to 0-1 (reverse: 1=certain to vote=1.0, 5=certain not to=0.0)
    df_clean['behav_vote_likelihood'] = df['cps19_v_likely'].copy()
    df_clean.loc[df_clean['behav_vote_likelihood'].isin([6.0, 7.0]), 'behav_vote_likelihood'] = np.nan
    df_clean['behav_vote_likelihood'] = df_clean['behav_vote_likelihood'].replace({
        1.0: 1.0,      # Certain to vote
        2.0: 0.75,
        3.0: 0.5,
        4.0: 0.25,
        5.0: 0.0       # Certain not to vote
    })

    # Variable: cps19_v_likely_pr -> behav_vote_likelihood_pr
    # Likelihood of voting in PR system
    # 1-5 scale (1=certain to vote, 5=certain not to vote), 6=ineligible, 7=don't know
    # Normalize to 0-1 (reverse: 1=certain to vote=1.0, 5=certain not to=0.0)
    df_clean['behav_vote_likelihood_pr'] = df['cps19_v_likely_pr'].copy()
    df_clean.loc[df_clean['behav_vote_likelihood_pr'].isin([6.0, 7.0]), 'behav_vote_likelihood_pr'] = np.nan
    df_clean['behav_vote_likelihood_pr'] = df_clean['behav_vote_likelihood_pr'].replace({
        1.0: 1.0,      # Certain to vote
        2.0: 0.75,
        3.0: 0.5,
        4.0: 0.25,
        5.0: 0.0       # Certain not to vote
    })

    # Variable: cps19_fed_gov_sat -> op_federal_government_satisfaction
    # Satisfaction with federal government (1=very satisfied, 4=very dissatisfied, 5=don't know)
    # Normalized to 0-1 (reversed: 1=very satisfied=1.0, 4=very dissatisfied=0.0)
    df_clean['op_federal_government_satisfaction'] = df['cps19_fed_gov_sat'].copy()
    df_clean.loc[df_clean['op_federal_government_satisfaction'] == 5.0, 'op_federal_government_satisfaction'] = np.nan
    df_clean['op_federal_government_satisfaction'] = df_clean['op_federal_government_satisfaction'].replace({
        1.0: 1.0,       # Very satisfied
        2.0: 0.667,     # Fairly satisfied
        3.0: 0.333,     # Not very satisfied
        4.0: 0.0        # Not at all satisfied
    })

    # ============================================================================
    # BATCH 1: Open-text overflow fields (mostly empty, <0.1% filled)
    # ============================================================================

    # Variable: cps199 -> op_most_important_issue_overflow1
    # Overflow text field for most important issue (continuation of text response)
    df_clean['op_most_important_issue_overflow1'] = df['cps199'].copy()
    df_clean.loc[df_clean['op_most_important_issue_overflow1'] == '', 'op_most_important_issue_overflow1'] = np.nan

    # Variable: cps19a -> op_most_important_issue_overflow2
    # Overflow text field for most important issue (continuation of text response)
    df_clean['op_most_important_issue_overflow2'] = df['cps19a'].copy()
    df_clean.loc[df_clean['op_most_important_issue_overflow2'] == '', 'op_most_important_issue_overflow2'] = np.nan

    # Variable: cps19b -> op_most_important_issue_overflow3
    # Overflow text field for most important issue (continuation of text response)
    df_clean['op_most_important_issue_overflow3'] = df['cps19b'].copy()
    df_clean.loc[df_clean['op_most_important_issue_overflow3'] == '', 'op_most_important_issue_overflow3'] = np.nan

    # Variable: cps19c -> op_most_important_issue_overflow4
    # Overflow text field for most important issue (continuation of text response)
    df_clean['op_most_important_issue_overflow4'] = df['cps19c'].copy()
    df_clean.loc[df_clean['op_most_important_issue_overflow4'] == '', 'op_most_important_issue_overflow4'] = np.nan

    # Variable: cps19d -> op_most_important_issue_overflow5
    # Overflow text field for most important issue (continuation of text response)
    df_clean['op_most_important_issue_overflow5'] = df['cps19d'].copy()
    df_clean.loc[df_clean['op_most_important_issue_overflow5'] == '', 'op_most_important_issue_overflow5'] = np.nan

    # Variable: cps198 -> op_party_best_issue_other_text
    # Open text: "Another party" specification for party best addressing most important issue
    df_clean['op_party_best_issue_other_text'] = df['cps198'].copy()
    df_clean.loc[df_clean['op_party_best_issue_other_text'] == '', 'op_party_best_issue_other_text'] = np.nan

    # Variable: cps195 -> op_most_important_local_issue_overflow1
    # Overflow text field for most important local issue (continuation of text response)
    df_clean['op_most_important_local_issue_overflow1'] = df['cps195'].copy()
    df_clean.loc[df_clean['op_most_important_local_issue_overflow1'] == '', 'op_most_important_local_issue_overflow1'] = np.nan

    # Variable: cps196 -> op_most_important_local_issue_overflow2
    # Overflow text field for most important local issue (continuation of text response)
    df_clean['op_most_important_local_issue_overflow2'] = df['cps196'].copy()
    df_clean.loc[df_clean['op_most_important_local_issue_overflow2'] == '', 'op_most_important_local_issue_overflow2'] = np.nan

    # Variable: cps197 -> op_most_important_local_issue_overflow3
    # Overflow text field for most important local issue (continuation of text response)
    df_clean['op_most_important_local_issue_overflow3'] = df['cps197'].copy()
    df_clean.loc[df_clean['op_most_important_local_issue_overflow3'] == '', 'op_most_important_local_issue_overflow3'] = np.nan

    # Variable: cps194 -> op_party_best_local_issue_other_text
    # Open text: "Another party" specification for party best addressing local issue
    df_clean['op_party_best_local_issue_other_text'] = df['cps194'].copy()
    df_clean.loc[df_clean['op_party_best_local_issue_other_text'] == '', 'op_party_best_local_issue_other_text'] = np.nan

    # ============================================================================
    # BATCH 2: Parties would absolutely NOT vote for (binary indicators)
    # ============================================================================
    # These are checkbox selections: 1.0 = selected (would NOT vote), NaN = not selected
    # Convert to binary: 1 = would NOT vote for this party, 0 = could vote for this party

    # Variable: cps19_not_vote_for_1 -> behav_not_vote_liberal
    # Binary: Would absolutely not vote for Liberal Party
    df_clean['behav_not_vote_liberal'] = df['cps19_not_vote_for_1'].copy()
    df_clean['behav_not_vote_liberal'] = df_clean['behav_not_vote_liberal'].fillna(0).astype(int)

    # Variable: cps19_not_vote_for_2 -> behav_not_vote_conservative
    # Binary: Would absolutely not vote for Conservative Party
    df_clean['behav_not_vote_conservative'] = df['cps19_not_vote_for_2'].copy()
    df_clean['behav_not_vote_conservative'] = df_clean['behav_not_vote_conservative'].fillna(0).astype(int)

    # Variable: cps19_not_vote_for_3 -> behav_not_vote_ndp
    # Binary: Would absolutely not vote for NDP
    df_clean['behav_not_vote_ndp'] = df['cps19_not_vote_for_3'].copy()
    df_clean['behav_not_vote_ndp'] = df_clean['behav_not_vote_ndp'].fillna(0).astype(int)

    # Variable: cps19_not_vote_for_4 -> behav_not_vote_bloc
    # Binary: Would absolutely not vote for Bloc Québécois
    df_clean['behav_not_vote_bloc'] = df['cps19_not_vote_for_4'].copy()
    df_clean['behav_not_vote_bloc'] = df_clean['behav_not_vote_bloc'].fillna(0).astype(int)

    # Variable: cps19_not_vote_for_5 -> behav_not_vote_green
    # Binary: Would absolutely not vote for Green Party
    df_clean['behav_not_vote_green'] = df['cps19_not_vote_for_5'].copy()
    df_clean['behav_not_vote_green'] = df_clean['behav_not_vote_green'].fillna(0).astype(int)

    # Variable: cps19_not_vote_for_6 -> behav_not_vote_peoples
    # Binary: Would absolutely not vote for People's Party
    df_clean['behav_not_vote_peoples'] = df['cps19_not_vote_for_6'].copy()
    df_clean['behav_not_vote_peoples'] = df_clean['behav_not_vote_peoples'].fillna(0).astype(int)

    # Variable: cps19_not_vote_for_7 -> behav_not_vote_other_party
    # Binary: Would absolutely not vote for another party (specified in text field)
    df_clean['behav_not_vote_other_party'] = df['cps19_not_vote_for_7'].copy()
    df_clean['behav_not_vote_other_party'] = df_clean['behav_not_vote_other_party'].fillna(0).astype(int)

    # Variable: cps19_not_vote_for_8 -> behav_could_vote_any_party
    # Binary: Could vote for any of the parties (no exclusions)
    df_clean['behav_could_vote_any_party'] = df['cps19_not_vote_for_8'].copy()
    df_clean['behav_could_vote_any_party'] = df_clean['behav_could_vote_any_party'].fillna(0).astype(int)

    # Variable: cps19_not_vote_for_9 -> behav_not_vote_dont_know
    # Binary: Don't know / Prefer not to answer which parties would not vote for
    df_clean['behav_not_vote_dont_know'] = df['cps19_not_vote_for_9'].copy()
    df_clean['behav_not_vote_dont_know'] = df_clean['behav_not_vote_dont_know'].fillna(0).astype(int)

    # ============================================================================
    # BATCH 3: Party and Leader Feeling Thermometers (0-100 scales -> 0-1)
    # ============================================================================
    # All feeling thermometers are 0-100 scales, normalized to 0-1
    # Missing values (NaN) kept as NaN

    # Variable: cps19_party_rating_23 -> op_party_rating_liberal
    # Feeling thermometer for Liberal Party (0-100 -> 0-1)
    df_clean['op_party_rating_liberal'] = df['cps19_party_rating_23'].copy() / 100.0

    # Variable: cps19_party_rating_24 -> op_party_rating_conservative
    # Feeling thermometer for Conservative Party (0-100 -> 0-1)
    df_clean['op_party_rating_conservative'] = df['cps19_party_rating_24'].copy() / 100.0

    # Variable: cps19_party_rating_25 -> op_party_rating_ndp
    # Feeling thermometer for NDP (0-100 -> 0-1)
    df_clean['op_party_rating_ndp'] = df['cps19_party_rating_25'].copy() / 100.0

    # Variable: cps19_party_rating_26 -> op_party_rating_bloc
    # Feeling thermometer for Bloc Québécois (0-100 -> 0-1)
    df_clean['op_party_rating_bloc'] = df['cps19_party_rating_26'].copy() / 100.0

    # Variable: cps19_party_rating_27 -> op_party_rating_green
    # Feeling thermometer for Green Party (0-100 -> 0-1)
    df_clean['op_party_rating_green'] = df['cps19_party_rating_27'].copy() / 100.0

    # Variable: cps19_party_rating_28 -> op_party_rating_peoples
    # Feeling thermometer for People's Party (0-100 -> 0-1)
    df_clean['op_party_rating_peoples'] = df['cps19_party_rating_28'].copy() / 100.0

    # Variable: cps19_lead_rating_23 -> op_leader_rating_trudeau
    # Feeling thermometer for Justin Trudeau (0-100 -> 0-1)
    df_clean['op_leader_rating_trudeau'] = df['cps19_lead_rating_23'].copy() / 100.0

    # Variable: cps19_lead_rating_24 -> op_leader_rating_scheer
    # Feeling thermometer for Andrew Scheer (0-100 -> 0-1)
    df_clean['op_leader_rating_scheer'] = df['cps19_lead_rating_24'].copy() / 100.0

    # Variable: cps19_lead_rating_25 -> op_leader_rating_singh
    # Feeling thermometer for Jagmeet Singh (0-100 -> 0-1)
    df_clean['op_leader_rating_singh'] = df['cps19_lead_rating_25'].copy() / 100.0

    # Variable: cps19_lead_rating_26 -> op_leader_rating_blanchet
    # Feeling thermometer for Yves-François Blanchet (0-100 -> 0-1)
    df_clean['op_leader_rating_blanchet'] = df['cps19_lead_rating_26'].copy() / 100.0

    # Variable: cps19_lead_rating_27 -> op_leader_rating_may
    # Feeling thermometer for Elizabeth May (0-100 -> 0-1)
    df_clean['op_leader_rating_may'] = df['cps19_lead_rating_27'].copy() / 100.0

    # Variable: cps19_lead_rating_28 -> op_leader_rating_bernier
    # Feeling thermometer for Maxime Bernier (0-100 -> 0-1)
    df_clean['op_leader_rating_bernier'] = df['cps19_lead_rating_28'].copy() / 100.0

    # ============================================================================
    # BATCH 4: Local Candidate Feeling Thermometers (0-100 scales -> 0-1)
    # ============================================================================

    # Variable: cps19_cand_rating_23 -> op_candidate_rating_liberal
    # Feeling thermometer for local Liberal candidate (0-100 -> 0-1)
    df_clean['op_candidate_rating_liberal'] = df['cps19_cand_rating_23'].copy() / 100.0

    # Variable: cps19_cand_rating_24 -> op_candidate_rating_conservative
    # Feeling thermometer for local Conservative candidate (0-100 -> 0-1)
    df_clean['op_candidate_rating_conservative'] = df['cps19_cand_rating_24'].copy() / 100.0

    # Variable: cps19_cand_rating_25 -> op_candidate_rating_ndp
    # Feeling thermometer for local NDP candidate (0-100 -> 0-1)
    df_clean['op_candidate_rating_ndp'] = df['cps19_cand_rating_25'].copy() / 100.0

    # Variable: cps19_cand_rating_26 -> op_candidate_rating_bloc
    # Feeling thermometer for local Bloc Québécois candidate (0-100 -> 0-1)
    df_clean['op_candidate_rating_bloc'] = df['cps19_cand_rating_26'].copy() / 100.0

    # Variable: cps19_cand_rating_27 -> op_candidate_rating_green
    # Feeling thermometer for local Green candidate (0-100 -> 0-1)
    df_clean['op_candidate_rating_green'] = df['cps19_cand_rating_27'].copy() / 100.0

    # Variable: cps19_cand_rating_28 -> op_candidate_rating_peoples
    # Feeling thermometer for local People's Party candidate (0-100 -> 0-1)
    df_clean['op_candidate_rating_peoples'] = df['cps19_cand_rating_28'].copy() / 100.0

    # ============================================================================
    # BATCH 5: Left-Right Ideological Scales (0-10 scales -> 0-1)
    # ============================================================================
    # All LR scales are 0-10 (0=left, 10=right), normalized to 0-1

    # Variable: cps19_lr_scale_bef_1 -> op_ideology_self_placement
    # Self-placement on left-right scale (0-10 -> 0-1)
    df_clean['op_ideology_self_placement'] = df['cps19_lr_scale_bef_1'].copy() / 10.0

    # Variable: cps19_lr_parties_1 -> op_ideology_liberal
    # Placement of Liberal Party on left-right scale (0-10 -> 0-1)
    df_clean['op_ideology_liberal'] = df['cps19_lr_parties_1'].copy() / 10.0

    # Variable: cps19_lr_parties_2 -> op_ideology_conservative
    # Placement of Conservative Party on left-right scale (0-10 -> 0-1)
    df_clean['op_ideology_conservative'] = df['cps19_lr_parties_2'].copy() / 10.0

    # Variable: cps19_lr_parties_3 -> op_ideology_ndp
    # Placement of NDP on left-right scale (0-10 -> 0-1)
    df_clean['op_ideology_ndp'] = df['cps19_lr_parties_3'].copy() / 10.0

    # Variable: cps19_lr_parties_4 -> op_ideology_bloc
    # Placement of Bloc Québécois on left-right scale (0-10 -> 0-1)
    df_clean['op_ideology_bloc'] = df['cps19_lr_parties_4'].copy() / 10.0

    # Variable: cps19_lr_parties_5 -> op_ideology_green
    # Placement of Green Party on left-right scale (0-10 -> 0-1)
    df_clean['op_ideology_green'] = df['cps19_lr_parties_5'].copy() / 10.0

    # Variable: cps19_lr_parties_6 -> op_ideology_peoples
    # Placement of People's Party on left-right scale (0-10 -> 0-1)
    df_clean['op_ideology_peoples'] = df['cps19_lr_parties_6'].copy() / 10.0

    # Variable: cps19_lr_scale_aft_1 -> op_ideology_self_placement_post
    # Self-placement on left-right scale (post-election, 0-10 -> 0-1)
    df_clean['op_ideology_self_placement_post'] = df['cps19_lr_scale_aft_1'].copy() / 10.0

    # ============================================================================
    # BATCH 6: Leader Intelligence Perceptions (binary indicators)
    # ============================================================================
    # Checkbox selections: 1.0 = leader perceived as intelligent, NaN = not selected
    # Convert to binary: 1 = intelligent, 0 = not selected

    # Variable: cps19_lead_int_113 -> op_leader_intelligent_trudeau
    # Binary: Justin Trudeau perceived as intelligent
    df_clean['op_leader_intelligent_trudeau'] = df['cps19_lead_int_113'].copy()
    df_clean['op_leader_intelligent_trudeau'] = df_clean['op_leader_intelligent_trudeau'].fillna(0).astype(int)

    # Variable: cps19_lead_int_114 -> op_leader_intelligent_scheer
    # Binary: Andrew Scheer perceived as intelligent
    df_clean['op_leader_intelligent_scheer'] = df['cps19_lead_int_114'].copy()
    df_clean['op_leader_intelligent_scheer'] = df_clean['op_leader_intelligent_scheer'].fillna(0).astype(int)

    # Variable: cps19_lead_int_115 -> op_leader_intelligent_singh
    # Binary: Jagmeet Singh perceived as intelligent
    df_clean['op_leader_intelligent_singh'] = df['cps19_lead_int_115'].copy()
    df_clean['op_leader_intelligent_singh'] = df_clean['op_leader_intelligent_singh'].fillna(0).astype(int)

    # Variable: cps19_lead_int_116 -> op_leader_intelligent_blanchet
    # Binary: Yves-François Blanchet perceived as intelligent
    df_clean['op_leader_intelligent_blanchet'] = df['cps19_lead_int_116'].copy()
    df_clean['op_leader_intelligent_blanchet'] = df_clean['op_leader_intelligent_blanchet'].fillna(0).astype(int)

    # Variable: cps19_lead_int_117 -> op_leader_intelligent_may
    # Binary: Elizabeth May perceived as intelligent
    df_clean['op_leader_intelligent_may'] = df['cps19_lead_int_117'].copy()
    df_clean['op_leader_intelligent_may'] = df_clean['op_leader_intelligent_may'].fillna(0).astype(int)

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