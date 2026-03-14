# ses_province — Province de résidence
# Source: Q2_province
# NOTE: Original variable 'Q2_province' was not found in the data file.
# Assumption: data is present in the 'codep' column instead.
# Assumption: codes 99 treated as missing (unlabelled in codebook)
df_clean['ses_province'] = df['codep'].map({
    1.0: 'quebec',
    2.0: 'ontario',
    3.0: 'alberta',
    99.0: np.nan,
})
CODEBOOK_VARIABLES['ses_province'] = {
    'original_variable': 'Q2_province',
    'question_label': "Province de résidence",
    'type': 'categorical',
    'value_labels': {'quebec': "Québec", 'ontario': "Ontario", 'alberta': "Alberta"},
}