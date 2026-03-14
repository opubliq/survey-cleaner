# ses_province — Province de કર્યો
# Source: Q2_province
# Note: Data column used is 'q2' as 'Q2_province' was not found in data exploration.
df_clean['ses_province'] = df['q2'].map({
    1.0: 'quebec',
    2.0: 'ontario',
    3.0: 'alberta',
    99.0: np.nan,
})
CODEBOOK_VARIABLES['ses_province'] = {
    'original_variable': 'Q2_province',
    'question_label': "Province de résidence",
    'type': 'categorical',
    'value_labels': {'quebec': "Québec", 'ontario': "Ontario", 'alberta': "Alberta"},
}