# ses_province — Province of residence (Inferred)
# Source: Q2
# Assumption: codes 1 and 2 mapped, code 9.0 treated as missing (inferred from similar variable structure)
df_clean['ses_province'] = df['Q2'].map({
    1.0: 'quebec',
    2.0: 'ontario',
    9.0: np.nan,
})
CODEBOOK_VARIABLES['ses_province'] = {
    'original_variable': 'Q2',
    'question_label': "Province of residence (Inferred)",
    'type': 'categorical',
    'value_labels': {'quebec': "Québec", 'ontario': "Ontario"},
}