# ses_sel3 — Inferred socio-economic indicator
# Source: SEL3
# Assumption: Binary variable, codes 1.0/2.0 mapped to level_1/level_2. Missing codes (not observed) assumed to map to np.nan.
df_clean['ses_sel3'] = df['SEL3'].map({
    1.0: 'level_1',
    2.0: 'level_2',
})
CODEBOOK_VARIABLES['ses_sel3'] = {
    'original_variable': 'SEL3',
    'question_label': "Inferred SES indicator 3 (Requires verification)",
    'type': 'categorical',
    'value_labels': {'level_1': "Level 1", 'level_2': "Level 2"},
}