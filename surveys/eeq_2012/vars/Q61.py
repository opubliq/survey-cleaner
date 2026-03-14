# op_q61 — Question 61 response
# Source: Q61
# Assumption: Codes 8.0 and 9.0 treated as missing (unlabelled in context)
df_clean['op_q61'] = df['Q61'].map({
    1.0: 'response_a',
    2.0: 'response_b',
    8.0: np.nan,
    9.0: np.nan,
})
CODEBOOK_VARIABLES['op_q61'] = {
    'original_variable': 'Q61',
    'question_label': "Question 61 response",
    'type': 'categorical',
    'value_labels': {'response_a': "Response A", 'response_b': "Response B"},
}
