# behav_vote_party — Party voted for
# Source: Q28
# Assumption: Codes 8.0 and 9.0 are system missing codes and mapped to np.nan.
# Assumption: Hypothetical value labels based on context: 1='liberal', 2='caq', 3='pq', 4='conservateur'
df_clean['behav_vote_party'] = df['Q28'].map({
    1.0: 'liberal',
    2.0: 'caq',
    3.0: 'pq',
    4.0: 'conservateur',
    8.0: np.nan,
    9.0: np.nan,
})
CODEBOOK_VARIABLES['behav_vote_party'] = {
    'original_variable': 'Q28',
    'question_label': "Party voted for (Inferred)",
    'type': 'categorical',
    'value_labels': {'liberal': "Liberal", 'caq': "CAQ", 'pq': "PQ", 'conservateur': "Conservateur"},
}