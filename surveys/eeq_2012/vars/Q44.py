# ses_province — Province de résidence (Inferred from data patterns)
# Source: Q44
# Assumption: Codes 8.0 and 9.0 are treated as missing as they lack labels and follow common survey patterns.
df_clean['ses_province'] = df['Q44'].map({
    1.0: 'quebec',
    2.0: 'ontario',
    3.0: 'alberta',
    8.0: np.nan,
    9.0: np.nan,
})
CODEBOOK_VARIABLES['ses_province'] = {
    'original_variable': 'Q44',
    'question_label': "Province de résidence (Inferred from data patterns)",
    'type': 'categorical',
    'value_labels': {'quebec': "Québec", 'ontario': "Ontario", 'alberta': "Alberta"},
}