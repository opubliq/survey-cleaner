# ses_province — Province de résidence
# Source: Q24C
# Assumption: codes 8.0 and 9.0 are unmapped/missing based on data exploration. Codebook missing code 99.0 was not observed.
df_clean['ses_province'] = df['Q24C'].map({
    1.0: 'quebec',
    2.0: 'ontario',
    3.0: 'alberta',
    8.0: np.nan,
    9.0: np.nan,
})
CODEBOOK_VARIABLES['ses_province'] = {
    'original_variable': 'Q24C',
    'question_label': "Province de résidence",
    'type': 'categorical',
    'value_labels': {'quebec': "Québec", 'ontario': "Ontario", 'alberta': "Alberta"},
}