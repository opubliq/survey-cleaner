# op_v85 — Unknown categorical response variable
# Source: Q85
# Assumption: Codes 8.0/9.0 are treated as missing (no codebook provided)
df_clean['op_v85'] = df['Q85'].map({
    1.0: 'cat1',
    2.0: 'cat2',
    3.0: 'cat3',
    8.0: np.nan,
    9.0: np.nan,
})
CODEBOOK_VARIABLES['op_v85'] = {
    'original_variable': 'Q85',
    'question_label': "Unknown - Inferred from data structure as a categorical response.",
    'type': 'categorical',
    'value_labels': {'cat1': 'Category 1', 'cat2': 'Category 2', 'cat3': 'Category 3'},
}