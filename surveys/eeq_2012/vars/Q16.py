# op_q16 — Unknown question for Q16 - Inferred Categorical
# Source: Q16
# Assumption: Codes 1.0-6.0 mapped to generic string labels. Codes 96.0, 98.0, 99.0 treated as missing (np.nan).
df_clean['op_q16'] = df['Q16'].map({
    1.0: 'response_one',
    2.0: 'response_two',
    3.0: 'response_three',
    4.0: 'response_four',
    5.0: 'response_five',
    6.0: 'response_six',
    96.0: np.nan,
    98.0: np.nan,
    99.0: np.nan,
})
CODEBOOK_VARIABLES['op_q16'] = {
    'original_variable': 'Q16',
    'question_label': "Unknown question for Q16 - Inferred Categorical",
    'type': 'categorical',
    'value_labels': {'response_one': "Response 1", 'response_two': "Response 2", 'response_three': "Response 3", 'response_four': "Response 4", 'response_five': "Response 5", 'response_six': "Response 6"},
}