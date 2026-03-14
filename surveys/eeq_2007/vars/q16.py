# behav_main_info_source — Main source of information on politics
# Source: q16
df_clean['behav_main_info_source'] = df['q16'].map({
    '01': 'television',
    '02': 'radio',
    '03': 'newspapers',
    '04': 'websites',
    '05': 'blogs',
    '06': 'family',
    '07': 'friends',
    '08': 'coworkers',
    '09': 'party_organizations',
    '96': 'other',
    '97': 'no_sources',
    '98': np.nan,
    '99': np.nan,
})
CODEBOOK_VARIABLES['behav_main_info_source'] = {
    'original_variable': 'q16',
    'question_label': "Quelle est votre PRINCIPALE source d'information sur la politique ? / NE PAS LIRE",
    'type': 'categorical',
    'value_labels': {
        'television': 'Télévision',
        'radio': 'Radio',
        'newspapers': 'Journaux',
        'websites': 'Sites web',
        'blogs': 'Blogs',
        'family': 'Famille',
        'friends': 'Amis',
        'coworkers': 'Collègues de travail',
        'party_organizations': 'Associations, organisations de partis politiques',
        'other': 'Autres',
        'no_sources': 'Pas de sources d\'information',
    },
}
