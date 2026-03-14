# ses_province — Province de résidence
# Source: Q11
# Assumption: codes 8/9 treated as missing (unlabelled in codebook)
df_clean['ses_province'] = df['Q11'].map({
    1.0: 'quebec',
    2.0: 'ontario',
    3.0: 'alberta',
    4.0: 'other',
    8.0: np.nan,
    9.0: np.nan,
})
CODEBOOK_VARIABLES['ses_province'] = {
    'original_variable': 'Q11',
    'question_label': "Province de résidence",
    'type': 'categorical',
    'value_labels': {'quebec': "Québec", 'ontario': "Ontario", 'alberta': "Alberta", 'other': "Other"},
}