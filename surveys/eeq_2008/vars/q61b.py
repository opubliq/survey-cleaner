# op_vote_intention — Vote intention
# Source: q61b
# Assumption: Codes 1-5 are distinct choices, codes 96-99 are user/system missing codes.
# TODO: Verify meaning of codes 1-5 against the actual codebook for eeq_2008.
df_clean['op_vote_intention'] = df['q61b'].map({
    1.0: 'party_a',
    2.0: 'party_b',
    3.0: 'party_c',
    4.0: 'party_d',
    5.0: 'other',
    96.0: np.nan,
    97.0: np.nan,
    98.0: np.nan,
    99.0: np.nan,
})
CODEBOOK_VARIABLES['op_vote_intention'] = {
    'original_variable': 'q61b',
    'question_label': "Vote intention (Placeholder)",
    'type': 'categorical',
    'value_labels': {'party_a': "Party A (Placeholder)", 'party_b': "Party B (Placeholder)", 'party_c': "Party C (Placeholder)", 'party_d': "Party D (Placeholder)", 'other': "Other (Placeholder)"},
}
