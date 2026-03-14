# op_vote_intention — Intention de vote
# Source: q66
# Assumption: 1 and 2 are valid choices, 8 and 9 are missing codes based on typical survey structure when codebook is missing.
df_clean['op_vote_intention'] = df['q66'].map({
    '1': 'intention_a',
    '2': 'intention_b',
    '8': np.nan,
    '9': np.nan,
})
CODEBOOK_VARIABLES['op_vote_intention'] = {
    'original_variable': 'q66',
    'question_label': "Intention de vote (inferred)",
    'type': 'categorical',
    'value_labels': {'intention_a': "Intention Parti A", 'intention_b': "Intention Parti B"},
}