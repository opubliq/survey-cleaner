# behav_vote_choice — Choice of vote in the 2008 election
# Source: q40
# Assumption: This mapping is a placeholder as data exploration failed. Codes 1-5 assumed for major parties, 99 for missing.
df_clean['behav_vote_choice'] = df['q40'].map({
    1.0: 'liberal',
    2.0: 'caq',
    3.0: 'pq',
    4.0: 'pc',
    5.0: 'ndp',
    99.0: np.nan,
})
CODEBOOK_VARIABLES['behav_vote_choice'] = {
    'original_variable': 'q40',
    'question_label': "Choice of vote in the 2008 election",
    'type': 'categorical',
    'value_labels': {'liberal': "Liberal", 'caq': "CAQ", 'pq': "PQ", 'pc': "PC", 'ndp': "NDP"},
}