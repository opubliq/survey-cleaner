# ses_age_group — Age category
# Source: CLAGE
# Note: Mapping inferred based on common age brackets for codes 2-8 as no codebook entry was supplied.
df_clean['ses_age_group'] = df['CLAGE'].map({
    2.0: '18-24',
    3.0: '25-34',
    4.0: '35-44',
    5.0: '45-54',
    6.0: '55-64',
    7.0: '65-74',
    8.0: '75+'
})
CODEBOOK_VARIABLES['ses_age_group'] = {
    'original_variable': 'CLAGE',
    'question_label': "Category of Age",
    'type': 'categorical',
    'value_labels': {'18-24': "18-24 years old", '25-34': "25-34 years old", '35-44': "35-44 years old", '45-54': "45-54 years old", '55-64': "55-64 years old", '65-74': "65-74 years old", '75+': "75 years or older"},
}