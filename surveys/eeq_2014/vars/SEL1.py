# ses_sel — Socio-Economic Level/Status (Assumed from two clean codes)
# Source: SEL1
# Assumption: Code 1.0 maps to 'level_1' and 2.0 maps to 'level_2'.
df_clean['ses_sel'] = df['SEL1'].map({
    1.0: 'level_1',
    2.0: 'level_2',
})
CODEBOOK_VARIABLES['ses_sel'] = {
    'original_variable': 'SEL1',
    'question_label': "Socio-Economic Level/Status (Assumed)",
    'type': 'categorical',
    'value_labels': {'level_1': "Level 1 (Assumed)", 'level_2': "Level 2 (Assumed)"},
}