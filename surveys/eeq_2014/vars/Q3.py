# op_q3 — Inferred categorical opinion variable from Q3
# Source: Q3
# Assumption: Variable type is categorical based on value distribution (1.0-6.0).
# Assumption: Codes 96.0 and 99.0 are treated as missing.
# TODO: Replace placeholder values ('cat_1', 'cat_2', etc.) and question label with actual survey metadata.
df_clean['op_q3'] = df['Q3'].map({
    1.0: 'option_1',
    2.0: 'option_2',
    3.0: 'option_3',
    4.0: 'option_4',
    5.0: 'option_5',
    6.0: 'option_6',
    96.0: np.nan,
    99.0: np.nan,
})
CODEBOOK_VARIABLES['op_q3'] = {
    'original_variable': 'Q3',
    'question_label': "Inferred category for Q3 (No label provided)",
    'type': 'categorical',
    'value_labels': {'option_1': "Category 1", 'option_2': "Category 2", 'option_3': "Category 3", 'option_4': "Category 4", 'option_5': "Category 5", 'option_6': "Category 6"},
}