# op_vote_party — Vote intention at last election
# Source: Q8
# Assumption: Codes 1-4 map to placeholder parties. Codes 8 and 9 are treated as missing.
df_clean['op_vote_party'] = df['Q8'].map({
    1.0: 'party_a',
    2.0: 'party_b',
    3.0: 'party_c',
    4.0: 'party_d',
    8.0: np.nan,
    9.0: np.nan,
})
CODEBOOK_VARIABLES['op_vote_party'] = {
    'original_variable': 'Q8',
    'question_label': "Vote intention at last election",
    'type': 'categorical',
    'value_labels': {'party_a': "Party A", 'party_b': "Party B", 'party_c': "Party C", 'party_d': "Party D"},
}