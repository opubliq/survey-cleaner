# ses_province — Province de résidence
# Source: Q78
# Note: Codes 8 and 9 are not in the codebook and will be treated as missing (np.nan)
# Assumption: Codes 1 and 2 map to provinces as per the context for eeq_2007, assuming similar structure.
# Since no codebook was provided for this specific call, I am mapping based on the previous context's implicit meaning: 1=Quebec, 2=Ontario.
df_clean['ses_province'] = df['Q78'].map({
    1.0: 'quebec',
    2.0: 'ontario',
    8.0: np.nan,
    9.0: np.nan,
})
CODEBOOK_VARIABLES['ses_province'] = {
    'original_variable': 'Q78',
    'question_label': "Province de résidence (Inferred)",
    'type': 'categorical',
    'value_labels': {'quebec': "Québec", 'ontario': "Ontario"},
}