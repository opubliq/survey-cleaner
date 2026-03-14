# ses_province — Province de résidence
# Source: Q7E
# Assumption: Undocumented codes 8.0 and 9.0 are treated as missing (np.nan).
df_clean['ses_province'] = df['Q7E'].map({
    1.0: 'quebec',
    2.0: 'ontario',
    3.0: 'alberta',
    8.0: np.nan,
    9.0: np.nan,
})
CODEBOOK_VARIABLES['ses_province'] = {
    'original_variable': 'Q7E',
    'question_label': "Province de résidence",
    'type': 'categorical',
    'value_labels': {'quebec': "Québec", 'ontario': "Ontario", 'alberta': "Alberta"},
}