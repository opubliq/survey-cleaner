# ses_province — Province of residence (Inferred)
# Source: Q55
# Assumption: Codes 8.0 and 9.0 treated as missing (not explicitly mapped in codebook)
df_clean['ses_province'] = df['Q55'].map({
    1.0: 'quebec',
    2.0: 'ontario',
    8.0: np.nan,
    9.0: np.nan,
})
CODEBOOK_VARIABLES['ses_province'] = {
    'original_variable': 'Q55',
    'question_label': "Province of residence (Inferred from similar variables)",
    'type': 'categorical',
    'value_labels': {'quebec': "Québec", 'ontario': "Ontario"},
}