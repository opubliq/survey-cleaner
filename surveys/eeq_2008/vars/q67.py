# op_q67 — Inferred mapping for question 67
# Source: q67
# WARNING: Codebook entry was missing. Type inferred as categorical based on data structure.
# Assumption: Codes 8.0 and 9.0 are treated as missing (unlabelled in data exploration).
df_clean['op_q67'] = df['q67'].map({
    1.0: 'response_one',
    2.0: 'response_two',
    3.0: 'response_three',
    4.0: 'response_four',
    8.0: np.nan,
    9.0: np.nan,
})
CODEBOOK_VARIABLES['op_q67'] = {
    'original_variable': 'q67',
    'question_label': "Placeholder: Question 67 label unknown (Missing codebook info)",
    'type': 'categorical',
    'value_labels': {'response_one': "Response 1", 'response_two': "Response 2", 'response_three': "Response 3", 'response_four': "Response 4"},
}