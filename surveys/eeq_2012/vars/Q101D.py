# behav_vote_party — Binary choice for party affiliation
# Source: Q101D
# Assumption: Codes 1 and 2 are substantive answers. Codes 8 and 9 are treated as missing.
df_clean['behav_vote_party'] = df['Q101D'].map({
    1.0: 'party_a',
    2.0: 'party_b',
    8.0: np.nan,
    9.0: np.nan,
})
CODEBOOK_VARIABLES['behav_vote_party'] = {
    'original_variable': 'Q101D',
    'question_label': "Assumed: Vote choice between two main parties",
    'type': 'categorical',
    'value_labels': {'party_a': "Party A", 'party_b': "Party B"},
}