# ses_province — Province de résidence
# Source: Q18
# Assumption: codes 8/9 are treated as missing (unlabelled in codebook). The codebook entry suggested this was a categorical variable.
# Mapping values 1-4 to provinces based on convention for Quebec election studies.
df_clean['ses_province'] = df['Q18'].map({
    1.0: 'quebec',
    2.0: 'ontario',
    3.0: 'alberta',
    4.0: 'british columbia',
    8.0: np.nan,
    9.0: np.nan,
})
CODEBOOK_VARIABLES['ses_province'] = {
    'original_variable': 'Q18',
    'question_label': "Province de résidence",
    'type': 'categorical',
    'value_labels': {'quebec': "Québec", 'ontario': "Ontario", 'alberta': "Alberta", 'british columbia': "British Columbia"},
}
