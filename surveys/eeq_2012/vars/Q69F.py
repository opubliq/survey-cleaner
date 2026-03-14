# op_q69f — Inferred opinion variable
# Source: Q69F
# Note: Codebook entry was missing. Codes 1.0-6.0 mapped to generic responses.
# Assumption: Codes 95.0, 97.0, 98.0, 99.0 are treated as missing (unmapped).
df_clean['op_q69f'] = df['Q69F'].map({
    1.0: 'response_1',
    2.0: 'response_2',
    3.0: 'response_3',
    4.0: 'response_4',
    5.0: 'response_5',
    6.0: 'response_6',
    99.0: np.nan,
})
CODEBOOK_VARIABLES['op_q69f'] = {
    'original_variable': 'Q69F',
    'question_label': "Inferred Opinion Question (Codebook Missing)",
    'type': 'categorical',
    'value_labels': {'response_1': "Response 1", 'response_2': "Response 2", 'response_3': "Response 3", 'response_4': "Response 4", 'response_5': "Response 5", 'response_6': "Response 6"},
}