# ses_province — Province de résidence
# Source: Q50
# Assumption: codes 4, 8, 9 are unlabelled/other, and code 99 is explicitly missing based on codebook. Codes 8 and 9 are treated as missing.
df_clean['ses_province'] = df['Q50'].map({
    1.0: 'quebec',
    2.0: 'ontario',
    3.0: 'alberta',
    4.0: 'other_province',
    8.0: np.nan,
    9.0: np.nan,
    99.0: np.nan,
})
CODEBOOK_VARIABLES['ses_province'] = {
    'original_variable': 'Q50',
    'question_label': "Province de résidence",
    'type': 'categorical',
    'value_labels': {'quebec': "Québec", 'ontario': "Ontario", 'alberta': "Alberta", 'other_province': "Other Province (Unlabelled 4)"},
}