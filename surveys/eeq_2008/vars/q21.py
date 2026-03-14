# op_q21 — Generic question response for Q21
# Source: q21
# Assumption: Missing codes 8.0 and 9.0 are treated as NaN.
# Question label is inferred as it was not provided in context.
df_clean['op_q21'] = df['q21'].map({
    1.0: 'one',
    2.0: 'two',
    3.0: 'three',
    4.0: 'four',
    8.0: np.nan,
    9.0: np.nan,
})
CODEBOOK_VARIABLES['op_q21'] = {
    'original_variable': 'q21',
    'question_label': "Response to Question 21 (Label missing)",
    'type': 'categorical',
    'value_labels': {'one': "Response 1", 'two': "Response 2", 'three': "Response 3", 'four': "Response 4"},
}
