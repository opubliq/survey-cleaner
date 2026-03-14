# ses_province — Province de résidence
# Source: reg
# Assumption: Missing codes from codebook were not present in data. Codes 1-5 are inferred regions based on typical survey distribution, as no codebook was provided.
df_clean['ses_province'] = df['reg'].map({
    1.0: 'quebec',
    2.0: 'ontario',
    3.0: 'alberta',
    4.0: 'british_columbia',
    5.0: 'other',
})
CODEBOOK_VARIABLES['ses_province'] = {
    'original_variable': 'reg',
    'question_label': "Province de résidence (inferred)",
    'type': 'categorical',
    'value_labels': {'quebec': "Québec", 'ontario': "Ontario", 'alberta': "Alberta", 'british_columbia': "British Columbia", 'other': "Other Province"},
}