# ses_province — Province de résidence
# Source: Q62AG
# Assumption: Since codebook values are empty, observed code 96.0 is mapped to 'unknown'.
# Assumption: Codebook missing code 99 is treated as np.nan.
df_clean['ses_province'] = df['Q62AG'].map({
    96.0: 'unknown',
    99.0: np.nan,
})
CODEBOOK_VARIABLES['ses_province'] = {
    'original_variable': 'Q62AG',
    'question_label': "Province de résidence",
    'type': 'categorical',
    'value_labels': {'unknown': "Unknown/Unlabelled"},
}