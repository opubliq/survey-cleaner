# op_q27 — Variable Q27 - Mapping is based on observed values only, as no codebook was provided.
# Source: Q27
# Assumption: Codes 96.0, 98.0, 99.0 are treated as missing.
# TODO: verify mapping for codes 1.0-5.0 and labels, as no codebook was provided.
df_clean['op_q27'] = df['Q27'].map({
    1.0: 'cat1',
    2.0: 'cat2',
    3.0: 'cat3',
    4.0: 'cat4',
    5.0: 'cat5',
    96.0: np.nan,
    98.0: np.nan,
    99.0: np.nan,
})
CODEBOOK_VARIABLES['op_q27'] = {
    'original_variable': 'Q27',
    'question_label': "Variable Q27 - Mapping is based on observed values only, as no codebook was provided.",
    'type': 'categorical',
    'value_labels': {'cat1': 'Category 1', 'cat2': 'Category 2', 'cat3': 'Category 3', 'cat4': 'Category 4', 'cat5': 'Category 5'},
}