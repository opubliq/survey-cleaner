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

    # Q9A - Élections provinciales du 7 avril 2014
    df_clean['behav_vote_turnout_provincial_2014'] = df['Q9A'].map({
        1: 1.0,      # Oui, a voté
        2: 0.0,      # Non, n'a pas voté
        8: np.nan,   # N'avait pas droit de vote
        9: np.nan    # Ne sait pas
    })

    # Q9B - Élections fédérales du 19 octobre 2015
    df_clean['behav_vote_turnout_federal_2015'] = df['Q9B'].map({
        1: 1.0,      # Oui, a voté
        2: 0.0,      # Non, n'a pas voté
        8: np.nan,   # N'avait pas droit de vote
        9: np.nan    # Ne sait pas
    })

    # Q9C - Élections municipales du 5 novembre 2017
    df_clean['behav_vote_turnout_municipal_2017'] = df['Q9C'].map({
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

    # Q11 - "Selon vous, est-ce important que les gens votent aux élections?"
    # Échelle ordinale 4 niveaux + don't know
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

    # Q12A - "Quel a été votre intérêt pour la politique en général?"
    df_clean['op_interest_politics_general'] = df['Q12A'] / 10.0

    # Q12B - "Quel a été votre intérêt pour l'élection provinciale qui vient de se terminer?"
    df_clean['op_interest_election_provincial_2018'] = df['Q12B'] / 10.0

    # Q13 - "En politique provinciale, est-ce qu'il y a un parti dont vous vous sentez proche?"
    # Identité partisane (partisan identity)
    df_clean['op_partisan_identity'] = df['Q13'].map({
        1: 1.0,      # Oui
        2: 0.0,      # Non
        9: np.nan    # Ne sais pas
    })

    # Q14 - "Quel était votre niveau d'information sur les politiques et plateformes électorales?"
    # Échelle ordinale 4 niveaux + don't know
    # Normalisation: 1=Très informé → 1.0, 4=Pas du tout informé → 0.0
    df_clean['op_information_level_election'] = df['Q14'].map({
        1: 1.0,      # Très informé(e)
        2: 0.67,     # Assez informé(e)
        3: 0.33,     # Peu informé(e)
        4: 0.0,      # Pas du tout informé(e)
        9: np.nan    # Je ne sais pas
    })

    # Q15 - "Quel est votre niveau de satisfaction de la façon dont la démocratie fonctionne au Québec?"
    # Échelle ordinale 4 niveaux + don't know
    # Normalisation: 1=Très satisfait → 1.0, 4=Pas du tout satisfait → 0.0
    df_clean['op_satisfaction_democracy_qc'] = df['Q15'].map({
        1: 1.0,      # Très satisfait(e)
        2: 0.67,     # Assez satisfait(e)
        3: 0.33,     # Peu satisfait(e)
        4: 0.0,      # Pas du tout satisfait(e)
        9: np.nan    # Je ne sais pas
    })

    # Q16A-Q16O - Attitudes politiques (échelles d'accord/désaccord)
    # Normalisation: 1=Tout à fait d'accord → 1.0, 4=Tout à fait en désaccord → 0.0

    # Q16A - "Les élections sont une façon de choisir l'orientation des politiques"
    df_clean['op_elections_choose_policies'] = df['Q16A'].map({
        1: 1.0, 2: 0.67, 3: 0.33, 4: 0.0, 5: np.nan
    })

    # Q16B - "Les élections tiennent les gouvernements responsables"
    df_clean['op_elections_accountability'] = df['Q16B'].map({
        1: 1.0, 2: 0.67, 3: 0.33, 4: 0.0, 5: np.nan
    })

    # Q16C - "Les députés perdent contact avec les citoyens une fois élus"
    df_clean['op_mps_lose_contact'] = df['Q16C'].map({
        1: 1.0, 2: 0.67, 3: 0.33, 4: 0.0, 5: np.nan
    })

    # Q16D - "Les élus reflètent la diversité de la société québécoise"
    df_clean['op_elected_reflect_diversity'] = df['Q16D'].map({
        1: 1.0, 2: 0.67, 3: 0.33, 4: 0.0, 5: np.nan
    })

    # Q16E - "Les gens comme vous n'ont pas leur mot à dire"
    df_clean['op_no_say_in_government'] = df['Q16E'].map({
        1: 1.0, 2: 0.67, 3: 0.33, 4: 0.0, 5: np.nan
    })

    # Q16F - "La politique semble si compliquée"
    df_clean['op_politics_too_complicated'] = df['Q16F'].map({
        1: 1.0, 2: 0.67, 3: 0.33, 4: 0.0, 5: np.nan
    })

    # Q16G - "Le gouvernement ne se préoccupe pas de ce que les gens pensent"
    df_clean['op_government_doesnt_care'] = df['Q16G'].map({
        1: 1.0, 2: 0.67, 3: 0.33, 4: 0.0, 5: np.nan
    })

    # Q16H - "Nous pouvons avoir confiance que le gouvernement fera ce qui est juste"
    df_clean['op_trust_government'] = df['Q16H'].map({
        1: 1.0, 2: 0.67, 3: 0.33, 4: 0.0, 5: np.nan
    })

    # Q16I - "Les politiciens font des promesses qu'ils n'ont pas l'intention de respecter"
    df_clean['op_politicians_broken_promises'] = df['Q16I'].map({
        1: 1.0, 2: 0.67, 3: 0.33, 4: 0.0, 5: np.nan
    })

    # Q16J - "Tous les partis se ressemblent, il n'y a pas vraiment de choix"
    df_clean['op_parties_all_same'] = df['Q16J'].map({
        1: 1.0, 2: 0.67, 3: 0.33, 4: 0.0, 5: np.nan
    })

    # Q16K - "Les partis politiques sont la meilleure façon de représenter les citoyens"
    df_clean['op_parties_best_representation'] = df['Q16K'].map({
        1: 1.0, 2: 0.67, 3: 0.33, 4: 0.0, 5: np.nan
    })

    # Q16L - "Les partis sont trop influencés par les gens riches"
    df_clean['op_parties_influenced_by_rich'] = df['Q16L'].map({
        1: 1.0, 2: 0.67, 3: 0.33, 4: 0.0, 5: np.nan
    })

    # Q16M - "Voter fait partie du devoir de tout bon citoyen"
    df_clean['op_voting_citizen_duty'] = df['Q16M'].map({
        1: 1.0, 2: 0.67, 3: 0.33, 4: 0.0, 5: np.nan
    })

    # Q16N - "Voter permet de préserver la démocratie"
    df_clean['op_voting_preserves_democracy'] = df['Q16N'].map({
        1: 1.0, 2: 0.67, 3: 0.33, 4: 0.0, 5: np.nan
    })

    # Q16O - "Il est plus probable que je vote si la course est serrée"
    df_clean['op_vote_if_close_race'] = df['Q16O'].map({
        1: 1.0, 2: 0.67, 3: 0.33, 4: 0.0, 5: np.nan
    })

    # Q17A-Q17C - Influence des sondages (variables conditionnelles)

    # Q17A - "Avez-vous pris connaissance de sondages indiquant les intentions de vote?"
    df_clean['behav_aware_of_polls'] = df['Q17A'].map({
        1: 1.0,      # Oui
        2: 0.0,      # Non
        9: np.nan    # Je ne sais pas
    })

    # Q17B - "Est-ce que ces sondages ont influencé votre décision de voter?" (votants)
    df_clean['behav_polls_influenced_vote'] = df['Q17B'].map({
        1: 1.0,      # Oui
        2: 0.0,      # Non
        9: np.nan    # Je ne sais pas
    })

    # Q17C - "Est-ce que ces sondages ont influencé votre décision de ne pas voter?" (non-votants)
    df_clean['behav_polls_influenced_abstention'] = df['Q17C'].map({
        1: 1.0,      # Oui
        2: 0.0,      # Non
        9: np.nan    # Je ne sais pas
    })

    # Q18A - "Durant la campagne, est-ce qu'un parti politique ou un candidat vous a contacté(e)?"
    df_clean['behav_contacted_by_party'] = df['Q18A'].map({
        1: 1.0,      # Oui
        2: 0.0,      # Non
        9: np.nan    # Je ne sais pas
    })

    # Q18BM*, Q18CM* - Multi-response questions (SKIP)
    # Q18B: Modes de communication (9 options multi-sélection)
    # Q18C: Buts de la communication (7 options multi-sélection)
    # Trop sparse (55-85% missing) et structure complexe

    # Q19A - "Votre ménage compte-t-il d'autres personnes ayant le droit de vote?"
    df_clean['ses_household_other_voters'] = df['Q19A'].map({
        1: 1.0,      # Oui
        2: 0.0,      # Non
        9: np.nan    # Préfère ne pas répondre
    })

    # Q19B - "À votre connaissance, ces personnes ont-elles l'habitude de voter?" (conditionnel)
    df_clean['ses_household_others_usually_vote'] = df['Q19B'].map({
        1.0: 1.0,    # Oui
        2.0: 0.0,    # Non
        9.0: np.nan  # Je ne sais pas
    })

    # Q20AM* - Qui vous a encouragé à voter (multi-réponses, SKIP)
    # 7 catégories multi-sélection avec 63% ayant répondu "Aucune personne"
    # Trop sparse et complexe pour le moment

    # Q21 - "Lorsque vous étiez enfant, est-ce que votre famille discutait de politique...?"
    # Échelle ordinale 4 niveaux + don't know
    # Normalisation: 1=Souvent → 1.0, 4=Jamais → 0.0
    df_clean['ses_family_discussed_politics_childhood'] = df['Q21'].map({
        1: 1.0,      # Souvent
        2: 0.67,     # Parfois
        3: 0.33,     # Rarement
        4: 0.0,      # Jamais
        9: np.nan    # Je ne sais pas
    })

    # Q22 - "Et aujourd'hui, discutez-vous de politique avec votre famille, vos amis ou vos collègues...?"
    # Échelle ordinale 4 niveaux + don't know
    # Normalisation: 1=Souvent → 1.0, 4=Jamais → 0.0
    df_clean['behav_discuss_politics_today'] = df['Q22'].map({
        1: 1.0,      # Souvent
        2: 0.67,     # Parfois
        3: 0.33,     # Rarement
        4: 0.0,      # Jamais
        9: np.nan    # Je ne sais pas
    })

    # Q23A-Q23H - Actions politiques au cours des 12 derniers mois
    # Échelle de fréquence: 1=Plus de 5 fois, 2=Entre 2 et 5 fois, 3=Une seule fois, 4=Jamais, 9=Je ne sais pas
    # Normalisation: 1 → 1.0, 2 → 0.67, 3 → 0.33, 4 → 0.0

    # Q23A - "Signer une pétition sur papier ou sur Internet"
    df_clean['behav_sign_petition'] = df['Q23A'].map({
        1: 1.0, 2: 0.67, 3: 0.33, 4: 0.0, 9: np.nan
    })

    # Q23B - "Acheter ou boycotter des produits pour des raisons politiques, éthiques ou environnementales"
    df_clean['behav_boycott_products'] = df['Q23B'].map({
        1: 1.0, 2: 0.67, 3: 0.33, 4: 0.0, 9: np.nan
    })

    # Q23C - "Exprimer votre opinion sur une question politique ou sociale sur un forum Internet ou un site Internet de nouvelles"
    df_clean['behav_express_opinion_online'] = df['Q23C'].map({
        1: 1.0, 2: 0.67, 3: 0.33, 4: 0.0, 9: np.nan
    })

    # Q23D - "Participer à une manifestation ou à une marche de protestation"
    df_clean['behav_participate_protest'] = df['Q23D'].map({
        1: 1.0, 2: 0.67, 3: 0.33, 4: 0.0, 9: np.nan
    })

    # Q23E - "Faire du bénévolat ou militer pour un parti politique"
    df_clean['behav_volunteer_party'] = df['Q23E'].map({
        1: 1.0, 2: 0.67, 3: 0.33, 4: 0.0, 9: np.nan
    })

    # Q23F - "Exprimer votre opinion sur une question en communiquant avec un journal ou un politicien"
    df_clean['behav_contact_media_politician'] = df['Q23F'].map({
        1: 1.0, 2: 0.67, 3: 0.33, 4: 0.0, 9: np.nan
    })

    # Q23G - "Prendre la parole lors d'une réunion publique"
    df_clean['behav_speak_public_meeting'] = df['Q23G'].map({
        1: 1.0, 2: 0.67, 3: 0.33, 4: 0.0, 9: np.nan
    })

    # Q23H - "Porter un macaron, un tee-shirt, afficher une pancarte pour appuyer ou vous opposer à une cause politique"
    df_clean['behav_display_political_symbol'] = df['Q23H'].map({
        1: 1.0, 2: 0.67, 3: 0.33, 4: 0.0, 9: np.nan
    })

    # Q24A-Q24E - Fréquence de consultation de sources d'information
    # Échelle: 1=Très souvent, 2=Souvent, 3=Rarement, 4=Jamais
    # Normalisation: 1 → 1.0, 2 → 0.67, 3 → 0.33, 4 → 0.0

    # Q24A - "Les nouvelles à la télévision"
    df_clean['behav_news_tv'] = df['Q24A'].map({
        1: 1.0, 2: 0.67, 3: 0.33, 4: 0.0
    })

    # Q24B - "Les journaux en format papier ou électronique"
    df_clean['behav_news_newspapers'] = df['Q24B'].map({
        1: 1.0, 2: 0.67, 3: 0.33, 4: 0.0
    })

    # Q24C - "Les sites Web des médias"
    df_clean['behav_news_websites'] = df['Q24C'].map({
        1: 1.0, 2: 0.67, 3: 0.33, 4: 0.0
    })

    # Q24D - "Les nouvelles sur les sites de réseautage social (Facebook, Twitter, LinkedIn, Instagram etc.)"
    df_clean['behav_news_social_media'] = df['Q24D'].map({
        1: 1.0, 2: 0.67, 3: 0.33, 4: 0.0
    })

    # Q24E - "Les nouvelles à la radio"
    df_clean['behav_news_radio'] = df['Q24E'].map({
        1: 1.0, 2: 0.67, 3: 0.33, 4: 0.0
    })

    # Q25A-Q25I - Attitudes envers la candidature politique
    # Échelle: 1=Tout à fait d'accord, 2=Plutôt d'accord, 3=Plutôt en désaccord, 4=Tout à fait en désaccord, 9=Je ne sais pas
    # Normalisation: 1 → 1.0, 2 → 0.67, 3 → 0.33, 4 → 0.0

    # Q25A - "Un jour, je pourrais souhaiter faire le saut en politique comme candidat aux élections"
    df_clean['op_consider_running_for_office'] = df['Q25A'].map({
        1: 1.0, 2: 0.67, 3: 0.33, 4: 0.0, 9: np.nan
    })

    # Q25B - "Pour être candidat aux élections, il faut avoir envie de servir sa communauté"
    df_clean['op_candidate_needs_serve_community'] = df['Q25B'].map({
        1: 1.0, 2: 0.67, 3: 0.33, 4: 0.0, 9: np.nan
    })

    # Q25C - "Pour être candidat aux élections, il faut avoir envie de défendre les intérêts des citoyens que l'on souhaite représenter"
    df_clean['op_candidate_needs_defend_interests'] = df['Q25C'].map({
        1: 1.0, 2: 0.67, 3: 0.33, 4: 0.0, 9: np.nan
    })

    # Q25D - "Pour être candidat aux élections, il faut être prêt à renoncer à une partie de sa vie privée"
    df_clean['op_candidate_sacrifice_privacy'] = df['Q25D'].map({
        1: 1.0, 2: 0.67, 3: 0.33, 4: 0.0, 9: np.nan
    })

    # Q25E - "Pour être candidat aux élections, il faut être prêt à faire des compromis"
    df_clean['op_candidate_make_compromises'] = df['Q25E'].map({
        1: 1.0, 2: 0.67, 3: 0.33, 4: 0.0, 9: np.nan
    })

    # Q25F - "Pour être candidat aux élections, il faut être prêt à l'affrontement"
    df_clean['op_candidate_ready_confrontation'] = df['Q25F'].map({
        1: 1.0, 2: 0.67, 3: 0.33, 4: 0.0, 9: np.nan
    })

    # Q25G - "Ma situation financière me permettrait d'être candidat aux élections"
    df_clean['op_financial_situation_allows_candidacy'] = df['Q25G'].map({
        1: 1.0, 2: 0.67, 3: 0.33, 4: 0.0, 9: np.nan
    })

    # Q25H - "Je crois être suffisamment qualifié(e) pour être candidat aux élections"
    df_clean['op_qualified_for_candidacy'] = df['Q25H'].map({
        1: 1.0, 2: 0.67, 3: 0.33, 4: 0.0, 9: np.nan
    })

    # Q25I - "Mes responsabilités familiales me permettraient d'être candidat aux élections"
    df_clean['op_family_allows_candidacy'] = df['Q25I'].map({
        1: 1.0, 2: 0.67, 3: 0.33, 4: 0.0, 9: np.nan
    })

    # Q26A-Q26B - Éducation politique (18-34 ans seulement, 69% missing)
    # Échelle: 1=Oui, 2=Non, 9=Je ne sais pas

    # Q26A - "Assisté à des cours sur la politique ou les élections?"
    df_clean['ses_education_politics_courses'] = df['Q26A'].map({
        1.0: 1.0,    # Oui
        2.0: 0.0,    # Non
        9.0: np.nan  # Je ne sais pas
    })

    # Q26B - "Participé à une ou des simulations d'élections, à des simulations politiques ou fait partie d'un conseil ou d'une association étudiante?"
    df_clean['ses_education_political_simulation'] = df['Q26B'].map({
        1.0: 1.0,    # Oui
        2.0: 0.0,    # Non
        9.0: np.nan  # Je ne sais pas
    })

    # Q27A-Q27C - Opinions sur réformes électorales
    # Échelle: 1=Tout à fait d'accord, 2=Plutôt d'accord, 3=Plutôt en désaccord, 4=Tout à fait en désaccord, 5=Je ne sais pas
    # Normalisation: 1 → 1.0, 2 → 0.67, 3 → 0.33, 4 → 0.0

    # Q27A - "Les bulletins de vote devraient comporter l'option 'Aucun de ces candidats'"
    df_clean['op_ballot_none_of_the_above'] = df['Q27A'].map({
        1: 1.0, 2: 0.67, 3: 0.33, 4: 0.0, 5: np.nan
    })

    # Q27B - "Une loi devrait obliger les électeurs à voter aux élections provinciales"
    df_clean['op_mandatory_voting'] = df['Q27B'].map({
        1: 1.0, 2: 0.67, 3: 0.33, 4: 0.0, 5: np.nan
    })

    # Q27C - "On devrait abaisser l'âge du vote à 16 ans"
    df_clean['op_voting_age_16'] = df['Q27C'].map({
        1: 1.0, 2: 0.67, 3: 0.33, 4: 0.0, 5: np.nan
    })

    # Q28 - SKIP (impact du vote le lundi, pas critique pour analyse)

    # ============================================================================
    # VARIABLES DÉMOGRAPHIQUES (Q28-Q39)
    # ============================================================================

    # Q29 - Genre
    df_clean['ses_gender'] = df['Q29'].map({
        1: 'male',          # Masculin
        2: 'female',        # Féminin
        3: 'other',         # Autre
        4: np.nan           # Préfère ne pas répondre
    })

    # Q30 - Niveau d'éducation (ordinal)
    df_clean['ses_education'] = df['Q30'].map({
        1: 'primary',               # Primaire (valeur 1 manque dans codebook)
        2: 'secondary_no_diploma',  # Secondaire sans diplôme
        3: 'secondary_diploma',     # Secondaire avec diplôme/DEP
        4: 'cegep_no_diploma',      # Cégep sans diplôme
        5: 'cegep_diploma',         # Cégep avec diplôme
        6: 'university_incomplete', # Université non complétée
        7: 'bachelors',             # Baccalauréat
        8: 'masters',               # Maîtrise
        9: 'doctorate',             # Doctorat
        98: np.nan,                 # Ne sais pas
        99: np.nan                  # Préfère ne pas répondre
    })

    # Q31 - Situation d'emploi
    df_clean['ses_employment_status'] = df['Q31'].map({
        1: 'employed',              # Travail rémunéré (valeur 1 manque dans codebook)
        2: 'unemployed',            # À la recherche d'emploi
        3: 'student',               # Étudiant
        4: 'caring_children',       # S'occuper des enfants
        5: 'housework',             # Travaux ménagers
        6: 'retired',               # À la retraite
        7: 'parental_leave',        # Congé parental
        8: 'long_term_illness',     # Maladie de longue durée
        9: 'volunteer_caregiver',   # Bénévolat/soins
        10: 'at_home',              # À la maison
        11: 'social_assistance',    # Aide sociale
        12: 'disability',           # Invalidité/CSST
        13: 'caregiver',            # Aidant naturel
        97: np.nan,                 # Autre
        98: np.nan,                 # Ne sais pas
        99: np.nan                  # Préfère ne pas répondre
    })

    # Q32 - Statut résidentiel (propriétaire/locataire)
    df_clean['ses_housing_status'] = df['Q32'].map({
        1: 'renter',                # Locataire (valeur 1 manque dans codebook)
        2: 'owner',                 # Propriétaire
        3: 'other',                 # Habite chez parents/amis
        8: np.nan,                  # Ne sais pas
        9: np.nan                   # Préfère ne pas répondre
    })

    # Q33 - "Depuis combien de temps habitez-vous à votre adresse actuelle?"
    df_clean['ses_residence_duration'] = df['Q33'].map({
        1: 'less_than_6_months',    # Moins de 6 mois
        2: '6_months_to_1_year',    # 6 mois à moins d'un an
        3: '1_to_3_years',          # 1 an à moins de 3 ans
        4: '3_to_5_years',          # 3 ans à moins de 5 ans
        5: '5_to_10_years',         # 5 ans à moins de 10 ans
        6: '10_years_or_more',      # 10 ans et plus
        8: np.nan,                  # Je ne sais pas
        9: np.nan                   # Je préfère ne pas répondre
    })

    # Q34 - "Quelle langue parlez-vous le plus souvent à la maison?"
    df_clean['ses_home_language'] = df['Q34'].map({
        1: 'french',                # Français
        2: 'english',               # Anglais
        97: 'other',                # Autre
        98: np.nan,                 # Je ne sais pas
        99: np.nan                  # Je préfère ne pas répondre
    })

    # Q35 - "Êtes-vous?" (statut relationnel)
    df_clean['ses_relationship_status'] = df['Q35'].map({
        1: 'in_couple',             # En couple
        2: 'single',                # Célibataire
        3: 'other',                 # Autre
        9: np.nan                   # Je préfère ne pas répondre
    })

    # Q36A - "Combien de personnes de 18 ans et plus composent votre ménage?"
    df_clean['ses_household_adults'] = df['Q36A'].map({
        1: 1,    # 1 personne
        2: 2,    # 2 personnes
        3: 3,    # 3 personnes
        4: 4     # 4 et plus
    })

    # Q36B - "Combien d'enfants de moins de 18 ans composent votre ménage?"
    df_clean['ses_household_children'] = df['Q36B'].map({
        0: 0,         # Aucun
        1: 1,         # 1 enfant
        2: 2,         # 2 enfants
        3: 3,         # 3 enfants
        4: 4,         # 4 enfants
        5: 5,         # 5 et plus
        9: np.nan     # Je préfère ne pas répondre
    })

    # Q37A - "Où êtes-vous né(e)?"
    df_clean['ses_birthplace'] = df['Q37A'].map({
        1: 'quebec',                # Au Québec
        2: 'rest_of_canada',        # Ailleurs au Canada
        3: 'outside_canada',        # À l'extérieur du Canada
        9: np.nan                   # Je préfère ne pas répondre
    })

    # Q37B - "Depuis quand vivez-vous au Québec?" (conditionnel, 92% missing)
    df_clean['ses_years_in_quebec'] = df['Q37B'].map({
        1.0: 'less_than_1_year',    # Moins d'un an
        2.0: '1_to_3_years',        # 1 an à moins de 3 ans
        3.0: '3_to_5_years',        # 3 ans à moins de 5 ans
        4.0: '5_to_10_years',       # 5 ans à moins de 10 ans
        5.0: '10_years_or_more'     # 10 ans et plus
    })

    # Q38 - "Appartenez-vous à une communauté autochtone (Premières Nations, Inuit ou Métis)?"
    df_clean['ses_indigenous'] = df['Q38'].map({
        1: 1.0,      # Oui
        2: 0.0,      # Non
        8: np.nan,   # Je ne sais pas
        9: np.nan    # Je préfère ne pas répondre
    })

    # Q39 - "Dans quelle catégorie se situe votre revenu brut annuel familial?"
    df_clean['ses_household_income'] = df['Q39'].map({
        1: 'less_than_20k',         # Moins de 20 000 $
        2: '20k_to_40k',            # De 20 000 $ à 39 999 $
        3: '40k_to_60k',            # De 40 000 $ à 59 999 $
        4: '60k_to_80k',            # De 60 000 $ à 79 999 $
        5: '80k_to_100k',           # De 80 000 $ à 99 999 $
        6: '100k_to_120k',          # De 100 000 $ à 119 999 $
        7: '120k_to_150k',          # De 120 000 $ à 150 000 $
        8: 'more_than_150k',        # Plus de 150 000 $
        98: np.nan,                 # Je ne sais pas
        99: np.nan                  # Préfère ne pas répondre
    })

    # ============================================================================
    # PONDÉRATION
    # ============================================================================

    # Pondération - Poids pour analyses
    df_clean['weight_standard'] = df['Pondération'].copy()

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
