# op_q33d — Inferred categorical variable from Q33D
# Source: Q33D
# Assumption: Codes 8.0 and 9.0 are treated as missing as no codebook was provided.
# Assumption: Codes 1.0-4.0 mapped to generic options 'a' through 'd'.
df_clean['op_q33d'] = df['Q33D'].map({
    1.0: 'option_a',
    2.0: 'option_b',
    3.0: 'option_c',
    4.0: 'option_d',
    8.0: np.nan,
    9.0: np.nan,
})
CODEBOOK_VARIABLES['op_q33d'] = {
    'original_variable': 'Q33D',
    'question_label': "Q33D - Unknown question text (No codebook provided)",
    'type': 'categorical',
    'value_labels': {'option_a': "Code 1", 'option_b': "Code 2", 'option_c': "Code 3", 'option_d': "Code 4"},
}