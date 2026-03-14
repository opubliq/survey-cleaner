# op_q19 — Unknown question, mapping based on value counts.
# Source: q19
# Assumption: Codes 8.0 (126) and 9.0 (22) treated as 'dk' and 'refused' respectively.
# TODO: verify mapping for codes 1.0, 2.0, 3.0, 8.0, 9.0 against actual codebook.
df_clean['op_q19'] = df['q19'].map({
    1.0: 'option_a',
    2.0: 'option_b',
    3.0: 'option_c',
    8.0: 'dk',
    9.0: 'refused',
})
CODEBOOK_VARIABLES['op_q19'] = {
    'original_variable': 'q19',
    'question_label': "Unknown question, mapping based on value counts.",
    'type': 'categorical',
    'value_labels': {'option_a': "Option A", 'option_b': "Option B", 'option_c': "Option C", 'dk': "Don't Know", 'refused': "Refused"},
}