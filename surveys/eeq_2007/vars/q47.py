# op_unknown_q47 — Unknown categorical variable from Q47
# Source: q47
# Assumption: Codes 8 and 9 are treated as missing (unlabelled in codebook)
df_clean['op_unknown_q47'] = df['q47'].map({
    '1': 'cat_1',
    '2': 'cat_2',
    '3': 'cat_3',
    '8': np.nan,
    '9': np.nan,
})
CODEBOOK_VARIABLES['op_unknown_q47'] = {
    'original_variable': 'q47',
    'question_label': "Unknown variable Q47 (No codebook provided)",
    'type': 'categorical',
    'value_labels': {'cat_1': "Value 1", 'cat_2': "Value 2", 'cat_3': "Value 3"},
}