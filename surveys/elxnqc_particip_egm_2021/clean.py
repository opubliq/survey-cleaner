#!/usr/bin/env python3
"""
Script de nettoyage pour [NOM_SONDAGE]

Ce script est exécuté par lambda_raffineur_nettoyage dans pipeline_sondages.
La lambda appelle:
  - clean_data(df) → retourne DataFrame nettoyé
  - get_metadata() → retourne dictionnaire avec métadonnées du sondage et variables

Les métadonnées enrichies sont sauvegardées comme codebook.json dans S3 et utilisées
par les marts downstream pour l'interprétation sémantique des données.
"""

import pandas as pd
import numpy as np

# ============================================================================
# SURVEY METADATA (à remplir au début du script)
# ============================================================================
# Métadonnées générales du sondage
SURVEY_METADATA = {
    'survey_id': '[SURVEY_ID]',           # ID unique du sondage (ex: "ces2019")
    'title': '[NOM_SONDAGE]',             # Titre complet
    'year': None,                          # Année de collecte
    'description': '',                     # Description du sondage
    'organization': '',                    # Organisation responsable
    'sample_size': None,                   # Taille de l'échantillon
    'language': 'fr',                      # Langue principale
    'methodology': '',                     # Méthodologie (web, téléphone, etc.)
}

# ============================================================================
# CODEBOOK VARIABLES (construit progressivement variable par variable)
# ============================================================================
# Ce dictionnaire accumule les métadonnées pour chaque variable nettoyée.
# Pour chaque variable, ajouter une entrée immédiatement après le code de nettoyage.
#
# Format:
# CODEBOOK_VARIABLES = {
#     'nom_variable_clean': {
#         'original_variable': 'Q1_raw_name',
#         'question_label': "Texte de la question du sondage",
#         'type': 'categorical|likert|numeric|binary',
#         'value_labels': {
#             valeur_cleanée: "Label descriptif",
#             ...
#         }
#     }
# }
#
# Types de variables:
#   - categorical: Variables nominales (province, parti, genre)
#   - likert: Échelles ordinales (satisfaction, accord/désaccord)
#   - numeric: Variables continues normalisées (ratings 0-1)
#   - binary: Variables oui/non
CODEBOOK_VARIABLES = {}


def clean_data(df):
    """Nettoie et standardise les données

    Appelé par lambda_raffineur_nettoyage dans pipeline_sondages.

    Args:
        df (pd.DataFrame): Données brutes chargées depuis Parquet

    Returns:
        pd.DataFrame: Données nettoyées

    Approche: Créer une nouvelle dataframe propre avec seulement les variables
    nettoyées. Les données raw (df) restent intactes.
    """
    # Initialize empty clean dataframe with same index
    df_clean = pd.DataFrame(index=df.index)

    # ========================================================================
    # VARIABLE PROCESSING - Pattern variable par variable
    # ========================================================================
    # Pour chaque variable:
    #   1. Code de nettoyage de la variable
    #   2. Entrée CODEBOOK immédiatement après (question_label + value_labels)
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
    # ========================================================================

    # EXEMPLE 1: Variable catégorielle (province)
    # ------------------------------------------
    # df_clean['ses_province'] = df['Q2_province'].map({
    #     1.0: 'quebec',
    #     2.0: 'ontario',
    #     3.0: 'alberta',
    #     4.0: 'british_columbia'
    # })
    #
    # CODEBOOK_VARIABLES['ses_province'] = {
    #     'original_variable': 'Q2_province',
    #     'question_label': "Dans quelle province habitez-vous?",
    #     'type': 'categorical',
    #     'value_labels': {
    #         'quebec': "Québec",
    #         'ontario': "Ontario",
    #         'alberta': "Alberta",
    #         'british_columbia': "Colombie-Britannique"
    #     }
    # }

    # EXEMPLE 2: Variable catégorielle (choix de vote)
    # ------------------------------------------------
    # df_clean['behav_vote_choice'] = df['Q10_vote'].map({
    #     1.0: 'liberal',
    #     2.0: 'conservative',
    #     3.0: 'ndp',
    #     4.0: 'bloc',
    #     5.0: 'green',
    #     6.0: 'ppc',
    #     7.0: 'other',
    #     99.0: np.nan
    # })
    #
    # CODEBOOK_VARIABLES['behav_vote_choice'] = {
    #     'original_variable': 'Q10_vote',
    #     'question_label': "Si les élections avaient lieu demain, pour quel parti voteriez-vous?",
    #     'type': 'categorical',
    #     'value_labels': {
    #         'liberal': "Parti libéral du Canada",
    #         'conservative': "Parti conservateur du Canada",
    #         'ndp': "Nouveau Parti démocratique",
    #         'bloc': "Bloc Québécois",
    #         'green': "Parti vert du Canada",
    #         'ppc': "Parti populaire du Canada",
    #         'other': "Autre parti"
    #     }
    # }

    # EXEMPLE 3: Variable ordinale (échelle Likert normalisée 0-1)
    # ------------------------------------------------------------
    # df_clean['op_satisfaction_gov'] = df['Q5_satisfaction'].map({
    #     1.0: 1.0,    # Very satisfied
    #     2.0: 0.75,   # Somewhat satisfied
    #     3.0: 0.5,    # Neutral
    #     4.0: 0.25,   # Somewhat dissatisfied
    #     5.0: 0.0,    # Very dissatisfied
    #     99.0: np.nan
    # })
    #
    # CODEBOOK_VARIABLES['op_satisfaction_gov'] = {
    #     'original_variable': 'Q5_satisfaction',
    #     'question_label': "Dans quelle mesure êtes-vous satisfait du gouvernement actuel?",
    #     'type': 'likert',
    #     'value_labels': {
    #         1.0: "Très satisfait",
    #         0.75: "Plutôt satisfait",
    #         0.5: "Neutre",
    #         0.25: "Plutôt insatisfait",
    #         0.0: "Très insatisfait"
    #     }
    # }

    # EXEMPLE 4: Variable numérique (normalisation 0-100 → 0-1)
    # ---------------------------------------------------------
    # df_clean['op_party_rating_liberal'] = np.nan
    # mask = (df['Q15_liberal_rating'] >= 0) & (df['Q15_liberal_rating'] <= 100)
    # df_clean.loc[mask, 'op_party_rating_liberal'] = df.loc[mask, 'Q15_liberal_rating'] / 100.0
    #
    # CODEBOOK_VARIABLES['op_party_rating_liberal'] = {
    #     'original_variable': 'Q15_liberal_rating',
    #     'question_label': "Sur une échelle de 0 à 100, comment évaluez-vous le Parti libéral?",
    #     'type': 'numeric',
    #     'value_labels': {}  # Pas de labels pour variables continues
    # }

    # EXEMPLE 5: Variable démographique (genre)
    # -----------------------------------------
    # df_clean['ses_gender'] = df['Q1_gender'].map({
    #     1.0: 'male',
    #     2.0: 'female',
    #     3.0: 'other',
    #     99.0: np.nan
    # })
    #
    # CODEBOOK_VARIABLES['ses_gender'] = {
    #     'original_variable': 'Q1_gender',
    #     'question_label': "Quel est votre genre?",
    #     'type': 'categorical',
    #     'value_labels': {
    #         'male': "Homme",
    #         'female': "Femme",
    #         'other': "Autre / Non-binaire"
    #     }
    # }

    # ========================================================================
    # TODO: Ajouter le code de nettoyage pour chaque variable ci-dessous
    # Pattern: nettoyage variable → entrée CODEBOOK_VARIABLES → prochaine variable
    # ========================================================================

    # behav_info_source_municipal - Primary information source for municipal election candidates (Q12_M1)
    # Source: q12_m1
    df_clean['behav_info_source_municipal'] = df['q12_m1'].map({
        1.0: 'source_1',
        2.0: 'source_2',
        3.0: 'source_3',
        4.0: 'source_4',
        5.0: 'source_5',
        6.0: 'source_6',
        7.0: 'source_7',
        8.0: 'source_8',
        9.0: 'source_9'
    })

    CODEBOOK_VARIABLES['behav_info_source_municipal'] = {
        'original_variable': 'q12_m1',
        'question_label': "Q12. Quelle(s) ont été vos principales sources d'information à propos des candidat(e)s et de leurs programmes lors des élections municipales du 7 novembre ? Cochez tout ce qui s'applique.",
        'type': 'categorical',
        'value_labels': {
            'source_1': "Source d'information 1",
            'source_2': "Source d'information 2",
            'source_3': "Source d'information 3",
            'source_4': "Source d'information 4",
            'source_5': "Source d'information 5",
            'source_6': "Source d'information 6",
            'source_7': "Source d'information 7",
            'source_8': "Source d'information 8",
            'source_9': "Source d'information 9"
        }
    }

    # op_trust_municipal_council - Trust in municipal council (Likert agreement scale)
    # Source: q10c
    df_clean['op_trust_municipal_council'] = df['q10c'].map({
        1.0: 1.0,    # Tout à fait d'accord
        2.0: 0.67,   # Plutôt d'accord
        3.0: 0.33,   # Plutôt en désaccord
        4.0: 0.0     # Tout à fait en désaccord
    })

    CODEBOOK_VARIABLES['op_trust_municipal_council'] = {
        'original_variable': 'q10c',
        'question_label': "Q10C. La plupart du temps, nous pouvons faire confiance au conseil municipal",
        'type': 'likert',
        'value_labels': {
            1.0: "Tout à fait d'accord",
            0.67: "Plutôt d'accord",
            0.33: "Plutôt en désaccord",
            0.0: "Tout à fait en désaccord"
        }
    }

    # behav_vote_participation - Municipal election voting participation
    # Source: q1
    df_clean['behav_vote_participation'] = df['q1'].map({
        1.0: 'voted',
        2.0: 'intended_to_vote',
        3.0: 'did_not_vote'
    })

    CODEBOOK_VARIABLES['behav_vote_participation'] = {
        'original_variable': 'q1',
        'question_label': "Q1. Les élections municipales ont eu lieu le 7 novembre. Dans toute élection, certaines personnes votent et d'autres ne votent pas. Lequel des choix suivants correspond le mieux à votre situation?",
        'type': 'categorical',
        'value_labels': {
            'voted': "Modalité 1",
            'intended_to_vote': "Modalité 2",
            'did_not_vote': "Modalité 3"
        }
    }

    # ses_region - Administrative region of Quebec
    # Source: regio
    df_clean['ses_region'] = df['regio'].map({
        1.0: 'bas_st_laurent',
        2.0: 'saguenay_lac_st_jean',
        3.0: 'capitale_nationale',
        4.0: 'mauricie',
        5.0: 'estrie',
        6.0: 'montreal',
        7.0: 'outaouais',
        8.0: 'abitibi_temiscamingue',
        9.0: 'cote_nord',
        10.0: 'nord_du_quebec',
        11.0: 'gaspesie_iles_madeleine',
        12.0: 'chaudiere_appalaches',
        13.0: 'laval',
        14.0: 'lanaudiere',
        15.0: 'laurentides',
        16.0: 'monteregie',
        17.0: 'centre_du_quebec'
    })

    CODEBOOK_VARIABLES['ses_region'] = {
        'original_variable': 'regio',
        'question_label': "REGIO. Région administrative",
        'type': 'categorical',
        'value_labels': {
            'bas_st_laurent': "Bas-Saint-Laurent",
            'saguenay_lac_st_jean': "Saguenay–Lac-Saint-Jean",
            'capitale_nationale': "Capitale-Nationale",
            'mauricie': "Mauricie",
            'estrie': "Estrie",
            'montreal': "Montréal",
            'outaouais': "Outaouais",
            'abitibi_temiscamingue': "Abitibi-Témiscamingue",
            'cote_nord': "Côte-Nord",
            'nord_du_quebec': "Nord-du-Québec",
            'gaspesie_iles_madeleine': "Gaspésie–Îles-de-la-Madeleine",
            'chaudiere_appalaches': "Chaudière-Appalaches",
            'laval': "Laval",
            'lanaudiere': "Lanaudière",
            'laurentides': "Laurentides",
            'monteregie': "Montérégie",
            'centre_du_quebec': "Centre-du-Québec"
        }
    }

    # respondent_id - Case identifier / Respondent ID
    # Source: caseid
    df_clean['respondent_id'] = df['caseid'].astype(str)

    CODEBOOK_VARIABLES['respondent_id'] = {
        'original_variable': 'caseid',
        'question_label': "Case identifier / Respondent ID",
        'type': 'identifier',
        'value_labels': {}
    }

    # ses_age_group - Age group categories
    # Source: age
    df_clean['ses_age_group'] = df['age'].map({
        1.0: '18-24',
        2.0: '25-34',
        3.0: '35-44',
        4.0: '45-54',
        5.0: '55-64',
        6.0: '65+'
    })

    CODEBOOK_VARIABLES['ses_age_group'] = {
        'original_variable': 'age',
        'question_label': "À quelle catégorie d'âge appartenez-vous?",
        'type': 'categorical',
        'value_labels': {
            '18-24': "18-24 ans",
            '25-34': "25-34 ans",
            '35-44': "35-44 ans",
            '45-54': "45-54 ans",
            '55-64': "55-64 ans",
            '65+': "65 ans et plus"
        }
    }

    # ses_population - Population size (normalized)
    # Source: popnum
    max_pop = df['popnum'].max()
    df_clean['ses_population'] = df['popnum'] / max_pop

    CODEBOOK_VARIABLES['ses_population'] = {
        'original_variable': 'popnum',
        'question_label': "POPNUM. Population (nombre)",
        'type': 'numeric',
        'value_labels': {}
    }

    # ses_population_quota - Population quota stratum
    # Source: qpop
    df_clean['ses_population_quota'] = df['qpop'].map({
        1.0: 'stratum_1',
        2.0: 'stratum_2',
        3.0: 'stratum_3',
        4.0: 'stratum_4'
    })

    CODEBOOK_VARIABLES['ses_population_quota'] = {
        'original_variable': 'qpop',
        'question_label': "QPOP. Quota population",
        'type': 'categorical',
        'value_labels': {
            'stratum_1': "Modalité 1",
            'stratum_2': "Modalité 2",
            'stratum_3': "Modalité 3",
            'stratum_4': "Modalité 4"
        }
    }

    # ses_region_quota - Regional quota stratum
    # Source: qregiz
    df_clean['ses_region_quota'] = df['qregiz'].map({
        1.0: 'region_group_1',
        2.0: 'region_group_2',
        3.0: 'region_group_3',
        4.0: 'region_group_4',
        5.0: 'region_group_5',
        6.0: 'region_group_6',
        7.0: 'region_group_7',
        8.0: 'region_group_8'
    })

    CODEBOOK_VARIABLES['ses_region_quota'] = {
        'original_variable': 'qregiz',
        'question_label': "QREGIZ. Quota régions",
        'type': 'categorical',
        'value_labels': {
            'region_group_1': "Modalité 1",
            'region_group_2': "Modalité 2",
            'region_group_3': "Modalité 3",
            'region_group_4': "Modalité 4",
            'region_group_5': "Modalité 5",
            'region_group_6': "Modalité 6",
            'region_group_7': "Modalité 7",
            'region_group_8': "Modalité 8"
        }
    }

    # methodological_exclude - Exclusion filter for invalid interviews
    # Source: excl
    df_clean['methodological_exclude'] = df['excl'].map({
        0.0: 'include',
        1.0: 'exclude'
    })

    CODEBOOK_VARIABLES['methodological_exclude'] = {
        'original_variable': 'excl',
        'question_label': "EXCL. Filtre pour exclure n=103 entrevues qui ont été dans des municipalités où aucune élection au poste de maire n'a été tenue.",
        'type': 'binary',
        'value_labels': {
            'include': "Interview à inclure dans l'analyse",
            'exclude': "Interview à exclure (municipalité sans élection mayoral)"
        }
    }

    # behav_vote_municipal - Municipal election voting participation
    # Source: q1x
    df_clean['behav_vote_municipal'] = df['q1x'].map({
        1.0: 'voted',
        2.0: 'eligible_did_not_vote', 
        3.0: 'not_eligible'
    })

    CODEBOOK_VARIABLES['behav_vote_municipal'] = {
        'original_variable': 'q1x',
        'question_label': "Les élections municipales ont eu lieu le 7 novembre. Dans toute élection, certaines personnes votent et d'autres ne votent pas. Lequel des choix suivants correspond le mieux à votre situation?",
        'type': 'categorical',
        'value_labels': {
            'voted': 'A voté',
            'eligible_did_not_vote': 'Éligible mais n\'a pas voté',
            'not_eligible': 'N\'était pas éligible'
        }
    }

    # behav_vote_method - How they voted (binary question for those who voted)
    # Source: q2
    df_clean['behav_vote_method'] = df['q2'].map({
        1.0: 'yes',
        2.0: 'no'
    })

    CODEBOOK_VARIABLES['behav_vote_method'] = {
        'original_variable': 'q2',
        'question_label': "Q2. De quelle façon avez-vous voté? (Base : ont voté)",
        'type': 'binary',
        'value_labels': {
            'yes': "Oui",
            'no': "Non"
        }
    }

    # op_sanitary_measures_clear - Agreement that sanitary measures were easy to understand
    # Source: q3a
    df_clean['op_sanitary_measures_clear'] = df['q3a'].map({
        1.0: 1.0,    # Tout à fait d'accord
        2.0: 0.67,   # Plutôt d'accord
        3.0: 0.33,   # Plutôt en désaccord
        4.0: 0.0     # Tout à fait en désaccord
    })

    CODEBOOK_VARIABLES['op_sanitary_measures_clear'] = {
        'original_variable': 'q3a',
        'question_label': "Q3A. Les consignes sanitaires étaient faciles à comprendre (Dans les bureaux de vote, des mesures sanitaires étaient en place pour assurer votre sécurité. Indiquer si vous êtes plus ou moins en accord avec les affirmations suivantes) (Base : ont voté au bureau de vote)",
        'type': 'likert',
        'value_labels': {
            1.0: "Tout à fait d'accord",
            0.67: "Plutôt d'accord",
            0.33: "Plutôt en désaccord",
            0.0: "Tout à fait en désaccord"
        }
    }

    # op_sanitary_measures_reassuring - Agreement that sanitary measures were reassuring
    # Source: q3b
    df_clean['op_sanitary_measures_reassuring'] = df['q3b'].map({
        1.0: 1.0,    # Tout à fait d'accord
        2.0: 0.67,   # Plutôt d'accord
        3.0: 0.33,   # Plutôt en désaccord
        4.0: 0.0     # Tout à fait en désaccord
    })

    CODEBOOK_VARIABLES['op_sanitary_measures_reassuring'] = {
        'original_variable': 'q3b',
        'question_label': "Q3B. Les mesures sanitaires étaient rassurantes (Dans les bureaux de vote, des mesures sanitaires étaient en place pour assurer votre sécurité. Indiquer si vous êtes plus ou moins en accord avec les affirmations suivantes) (Base : ont voté au bureau de vote)",
        'type': 'likert',
        'value_labels': {
            1.0: "Tout à fait d'accord",
            0.67: "Plutôt d'accord",
            0.33: "Plutôt en désaccord",
            0.0: "Tout à fait en désaccord"
        }
    }

    # op_voting_ease - Ease of voting in municipal election (normalized scale)
    # Source: q4
    df_clean['op_voting_ease'] = df['q4'].map({
        1.0: 1.0,    # Très facile
        2.0: 0.67,   # Plutôt facile
        3.0: 0.33,   # Plutôt difficile
        4.0: 0.0     # Très difficile
    })

    CODEBOOK_VARIABLES['op_voting_ease'] = {
        'original_variable': 'q4',
        'question_label': "Q4. Diriez-vous qu'il était facile ou difficile de voter à cette élection municipale ? (Base : Ont voté)",
        'type': 'likert',
        'value_labels': {
            1.0: "Très facile",
            0.67: "Plutôt facile",
            0.33: "Plutôt difficile",
            0.0: "Très difficile"
        }
    }

    # op_nonvoting_no_interest - No interest in municipal politics as reason for not voting
    # Source: q5a
    df_clean['op_nonvoting_no_interest'] = df['q5a'].map({
        1.0: 'yes',
        2.0: 'no'
    })

    CODEBOOK_VARIABLES['op_nonvoting_no_interest'] = {
        'original_variable': 'q5a',
        'question_label': "Q5A. Je n'ai aucun intérêt pour la politique municipale (Voici différentes raisons pour lesquelles les gens ne votent pas. Indiquez dans chaque cas si la raison a joué un rôle dans votre décision de ne pas voter aux élections municipales du 7 novembre)",
        'type': 'binary',
        'value_labels': {
            'yes': "Oui",
            'no': "Non"
        }
    }

    # behav_lack_info - Lacked information on issues/candidates as reason for not voting
    # Source: q5b
    df_clean['behav_lack_info'] = df['q5b'].map({
        1.0: 'yes',
        2.0: 'no'
    })

    CODEBOOK_VARIABLES['behav_lack_info'] = {
        'original_variable': 'q5b',
        'question_label': "Q5B. Je manquais d'information sur les enjeux, les candidats et leurs idées (Voici différentes raisons pour lesquelles les gens ne votent pas. Indiquez dans chaque cas si la raison a joué un rôle dans votre décision de ne pas voter aux élections municipales du 7 novembre 2021)",
        'type': 'binary',
        'value_labels': {
            'yes': "Oui",
            'no': "Non"
        }
    }

    # behav_dislike_candidates - Didn't like any candidates/parties as reason for not voting
    # Source: q5c
    df_clean['behav_dislike_candidates'] = df['q5c'].map({
        1.0: 'yes',
        2.0: 'no'
    })

    CODEBOOK_VARIABLES['behav_dislike_candidates'] = {
        'original_variable': 'q5c',
        'question_label': "Q5C. Je n'aimais aucun des candidats ou des partis (Voici différentes raisons pour lesquelles les gens ne votent pas. Indiquez dans chaque cas si la raison a joué un rôle dans votre décision de ne pas voter aux élections municipales du 7 novembre 2021)",
        'type': 'binary',
        'value_labels': {
            'yes': "Oui",
            'no': "Non"
        }
    }

    # op_not_concerned_issues - Didn't feel concerned by campaign issues as reason for not voting
    # Source: q5d
    df_clean['op_not_concerned_issues'] = df['q5d'].map({
        1.0: 'yes',
        2.0: 'no'
    })

    CODEBOOK_VARIABLES['op_not_concerned_issues'] = {
        'original_variable': 'q5d',
        'question_label': "Q5D. Je ne me sentais pas concerné(e) par les enjeux de la campagne (Voici différentes raisons pour lesquelles les gens ne votent pas. Indiquez dans chaque cas si la raison a joué un rôle dans votre décision de ne pas voter aux élections municipales du 7 novembre 2021)",
        'type': 'binary',
        'value_labels': {
            'yes': "Oui",
            'no': "Non"
        }
    }

    # op_vote_no_change - Felt my vote wouldn't change anything as reason for not voting
    # Source: q5e
    df_clean['op_vote_no_change'] = df['q5e'].map({
        1.0: 'yes',
        2.0: 'no'
    })

    CODEBOOK_VARIABLES['op_vote_no_change'] = {
        'original_variable': 'q5e',
        'question_label': "Q5E. J'avais l'impression que mon vote ne changerait rien (Voici différentes raisons pour lesquelles les gens ne votent pas. Indiquez dans chaque cas si la raison a joué un rôle dans votre décision de ne pas voter aux élections municipales du 7 novembre)",
        'type': 'binary',
        'value_labels': {
            'yes': "Oui",
            'no': "Non"
        }
    }

    # behav_nonvote_lost_confidence - Lost confidence in elected officials and politics (reason for not voting)
    # Source: q5f
    df_clean['behav_nonvote_lost_confidence'] = df['q5f'].map({
        1.0: 'yes',
        2.0: 'no'
    })

    CODEBOOK_VARIABLES['behav_nonvote_lost_confidence'] = {
        'original_variable': 'q5f',
        'question_label': "J'ai perdu confiance envers les élus et la politique (raison de ne pas voter)",
        'type': 'binary',
        'value_labels': {
            'yes': 'Oui',
            'no': 'Non'
        }
    }

    # behav_too_busy - Being too busy as reason for not voting
    # Source: q5g
    df_clean['behav_too_busy'] = df['q5g'].map({
        1.0: 'yes',
        2.0: 'no'
    })

    CODEBOOK_VARIABLES['behav_too_busy'] = {
        'original_variable': 'q5g',
        'question_label': "Q5G. J'étais trop occupé(e) (Voici différentes raisons pour lesquelles les gens ne votent pas. Indiquez dans chaque cas si la raison a joué un rôle dans votre décision de ne pas voter aux élections municipales du 7 novembre 2021) (Base : N'ont pas voté)",
        'type': 'binary',
        'value_labels': {
            'yes': "Oui",
            'no': "Non"
        }
    }

    # behav_away_from_home - Being away from home/city as reason for not voting
    # Source: q5h
    df_clean['behav_away_from_home'] = df['q5h'].map({
        1.0: 'yes',
        2.0: 'no'
    })

    CODEBOOK_VARIABLES['behav_away_from_home'] = {
        'original_variable': 'q5h',
        'question_label': "Q5H. J'étais à l'extérieur de la ville ou loin de la maison (Voici différentes raisons pour lesquelles les gens ne votent pas. Indiquez dans chaque cas si la raison a joué un rôle dans votre décision de ne pas voter aux élections municipales du 7 novembre 2021)",
        'type': 'binary',
        'value_labels': {
            'yes': "Oui",
            'no': "Non"
        }
    }

    # behav_no_vote_health_concerns - Concerned about health situation as reason for not voting
    # Source: q5i
    df_clean['behav_no_vote_health_concerns'] = df['q5i'].map({
        1.0: 1.0,  # Oui
        2.0: 0.0   # Non
    })

    CODEBOOK_VARIABLES['behav_no_vote_health_concerns'] = {
        'original_variable': 'q5i',
        'question_label': "J'étais préoccupé(e) par la situation sanitaire (raison de ne pas voter)",
        'type': 'binary',
        'value_labels': {
            1.0: "Oui",
            0.0: "Non"
        }
    }

    # behav_no_vote_other_reason - Other reason for not voting
    # Source: q5j
    df_clean['behav_no_vote_other_reason'] = df['q5j'].map({
        1.0: 'yes',
        2.0: 'no'
    })

    CODEBOOK_VARIABLES['behav_no_vote_other_reason'] = {
        'original_variable': 'q5j',
        'question_label': "Q5J. Autre raison (Voici différentes raisons pour lesquelles les gens ne votent pas. Indiquez dans chaque cas si la raison a joué un rôle dans votre décision de ne pas voter aux élections municipales du 7 novembre 2021) (Base : N'ont pas voté)",
        'type': 'binary',
        'value_labels': {
            'yes': "Oui",
            'no': "Non"
        }
    }

    # behav_other_reason_specific - Specific categorized other reason for not voting
    # Source: q5j_o_m1
    df_clean['behav_other_reason_specific'] = df['q5j_o_m1'].map({
        10.0: 'reason_code_10',
        11.0: 'reason_code_11',
        12.0: 'reason_code_12',
        13.0: 'reason_code_13',
        14.0: 'reason_code_14',
        15.0: 'reason_code_15',
        16.0: 'reason_code_16',
        17.0: 'reason_code_17',
        18.0: 'reason_code_18',
        19.0: 'reason_code_19',
        20.0: 'reason_code_20',
        97.0: np.nan  # Don't know/refuse
    })

    CODEBOOK_VARIABLES['behav_other_reason_specific'] = {
        'original_variable': 'q5j_o_m1',
        'question_label': "Q5J_O. Voici différentes raisons pour lesquelles les gens ne votent pas. Indiquez dans chaque cas si la raison a joué un rôle dans votre décision de ne pas voter aux élections municipales du 7 novembre 2021.",
        'type': 'categorical',
        'value_labels': {
            'reason_code_10': "Code de raison 10",
            'reason_code_11': "Code de raison 11",
            'reason_code_12': "Code de raison 12",
            'reason_code_13': "Code de raison 13",
            'reason_code_14': "Code de raison 14",
            'reason_code_15': "Code de raison 15",
            'reason_code_16': "Code de raison 16",
            'reason_code_17': "Code de raison 17",
            'reason_code_18': "Code de raison 18",
            'reason_code_19': "Code de raison 19",
            'reason_code_20': "Code de raison 20"
        }
    }

    # behav_other_reason_second - Second categorized other reason for not voting
    # Source: q5j_o_m2
    df_clean['behav_other_reason_second'] = df['q5j_o_m2'].map({
        11.0: 'reason_code_11',
        12.0: 'reason_code_12',
        17.0: 'reason_code_17'
    })

    CODEBOOK_VARIABLES['behav_other_reason_second'] = {
        'original_variable': 'q5j_o_m2',
        'question_label': "Q5J_O. Voici différentes raisons pour lesquelles les gens ne votent pas. Indiquez dans chaque cas si la raison a joué un rôle dans votre décision de ne pas voter aux élections municipales du 7 novembre 2021.",
        'type': 'categorical',
        'value_labels': {
            'reason_code_11': "Code de raison 11 (deuxième mention)",
            'reason_code_12': "Code de raison 12 (deuxième mention)", 
            'reason_code_17': "Code de raison 17 (deuxième mention)"
        }
    }

    # behav_no_vote_reason_other - Other reasons for not voting (open-ended)
    # Source: q5j_o
    df_clean['behav_no_vote_reason_other'] = df['q5j_o'].astype(str).str.strip().replace('nan', np.nan)

    CODEBOOK_VARIABLES['behav_no_vote_reason_other'] = {
        'original_variable': 'q5j_o',
        'question_label': "Q5J_O. Autres raisons pour ne pas avoir voté aux élections municipales (spécifiez)",
        'type': 'text',
        'value_labels': {}
    }

    # behav_no_vote_reason_first - First reason mentioned for not voting (multiple response format)
    # Source: q5t_m1
    df_clean['behav_no_vote_reason_first'] = df['q5t_m1'].map({
        1.0: 'no_interest',
        2.0: 'lack_information',
        3.0: 'dislike_candidates',
        4.0: 'not_concerned',
        5.0: 'vote_no_change',
        6.0: 'lost_confidence',
        7.0: 'too_busy',
        8.0: 'away_from_home',
        9.0: 'health_concerns',
        10.0: 'other_reason',
        11.0: 'other_reason_2'
    })

    CODEBOOK_VARIABLES['behav_no_vote_reason_first'] = {
        'original_variable': 'q5t_m1',
        'question_label': "Q5T. Première raison mentionnée pour ne pas avoir voté aux élections municipales du 7 novembre 2021 (Base : N'ont pas voté)",
        'type': 'categorical',
        'value_labels': {
            'no_interest': "Aucun intérêt pour la politique municipale",
            'lack_information': "Manque d'information sur les enjeux/candidats",
            'dislike_candidates': "N'aimait aucun des candidats ou partis",
            'not_concerned': "Ne se sentait pas concerné par les enjeux",
            'vote_no_change': "Impression que le vote ne changerait rien",
            'lost_confidence': "Perte de confiance envers les élus/politique",
            'too_busy': "Trop occupé",
            'away_from_home': "À l'extérieur de la ville/loin de la maison",
            'health_concerns': "Préoccupé par la situation sanitaire",
            'other_reason': "Autre raison",
            'other_reason_2': "Autre raison (second type)"
        }
    }

    # behav_no_vote_reason_rank_2 - Second most important reason for not voting (ranking 2-10, normalized)
    # Source: q5t_m2
    df_clean['behav_no_vote_reason_rank_2'] = df['q5t_m2'].map({
        2.0: 0.0,    # Rank 2 (highest importance for second reason)
        3.0: 0.125,  # Rank 3
        4.0: 0.25,   # Rank 4
        5.0: 0.375,  # Rank 5
        6.0: 0.5,    # Rank 6
        7.0: 0.625,  # Rank 7
        8.0: 0.75,   # Rank 8
        9.0: 0.875,  # Rank 9
        10.0: 1.0    # Rank 10 (lowest importance for second reason)
    })

    CODEBOOK_VARIABLES['behav_no_vote_reason_rank_2'] = {
        'original_variable': 'q5t_m2',
        'question_label': "Q5T. Classement de la deuxième raison la plus importante pour ne pas voter aux élections municipales du 7 novembre 2021 (Base : N'ont pas voté)",
        'type': 'likert',
        'value_labels': {
            0.0: "Rang 2 (deuxième raison la plus importante)",
            0.125: "Rang 3",
            0.25: "Rang 4",
            0.375: "Rang 5",
            0.5: "Rang 6",
            0.625: "Rang 7",
            0.75: "Rang 8",
            0.875: "Rang 9",
            1.0: "Rang 10 (deuxième raison la moins importante)"
        }
    }

    # behav_no_vote_reason_rank_3 - Third most important reason for not voting (ranking 3-10, normalized)
    # Source: q5t_m3
    df_clean['behav_no_vote_reason_rank_3'] = df['q5t_m3'].map({
        3.0: 0.0,       # Rank 3 (highest importance for third reason)
        4.0: 0.143,     # Rank 4
        5.0: 0.286,     # Rank 5
        6.0: 0.429,     # Rank 6
        7.0: 0.571,     # Rank 7
        8.0: 0.714,     # Rank 8
        9.0: 0.857,     # Rank 9
        10.0: 1.0       # Rank 10 (lowest importance for third reason)
    })

    CODEBOOK_VARIABLES['behav_no_vote_reason_rank_3'] = {
        'original_variable': 'q5t_m3',
        'question_label': "Q5T. Classement de la troisième raison la plus importante pour ne pas voter aux élections municipales du 7 novembre 2021 (Base : N'ont pas voté)",
        'type': 'likert',
        'value_labels': {
            0.0: "Rang 3 (troisième raison la plus importante)",
            0.143: "Rang 4",
            0.286: "Rang 5",
            0.429: "Rang 6",
            0.571: "Rang 7",
            0.714: "Rang 8",
            0.857: "Rang 9",
            1.0: "Rang 10 (troisième raison la moins importante)"
        }
    }

    # behav_no_vote_reason_rank_4 - Fourth most important reason for not voting (ranking 4-10, normalized)
    # Source: q5t_m4
    df_clean['behav_no_vote_reason_rank_4'] = df['q5t_m4'].map({
        4.0: 0.0,       # Rank 4 (highest importance for fourth reason)
        5.0: 0.167,     # Rank 5
        6.0: 0.333,     # Rank 6
        7.0: 0.5,       # Rank 7
        8.0: 0.667,     # Rank 8
        9.0: 0.833,     # Rank 9
        10.0: 1.0       # Rank 10 (lowest importance for fourth reason)
    })

    CODEBOOK_VARIABLES['behav_no_vote_reason_rank_4'] = {
        'original_variable': 'q5t_m4',
        'question_label': "Q5T. Classement de la quatrième raison la plus importante pour ne pas voter aux élections municipales du 7 novembre 2021 (Base : N'ont pas voté)",
        'type': 'likert',
        'value_labels': {
            0.0: "Rang 4 (quatrième raison la plus importante)",
            0.167: "Rang 5",
            0.333: "Rang 6",
            0.5: "Rang 7",
            0.667: "Rang 8",
            0.833: "Rang 9",
            1.0: "Rang 10 (quatrième raison la moins importante)"
        }
    }

    # behav_no_vote_reason_rank_5 - Fifth most important reason for not voting (ranking 5-10, normalized)
    # Source: q5t_m5
    df_clean['behav_no_vote_reason_rank_5'] = df['q5t_m5'].map({
        5.0: 0.0,       # Rank 5 (highest importance for fifth reason)
        6.0: 0.2,       # Rank 6
        7.0: 0.4,       # Rank 7
        8.0: 0.6,       # Rank 8
        9.0: 0.8,       # Rank 9
        10.0: 1.0       # Rank 10 (lowest importance for fifth reason)
    })

    CODEBOOK_VARIABLES['behav_no_vote_reason_rank_5'] = {
        'original_variable': 'q5t_m5',
        'question_label': "Q5T. Classement de la cinquième raison la plus importante pour ne pas voter aux élections municipales du 7 novembre 2021 (Base : N'ont pas voté)",
        'type': 'likert',
        'value_labels': {
            0.0: "Rang 5 (cinquième raison la plus importante)",
            0.2: "Rang 6",
            0.4: "Rang 7",
            0.6: "Rang 8",
            0.8: "Rang 9",
            1.0: "Rang 10 (cinquième raison la moins importante)"
        }
    }

    # behav_nonvote_reason_6 - Sixth mentioned reason for not voting in municipal election
    # Source: q5t_m6
    df_clean['behav_nonvote_reason_6'] = df['q5t_m6'].map({
        6.0: 'lost_confidence',
        7.0: 'too_busy', 
        8.0: 'away_from_home',
        9.0: 'health_concerns',
        10.0: 'other_reason'
    })

    CODEBOOK_VARIABLES['behav_nonvote_reason_6'] = {
        'original_variable': 'q5t_m6',
        'question_label': 'Q5T - Raisons pour ne pas voter (mention 6)',
        'type': 'categorical',
        'value_labels': {
            'lost_confidence': 'J\'ai perdu confiance envers les élus et la politique',
            'too_busy': 'J\'étais trop occupé(e)',
            'away_from_home': 'J\'étais à l\'extérieur de la ville ou loin de la maison',
            'health_concerns': 'J\'étais préoccupé(e) par la situation sanitaire',
            'other_reason': 'Autre raison'
        }
    }

    # behav_no_vote_too_busy_rank - Ranking importance of "too busy" as reason for not voting (normalized)
    # Source: q5t_m7
    df_clean['behav_no_vote_too_busy_rank'] = df['q5t_m7'].map({
        7.0: 1.0,    # Rank 7 (highest importance - best rank available for this variable)
        8.0: 0.5,    # Rank 8 (medium importance)
        9.0: 0.0     # Rank 9 (lowest importance)
    })

    CODEBOOK_VARIABLES['behav_no_vote_too_busy_rank'] = {
        'original_variable': 'q5t_m7',
        'question_label': "Q5T. Classement de 'J'étais trop occupé(e)' comme raison de ne pas voter aux élections municipales du 7 novembre 2021 (Base : N'ont pas voté)",
        'type': 'likert',
        'value_labels': {
            1.0: "Rang 7 (importance la plus élevée disponible)",
            0.5: "Rang 8 (importance moyenne)",
            0.0: "Rang 9 (importance la plus faible)"
        }
    }

    # behav_no_vote_away_home_rank - Ranking importance of "away from home" as reason for not voting (normalized)
    # Source: q5t_m8
    df_clean['behav_no_vote_away_home_rank'] = df['q5t_m8'].map({
        8.0: 1.0,    # Rank 8 (highest importance - best rank available for this variable)
        9.0: 0.5,    # Rank 9 (medium importance)
        10.0: 0.0    # Rank 10 (lowest importance)
    })

    CODEBOOK_VARIABLES['behav_no_vote_away_home_rank'] = {
        'original_variable': 'q5t_m8',
        'question_label': "Q5T. Classement de 'J'étais à l'extérieur de la ville ou loin de la maison' comme raison de ne pas voter aux élections municipales du 7 novembre 2021 (Base : N'ont pas voté)",
        'type': 'likert',
        'value_labels': {
            1.0: "Rang 8 (importance la plus élevée disponible)",
            0.5: "Rang 9 (importance moyenne)",
            0.0: "Rang 10 (importance la plus faible)"
        }
    }

    # behav_no_vote_health_concerns_rank - Ranking importance of "health concerns" as reason for not voting
    # Source: q5t_m9
    df_clean['behav_no_vote_health_concerns_rank'] = df['q5t_m9'].map({
        9.0: 1.0    # Rank 9 - only rank available for this reason (mentioned by 40 respondents)
    })

    CODEBOOK_VARIABLES['behav_no_vote_health_concerns_rank'] = {
        'original_variable': 'q5t_m9',
        'question_label': "Q5T. Classement de 'J'étais préoccupé(e) par la situation sanitaire' comme raison de ne pas voter aux élections municipales du 7 novembre 2021 (Base : N'ont pas voté)",
        'type': 'binary',
        'value_labels': {
            1.0: "Rang 9 - Raison mentionnée (préoccupé par la situation sanitaire)"
        }
    }

    # know_candidate_names - Knowledge of mayoral candidate names (ordinal scale)
    # Source: q6a
    df_clean['know_candidate_names'] = df['q6a'].map({
        1.0: 1.0,    # Likely "Très bien" / "Complètement"
        2.0: 0.5,    # Likely "Un peu" / "Partiellement"  
        3.0: 0.0     # Likely "Pas du tout" / "Non"
    })

    CODEBOOK_VARIABLES['know_candidate_names'] = {
        'original_variable': 'q6a',
        'question_label': "Q6A. Est-ce que vous connaissiez le nom des candidat(e)s à la mairie dans votre municipalité ?",
        'type': 'likert',
        'value_labels': {
            1.0: "Modalité 1 (connaissance élevée)",
            0.5: "Modalité 2 (connaissance partielle)",
            0.0: "Modalité 3 (aucune connaissance)"
        }
    }

    # know_candidate_programs - Knowledge of mayoral candidates' programs and projects
    # Source: q6b
    df_clean['know_candidate_programs'] = df['q6b'].map({
        1.0: 1.0,    # Très bien / Complètement
        2.0: 0.5,    # Un peu / Partiellement  
        3.0: 0.0     # Pas du tout / Non
    })

    CODEBOOK_VARIABLES['know_candidate_programs'] = {
        'original_variable': 'q6b',
        'question_label': "Q6B. Diriez-vous que vous connaissiez le programme et les projets des candidat(e)s à la mairie ?",
        'type': 'likert',
        'value_labels': {
            1.0: "Modalité 1 (connaissance élevée du programme)",
            0.5: "Modalité 2 (connaissance partielle du programme)",
            0.0: "Modalité 3 (aucune connaissance du programme)"
        }
    }

    # op_political_proximity - Feeling close to municipal political team/party
    # Source: q7
    df_clean['op_political_proximity'] = df['q7'].map({
        1.0: 1.0,    # Très proche
        2.0: 0.67,   # Assez proche
        3.0: 0.33,   # Peu proche
        4.0: 0.0,    # Pas proche du tout
        9.0: np.nan  # Ne sait pas/Refuse
    })

    CODEBOOK_VARIABLES['op_political_proximity'] = {
        'original_variable': 'q7',
        'question_label': "Q7. Est-ce que vous vous sentiez proche d'une équipe ou d'un parti politique de votre municipalité?",
        'type': 'likert',
        'value_labels': {
            1.0: "Très proche",
            0.67: "Assez proche",
            0.33: "Peu proche",
            0.0: "Pas proche du tout"
        }
    }

    # op_electoral_rules_adequate - Assessment of adequacy of electoral financing rules
    # Source: q8
    df_clean['op_electoral_rules_adequate'] = df['q8'].map({
        1.0: 0.0,    # Not adequate (assuming 1 = least adequate)
        2.0: 0.5,    # Somewhat adequate
        3.0: 1.0,    # Adequate (assuming 3 = most adequate)
        9.0: np.nan  # Don't know/Not applicable
    })

    CODEBOOK_VARIABLES['op_electoral_rules_adequate'] = {
        'original_variable': 'q8',
        'question_label': "Q8. Dans l'ensemble, estimez-vous que les règles de financement et de contrôle des dépenses électorales qui s'appliquent dans votre municipalité sont adéquates ?",
        'type': 'likert',
        'value_labels': {
            0.0: "Modalité 1 (pas adéquates)",
            0.5: "Modalité 2 (partiellement adéquates)",
            1.0: "Modalité 3 (adéquates)"
        }
    }

    # op_electoral_rules_adequate_filtered - Assessment of adequacy of electoral financing rules (filtered base)
    # Source: q8x
    df_clean['op_electoral_rules_adequate_filtered'] = df['q8x'].map({
        1.0: 0.0,    # Not adequate at all
        2.0: 0.5,    # Somewhat adequate
        3.0: 1.0     # Completely adequate
    })

    CODEBOOK_VARIABLES['op_electoral_rules_adequate_filtered'] = {
        'original_variable': 'q8x',
        'question_label': "Q8. Dans l'ensemble, estimez-vous que les règles de financement et de contrôle des dépenses électorales qui s'appliquent dans votre municipalité sont adéquates ? (Base : connaissent les règles de financement)",
        'type': 'likert',
        'value_labels': {
            0.0: "Pas du tout adéquates",
            0.5: "Plutôt adéquates", 
            1.0: "Tout à fait adéquates"
        }
    }

    # op_satisfaction_democracy - Satisfaction with how democracy functions in municipality
    # Source: q9
    df_clean['op_satisfaction_democracy'] = df['q9'].map({
        1.0: 1.0,    # Très satisfait
        2.0: 0.67,   # Plutôt satisfait  
        3.0: 0.33,   # Plutôt insatisfait
        4.0: 0.0     # Très insatisfait
    })

    CODEBOOK_VARIABLES['op_satisfaction_democracy'] = {
        'original_variable': 'q9',
        'question_label': "Q9. Dans l'ensemble, êtes-vous satisfait(e) de la façon dont la démocratie fonctionne dans votre municipalité ?",
        'type': 'likert',
        'value_labels': {
            1.0: "Très satisfait",
            0.67: "Plutôt satisfait",
            0.33: "Plutôt insatisfait",
            0.0: "Très insatisfait"
        }
    }

    # op_municipal_govt_complex - Agreement that municipal government functioning is too complex (REVERSED)
    # Source: q10a
    df_clean['op_municipal_govt_complex'] = df['q10a'].map({
        1.0: 0.0,    # Tout à fait d'accord → 0 (government IS too complex - negative)
        2.0: 0.33,   # Plutôt d'accord → 0.33 (somewhat agree it's complex - somewhat negative)
        3.0: 0.67,   # Plutôt en désaccord → 0.67 (disagree it's complex - somewhat positive)
        4.0: 1.0     # Tout à fait en désaccord → 1 (strongly disagree it's complex - positive)
    })

    CODEBOOK_VARIABLES['op_municipal_govt_complex'] = {
        'original_variable': 'q10a',
        'question_label': "Q10A. Le fonctionnement du conseil municipal est si compliqué qu'il est difficile de vraiment comprendre ce qui se passe",
        'type': 'likert',
        'value_labels': {
            0.0: "Tout à fait d'accord (gouvernement très complexe)",
            0.33: "Plutôt d'accord (gouvernement assez complexe)",
            0.67: "Plutôt en désaccord (gouvernement pas très complexe)",
            1.0: "Tout à fait en désaccord (gouvernement pas complexe du tout)"
        }
    }

    # op_officials_dont_care - Agreement that municipal officials don't care about ordinary people (REVERSED)
    # Source: q10b
    df_clean['op_officials_dont_care'] = df['q10b'].map({
        1.0: 0.0,    # Tout à fait d'accord → 0 (agree officials don't care - negative)
        2.0: 0.33,   # Plutôt d'accord → 0.33 (somewhat agree - somewhat negative)
        3.0: 0.67,   # Plutôt en désaccord → 0.67 (disagree - somewhat positive)
        4.0: 1.0     # Tout à fait en désaccord → 1 (strongly disagree - positive)
    })

    CODEBOOK_VARIABLES['op_officials_dont_care'] = {
        'original_variable': 'q10b',
        'question_label': "Q10B. Les élu(e)s municipaux ne se préoccupent pas beaucoup de ce que les gens ordinaires pensent",
        'type': 'likert',
        'value_labels': {
            0.0: "Tout à fait d'accord (les élus ne se préoccupent pas)",
            0.33: "Plutôt d'accord (les élus se préoccupent peu)",
            0.67: "Plutôt en désaccord (les élus se préoccupent assez)",
            1.0: "Tout à fait en désaccord (les élus se préoccupent beaucoup)"
        }
    }

    # op_citizens_can_influence - Agreement that citizens can influence municipal council decisions
    # Source: q10d
    df_clean['op_citizens_can_influence'] = df['q10d'].map({
        1.0: 1.0,    # Tout à fait d'accord
        2.0: 0.67,   # Plutôt d'accord
        3.0: 0.33,   # Plutôt en désaccord
        4.0: 0.0     # Tout à fait en désaccord
    })

    CODEBOOK_VARIABLES['op_citizens_can_influence'] = {
        'original_variable': 'q10d',
        'question_label': "Q10D. Les citoyens peuvent influencer les décisions du conseil municipal",
        'type': 'likert',
        'value_labels': {
            1.0: "Tout à fait d'accord",
            0.67: "Plutôt d'accord",
            0.33: "Plutôt en désaccord",
            0.0: "Tout à fait en désaccord"
        }
    }

    # op_officials_reflect_diversity - Agreement that municipal officials reflect diversity of municipality
    # Source: q10e
    df_clean['op_officials_reflect_diversity'] = df['q10e'].map({
        1.0: 1.0,    # Tout à fait d'accord
        2.0: 0.67,   # Plutôt d'accord
        3.0: 0.33,   # Plutôt en désaccord
        4.0: 0.0     # Tout à fait en désaccord
    })

    CODEBOOK_VARIABLES['op_officials_reflect_diversity'] = {
        'original_variable': 'q10e',
        'question_label': "Q10E. Les élus municipaux reflètent la diversité de ma municipalité",
        'type': 'likert',
        'value_labels': {
            1.0: "Tout à fait d'accord",
            0.67: "Plutôt d'accord", 
            0.33: "Plutôt en désaccord",
            0.0: "Tout à fait en désaccord"
        }
    }

    # op_municipal_impact - Perceived impact of municipal council decisions on respondent
    # Source: q11
    df_clean['op_municipal_impact'] = df['q11'].map({
        1.0: 1.0,    # Beaucoup d'impact
        2.0: 0.67,   # Assez d'impact
        3.0: 0.33,   # Peu d'impact
        4.0: 0.0     # Pas d'impact du tout
    })

    CODEBOOK_VARIABLES['op_municipal_impact'] = {
        'original_variable': 'q11',
        'question_label': "Q11. Les personnes élues prennent des décisions susceptibles d'avoir un impact sur la vie des citoyens et des citoyennes. Selon vous, à quel point les décisions prises par votre conseil municipal ont un impact sur vous ?",
        'type': 'likert',
        'value_labels': {
            1.0: "Beaucoup d'impact",
            0.67: "Assez d'impact",
            0.33: "Peu d'impact",
            0.0: "Pas d'impact du tout"
        }
    }

    # behav_info_source_municipal_2nd - Second choice information source for municipal election candidates
    # Source: q12_m2
    df_clean['behav_info_source_municipal_2nd'] = df['q12_m2'].map({
        1.0: 'source_1',
        2.0: 'source_2',
        3.0: 'source_3',
        4.0: 'source_4',
        5.0: 'source_5',
        6.0: 'source_6',
        7.0: 'source_7',
        8.0: 'source_8'
    })

    CODEBOOK_VARIABLES['behav_info_source_municipal_2nd'] = {
        'original_variable': 'q12_m2',
        'question_label': "Q12. Quelle(s) ont été vos principales sources d'information à propos des candidat(e)s et de leurs programmes lors des élections municipales du 7 novembre ? Cochez tout ce qui s'applique. (Deuxième choix)",
        'type': 'categorical',
        'value_labels': {
            'source_1': "Source d'information 1 (deuxième choix)",
            'source_2': "Source d'information 2 (deuxième choix)",
            'source_3': "Source d'information 3 (deuxième choix)",
            'source_4': "Source d'information 4 (deuxième choix)",
            'source_5': "Source d'information 5 (deuxième choix)",
            'source_6': "Source d'information 6 (deuxième choix)",
            'source_7': "Source d'information 7 (deuxième choix)",
            'source_8': "Source d'information 8 (deuxième choix)"
        }
    }

    # behav_info_source_municipal_3rd - Third choice information source for municipal election candidates (ranking 1-8)
    # Source: q12_m3
    df_clean['behav_info_source_municipal_3rd'] = df['q12_m3'].map({
        1.0: 1.0,    # Rank 1 (most important)
        2.0: 0.857,  # Rank 2
        3.0: 0.714,  # Rank 3
        4.0: 0.571,  # Rank 4
        5.0: 0.429,  # Rank 5
        6.0: 0.286,  # Rank 6
        7.0: 0.143,  # Rank 7
        8.0: 0.0     # Rank 8 (least important)
    })

    CODEBOOK_VARIABLES['behav_info_source_municipal_3rd'] = {
        'original_variable': 'q12_m3',
        'question_label': "Q12. Quelle(s) ont été vos principales sources d'information à propos des candidat(e)s et de leurs programmes lors des élections municipales du 7 novembre ? Cochez tout ce qui s'applique. (Troisième choix - classement)",
        'type': 'likert',
        'value_labels': {
            1.0: "Rang 1 (source la plus importante)",
            0.857: "Rang 2",
            0.714: "Rang 3",
            0.571: "Rang 4",
            0.429: "Rang 5",
            0.286: "Rang 6",
            0.143: "Rang 7",
            0.0: "Rang 8 (source la moins importante)"
        }
    }

    # behav_info_source_municipal_4th - Fourth ranked information source for municipal election candidates
    # Source: q12_m4
    df_clean['behav_info_source_municipal_4th'] = df['q12_m4'].map({
        1.0: 1.0,    # Rank 1 (most important)
        2.0: 0.857,  # Rank 2
        3.0: 0.714,  # Rank 3
        4.0: 0.571,  # Rank 4
        5.0: 0.429,  # Rank 5
        6.0: 0.286,  # Rank 6
        7.0: 0.143,  # Rank 7
        8.0: 0.0     # Rank 8 (least important)
    })

    CODEBOOK_VARIABLES['behav_info_source_municipal_4th'] = {
        'original_variable': 'q12_m4',
        'question_label': "Q12. Quelle(s) ont été vos principales sources d'information à propos des candidat(e)s et de leurs programmes lors des élections municipales du 7 novembre ? Cochez tout ce qui s'applique. (Quatrième choix - classement)",
        'type': 'likert',
        'value_labels': {
            1.0: "Rang 1 (source la plus importante)",
            0.857: "Rang 2",
            0.714: "Rang 3",
            0.571: "Rang 4",
            0.429: "Rang 5",
            0.286: "Rang 6",
            0.143: "Rang 7",
            0.0: "Rang 8 (source la moins importante)"
        }
    }

    # behav_info_source_municipal_5th - Fifth ranked information source for municipal election candidates
    # Source: q12_m5
    df_clean['behav_info_source_municipal_5th'] = df['q12_m5'].map({
        1.0: 1.0,    # Rank 1 (most important)
        2.0: 0.857,  # Rank 2
        3.0: 0.714,  # Rank 3
        4.0: 0.571,  # Rank 4
        5.0: 0.429,  # Rank 5
        6.0: 0.286,  # Rank 6
        7.0: 0.143,  # Rank 7
        8.0: 0.0     # Rank 8 (least important)
    })

    CODEBOOK_VARIABLES['behav_info_source_municipal_5th'] = {
        'original_variable': 'q12_m5',
        'question_label': "Q12. Quelle(s) ont été vos principales sources d'information à propos des candidat(e)s et de leurs programmes lors des élections municipales du 7 novembre ? Cochez tout ce qui s'applique. (Cinquième choix - classement)",
        'type': 'likert',
        'value_labels': {
            1.0: "Rang 1 (source la plus importante)",
            0.857: "Rang 2",
            0.714: "Rang 3",
            0.571: "Rang 4",
            0.429: "Rang 5",
            0.286: "Rang 6",
            0.143: "Rang 7",
            0.0: "Rang 8 (source la moins importante)"
        }
    }

    # behav_info_source_municipal_6th - Sixth ranked information source for municipal election candidates
    # Source: q12_m6
    df_clean['behav_info_source_municipal_6th'] = df['q12_m6'].map({
        1.0: 1.0,    # Rank 1 (most important)
        2.0: 0.857,  # Rank 2
        3.0: 0.714,  # Rank 3
        4.0: 0.571,  # Rank 4
        5.0: 0.429,  # Rank 5
        6.0: 0.286,  # Rank 6
        7.0: 0.143,  # Rank 7
        8.0: 0.0     # Rank 8 (least important)
    })

    CODEBOOK_VARIABLES['behav_info_source_municipal_6th'] = {
        'original_variable': 'q12_m6',
        'question_label': "Q12. Quelle(s) ont été vos principales sources d'information à propos des candidat(e)s et de leurs programmes lors des élections municipales du 7 novembre ? Cochez tout ce qui s'applique. (Sixième choix - classement)",
        'type': 'likert',
        'value_labels': {
            1.0: "Rang 1 (source la plus importante)",
            0.857: "Rang 2",
            0.714: "Rang 3",
            0.571: "Rang 4",
            0.429: "Rang 5",
            0.286: "Rang 6",
            0.143: "Rang 7",
            0.0: "Rang 8 (source la moins importante)"
        }
    }

    return df_clean


def get_metadata():
    """Retourne les métadonnées enrichies (survey + variables)

    Appelé par lambda_raffineur_nettoyage après clean_data().
    Les métadonnées sont sauvegardées comme codebook.json dans S3.

    Returns:
        dict: Dictionnaire structuré avec:
            - survey_metadata: Métadonnées générales du sondage
            - variables: Métadonnées pour chaque variable nettoyée
    """
    return {
        'survey_metadata': SURVEY_METADATA,
        'variables': CODEBOOK_VARIABLES
    }
