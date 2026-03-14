# op_vote_choice — Inferred outcome of vote selection
# Source: Q56
# Assumption: Codes 1.0 and 2.0 are two main options. Codes 8.0/9.0 are missing.
df_clean['op_vote_choice'] = df['Q56'].map({
    1.0: 'option_a',
    2.0: 'option_b',
    8.0: np.nan,
    9.0: np.nan,
})
CODEBOOK_VARIABLES['op_vote_choice'] = {
    'original_variable': 'Q56',
    'question_label': "Inferred vote choice or outcome based on codes 1, 2, 8, 9.",
    'type': 'categorical',
    'value_labels': {'option_a': "Option A", 'option_b': "Option B"},
}