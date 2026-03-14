# op_trust_government — Trust in governments to do what is right
# Source: q23
# Assumption: codes 8/9 treated as missing (Don't know, Refused)
df_clean['op_trust_government'] = df['q23'].map({
    '1': 'almost_always',
    '2': 'most_of_time',
    '3': 'sometimes',
    '4': 'almost_never',
    '8': np.nan,
    '9': np.nan,
})
CODEBOOK_VARIABLES['op_trust_government'] = {
    'original_variable': 'q23',
    'question_label': "Dans quelle mesure faites-vous confiance aux gouvernements pour faire ce qui doit être fait ?",
    'type': 'likert',
    'value_labels': {
        'almost_always': "presque toujours",
        'most_of_time': "la plupart du temps",
        'sometimes': "parfois seulement",
        'almost_never': "presque jamais"
    },
    'likert_direction': 'higher_is_more_trust'
}
