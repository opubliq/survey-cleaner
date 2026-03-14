# ses_province — Province de résistance
# Source: Q2_province
# Assumption: Column found in data is 'q2' as 'Q2_province' was missing. Codes 4, 8, 9 are unmapped/missing from codebook and treated as NaN. Code 99 from codebook is also treated as NaN.
df_clean['ses_province'] = df['q2'].map({
    '1': 'quebec',
    '2': 'ontario',
    '3': 'alberta',
    '4': np.nan,
    '8': np.nan,
    '9': np.nan,
    '99': np.nan,
})
CODEBOOK_VARIABLES['ses_province'] = {
    'original_variable': 'Q2_province',
    'question_label': "Province de résidence",
    'type': 'categorical',
    'value_labels': {'quebec': "Québec", 'ontario': "Ontario", 'alberta': "Alberta"},
}