# op_q27 — Choice for question 27
# Source: q27
# Note: No codebook provided. Codes 8 and 9 treated as missing/unlabelled.
df_clean['op_q27'] = df['q27'].map({
    '1': 'choice_1',
    '2': 'choice_2',
    '3': 'choice_3',
    '4': 'choice_4',
    '8': np.nan,
    '9': np.nan,
})
CODEBOOK_VARIABLES['op_q27'] = {
    'original_variable': 'q27',
    'question_label': "Choice for Q27 (No label available)",
    'type': 'categorical',
    'value_labels': {'choice_1': "Code 1", 'choice_2': "Code 2", 'choice_3': "Code 3", 'choice_4': "Code 4"},
}