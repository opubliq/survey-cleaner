# behav_info_source_2 — Deuxième source d'information sur la politique
# Source: q17
# Note: code 42 found in data but not documented in codebook (treated as missing)
# Assumption: codes 97, 98, 99 treated as missing/refusal
df_clean['behav_info_source_2'] = df['q17'].map({
    '01': 'television',
    '02': 'radio',
    '03': 'newspapers',
    '04': 'websites',
    '05': 'blogs',
    '06': 'family',
    '07': 'friends',
    '08': 'colleagues',
    '09': 'organizations',
    '96': 'other',
    '97': np.nan,
    '98': np.nan,
    '99': np.nan,
})
CODEBOOK_VARIABLES['behav_info_source_2'] = {
    'original_variable': 'q17',
    'question_label': "Quelle est votre deuxième source d'information sur la politique?",
    'type': 'categorical',
    'value_labels': {
        'television': 'Télévision',
        'radio': 'Radio',
        'newspapers': 'Journaux',
        'websites': 'Sites web',
        'blogs': 'Blogs',
        'family': 'Famille',
        'friends': 'Amis',
        'colleagues': 'Collègues de travail',
        'organizations': 'Associations, organisations de partis politiques',
        'other': 'Autres',
    },
}
