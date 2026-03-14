# op_q34b — Inferred 4-point scale/categorical response
# Source: Q34B
# Assumption: Codes 8.0 and 9.0 are treated as missing (Not explicitly defined in codebook for this run)
df_clean['op_q34b'] = df['Q34B'].map({
    1.0: 'cat_1',
    2.0: 'cat_2',
    3.0: 'cat_3',
    4.0: 'cat_4',
    8.0: np.nan,
    9.0: np.nan,
})
CODEBOOK_VARIABLES['op_q34b'] = {
    'original_variable': 'Q34B',
    'question_label': "Q34B (Inferred Categorical)",
    'type': 'categorical',
    'value_labels': {'cat_1': "Category 1", 'cat_2': "Category 2", 'cat_3': "Category 3", 'cat_4': "Category 4"},
}