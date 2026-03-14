# op_q77b — Unknown variable (defaulted to op_ prefix)
# Source: Q77B
# CRITICAL: No codebook entry provided. Labels for 1.0-4.0 are placeholder guesses.
# Assumption: Codes 8.0 and 9.0 (48 and 21 counts respectively) are unlabelled and treated as missing.
df_clean['op_q77b'] = df['Q77B'].map({
    1.0: 'value_1',
    2.0: 'value_2',
    3.0: 'value_3',
    4.0: 'value_4',
    8.0: np.nan,
    9.0: np.nan,
})
CODEBOOK_VARIABLES['op_q77b'] = {
    'original_variable': 'Q77B',
    'question_label': "Q77B - NOTE: Original question label is UNKNOWN",
    'type': 'categorical',
    'value_labels': {'value_1': 'Value 1 (Unknown)', 'value_2': 'Value 2 (Unknown)', 'value_3': 'Value 3 (Unknown)', 'value_4': 'Value 4 (Unknown)'},
}