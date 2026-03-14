# behav_vote_intention — Vote intention
# Source: Q31
# Assumption: Codes 96, 97, 98, 99 treated as missing (unlabelled in codebook).
# Assumption: Codes 1-5 map to major Quebec parties in 2012 election context.
df_clean['behav_vote_intention'] = df['Q31'].map({
    1.0: 'bloc_quebecois',
    2.0: 'caq',
    3.0: 'liberal',
    4.0: 'péquiste',
    5.0: 'conservative',
    96.0: np.nan,
    97.0: np.nan,
    98.0: np.nan,
    99.0: np.nan,
})
CODEBOOK_VARIABLES['behav_vote_intention'] = {
    'original_variable': 'Q31',
    'question_label': "Which party do you intend to vote for?",
    'type': 'categorical',
    'value_labels': {'bloc_quebecois': "Bloc Québécois", 'caq': "CAQ", 'liberal': "Liberal", 'péquiste': "PQ", 'conservative': "Conservative"},
}