# behav_vote_choice — Vote choice
# Source: Q35
# Assumption: Codes 8/9 are missing. Mapping to generic labels as no codebook was provided.
df_clean['behav_vote_choice'] = df['Q35'].map({
    1.0: 'party_a',
    2.0: 'party_b',
    3.0: 'party_c',
    4.0: 'party_d',
    8.0: np.nan,
    9.0: np.nan,
})
CODEBOOK_VARIABLES['behav_vote_choice'] = {
    'original_variable': 'Q35',
    'question_label': "Vote choice",
    'type': 'categorical',
    'value_labels': {'party_a': 'Choice 1', 'party_b': 'Choice 2', 'party_c': 'Choice 3', 'party_d': 'Choice 4'},
}