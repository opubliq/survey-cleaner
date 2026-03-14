# op_attitude_q82b — Attitude/Opinion question (Q82B)
# Source: Q82B
# Assumption: Codes 8 and 9 treated as missing (not present in original context codebook)
df_clean['op_attitude_q82b'] = df['Q82B'].map({
    1.0: 'response_1',
    2.0: 'response_2',
    3.0: 'response_3',
    4.0: 'response_4',
    8.0: np.nan,
    9.0: np.nan,
})
CODEBOOK_VARIABLES['op_attitude_q82b'] = {
    'original_variable': 'Q82B',
    'question_label': "Inferred: Response to Question 82B (No label provided in context)",
    'type': 'categorical',
    'value_labels': {'response_1': "Response 1 (Code 1)", 'response_2': "Response 2 (Code 2)", 'response_3': "Response 3 (Code 3)", 'response_4': "Response 4 (Code 4)"},
}
