# op_q22 — Generic categorical question Q22
# Source: Q22
# Assumption: Codes 8.0 and 9.0 are treated as missing (not present in codebook)
df_clean['op_q22'] = df['Q22'].map({
    1.0: 'choice_1',
    2.0: 'choice_2',
    3.0: 'choice_3',
    8.0: np.nan,
    9.0: np.nan,
})
CODEBOOK_VARIABLES['op_q22'] = {
    'original_variable': 'Q22',
    'question_label': "Generic question Q22 (No codebook provided)",
    'type': 'categorical',
    'value_labels': {'choice_1': "Category 1", 'choice_2': "Category 2", 'choice_3': "Category 3"},
}