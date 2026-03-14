# ses_age_group — Âge du répondant (catégories)
# Source: q0age
df_clean['ses_age_group'] = df['q0age'].map({
    2.0: '18-24',
    3.0: '25-34',
    4.0: '35-44',
    5.0: '45-54',
    6.0: '55-64',
    7.0: '65-74',
    8.0: '75+',
    99.0: np.nan,
})
CODEBOOK_VARIABLES['ses_age_group'] = {
    'original_variable': 'q0age',
    'question_label': "Quel âge avez-vous ?",
    'type': 'categorical',
    'value_labels': {
        '18-24': "Entre 18 et 24 ans",
        '25-34': "Entre 25 et 34 ans",
        '35-44': "Entre 35 et 44 ans",
        '45-54': "Entre 45 et 54 ans",
        '55-64': "Entre 55 et 64 ans",
        '65-74': "Entre 65 et 74 ans",
        '75+': "75 ans ou plus",
    },
}
