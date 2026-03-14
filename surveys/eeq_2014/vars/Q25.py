# ses_province — Province de résidence
# Source: Q25
# Assumption: codes 8 and 9 are treated as missing (unlabelled in provided codebook context)
df_clean['ses_province'] = df['Q25'].map({
    1.0: 'quebec',
    2.0: 'ontario',
    3.0: 'alberta',
    8.0: np.nan,
    9.0: np.nan,
})
CODEBOOK_VARIABLES['ses_province'] = {
    'original_variable': 'Q25',
    'question_label': "Province de résidence",
    'type': 'categorical',
    'value_labels': {'quebec': "Québec", 'ontario': "Ontario", 'alberta': "Alberta"},
}