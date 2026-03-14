# ses_province — Province de résidence (Inferred from context)
# Source: Q62B
# Assumption: Codes 3, 6, 8, 9 are treated as missing/unmapped as they don't fit the known structure from context.
df_clean['ses_province'] = df['Q62B'].map({
    1.0: 'quebec',
    2.0: 'ontario',
    3.0: 'alberta',
})
CODEBOOK_VARIABLES['ses_province'] = {
    'original_variable': 'Q62B',
    'question_label': "Province de résidence (Inferred)",
    'type': 'categorical',
    'value_labels': {'quebec': "Québec", 'ontario': "Ontario", 'alberta': "Alberta"},
}