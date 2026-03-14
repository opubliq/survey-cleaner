# ses_age_group — Grouped age of respondent
# Source: Q24A
# Assumption: codes 8 and 9 are missing values (not in provided codebook, inferred from context of typical survey coding)
df_clean['ses_age_group'] = df['Q24A'].map({
    1.0: '18-29',
    2.0: '30-44',
    3.0: '45-64',
    8.0: np.nan,
    9.0: np.nan,
})
CODEBOOK_VARIABLES['ses_age_group'] = {
    'original_variable': 'Q24A',
    'question_label': "Grouped age of respondent",
    'type': 'categorical',
    'value_labels': {'18-29': "18-29", '30-44': "30-44", '45-64': "45-64"},
}