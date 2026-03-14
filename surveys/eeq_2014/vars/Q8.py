# ses_province — Province de résidence
# Source: Q8
# Assumption: codes 96 and 98 are unlabelled and map to missing
# Assumption: code 99 treated as missing (explicitly listed in missing_codes)
df_clean['ses_province'] = df['Q8'].map({
    1.0: 'quebec',
    2.0: 'ontario',
    3.0: 'alberta',
    99.0: np.nan,
})
CODEBOOK_VARIABLES['ses_province'] = {
    'original_variable': 'Q8',
    'question_label': "Province de résidence",
    'type': 'categorical',
    'value_labels': {'quebec': "Québec", 'ontario': "Ontario", 'alberta': "Alberta"},
}