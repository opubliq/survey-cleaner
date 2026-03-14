# op_vote_intent — Vote intention
# Source: Q1
# Assumption: Codes 1-4 are parties, 8/9 are missing (unlabelled in initial context)
df_clean['op_vote_intent'] = df['Q1'].map({
    1.0: 'liberal',
    2.0: 'caq',
    3.0: 'pq',
    4.0: 'adq',
    8.0: np.nan,
    9.0: np.nan,
})
CODEBOOK_VARIABLES['op_vote_intent'] = {
    'original_variable': 'Q1',
    'question_label': "Vote intention",
    'type': 'categorical',
    'value_labels': {'liberal': "Liberal", 'caq': "CAQ", 'pq': "PQ", 'adq': "ADQ"},
}