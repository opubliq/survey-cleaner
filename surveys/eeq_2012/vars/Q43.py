# op_vote_intent — Vote intention (Inferred)
# Source: Q43
# Assumption: No codebook provided. Inferred type is categorical.
# Assumption: Codes 8.0/9.0 are missing/refused.
# TODO: verify mapping and standard name for Q43.
df_clean['op_vote_intent'] = df['Q43'].map({
    1.0: 'vote_party_a',
    2.0: 'vote_party_b',
    3.0: 'vote_party_c',
    4.0: 'vote_party_d',
    8.0: np.nan,
    9.0: np.nan,
})
CODEBOOK_VARIABLES['op_vote_intent'] = {
    'original_variable': 'Q43',
    'question_label': "Vote intention (Inferred)",
    'type': 'categorical',
    'value_labels': {'vote_party_a': "Party A", 'vote_party_b': "Party B", 'vote_party_c': "Party C", 'vote_party_d': "Party D"},
}
