# ses_province — Province de résidence
# Source: Q2_province
# Assumption: Data column is 'q2' instead of 'Q2_province'
# Assumption: Codes '4', '8', '9' found in data but not in codebook values are treated as missing (np.nan)
df_clean['ses_province'] = df['q2'].map({
    '1': 'quebec',
    '2': 'ontario',
    '3': 'alberta',
    '4': np.nan,
    '8': np.nan,
    '9': np.nan,
})
CODEBOOK_VARIABLES['ses_province'] = {
    'original_variable': 'Q2_province',
    'question_label': "Province de résidence",
    'type': 'categorical',
    'value_labels': {'quebec': "Québec", 'ontario': "Ontario", 'alberta': "Alberta"},
}