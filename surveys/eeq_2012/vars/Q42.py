# know_q42 — Unknown knowledge variable
# Source: Q42
# Assumption: Codes 1-4 mapped to generic responses. Codes 8/9 treated as missing based on data exploration.
df_clean['know_q42'] = df['Q42'].map({
    1.0: 'response_one',
    2.0: 'response_two',
    3.0: 'response_three',
    4.0: 'response_four',
    8.0: np.nan,
    9.0: np.nan,
})
CODEBOOK_VARIABLES['know_q42'] = {
    'original_variable': 'Q42',
    'question_label': "Question 42 (Mapping inferred from data)",
    'type': 'categorical',
    'value_labels': {'response_one': "Response 1", 'response_two': "Response 2", 'response_three': "Response 3", 'response_four': "Response 4"},
}