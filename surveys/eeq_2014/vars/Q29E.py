# ses_province — Province de résidence
# Source: Q29E
# WARNING: Data exploration showed many float values (0.0, 5.0, 10.0...) which contradicts the codebook's 3-value categorical definition.
# Assumption: The codebook values (1, 2, 3) for province are correct, and all other observed values map to missing.
df_clean['ses_province'] = df['Q29E'].map({
    1.0: 'quebec',
    2.0: 'ontario',
    3.0: 'alberta',
    99.0: np.nan,
})
CODEBOOK_VARIABLES['ses_province'] = {
    'original_variable': 'Q29E',
    'question_label': "Province de résidence",
    'type': 'categorical',
    'value_labels': {'quebec': "Québec", 'ontario': "Ontario", 'alberta': "Alberta"},
}