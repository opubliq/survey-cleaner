# op_q37 — Unknown opinion question 37
# Source: Q37
# Assumption: Codes 8.0/9.0 treated as missing (unlabelled in codebook)
df_clean['op_q37'] = df['Q37'].map({
    1.0: 'response_a',
    2.0: 'response_b',
    8.0: np.nan,
    9.0: np.nan,
})
CODEBOOK_VARIABLES['op_q37'] = {
    'original_variable': 'Q37',
    'question_label': "Q37 (Label unknown, derived from data)",
    'type': 'categorical',
    'value_labels': {'response_a': "Response A (Assumed)", 'response_b': "Response B (Assumed)"},
}
