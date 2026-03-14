# behav_vote_intent — Vote intention or party supported
# Source: Q13
# Assumption: codes 8.0 and 9.0 treated as missing (unlabelled in data exploration)
df_clean['behav_vote_intent'] = df['Q13'].map({
    1.0: 'vote_party_a',
    2.0: 'vote_party_b',
    3.0: 'vote_party_c',
    4.0: 'vote_other',
    8.0: np.nan,
    9.0: np.nan,
})
CODEBOOK_VARIABLES['behav_vote_intent'] = {
    'original_variable': 'Q13',
    'question_label': "Vote intention or party supported (Placeholder)",
    'type': 'categorical',
    'value_labels': {'vote_party_a': "Party A", 'vote_party_b': "Party B", 'vote_party_c': "Party C", 'vote_other': "Other/Undecided"},
}