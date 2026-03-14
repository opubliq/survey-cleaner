# ses_province — Province de résidence (Inferred mapping due to missing codebook)
# Source: q38
# Assumption: Codes 8 and 9 are treated as missing (unlabelled in data exploration). Code 4 is mapped to 'other_province'.
df_clean['ses_province'] = df['q38'].map({
    '1': 'quebec',
    '2': 'ontario',
    '3': 'alberta',
    '4': 'other_province',
    '8': np.nan,
    '9': np.nan,
})
CODEBOOK_VARIABLES['ses_province'] = {
    'original_variable': 'q38',
    'question_label': "Province de résidence (Requires label verification)",
    'type': 'categorical',
    'value_labels': {'quebec': "Québec", 'ontario': "Ontario", 'alberta': "Alberta", 'other_province': "Other Province (Unlabelled)"},
}