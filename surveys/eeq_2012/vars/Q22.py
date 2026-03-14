# ses_province — Province de résidence
# Source: Q2_province
# Assumption: Codes 8.0 and 9.0 from data map to missing values, as they are unlabelled in the provided codebook excerpt.
df_clean['ses_province'] = df['Q22'].map({
    1.0: 'quebec',
    2.0: 'ontario',
    8.0: np.nan,
    9.0: np.nan,
})
CODEBOOK_VARIABLES['ses_province'] = {
    'original_variable': 'Q22',
    'question_label': "Province de résidence",
    'type': 'categorical',
    'value_labels': {'quebec': "Québec", 'ontario': "Ontario"},
}